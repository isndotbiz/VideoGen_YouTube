#!/usr/bin/env python3
"""
Add subtitles to uploaded YouTube video
"""

import os
import sys
import pickle
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from config import APIConfig

try:
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    print("ERROR: Google API libraries not installed")
    sys.exit(1)

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

print("=" * 80)
print("ADD SUBTITLES TO YOUTUBE VIDEO")
print("=" * 80)
print()

# Load video ID from results
results_file = "output/YOUTUBE_UPLOAD_RESULTS.json"
if not os.path.exists(results_file):
    log("ERROR: Upload results file not found")
    sys.exit(1)

with open(results_file, 'r') as f:
    results = json.load(f)

video_id = results['video_id']
log(f"Video ID: {video_id}")

# Load token
TOKEN_FILE = "youtube_token.pickle"
if not os.path.exists(TOKEN_FILE):
    log("ERROR: Token file not found")
    sys.exit(1)

with open(TOKEN_FILE, 'rb') as token:
    credentials = pickle.load(token)

# Refresh if needed
if credentials.expired and credentials.refresh_token:
    credentials.refresh(Request())

# Build service
youtube = build('youtube', 'v3', credentials=credentials)
log("YouTube service: OK")

# Upload subtitles
SUBTITLE_FILE = "output/n8n_subtitles/n8n_3min_subtitles.srt"

if not os.path.exists(SUBTITLE_FILE):
    log(f"ERROR: Subtitle file not found: {SUBTITLE_FILE}")
    sys.exit(1)

log(f"\nUploading subtitles: {SUBTITLE_FILE}")

try:
    # Read subtitle content
    with open(SUBTITLE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    log(f"  File size: {len(content)} bytes")

    # Prepare caption body
    caption_body = {
        'snippet': {
            'videoId': video_id,
            'language': 'en',
            'name': 'English',
            'description': 'English subtitles for N8N video'
        }
    }

    # Upload media
    media = MediaFileUpload(
        SUBTITLE_FILE,
        mimetype='text/plain',
        resumable=False
    )

    # Insert caption
    request = youtube.captions().insert(
        part='snippet',
        body=caption_body,
        media_body=media
    )

    response = request.execute()
    caption_id = response.get('id')
    log(f"  Subtitles uploaded: OK")
    log(f"  Caption ID: {caption_id}")

except Exception as e:
    log(f"  ERROR: {e}")
    log(f"  Note: Subtitles can be added manually in YouTube Studio:")
    log(f"  1. Go to https://studio.youtube.com/video/{video_id}")
    log(f"  2. Select 'Subtitles' from left menu")
    log(f"  3. Click 'Add Language' and select 'English'")
    log(f"  4. Upload {SUBTITLE_FILE}")

log("\nDone!")
