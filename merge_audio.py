#!/usr/bin/env python3
"""
Merge audio with video using imageio-ffmpeg
"""

from pathlib import Path
import subprocess
import sys

# Get ffmpeg from imageio
try:
    from imageio_ffmpeg import get_ffmpeg_exe
    ffmpeg_exe = get_ffmpeg_exe()
    print(f"Found ffmpeg: {ffmpeg_exe}")
except Exception as e:
    print(f"Error getting ffmpeg: {e}")
    sys.exit(1)

OUTPUT_DIR = Path("D:/workspace/True_Nas/firecrawl-mdjsonl/output")
VIDEO_NO_AUDIO = OUTPUT_DIR / "montage_no_audio.mp4"
NARRATION_FILE = OUTPUT_DIR / "narration_enhanced.mp3"
OUTPUT_FILE = OUTPUT_DIR / "claude_codex_montage.mp4"

print(f"Input video: {VIDEO_NO_AUDIO}")
print(f"Input audio: {NARRATION_FILE}")
print(f"Output file: {OUTPUT_FILE}")

# Build ffmpeg command
cmd = [
    ffmpeg_exe, '-y',  # overwrite output
    '-i', str(VIDEO_NO_AUDIO),  # input video
    '-i', str(NARRATION_FILE),  # input audio
    '-c:v', 'libx264',  # re-encode video with H.264
    '-preset', 'medium',  # encoding speed/quality tradeoff
    '-crf', '23',  # quality (lower = better, 18-28 is good range)
    '-c:a', 'aac',  # audio codec
    '-b:a', '192k',  # audio bitrate
    '-shortest',  # finish when shortest stream ends
    '-movflags', '+faststart',  # optimize for web streaming
    str(OUTPUT_FILE)
]

print("\nRunning ffmpeg command...")
print(" ".join(cmd))
print("\nThis may take several minutes...\n")

try:
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("\nAudio merge successful!")

        # Get file size
        if OUTPUT_FILE.exists():
            file_size = OUTPUT_FILE.stat().st_size
            file_size_mb = file_size / (1024 * 1024)

            print(f"\nFinal output: {OUTPUT_FILE}")
            print(f"File size: {file_size_mb:.2f} MB")
            print(f"Resolution: 1920x1080 @ 30fps")
            print("\nVideo is ready to upload to YouTube!")
        else:
            print("ERROR: Output file was not created")
            sys.exit(1)
    else:
        print(f"ERROR: ffmpeg failed with return code {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
