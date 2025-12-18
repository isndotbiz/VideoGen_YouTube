#!/usr/bin/env python3
"""
Simplified YouTube Upload for N8N Video
- Uses OAuth2 credentials from .env file
- Authenticates with YouTube API
- Uploads video with metadata
- Uploads subtitles
- Publishes video
"""

import os
import sys
import json
import time
import pickle
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from config import APIConfig

# Check for required libraries
try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("ERROR: Google API libraries not installed")
    print("\nInstall with:")
    print("  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

print("=" * 80)
print("YOUTUBE UPLOAD - N8N VIDEO (SIMPLIFIED)")
print("=" * 80)
print()

# ============================================================================
# CONFIGURATION
# ============================================================================

log("Loading configuration...")

VIDEO_FILE = "output/n8n_shotstack/n8n_3min_shotstack_final.mp4"
SUBTITLE_FILE = "output/n8n_subtitles/n8n_3min_subtitles.srt"
SEO_FILE = "output/N8N_VIDEO_SEO_OPTIMIZATION.json"
TOKEN_FILE = "youtube_token.pickle"

# Verify files exist
for file_path in [VIDEO_FILE, SUBTITLE_FILE, SEO_FILE]:
    if not os.path.exists(file_path):
        log(f"ERROR: File not found: {file_path}")
        sys.exit(1)

log(f"  Video: {VIDEO_FILE} ({os.path.getsize(VIDEO_FILE) / (1024*1024):.1f} MB)")
log(f"  Subtitles: {SUBTITLE_FILE}")
log(f"  Metadata: {SEO_FILE}")

# ============================================================================
# LOAD METADATA
# ============================================================================

log("\nLoading SEO metadata...")

with open(SEO_FILE, 'r') as f:
    seo_data = json.load(f)

metadata = seo_data.get("youtube_metadata", {})
title = metadata.get("title", "N8N Workflow Automation")
description = metadata.get("description", "")
tags = metadata.get("tags", [])

log(f"  Title: {title[:50]}...")
log(f"  Description: {len(description)} chars")
log(f"  Tags: {len(tags)}")

# ============================================================================
# YOUTUBE API AUTHENTICATION
# ============================================================================

log("\nYouTube API Authentication...")

SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube']

credentials = None

# Try to load existing token
if os.path.exists(TOKEN_FILE):
    log("  Loading existing token...")
    try:
        with open(TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        log("  Token loaded: OK")
    except Exception as e:
        log(f"  Token load failed: {e}")
        credentials = None

# If no token, create OAuth2 flow
if not credentials or not credentials.valid:
    log("  Starting OAuth2 authentication flow...")
    log("  (Browser will open for authorization)")

    # Create OAuth2 credentials from .env values
    client_config = {
        "installed": {
            "client_id": APIConfig.YOUTUBE_CLIENT_ID,
            "client_secret": APIConfig.YOUTUBE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [APIConfig.YOUTUBE_REDIRECT_URI]
        }
    }

    try:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        credentials = flow.run_local_server(port=8888)

        # Save token for future use
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)

        log("  Authentication: OK")
        log("  Token saved for future uploads")

    except Exception as e:
        log(f"  ERROR: {e}")
        log("\n  Make sure:")
        log("  1. YOUTUBE_CLIENT_ID is set in .env")
        log("  2. YOUTUBE_CLIENT_SECRET is set in .env")
        log("  3. YOUTUBE_REDIRECT_URI is set to http://localhost:8888/callback in .env")
        sys.exit(1)

# ============================================================================
# BUILD YOUTUBE SERVICE
# ============================================================================

log("\nBuilding YouTube service...")

try:
    youtube = build('youtube', 'v3', credentials=credentials)
    log("  Service: OK")
except Exception as e:
    log(f"  ERROR: {e}")
    sys.exit(1)

# ============================================================================
# UPLOAD VIDEO
# ============================================================================

log("\nUploading video...")

body = {
    'snippet': {
        'title': title,
        'description': description,
        'tags': tags[:30],
        'categoryId': '27',  # Education
        'defaultLanguage': 'en',
        'defaultAudioLanguage': 'en'
    },
    'status': {
        'privacyStatus': 'public',
        'selfDeclaredMadeForKids': False
    }
}

try:
    media = MediaFileUpload(
        VIDEO_FILE,
        mimetype='video/mp4',
        resumable=True,
        chunksize=5 * 1024 * 1024
    )

    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )

    log(f"  Uploading {os.path.getsize(VIDEO_FILE) / (1024*1024):.1f} MB...")

    response = None
    start_time = time.time()

    while response is None:
        try:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                elapsed = time.time() - start_time
                log(f"    {progress}% ({elapsed:.0f}s)")
        except Exception as e:
            log(f"  Upload error: {e}")
            sys.exit(1)

    video_id = response['id']
    elapsed = time.time() - start_time

    log(f"  Upload complete: {elapsed:.0f}s")
    log(f"  Video ID: {video_id}")

except Exception as e:
    log(f"  ERROR: {e}")
    sys.exit(1)

# ============================================================================
# UPLOAD SUBTITLES
# ============================================================================

log("\nUploading subtitles...")

try:
    subtitle_body = {
        'snippet': {
            'videoId': video_id,
            'language': 'en',
            'name': 'English',
        }
    }

    media = MediaFileUpload(
        SUBTITLE_FILE,
        mimetype='text/plain'
    )

    request = youtube.captions().insert(
        part='snippet',
        body=subtitle_body,
        media_body=media
    )

    caption = request.execute()
    log(f"  Subtitles: OK")

except Exception as e:
    log(f"  Subtitles: SKIPPED ({type(e).__name__})")

# ============================================================================
# RESULTS
# ============================================================================

print("\n" + "=" * 80)
log("UPLOAD COMPLETE!")
print("=" * 80)

youtube_url = f"https://www.youtube.com/watch?v={video_id}"
studio_url = f"https://studio.youtube.com/video/{video_id}"

log(f"\nYouTube URL: {youtube_url}")
log(f"Studio URL: {studio_url}")
log(f"\nVideo is now PUBLIC on YouTube!")

# Save results
results = {
    "timestamp": datetime.now().isoformat(),
    "video_id": video_id,
    "youtube_url": youtube_url,
    "studio_url": studio_url,
    "title": title,
    "file_size_mb": os.path.getsize(VIDEO_FILE) / (1024*1024)
}

with open("output/YOUTUBE_UPLOAD_RESULTS.json", "w") as f:
    json.dump(results, f, indent=2)

log(f"\nResults saved to: output/YOUTUBE_UPLOAD_RESULTS.json")
log(f"\nDone!")
