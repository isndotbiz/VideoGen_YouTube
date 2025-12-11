#!/usr/bin/env python3
"""Test minimal YouTube video metadata update"""

import os
import pickle
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def get_youtube_service():
    """Get authenticated YouTube service"""
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    SCOPES = ['https://www.googleapis.com/auth/youtube']
    credentials = None
    token_file = Path("youtube_token.pickle")

    if token_file.exists():
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            logger.info("Refreshing expired credentials...")
            credentials.refresh(Request())
        else:
            credentials_file = Path("youtube_credentials.json")
            if not credentials_file.exists():
                logger.error("YouTube credentials file not found!")
                return None
            logger.info("Starting OAuth authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES)
            credentials = flow.run_local_server(port=8888)

        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)

    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

def test_video_retrieval():
    """Test if we can retrieve video metadata"""
    youtube = get_youtube_service()
    if not youtube:
        return False

    video_id = "e21KjZzV-Ss"

    try:
        logger.info("Testing video retrieval...")
        request = youtube.videos().list(
            part='snippet,status',
            id=video_id
        )
        response = request.execute()

        if response['items']:
            video = response['items'][0]
            logger.info("SUCCESS: Can retrieve video")
            logger.info(f"Current Title: {video['snippet']['title']}")
            logger.info(f"Current Privacy: {video['status']['privacyStatus']}")
            logger.info(f"Channel: {video['snippet']['channelId']}")
            return True
        else:
            logger.error(f"Video not found: {video_id}")
            return False

    except Exception as e:
        logger.error(f"Failed to retrieve video: {e}")
        return False

def test_minimal_privacy_update():
    """Test updating only privacy status"""
    youtube = get_youtube_service()
    if not youtube:
        return False

    video_id = "e21KjZzV-Ss"

    try:
        logger.info("\nTesting minimal update (privacy status only)...")

        metadata = {
            "id": video_id,
            "status": {
                "privacyStatus": "public"
            }
        }

        request = youtube.videos().update(
            part='status',
            body=metadata
        )
        response = request.execute()

        logger.info("SUCCESS: Minimal update worked!")
        logger.info(f"New Privacy: {response['status']['privacyStatus']}")
        return True

    except Exception as e:
        logger.error(f"Failed minimal update: {e}")
        logger.error(f"Error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("YOUTUBE API PERMISSION TEST")
    logger.info("=" * 60 + "\n")

    if test_video_retrieval():
        logger.info("\n✓ Video retrieval works")
        test_minimal_privacy_update()
    else:
        logger.error("\n✗ Cannot retrieve video - permission issue")
