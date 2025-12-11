#!/usr/bin/env python3
"""
Test YouTube authentication without uploading
Verifies credentials and connection to YouTube API
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_youtube_auth():
    """Test YouTube authentication"""
    try:
        from upload_to_youtube import get_youtube_service
    except ImportError as e:
        logger.error(f"Cannot import upload script: {e}")
        return False

    logger.info("Testing YouTube authentication...")
    logger.info("")

    # Check credentials file
    creds_file = Path("youtube_credentials.json")
    if not creds_file.exists():
        logger.error("Credentials file not found: youtube_credentials.json")
        return False
    logger.info("✓ Credentials file exists")

    # Check token cache
    token_file = Path("youtube_token.pickle")
    if token_file.exists():
        logger.info("✓ Token cache exists")
    else:
        logger.warning("⚠ No token cache - will need to authenticate")

    # Try to get YouTube service
    logger.info("")
    logger.info("Attempting to connect to YouTube API...")
    youtube = get_youtube_service()

    if not youtube:
        logger.error("Failed to authenticate with YouTube")
        return False

    logger.info("✓ Successfully authenticated with YouTube!")

    # Try to get channel info
    try:
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()

        if response.get('items'):
            channel = response['items'][0]
            snippet = channel['snippet']
            stats = channel.get('statistics', {})

            logger.info("")
            logger.info("="*60)
            logger.info("CHANNEL INFORMATION")
            logger.info("="*60)
            logger.info(f"Channel: {snippet['title']}")
            logger.info(f"Subscribers: {stats.get('subscriberCount', 'Hidden')}")
            logger.info(f"Total Views: {stats.get('viewCount', '0')}")
            logger.info(f"Video Count: {stats.get('videoCount', '0')}")
            logger.info("="*60)
        else:
            logger.warning("No channel found for this account")

    except Exception as e:
        logger.warning(f"Could not fetch channel info: {e}")

    logger.info("")
    logger.info("Authentication test completed successfully!")
    logger.info("You are ready to upload videos to YouTube.")

    return True


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("YOUTUBE AUTHENTICATION TEST")
    logger.info("="*60)
    logger.info("")

    success = test_youtube_auth()

    if success:
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Run: python upload_to_youtube.py --video output/claude_codex_video.mp4")
        logger.info("2. Or: python upload_to_youtube.py --video output/video_final.mp4")
        logger.info("")
        logger.info("For help: python upload_to_youtube.py --help")

    sys.exit(0 if success else 1)
