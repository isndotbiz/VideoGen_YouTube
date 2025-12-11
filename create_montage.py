#!/usr/bin/env python3
"""
Quick video montage creator for Claude Code Showcase
Creates a slideshow with crossfade transitions and narration overlay
"""

import os
import glob
from pathlib import Path
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip
)
from moviepy.video.fx.all import fadein, fadeout

# Configuration
OUTPUT_DIR = Path("D:/workspace/True_Nas/firecrawl-mdjsonl/output")
IMAGES_DIR = OUTPUT_DIR / "generated_images"
NARRATION_FILE = OUTPUT_DIR / "narration_enhanced.mp3"
OUTPUT_FILE = OUTPUT_DIR / "claude_codex_montage.mp4"

# Video settings
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
FPS = 30
CROSSFADE_DURATION = 1.0  # 1 second crossfade between images

def create_montage():
    print("Starting montage creation...")

    # Get all images sorted by filename
    image_files = sorted(glob.glob(str(IMAGES_DIR / "*.png")))
    print(f"Found {len(image_files)} images")

    # Load audio to get duration
    audio = AudioFileClip(str(NARRATION_FILE))
    audio_duration = audio.duration
    print(f"Audio duration: {audio_duration:.2f} seconds ({audio_duration/60:.2f} minutes)")

    # Calculate time per image (accounting for crossfades)
    num_images = len(image_files)
    total_crossfade_time = (num_images - 1) * CROSSFADE_DURATION
    available_time = audio_duration - total_crossfade_time
    time_per_image = available_time / num_images

    print(f"Time per image: {time_per_image:.2f} seconds")
    print(f"Total crossfade time: {total_crossfade_time:.2f} seconds")

    # Create image clips with crossfade
    clips = []
    for i, img_path in enumerate(image_files):
        print(f"Processing image {i+1}/{num_images}: {Path(img_path).name}")

        # Create image clip
        clip = (ImageClip(img_path)
                .set_duration(time_per_image + CROSSFADE_DURATION)
                .resize(height=VIDEO_HEIGHT))

        # Center crop to 1920x1080 if wider than aspect ratio
        if clip.w > VIDEO_WIDTH:
            clip = clip.crop(x_center=clip.w/2, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)

        # Apply crossfade (fade out at end)
        if i > 0:
            clip = clip.fadein(CROSSFADE_DURATION)
        if i < num_images - 1:
            clip = clip.fadeout(CROSSFADE_DURATION)

        clips.append(clip)

    print("Concatenating clips with crossfades...")
    # Concatenate with overlap for crossfade effect
    final_clips = [clips[0]]
    current_time = clips[0].duration - CROSSFADE_DURATION

    for i in range(1, len(clips)):
        clip = clips[i].set_start(current_time)
        final_clips.append(clip)
        current_time += clips[i].duration - CROSSFADE_DURATION

    # Compose all clips
    video = CompositeVideoClip(final_clips, size=(VIDEO_WIDTH, VIDEO_HEIGHT))

    # Add black letterbox fade in/out (2 seconds each)
    print("Adding fade in/out effects...")
    video = fadein(video, duration=2.0)
    video = fadeout(video, duration=2.0)

    # Set audio
    video = video.set_audio(audio)

    # Ensure video matches audio duration exactly
    video = video.set_duration(audio_duration)

    print(f"Writing video to: {OUTPUT_FILE}")
    print("This may take several minutes...")

    # Write video file
    video.write_videofile(
        str(OUTPUT_FILE),
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        bitrate='8000k',
        threads=4,
        verbose=False,
        logger=None
    )

    print("\nMontage creation complete!")

    # Get file size
    file_size = OUTPUT_FILE.stat().st_size
    file_size_mb = file_size / (1024 * 1024)

    print(f"Output file: {OUTPUT_FILE}")
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Duration: {audio_duration:.2f} seconds ({audio_duration/60:.2f} minutes)")
    print(f"Resolution: {VIDEO_WIDTH}x{VIDEO_HEIGHT} @ {FPS}fps")

    return OUTPUT_FILE, file_size_mb

if __name__ == "__main__":
    create_montage()
