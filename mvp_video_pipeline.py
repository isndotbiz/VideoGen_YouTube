#!/usr/bin/env python3
"""
MVP end-to-end pipeline: URL → scrape → script → images → narration → video (optional YouTube upload).
Designed to run in under an hour using existing API keys from .env.
"""

import argparse
import json
import logging
import os
import subprocess
import textwrap
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv
import imageio_ffmpeg

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
IMAGES_DIR = OUTPUT_DIR / "generated_images"
LOGS_DIR = BASE_DIR / "logs"

for directory in (OUTPUT_DIR, IMAGES_DIR, LOGS_DIR):
    directory.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "mvp_pipeline.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("mvp_pipeline")


# ---------------------------------------------------------------------------
# Binaries
# ---------------------------------------------------------------------------
def ffmpeg_bin() -> str:
    """Return ffmpeg binary path (bundled via imageio_ffmpeg when available)."""
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def run_cmd(cmd: List[str], desc: str, timeout: int = 600) -> Tuple[bool, str]:
    """Run a command and capture stdout/stderr."""
    logger.info(f"[CMD] {desc}: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=BASE_DIR,
            timeout=timeout,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=False,
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        if result.returncode == 0:
            logger.info(f"[CMD] OK: {desc}")
            return True, stdout
        logger.error(f"[CMD] Failed ({result.returncode}): {desc}")
        if stdout:
            logger.error(stdout)
        if stderr:
            logger.error(stderr)
        return False, stderr or stdout
    except subprocess.TimeoutExpired:
        logger.error(f"[CMD] Timeout: {desc}")
        return False, "timeout"
    except Exception as exc:
        logger.error(f"[CMD] Error: {exc}")
        return False, str(exc)


def read_jsonl_record(path: Path) -> Dict:
    """Read the first JSONL record from a file."""
    if not path.exists():
        raise FileNotFoundError(f"JSONL not found: {path}")
    line = path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()[0]
    return json.loads(line)


# ---------------------------------------------------------------------------
# Phase 1: Scrape
# ---------------------------------------------------------------------------
def scrape_url(url: str) -> Dict:
    """Scrape a URL using the existing Node scraper."""
    ok, _ = run_cmd(["node", "scrape-and-convert.js", url], "Scrape article to dataset.jsonl")
    if not ok:
        raise RuntimeError("Scrape step failed")

    # Clean JSONL for consistent structure
    run_cmd(["node", "clean-jsonl.js", "dataset.jsonl"], "Clean JSONL")

    cleaned_path = BASE_DIR / "dataset.jsonl.cleaned"
    if cleaned_path.exists():
        logger.info("Using cleaned JSONL")
        return read_jsonl_record(cleaned_path)

    return read_jsonl_record(BASE_DIR / "dataset.jsonl")


# ---------------------------------------------------------------------------
# Phase 2: Script generation
# ---------------------------------------------------------------------------
def call_openrouter(prompt: str, model: Optional[str] = None) -> Optional[str]:
    """Call OpenRouter chat completion API and return message content."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None

    import requests

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model or os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an editor who turns an article into a 3-minute YouTube video script. "
                    "Keep it tight, factual, and engaging. Return JSON with fields: "
                    "`title`, `summary`, and `sections` (each section has `heading`, "
                    "`narration` ~80-120 words, and `image_prompt` describing a cinematic still)."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=90,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def build_script(article: Dict, use_openrouter: bool = True) -> Dict:
    """Generate a structured script dict."""
    article_text = article.get("content", "")
    clipped = article_text[:4000]

    if use_openrouter:
        try:
            prompt = (
                f"Article title: {article.get('title')}\n"
                f"URL: {article.get('url')}\n"
                f"Article excerpt (truncated to 4000 chars):\n{clipped}"
            )
            content = call_openrouter(prompt)
            if content:
                script = json.loads(content)
                logger.info("Script generated via OpenRouter")
                return script
        except Exception as exc:
            logger.warning(f"OpenRouter generation failed, falling back. Reason: {exc}")

    # Fallback: simple template based on content chunks
    paragraphs = [p.strip() for p in clipped.split("\n") if p.strip()]
    chunks = [" ".join(paragraphs[i : i + 2]) for i in range(0, len(paragraphs), 2)]
    sections = []
    for idx, chunk in enumerate(chunks[:4]):
        sections.append(
            {
                "heading": f"Key Point {idx + 1}",
                "narration": textwrap.shorten(chunk, width=320, placeholder="..."),
                "image_prompt": f"Cinematic photo representing: {chunk[:120]}",
            }
        )

    if not sections:
        sections = [
            {
                "heading": "Overview",
                "narration": textwrap.shorten(clipped, width=320, placeholder="..."),
                "image_prompt": "Cinematic tech workspace with article highlights on screen",
            }
        ]

    logger.info("Script generated via fallback template")
    return {
        "title": article.get("title", "Generated Video"),
        "summary": article.get("description", "") or sections[0]["narration"],
        "sections": sections,
    }


def render_tts_text(script: Dict) -> str:
    """Flatten script into narration text."""
    lines = [f"{script.get('title', '')}"]
    for section in script.get("sections", []):
        lines.append(section.get("heading", ""))
        lines.append(section.get("narration", ""))
    full_text = "\n\n".join(line for line in lines if line)

    # Target ~3 minute read (~450 words at 150 wpm)
    target_words = int(os.getenv("TARGET_TTS_WORDS", "450"))
    words = full_text.split()
    if len(words) > target_words:
        trimmed = " ".join(words[:target_words])
        logger.info(f"[TTS] Trimming narration from {len(words)} to {target_words} words for ~3min duration")
        return trimmed

    return full_text


def generate_srt_from_script(script: Dict, audio_duration: float) -> Path:
    """
    Create a simple SRT file by evenly distributing section durations across the audio length.
    This is a heuristic to allow captions without TTS word-level timestamps.
    """
    sections = script.get("sections", [])
    if not sections:
        return Path()

    per_section = audio_duration / len(sections)

    def fmt(ts: float) -> str:
        hrs = int(ts // 3600)
        mins = int((ts % 3600) // 60)
        secs = int(ts % 60)
        ms = int((ts - int(ts)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

    srt_lines = []
    current = 0.0
    for idx, section in enumerate(sections, start=1):
        start = current
        end = min(audio_duration, current + per_section)
        text = section.get("narration") or section.get("heading") or "Section"
        srt_lines.append(f"{idx}")
        srt_lines.append(f"{fmt(start)} --> {fmt(end)}")
        srt_lines.append(text.strip())
        srt_lines.append("")
        current = end

    srt_path = OUTPUT_DIR / "captions.srt"
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
    logger.info(f"[SUBS] Wrote SRT captions to {srt_path}")
    return srt_path


def build_infographic_prompts(script: Dict, max_items: int = 3) -> List[str]:
    prompts = []
    sections = script.get("sections", [])[:max_items]
    for sec in sections:
        heading = sec.get("heading", "Key Point")
        prompts.append(
            f"Professional infographic, 16:9, clear typography, minimal colors, heading '{heading}', "
            "bullet list of key takeaways, simple icons, clean grid layout, readable at 1080p."
        )
    if not prompts:
        prompts.append(
            "Professional infographic, 16:9, key insights summary, bullet list, clean typography, readable at 1080p."
        )
    return prompts


def generate_seo_metadata(script: Dict, url: str) -> Dict:
    title = script.get("title") or "AI Generated Video"
    sections = script.get("sections", [])
    tags = list({w.strip("#").lower() for sec in sections for w in (sec.get("heading", "") + " " + sec.get("narration", "")).split() if len(w) > 4})
    tags = tags[:30]

    description_lines = [title, "", f"Source: {url}", ""]
    current = 0
    for sec in sections:
        description_lines.append(f"[{current//60:02d}:{current%60:02d}] {sec.get('heading','Section')}")
        current += 30
    description_lines.append("\nIf you enjoyed this, like and subscribe for more.")

    return {
        "title": title[:95],
        "description": "\n".join(description_lines)[:4800],
        "tags": tags,
        "chapters": [s.get("heading", "Section") for s in sections],
    }


# ---------------------------------------------------------------------------
# Phase 3: Image generation (FAL.ai)
# ---------------------------------------------------------------------------
def generate_images(image_prompts: List[str]) -> List[Path]:
    """Generate images via FAL.ai Flux. Falls back to solid frames if unavailable."""
    generated: List[Path] = []
    manifest_entries = []
    api_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")

    try:
        import fal_client  # type: ignore
        import requests
    except Exception:
        api_key = None

    if not api_key:
        logger.warning("FAL_API_KEY missing or fal_client unavailable; creating placeholders.")
        return create_placeholder_images(len(image_prompts) or 1)

    os.environ["FAL_KEY"] = api_key

    for idx, prompt in enumerate(image_prompts, start=1):
        try:
            logger.info(f"[FAL] Generating image {idx}/{len(image_prompts)}")
            result = fal_client.run(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": prompt,
                    "seed": 1234 + idx,
                    "image_size": "landscape_16_9",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                },
            )

            img_url = result.get("images", [{}])[0].get("url")
            if not img_url:
                raise RuntimeError("No image URL returned from FAL")

            response = requests.get(img_url, timeout=60)
            response.raise_for_status()

            img_path = IMAGES_DIR / f"scene_{idx:02d}.png"
            img_path.write_bytes(response.content)
            generated.append(img_path)
            manifest_entries.append(
                {
                    "id": f"scene_{idx:02d}",
                    "prompt": prompt,
                    "model": "fal-ai/flux/dev",
                    "url": img_url,
                    "path": str(img_path),
                }
            )
            logger.info(f"[FAL] Saved {img_path.name} ({len(response.content)} bytes)")

        except Exception as exc:
            logger.error(f"[FAL] Failed to generate image {idx}: {exc}")

    if not generated:
        placeholders = create_placeholder_images(len(image_prompts) or 1)
        save_asset_manifest([], placeholders)
        return placeholders

    save_asset_manifest(manifest_entries, generated)
    return generated


def generate_nano_banana_images(prompts: List[str]) -> List[Path]:
    """Generate infographic/text images using FAL Nano Banana."""
    generated: List[Path] = []
    manifest_entries = []
    api_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
    if not api_key:
        logger.warning("[NANO] FAL_API_KEY missing; skipping Nano Banana images.")
        return generated
    try:
        import fal_client  # type: ignore
        import requests
    except Exception:
        logger.warning("[NANO] fal_client missing; skipping Nano Banana images.")
        return generated

    os.environ["FAL_KEY"] = api_key
    for idx, prompt in enumerate(prompts, start=1):
        try:
            logger.info(f"[NANO] Generating infographic {idx}/{len(prompts)}")
            result = fal_client.run(
                "fal-ai/nano-banana",
                arguments={
                    "prompt": prompt,
                    "image_size": "landscape_16_9",
                },
            )
            img_url = result.get("images", [{}])[0].get("url")
            if not img_url:
                raise RuntimeError("No image URL returned from Nano Banana")
            response = requests.get(img_url, timeout=60)
            response.raise_for_status()
            img_path = IMAGES_DIR / f"nano_{idx:02d}.png"
            img_path.write_bytes(response.content)
            generated.append(img_path)
            manifest_entries.append(
                {
                    "id": f"nano_{idx:02d}",
                    "prompt": prompt,
                    "model": "fal-ai/nano-banana",
                    "url": img_url,
                    "path": str(img_path),
                }
            )
            logger.info(f"[NANO] Saved {img_path.name} ({len(response.content)} bytes)")
        except Exception as exc:
            logger.error(f"[NANO] Failed to generate infographic {idx}: {exc}")

    if manifest_entries:
        append_asset_manifest(manifest_entries)

    return generated


def create_placeholder_images(count: int) -> List[Path]:
    """Create simple placeholder frames when image generation fails."""
    from moviepy.editor import ColorClip

    paths: List[Path] = []
    for idx in range(count):
        clip = ColorClip(size=(1920, 1080), color=(40 + idx * 10 % 200, 60, 90))
        img_path = IMAGES_DIR / f"placeholder_{idx+1:02d}.png"
        clip.save_frame(str(img_path))
        paths.append(img_path)
    logger.info(f"Created {len(paths)} placeholder image(s)")
    return paths


def save_asset_manifest(entries: List[Dict], image_paths: List[Path]):
    """Persist generated asset metadata for downstream tools (Runway, Descript, etc.)."""
    manifest = {
        "images": entries,
        "local_paths": [str(p) for p in image_paths],
        "timestamp": time.time(),
    }
    manifest_path = OUTPUT_DIR / "generated_assets.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    logger.info(f"[ASSETS] Saved manifest to {manifest_path}")


def append_asset_manifest(entries: List[Dict]):
    """Append new entries to existing manifest (if any)."""
    manifest_path = OUTPUT_DIR / "generated_assets.json"
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text())
        except Exception:
            data = {}
    else:
        data = {}
    images = data.get("images", [])
    images.extend(entries)
    data["images"] = images
    manifest_path.write_text(json.dumps(data, indent=2))
    logger.info(f"[ASSETS] Appended {len(entries)} entries to manifest")


def load_asset_entries() -> List[Dict]:
    manifest_path = OUTPUT_DIR / "generated_assets.json"
    if manifest_path.exists():
        try:
            data = json.loads(manifest_path.read_text())
            return data.get("images", [])
        except Exception:
            return []
    return []


# ---------------------------------------------------------------------------
# Phase 4: Narration (ElevenLabs)
# ---------------------------------------------------------------------------
def _elevenlabs_tts(text: str, output_path: Path) -> Path:
    """Low-level ElevenLabs call so we can retry with shorter text if needed."""
    from elevenlabs import ElevenLabs

    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Rachel
    model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_monolingual_v1")

    logger.info(f"[TTS] Generating narration with voice {voice_id}")
    audio_stream = client.text_to_speech.convert(text=text[:6000], voice_id=voice_id, model_id=model_id)

    bytes_written = 0
    with open(output_path, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
                bytes_written += len(chunk)

    logger.info(f"[TTS] Saved {output_path.name} ({bytes_written} bytes)")
    return output_path


def _gtts_fallback(text: str, output_path: Path) -> Optional[Path]:
    """Try gTTS when ElevenLabs quota is exhausted."""
    try:
        from gtts import gTTS  # type: ignore

        tts = gTTS(text)
        tts.save(str(output_path))
        logger.info("[TTS] gTTS fallback succeeded")
        return output_path
    except Exception as exc:
        logger.warning(f"[TTS] gTTS fallback failed: {exc}")
        return None


def generate_narration(text: str) -> Path:
    """Generate narration audio via ElevenLabs; retry shorter text if quota tight."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    audio_path = OUTPUT_DIR / "narration.mp3"

    if not api_key:
        logger.warning("ELEVENLABS_API_KEY missing; creating silent placeholder narration.")
        return create_silent_audio(text)

    words = text.split()
    try:
        return _elevenlabs_tts(text, audio_path)
    except Exception as exc:
        message = str(exc).lower()
        logger.error(f"[TTS] Failed to generate narration ({exc})")

        # Quota exceeded: try again with a shorter script (~35% length)
        if "quota" in message or "credit" in message:
            # First preference: keep length by switching to gTTS
            gtts_full = _gtts_fallback(" ".join(words[:800]), audio_path)
            if gtts_full:
                return gtts_full

            shorter = " ".join(words[: max(30, int(len(words) * 0.35))])
            if len(shorter.split()) < len(words):
                logger.info("[TTS] Retrying ElevenLabs with shorter script to fit remaining credits")
                try:
                    return _elevenlabs_tts(shorter, audio_path)
                except Exception as exc2:
                    logger.error(f"[TTS] Retry failed: {exc2}")

        # Last-ditch: gTTS
        gtts_path = _gtts_fallback(" ".join(words[:500]), audio_path)
        if gtts_path:
            return gtts_path

        logger.error("[TTS] Falling back to silent placeholder narration.")
        return create_silent_audio(text)


def create_silent_audio(text: str, output_path: Optional[Path] = None) -> Path:
    """Create a silent audio placeholder matching approximate speech duration."""
    import wave
    import struct

    output_path = output_path or OUTPUT_DIR / "narration.wav"
    output_path = output_path.with_suffix(".wav")

    words = max(len(text.split()), 1)
    duration_seconds = max(int(words / 2.5), 30)  # ~150 wpm, minimum 30s

    sample_rate = 16000
    n_frames = duration_seconds * sample_rate

    with wave.open(str(output_path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        silence_frame = struct.pack("<h", 0)
        wf.writeframes(silence_frame * n_frames)

    logger.info(f"[AUDIO] Created silent placeholder narration ({duration_seconds}s) at {output_path}")
    return output_path


def mix_audio(narration_path: Path, music_path: Path, music_db: float = -18.0) -> Path:
    """Mix narration with background music using ffmpeg if available."""
    mixed_path = OUTPUT_DIR / "narration_with_bgm.mp3"
    cmd = [
        ffmpeg_bin(),
        "-y",
        "-i",
        str(narration_path),
        "-i",
        str(music_path),
        "-filter_complex",
        f"[1:a]volume={music_db}dB[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2",
        "-c:a",
        "mp3",
        str(mixed_path),
    ]
    ok, _ = run_cmd(cmd, "ffmpeg audio mix", timeout=120)
    if not ok:
        raise RuntimeError("ffmpeg mix failed")
    return mixed_path


def generate_placeholder_bgm(duration_seconds: float) -> Path:
    """
    Generate a simple low-volume background tone using ffmpeg lavfi.
    Avoids external downloads while providing filler music.
    """
    bgm_path = OUTPUT_DIR / "placeholder_bgm.mp3"
    cmd = [
        ffmpeg_bin(),
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=440:duration={int(duration_seconds)}:sample_rate=44100",
        "-filter:a",
        "volume=-25dB",
        str(bgm_path),
    ]
    ok, _ = run_cmd(cmd, "ffmpeg generate placeholder bgm", timeout=120)
    if not ok:
        raise RuntimeError("bgm generation failed")
    return bgm_path


def generate_runway_clips(image_entries: List[Dict], motion_prompt: str = "Cinematic pan and subtle zoom, 3 seconds") -> List[Path]:
    """
    Generate short clips from images using Runway image_to_video.
    Returns list of downloaded mp4 paths.
    """
    api_key = os.getenv("RUNWAY_API_KEY")
    if not api_key:
        logger.warning("[RUNWAY] RUNWAY_API_KEY missing; skipping Runway clips.")
        return []

    import requests

    output_dir = OUTPUT_DIR / "runway_videos"
    output_dir.mkdir(parents=True, exist_ok=True)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    clip_paths: List[Path] = []

    for idx, entry in enumerate(image_entries, start=1):
        img_url = entry.get("url")
        if not img_url:
            continue
        payload = {
            "model": "gen3",
            "prompt_image": img_url,
            "prompt_text": entry.get("prompt", motion_prompt),
            "duration": 3,
            "watermark": False,
        }
        try:
            logger.info(f"[RUNWAY] Submitting clip {idx} from image {img_url}")
            resp = requests.post("https://api.runwayml.com/v1/image_to_video", headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            task_id = resp.json().get("id")
            if not task_id:
                raise RuntimeError("No task id returned")

            # Poll
            status = "PENDING"
            start_poll = time.time()
            video_url = None
            while status not in ("COMPLETED", "FAILED") and time.time() - start_poll < 240:
                poll = requests.get(f"https://api.runwayml.com/v1/tasks/{task_id}", headers=headers, timeout=15)
                poll.raise_for_status()
                data = poll.json()
                status = data.get("status")
                if status == "COMPLETED":
                    video_url = data.get("output", {}).get("video")
                    break
                time.sleep(3)

            if status != "COMPLETED" or not video_url:
                logger.warning(f"[RUNWAY] Task {task_id} did not complete: {status}")
                continue

            # Download video
            vid_resp = requests.get(video_url, timeout=120)
            vid_resp.raise_for_status()
            clip_path = output_dir / f"runway_clip_{idx:02d}.mp4"
            clip_path.write_bytes(vid_resp.content)
            clip_paths.append(clip_path)
            logger.info(f"[RUNWAY] Saved {clip_path}")
        except Exception as exc:
            logger.error(f"[RUNWAY] Failed clip {idx}: {exc}")

    return clip_paths


# ---------------------------------------------------------------------------
# Phase 5: Assembly (MoviePy)
# ---------------------------------------------------------------------------
def assemble_video(image_paths: List[Path], narration_path: Path, title: str) -> Path:
    """Assemble a simple slideshow video with narration."""
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
    from PIL import Image

    # Normalize image sizes
    uniform_dir = OUTPUT_DIR / "temp_uniform_images"
    uniform_dir.mkdir(parents=True, exist_ok=True)
    target_size = None
    uniform_paths = []
    for idx, img_path in enumerate(image_paths, start=1):
        with Image.open(img_path) as im:
            if target_size is None:
                target_size = im.size
            resized = im.resize(target_size)
            out_path = uniform_dir / f"uniform_{idx:02d}.png"
            resized.save(out_path)
            uniform_paths.append(out_path)

    audio_clip = AudioFileClip(str(narration_path))
    duration = audio_clip.duration
    per_image = max(duration / max(len(uniform_paths), 1), 3.0)

    clip = ImageSequenceClip([str(p) for p in uniform_paths], durations=[per_image] * len(uniform_paths))
    if hasattr(clip, "resized"):
        clip = clip.resized(height=1080)
    if hasattr(clip, "with_audio"):
        clip = clip.with_audio(audio_clip)

    output_path = OUTPUT_DIR / "final_video.mp4"
    logger.info("[VIDEO] Rendering final_video.mp4 ... this may take a minute")
    clip.write_videofile(
        str(output_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
    )
    logger.info("[VIDEO] Video render complete")
    return output_path


# ---------------------------------------------------------------------------
# Phase 6: YouTube upload (optional)
# ---------------------------------------------------------------------------
def upload_to_youtube(video_path: Path, title: str, description: str):
    """Upload video via existing uploader (requires OAuth)."""
    try:
        from upload_to_youtube import upload_video
    except Exception as exc:
        logger.error(f"Upload module not available: {exc}")
        return False

    tags = [w for w in title.split() if len(w) > 3][:10]
    return upload_video(
        video_path=str(video_path),
        title=title[:95],
        description=description[:4500],
        tags=tags,
        privacy="unlisted",
    )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def run_pipeline(url: str, upload: bool = False, skip_openrouter: bool = False):
    start = time.time()
    logger.info("=" * 70)
    logger.info("MVP VIDEO PIPELINE START")
    logger.info("=" * 70)

    article = scrape_url(url)
    script = build_script(article, use_openrouter=not skip_openrouter)
    narration_text = render_tts_text(script)

    image_prompts = [s.get("image_prompt", "") for s in script.get("sections", []) if s.get("image_prompt")]
    if not image_prompts:
        image_prompts = ["Cinematic tech workspace, soft lighting, shallow depth of field"]

    images = generate_images(image_prompts)

    # Infographics via Nano Banana
    nano_prompts = build_infographic_prompts(script, max_items=3)
    nano_images = generate_nano_banana_images(nano_prompts)
    if nano_images:
        images.extend(nano_images)

    narration_path = generate_narration(narration_text)

    audio_duration = None
    try:
        from mutagen import File  # type: ignore

        audio_info = File(str(narration_path))
        if audio_info and getattr(audio_info, "info", None):
            audio_duration = getattr(audio_info.info, "length", None)
    except Exception as exc:
        logger.warning(f"[AUDIO] Could not read narration duration via mutagen: {exc}")

    if audio_duration is None:
        try:
            from moviepy.audio.io.AudioFileClip import AudioFileClip

            with AudioFileClip(str(narration_path)) as clip_duration:
                audio_duration = clip_duration.duration
        except Exception as exc:
            logger.warning(f"[AUDIO] Could not read narration duration via moviepy: {exc}")

    if audio_duration is None:
        audio_duration = max(len(narration_text.split()) / 2.5, 30)  # fallback estimate
        logger.info(f"[AUDIO] Using estimated duration {audio_duration:.1f}s based on script length")

    # Background music (env BGM_PATH or generated placeholder)
    bgm_env = os.getenv("BGM_PATH")
    bgm_path = None
    if bgm_env and Path(bgm_env).exists():
        bgm_path = Path(bgm_env)
    elif audio_duration:
        try:
            bgm_path = generate_placeholder_bgm(audio_duration)
        except Exception as exc:
            logger.warning(f"[AUDIO] Placeholder bgm failed: {exc}")

    mixed_audio = narration_path
    if bgm_path:
        try:
            mixed_audio = mix_audio(narration_path, bgm_path)
        except Exception as exc:
            logger.warning(f"[AUDIO] Mix failed, using narration only: {exc}")

    video_path = assemble_video(images, mixed_audio, script.get("title", "Generated Video"))

    # Generate simple SRT captions based on section splits
    srt_path = Path()
    try:
        if audio_duration:
            srt_path = generate_srt_from_script(script, audio_duration)
    except Exception as exc:
        logger.warning(f"[SUBS] Could not create SRT: {exc}")

    # Burn subtitles if available
    burned_path = video_path
    if srt_path and srt_path.exists():
        burned_path = OUTPUT_DIR / "final_video_subbed.mp4"
        vf_path = srt_path.as_posix()
        vf_escaped = vf_path.replace(":", "\\:").replace("'", "\\'")
        in_path = video_path.as_posix()
        cmd = [
            ffmpeg_bin(),
            "-y",
            "-i",
            in_path,
            "-vf",
            f"subtitles='{vf_escaped}'",
            "-c:a",
            "copy",
            str(burned_path),
        ]
        ok, _ = run_cmd(cmd, "ffmpeg burn subtitles", timeout=300)
        if not ok:
            burned_path = video_path

    # Runway clips (optional)
    runway_clips = []
    manifest_entries = load_asset_entries()
    if manifest_entries:
        runway_clips = generate_runway_clips(manifest_entries)

    upload_result = None
    if upload:
        logger.info("[YOUTUBE] Uploading video...")
        upload_result = upload_to_youtube(burned_path, script.get("title", ""), script.get("summary", ""))
        logger.info(f"[YOUTUBE] Upload status: {'SUCCESS' if upload_result else 'FAILED'}")

    # SEO metadata
    seo_meta = generate_seo_metadata(script, url)
    (OUTPUT_DIR / "seo_metadata.json").write_text(json.dumps(seo_meta, indent=2), encoding="utf-8")

    # Cost estimate
    flux_count = len([p for p in images if "nano_" not in p.name])
    nano_count = len([p for p in images if "nano_" in p.name])
    runway_count = len(runway_clips)
    flux_cost = flux_count * float(os.getenv("COST_FLUX", "0.06"))
    nano_cost = nano_count * float(os.getenv("COST_NANO", "0.03"))
    runway_cost = runway_count * float(os.getenv("COST_RUNWAY", "0.08"))
    audio_minutes = (audio_duration or 0) / 60 if audio_duration else 0
    eleven_cost = audio_minutes * float(os.getenv("COST_ELEVEN_PER_MIN", "0.02"))
    total_cost = flux_cost + nano_cost + runway_cost + eleven_cost

    elapsed = time.time() - start
    logger.info(f"Pipeline complete in {elapsed/60:.1f} minutes")
    return {
        "video_path": str(burned_path),
        "n_images": len(images),
        "upload": upload_result,
        "duration_minutes": elapsed / 60,
        "cost_estimate": {
            "flux_images": flux_cost,
            "nano_images": nano_cost,
            "runway_clips": runway_cost,
            "elevenlabs": eleven_cost,
            "total": total_cost,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run MVP end-to-end video pipeline")
    parser.add_argument("url", help="Article URL to convert into a video")
    parser.add_argument("--upload", action="store_true", help="Upload to YouTube after rendering")
    parser.add_argument(
        "--no-openrouter",
        action="store_true",
        help="Skip OpenRouter and use fallback templating for script",
    )
    args = parser.parse_args()

    result = run_pipeline(args.url, upload=args.upload, skip_openrouter=args.no_openrouter)
    logger.info(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
