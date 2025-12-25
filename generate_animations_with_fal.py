#!/usr/bin/env python3
"""
Generate Video 1 animations using FAL.ai's image-to-video
Properly sets up FAL_KEY environment variable
1. Generate image with Flux
2. Convert image to video using wan-25-preview/image-to-video
3. Save final video
"""
import os
import sys
from pathlib import Path

# Import config and set FAL_KEY environment variable
from config import APIConfig

# Set environment variable BEFORE importing fal_client
os.environ['FAL_KEY'] = APIConfig.FAL_API_KEY

# Now import fal_client
import fal_client
import time
import requests


class FALImageToVideoGenerator:
    """Generate animations using FAL.ai image-to-video"""

    def __init__(self):
        # FAL API key is already set via environment variable
        self.output_dir = "output/free-ai-tools-course/video_1_the_8_tools/animations"
        os.makedirs(self.output_dir, exist_ok=True)

        self.animations = [
            {
                "index": 1,
                "name": "ChatGPT Interface",
                "image_prompt": "Professional ChatGPT interface screenshot showing text input field and AI response, sleek dark theme, modern UI, high quality 4K",
                "video_prompt": "The camera smoothly pans across the ChatGPT interface as text appears being typed. Focus on the elegant design and responsive UI elements."
            },
            {
                "index": 2,
                "name": "Midjourney Image Grid",
                "image_prompt": "Beautiful grid of 4 different AI-generated artwork images showing various styles (realistic, digital art, 3D render, illustration), Midjourney style, professional gallery layout",
                "video_prompt": "Camera zooms in and pans across the grid of AI artwork images, each image glowing as it becomes highlighted. Smooth elegant transitions between images."
            },
            {
                "index": 3,
                "name": "ElevenLabs Voice",
                "image_prompt": "Sound waveform visualization with glowing audio waves, equalizer bars pulsing, professional audio software interface, neon blue and purple colors, high tech aesthetic",
                "video_prompt": "Smooth animation showing audio waveforms flowing and pulsing with energy. Equalizer bars dancing to a rhythm. Neon glow effects intensifying."
            },
            {
                "index": 4,
                "name": "Claude Analysis",
                "image_prompt": "Professional business analytics dashboard showing data charts, graphs, insights appearing on screen. Claude AI logo. Dark professional theme with accent colors. High quality UI",
                "video_prompt": "Camera reveals the analytics dashboard as data points and insights populate. Smooth transitions between different charts and metrics. Professional and polished."
            },
            {
                "index": 5,
                "name": "Synthesys AI Avatar",
                "image_prompt": "Professional AI avatar character (virtual human) in business attire, speaking pose, professional studio lighting, 3D realistic render, high quality, confident expression",
                "video_prompt": "The AI avatar speaks naturally with mouth movements synchronized to audio. Camera slowly zooms in showing facial expressions and hand gestures."
            },
            {
                "index": 6,
                "name": "Runway Video Editing",
                "image_prompt": "Video editing interface split screen showing raw footage on left side and professionally edited polished video on right. Effects and color grading visible. Modern editor UI",
                "video_prompt": "Camera pans showing the transformation from raw footage to edited video. Effects being applied, colors shifting, transitions appearing dynamically on right side."
            },
            {
                "index": 7,
                "name": "Zapier Workflow",
                "image_prompt": "Automation workflow diagram showing app icons (ChatGPT, Email, CRM, Calendar) connected with flowing arrows and glowing lines. Data flowing between apps. Professional tech aesthetic",
                "video_prompt": "Smooth animation showing data flowing through the connected app workflow. Icons lighting up sequentially. Lines glowing as connections activate. Dynamic and energetic."
            },
            {
                "index": 8,
                "name": "CapCut Editing",
                "image_prompt": "CapCut video editor interface showing timeline with clips, effects, transitions ready to apply. Split view showing raw vs edited result. Professional mobile editor design",
                "video_prompt": "Camera shows the CapCut timeline as effects and transitions are applied in real-time. Smooth transitions between clips. Final polished video appearing on the right side."
            }
        ]

    def generate_image(self, animation: dict) -> str:
        """Generate image using FAL.ai Flux"""
        print(f"\n  [IMAGE] Generating image for {animation['name']}...")

        try:
            result = fal_client.subscribe(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": animation['image_prompt'],
                    "image_size": "landscape_4_3",
                    "num_inference_steps": 24,
                    "guidance_scale": 3.5,
                },
            )

            image_url = result["images"][0]["url"]
            print(f"  [IMAGE] Generated: {image_url[:60]}...")
            return image_url

        except Exception as e:
            print(f"  [ERROR] Image generation failed: {str(e)}")
            return None

    def generate_video_from_image(self, animation: dict, image_url: str) -> str:
        """Convert image to video using wan-25-preview"""
        print(f"  [VIDEO] Converting image to video...")

        try:
            def on_queue_update(update):
                if isinstance(update, fal_client.InProgress):
                    for log in update.logs:
                        print(f"    [LOG] {log['message']}")

            result = fal_client.subscribe(
                "fal-ai/wan-25-preview/image-to-video",
                arguments={
                    "prompt": animation['video_prompt'],
                    "image_url": image_url,
                    "duration": "5",
                    "aspect_ratio": "16:9",
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )

            video_url = result.get("video", {}).get("url")
            if not video_url:
                video_url = result.get("video_url")

            if not video_url:
                print(f"  [ERROR] No video URL in response: {result}")
                return None

            print(f"  [VIDEO] Generated: {video_url[:60]}...")
            return video_url

        except Exception as e:
            print(f"  [ERROR] Video generation failed: {str(e)}")
            return None

    def download_video(self, video_url: str, output_path: str) -> bool:
        """Download video from URL"""
        print(f"  [DOWNLOAD] Saving video...")

        try:
            response = requests.get(video_url, timeout=60, stream=True)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  [OK] Saved: {output_path} ({size_mb:.1f} MB)")
            return True

        except Exception as e:
            print(f"  [ERROR] Download failed: {str(e)}")
            return False

    def generate_animation(self, animation: dict) -> bool:
        """Generate complete animation (image + video)"""
        print(f"\n[ANIMATION {animation['index']}/8] {animation['name']}")

        # Step 1: Generate image
        image_url = self.generate_image(animation)
        if not image_url:
            return False

        time.sleep(1)

        # Step 2: Convert image to video
        video_url = self.generate_video_from_image(animation, image_url)
        if not video_url:
            return False

        time.sleep(1)

        # Step 3: Download video
        output_path = f"{self.output_dir}/animation_{animation['index']:02d}_{animation['name'].lower().replace(' ', '_')}.mp4"
        if self.download_video(video_url, output_path):
            print(f"  [SUCCESS] Animation {animation['index']}/8 complete!")
            return True

        return False

    def generate_all_animations(self):
        """Generate all 8 animations"""
        print("\n" + "=" * 80)
        print("VIDEO 1 ANIMATION GENERATOR - FAL.ai Image-to-Video (WAN-25)")
        print("=" * 80)
        print(f"\nAPI Key: {APIConfig.FAL_API_KEY[:30]}...")
        print(f"Output Directory: {self.output_dir}")
        print(f"Total Animations: 8")
        print(f"Duration Each: 5 seconds")
        print(f"Estimated Time: 2-3 minutes per animation\n")

        successful = 0
        failed = 0

        for animation in self.animations:
            try:
                if self.generate_animation(animation):
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"[ERROR] Unexpected error in animation {animation['index']}: {e}")
                failed += 1

        print("\n" + "=" * 80)
        print(f"SUMMARY: {successful}/8 animations generated successfully")
        print("=" * 80)

        if successful > 0:
            print(f"\n[SUCCESS] Animations ready at:")
            print(f"  {self.output_dir}/")
            print(f"\n[NEXT] Overlay animations onto base video")

        if failed > 0:
            print(f"\n[WARNING] {failed} animations failed to generate")

        return successful, failed


def main():
    generator = FALImageToVideoGenerator()
    successful, failed = generator.generate_all_animations()

    if successful == 8:
        print("\n[COMPLETE] All 8 animations generated!")
        print("[NEXT] Compose final video with animations")
        return 0
    elif successful > 0:
        print(f"\n[PARTIAL] {successful} animations ready, {failed} need retry")
        return 1
    else:
        print("\n[FAILED] Animation generation unsuccessful")
        print("[TIP] Check FAL.ai account status and API key")
        return 1


if __name__ == '__main__':
    sys.exit(main())
