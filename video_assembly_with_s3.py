#!/usr/bin/env python3
"""Shotstack video assembly with S3 image upload"""

import os
import json
import logging
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_images_to_s3():
    """Upload all images to S3 and return HTTPS URLs"""
    import boto3

    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    bucket = os.getenv("AWS_S3_BUCKET")

    if not all([aws_key, aws_secret, bucket]):
        logger.error("Missing AWS credentials in .env (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET)")
        return None

    try:
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        # Get all images
        images_dir = Path("output/generated_images")
        images = sorted(list(images_dir.glob("*.png")))

        if not images:
            logger.error("No images found in output/generated_images")
            return None

        logger.info(f"Uploading {len(images)} images to S3...")
        image_urls = []

        for i, img_path in enumerate(images, 1):
            try:
                # Upload to S3
                s3_key = f"video-generation/{img_path.name}"
                logger.info(f"[{i}/{len(images)}] Uploading {img_path.name}...")

                s3_client.upload_file(
                    str(img_path),
                    bucket,
                    s3_key,
                    ExtraArgs={'ContentType': 'image/png'}
                )

                # Build public HTTPS URL
                https_url = f"https://{bucket}.s3.{aws_region}.amazonaws.com/{s3_key}"
                image_urls.append(https_url)
                logger.info(f"  -> {https_url}")

            except Exception as e:
                logger.error(f"Failed to upload {img_path.name}: {e}")
                return None

        logger.info(f"Successfully uploaded {len(image_urls)} images to S3")
        return image_urls

    except ImportError:
        logger.error("boto3 not installed. Run: pip install boto3")
        return None
    except Exception as e:
        logger.error(f"S3 upload failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def assemble_video_with_s3():
    """Assemble video using S3 image URLs"""
    api_key = os.getenv("SHOTSTACK_API_KEY")
    if not api_key:
        logger.error("SHOTSTACK_API_KEY not set")
        return False

    # Upload images to S3 and get URLs
    image_urls = upload_images_to_s3()
    if not image_urls:
        logger.error("Failed to upload images to S3")
        return False

    try:
        import requests

        narration_file = Path("output/narration.mp3")
        if not narration_file.exists():
            logger.error(f"Narration file not found: {narration_file}")
            return False

        logger.info(f"Building video assembly with {len(image_urls)} S3 images...")

        # Upload narration to S3 too
        logger.info("Uploading narration to S3...")
        aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        bucket = os.getenv("AWS_S3_BUCKET")

        import boto3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        audio_s3_key = "video-generation/narration.mp3"
        s3_client.upload_file(
            str(narration_file),
            bucket,
            audio_s3_key,
            ExtraArgs={'ContentType': 'audio/mpeg'}
        )
        audio_url = f"https://{bucket}.s3.{aws_region}.amazonaws.com/{audio_s3_key}"
        logger.info(f"Narration uploaded: {audio_url}")

        # Build clips from S3 image URLs (5 seconds each)
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

        # Build edit JSON with S3 URLs
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
                                    "src": audio_url
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

        # Submit render with S3 URLs
        headers = {"x-api-key": api_key}
        render_request = {
            "timeline": edit["timeline"],
            "output": edit["output"],
            "callback": "https://example.com/callback"
        }

        logger.info(f"Sending render request with {len(clips)} S3 image URLs")

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

        # Check both success flag and status code
        if response_data.get("success") or response.status_code in [200, 201]:
            render_id = response_data.get("response", {}).get("id")
            logger.info(f"SUCCESS: Render job submitted!")
            logger.info(f"Render ID: {render_id}")
            logger.info(f"Status: Render successfully queued on Shotstack servers")
            logger.info(f"Estimated rendering time: {(len(image_urls) * 5 / 60 * 1.5):.0f} minutes")
            logger.info(f"\nNext steps:")
            logger.info(f"1. Monitor render progress at: https://dashboard.shotstack.io/renders/{render_id}")
            logger.info(f"2. When complete, download video from S3 output URL")
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
    success = assemble_video_with_s3()
    exit(0 if success else 1)
