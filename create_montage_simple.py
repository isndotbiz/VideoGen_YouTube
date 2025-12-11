#!/usr/bin/env python3
"""
Simple video montage creator using PIL and OpenCV
Creates a slideshow with crossfade transitions
"""

import os
import glob
import cv2
import numpy as np
from pathlib import Path
from PIL import Image

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

# Estimated audio duration (we'll calculate based on file size)
# MP3 typically ~192kbps, file is 6.4MB
AUDIO_FILE_SIZE_MB = 6.4
ESTIMATED_BITRATE_KBPS = 192
ESTIMATED_AUDIO_DURATION = (AUDIO_FILE_SIZE_MB * 8192) / ESTIMATED_BITRATE_KBPS  # seconds

CROSSFADE_DURATION = 1.0  # 1 second crossfade
CROSSFADE_FRAMES = int(FPS * CROSSFADE_DURATION)

def load_and_resize_image(img_path):
    """Load image using PIL and convert to OpenCV format, resize to fit 1920x1080"""
    # Load with PIL for better format support
    img_pil = Image.open(img_path).convert('RGB')
    w, h = img_pil.size

    # Calculate scaling to fit height
    scale = VIDEO_HEIGHT / h
    new_w = int(w * scale)
    new_h = VIDEO_HEIGHT

    img_pil = img_pil.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Convert to OpenCV format (BGR)
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # Center crop if wider than video width
    if new_w > VIDEO_WIDTH:
        x_start = (new_w - VIDEO_WIDTH) // 2
        img_cv = img_cv[:, x_start:x_start + VIDEO_WIDTH]
    # Pad if narrower
    elif new_w < VIDEO_WIDTH:
        pad_left = (VIDEO_WIDTH - new_w) // 2
        pad_right = VIDEO_WIDTH - new_w - pad_left
        img_cv = cv2.copyMakeBorder(img_cv, 0, 0, pad_left, pad_right,
                                    cv2.BORDER_CONSTANT, value=(0, 0, 0))

    return img_cv

def blend_images(img1, img2, alpha):
    """Blend two images with given alpha (0-1)"""
    return cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)

def create_montage():
    print("Starting montage creation...")

    # Get all images sorted by filename
    image_files = sorted(glob.glob(str(IMAGES_DIR / "*.png")))
    print(f"Found {len(image_files)} images")

    # Use estimated audio duration
    audio_duration = ESTIMATED_AUDIO_DURATION
    print(f"Estimated audio duration: {audio_duration:.2f} seconds ({audio_duration/60:.2f} minutes)")

    # Calculate time per image (accounting for crossfades)
    num_images = len(image_files)
    total_crossfade_time = (num_images - 1) * CROSSFADE_DURATION
    available_time = audio_duration - total_crossfade_time - 4.0  # Reserve 4s for fade in/out
    time_per_image = available_time / num_images
    frames_per_image = int(time_per_image * FPS)

    print(f"Time per image: {time_per_image:.2f} seconds")
    print(f"Frames per image: {frames_per_image}")
    print(f"Crossfade frames: {CROSSFADE_FRAMES}")

    # Initialize video writer with H.264 codec
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264
    out = cv2.VideoWriter(str(OUTPUT_VIDEO_NO_AUDIO), fourcc, FPS,
                          (VIDEO_WIDTH, VIDEO_HEIGHT))

    if not out.isOpened():
        print("Failed to open with avc1, trying mp4v...")
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
    total_frames = fade_frames

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

    print(f"\nVideo created (no audio): {total_frames} frames")
    print(f"Video duration: {total_frames/FPS:.2f} seconds")

    # Get file size of video without audio
    file_size_no_audio = OUTPUT_VIDEO_NO_AUDIO.stat().st_size
    file_size_mb = file_size_no_audio / (1024 * 1024)

    print(f"Output file (no audio): {OUTPUT_VIDEO_NO_AUDIO}")
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT} @ {FPS}fps")

    print("\n" + "="*60)
    print("VIDEO CREATED SUCCESSFULLY (WITHOUT AUDIO)")
    print("="*60)
    print("\nTo add audio, run this command in PowerShell or CMD:")
    print(f'\nffmpeg -i "{OUTPUT_VIDEO_NO_AUDIO}" -i "{NARRATION_FILE}" \\')
    print(f'       -c:v copy -c:a aac -b:a 192k -shortest \\')
    print(f'       "{OUTPUT_FILE}"')
    print("\nOr use any video editing tool to merge the audio manually.")
    print("="*60)

    return OUTPUT_VIDEO_NO_AUDIO, file_size_mb

if __name__ == "__main__":
    try:
        output_file, size_mb = create_montage()
        print(f"\nFinal output: {output_file}")
        print(f"Size: {size_mb:.2f} MB")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
