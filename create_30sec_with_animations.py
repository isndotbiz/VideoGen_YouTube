#!/usr/bin/env python3
"""
30-Second Video with FAL.ai Animations
Complete pipeline: Narration + Animations + Music + Assembly
"""
import os
import sys
import time
import fal_client
from pathlib import Path
from config import APIConfig, VideoConfig

# Configure FAL client
os.environ["FAL_KEY"] = APIConfig.FAL_API_KEY

# Animation prompts for the 8 tools
ANIMATIONS = [
    {
        "tool": "Intro",
        "prompt": "Professional title card with text '8 Best Free AI Tools', modern gradient background, sleek typography, corporate style",
        "duration": 5
    },
    {
        "tool": "ChatGPT",
        "prompt": "ChatGPT interface with code being written automatically, terminal window, programming code flowing, tech aesthetic",
        "duration": 3
    },
    {
        "tool": "Midjourney",
        "prompt": "Beautiful AI-generated images grid appearing one by one, stunning artwork, creative compositions, vibrant colors",
        "duration": 3
    },
    {
        "tool": "ElevenLabs",
        "prompt": "Sound waves visualization with voice synthesis, audio waveforms, professional studio aesthetic, blue and purple colors",
        "duration": 3
    },
    {
        "tool": "Claude",
        "prompt": "AI assistant analyzing documents, data flowing across screen, analytical visualization, professional interface",
        "duration": 3
    },
    {
        "tool": "Synthesys",
        "prompt": "AI avatar speaking naturally, professional presenter, modern background, realistic human face",
        "duration": 3
    },
    {
        "tool": "Runway",
        "prompt": "Video editing interface with creative effects, timeline with clips, professional video production tools",
        "duration": 3
    },
    {
        "tool": "Zapier",
        "prompt": "Workflow automation with apps connecting, data flowing between services, integration visualization",
        "duration": 3
    },
    {
        "tool": "CapCut",
        "prompt": "Mobile video editing with effects and transitions, timeline editing, creative video production",
        "duration": 3
    }
]

