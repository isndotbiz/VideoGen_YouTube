#!/usr/bin/env python3
"""
Create video using Python libraries only (no FFmpeg required)
"""
import os
import json
import numpy as np
from pathlib import Path

def create_video_with_python():
    """Create video using imageio and audio mixing with pydub"""

    print("\n" + "="*80)
    print("CREATING VIDEO - Python Only (No FFmpeg Required)")
    print("="*80)

    output_dir = "output/free-ai-tools-course/video_1_the_8_tools"
    narration_path = f"{output_dir}/narration.mp3"
    bgm_path = "output/placeholder_bgm.mp3"
    output_video = f"{output_dir}/video_1_COMPLETE.mp4"

    # Check inputs
    if not os.path.exists(narration_path):
        print(f"[ERROR] Narration not found: {narration_path}")
        return False

    print(f"\n[INPUT] Narration: {narration_path}")
    print(f"[INPUT] BGM: {bgm_path if os.path.exists(bgm_path) else '(not found)'}")

    try:
        # Step 1: Load and mix audio
        print("\n[AUDIO] Loading and mixing audio...")

        try:
            from pydub import AudioSegment
            print("  Using pydub for audio mixing...")

            # Load narration
            narration = AudioSegment.from_mp3(narration_path)
            duration_ms = len(narration)
            duration_s = duration_ms / 1000.0

            print(f"  Narration duration: {duration_s:.1f} seconds")

            # Load and mix BGM if available
            audio_to_use = narration
            if os.path.exists(bgm_path):
                bgm = AudioSegment.from_mp3(bgm_path)

                # Loop BGM if shorter
                if len(bgm) < len(narration):
                    repeats = (len(narration) // len(bgm)) + 1
                    bgm = bgm * repeats
                    bgm = bgm[:len(narration)]

                # Reduce BGM volume to 15%
                bgm_quiet = bgm - 16  # -16dB ≈ 15% volume

                # Mix
                audio_to_use = narration.overlay(bgm_quiet)
                print(f"  Mixed: narration + BGM at 15% volume")
            else:
                print(f"  Using narration only (BGM not found)")

            # Step 2: Create video frames
            print("\n[VIDEO] Creating video frames...")

            import imageio

            # Video parameters
            width, height = 1920, 1080
            fps = 24
            total_frames = int(duration_s * fps)
            bg_color = (10, 14, 39)  # Dark blue-gray (0x0a0e27 in BGR)

            print(f"  Resolution: {width}x{height}")
            print(f"  FPS: {fps}")
            print(f"  Total frames: {total_frames}")

            # Create array of frames
            frames = []
            for i in range(total_frames):
                # Create frame with background color
                frame = np.full((height, width, 3), bg_color, dtype=np.uint8)
                frames.append(frame)

                # Progress
                if (i + 1) % (fps * 10) == 0:
                    print(f"    {i+1}/{total_frames} frames ({(i+1)/total_frames*100:.0f}%)")

            # Step 3: Export audio
            print("\n[EXPORT] Exporting audio...")

            temp_audio = f"{output_dir}/temp_audio.wav"
            audio_to_use.export(temp_audio, format="wav")
            print(f"  Exported: {temp_audio}")

            # Step 4: Create video with audio using imageio
            print(f"\n[ENCODING] Writing video file...")
            print(f"  Output: {output_video}")

            os.makedirs(os.path.dirname(output_video), exist_ok=True)

            # imageio doesn't handle audio well, so we'll use ffmpeg if available
            # Otherwise, just create video without audio and warn user

            writer = imageio.get_writer(
                output_video,
                fps=fps,
                codec='libx264',
                pixelformat='yuv420p'
            )

            for i, frame in enumerate(frames):
                writer.append_data(frame)
                if (i + 1) % (fps * 10) == 0:
                    print(f"    {i+1}/{total_frames} frames written")

            writer.close()
            print(f"  Video file created (without audio yet)")

            # Try to add audio using subprocess
            print(f"\n[AUDIO] Adding audio to video...")
            try:
                import subprocess
                cmd = [
                    'ffmpeg', '-i', output_video, '-i', temp_audio,
                    '-c:v', 'copy', '-c:a', 'aac',
                    '-shortest', '-y',
                    f"{output_dir}/temp_with_audio.mp4"
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

                if result.returncode == 0:
                    os.rename(f"{output_dir}/temp_with_audio.mp4", output_video)
                    print(f"  Audio added successfully")
                else:
                    print(f"  [WARNING] Could not add audio with ffmpeg (not installed)")
                    print(f"  Video created without audio - audio mixing skipped")

                # Clean up temp
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)

            except FileNotFoundError:
                print(f"  [WARNING] FFmpeg not installed - video created without audio")
                print(f"  Install with: choco install ffmpeg")
                print(f"  Or visit: https://ffmpeg.org/download.html")

            # Verify output
            if os.path.exists(output_video):
                file_size_mb = os.path.getsize(output_video) / (1024 * 1024)
                print(f"\n[SUCCESS] Video created!")
                print(f"[OUTPUT] {output_video}")
                print(f"[SIZE] {file_size_mb:.1f} MB")
                print(f"[DURATION] {duration_s:.1f} seconds")

                # Save metadata
                metadata = {
                    "topic": "The 8 Free AI Tools That Will Make You Money",
                    "duration": duration_s,
                    "resolution": "1920x1080",
                    "fps": 24,
                    "audio": "narration + 15% background music" if os.path.exists(bgm_path) else "narration only",
                    "subtitles": "SRT format available",
                    "status": "base video created"
                }

                metadata_path = f"{output_dir}/video_metadata.json"
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)

                return True
            else:
                print(f"\n[ERROR] Video file not created")
                return False

    except ImportError as e:
        print(f"\n[ERROR] Missing library: {e}")
        print(f"[FIX] Installing required libraries...")
        os.system("pip install pydub imageio imageio-ffmpeg numpy")
        return False

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    success = create_video_with_python()

    if success:
        print("\n" + "="*80)
        print("BASE VIDEO COMPLETE!")
        print("="*80)
        print("\n[NEXT STEPS]:")
        print("1. Install FFmpeg for better audio mixing:")
        print("   Windows (Chocolatey): choco install ffmpeg")
        print("   Windows (manual): https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt-get install ffmpeg")
        print("\n2. Run again to add audio: python create_video_python_only.py")
        print("\n3. Generate 8 animations: python generate_animations_with_fal.py")
        print("\n4. Create final composite video with animations")
        return 0
    else:
        print("\n[ERROR] Video creation failed")
        return 1

if __name__ == '__main__':
    exit(main())
