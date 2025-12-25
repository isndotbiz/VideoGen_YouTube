#!/usr/bin/env python3
"""
PRODUCTION VIDEO PIPELINE - 6 Minute Videos
Uses: Flux.1 Pro (images), Nano Banana Pro (infographics), WAN (videos)
Background music at 10-15% volume from Moderate-Recommended folder
"""
import os
import sys
import json
import time
import fal_client
import requests
from pathlib import Path
from config import APIConfig

# Configure FAL client
os.environ["FAL_KEY"] = APIConfig.FAL_API_KEY

# CLEAN SCRIPT FOR 6-MINUTE VIDEO (NO INSTRUCTIONS, ONLY NARRATION)
# This is the FIRST 30 SECONDS for testing
SCRIPT_SEGMENT_1 = """
Welcome to the ultimate guide to free AI tools that are transforming how we work in 2025.
In the next six minutes, you'll discover eight powerful tools that can save you thousands of dollars
and countless hours every single month.

These aren't just simple utilities. These are game-changing AI platforms that professionals are using
right now to automate their workflows, create stunning content, and solve complex problems in seconds.

Let's dive into the first tool that's revolutionizing how we interact with artificial intelligence.
"""

# Full 6-minute script sections
FULL_SCRIPT_SECTIONS = {
    "intro": {
        "text": SCRIPT_SEGMENT_1,
        "duration": 30,
        "visuals": [
            {"type": "infographic", "content": "Title card: 8 Free AI Tools 2025"},
            {"type": "video", "content": "Dynamic montage of AI interfaces"},
        ]
    },
    "tool_1_chatgpt": {
        "text": """
First up is ChatGPT, the conversational AI that's become essential for millions of users worldwide.
Whether you're writing code, drafting emails, analyzing data, or brainstorming ideas, ChatGPT handles it all.
The free tier gives you access to GPT-3.5, which is more than capable for most tasks.
You can generate content, debug code, translate languages, and even create structured data formats.
What makes ChatGPT special is its ability to understand context and maintain conversation flow.
""",
        "duration": 30,
        "visuals": [
            {"type": "image", "content": "ChatGPT interface clean UI"},
            {"type": "infographic", "content": "ChatGPT key features list"},
            {"type": "video", "content": "ChatGPT conversation demo"},
        ]
    },
    "tool_2_midjourney": {
        "text": """
Next is Midjourney, the AI image generator that's pushing the boundaries of digital art.
With just a text prompt, you can create photorealistic images, stunning artwork, or professional graphics.
The free trial gives you 25 image generations to explore what's possible.
Artists, designers, and marketers are using Midjourney to create everything from product mockups to book covers.
The quality is so high that many AI-generated images are indistinguishable from professional photography.
""",
        "duration": 30,
        "visuals": [
            {"type": "video", "content": "Midjourney image generation process"},
            {"type": "image", "content": "Gallery of AI-generated artwork"},
            {"type": "infographic", "content": "Midjourney use cases"},
        ]
    },
    # Additional sections truncated for first test
}

