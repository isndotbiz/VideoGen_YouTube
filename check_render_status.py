#!/usr/bin/env python3
"""Check Shotstack render status and download when complete"""

import os
import json
import requests
import time
from pathlib import Path

def check_render_status(render_id):
    """Check the current status of a render job"""
    api_key = os.getenv("SHOTSTACK_API_KEY")
    if not api_key:
        print("ERROR: SHOTSTACK_API_KEY not set")
        return None
    
    headers = {"x-api-key": api_key}
    url = f"https://api.shotstack.io/v1/render/{render_id}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            status_data = data.get("response", {})
            return status_data
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    render_id = "5c91823b-7a80-47c5-9223-2a2385ce50cf"
    
    print("=" * 60)
    print("CHECKING RENDER STATUS")
    print("=" * 60)
    print(f"Render ID: {render_id}\n")
    
    # Check status
    status = check_render_status(render_id)
    
    if status:
        print(f"\nStatus: {status.get('status', 'Unknown')}")
        print(f"Progress: {status.get('progress', 'N/A')}%")
        
        if status.get('status') == 'done':
            print(f"\n✓ Video READY!")
            print(f"Download URL: {status.get('url', 'N/A')}")
            
            # Try to download
            if status.get('url'):
                output_file = Path("output/claude_codex_video.mp4")
                print(f"\nDownloading to: {output_file}")
                
                try:
                    response = requests.get(status.get('url'), timeout=30)
                    if response.status_code == 200:
                        with open(output_file, 'wb') as f:
                            f.write(response.content)
                        file_size = output_file.stat().st_size / (1024*1024)
                        print(f"✓ Downloaded successfully: {file_size:.1f}MB")
                    else:
                        print(f"Download failed: HTTP {response.status_code}")
                except Exception as e:
                    print(f"Download error: {e}")
        elif status.get('status') == 'rendering':
            print(f"Still rendering... {status.get('progress', '?')}% complete")
        elif status.get('status') == 'queued':
            print("Job queued, waiting for processing...")
    else:
        print("Failed to retrieve status")

if __name__ == "__main__":
    main()
