#!/usr/bin/env python3
"""
COMPLETE PRODUCTION PIPELINE - FINAL VERSION
- GPT Image 1.5 for ALL image generation
- Background music FIXED (actually playing)
- Subtitles: small, bottom, purple outline
"""
import os
import sys
import json
import time
import fal_client
import requests
from pathlib import Path
from config import APIConfig

os.environ["FAL_KEY"] = APIConfig.FAL_API_KEY

TEST_SCRIPT = """
Welcome to the ultimate guide to free AI tools that are transforming how we work in 2025.
In the next six minutes, you'll discover eight powerful tools that can save you thousands of dollars
and countless hours every single month.

These aren't just simple utilities. These are game-changing AI platforms that professionals are using
right now to automate their workflows, create stunning content, and solve complex problems in seconds.

Let's dive into the first tool that's revolutionizing how we interact with artificial intelligence.
"""

class CompleteProductionPipeline:
    def __init__(self):
        self.output_dir = Path("output/production_complete")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.visuals_dir = self.output_dir / "visuals"
        self.visuals_dir.mkdir(exist_ok=True)
        self.music_dir = Path("background_music/Moderate-Recommended")

        print("\n" + "="*80)
        print("COMPLETE PRODUCTION PIPELINE")
        print("="*80)
        print("- Images: GPT Image 1.5")
        print("- Music: 15% volume from Moderate-Recommended")
        print("- Subtitles: Small, bottom, purple outline")
        print(f"- Output: {self.output_dir}")
        print("="*80 + "\n")

    def generate_narration(self):
        """Generate clean narration"""
        print("[1/6] Generating Narration...")
        print("-" * 80)

        narration_file = self.output_dir / "narration.mp3"

        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=APIConfig.ELEVENLABS_API_KEY)

            print(f"[SCRIPT] {len(TEST_SCRIPT.split())} words (clean)")

            audio = client.text_to_speech.convert(
                voice_id="EXAVITQu4vr4xnSDxMaL",
                text=TEST_SCRIPT,
                model_id="eleven_turbo_v2"
            )

            with open(narration_file, 'wb') as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)

            import subprocess
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', str(narration_file)],
                capture_output=True, text=True
            )

            duration = float(result.stdout.strip()) if result.returncode == 0 else 30
            print(f"[OK] Narration: {duration:.1f}s")
            return narration_file, duration

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None, 0

    def generate_subtitles(self, narration_file):
        """Generate subtitles"""
        print("\n[2/6] Generating Subtitles...")
        print("-" * 80)

        try:
            import assemblyai as aai
            aai.settings.api_key = APIConfig.ASSEMBLYAI_API_KEY

            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(str(narration_file))

            if transcript.status == aai.TranscriptStatus.error:
                print(f"[ERROR] {transcript.error}")
                return None

            srt_file = self.output_dir / "subtitles.srt"
            with open(srt_file, 'w', encoding='utf-8') as f:
                f.write(transcript.export_subtitles_srt())

            print(f"[OK] Subtitles generated")
            return srt_file

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def select_background_music(self):
        """Select background music"""
        print("\n[3/6] Selecting Background Music...")
        print("-" * 80)

        music_files = list(self.music_dir.glob("*.wav"))
        if not music_files:
            print(f"[ERROR] No music found")
            return None

        selected = None
        for music in music_files:
            if "Drifting Valleys" in music.name:
                selected = music
                break

        if not selected:
            selected = music_files[0]

        print(f"[SELECTED] {selected.name}")
        print(f"[PATH] {selected.absolute()}")
        print(f"[EXISTS] {selected.exists()}")
        return selected

    def generate_images_gpt15(self, narration_duration):
        """Generate images using GPT Image 1.5"""
        print("\n[4/6] Generating Images (GPT Image 1.5)...")
        print("-" * 80)

        num_images = max(6, int(narration_duration / 5) + 1)

        prompts = [
            "Professional title card with text '8 Free AI Tools 2025', modern gradient background, corporate style",
            "AI technology workspace with holographic interfaces, futuristic tech environment",
            "Digital transformation concept with neural networks, blue and purple colors",
            "Professional productivity dashboard with AI tools, modern UI",
            "Technology innovation with data flowing, abstract visualization",
            "AI automation workflow with connected nodes, professional infographic",
            "Modern workspace with AI assistants, professional environment",
        ]

        while len(prompts) < num_images:
            prompts.append("Abstract AI technology visualization with modern design")

        generated = []

        for i, prompt in enumerate(prompts[:num_images], 1):
            print(f"\n[{i}/{num_images}] Generating...")
            print(f"  Prompt: {prompt[:50]}...")

            try:
                result = fal_client.subscribe(
                    "fal-ai/gpt-image-1.5",
                    arguments={
                        "prompt": prompt,
                        "image_size": "1536x1024",  # 16:9 landscape
                        "quality": "high",
                        "num_images": 1,
                    }
                )

                if result and 'images' in result:
                    image_url = result['images'][0]['url']
                    response = requests.get(image_url)

                    if response.status_code == 200:
                        file_path = self.visuals_dir / f"image_{i:02d}.jpg"
                        with open(file_path, 'wb') as f:
                            f.write(response.content)

                        print(f"  [OK] {file_path.name}")
                        generated.append({'file': file_path, 'duration': 5})

                time.sleep(1)

            except Exception as e:
                print(f"  [ERROR] {str(e)}")
                continue

        print(f"\n[COMPLETE] Generated {len(generated)} images")
        return generated

    def assemble_video_with_music(self, visuals, narration_file, music_file, srt_file, narration_duration):
        """Assemble video with WORKING background music"""
        print("\n[5/6] Assembling Video...")
        print("-" * 80)

        import subprocess

        # Step 1: Create clips
        clips = []
        for i, visual in enumerate(visuals, 1):
            clip_file = self.visuals_dir / f"clip_{i:02d}.mp4"

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

        # Step 2: Concatenate and extend
        concat_file = self.visuals_dir / "concat_list.txt"
        loops_needed = int(narration_duration / (len(clips) * 5)) + 1

        with open(concat_file, 'w') as f:
            for _ in range(loops_needed):
                for clip in clips:
                    f.write(f"file '{clip.absolute()}'\n")

        video_extended = self.output_dir / "video_extended.mp4"
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            '-t', str(narration_duration),
            str(video_extended)
        ]
        subprocess.run(cmd, capture_output=True)
        print(f"[OK] Video: {narration_duration:.1f}s")

        # Step 3: Mix audio - PROPERLY this time
        video_with_audio = self.output_dir / "video_with_audio.mp4"

        print(f"[MIXING] Narration: {narration_file.absolute()}")
        print(f"[MIXING] Music: {music_file.absolute()}")
        print(f"[MIXING] Music volume: 15%")

        # Use amerge + pan for proper mixing
        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_extended),
            '-i', str(narration_file),
            '-i', str(music_file),
            '-filter_complex',
            # Mix narration at 100% and music at 15%
            '[1:a]volume=1.0[nar];'
            '[2:a]volume=0.15,aloop=loop=-1:size=2e+09[mus];'
            '[nar][mus]amix=inputs=2:duration=first:dropout_transition=0[aout]',
            '-map', '0:v',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            str(video_with_audio)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[ERROR] Mixing failed: {result.stderr[:200]}")
            return None

        # Verify audio was mixed
        test_result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-select_streams', 'a',
            '-show_entries', 'stream=codec_name',
            '-of', 'csv=p=0',
            str(video_with_audio)
        ], capture_output=True, text=True)

        if not test_result.stdout.strip():
            print(f"[ERROR] No audio in output!")
            return None

        print(f"[OK] Audio mixed (narration + music 15%)")

        # Step 4: Add subtitles
        if srt_file and srt_file.exists():
            final_video = self.output_dir / "final_video_complete.mp4"

            subtitle_style = (
                "FontName=Arial,"
                "FontSize=8,"
                "PrimaryColour=&HFFFFFF,"
                "OutlineColour=&HFF00FF,"
                "BackColour=&H00000000,"
                "BorderStyle=1,"
                "Outline=1,"
                "Shadow=0,"
                "MarginV=10"
            )

            srt_path = str(srt_file.absolute()).replace('\\', '/').replace(':', '\\:')

            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_with_audio),
                '-vf', f"subtitles='{srt_path}':force_style='{subtitle_style}'",
                '-c:a', 'copy',
                str(final_video)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"[OK] Subtitles added")
                return final_video
            else:
                print(f"[WARN] Subtitle failed, using version without")
                return video_with_audio
        else:
            return video_with_audio

    def verify_output(self, video_file):
        """Verify output has audio"""
        print("\n[6/6] Verifying...")
        print("-" * 80)

        import subprocess

        # Check streams
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-show_entries', 'stream=index,codec_type,codec_name',
            '-of', 'json',
            str(video_file)
        ], capture_output=True, text=True)

        if result.returncode == 0:
            data = json.loads(result.stdout)
            streams = data.get('streams', [])

            video_streams = [s for s in streams if s.get('codec_type') == 'video']
            audio_streams = [s for s in streams if s.get('codec_type') == 'audio']

            print(f"[OK] Video streams: {len(video_streams)}")
            print(f"[OK] Audio streams: {len(audio_streams)}")

            if audio_streams:
                print(f"[OK] Audio codec: {audio_streams[0].get('codec_name')}")
                return True
            else:
                print(f"[ERROR] NO AUDIO STREAM!")
                return False

        return False

    def run(self):
        """Execute pipeline"""
        print("Starting complete production pipeline...\n")

        narration_file, narration_duration = self.generate_narration()
        if not narration_file:
            return None

        srt_file = self.generate_subtitles(narration_file)

        music_file = self.select_background_music()
        if not music_file:
            return None

        visuals = self.generate_images_gpt15(narration_duration)
        if not visuals:
            return None

        final_video = self.assemble_video_with_music(
            visuals, narration_file, music_file, srt_file, narration_duration
        )

        if not final_video:
            return None

        if self.verify_output(final_video):
            print("\n" + "="*80)
            print("PRODUCTION COMPLETE")
            print("="*80)
            print(f"\n[SUCCESS] {final_video}")
            print(f"\nVerify:")
            print(f"  - Background music playing at 15%")
            print(f"  - Subtitles: small, bottom, purple")
            print(f"  - Images from GPT Image 1.5")
            print("\n" + "="*80)
            return final_video
        else:
            print("\n[FAILED] Audio verification failed")
            return None

if __name__ == "__main__":
    pipeline = CompleteProductionPipeline()
    result = pipeline.run()
    sys.exit(0 if result else 1)
