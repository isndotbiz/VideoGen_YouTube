#!/usr/bin/env python3
"""Find or create S3 bucket for video generation"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def list_buckets():
    """List all S3 buckets"""
    try:
        import boto3

        aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        if not aws_key or not aws_secret:
            logger.error("AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY not set in .env")
            return None

        # Create S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        logger.info("Listing your S3 buckets...")
        response = s3_client.list_buckets()

        if not response['Buckets']:
            logger.warning("No S3 buckets found. Creating one...")
            return None

        logger.info(f"\nFound {len(response['Buckets'])} bucket(s):\n")
        for i, bucket in enumerate(response['Buckets'], 1):
            logger.info(f"{i}. {bucket['Name']}")
            logger.info(f"   Created: {bucket['CreationDate']}\n")

        return response['Buckets']

    except ImportError:
        logger.error("boto3 not installed. Run: pip install boto3")
        return None
    except Exception as e:
        logger.error(f"Error listing buckets: {e}")
        return None

def create_bucket(bucket_name):
    """Create a new S3 bucket"""
    try:
        import boto3

        aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        logger.info(f"Creating S3 bucket: {bucket_name}")

        if aws_region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': aws_region}
            )

        logger.info(f"SUCCESS: Bucket created: {bucket_name}")
        return bucket_name

    except Exception as e:
        logger.error(f"Error creating bucket: {e}")
        return None

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("AWS S3 BUCKET FINDER")
    logger.info("=" * 50 + "\n")

    # Try to list existing buckets
    buckets = list_buckets()

    if buckets:
        logger.info("Choose a bucket number above, or enter a new bucket name to create one.")
        choice = input("\nEnter bucket # (1-{}) or new bucket name: ".format(len(buckets))).strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(buckets):
                selected = buckets[idx]['Name']
                logger.info(f"\nSelected bucket: {selected}")
                logger.info(f"Update .env with: AWS_S3_BUCKET={selected}")
            else:
                logger.error("Invalid selection")
        else:
            # Create new bucket
            new_bucket = choice.lower().replace(" ", "-")
            created = create_bucket(new_bucket)
            if created:
                logger.info(f"Update .env with: AWS_S3_BUCKET={created}")
    else:
        logger.info("Creating new bucket...")
        new_bucket = input("Enter bucket name (lowercase, no spaces): ").strip().lower().replace(" ", "-")
        created = create_bucket(new_bucket)
        if created:
            logger.info(f"Update .env with: AWS_S3_BUCKET={created}")
