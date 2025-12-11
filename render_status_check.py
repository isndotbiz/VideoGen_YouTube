#!/usr/bin/env python3
"""Check and download completed render from Shotstack"""

import os
import json
import requests

# Set API key directly (reading from .env simulation)
SHOTSTACK_API_KEY = "zZzUDIrXAe2WW3ddq0lS8j73hbrevSYAiT8NjpM8"
render_id = "5c91823b-7a80-47c5-9223-2a2385ce50cf"

print("=" * 60)
print("SHOTSTACK RENDER STATUS CHECK")
print("=" * 60)
print(f"Render ID: {render_id}\n")

headers = {"x-api-key": SHOTSTACK_API_KEY}
url = f"https://api.shotstack.io/v1/render/{render_id}"

try:
    print(f"Checking: {url}\n")
    response = requests.get(url, headers=headers, timeout=10)

    print(f"HTTP Response: {response.status_code}\n")

    if response.status_code == 200:
        data = response.json()
        status = data.get("response", {})

        print(f"Status: {status.get('status', 'Unknown')}")
        print(f"Progress: {status.get('progress', 0)}%")
        print(f"Owner: {status.get('owner', 'N/A')}")

        if status.get('status') == 'done':
            print("\n" + "=" * 60)
            print("VIDEO RENDER COMPLETE!")
            print("=" * 60)
            download_url = status.get('url')
            print(f"Download URL: {download_url}")
            print(f"File size: {status.get('size', 'Unknown')} bytes")
            print(f"Duration: {status.get('duration', 'Unknown')} seconds")

            # Download the video
            if download_url:
                print(f"\nDownloading to: output/claude_codex_video.mp4")
                video_response = requests.get(download_url, timeout=60)

                if video_response.status_code == 200:
                    with open("output/claude_codex_video.mp4", "wb") as f:
                        f.write(video_response.content)

                    size_mb = len(video_response.content) / (1024 * 1024)
                    print(f"✓ Downloaded successfully: {size_mb:.1f}MB")
                else:
                    print(f"Download failed: HTTP {video_response.status_code}")
        else:
            print(f"\nCurrent Phase: {status.get('status').upper()}")
            print("Render is still processing...")

    else:
        print(f"API Error: {response.text}")

except Exception as e:
    print(f"Error: {e}")
