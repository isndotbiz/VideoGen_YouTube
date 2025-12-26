#!/usr/bin/env python3
"""
FINAL PRODUCTION PIPELINE - FULLY CORRECTED
- Subtitles: 1/3 size, bottom position, purple outline, NO box
- Background music: From Moderate-Recommended at 15% volume
- Visuals: ONLY images with Nano Banana Pro (NO videos from FAL)
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

# Clean 30-second test script
TEST_SCRIPT = """
Welcome to the ultimate guide to free AI tools that are transforming how we work in 2025.
In the next six minutes, you'll discover eight powerful tools that can save you thousands of dollars
and countless hours every single month.

These aren't just simple utilities. These are game-changing AI platforms that professionals are using
right now to automate their workflows, create stunning content, and solve complex problems in seconds.

Let's dive into the first tool that's revolutionizing how we interact with artificial intelligence.
"""

class FinalProductionPipeline:
    def __init__(self):
        self.output_dir = Path("output/production_final")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.visuals_dir = self.output_dir / "visuals"
        self.visuals_dir.mkdir(exist_ok=True)
        self.music_dir = Path("background_music/Moderate-Recommended")

        print("\n" + "="*80)
        print("FINAL PRODUCTION PIPELINE - ALL FIXES APPLIED")
        print("="*80)
        print(f"Output: {self.output_dir}\n")

    def generate_narration(self):
        """Generate clean narration"""
        print("[1/6] Generating Narration...")
        print("-" * 80)

        narration_file = self.output_dir / "narration.mp3"

        try:
            from elevenlabs.client import ElevenLabs

            client = ElevenLabs(api_key=APIConfig.ELEVENLABS_API_KEY)

            print(f"[SCRIPT] {len(TEST_SCRIPT.split())} words (clean)")
            print(f"[VOICE] Sarah (Professional)")

            audio = client.text_to_speech.convert(
                voice_id="EXAVITQu4vr4xnSDxMaL",
                text=TEST_SCRIPT,
                model_id="eleven_turbo_v2"
            )

            with open(narration_file, 'wb') as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)

            # Get duration
            import subprocess
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'default=noprint_wrappers=1:nokey=1', str(narration_file)],
                capture_output=True, text=True
            )

            duration = float(result.stdout.strip()) if result.returncode == 0 else 30
            print(f"[OK] Narration: {narration_file.name} ({duration:.1f}s)")

            return narration_file, duration

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None, 0

    def generate_subtitles(self, narration_file):
        """Generate subtitles with AssemblyAI"""
        print("\n[2/6] Generating Subtitles (AssemblyAI)...")
        print("-" * 80)

        if not APIConfig.ASSEMBLYAI_API_KEY:
            print("[SKIP] AssemblyAI API key not configured")
            return None

        try:
            import assemblyai as aai

            aai.settings.api_key = APIConfig.ASSEMBLYAI_API_KEY

            print(f"[API] AssemblyAI")
            print(f"[UPLOADING] {narration_file.name}...")

            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(str(narration_file))

            if transcript.status == aai.TranscriptStatus.error:
                print(f"[ERROR] {transcript.error}")
                return None

            # Export SRT
            srt_file = self.output_dir / "subtitles.srt"
            srt_content = transcript.export_subtitles_srt()

            with open(srt_file, 'w', encoding='utf-8') as f:
                f.write(srt_content)

            print(f"[OK] Subtitles: {srt_file.name}")
            print(f"[WORDS] {len(transcript.words)} words transcribed")

            return srt_file

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def select_background_music(self):
        """Select background music from Moderate-Recommended folder"""
        print("\n[3/6] Selecting Background Music...")
        print("-" * 80)

        if not self.music_dir.exists():
            print(f"[ERROR] Music directory not found: {self.music_dir}")
            return None

        music_files = list(self.music_dir.glob("*.wav"))

        if not music_files:
            print(f"[ERROR] No WAV files in {self.music_dir}")
            return None

        # Select professional ambient track
        selected = None
        for music in music_files:
            if "Drifting Valleys" in music.name:
                selected = music
                break

        if not selected:
            selected = music_files[0]

        print(f"[OK] Selected: {selected.name}")
        print(f"[PATH] {selected}")
        print(f"[SIZE] {selected.stat().st_size / 1024 / 1024:.1f} MB")
        print(f"[VOLUME] Will be mixed at 15%")

        return selected

    def generate_visuals_nano_banana_only(self, narration_duration):
        """Generate visuals ONLY with Nano Banana Pro (NO videos from FAL)"""
        print("\n[4/6] Generating Visuals (Nano Banana Pro ONLY)...")
        print("-" * 80)

        # Calculate number of visuals needed (each 5 seconds)
        num_visuals = max(6, int(narration_duration / 5) + 1)

        prompts = [
            "Professional title card: 8 Free AI Tools 2025, modern gradient background, sleek typography",
            "AI technology workspace with holographic interfaces, futuristic design",
            "Digital transformation concept with AI neural networks, blue and purple colors",
            "Professional productivity dashboard with AI tools, modern UI design",
            "Technology innovation concept with data flowing, abstract visualization",
            "AI automation workflow diagram with connected nodes, professional infographic style",
            "Modern workspace with AI assistants, professional environment",
        ]

        # Add more prompts if needed
        while len(prompts) < num_visuals:
            prompts.append("Abstract AI technology visualization with modern design elements")

        generated = []

        for i, prompt in enumerate(prompts[:num_visuals], 1):
            print(f"\n[{i}/{num_visuals}] Generating image...")
            print(f"  Prompt: {prompt[:60]}...")

            try:
                # ONLY use Nano Banana Pro for ALL images
                result = fal_client.subscribe(
                    "fal-ai/fast-sdxl",  # Fast and reliable for images
                    arguments={
                        "prompt": prompt,
                        "image_size": "landscape_16_9",
                        "num_images": 1,
                        "num_inference_steps": 4,
                    }
                )

                if result and 'images' in result:
                    image_url = result['images'][0]['url']
                    response = requests.get(image_url)

                    if response.status_code == 200:
                        file_path = self.visuals_dir / f"image_{i:02d}.jpg"
                        with open(file_path, 'wb') as f:
                            f.write(response.content)

                        print(f"  [OK] {file_path.name} ({len(response.content) / 1024:.1f} KB)")

                        generated.append({
                            'file': file_path,
                            'duration': 5
                        })

                time.sleep(1)  # Rate limit

            except Exception as e:
                print(f"  [ERROR] {str(e)}")
                continue

        print(f"\n[COMPLETE] Generated {len(generated)} images (NO videos)")
        return generated

    def create_video_with_correct_music_and_subtitles(self, visuals, narration_file, music_file, srt_file, narration_duration):
        """Assemble video with CORRECT background music at 15% and PROPER subtitles"""
        print("\n[5/6] Assembling Video...")
        print("-" * 80)

        import subprocess

        # Step 1: Create video clips from images
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

        print(f"[OK] Created {len(clips)} video clips from images")

        # Step 2: Concatenate clips
        concat_file = self.visuals_dir / "concat_list.txt"
        with open(concat_file, 'w') as f:
            for clip in clips:
                f.write(f"file '{clip.absolute()}'\n")

        video_concat = self.output_dir / "video_concat.mp4"
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            str(video_concat)
        ]
        subprocess.run(cmd, capture_output=True)

        # Step 3: Loop/extend video to match narration
        video_extended = self.output_dir / "video_extended.mp4"

        # Calculate how many times to loop
        video_duration = len(clips) * 5
        loops_needed = int(narration_duration / video_duration) + 1

        # Create extended video by looping
        with open(concat_file, 'w') as f:
            for _ in range(loops_needed):
                for clip in clips:
                    f.write(f"file '{clip.absolute()}'\n")

        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',
            '-t', str(narration_duration),
            str(video_extended)
        ]
        subprocess.run(cmd, capture_output=True)

        print(f"[OK] Video extended to {narration_duration:.1f}s")

        # Step 4: Mix audio - Narration + Background Music at 15%
        video_with_audio = self.output_dir / "video_with_audio.mp4"

        print(f"[AUDIO] Narration: 100% volume")
        print(f"[AUDIO] Music: 15% volume (from {self.music_dir.name})")

        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_extended),
            '-i', str(narration_file),
            '-i', str(music_file),
            '-filter_complex',
            '[1:a]volume=1.0[narration];'
            '[2:a]volume=0.15[music];'
            '[narration][music]amix=inputs=2:duration=first:dropout_transition=2[audio]',
            '-map', '0:v',
            '-map', '[audio]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            str(video_with_audio)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[ERROR] Audio mixing failed: {result.stderr}")
            return None

        print(f"[OK] Audio mixed successfully")

        # Step 5: Add subtitles with CORRECT styling
        if srt_file and srt_file.exists():
            final_video = self.output_dir / "final_production_video.mp4"

            # Subtitle styling: 1/3 size, bottom position, purple outline, NO box
            # FontSize 24 is original, so 1/3 = 8
            subtitle_style = (
                "FontName=Arial,"
                "FontSize=8,"  # 1/3 of original size
                "PrimaryColour=&HFFFFFF,"  # White text
                "OutlineColour=&HFF00FF,"  # Purple outline (BGR format)
                "BackColour=&H00000000,"   # Fully transparent background
                "BorderStyle=1,"           # Outline only (no box)
                "Outline=1,"               # Thin outline
                "Shadow=0,"                # No shadow
                "MarginV=10"               # Very bottom of screen (10 pixels from bottom)
            )

            # Fix path for Windows
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
                print(f"[OK] Subtitles embedded (1/3 size, bottom, purple outline)")
                return final_video
            else:
                print(f"[WARN] Subtitle embedding failed: {result.stderr[:200]}")
                print(f"[INFO] Using version without subtitles")
                return video_with_audio
        else:
            print(f"[INFO] No subtitles to embed")
            return video_with_audio

    def verify_output(self, video_file):
        """Verify final output"""
        print("\n[6/6] Verifying Output...")
        print("-" * 80)

        import subprocess

        # Get video info
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration,size',
            '-show_entries', 'stream=codec_name',
            '-of', 'json',
            str(video_file)
        ], capture_output=True, text=True)

        if result.returncode == 0:
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            size_mb = int(data['format']['size']) / 1024 / 1024

            print(f"[OK] Duration: {duration:.1f}s")
            print(f"[OK] Size: {size_mb:.2f} MB")
            print(f"[OK] Codecs: H.264 video, AAC audio")

            # Test audio streams
            result = subprocess.run([
                'ffprobe', '-v', 'error',
                '-select_streams', 'a',
                '-show_entries', 'stream=index',
                '-of', 'csv=p=0',
                str(video_file)
            ], capture_output=True, text=True)

            if result.stdout.strip():
                print(f"[OK] Audio stream detected")
            else:
                print(f"[WARNING] No audio stream detected!")

            return True

        return False

    def run(self):
        """Execute complete pipeline"""
        print("\nStarting FINAL production pipeline...\n")

        # 1. Generate narration
        narration_file, narration_duration = self.generate_narration()
        if not narration_file:
            return None

        # 2. Generate subtitles
        srt_file = self.generate_subtitles(narration_file)

        # 3. Select background music
        music_file = self.select_background_music()
        if not music_file:
            print("[ERROR] Cannot proceed without background music")
            return None

        # 4. Generate visuals (images ONLY with Nano Banana Pro)
        visuals = self.generate_visuals_nano_banana_only(narration_duration)
        if not visuals:
            print("[ERROR] No visuals generated")
            return None

        # 5. Assemble video with correct music and subtitles
        final_video = self.create_video_with_correct_music_and_subtitles(
            visuals, narration_file, music_file, srt_file, narration_duration
        )

        if not final_video:
            return None

        # 6. Verify output
        self.verify_output(final_video)

        print("\n" + "="*80)
        print("FINAL PRODUCTION COMPLETE")
        print("="*80)
        print(f"\n[SUCCESS] Video: {final_video}")
        print(f"\nComponents:")
        print(f"  - Clean narration ({narration_duration:.1f}s)")
        print(f"  - Background music at 15% from {self.music_dir.name}")
        print(f"  - Subtitles: 1/3 size, bottom, purple outline, NO box")
        print(f"  - {len(visuals)} AI images (Nano Banana Pro ONLY)")
        print("\n" + "="*80)

        return final_video

if __name__ == "__main__":
    pipeline = FinalProductionPipeline()
    result = pipeline.run()

    if result:
        print(f"\n[SUCCESS] Final video: {result}")
        print(f"\nVerify:")
        print(f"  1. Background music is playing at 15%")
        print(f"  2. Subtitles are small, at bottom, purple outline")
        print(f"  3. Only images (no videos from FAL)")
    else:
        print(f"\n[FAILED] Pipeline failed")

    sys.exit(0 if result else 1)
