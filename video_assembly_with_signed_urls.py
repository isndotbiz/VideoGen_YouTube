#!/usr/bin/env python3
"""Shotstack video assembly with S3 Signed URLs (no public access needed)"""

import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_signed_urls():
    """Generate signed URLs for S3 images (valid for 24 hours)"""
    import boto3

    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    bucket = os.getenv("AWS_S3_BUCKET")

    if not all([aws_key, aws_secret, bucket]):
        logger.error("Missing AWS credentials")
        return None, None

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        # Get all images
        images_dir = Path("output/generated_images")
        images = sorted(list(images_dir.glob("*.png")))

        logger.info(f"Generating signed URLs for {len(images)} images...")
        image_urls = []

        for i, img_path in enumerate(images, 1):
            s3_key = f"video-generation/{img_path.name}"

            # Generate signed URL valid for 24 hours
            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': s3_key},
                ExpiresIn=86400  # 24 hours
            )
            image_urls.append(signed_url)
            logger.info(f"[{i}/{len(images)}] {img_path.name}")

        logger.info(f"Generated {len(image_urls)} signed URLs\n")

        # Generate signed URL for narration
        logger.info("Generating signed URL for narration...")
        narration_s3_key = "video-generation/narration.mp3"
        narration_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': narration_s3_key},
            ExpiresIn=86400
        )
        logger.info("Narration URL generated\n")

        return image_urls, narration_url

    except Exception as e:
        logger.error(f"Error generating signed URLs: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def assemble_video():
    """Submit video assembly to Shotstack using signed URLs"""
    api_key = os.getenv("SHOTSTACK_API_KEY")
    if not api_key:
        logger.error("SHOTSTACK_API_KEY not set")
        return False

    # Generate signed URLs (valid for 24 hours)
    image_urls, narration_url = generate_signed_urls()

    if not image_urls or not narration_url:
        logger.error("Failed to generate signed URLs")
        return False

    try:
        import requests

        logger.info(f"Building video assembly with {len(image_urls)} signed image URLs...")

        # Build clips from signed URLs (5 seconds each)
        clips = []
        for url in image_urls:
            clips.append({
                "asset": {
                    "type": "image",
                    "src": url
                },
                "start": 0,
                "length": 5
            })

        # Build edit JSON with signed URLs
        edit = {
            "timeline": {
                "tracks": [
                    {
                        "clips": clips
                    },
                    {
                        "clips": [
                            {
                                "asset": {
                                    "type": "audio",
                                    "src": narration_url
                                },
                                "start": 0,
                                "length": len(image_urls) * 5
                            }
                        ]
                    }
                ]
            },
            "output": {
                "format": "mp4",
                "resolution": "1080"
            }
        }

        logger.info("Submitting render to Shotstack...")
        logger.info(f"Duration: {len(image_urls) * 5} seconds ({len(image_urls) * 5 / 60:.1f} minutes)")
        logger.info(f"Cost: ${(len(image_urls) * 5 / 60) * 0.20:.2f}")
        logger.info(f"Sending render request with {len(clips)} signed image URLs")

        # Submit render
        headers = {"x-api-key": api_key}
        render_request = {
            "timeline": edit["timeline"],
            "output": edit["output"],
            "callback": "https://example.com/callback"
        }

        response = requests.post(
            "https://api.shotstack.io/v1/render",
            json=render_request,
            headers=headers,
            timeout=30
        )

        if response.status_code not in [200, 201]:
            logger.error(f"Render submission failed: {response.text}")
            return False

        response_data = response.json()

        if response_data.get("success") or response.status_code in [200, 201]:
            render_id = response_data.get("response", {}).get("id")
            logger.info(f"SUCCESS: Render job submitted!")
            logger.info(f"Render ID: {render_id}")
            logger.info(f"Status: Render successfully queued on Shotstack servers")
            logger.info(f"Estimated rendering time: {(len(image_urls) * 5 / 60 * 1.5):.0f} minutes")
            logger.info(f"\nNext steps:")
            logger.info(f"1. Monitor render progress at: https://dashboard.shotstack.io/renders/{render_id}")
            logger.info(f"2. When complete, download video or run check_render_status.py")
            logger.info(f"3. Upload to YouTube using: python optimized_youtube_uploader.py")
        else:
            logger.error(f"Render submission failed: {response.text}")
            return False

        return True

    except Exception as e:
        logger.error(f"Video assembly failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SHOTSTACK VIDEO ASSEMBLY WITH SIGNED URLS")
    logger.info("=" * 60 + "\n")

    success = assemble_video()

    if success:
        logger.info("\nVideo assembly submitted successfully!")
    else:
        logger.error("\nVideo assembly failed!")

    exit(0 if success else 1)
