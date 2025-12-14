#!/usr/bin/env python3
"""
Create a simple test video with narration - fast and reliable
"""
import os
import subprocess
import json
from pathlib import Path

def get_audio_duration(audio_path):
    """Get audio duration in seconds using ffprobe"""
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1',
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass

    # Fallback: estimate from file size (rough estimate)
    size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    return size_mb * 90  # Rough estimate: 90 seconds per MB for MP3

def create_video_simple():
    """Create a simple video with colored background and audio"""

    print("\n" + "="*80)
    print("CREATING VIDEO - Simple Method")
    print("="*80)

    output_dir = "output/free-ai-tools-course/video_1_the_8_tools"
    narration_path = f"{output_dir}/narration.mp3"
    bgm_path = "output/placeholder_bgm.mp3"
    subtitles_path = f"{output_dir}/subtitles.srt"
    output_video = f"{output_dir}/video_1_COMPLETE.mp4"

    # Check narration exists
    if not os.path.exists(narration_path):
        print(f"[ERROR] Narration not found: {narration_path}")
        return False

    print(f"\n[INPUT] Narration: {narration_path}")
    print(f"[INPUT] BGM: {bgm_path if os.path.exists(bgm_path) else '(not found - will skip)'}")
    print(f"[INPUT] Subtitles: {subtitles_path if os.path.exists(subtitles_path) else '(not found)'}")

    try:
        # Get narration duration
        print("\n[DURATION] Getting audio duration...")
        duration = get_audio_duration(narration_path)
        print(f"[DURATION] {duration:.1f} seconds")

        # If BGM exists, mix it with narration first
        mixed_audio = narration_path
        if os.path.exists(bgm_path):
            print("\n[MIXING] Mixing narration with background music...")
            mixed_audio = f"{output_dir}/mixed_audio.mp3"

            # Use ffmpeg to mix audio
            # Formula: -filter_complex "[0]aformat=sample_rates=44100:channel_layouts=stereo[a];[1]volume=0.15[b];[a][b]amix=inputs=2:duration=first[out]"
            cmd = [
                'ffmpeg', '-i', narration_path, '-i', bgm_path,
                '-filter_complex',
                '[0]aformat=sample_rates=44100:channel_layouts=stereo[a];[1]volume=0.15[b];[a][b]amix=inputs=2:duration=first[out]',
                '-map', '[out]',
                '-c:a', 'libmp3lame', '-b:a', '128k',
                '-y', mixed_audio
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0 and os.path.exists(mixed_audio):
                print(f"[OK] Mixed audio created: {mixed_audio}")
            else:
                print(f"[WARNING] Audio mixing failed, using narration only")
                mixed_audio = narration_path

        # Create video with colored background
        print("\n[VIDEO] Creating video background...")
        print(f"[VIDEO] Resolution: 1920x1080, Duration: {duration:.1f}s, FPS: 24")

        # Use ffmpeg to create a colored video
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', f'color=c=0x0a0e27:s=1920x1080:d={duration}',
            '-i', mixed_audio,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-c:a', 'aac',
            '-shortest',
            '-y', output_video
        ]

        print(f"[CMD] Running FFmpeg...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode == 0 and os.path.exists(output_video):
            file_size_mb = os.path.getsize(output_video) / (1024 * 1024)
            print(f"\n[SUCCESS] Video created!")
            print(f"[OUTPUT] {output_video}")
            print(f"[SIZE] {file_size_mb:.1f} MB")
            print(f"[DURATION] {duration:.1f} seconds")

            # Save metadata
            metadata = {
                "topic": "The 8 Free AI Tools That Will Make You Money",
                "duration": duration,
                "resolution": "1920x1080",
                "fps": 24,
                "audio": "narration + 15% background music",
                "subtitles": "SRT format",
                "status": "base video created"
            }

            metadata_path = f"{output_dir}/video_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"[METADATA] {metadata_path}")
            return True
        else:
            print(f"\n[ERROR] FFmpeg failed:")
            print(f"Return code: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[:500]}")
            return False

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = create_video_simple()

    if success:
        print("\n" + "="*80)
        print("BASE VIDEO COMPLETE!")
        print("="*80)
        print("\n[NEXT STEPS]:")
        print("1. Generate 8 animations with FAL.ai (python generate_animations_with_fal.py)")
        print("2. Overlay animations on base video")
        print("3. Create platform-specific versions (YouTube, TikTok, Instagram)")
        print("4. Upload to YouTube")
        return 0
    else:
        print("\n[ERROR] Video creation failed")
        return 1

if __name__ == '__main__':
    exit(main())