class Enhanced30SecVideo:
    def __init__(self):
        self.output_dir = Path("output/test_30sec_animated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.animations_dir = self.output_dir / "animations"
        self.animations_dir.mkdir(exist_ok=True)

        print("\n" + "="*80)
        print("30-SECOND VIDEO WITH ANIMATIONS")
        print("="*80)
        print(f"Output: {self.output_dir}")

    def generate_animations(self):
        """Generate animations using FAL.ai"""
        print("\n[1/3] Generating Animations with FAL.ai...")
        print("-" * 80)

        generated = []

        for i, anim in enumerate(ANIMATIONS, 1):
            print(f"\n[{i}/{len(ANIMATIONS)}] {anim['tool']}")
            print(f"Prompt: {anim['prompt'][:60]}...")

            try:
                # Use FAL.ai flux-pro/v1.1-ultra for high quality images
                result = fal_client.subscribe(
                    "fal-ai/flux-pro/v1.1-ultra",
                    arguments={
                        "prompt": anim['prompt'],
                        "image_size": "landscape_16_9",
                        "num_inference_steps": 28,
                        "guidance_scale": 3.5,
                        "num_images": 1,
                        "enable_safety_checker": True,
                        "output_format": "jpeg",
                        "safety_tolerance": "2"
                    }
                )

                if result and 'images' in result and len(result['images']) > 0:
                    image_url = result['images'][0]['url']

                    # Download image
                    import requests
                    response = requests.get(image_url)

                    if response.status_code == 200:
                        # Save image
                        image_file = self.animations_dir / f"animation_{i:02d}_{anim['tool'].lower()}.jpg"
                        with open(image_file, 'wb') as f:
                            f.write(response.content)

                        file_size = image_file.stat().st_size / 1024
                        print(f"[OK] Downloaded: {image_file.name} ({file_size:.1f} KB)")

                        generated.append({
                            'file': image_file,
                            'tool': anim['tool'],
                            'duration': anim['duration']
                        })
                    else:
                        print(f"[ERROR] Failed to download image: HTTP {response.status_code}")
                else:
                    print(f"[ERROR] No images in result")

            except Exception as e:
                print(f"[ERROR] {str(e)}")
                continue

            # Small delay to avoid rate limits
            time.sleep(1)

        print(f"\n[COMPLETE] Generated {len(generated)}/{len(ANIMATIONS)} animations")
        return generated

    def create_video_from_images(self, animations):
        """Convert images to video clips and assemble"""
        print("\n[2/3] Creating Video from Images...")
        print("-" * 80)

        if not animations:
            print("[ERROR] No animations to process")
            return None

        try:
            import subprocess

            # Create individual video clips from each image
            clips = []
            for i, anim in enumerate(animations, 1):
                clip_file = self.animations_dir / f"clip_{i:02d}.mp4"

                # Convert image to video clip with specified duration
                cmd = [
                    'ffmpeg', '-y',
                    '-loop', '1',
                    '-i', str(anim['file']),
                    '-c:v', 'libx264',
                    '-t', str(anim['duration']),
                    '-pix_fmt', 'yuv420p',
                    '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
                    str(clip_file)
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    clips.append(clip_file)
                    print(f"[OK] Clip {i}/{len(animations)}: {anim['tool']} ({anim['duration']}s)")
                else:
                    print(f"[ERROR] Failed to create clip {i}")

            if not clips:
                print("[ERROR] No clips created")
                return None

            # Create concat file for FFmpeg
            concat_file = self.animations_dir / "concat_list.txt"
            with open(concat_file, 'w') as f:
                for clip in clips:
                    f.write(f"file '{clip.absolute()}'\n")

            # Concatenate all clips
            video_no_audio = self.output_dir / "video_no_audio.mp4"
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                str(video_no_audio)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"[OK] Video assembled: {video_no_audio}")
                return video_no_audio
            else:
                print(f"[ERROR] Failed to concatenate clips: {result.stderr}")
                return None

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def add_audio_to_video(self, video_file):
        """Add narration and background music"""
        print("\n[3/3] Adding Audio...")
        print("-" * 80)

        # Use narration from previous test
        narration = Path("output/test_30sec/narration_30sec.mp3")
        music = Path("output/test_30sec/background_music.mp3")

        if not narration.exists():
            print(f"[ERROR] Narration not found: {narration}")
            print("[INFO] Run create_quick_30sec_test.py first")
            return None

        final_video = self.output_dir / "final_video_30sec.mp4"

        try:
            import subprocess

            if music.exists():
                # Mix narration + music, then add to video
                print("[INFO] Mixing narration + background music...")
                cmd = [
                    'ffmpeg', '-y',
                    '-i', str(video_file),
                    '-i', str(narration),
                    '-i', str(music),
                    '-filter_complex', '[1:a][2:a]amix=inputs=2:duration=shortest:weights=1 0.15[a]',
                    '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy', '-c:a', 'aac',
                    '-shortest',
                    str(final_video)
                ]
            else:
                # Just add narration
                print("[INFO] Adding narration only...")
                cmd = [
                    'ffmpeg', '-y',
                    '-i', str(video_file),
                    '-i', str(narration),
                    '-c:v', 'copy', '-c:a', 'aac',
                    '-shortest',
                    str(final_video)
                ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                file_size = final_video.stat().st_size / 1024 / 1024
                print(f"[OK] Final video: {final_video}")
                print(f"[SIZE] {file_size:.2f} MB")
                return final_video
            else:
                print(f"[ERROR] Failed to add audio: {result.stderr}")
                return None

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def run(self):
        """Execute complete pipeline"""
        print("\nStarting enhanced 30-second video generation...\n")

        # Generate animations
        animations = self.generate_animations()

        if not animations:
            print("\n[FAILED] No animations generated")
            return None

        # Create video from images
        video_no_audio = self.create_video_from_images(animations)

        if not video_no_audio:
            print("\n[FAILED] Could not create video")
            return None

        # Add audio
        final_video = self.add_audio_to_video(video_no_audio)

        # Summary
        print("\n" + "="*80)
        print("PIPELINE COMPLETE")
        print("="*80)

        if final_video:
            print(f"\n[OK] SUCCESS! Enhanced video created!")
            print(f"\nFinal video: {final_video}")
            print(f"Animations: {len(animations)} images")
            print(f"\nFiles location:")
            print(f"  - Final video: {final_video}")
            print(f"  - Animations: {self.animations_dir}/")
        else:
            print("\n[FAILED] Could not complete video")

        print("\n" + "="*80)
        return final_video

if __name__ == "__main__":
    if not APIConfig.FAL_API_KEY:
        print("[ERROR] FAL_API_KEY not configured")
        print("[FIX] Add FAL_API_KEY to .env file")
        sys.exit(1)

    pipeline = Enhanced30SecVideo()
    result = pipeline.run()

    if result:
        print(f"\n[SUCCESS] Video ready: {result}")
        sys.exit(0)
    else:
        print("\n[FAILED] Pipeline failed")
        sys.exit(1)
