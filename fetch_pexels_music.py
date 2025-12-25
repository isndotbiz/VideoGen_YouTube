#!/usr/bin/env python3
"""
Download background music from Pexels API
"""
import os
import requests
from config import APIConfig

def download_pexels_music(search_term="ambient", output_path="output/pexels_bgm.mp3"):
    """Download background music from Pexels"""

    print("\n" + "=" * 80)
    print("DOWNLOADING BACKGROUND MUSIC FROM PEXELS")
    print("=" * 80)

    url = "https://api.pexels.com/videos/search"

    params = {
        "query": search_term,
        "per_page": 1,
        "page": 1
    }

    headers = {
        "Authorization": APIConfig.PEXELS_API_KEY
    }

    try:
        print(f"\n[INFO] Searching Pexels for: {search_term}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        videos = data.get("videos", [])

        if not videos:
            print(f"[ERROR] No videos found for: {search_term}")
            return None

        video = videos[0]
        video_files = video.get("video_files", [])

        if not video_files:
            print(f"[ERROR] No video files found")
            return None

        # Get the video file URL (preferably HD)
        video_url = None
        for vf in video_files:
            if vf.get("height") == 720:
                video_url = vf.get("link")
                break

        if not video_url:
            video_url = video_files[0].get("link")

        print(f"[INFO] Video URL: {video_url[:60]}...")
        print(f"[DOWNLOAD] Downloading video...")

        # Download video
        video_response = requests.get(video_url, stream=True, timeout=30)
        video_response.raise_for_status()

        temp_video = "temp_pexels_video.mp4"
        with open(temp_video, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"[INFO] Video downloaded: {temp_video}")

        # Extract audio using ffmpeg
        print(f"[AUDIO] Extracting audio from video...")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        import subprocess
        cmd = [
            'ffmpeg', '-i', temp_video,
            '-q:a', '0', '-map', 'a',
            '-y', output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        os.remove(temp_video)

        if os.path.exists(output_path):
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"[SUCCESS] Audio extracted: {output_path} ({file_size_mb:.1f} MB)")
            return output_path
        else:
            print(f"[ERROR] Failed to extract audio")
            return None

    except Exception as e:
        print(f"[ERROR] Failed to download from Pexels: {str(e)}")
        return None


def main():
    music_path = download_pexels_music(
        search_term="ambient music background",
        output_path="output/pexels_ambient_bgm.mp3"
    )

    if music_path:
        print(f"\n[SUCCESS] Background music ready: {music_path}")
        print("[NEXT] Use this file in video composition")
        return 0
    else:
        print("\n[FALLBACK] Using placeholder background music")
        return 1


if __name__ == '__main__':
    exit(main())
