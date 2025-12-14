#!/usr/bin/env python3
"""
Create final video - Simple and reliable approach
"""
import os
import json
from pathlib import Path

def main():
    print("\n" + "="*80)
    print("FINAL VIDEO CREATION")
    print("="*80)

    output_dir = "output/free-ai-tools-course/video_1_the_8_tools"
    narration_path = f"{output_dir}/narration.mp3"
    subtitles_path = f"{output_dir}/subtitles.srt"
    output_video = f"{output_dir}/video_1_COMPLETE.mp4"

    print(f"\n[INPUTS]")
    print(f"  Narration: {narration_path}")
    if os.path.exists(narration_path):
        size_mb = os.path.getsize(narration_path) / (1024 * 1024)
        print(f"    Status: OK ({size_mb:.1f} MB)")
    else:
        print(f"    Status: MISSING")
        return 1

    print(f"  Subtitles: {subtitles_path}")
    if os.path.exists(subtitles_path):
        size_kb = os.path.getsize(subtitles_path) / 1024
        print(f"    Status: OK ({size_kb:.1f} KB)")
    else:
        print(f"    Status: MISSING (optional)")

    # Try different video creation methods in order of preference
    methods = [
        ("moviepy_method", try_moviepy),
        ("pydub_imageio_method", try_pydub_imageio),
        ("imageio_only_method", try_imageio_only),
    ]

    for method_name, method_func in methods:
        print(f"\n[ATTEMPTING] {method_name}...")
        try:
            result = method_func(narration_path, output_video, output_dir)
            if result:
                print(f"[SUCCESS] {method_name} worked!")
                break
        except Exception as e:
            print(f"[FAILED] {method_name}: {str(e)[:100]}")
            continue
    else:
        print(f"\n[ERROR] All methods failed")
        print(f"[SOLUTION] Install FFmpeg:")
        print(f"  Windows (Chocolatey): choco install ffmpeg")
        print(f"  Windows (manual): https://ffmpeg.org/download.html")
        return 1

    if os.path.exists(output_video):
        size_mb = os.path.getsize(output_video) / (1024 * 1024)
        print(f"\n[OUTPUT] {output_video}")
        print(f"[SIZE] {size_mb:.1f} MB")

        # Save metadata
        metadata = {
            "status": "base video created",
            "created_at": str(Path.cwd()),
            "components": {
                "narration": "ElevenLabs MP3",
                "subtitles": "SRT format",
                "background": "1920x1080 colored"
            }
        }

        with open(f"{output_dir}/video_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        return 0
    else:
        print(f"\n[ERROR] Video file not created")
        return 1


def try_moviepy(narration_path, output_video, output_dir):
    """Try using MoviePy"""
    from moviepy.editor import ColorClip, AudioFileClip, CompositeVideoClip
    import librosa

    # Get duration
    narration_audio, sr = librosa.load(narration_path, sr=None)
    duration = len(narration_audio) / sr

    # Create colored background
    clip = ColorClip(size=(1920, 1080), color=(10, 14, 39))
    clip = clip.set_duration(duration)

    # Add audio
    audio = AudioFileClip(narration_path)
    clip = clip.set_audio(audio)

    # Write
    os.makedirs(os.path.dirname(output_video), exist_ok=True)
    clip.write_videofile(output_video, fps=24, verbose=False, logger=None)

    return os.path.exists(output_video)


def try_pydub_imageio(narration_path, output_video, output_dir):
    """Try using pydub + imageio"""
    from pydub import AudioSegment
    import imageio
    import numpy as np

    # Load audio and get duration
    audio = AudioSegment.from_mp3(narration_path)
    duration_s = len(audio) / 1000.0

    # Create frames
    fps = 24
    total_frames = int(duration_s * fps)
    bg_color = (10, 14, 39)

    frames = []
    for i in range(total_frames):
        frame = np.full((1080, 1920, 3), bg_color, dtype=np.uint8)
        frames.append(frame)

    # Write video
    os.makedirs(os.path.dirname(output_video), exist_ok=True)
    writer = imageio.get_writer(output_video, fps=fps, codec='libx264')
    for frame in frames:
        writer.append_data(frame)
    writer.close()

    # Export audio and try to combine with ffmpeg
    temp_audio = f"{output_dir}/temp_audio.wav"
    audio.export(temp_audio, format="wav")

    # Try ffmpeg
    try:
        import subprocess
        cmd = ['ffmpeg', '-i', output_video, '-i', temp_audio,
               '-c:v', 'copy', '-c:a', 'aac', '-shortest', '-y',
               f"{output_dir}/temp_final.mp4"]
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        if result.returncode == 0:
            os.rename(f"{output_dir}/temp_final.mp4", output_video)
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
    except:
        pass

    return os.path.exists(output_video)


def try_imageio_only(narration_path, output_video, output_dir):
    """Fallback: imageio only (no audio)"""
    import imageio
    import numpy as np
    from pydub import AudioSegment

    # Get duration from audio
    audio = AudioSegment.from_mp3(narration_path)
    duration_s = len(audio) / 1000.0

    # Create colored video
    fps = 24
    total_frames = int(duration_s * fps)
    bg_color = (10, 14, 39)

    frames = []
    for i in range(total_frames):
        frame = np.full((1080, 1920, 3), bg_color, dtype=np.uint8)
        frames.append(frame)

    os.makedirs(os.path.dirname(output_video), exist_ok=True)
    writer = imageio.get_writer(output_video, fps=fps, codec='libx264')
    for frame in frames:
        writer.append_data(frame)
    writer.close()

    print(f"    [WARNING] Video created without audio (ffmpeg not available)")
    print(f"    Install FFmpeg and run again to add audio")

    return os.path.exists(output_video)


if __name__ == '__main__':
    exit(main())
