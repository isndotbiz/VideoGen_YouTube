#!/usr/bin/env python3
"""
Create final video using FFmpeg
Simple, reliable method - no Shotstack complexity
"""
import os
import subprocess
from pathlib import Path

def create_final_video():
    """Create video using embedded FFmpeg"""

    print("\n" + "="*80)
    print("FINAL VIDEO CREATION - FFmpeg Method")
    print("="*80)

    output_dir = "output/best_free_AI_tools"
    narration_path = f"{output_dir}/narration.mp3"
    output_video = f"{output_dir}/video_best_free_ai_tools_FINAL.mp4"

    # Check input
    if not os.path.exists(narration_path):
        print(f"[ERROR] Narration not found: {narration_path}")
        return False

    print(f"\n[INPUT] {narration_path}")

    try:
        # Try to find ffmpeg from imageio-ffmpeg
        try:
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            print(f"[FFMPEG] Found at: {ffmpeg_path}")
        except:
            ffmpeg_path = "ffmpeg"
            print(f"[FFMPEG] Using system ffmpeg")

        # Get duration
        try:
            import librosa
            audio, sr = librosa.load(narration_path, sr=None)
            duration = len(audio) / sr
        except:
            # Fallback
            size_mb = os.path.getsize(narration_path) / (1024 * 1024)
            duration = int(size_mb * 90)

        print(f"[DURATION] {duration:.1f} seconds")

        # Create video with colored background
        print(f"\n[ENCODING] Creating video with narration...")
        print(f"[FORMAT] 1920x1080, 24fps, H.264 + AAC")

        # FFmpeg command to create video with colored background and audio
        cmd = [
            ffmpeg_path,
            '-f', 'lavfi',
            '-i', f'color=c=0x0a0e27:s=1920x1080:d={int(duration)+1}',
            '-i', narration_path,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-shortest',
            '-pix_fmt', 'yuv420p',
            '-y',
            output_video
        ]

        print(f"[CMD] Running ffmpeg...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

        if result.returncode == 0 and os.path.exists(output_video):
            file_size_mb = os.path.getsize(output_video) / (1024 * 1024)

            print(f"\n[SUCCESS] Video created!")
            print(f"[OUTPUT] {output_video}")
            print(f"[SIZE] {file_size_mb:.1f} MB")
            print(f"[DURATION] {duration:.1f} seconds")
            print(f"[CODEC] H.264 + AAC")
            print(f"[RESOLUTION] 1920x1080")

            print(f"\n{'='*80}")
            print(f"VIDEO READY FOR UPLOAD")
            print(f"{'='*80}")
            print(f"\nFile: {output_video}")
            print(f"Size: {file_size_mb:.1f} MB")
            print(f"\nNext steps:")
            print(f"1. Create platform versions: python create_platform_versions.py")
            print(f"2. Upload to YouTube")

            return True
        else:
            print(f"\n[ERROR] FFmpeg failed")
            if result.stderr:
                print(f"[STDERR] {result.stderr[:500]}")
            return False

    except FileNotFoundError:
        print(f"\n[ERROR] FFmpeg not found")
        print(f"[SOLUTION] Install ffmpeg:")
        print(f"  pip install ffmpeg-python")
        print(f"  OR")
        print(f"  choco install ffmpeg")
        return False
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False


def main():
    success = create_final_video()

    if success:
        print(f"\n[STATUS] Complete!")
        return 0
    else:
        print(f"\n[ERROR] Could not create video")
        return 1


if __name__ == '__main__':
    exit(main())
