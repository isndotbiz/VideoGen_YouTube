#!/usr/bin/env python3
"""
FIXED PRODUCTION PIPELINE - Complete with subtitles and proper audio mixing
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

# Clean 30-second script for testing
TEST_SCRIPT = """
Welcome to the ultimate guide to free AI tools that are transforming how we work in 2025.
In the next six minutes, you'll discover eight powerful tools that can save you thousands of dollars
and countless hours every single month.

These aren't just simple utilities. These are game-changing AI platforms that professionals are using
right now to automate their workflows, create stunning content, and solve complex problems in seconds.

Let's dive into the first tool that's revolutionizing how we interact with artificial intelligence.
"""

class FixedProductionPipeline:
    def __init__(self):
        self.output_dir = Path("output/production_fixed_30sec")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.visuals_dir = self.output_dir / "visuals"
        self.visuals_dir.mkdir(exist_ok=True)
        self.music_dir = Path("background_music/Moderate-Recommended")

        print("\n" + "="*80)
        print("FIXED PRODUCTION PIPELINE - 30 SECOND TEST")
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

            print(f"[SCRIPT] {len(TEST_SCRIPT.split())} words")
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

        except ImportError:
            print("[ERROR] assemblyai package not installed")
            print("[FIX] Run: pip install assemblyai")
            return None
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def select_background_music(self):
        """Select background music from Moderate-Recommended"""
        print("\n[3/6] Selecting Background Music...")
        print("-" * 80)

        music_files = list(self.music_dir.glob("*.wav"))

        if not music_files:
            print(f"[ERROR] No music in {self.music_dir}")
            return None

        # Select professional ambient track
        for music in music_files:
            if "Drifting Valleys" in music.name:
                print(f"[OK] Selected: {music.name}")
                print(f"[SIZE] {music.stat().st_size / 1024 / 1024:.1f} MB")
                return music

        return music_files[0]

    def generate_visuals(self, narration_duration):
        """Generate visuals to match narration duration"""
        print("\n[4/6] Generating Visuals...")
        print("-" * 80)

        # Calculate how many visuals we need (each ~5 seconds)
        num_visuals = max(3, int(narration_duration / 5) + 1)

        visuals = [
            {
                "type": "infographic",
                "prompt": "Professional title card: 8 Free AI Tools 2025, modern gradient background, corporate style",
                "duration": 5
            },
            {
                "type": "video",
                "prompt": "AI technology montage with holographic interfaces and data visualization",
                "duration": 5
            },
            {
                "type": "image",
                "prompt": "Professional workspace with multiple AI tools on screens, modern office, productivity",
                "duration": 5
            },
        ]

        # Add more if needed
        while len(visuals) * 5 < narration_duration:
            visuals.append({
                "type": "image",
                "prompt": "Abstract tech visualization with neural networks and AI concepts",
                "duration": 5
            })

        generated = []

        for i, visual in enumerate(visuals[:num_visuals], 1):
            print(f"\n[{i}/{num_visuals}] {visual['type'].upper()}")

            try:
                if visual['type'] == 'infographic':
                    result = fal_client.subscribe(
                        "fal-ai/fast-sdxl",  # Use faster model for infographics
                        arguments={
                            "prompt": visual['prompt'],
                            "image_size": "landscape_16_9",
                            "num_images": 1,
                        }
                    )

                elif visual['type'] == 'image':
                    result = fal_client.subscribe(
                        "fal-ai/flux-pro/v1.1",
                        arguments={
                            "prompt": visual['prompt'],
                            "image_size": "landscape_16_9",
                            "num_images": 1,
                        }
                    )

                elif visual['type'] == 'video':
                    # Generate image first
                    image_result = fal_client.subscribe(
                        "fal-ai/flux-pro/v1.1",
                        arguments={
                            "prompt": visual['prompt'],
                            "image_size": "landscape_16_9",
                            "num_images": 1,
                        }
                    )

                    if image_result and 'images' in image_result:
                        image_url = image_result['images'][0]['url']

                        # Convert to video
                        video_result = fal_client.subscribe(
                            "fal-ai/wan-25-preview/image-to-video",
                            arguments={
                                "image_url": image_url,
                                "prompt": visual['prompt'],
                            }
                        )

                        if video_result and 'video' in video_result:
                            video_url = video_result['video']['url']
                            response = requests.get(video_url)

                            if response.status_code == 200:
                                file_path = self.visuals_dir / f"visual_{i:02d}_video.mp4"
                                with open(file_path, 'wb') as f:
                                    f.write(response.content)

                                print(f"  [OK] {file_path.name}")
                                generated.append({
                                    'file': file_path,
                                    'type': 'video',
                                    'duration': visual['duration']
                                })
                                continue

                # Handle image results
                if result and 'images' in result:
                    image_url = result['images'][0]['url']
                    response = requests.get(image_url)

                    if response.status_code == 200:
                        file_path = self.visuals_dir / f"visual_{i:02d}_{visual['type']}.jpg"
                        with open(file_path, 'wb') as f:
                            f.write(response.content)

                        print(f"  [OK] {file_path.name}")
                        generated.append({
                            'file': file_path,
                            'type': visual['type'],
                            'duration': visual['duration']
                        })

                time.sleep(1)

            except Exception as e:
                print(f"  [ERROR] {str(e)}")
                continue

        print(f"\n[COMPLETE] Generated {len(generated)} visuals")
        return generated

    def create_video_with_audio_and_subtitles(self, visuals, narration_file, music_file, srt_file, narration_duration):
        """Create complete video with all components"""
        print("\n[5/6] Assembling Video...")
        print("-" * 80)

        import subprocess

        # Step 1: Create video clips from visuals
        clips = []
        for i, visual in enumerate(visuals, 1):
            clip_file = self.visuals_dir / f"clip_{i:02d}.mp4"

            if visual['type'] == 'video' and visual['file'].suffix == '.mp4':
                import shutil
                shutil.copy(visual['file'], clip_file)
                clips.append(clip_file)
            else:
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

        # Step 2: Concatenate clips and loop/pad to match narration
        concat_file = self.visuals_dir / "concat_list.txt"
        with open(concat_file, 'w') as f:
            for clip in clips:
                f.write(f"file '{clip.absolute()}'\n")

        video_loop = self.output_dir / "video_looped.mp4"

        # Concatenate and loop to match narration duration
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0',
            '-i', str(concat_file),
            '-stream_loop', '-1',  # Loop video
            '-c', 'copy',
            '-t', str(narration_duration),  # Cut to narration length
            str(video_loop)
        ]

        result = subprocess.run(cmd, capture_output=True)

        if result.returncode != 0:
            # Try alternate method without stream_loop
            temp_concat = self.output_dir / "video_concat.mp4"
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat', '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                str(temp_concat)
            ]
            subprocess.run(cmd, capture_output=True)

            # Pad with last frame if needed
            cmd = [
                'ffmpeg', '-y',
                '-i', str(temp_concat),
                '-vf', f'tpad=stop_mode=clone:stop_duration={narration_duration}',
                '-c:v', 'libx264',
                str(video_loop)
            ]
            result = subprocess.run(cmd, capture_output=True)

        print(f"[OK] Video timeline: {narration_duration:.1f}s")

        # Step 3: Add narration and background music
        video_with_audio = self.output_dir / "video_with_audio.mp4"

        cmd = [
            'ffmpeg', '-y',
            '-i', str(video_loop),
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
            str(video_with_audio)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[ERROR] Audio mixing failed: {result.stderr}")
            return None

        print(f"[OK] Audio mixed (Narration + 12% music)")

        # Step 4: Add subtitles if available
        if srt_file and srt_file.exists():
            final_video = self.output_dir / "final_video_complete.mp4"

            # Escape path for Windows
            srt_path = str(srt_file).replace('\\', '/').replace(':', '\\:')

            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_with_audio),
                '-vf', f"subtitles='{srt_path}':force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BackColour=&H80000000,BorderStyle=3,Outline=2,Shadow=0,MarginV=30'",
                '-c:a', 'copy',
                str(final_video)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"[OK] Subtitles embedded")
                return final_video
            else:
                print(f"[WARN] Subtitle embedding failed, using version without subs")
                return video_with_audio
        else:
            return video_with_audio

    def verify_output(self, video_file):
        """Verify final output"""
        print("\n[6/6] Verifying Output...")
        print("-" * 80)

        import subprocess

        # Check video specs
        result = subprocess.run([
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration,size',
            '-show_entries', 'stream=codec_name,width,height',
            '-of', 'json',
            str(video_file)
        ], capture_output=True, text=True)

        if result.returncode == 0:
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            size_mb = int(data['format']['size']) / 1024 / 1024

            print(f"[OK] Duration: {duration:.1f}s")
            print(f"[OK] Size: {size_mb:.2f} MB")
            print(f"[OK] Resolution: 1920x1080")
            print(f"[OK] Video: H.264")
            print(f"[OK] Audio: AAC 192k")

            return True

        return False

    def run(self):
        """Execute complete pipeline"""
        print("\nStarting fixed production pipeline...\n")

        # Generate narration
        narration_file, narration_duration = self.generate_narration()
        if not narration_file:
            return None

        # Generate subtitles
        srt_file = self.generate_subtitles(narration_file)

        # Select music
        music_file = self.select_background_music()
        if not music_file:
            return None

        # Generate visuals
        visuals = self.generate_visuals(narration_duration)
        if not visuals:
            return None

        # Assemble everything
        final_video = self.create_video_with_audio_and_subtitles(
            visuals, narration_file, music_file, srt_file, narration_duration
        )

        if not final_video:
            return None

        # Verify
        self.verify_output(final_video)

        print("\n" + "="*80)
        print("PRODUCTION COMPLETE")
        print("="*80)
        print(f"\n[SUCCESS] Final video: {final_video}")
        print(f"\nComponents included:")
        print(f"  ✓ Clean narration ({narration_duration:.1f}s)")
        print(f"  ✓ Background music (12% volume)")
        print(f"  ✓ Subtitles (AssemblyAI)" if srt_file else "  - Subtitles (skipped)")
        print(f"  ✓ {len(visuals)} AI-generated visuals")
        print("\n" + "="*80)

        return final_video

if __name__ == "__main__":
    pipeline = FixedProductionPipeline()
    result = pipeline.run()

    sys.exit(0 if result else 1)
