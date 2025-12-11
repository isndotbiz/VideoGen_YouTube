#!/usr/bin/env python3
"""Optimized YouTube video uploader with OAuth"""

import os
import json
import logging
import pickle
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_to_youtube():
    """Upload video to YouTube"""
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_apis.youtube_v3 import build

        video_file = Path("output/video_final.mp4")
        if not video_file.exists():
            logger.error(f"Video file not found: {video_file}")
            return False

        # Get credentials
        credentials = None
        token_file = Path("token.pickle")

        if token_file.exists():
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)
                logger.info("Loaded cached credentials")

        if not credentials:
            logger.error("No YouTube credentials found")
            logger.info("First run requires OAuth authentication")
            logger.info("Instructions:")
            logger.info("1. Go to https://console.cloud.google.com")
            logger.info("2. Create OAuth 2.0 credentials (Desktop app)")
            logger.info("3. Download JSON and save as credentials.json")
            logger.info("4. Re-run this script for OAuth flow")
            return False

        # Build YouTube service
        youtube = build('youtube', 'v3', credentials=credentials)

        # Upload metadata
        metadata = {
            "snippet": {
                "title": "TrueNAS Infrastructure Visualization",
                "description": "Complete overview of TrueNAS infrastructure setup including networking, storage, backup, virtualization, and monitoring systems.",
                "tags": ["TrueNAS", "Infrastructure", "NAS", "Networking", "Storage"],
                "categoryId": "28"  # Science & Technology
            },
            "status": {
                "privacyStatus": "unlisted"  # Change to 'public' when ready
            }
        }

        logger.info("Uploading video to YouTube...")
        logger.info(f"File: {video_file} ({video_file.stat().st_size / (1024**3):.1f} GB)")

        # Prepare upload
        request = youtube.videos().insert(
            part="snippet,status",
            body=metadata,
            media_body=str(video_file)
        )

        # Execute with progress
        response = None
        retry_count = 0
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    percent = int(status.progress() * 100)
                    logger.info(f"Upload progress: {percent}%")
            except Exception as e:
                retry_count += 1
                if retry_count > 3:
                    logger.error(f"Upload failed after retries: {e}")
                    return False
                logger.warning(f"Upload interrupted, retrying... (attempt {retry_count})")

        video_id = response['id']
        logger.info(f"Video uploaded successfully!")
        logger.info(f"Video ID: {video_id}")
        logger.info(f"URL: https://youtube.com/watch?v={video_id}")
        logger.info(f"Status: Unlisted (change in YouTube Studio to publish)")

        return True

    except Exception as e:
        logger.error(f"YouTube upload failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = upload_to_youtube()
    exit(0 if success else 1)
