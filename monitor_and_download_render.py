#!/usr/bin/env python3
"""Monitor render status and download when complete"""

import os
import requests
import time
from pathlib import Path

SHOTSTACK_API_KEY = "zZzUDIrXAe2WW3ddq0lS8j73hbrevSYAiT8NjpM8"
render_id = "617fc235-158b-4309-a8c6-462e2a0eb994"

def check_status():
    """Check render status"""
    headers = {"x-api-key": SHOTSTACK_API_KEY}
    url = f"https://api.shotstack.io/v1/render/{render_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("response", {})
    except:
        pass
    return None

def download_video(url):
    """Download completed video"""
    output_file = Path("output/claude_codex_video.mp4")

    print(f"Downloading: {output_file}")
    try:
        response = requests.get(url, timeout=120, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(output_file, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        pct = (downloaded / total_size) * 100
                        print(f"  Downloaded: {downloaded/1024/1024:.1f}MB ({pct:.0f}%)")

        file_size_mb = output_file.stat().st_size / (1024*1024)
        print(f"✓ Downloaded: {file_size_mb:.1f}MB")
        return True
    except Exception as e:
        print(f"Download error: {e}")
        return False

def main():
    print("=" * 60)
    print("MONITORING RENDER JOB")
    print("=" * 60)
    print(f"Render ID: {render_id}\n")

    check_count = 0
    while check_count < 240:  # Check for up to 2 hours
        status = check_status()

        if not status:
            print(f"[{check_count}] Unable to reach API")
        else:
            current_status = status.get('status', 'unknown')
            progress = status.get('progress', 0)

            print(f"[{check_count}] Status: {current_status} ({progress}%)")

            if current_status == 'done':
                print("\n✓ VIDEO RENDER COMPLETE!")
                download_url = status.get('url')
                if download_url:
                    if download_video(download_url):
                        print("\n" + "=" * 60)
                        print("VIDEO READY: output/claude_codex_video.mp4")
                        print("=" * 60)
                        return True
            elif current_status == 'failed':
                print(f"\n✗ RENDER FAILED!")
                print(f"Error: {status.get('error', 'Unknown')}")
                return False

        check_count += 1
        if check_count < 240:
            time.sleep(30)  # Check every 30 seconds

    print("\nTimeout: Render taking longer than expected")
    print("You can check manually with:")
    print(f"  python render_status_check.py")
    return False

if __name__ == "__main__":
    main()