class ProductionPipeline:
    def __init__(self, test_mode=True):
        self.test_mode = test_mode
        self.output_dir = Path("output/production_6min" if not test_mode else "output/production_test_30sec")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.visuals_dir = self.output_dir / "visuals"
        self.visuals_dir.mkdir(exist_ok=True)

        self.music_dir = Path("background_music/Moderate-Recommended")

        print("\n" + "="*80)
        print("PRODUCTION VIDEO PIPELINE")
        print("="*80)
        print(f"Mode: {'TEST (30 seconds)' if test_mode else 'FULL (6 minutes)'}")
        print(f"Output: {self.output_dir}")
        print("="*80)

    def select_background_music(self):
        """Select best background music track"""
        print("\n[1/6] Selecting Background Music...")
        print("-" * 80)

        # Use a calm, professional track
        music_files = list(self.music_dir.glob("*.wav"))

        if not music_files:
            print(f"[ERROR] No music files found in {self.music_dir}")
            return None

        # Prefer "Drifting Valleys" or "Autodidact" for professional content
        preferred = ["Drifting Valleys", "Autodidact", "Cruise Control"]

        selected = None
        for pref in preferred:
            for music in music_files:
                if pref in music.name:
                    selected = music
                    break
            if selected:
                break

        if not selected:
            selected = music_files[0]

        print(f"[OK] Selected: {selected.name}")
        print(f"[SIZE] {selected.stat().st_size / 1024 / 1024:.1f} MB")

        return selected

    def generate_narration(self, script_text):
        """Generate clean narration (no instructions, only the text)"""
        print("\n[2/6] Generating Narration...")
        print("-" * 80)

        narration_file = self.output_dir / "narration.mp3"

        # Clean the script - remove any stage directions or instructions
        clean_script = script_text.strip()

        # Verify no instructions are in the script
        forbidden_words = ["[", "]", "INSTRUCTION", "NOTE:", "TODO:", "STAGE:"]
        for word in forbidden_words:
            if word in clean_script:
                print(f"[WARNING] Found instruction marker '{word}' in script!")
                print("[INFO] Removing instruction markers...")
                clean_script = clean_script.replace(word, "")

        word_count = len(clean_script.split())
        print(f"[SCRIPT] {word_count} words (clean)")
        print(f"[PREVIEW] {clean_script[:100]}...")

        try:
            from elevenlabs.client import ElevenLabs

            client = ElevenLabs(api_key=APIConfig.ELEVENLABS_API_KEY)

            print(f"[API] ElevenLabs")
            print(f"[VOICE] Sarah (Professional)")

            # Generate with professional settings
            audio = client.text_to_speech.convert(
                voice_id="EXAVITQu4vr4xnSDxMaL",  # Sarah
                text=clean_script,
                model_id="eleven_turbo_v2"
            )

            # Save
            with open(narration_file, 'wb') as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)

            size = narration_file.stat().st_size / 1024 / 1024
            print(f"[OK] Narration saved: {narration_file}")
            print(f"[SIZE] {size:.2f} MB")

            # Verify duration
            import subprocess
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', str(narration_file)],
                capture_output=True, text=True
            )

            if result.returncode == 0:
                duration = float(result.stdout.strip())
                print(f"[DURATION] {duration:.1f} seconds")

                if duration > 35 and self.test_mode:
                    print(f"[WARNING] Narration is {duration:.1f}s (expected ~30s)")
                    print("[INFO] This is OK for testing")

            return narration_file

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def generate_visuals_with_fal(self, segment_info):
        """Generate visuals using FAL.ai (Flux.1 Pro, Nano Banana Pro, WAN)"""
        print("\n[3/6] Generating Visuals with FAL.ai...")
        print("-" * 80)

        visuals = []

        for i, visual in enumerate(segment_info.get('visuals', []), 1):
            visual_type = visual['type']
            content = visual['content']

            print(f"\n[{i}/{len(segment_info['visuals'])}] {visual_type.upper()}: {content}")

            try:
                if visual_type == "image":
                    # Use Flux.1 Pro for high-quality images
                    print(f"  [MODEL] Flux.1 Pro")
                    result = fal_client.subscribe(
                        "fal-ai/flux-pro/v1.1",
                        arguments={
                            "prompt": content,
                            "image_size": "landscape_16_9",
                            "num_inference_steps": 28,
                            "guidance_scale": 3.5,
                            "num_images": 1,
                            "enable_safety_checker": True,
                        }
                    )

                    if result and 'images' in result:
                        image_url = result['images'][0]['url']
                        response = requests.get(image_url)

                        if response.status_code == 200:
                            file_path = self.visuals_dir / f"visual_{i:02d}_image.jpg"
                            with open(file_path, 'wb') as f:
                                f.write(response.content)

                            print(f"  [OK] Saved: {file_path.name}")
                            visuals.append({
                                'file': file_path,
                                'type': 'image',
                                'duration': 3
                            })

                elif visual_type == "infographic":
                    # Use Nano Banana Pro for infographics
                    print(f"  [MODEL] Nano Banana Pro (Infographic)")
                    result = fal_client.subscribe(
                        "fal-ai/nano-banana-pro",
                        arguments={
                            "prompt": content,
                            "image_size": "landscape_16_9",
                            "num_inference_steps": 4,
                            "num_images": 1,
                        }
                    )

                    if result and 'images' in result:
                        image_url = result['images'][0]['url']
                        response = requests.get(image_url)

                        if response.status_code == 200:
                            file_path = self.visuals_dir / f"visual_{i:02d}_infographic.jpg"
                            with open(file_path, 'wb') as f:
                                f.write(response.content)

                            print(f"  [OK] Saved: {file_path.name}")
                            visuals.append({
                                'file': file_path,
                                'type': 'infographic',
                                'duration': 5
                            })

                elif visual_type == "video":
                    # Generate image first, then use WAN for video
                    print(f"  [MODEL] WAN (Image-to-Video)")

                    # First generate a base image with Flux
                    image_result = fal_client.subscribe(
                        "fal-ai/flux-pro/v1.1",
                        arguments={
                            "prompt": content,
                            "image_size": "landscape_16_9",
                            "num_images": 1,
                        }
                    )

                    if image_result and 'images' in image_result:
                        image_url = image_result['images'][0]['url']

                        # Now convert to video with WAN
                        video_result = fal_client.subscribe(
                            "fal-ai/wan-25-preview/image-to-video",
                            arguments={
                                "image_url": image_url,
                                "prompt": content,
                            }
                        )

                        if video_result and 'video' in video_result:
                            video_url = video_result['video']['url']
                            response = requests.get(video_url)

                            if response.status_code == 200:
                                file_path = self.visuals_dir / f"visual_{i:02d}_video.mp4"
                                with open(file_path, 'wb') as f:
                                    f.write(response.content)

                                print(f"  [OK] Saved: {file_path.name}")
                                visuals.append({
                                    'file': file_path,
                                    'type': 'video',
                                    'duration': 5
                                })

                # Small delay to avoid rate limits
                time.sleep(2)

            except Exception as e:
                print(f"  [ERROR] {str(e)}")
                continue

        print(f"\n[COMPLETE] Generated {len(visuals)} visuals")
        return visuals

    def create_video_timeline(self, visuals, narration_duration):
        """Create video clips from visuals"""
        print("\n[4/6] Creating Video Timeline...")
        print("-" * 80)

        clips = []

        for i, visual in enumerate(visuals, 1):
            clip_file = self.visuals_dir / f"clip_{i:02d}.mp4"

            try:
                import subprocess

                if visual['type'] == 'video':
                    # Already a video, just copy
                    import shutil
                    shutil.copy(visual['file'], clip_file)
                    clips.append(clip_file)
                    print(f"[{i}/{len(visuals)}] Video clip ready: {visual['file'].name}")

                else:
                    # Convert image/infographic to video clip
                    cmd = [
                        'ffmpeg', '-y', '-loop', '1',
                        '-i', str(visual['file']),
                        '-c:v', 'libx264', '-t', str(visual['duration']),
                        '-pix_fmt', 'yuv420p',
                        '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
                        str(clip_file)
                    ]

                    result = subprocess.run(cmd, capture_output=True)

                    if result.returncode == 0:
                        clips.append(clip_file)
                        print(f"[{i}/{len(visuals)}] Clip created: {visual['file'].name} ({visual['duration']}s)")

            except Exception as e:
                print(f"[ERROR] Failed to create clip {i}: {e}")
                continue

        # Concatenate clips
        if clips:
            concat_file = self.visuals_dir / "concat_list.txt"
            with open(concat_file, 'w') as f:
                for clip in clips:
                    f.write(f"file '{clip.absolute()}'\n")

            video_only = self.output_dir / "video_visuals_only.mp4"

            cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                str(video_only)
            ]

            result = subprocess.run(cmd, capture_output=True)

            if result.returncode == 0:
                print(f"[OK] Visual timeline created: {video_only}")
                return video_only

        return None

    def mix_audio(self, video_file, narration_file, music_file):
        """Mix narration and background music at correct levels"""
        print("\n[5/6] Mixing Audio...")
        print("-" * 80)

        final_video = self.output_dir / "final_video_production.mp4"

        try:
            import subprocess

            # Mix at 10-15% background music volume
            print(f"[NARRATION] 100% volume")
            print(f"[MUSIC] 12% volume (background)")

            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_file),
                '-i', str(narration_file),
                '-i', str(music_file),
                '-filter_complex',
                '[1:a]volume=1.0[narration];'
                '[2:a]volume=0.12[music];'
                '[narration][music]amix=inputs=2:duration=first[audio]',
                '-map', '0:v',
                '-map', '[audio]',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-shortest',
                str(final_video)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                size = final_video.stat().st_size / 1024 / 1024
                print(f"[OK] Final video created: {final_video}")
                print(f"[SIZE] {size:.2f} MB")
                return final_video
            else:
                print(f"[ERROR] FFmpeg failed: {result.stderr}")
                return None

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def verify_audio_quality(self, video_file):
        """Verify the audio is clean and mixed correctly"""
        print("\n[6/6] Verifying Audio Quality...")
        print("-" * 80)

        try:
            import subprocess

            # Extract audio for analysis
            audio_extract = self.output_dir / "audio_extract.mp3"

            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_file),
                '-vn', '-acodec', 'mp3',
                str(audio_extract)
            ]

            result = subprocess.run(cmd, capture_output=True)

            if result.returncode == 0:
                size = audio_extract.stat().st_size / 1024
                print(f"[OK] Audio extracted for review: {audio_extract}")
                print(f"[SIZE] {size:.1f} KB")
                print(f"[ACTION] Please listen to verify:")
                print(f"  1. Narration is clear and intelligible")
                print(f"  2. No instructions/stage directions are spoken")
                print(f"  3. Background music is at 10-15% (not overpowering)")
                print(f"  4. Audio levels are balanced")

                return True

        except Exception as e:
            print(f"[ERROR] {str(e)}")

        return False

    def run(self):
        """Execute production pipeline"""
        print("\nStarting production pipeline...\n")

        # Select music
        music_file = self.select_background_music()
        if not music_file:
            return None

        # Generate narration
        segment = FULL_SCRIPT_SECTIONS["intro"] if self.test_mode else FULL_SCRIPT_SECTIONS
        narration_file = self.generate_narration(segment["text"])
        if not narration_file:
            return None

        # Generate visuals
        visuals = self.generate_visuals_with_fal(segment)
        if not visuals:
            print("[WARNING] No visuals generated, creating simple video")

        # Create video timeline
        video_file = self.create_video_timeline(visuals, 30)
        if not video_file:
            return None

        # Mix audio
        final_video = self.mix_audio(video_file, narration_file, music_file)
        if not final_video:
            return None

        # Verify quality
        self.verify_audio_quality(final_video)

        # Summary
        print("\n" + "="*80)
        print("PRODUCTION PIPELINE COMPLETE")
        print("="*80)
        print(f"\n[SUCCESS] Production video created!")
        print(f"\nFinal video: {final_video}")
        print(f"Output directory: {self.output_dir}")

        if self.test_mode:
            print(f"\n[NEXT STEP] Review this 30-second test, then run full 6-minute production")

        print("\n" + "="*80)

        return final_video

if __name__ == "__main__":
    # Start with TEST mode (30 seconds)
    pipeline = ProductionPipeline(test_mode=True)
    result = pipeline.run()

    if result:
        print(f"\n[SUCCESS] Test video ready: {result}")
        print(f"\nTo generate full 6-minute video, run:")
        print(f"  python production_video_pipeline.py --full")
    else:
        print("\n[FAILED] Pipeline failed")
        sys.exit(1)
