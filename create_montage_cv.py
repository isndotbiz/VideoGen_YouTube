#!/usr/bin/env python3
"""
Quick video montage creator using OpenCV and pydub
Creates a slideshow with crossfade transitions and narration overlay
"""

import os
import glob
import cv2
import numpy as np
from pathlib import Path
from pydub import AudioSegment
from pydub.utils import mediainfo
import subprocess

# Configuration
OUTPUT_DIR = Path("D:/workspace/True_Nas/firecrawl-mdjsonl/output")
IMAGES_DIR = OUTPUT_DIR / "generated_images"
NARRATION_FILE = OUTPUT_DIR / "narration_enhanced.mp3"
OUTPUT_VIDEO_NO_AUDIO = OUTPUT_DIR / "montage_no_audio.mp4"
OUTPUT_FILE = OUTPUT_DIR / "claude_codex_montage.mp4"

# Video settings
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30
CROSSFADE_DURATION = 1.0  # 1 second crossfade between images
CROSSFADE_FRAMES = int(FPS * CROSSFADE_DURATION)

def get_audio_duration(audio_file):
    """Get audio duration using pydub"""
    audio = AudioSegment.from_file(str(audio_file))
    return len(audio) / 1000.0  # Convert ms to seconds

def load_and_resize_image(img_path):
    """Load image and resize to fit 1920x1080 maintaining aspect ratio"""
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Failed to load image: {img_path}")

    h, w = img.shape[:2]

    # Calculate scaling to fit height
    scale = VIDEO_HEIGHT / h
    new_w = int(w * scale)
    new_h = VIDEO_HEIGHT

    img_resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    # Center crop if wider than video width
    if new_w > VIDEO_WIDTH:
        x_start = (new_w - VIDEO_WIDTH) // 2
        img_resized = img_resized[:, x_start:x_start + VIDEO_WIDTH]
    # Pad if narrower
    elif new_w < VIDEO_WIDTH:
        pad_left = (VIDEO_WIDTH - new_w) // 2
        pad_right = VIDEO_WIDTH - new_w - pad_left
        img_resized = cv2.copyMakeBorder(img_resized, 0, 0, pad_left, pad_right,
                                         cv2.BORDER_CONSTANT, value=(0, 0, 0))

    return img_resized

def blend_images(img1, img2, alpha):
    """Blend two images with given alpha (0-1)"""
    return cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)

def create_montage():
    print("Starting montage creation with OpenCV...")

    # Get all images sorted by filename
    image_files = sorted(glob.glob(str(IMAGES_DIR / "*.png")))
    print(f"Found {len(image_files)} images")

    # Get audio duration
    audio_duration = get_audio_duration(NARRATION_FILE)
    print(f"Audio duration: {audio_duration:.2f} seconds ({audio_duration/60:.2f} minutes)")

    # Calculate time per image (accounting for crossfades)
    num_images = len(image_files)
    total_crossfade_time = (num_images - 1) * CROSSFADE_DURATION
    available_time = audio_duration - total_crossfade_time
    time_per_image = available_time / num_images
    frames_per_image = int(time_per_image * FPS)

    print(f"Time per image: {time_per_image:.2f} seconds")
    print(f"Frames per image: {frames_per_image}")
    print(f"Crossfade frames: {CROSSFADE_FRAMES}")

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(OUTPUT_VIDEO_NO_AUDIO), fourcc, FPS,
                          (VIDEO_WIDTH, VIDEO_HEIGHT))

    if not out.isOpened():
        raise RuntimeError("Failed to open video writer")

    # Add 2-second fade in from black
    print("Adding fade-in from black...")
    fade_frames = int(2.0 * FPS)
    first_img = load_and_resize_image(image_files[0])
    black_frame = np.zeros((VIDEO_HEIGHT, VIDEO_WIDTH, 3), dtype=np.uint8)

    for i in range(fade_frames):
        alpha = i / fade_frames
        frame = blend_images(black_frame, first_img, alpha)
        out.write(frame)

    # Process each image
    prev_img = None
    total_frames = 0

    for idx, img_path in enumerate(image_files):
        print(f"Processing image {idx+1}/{num_images}: {Path(img_path).name}")

        curr_img = load_and_resize_image(img_path)

        # Crossfade from previous image (except for first)
        if idx > 0 and prev_img is not None:
            for i in range(CROSSFADE_FRAMES):
                alpha = i / CROSSFADE_FRAMES
                frame = blend_images(prev_img, curr_img, alpha)
                out.write(frame)
                total_frames += 1

        # Write full image frames
        for _ in range(frames_per_image):
            out.write(curr_img)
            total_frames += 1

        prev_img = curr_img

    # Add 2-second fade out to black
    print("Adding fade-out to black...")
    for i in range(fade_frames):
        alpha = i / fade_frames
        frame = blend_images(prev_img, black_frame, alpha)
        out.write(frame)
        total_frames += 1

    out.release()

    print(f"Video without audio created: {total_frames} frames")
    print(f"Video duration: {total_frames/FPS:.2f} seconds")

    # Merge video with audio using subprocess (ffmpeg via opencv)
    print("\nMerging video with audio...")

    # Try to find ffmpeg
    ffmpeg_path = "ffmpeg"

    cmd = [
        ffmpeg_path, '-y',
        '-i', str(OUTPUT_VIDEO_NO_AUDIO),
        '-i', str(NARRATION_FILE),
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-movflags', '+faststart',
        str(OUTPUT_FILE)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Audio merge successful!")
    except FileNotFoundError:
        print("ERROR: ffmpeg not found. Trying alternative method...")
        # If ffmpeg is not available, just keep the video without audio
        import shutil
        shutil.copy(OUTPUT_VIDEO_NO_AUDIO, OUTPUT_FILE)
        print("WARNING: Video created without audio sync. Please merge manually.")
        return OUTPUT_FILE, OUTPUT_VIDEO_NO_AUDIO.stat().st_size / (1024 * 1024)
    except subprocess.CalledProcessError as e:
        print(f"ERROR merging audio: {e}")
        print(f"STDERR: {e.stderr}")
        raise

    # Clean up temp file
    if OUTPUT_VIDEO_NO_AUDIO.exists():
        OUTPUT_VIDEO_NO_AUDIO.unlink()

    # Get file size
    file_size = OUTPUT_FILE.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    print("\nMontage creation complete!")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Duration: {audio_duration:.2f} seconds ({audio_duration/60:.2f} minutes)")
    print(f"Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT} @ {FPS}fps")

    return OUTPUT_FILE, file_size_mb

if __name__ == "__main__":
    try:
        create_montage()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
