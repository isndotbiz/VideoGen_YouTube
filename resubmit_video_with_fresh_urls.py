#!/usr/bin/env python3
"""Resubmit video render with fresh signed URLs"""

import os
import json
import logging
import requests
import boto3
from pathlib import Path
from typing import List, Dict, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Timing configuration
SECTION_TIMINGS = {
    "title": 5.0,
    "intro_fast": 12.0,
    "intro_slow": 18.0,
    "section_normal": 18.0,
    "conclusion": 20.0,
    "transition": 2.0
}

def calculate_image_duration(image_index: int, total_images: int) -> float:
    """Calculate duration for each image"""
    if image_index == 0:
        return SECTION_TIMINGS["title"]
    if 1 <= image_index <= 3:
        return SECTION_TIMINGS["intro_fast"] / 3
    if 4 <= image_index <= 5:
        return SECTION_TIMINGS["intro_slow"] / 2
    if image_index >= total_images - 5:
        return SECTION_TIMINGS["conclusion"]
    return SECTION_TIMINGS["section_normal"]

def generate_signed_urls() -> Tuple[Optional[List[str]], Optional[str], Optional[Dict]]:
    """Generate FRESH signed URLs for S3 images"""
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    bucket = os.getenv("AWS_S3_BUCKET")

    if not all([aws_key, aws_secret, bucket]):
        logger.error("Missing AWS credentials")
        return None, None, None

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        # Get local images
        images_dir = Path("output/generated_images")
        if not images_dir.exists():
            logger.error(f"Images directory not found: {images_dir}")
            return None, None, None

        images = sorted(list(images_dir.glob("*.png")))
        logger.info(f"Found {len(images)} images locally")
        logger.info(f"Generating FRESH signed URLs (24-hour expiry)...")

        image_urls = []
        image_metadata = {}

        for i, img_path in enumerate(images):
            s3_key = f"video-generation/{img_path.name}"

            # Generate FRESH signed URL valid for 24 hours
            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': s3_key},
                ExpiresIn=86400  # 24 hours
            )
            image_urls.append(signed_url)

            duration = calculate_image_duration(i, len(images))
            image_metadata[i] = {
                "filename": img_path.name,
                "duration": duration,
                "s3_key": s3_key
            }

            if (i + 1) % 10 == 0:
                logger.info(f"[{i+1}/{len(images)}] Generated signed URLs")

        logger.info(f"\nGenerated {len(image_urls)} FRESH signed URLs")

        # Generate signed URL for narration
        narration_path = Path("output/narration_enhanced.mp3")
        if not narration_path.exists():
            logger.error(f"Narration file not found")
            return None, None, None

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
        return None, None, None

def build_video_clips(image_urls: List[str], metadata: Dict) -> List[Dict]:
    """Build Shotstack video clips"""
    clips = []
    current_time = 0.0
    transition_duration = SECTION_TIMINGS["transition"]
    total_images = len(image_urls)

    for i, url in enumerate(image_urls):
        duration = metadata[i]["duration"]

        clip = {
            "asset": {
                "type": "image",
                "src": url
            },
            "start": current_time,
            "length": duration,
            "fit": "cover",
            "scale": 1.0,
            "transition": {
                "in": "fade",
                "out": "fade"
            }
        }

        clips.append(clip)
        current_time += duration - transition_duration

    return clips

def submit_render(image_urls: List[str], narration_url: str, metadata: Dict) -> Tuple[bool, Optional[str]]:
    """Submit render to Shotstack with fresh URLs"""
    api_key = os.getenv("SHOTSTACK_API_KEY")
    if not api_key:
        logger.error("SHOTSTACK_API_KEY not set")
        return False, None

    total_images = len(image_urls)
    total_duration = sum(metadata[i]["duration"] for i in range(total_images))

    logger.info(f"\n{'='*60}")
    logger.info("REGENERATING VIDEO WITH FRESH URLS")
    logger.info(f"{'='*60}")
    logger.info(f"Total Images: {total_images}")
    logger.info(f"Total Duration: {total_duration:.1f}s ({total_duration/60:.2f} minutes)")
    logger.info(f"Resolution: 1080p")
    logger.info(f"{'='*60}\n")

    # Build clips
    logger.info("Building video clips...")
    clips = build_video_clips(image_urls, metadata)
    logger.info(f"Created {len(clips)} video clips")

    # Build Shotstack edit
    edit = {
        "timeline": {
            "soundtrack": {
                "src": narration_url,
                "effect": "fadeOut",
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

    # Submit render
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    render_request = {
        "timeline": edit["timeline"],
        "output": edit["output"]
    }

    logger.info("Submitting render to Shotstack API...")
    try:
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
            logger.info("SUCCESS: RENDER JOB SUBMITTED (FRESH URLS)")
            logger.info(f"{'='*60}")
            logger.info(f"Render ID: {render_id}")
            logger.info(f"Duration: {total_duration/60:.2f} minutes")
            logger.info(f"Images: {total_images}")
            logger.info(f"{'='*60}\n")

            return True, render_id
        else:
            logger.error(f"Render submission failed: {response.text}")
            return False, None

    except Exception as e:
        logger.error(f"Video assembly failed: {e}")
        return False, None

def main():
    logger.info("=" * 60)
    logger.info("REGENERATING VIDEO WITH FRESH SIGNED URLS")
    logger.info("=" * 60 + "\n")

    # Generate fresh signed URLs
    image_urls, narration_url, metadata = generate_signed_urls()

    if not image_urls or not narration_url:
        logger.error("Failed to generate signed URLs")
        return False

    # Submit render
    success, render_id = submit_render(image_urls, narration_url, metadata)

    if success and render_id:
        logger.info(f"New Render ID: {render_id}")
        logger.info("Save this ID to check status later\n")
        return True

    return False

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    success = main()
    exit(0 if success else 1)
