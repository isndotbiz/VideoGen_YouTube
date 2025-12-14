#!/usr/bin/env python3
"""
Shotstack Video Composer - Complete video rendering pipeline
Uploads assets to S3 and submits render job to Shotstack API
"""
import os
import json
import time
import requests
from pathlib import Path
from config import APIConfig

class ShotstackComposer:
    def __init__(self, project_dir="output/best_free_AI_tools"):
        self.project_dir = project_dir
        self.narration_path = f"{project_dir}/narration.mp3"
        self.config_path = f"{project_dir}/shotstack_config.json"
        self.shotstack_api_key = APIConfig.SHOTSTACK_API_KEY
        self.shotstack_api_url = "https://api.shotstack.io/stage/render"

        print(f"\n{'='*80}")
        print(f"SHOTSTACK VIDEO COMPOSER")
        print(f"{'='*80}")
        print(f"[PROJECT] {project_dir}")

        if not self.shotstack_api_key:
            print("[ERROR] SHOTSTACK_API_KEY not configured in .env")
            return

    def upload_to_s3_hotlink(self):
        """Use Hotlink URL service instead of S3 for testing"""
        print(f"\n[STEP 1] PREPARING HOTLINK URLS")
        print("-" * 80)

        try:
            # For local testing, we'll use file:// URLs as fallback
            # In production, upload to S3 and use S3 URLs

            if os.path.exists(self.narration_path):
                # For Shotstack, we need a public URL
                # Use a simple HTTP server or S3 in production
                print(f"[INFO] Narration file found: {self.narration_path}")
                print(f"[NOTE] In production, upload to S3 and use S3 URL")

                # For now, use file:// as fallback
                narration_url = f"file://{os.path.abspath(self.narration_path)}"
                print(f"[URL] {narration_url}")
                return narration_url
            else:
                print(f"[ERROR] Narration file not found: {self.narration_path}")
                return None

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def build_shotstack_payload(self, narration_url):
        """Build complete Shotstack render payload"""
        print(f"\n[STEP 2] BUILDING SHOTSTACK PAYLOAD")
        print("-" * 80)

        try:
            # Load the template config
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            # Update with actual narration URL
            config["timeline"]["soundtrack"]["src"] = narration_url

            # Build complete render payload
            payload = {
                "timeline": config["timeline"],
                "output": config["output"],
                "callback": ""  # Leave empty for now, or provide webhook URL
            }

            print(f"[CONFIG] Payload prepared")
            print(f"[DURATION] {config['timeline']['clips'][0]['duration']} seconds")
            print(f"[RESOLUTION] {config['output']['resolution']}")

            return payload

        except Exception as e:
            print(f"[ERROR] Failed to build payload: {str(e)}")
            return None

    def submit_render_job(self, payload):
        """Submit render job to Shotstack API"""
        print(f"\n[STEP 3] SUBMITTING RENDER JOB TO SHOTSTACK")
        print("-" * 80)

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.shotstack_api_key}"
            }

            print(f"[API] Sending request to Shotstack...")
            print(f"[URL] {self.shotstack_api_url}")

            response = requests.post(
                self.shotstack_api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 201:
                result = response.json()
                render_id = result.get("response", {}).get("id")
                print(f"[OK] Render job submitted!")
                print(f"[RENDER_ID] {render_id}")
                return render_id
            else:
                print(f"[ERROR] {response.status_code}: {response.text[:500]}")
                return None

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def check_render_status(self, render_id):
        """Check status of render job"""
        print(f"\n[STEP 4] MONITORING RENDER PROGRESS")
        print("-" * 80)

        try:
            status_url = f"https://api.shotstack.io/stage/render/{render_id}"
            headers = {
                "Authorization": f"Bearer {self.shotstack_api_key}"
            }

            print(f"[CHECKING] Status for render {render_id}...")

            response = requests.get(status_url, headers=headers, timeout=10)

            if response.status_code == 200:
                result = response.json()
                status = result.get("response", {}).get("status")

                print(f"[STATUS] {status}")

                if status == "done":
                    video_url = result.get("response", {}).get("url")
                    print(f"[OK] Video ready!")
                    print(f"[URL] {video_url}")
                    return video_url
                elif status == "failed":
                    error = result.get("response", {}).get("error")
                    print(f"[ERROR] Render failed: {error}")
                    return None
                else:
                    print(f"[PROGRESS] Still processing... ({status})")
                    return None
            else:
                print(f"[ERROR] {response.status_code}: {response.text[:300]}")
                return None

        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return None

    def download_video(self, video_url, output_filename="video_best_free_ai_tools.mp4"):
        """Download final video from Shotstack"""
        print(f"\n[STEP 5] DOWNLOADING FINAL VIDEO")
        print("-" * 80)

        try:
            output_path = f"{self.project_dir}/{output_filename}"

            print(f"[DOWNLOAD] Fetching video from {video_url}...")
            response = requests.get(video_url, stream=True, timeout=60)

            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                print(f"[OK] Video downloaded!")
                print(f"[FILE] {output_path}")
                print(f"[SIZE] {file_size_mb:.1f} MB")
                return output_path
            else:
                print(f"[ERROR] {response.status_code}")
                return None

        except Exception as e:
            print(f"[ERROR] Download failed: {str(e)}")
            return None

    def run_full_composition(self):
        """Execute complete composition workflow"""

        # Step 1: Upload to hotlink/S3
        narration_url = self.upload_to_s3_hotlink()
        if not narration_url:
            return False

        time.sleep(1)

        # Step 2: Build payload
        payload = self.build_shotstack_payload(narration_url)
        if not payload:
            return False

        time.sleep(1)

        # Step 3: Submit render job
        render_id = self.submit_render_job(payload)
        if not render_id:
            return False

        print(f"\n[INFO] Render job submitted with ID: {render_id}")
        print(f"[NOTE] Shotstack typically takes 1-5 minutes to render")

        # Step 4: Poll for completion
        max_attempts = 60  # Check every 10 seconds for up to 10 minutes
        for attempt in range(max_attempts):
            time.sleep(10)

            video_url = self.check_render_status(render_id)
            if video_url:
                # Step 5: Download video
                final_path = self.download_video(video_url)
                if final_path:
                    print(f"\n{'='*80}")
                    print(f"VIDEO COMPOSITION COMPLETE!")
                    print(f"{'='*80}")
                    print(f"\n[SUCCESS] Final video: {final_path}")
                    return True
                else:
                    return False

            print(f"[WAIT] Attempt {attempt + 1}/{max_attempts}... Checking again in 10 seconds")

        print(f"\n[ERROR] Render timeout after 10 minutes")
        print(f"[NOTE] Check Shotstack dashboard for status: {render_id}")
        return False


def main():
    composer = ShotstackComposer()

    # Check if API key is configured
    if not composer.shotstack_api_key:
        print("\n[SETUP REQUIRED]")
        print("Add SHOTSTACK_API_KEY to your .env file:")
        print("  SHOTSTACK_API_KEY=your_api_key_here")
        print("\nGet your free API key at: https://www.shotstack.io")
        return 1

    success = composer.run_full_composition()

    if success:
        print(f"\n[NEXT] Upload platform versions: python create_platform_versions.py")
        return 0
    else:
        print(f"\n[INFO] Manual approach:")
        print(f"  1. Upload narration to S3")
        print(f"  2. Update shotstack_config.json with S3 URL")
        print(f"  3. Use Shotstack dashboard to submit render job")
        return 1


if __name__ == '__main__':
    exit(main())
