#!/usr/bin/env python3
"""
Create platform-specific video versions
Optimizes for YouTube, TikTok, Instagram, and Twitter
"""
import os
import subprocess
import json
from pathlib import Path

def create_platform_versions():
    """Create optimized versions for different platforms"""

    print("\n" + "="*80)
    print("PLATFORM-SPECIFIC VIDEO VERSIONS")
    print("="*80)

    output_dir = "output/free-ai-tools-course/video_1_the_8_tools"
    input_video = f"{output_dir}/video_1_COMPLETE.mp4"
    platforms_dir = f"{output_dir}/platforms"

    # Check input
    if not os.path.exists(input_video):
        print(f"[ERROR] Input video not found: {input_video}")
        return False

    file_size_mb = os.path.getsize(input_video) / (1024 * 1024)
    print(f"\n[INPUT] {input_video}")
    print(f"[SIZE] {file_size_mb:.1f} MB")

    os.makedirs(platforms_dir, exist_ok=True)

    # Get ffmpeg from imageio_ffmpeg
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except:
        ffmpeg_exe = "ffmpeg"

    platforms = [
        {
            "name": "YouTube",
            "filename": "video_1_youtube.mp4",
            "width": 1920,
            "height": 1080,
            "ratio": "16:9",
            "description": "Full HD landscape for desktop"
        },
        {
            "name": "TikTok",
            "filename": "video_1_tiktok.mp4",
            "width": 1080,
            "height": 1920,
            "ratio": "9:16",
            "description": "Vertical format for mobile"
        },
        {
            "name": "Instagram Reels",
            "filename": "video_1_instagram.mp4",
            "width": 1080,
            "height": 1920,
            "ratio": "9:16",
            "description": "Vertical format with safe area"
        },
        {
            "name": "Twitter/X",
            "filename": "video_1_twitter.mp4",
            "width": 1280,
            "height": 720,
            "ratio": "16:9",
            "description": "HD landscape for Twitter"
        }
    ]

    print(f"\n[PLATFORMS] Creating {len(platforms)} versions...\n")

    created_files = []

    for i, platform in enumerate(platforms, 1):
        print(f"[{i}/{len(platforms)}] {platform['name']}")
        print(f"      Resolution: {platform['width']}x{platform['height']} ({platform['ratio']})")
        print(f"      {platform['description']}")

        output_path = f"{platforms_dir}/{platform['filename']}"

        try:
            # Use ffmpeg to resize
            cmd = [
                ffmpeg_exe,
                '-i', input_video,
                '-vf', f"scale={platform['width']}:{platform['height']}:force_original_aspect_ratio=decrease,pad={platform['width']}:{platform['height']}:(ow-iw)/2:(oh-ih)/2",
                '-c:v', 'libx264',
                '-preset', 'fast',
                '-c:a', 'aac',
                '-y', output_path
            ]

            print(f"      Encoding...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"      [OK] Success: {file_size:.1f} MB\n")
                created_files.append({
                    "platform": platform["name"],
                    "file": output_path,
                    "size_mb": file_size,
                    "resolution": f"{platform['width']}x{platform['height']}"
                })
            else:
                print(f"      [FAIL] Failed (FFmpeg error)\n")

        except Exception as e:
            print(f"      [ERROR] {str(e)[:60]}\n")

    # Summary
    if created_files:
        print("="*80)
        print(f"[SUCCESS] {len(created_files)}/{len(platforms)} versions created!")
        print("="*80)

        print(f"\n[OUTPUT FILES]:")
        for f in created_files:
            print(f"  [OK] {f['platform']:20} {f['size_mb']:.1f} MB")

        # Save metadata
        metadata = {
            "base_video": input_video,
            "platforms_created": len(created_files),
            "files": created_files,
            "upload_instructions": {
                "YouTube": "Upload as-is, standard YouTube format",
                "TikTok": "Vertical 9:16 format, optimal for mobile",
                "Instagram": "Portrait format, same as TikTok",
                "Twitter": "Landscape format for Twitter/X feed"
            }
        }

        metadata_path = f"{platforms_dir}/platform_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"\n[METADATA] {metadata_path}")
        print(f"\n[READY] Videos are ready for upload!")
        return True

    else:
        print(f"\n[ERROR] No versions created (FFmpeg may not be available)")
        print(f"[FALLBACK] You can still upload the base video: {input_video}")
        return False


def main():
    success = create_platform_versions()

    if success:
        print("\n" + "="*80)
        print("PLATFORM VERSIONS COMPLETE!")
        print("="*80)
        print("\n[UPLOAD GUIDE]:")
        print("  YouTube: output/free-ai-tools-course/video_1_the_8_tools/platforms/video_1_youtube.mp4")
        print("  TikTok:  output/free-ai-tools-course/video_1_the_8_tools/platforms/video_1_tiktok.mp4")
        print("  Instagram: output/free-ai-tools-course/video_1_the_8_tools/platforms/video_1_instagram.mp4")
        print("  Twitter: output/free-ai-tools-course/video_1_the_8_tools/platforms/video_1_twitter.mp4")
        return 0
    else:
        print("\n[INFO] Base video is ready: output/free-ai-tools-course/video_1_the_8_tools/video_1_COMPLETE.mp4")
        return 1


if __name__ == '__main__':
    exit(main())
