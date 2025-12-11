#!/usr/bin/env python3
"""
Enhanced Long-Form Video Assembly for Shotstack
Handles 30+ images with variable timing, transitions, and section-based pacing
Duration: 9-10 minutes @ 1080p, 30fps, H.264
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


# Timing configuration for different sections
SECTION_TIMINGS = {
    "title": 5.0,           # Title card duration
    "intro_fast": 12.0,     # Images 1-3: quick intro (4 seconds each)
    "intro_slow": 18.0,     # Images 4-5: key points (9 seconds each)
    "section_normal": 18.0, # Most images: standard narration pace
    "conclusion": 20.0,     # Final images: allow for wrap-up
    "transition": 2.0       # Crossfade transition duration
}

# Section boundaries (image indices)
SECTION_BOUNDARIES = {
    "title": (0, 1),        # Title card
    "intro_fast": (1, 4),   # Images 1-3
    "intro_slow": (4, 6),   # Images 4-5
    "section_2": (6, 12),   # Images 6-11
    "section_3": (12, 18),  # Images 12-17
    "section_4": (18, 24),  # Images 18-23
    "section_5": (24, 30),  # Images 24-29
    "conclusion": (30, None) # Images 30+
}


def calculate_image_duration(image_index: int, total_images: int) -> float:
    """Calculate duration for each image based on section"""

    # Title card
    if image_index == 0:
        return SECTION_TIMINGS["title"]

    # Intro - fast section (images 1-3)
    if 1 <= image_index <= 3:
        return SECTION_TIMINGS["intro_fast"] / 3  # ~4 seconds each

    # Intro - slow section (images 4-5, key points)
    if 4 <= image_index <= 5:
        return SECTION_TIMINGS["intro_slow"] / 2  # ~9 seconds each

    # Conclusion (last 3-5 images)
    if image_index >= total_images - 5:
        return SECTION_TIMINGS["conclusion"]

    # Normal section pacing
    return SECTION_TIMINGS["section_normal"]


def calculate_total_duration(image_count: int) -> float:
    """Calculate total video duration based on image count"""
    total = 0.0
    for i in range(image_count):
        total += calculate_image_duration(i, image_count)
    return total


def generate_signed_urls() -> Tuple[Optional[List[str]], Optional[str], Optional[Dict]]:
    """Generate signed URLs for S3 images (valid for 24 hours)"""
    import boto3

    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    bucket = os.getenv("AWS_S3_BUCKET")

    if not all([aws_key, aws_secret, bucket]):
        logger.error("Missing AWS credentials in .env file")
        logger.error("Required: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET")
        return None, None, None

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        # Get all images
        images_dir = Path("output/generated_images")
        if not images_dir.exists():
            logger.error(f"Images directory not found: {images_dir}")
            return None, None, None

        images = sorted(list(images_dir.glob("*.png")))

        if len(images) < 10:
            logger.warning(f"Only {len(images)} images found. Long-form videos typically need 30+")

        logger.info(f"Found {len(images)} images in {images_dir}")
        logger.info(f"Generating signed URLs (24-hour expiry)...")

        image_urls = []
        image_metadata = {}

        for i, img_path in enumerate(images):
            s3_key = f"video-generation/{img_path.name}"

            # Generate signed URL valid for 24 hours
            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': s3_key},
                ExpiresIn=86400  # 24 hours
            )
            image_urls.append(signed_url)

            # Store metadata
            duration = calculate_image_duration(i, len(images))
            image_metadata[i] = {
                "filename": img_path.name,
                "duration": duration,
                "s3_key": s3_key
            }

            logger.info(f"[{i+1}/{len(images)}] {img_path.name} - Duration: {duration:.1f}s")

        logger.info(f"\nGenerated {len(image_urls)} signed URLs")

        # Generate signed URL for narration
        narration_path = Path("output/narration.mp3")
        if not narration_path.exists():
            logger.error(f"Narration file not found: {narration_path}")
            return None, None, None

        logger.info(f"\nGenerating signed URL for narration: {narration_path.name}")
        narration_s3_key = "video-generation/narration.mp3"
        narration_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': narration_s3_key},
            ExpiresIn=86400
        )
        logger.info("Narration URL generated")

        return image_urls, narration_url, image_metadata

    except Exception as e:
        logger.error(f"Error generating signed URLs: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


def build_video_clips(image_urls: List[str], metadata: Dict) -> List[Dict]:
    """Build Shotstack video clips with transitions and variable timing"""
    clips = []
    current_time = 0.0
    transition_duration = SECTION_TIMINGS["transition"]

    total_images = len(image_urls)

    for i, url in enumerate(image_urls):
        duration = metadata[i]["duration"]

        # Determine transition type (using valid Shotstack transitions)
        if i == 0:
            # First image: fade in only
            transition = {
                "in": "fade",
                "out": "fade"
            }
        elif i == total_images - 1:
            # Last image: fade out
            transition = {
                "in": "fade",
                "out": "fadeSlow"  # Slower fade out for conclusion
            }
        else:
            # Middle images: smooth fades between images
            transition = {
                "in": "fade",
                "out": "fade"
            }

        clip = {
            "asset": {
                "type": "image",
                "src": url
            },
            "start": current_time,
            "length": duration,
            "fit": "cover",  # Ensure images fill frame
            "scale": 1.0,
            "transition": transition
        }

        clips.append(clip)

        # Overlap clips by transition duration for smooth transitions
        current_time += duration - transition_duration

        logger.debug(f"Clip {i+1}: Start={current_time:.1f}s, Duration={duration:.1f}s")

    return clips


def assemble_longform_video() -> Tuple[bool, Optional[str]]:
    """Submit long-form video assembly to Shotstack using signed URLs"""
    api_key = os.getenv("SHOTSTACK_API_KEY")
    if not api_key:
        logger.error("SHOTSTACK_API_KEY not set in .env file")
        return False, None

    # Generate signed URLs (valid for 24 hours)
    image_urls, narration_url, metadata = generate_signed_urls()

    if not image_urls or not narration_url or not metadata:
        logger.error("Failed to generate signed URLs")
        return False, None

    try:
        import requests

        total_images = len(image_urls)
        total_duration = calculate_total_duration(total_images)

        logger.info(f"\n{'='*60}")
        logger.info("VIDEO ASSEMBLY CONFIGURATION")
        logger.info(f"{'='*60}")
        logger.info(f"Total Images: {total_images}")
        logger.info(f"Total Duration: {total_duration:.1f}s ({total_duration/60:.2f} minutes)")
        logger.info(f"Resolution: 1080p (1920x1080)")
        logger.info(f"Frame Rate: 30fps")
        logger.info(f"Codec: H.264")
        logger.info(f"Transition: {SECTION_TIMINGS['transition']}s crossfade")
        logger.info(f"{'='*60}\n")

        # Build clips with transitions
        logger.info("Building video clips with variable timing...")
        clips = build_video_clips(image_urls, metadata)
        logger.info(f"Created {len(clips)} video clips")

        # Build Shotstack edit JSON
        edit = {
            "timeline": {
                "soundtrack": {
                    "src": narration_url,
                    "effect": "fadeOut",  # Fade out at end
                    "volume": 1.0
                },
                "tracks": [
                    {
                        "clips": clips
                    }
                ]
            },
            "output": {
                "format": "mp4",
                "resolution": "1080"
            }
        }

        # Estimate costs
        cost_per_minute = 0.20  # Shotstack pricing
        estimated_cost = (total_duration / 60) * cost_per_minute
        estimated_render_time = (total_duration / 60) * 1.5  # ~1.5x real-time

        logger.info(f"\n{'='*60}")
        logger.info("RENDER SUBMISSION")
        logger.info(f"{'='*60}")
        logger.info(f"Estimated Cost: ${estimated_cost:.2f}")
        logger.info(f"Estimated Render Time: {estimated_render_time:.0f} minutes")
        logger.info(f"{'='*60}\n")

        # Submit render
        headers = {"x-api-key": api_key, "Content-Type": "application/json"}
        render_request = {
            "timeline": edit["timeline"],
            "output": edit["output"]
        }

        logger.info("Submitting render to Shotstack API...")
        response = requests.post(
            "https://api.shotstack.io/v1/render",
            json=render_request,
            headers=headers,
            timeout=30
        )

        if response.status_code not in [200, 201]:
            logger.error(f"Render submission failed: HTTP {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False, None

        response_data = response.json()

        if response_data.get("success") or response.status_code in [200, 201]:
            render_id = response_data.get("response", {}).get("id")

            logger.info(f"\n{'='*60}")
            logger.info("SUCCESS: RENDER JOB SUBMITTED")
            logger.info(f"{'='*60}")
            logger.info(f"Render ID: {render_id}")
            logger.info(f"Status: Queued on Shotstack servers")
            logger.info(f"Duration: {total_duration/60:.2f} minutes")
            logger.info(f"Images: {total_images}")
            logger.info(f"{'='*60}\n")

            logger.info("NEXT STEPS:")
            logger.info(f"1. Monitor progress: https://dashboard.shotstack.io/renders/{render_id}")
            logger.info(f"2. Check status: python check_render_status.py {render_id}")
            logger.info(f"3. Upload to YouTube: python optimized_youtube_uploader.py")
            logger.info(f"\nEstimated completion: {estimated_render_time:.0f} minutes from now")

            # Save render metadata
            metadata_file = Path("output/render_metadata.json")
            render_metadata = {
                "render_id": render_id,
                "total_images": total_images,
                "duration_seconds": total_duration,
                "duration_minutes": total_duration / 60,
                "estimated_cost": estimated_cost,
                "image_metadata": metadata,
                "submitted_at": None  # Add timestamp if needed
            }

            with open(metadata_file, "w") as f:
                json.dump(render_metadata, f, indent=2)
            logger.info(f"\nMetadata saved to: {metadata_file}")

            return True, render_id
        else:
            logger.error(f"Render submission failed: {response.text}")
            return False, None

    except Exception as e:
        logger.error(f"Video assembly failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("ENHANCED LONG-FORM VIDEO ASSEMBLY")
    logger.info("=" * 60 + "\n")

    success, render_id = assemble_longform_video()

    if success:
        logger.info("\n" + "=" * 60)
        logger.info("VIDEO ASSEMBLY COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info(f"Render ID: {render_id}")
    else:
        logger.error("\n" + "=" * 60)
        logger.error("VIDEO ASSEMBLY FAILED")
        logger.error("=" * 60)
        logger.error("Check the error messages above for details")

    exit(0 if success else 1)
