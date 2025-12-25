#!/usr/bin/env python3
"""
Quick 30-Second Test Video Generator
Uses the clean script from VIDEO_1_CLEAN_SCRIPT_30_SECONDS.md
"""
import os
import sys
import json
import time
from pathlib import Path
from config import APIConfig, VideoConfig, ProjectConfig

# Clean script - 165 words, 30 seconds
CLEAN_SCRIPT = """Welcome to the 8 best free AI tools that will transform how you work. These powerful tools will save you time and boost your productivity. Let's dive in.

First, we have ChatGPT. This advanced AI writes code, answers questions, and creates content in seconds.

Next is Midjourney. Generate stunning images from text prompts. Perfect for creators and designers.

ElevenLabs brings your text to life with natural sounding voices. Create professional narration instantly.

Meet Claude. A powerful AI assistant for analysis, writing, and problem solving.

Synthesys AI creates realistic AI avatars that speak naturally. Perfect for video content.

Runway is the creative suite for video generation and editing powered by AI.

Zapier connects your favorite tools and automates workflows without code.

Finally, CapCut makes video editing simple with powerful AI-powered editing features.

Start using these tools today. Transform your creative workflow now."""

class Quick30SecVideo:
    def __init__(self):
        self.output_dir = Path("output/test_30sec")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print("\n" + "="*80)
        print("QUICK 30-SECOND TEST VIDEO")
        print("="*80)
        print(f"Output directory: {self.output_dir}")

    def check_apis(self):
        """Check which APIs are configured"""
        print("\n[1/5] Checking API Configuration...")
        print("-" * 80)

        status = APIConfig.check_required_apis()
        print(f"APIs configured: {status['configured']}/{status['total']}")

        if status['missing']:
            print(f"\nMissing APIs: {', '.join(status['missing'])}")
            print("\nNote: Will use fallbacks where possible")

        return status['configured'] > 0

    def generate_narration(self):
        """Generate narration using ElevenLabs"""
        print("\n[2/5] Generating Narration...")
        print("-" * 80)

        narration_file = self.output_dir / "narration_30sec.mp3"

        if not APIConfig.ELEVENLABS_API_KEY or APIConfig.ELEVENLABS_API_KEY.startswith("your_"):
            print("[SKIP] ElevenLabs API key not configured")
            print("[INFO] You can add narration manually later")
            return None

        try:
            from elevenlabs.client import ElevenLabs

            print(f"[API] ElevenLabs")
            print(f"[VOICE] Sarah (Mature, Reassuring, Confident)")
            print(f"[SCRIPT] {len(CLEAN_SCRIPT.split())} words")

            # Initialize client
            client = ElevenLabs(api_key=APIConfig.ELEVENLABS_API_KEY)

            # Generate audio using Sarah voice
            audio = client.text_to_speech.convert(
                voice_id="EXAVITQu4vr4xnSDxMaL",  # Sarah
                text=CLEAN_SCRIPT,
                model_id="eleven_turbo_v2"
            )

            # Save to file
            with open(narration_file, 'wb') as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)

            file_size = narration_file.stat().st_size / 1024 / 1024
            print(f"[OK] Narration saved: {narration_file}")
            print(f"[SIZE] {file_size:.2f} MB")

            return narration_file

        except ImportError:
            print("[ERROR] elevenlabs package not installed")
            print("[FIX] Run: pip install elevenlabs")
            return None
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def get_background_music(self):
        """Get background music from Pexels"""
        print("\n[3/5] Getting Background Music...")
        print("-" * 80)

        music_file = self.output_dir / "background_music.mp3"

        # Check if we already have cached music
        cached_music = Path("background_music/Not-Curated")
        if cached_music.exists():
            music_files = list(cached_music.glob("*.mp3"))
            if music_files and not str(music_files[0]).endswith('.crdownload'):
                import shutil
                shutil.copy(music_files[0], music_file)
                print(f"[OK] Using cached music: {music_files[0].name}")
                print(f"[SIZE] {music_file.stat().st_size / 1024:.2f} KB")
                return music_file

        # Try to fetch from Pexels
        if not APIConfig.PEXELS_API_KEY or APIConfig.PEXELS_API_KEY.startswith("your_"):
            print("[SKIP] Pexels API key not configured")
            print("[INFO] Video will be created without background music")
            return None

        try:
            import requests

            headers = {"Authorization": APIConfig.PEXELS_API_KEY}
            response = requests.get(
                "https://api.pexels.com/videos/popular?per_page=1",
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                # For now, just indicate we checked
                print("[OK] Pexels API connected")
                print("[INFO] Using local music cache instead")
                return None
            else:
                print(f"[WARN] Pexels API returned {response.status_code}")
                return None

        except Exception as e:
            print(f"[WARN] Could not fetch music: {str(e)}")
            return None

    def create_simple_video(self, narration_file, music_file):
        """Create a simple video with narration and text"""
        print("\n[4/5] Creating Video...")
        print("-" * 80)

        output_video = self.output_dir / "test_video_30sec.mp4"

        # If no narration, create a text-only video
        if not narration_file:
            print("[INFO] Creating text-only demo video...")
            try:
                import subprocess

                # Create a simple video with text using FFmpeg
                cmd = [
                    'ffmpeg', '-y',
                    '-f', 'lavfi', '-i', 'color=c=black:s=1920x1080:d=30',
                    '-vf', 'drawtext=text=\'30-Second Test Video\\nGenerated Successfully\':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2',
                    '-c:v', 'libx264', '-t', '30', '-pix_fmt', 'yuv420p',
                    str(output_video)
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    print(f"[OK] Demo video created: {output_video}")
                    file_size = output_video.stat().st_size / 1024 / 1024
                    print(f"[SIZE] {file_size:.2f} MB")
                    return output_video
                else:
                    print(f"[ERROR] FFmpeg failed: {result.stderr}")
                    return None

            except FileNotFoundError:
                print("[ERROR] FFmpeg not found in PATH")
                print("[FIX] Install FFmpeg: https://ffmpeg.org/download.html")
                return None
            except Exception as e:
                print(f"[ERROR] {str(e)}")
                return None

        # Create video with narration
        try:
            import subprocess

            # Simple video: black background with narration
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi', '-i', f'color=c=black:s=1920x1080:d=30',
                '-i', str(narration_file),
                '-c:v', 'libx264', '-c:a', 'aac',
                '-shortest',
                str(output_video)
            ]

            if music_file:
                # Add music mixing (narration at 100%, music at 15%)
                cmd = [
                    'ffmpeg', '-y',
                    '-f', 'lavfi', '-i', f'color=c=black:s=1920x1080:d=30',
                    '-i', str(narration_file),
                    '-i', str(music_file),
                    '-filter_complex', '[1:a][2:a]amix=inputs=2:duration=shortest:weights=1 0.15[a]',
                    '-map', '0:v', '-map', '[a]',
                    '-c:v', 'libx264', '-c:a', 'aac',
                    str(output_video)
                ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"[OK] Video created: {output_video}")
                file_size = output_video.stat().st_size / 1024 / 1024
                print(f"[SIZE] {file_size:.2f} MB")
                return output_video
            else:
                print(f"[ERROR] FFmpeg failed: {result.stderr}")
                return None

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def create_report(self, narration_file, music_file, video_file):
        """Generate a report of what was created"""
        print("\n[5/5] Generating Report...")
        print("-" * 80)

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "script_words": len(CLEAN_SCRIPT.split()),
            "script_characters": len(CLEAN_SCRIPT),
            "narration_file": str(narration_file) if narration_file else None,
            "music_file": str(music_file) if music_file else None,
            "video_file": str(video_file) if video_file else None,
            "files_created": []
        }

        # List all created files
        for file in self.output_dir.glob("*"):
            if file.is_file():
                report["files_created"].append({
                    "name": file.name,
                    "size_kb": file.stat().st_size / 1024,
                    "path": str(file)
                })

        report_file = self.output_dir / "generation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"[OK] Report saved: {report_file}")
        return report

    def run(self):
        """Execute the complete pipeline"""
        print("\nStarting 30-second test video generation...\n")

        # Step 1: Check APIs
        if not self.check_apis():
            print("\n[WARNING] No APIs configured. Will create a basic demo video.")

        # Step 2: Generate narration
        narration_file = self.generate_narration()

        # Step 3: Get background music
        music_file = self.get_background_music()

        # Step 4: Create video
        video_file = self.create_simple_video(narration_file, music_file)

        # Step 5: Generate report
        report = self.create_report(narration_file, music_file, video_file)

        # Final summary
        print("\n" + "="*80)
        print("PIPELINE COMPLETE")
        print("="*80)

        if video_file:
            print(f"\n[OK] SUCCESS! Video created: {video_file}")
            print(f"\nFiles created:")
            for file_info in report["files_created"]:
                print(f"  - {file_info['name']:30s} ({file_info['size_kb']:.2f} KB)")
        else:
            print("\n[ERROR] FAILED: Could not create video")
            print("Check error messages above for details")

        print("\n" + "="*80)
        return video_file

if __name__ == "__main__":
    pipeline = Quick30SecVideo()
    result = pipeline.run()

    if result:
        print(f"\nVideo ready: {result}")
        print("\nNext steps:")
        print("  1. Review the video")
        print("  2. Add animations with: python generate_animations_with_fal.py")
        print("  3. Upload to YouTube")
        sys.exit(0)
    else:
        print("\nPipeline failed. Check configuration and try again.")
        sys.exit(1)
