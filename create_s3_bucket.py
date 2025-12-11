#!/usr/bin/env python3
"""Create S3 bucket for video generation"""

import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def create_bucket():
    """Create S3 bucket with auto-generated name"""
    try:
        import boto3

        aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        if not aws_key or not aws_secret:
            logger.error("AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY not set in .env")
            return None

        # Generate unique bucket name (must be globally unique across all AWS)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        bucket_name = f"video-gen-{timestamp}".lower()

        logger.info(f"Creating S3 bucket: {bucket_name}")

        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        # Create bucket
        if aws_region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': aws_region}
            )

        logger.info(f"SUCCESS: Bucket created!\n")
        logger.info(f"Bucket name: {bucket_name}")
        logger.info(f"Region: {aws_region}\n")

        # Update .env file
        env_path = ".env"
        with open(env_path, "r") as f:
            content = f.read()

        # Replace the AWS_S3_BUCKET line
        new_content = content.replace(
            "AWS_S3_BUCKET=",
            f"AWS_S3_BUCKET={bucket_name}"
        )

        with open(env_path, "w") as f:
            f.write(new_content)

        logger.info(f"Updated .env with bucket name!")
        logger.info(f"Ready to run: python video_assembly_with_s3.py")

        return bucket_name

    except ImportError:
        logger.error("boto3 not installed. Run: pip install boto3")
        return None
    except Exception as e:
        logger.error(f"Error creating bucket: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("CREATE S3 BUCKET FOR VIDEO GENERATION")
    logger.info("=" * 50 + "\n")

    bucket = create_bucket()

    if bucket:
        logger.info(f"Bucket ready for video upload!")
    else:
        logger.error("Failed to create bucket")
