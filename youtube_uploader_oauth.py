#!/usr/bin/env python3
"""YouTube video uploader with OAuth 2.0 authentication"""

import os
import json
import logging
import pickle
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def get_youtube_service():
    """Get authenticated YouTube service using OAuth"""
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    # Scopes needed for YouTube upload
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    credentials = None
    token_file = Path("youtube_token.pickle")

    # Load cached credentials if available
    if token_file.exists():
        logger.info("Loading cached YouTube credentials...")
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)
            logger.info("Credentials loaded from cache")

    # If no cached credentials, get new ones via OAuth
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            logger.info("Refreshing expired credentials...")
            credentials.refresh(Request())
        else:
            # Need to do OAuth flow
            credentials_file = Path("youtube_credentials.json")
            if not credentials_file.exists():
                logger.error("YouTube credentials file not found!")
                logger.info("\nSetup steps:")
                logger.info("1. Go to https://console.cloud.google.com")
                logger.info("2. Create a new project or select existing")
                logger.info("3. Enable YouTube Data API v3")
                logger.info("4. Create OAuth 2.0 credentials (Desktop app)")
                logger.info("5. Download JSON credentials")
                logger.info("6. Save as 'youtube_credentials.json' in this directory")
                logger.info("7. Re-run this script")
                return None

            logger.info("Starting OAuth authentication...")
            logger.info("A browser window will open for you to authenticate...")

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES)
            credentials = flow.run_local_server(port=8888)

        # Save credentials for next run
        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)
            logger.info("Credentials cached for future use")

    # Build YouTube service
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

def upload_video_to_youtube():
    """Upload video to YouTube with metadata"""
    try:
        from googleapiclient.http import MediaFileUpload

        video_file = Path("output/video_final.mp4")
        if not video_file.exists():
            logger.error(f"Video file not found: {video_file}")
            return False

        logger.info(f"Video file: {video_file}")
        logger.info(f"File size: {video_file.stat().st_size / (1024**2):.1f} MB")

        # Get YouTube service
        youtube = get_youtube_service()
        if not youtube:
            logger.error("Failed to authenticate with YouTube")
            return False

        # Video metadata
        metadata = {
            "snippet": {
                "title": "TrueNAS Infrastructure Visualization",
                "description": (
                    "Complete overview of TrueNAS infrastructure setup.\n\n"
                    "Includes:\n"
                    "- Network topology and WireGuard VPN\n"
                    "- ZFS storage pools and data protection\n"
                    "- Automated backup systems\n"
                    "- Virtualization and containerization\n"
                    "- Media server and GPU transcoding\n"
                    "- AI model deployment\n"
                    "- Security and monitoring\n"
                    "- Remote access configuration"
                ),
                "tags": ["TrueNAS", "Infrastructure", "NAS", "Networking", "Storage", "Linux"],
                "categoryId": "28"  # Science & Technology
            },
            "status": {
                "privacyStatus": "unlisted",  # unlisted, private, or public
                "madeForKids": False
            }
        }

        logger.info("\nUploading video to YouTube...")
        logger.info(f"Title: {metadata['snippet']['title']}")
        logger.info(f"Privacy: {metadata['status']['privacyStatus']}")

        # Prepare media upload
        media = MediaFileUpload(
            str(video_file),
            mimetype='video/mp4',
            resumable=True,
            chunksize=1024*1024  # 1MB chunks
        )

        # Create insert request
        request = youtube.videos().insert(
            part='snippet,status',
            body=metadata,
            media_body=media
        )

        # Execute upload with progress tracking
        response = None
        chunk_count = 0
        while response is None:
            try:
                status, response = request.next_chunk()
                chunk_count += 1

                if status:
                    percent = int(status.progress() * 100)
                    logger.info(f"Upload progress: {percent}% ({chunk_count} chunks)")

            except Exception as e:
                logger.error(f"Upload error: {e}")
                return False

        # Success!
        video_id = response['id']
        logger.info("\n" + "="*60)
        logger.info("SUCCESS: Video uploaded to YouTube!")
        logger.info("="*60)
        logger.info(f"Video ID: {video_id}")
        logger.info(f"YouTube URL: https://youtu.be/{video_id}")
        logger.info(f"Watch URL: https://youtube.com/watch?v={video_id}")
        logger.info(f"\nPrivacy: {metadata['status']['privacyStatus']}")
        logger.info("To publish: Open YouTube Studio and change privacy to 'Public'")
        logger.info("="*60)

        return True

    except ImportError as e:
        logger.error(f"Missing required library: {e}")
        logger.info("Install with: pip install google-auth-oauthlib google-api-python-client")
        return False
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("="*60)
    logger.info("YOUTUBE VIDEO UPLOADER")
    logger.info("="*60 + "\n")

    success = upload_video_to_youtube()
    exit(0 if success else 1)
