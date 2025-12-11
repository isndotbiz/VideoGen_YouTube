#!/usr/bin/env python3
"""
YouTube Video Uploader - Claude vs Codex Comparison
Uploads video with OAuth 2.0 authentication
"""

import os
import sys
import json
import logging
import pickle
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_youtube_service():
    """Get authenticated YouTube service using OAuth"""
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError as e:
        logger.error(f"Missing required library: {e}")
        logger.info("Install with: pip install google-auth-oauthlib google-api-python-client")
        return None

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
            try:
                credentials.refresh(Request())
            except Exception as e:
                logger.warning(f"Token refresh failed: {e}")
                logger.info("Will request new authorization...")
                credentials = None

        if not credentials:
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


def upload_video(video_path, title=None, description=None, tags=None,
                privacy="public", category="28", made_for_kids=False):
    """
    Upload video to YouTube with metadata

    Args:
        video_path: Path to video file
        title: Video title (default: auto-generated)
        description: Video description
        tags: List of tags
        privacy: Privacy status (public, unlisted, private)
        category: YouTube category ID (28 = Science & Technology)
        made_for_kids: Whether video is for children
    """
    try:
        from googleapiclient.http import MediaFileUpload
    except ImportError as e:
        logger.error(f"Missing required library: {e}")
        return False

    video_file = Path(video_path)
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

    # Default metadata
    if not title:
        title = "Claude vs Codex: AI Assistant Comparison"

    if not description:
        description = """A comprehensive comparison of Claude and Codex AI assistants.

This video explores:
- Response quality and accuracy
- Code generation capabilities
- Problem-solving approaches
- User experience and interface
- Strengths and weaknesses of each platform
- Real-world use cases and examples

Whether you're a developer, researcher, or AI enthusiast, this comparison will help you understand which AI assistant best fits your needs.

#AI #Claude #Codex #ArtificialIntelligence #MachineLearning #CodeGeneration #Programming

Created: """ + datetime.now().strftime("%B %Y")

    if not tags:
        tags = [
            "Claude",
            "Codex",
            "AI Assistant",
            "OpenAI",
            "Anthropic",
            "Code Generation",
            "Machine Learning",
            "Artificial Intelligence",
            "AI Comparison",
            "Programming",
            "Developer Tools",
            "Tech Review"
        ]

    # Video metadata
    metadata = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category
        },
        "status": {
            "privacyStatus": privacy,
            "madeForKids": made_for_kids,
            "selfDeclaredMadeForKids": made_for_kids
        }
    }

    logger.info("\n" + "="*70)
    logger.info("UPLOADING TO YOUTUBE")
    logger.info("="*70)
    logger.info(f"Title: {metadata['snippet']['title']}")
    logger.info(f"Privacy: {metadata['status']['privacyStatus']}")
    logger.info(f"Category: {category}")
    logger.info(f"Tags: {', '.join(tags[:5])}...")
    logger.info("="*70 + "\n")

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
    last_percent = -1

    try:
        while response is None:
            status, response = request.next_chunk()
            chunk_count += 1

            if status:
                percent = int(status.progress() * 100)
                if percent != last_percent:
                    logger.info(f"Upload progress: {percent}% ({chunk_count} chunks)")
                    last_percent = percent

    except Exception as e:
        logger.error(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Success!
    video_id = response['id']
    logger.info("\n" + "="*70)
    logger.info("SUCCESS: Video uploaded to YouTube!")
    logger.info("="*70)
    logger.info(f"Video ID: {video_id}")
    logger.info(f"YouTube URL: https://youtu.be/{video_id}")
    logger.info(f"Watch URL: https://youtube.com/watch?v={video_id}")
    logger.info(f"Studio URL: https://studio.youtube.com/video/{video_id}/edit")
    logger.info(f"\nPrivacy Status: {privacy.upper()}")

    if privacy == "unlisted":
        logger.info("Note: Video is unlisted - only people with the link can watch")
        logger.info("To publish: Open YouTube Studio and change privacy to 'Public'")
    elif privacy == "private":
        logger.info("Note: Video is private - only you can watch")
        logger.info("To publish: Open YouTube Studio and change privacy to 'Public'")

    logger.info("="*70)

    # Save upload info
    upload_info = {
        "video_id": video_id,
        "title": title,
        "upload_time": datetime.now().isoformat(),
        "file_path": str(video_file),
        "privacy": privacy,
        "youtube_url": f"https://youtu.be/{video_id}",
        "studio_url": f"https://studio.youtube.com/video/{video_id}/edit"
    }

    info_file = Path("youtube_upload_info.json")
    with open(info_file, 'w') as f:
        json.dump(upload_info, f, indent=2)
    logger.info(f"\nUpload info saved to: {info_file}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Upload video to YouTube with OAuth authentication'
    )
    parser.add_argument(
        '--video',
        required=True,
        help='Path to video file to upload'
    )
    parser.add_argument(
        '--title',
        default=None,
        help='Video title (default: "Claude vs Codex: AI Assistant Comparison")'
    )
    parser.add_argument(
        '--description',
        default=None,
        help='Video description'
    )
    parser.add_argument(
        '--tags',
        default=None,
        help='Comma-separated list of tags'
    )
    parser.add_argument(
        '--privacy',
        choices=['public', 'unlisted', 'private'],
        default='public',
        help='Privacy status (default: public)'
    )
    parser.add_argument(
        '--category',
        default='28',
        help='YouTube category ID (default: 28 = Science & Technology)'
    )
    parser.add_argument(
        '--made-for-kids',
        action='store_true',
        help='Mark video as made for kids'
    )

    args = parser.parse_args()

    # Parse tags if provided
    tags = None
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(',')]

    # Upload video
    success = upload_video(
        video_path=args.video,
        title=args.title,
        description=args.description,
        tags=tags,
        privacy=args.privacy,
        category=args.category,
        made_for_kids=args.made_for_kids
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    logger.info("="*70)
    logger.info("YOUTUBE VIDEO UPLOADER")
    logger.info("Claude vs Codex Comparison")
    logger.info("="*70 + "\n")

    main()
