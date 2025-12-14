#!/usr/bin/env python3
"""
Upload video assets to AWS S3 for Shotstack rendering
"""
import os
import boto3
from pathlib import Path
from config import APIConfig

def upload_to_s3():
    """Upload narration and images to S3"""

    print("\n" + "="*80)
    print("UPLOADING ASSETS TO AWS S3")
    print("="*80)

    # AWS credentials from config
    aws_access_key = APIConfig.AWS_ACCESS_KEY_ID
    aws_secret_key = APIConfig.AWS_SECRET_ACCESS_KEY
    aws_region = APIConfig.AWS_REGION or "us-east-1"
    aws_bucket = APIConfig.AWS_S3_BUCKET or "videogen-assets"

    if not aws_access_key or not aws_secret_key:
        print("[ERROR] AWS credentials not configured in .env")
        print("[INFO] Add these to .env:")
        print("  AWS_ACCESS_KEY_ID=your_key")
        print("  AWS_SECRET_ACCESS_KEY=your_secret")
        print("  AWS_REGION=us-east-1")
        print("  AWS_S3_BUCKET=videogen-assets")
        return None, None

    try:
        # Create S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )

        print(f"\n[AWS] Region: {aws_region}")
        print(f"[BUCKET] {aws_bucket}")

        # Check if bucket exists, create if not
        try:
            s3_client.head_bucket(Bucket=aws_bucket)
            print(f"[OK] Bucket exists")
        except:
            print(f"[CREATE] Creating bucket...")
            s3_client.create_bucket(Bucket=aws_bucket)
            print(f"[OK] Bucket created")

        # Upload narration
        narration_file = "output/best_free_AI_tools/narration.mp3"

        if os.path.exists(narration_file):
            print(f"\n[UPLOAD] Narration file...")
            s3_key = "best_free_ai_tools/narration.mp3"

            s3_client.upload_file(
                narration_file,
                aws_bucket,
                s3_key
            )

            narration_url = f"https://{aws_bucket}.s3.{aws_region}.amazonaws.com/{s3_key}"
            print(f"[OK] Uploaded: {s3_key}")
            print(f"[URL] {narration_url}")

            return narration_url, aws_bucket
        else:
            print(f"[ERROR] Narration file not found: {narration_file}")
            return None, None

    except Exception as e:
        print(f"[ERROR] S3 upload failed: {str(e)}")
        print(f"\n[SOLUTION] Make sure boto3 is installed:")
        print("  pip install boto3")
        return None, None


if __name__ == "__main__":
    narration_url, bucket = upload_to_s3()

    if narration_url:
        print("\n" + "="*80)
        print("S3 UPLOAD COMPLETE")
        print("="*80)
        print(f"\n[URL] {narration_url}")
        print(f"\nNext: Run shotstack_video_composer.py")
    else:
        print("\n[ERROR] Upload failed")
        exit(1)
