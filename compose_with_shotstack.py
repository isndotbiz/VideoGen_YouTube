#!/usr/bin/env python3
"""
Create final video using Shotstack API (no FFmpeg required)
Shotstack handles all video encoding and composition
"""
import os
import json
import requests
import time
from pathlib import Path

def compose_with_shotstack():
    """Use Shotstack API to compose the final video"""

    print("\n" + "="*80)
    print("VIDEO COMPOSITION - Shotstack API")
    print("="*80)

    from config import APIConfig

    # Check API key
    if not APIConfig.SHOTSTACK_API_KEY:
        print("[ERROR] SHOTSTACK_API_KEY not configured")
        return False

    print(f"\n[AUTH] Shotstack API Key: {APIConfig.SHOTSTACK_API_KEY[:30]}...")

    # File paths
    output_dir = "output/free-ai-tools-course/video_1_the_8_tools"
    narration_path = f"{output_dir}/narration.mp3"
    subtitles_path = f"{output_dir}/subtitles.srt"
    output_video = f"{output_dir}/video_1_COMPLETE.mp4"

    # Verify inputs
    if not os.path.exists(narration_path):
        print(f"[ERROR] Narration not found: {narration_path}")
        return False

    print(f"\n[INPUT] Narration: {narration_path}")
    if os.path.exists(subtitles_path):
        print(f"[INPUT] Subtitles: {subtitles_path}")

    try:
        # Create Shotstack request
        print("\n[SHOTSTACK] Building video request...")

        # Get narration duration
        # Using librosa for accurate duration
        try:
            import librosa
            narration_audio, sr = librosa.load(narration_path, sr=None)
            duration = len(narration_audio) / sr
        except:
            # Fallback estimate
            size_mb = os.path.getsize(narration_path) / (1024 * 1024)
            duration = size_mb * 90

        print(f"[DURATION] {duration:.1f} seconds")

        # Build Shotstack JSON
        shotstack_json = {
            "timeline": {
                "soundtrack": {
                    "src": f"file://{os.path.abspath(narration_path)}"
                },
                "tracks": [
                    {
                        "clips": [
                            {
                                "type": "color",
                                "duration": duration,
                                "color": "#0a0e27"  # Dark blue-gray background
                            }
                        ]
                    }
                ]
            },
            "output": {
                "format": "mp4",
                "resolution": "1920x1080",
                "aspectRatio": "16:9",
                "size": {
                    "width": 1920,
                    "height": 1080
                },
                "frame_rate": 24,
                "bitrate": "8000k",
                "quality": "high"
            }
        }

        print(f"[CONFIG] 1920x1080, 24fps, H.264, Duration: {duration:.1f}s")

        # Make request to Shotstack
        print(f"\n[REQUEST] Sending to Shotstack...")

        headers = {
            "Content-Type": "application/json",
            "x-api-key": APIConfig.SHOTSTACK_API_KEY
        }

        # Shotstack endpoint (using sandbox for testing)
        # Change to https://api.shotstack.io/stage/render for production
        url = "https://api.shotstack.io/stage/render"

        response = requests.post(
            url,
            json=shotstack_json,
            headers=headers,
            timeout=30
        )

        print(f"[RESPONSE] Status: {response.status_code}")

        if response.status_code not in [200, 201, 202]:
            print(f"[ERROR] Shotstack returned: {response.status_code}")
            print(f"[ERROR] Response: {response.text[:500]}")
            return False

        result = response.json()

        if "response" not in result:
            print(f"[ERROR] No response data from Shotstack")
            print(f"[ERROR] {result}")
            return False

        render_id = result["response"].get("id")
        print(f"[RENDER_ID] {render_id}")

        if not render_id:
            print(f"[ERROR] No render ID returned")
            return False

        # Poll for completion
        print(f"\n[POLLING] Waiting for video encoding...")

        max_polls = 120  # 10 minutes max
        poll_interval = 5  # seconds

        for poll_num in range(max_polls):
            # Check status
            status_url = f"https://api.shotstack.io/stage/render/{render_id}"

            status_response = requests.get(
                status_url,
                headers=headers,
                timeout=10
            )

            if status_response.status_code != 200:
                print(f"[ERROR] Status check failed: {status_response.status_code}")
                return False

            status_result = status_response.json()
            status_data = status_result.get("response", {})
            status = status_data.get("status")
            progress = status_data.get("progress", 0)

            print(f"  [{poll_num+1}/{max_polls}] Status: {status}, Progress: {progress}%", end="\r")

            if status == "succeeded":
                print(f"\n[SUCCESS] Video encoding complete!")

                # Get download URL
                output_url = status_data.get("output", {}).get("url")

                if output_url:
                    print(f"[URL] {output_url[:60]}...")

                    # Download video
                    print(f"\n[DOWNLOAD] Downloading video...")

                    video_response = requests.get(output_url, stream=True, timeout=120)
                    video_response.raise_for_status()

                    os.makedirs(os.path.dirname(output_video), exist_ok=True)

                    with open(output_video, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                    if os.path.exists(output_video):
                        file_size_mb = os.path.getsize(output_video) / (1024 * 1024)
                        print(f"[SAVED] {output_video}")
                        print(f"[SIZE] {file_size_mb:.1f} MB")
                        print(f"[DURATION] {duration:.1f} seconds")

                        # Save metadata
                        metadata = {
                            "status": "complete",
                            "tool": "Shotstack API",
                            "duration": duration,
                            "resolution": "1920x1080",
                            "fps": 24,
                            "codec": "H.264",
                            "audio": "AAC",
                            "render_id": render_id
                        }

                        with open(f"{output_dir}/video_metadata.json", "w") as f:
                            json.dump(metadata, f, indent=2)

                        return True
                else:
                    print(f"[ERROR] No download URL in response")
                    return False

            elif status == "failed":
                print(f"\n[ERROR] Video encoding failed")
                print(f"[ERROR] {status_data.get('error', 'Unknown error')}")
                return False

            elif status == "queued" or status == "processing":
                time.sleep(poll_interval)
                continue
            else:
                print(f"\n[ERROR] Unknown status: {status}")
                return False

        print(f"\n[ERROR] Polling timeout after {max_polls * poll_interval} seconds")
        return False

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    success = compose_with_shotstack()

    if success:
        print("\n" + "="*80)
        print("VIDEO COMPOSITION COMPLETE!")
        print("="*80)
        print("\n[NEXT STEPS]:")
        print("1. Video ready: output/free-ai-tools-course/video_1_the_8_tools/video_1_COMPLETE.mp4")
        print("2. Create platform versions: python create_platform_versions.py")
        print("3. Upload to YouTube")
        return 0
    else:
        print("\n[ERROR] Video composition failed")
        return 1


if __name__ == '__main__':
    exit(main())
