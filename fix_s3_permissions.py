#!/usr/bin/env python3
"""Fix S3 bucket permissions for public read access"""

import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def fix_s3_permissions():
    """Make S3 objects publicly readable"""
    try:
        import boto3

        aws_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        bucket = os.getenv("AWS_S3_BUCKET")

        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret,
            region_name=aws_region
        )

        logger.info(f"Fixing permissions for bucket: {bucket}\n")

        # Set bucket policy to allow public read
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket}/video-generation/*"
                }
            ]
        }

        logger.info("Setting bucket policy for public read access...")
        s3_client.put_bucket_policy(
            Bucket=bucket,
            Policy=json.dumps(bucket_policy)
        )
        logger.info("SUCCESS: Bucket policy updated\n")

        # Make all existing objects publicly readable
        logger.info("Making all objects publicly readable...")
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix='video-generation/')

        count = 0
        for page in pages:
            if 'Contents' not in page:
                continue

            for obj in page['Contents']:
                key = obj['Key']
                # Update object ACL to public-read
                try:
                    s3_client.put_object_acl(
                        Bucket=bucket,
                        Key=key,
                        ACL='public-read'
                    )
                    count += 1
                    logger.info(f"  {key}")
                except Exception as e:
                    logger.warning(f"  {key} - {e}")

        logger.info(f"\nUpdated ACL for {count} objects")
        logger.info("\nS3 permissions fixed! Ready to retry video assembly.")

        return True

    except ImportError:
        logger.error("boto3 not installed")
        return False
    except Exception as e:
        logger.error(f"Error fixing permissions: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("FIX S3 PERMISSIONS")
    logger.info("=" * 50 + "\n")

    success = fix_s3_permissions()

    if success:
        logger.info("\n" + "=" * 50)
        logger.info("Next: Run video_assembly_with_s3.py again")
        logger.info("=" * 50)
