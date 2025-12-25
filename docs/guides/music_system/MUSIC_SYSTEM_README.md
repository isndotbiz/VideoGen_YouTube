# Complete Platform Music System

## Overview

A comprehensive music management system for multi-platform video production. Download, organize, and integrate background music optimized for YouTube, TikTok, Instagram, and Twitter.

## System Components

### 1. Master Downloader
**File:** `download_all_platform_music.py`

Downloads 60 curated tracks organized by platform and content type.

```bash
# Download all 60 tracks
python download_all_platform_music.py

# Quick test (20 tracks)
python download_all_platform_music.py --quick

# Specific platforms
python download_all_platform_music.py --platforms youtube,tiktok
```

**Features:**
- Parallel downloading (5 tracks simultaneously)
- Smart deduplication (skips existing tracks)
- Automatic retry logic (3 attempts)
- BPM and mood filtering
- Instrumental only (no vocals)
- Complete metadata tracking

### 2. Library Browser
**File:** `show_music_library.py`

View and search your downloaded music library.

```bash
# Show statistics
python show_music_library.py

# Platform-specific view
python show_music_library.py --platform youtube

# List all tracks
python show_music_library.py --list

# Filter by BPM
python show_music_library.py --bpm 100-130

# Search tracks
python show_music_library.py --search "ambient"
```

### 3. Music Integration
**File:** `use_platform_music.py`

Python module for integrating music into video production.

```python
from use_platform_music import (
    get_background_music,
    mix_narration_with_music,
    loop_music_for_duration
)

# Get music for platform
music, meta = get_background_music("youtube", "calm")

# Mix with narration
mix_narration_with_music(
    "narration.mp3",
    platform="youtube",
    category="energetic",
    output_file="final_audio.mp3"
)

# Loop to duration
looped = loop_music_for_duration(music, duration_ms=180000)
```

## Music Library Structure

### Platform Configuration

```
Total: 60 tracks across 4 platforms

YouTube (20 tracks):
├── calm/          10 tracks (60-80 BPM)
│   ├── Tutorial videos
│   ├── Educational content
│   └── Vlogs
└── energetic/     10 tracks (120-140 BPM)
    ├── Product reviews
    ├── Tech videos
    └── Lifestyle content

TikTok (15 tracks):
└── high_energy/   15 tracks (140-160 BPM)
    ├── Quick cuts
    ├── Transitions
    └── Viral content

Instagram (15 tracks):
├── fitness/       5 tracks (130-150 BPM)
│   ├── Workout videos
│   ├── Fitness tips
│   └── Gym content
├── beauty/        5 tracks (90-120 BPM)
│   ├── Makeup tutorials
│   ├── Skincare routines
│   └── Fashion content
└── travel/        5 tracks (80-110 BPM)
    ├── Travel vlogs
    ├── Destination guides
    └── Adventures

Twitter (10 tracks):
└── professional/  10 tracks (100-130 BPM)
    ├── News commentary
    ├── Professional updates
    └── Thread videos
```

### Directory Structure

```
background_music_epidemic/
├── youtube/
│   ├── calm/
│   │   ├── youtube_calm_01_TrackTitle_trackid.mp3
│   │   ├── youtube_calm_02_TrackTitle_trackid.mp3
│   │   └── ... (10 files)
│   └── energetic/
│       └── ... (10 files)
├── tiktok/
│   └── high_energy/
│       └── ... (15 files)
├── instagram/
│   ├── fitness/
│   │   └── ... (5 files)
│   ├── beauty/
│   │   └── ... (5 files)
│   └── travel/
│       └── ... (5 files)
├── twitter/
│   └── professional/
│       └── ... (10 files)
├── library_index.json        # Master catalog with metadata
└── download_log.json         # Download history and errors
```

## Quick Start Guide

### Prerequisites

1. **Python 3.7+**
2. **Required packages:**
   ```bash
   pip install requests pydub
   ```

3. **Epidemic Sound API credentials:**
   - Sign up at https://www.epidemicsound.com
   - Get API credentials from developer portal

### Step 1: Set Environment Variables

```bash
# Windows (PowerShell)
$env:EPIDEMIC_ACCESS_KEY_ID="your_access_key_id"
$env:EPIDEMIC_ACCESS_KEY_SECRET="your_access_key_secret"

# Linux/Mac
export EPIDEMIC_ACCESS_KEY_ID="your_access_key_id"
export EPIDEMIC_ACCESS_KEY_SECRET="your_access_key_secret"
```

### Step 2: Download Music

```bash
# Test with quick mode first (20 tracks, ~3 minutes)
python download_all_platform_music.py --quick

# Download all 60 tracks (~10-15 minutes)
python download_all_platform_music.py
```

### Step 3: Verify Library

```bash
# View statistics
python show_music_library.py

# Check specific platform
python show_music_library.py --platform youtube
```

### Step 4: Use in Production

```python
from use_platform_music import get_background_music, mix_narration_with_music

# Example: Create video with music
music, meta = get_background_music("youtube", "calm")
print(f"Using: {meta['title']} ({meta['bpm']} BPM)")

# Mix with narration
mix_narration_with_music(
    "narration.mp3",
    "youtube",
    "calm",
    "final_audio.mp3"
)
```

## Usage Examples

### Example 1: YouTube Tutorial Video

```python
from use_platform_music import mix_narration_with_music

# Create calm background for tutorial
mix_narration_with_music(
    narration_file="tutorial_narration.mp3",
    platform="youtube",
    category="calm",
    output_file="tutorial_final_audio.mp3",
    music_volume_db=-18  # Quieter for tutorials
)
```

### Example 2: TikTok High-Energy Video

```python
from use_platform_music import get_music_for_video_duration

# Get 15-second music for TikTok
music, meta = get_music_for_video_duration(
    duration_seconds=15,
    platform="tiktok",
    category="high_energy"
)

# Export for video editing
music.export("tiktok_bg.mp3", format="mp3", bitrate="192k")
```

### Example 3: Instagram Fitness Reel

```python
from use_platform_music import get_background_music, loop_music_for_duration

# Get fitness music
music, meta = get_background_music("instagram", "fitness")

# Loop to 60 seconds
looped = loop_music_for_duration(music, duration_ms=60000)

# Export
looped.export("fitness_reel_bg.mp3", format="mp3")
```

### Example 4: Twitter Professional Update

```python
from use_platform_music import get_music_by_bpm

# Get professional music in specific BPM range
music, meta = get_music_by_bpm(
    bpm_min=100,
    bpm_max=120,
    platform="twitter"
)

print(f"Using: {meta['title']} ({meta['bpm']} BPM)")
```

### Example 5: Batch Processing Multiple Videos

```python
import json
from pathlib import Path
from use_platform_music import get_background_music, loop_music_for_duration

# Load library
with open("background_music_epidemic/library_index.json") as f:
    library = json.load(f)

# Get all YouTube energetic tracks
track_ids = library['platforms']['youtube']['energetic']

# Create individual files for each track
for idx, track_id in enumerate(track_ids):
    track = library['tracks'][track_id]
    music_path = track['file_path']

    # Process each track
    from pydub import AudioSegment
    music = AudioSegment.from_mp3(music_path)
    music = music - 16  # Background volume

    # Loop to 3 minutes
    looped = loop_music_for_duration(music, 180000)

    # Export
    output = f"video_{idx+1}_bg.mp3"
    looped.export(output, format="mp3", bitrate="192k")
    print(f"Created: {output}")
```

## Integration with Video Pipeline

### Step 1: Select Music

```python
from use_platform_music import get_background_music

# Determine platform from video config
video_config = {
    "platform": "youtube",
    "content_type": "tutorial",
    "duration": 180  # seconds
}

# Select appropriate category
if video_config["content_type"] == "tutorial":
    category = "calm"
elif video_config["content_type"] == "review":
    category = "energetic"

# Get music
music, metadata = get_background_music(
    video_config["platform"],
    category
)
```

### Step 2: Mix Audio

```python
from use_platform_music import mix_narration_with_music

# Mix narration with selected music
final_audio = mix_narration_with_music(
    narration_file="generated_narration.mp3",
    platform=video_config["platform"],
    category=category,
    output_file="final_audio.mp3"
)
```

### Step 3: Compose Video

```python
from moviepy.editor import VideoClip, AudioFileClip

# Load final audio
audio = AudioFileClip("final_audio.mp3")

# Compose video with audio
video = video.set_audio(audio)

# Export
video.write_videofile(
    "final_video.mp4",
    codec="libx264",
    audio_codec="aac"
)
```

## Advanced Features

### Custom Music Selection

```python
import random
import json

def select_music_smart(platform, category, video_duration, previous_tracks=[]):
    """
    Smart music selection with variety tracking.

    Args:
        platform: Target platform
        category: Music category
        video_duration: Video length in seconds
        previous_tracks: List of recently used track IDs

    Returns:
        (music, metadata) tuple
    """
    from use_platform_music import get_background_music, loop_music_for_duration

    # Load library
    with open("background_music_epidemic/library_index.json") as f:
        library = json.load(f)

    # Get available tracks
    track_ids = library['platforms'][platform][category]

    # Filter out recently used
    available = [tid for tid in track_ids if tid not in previous_tracks]

    if not available:
        available = track_ids  # Reset if all used

    # Select track
    track_id = random.choice(available)
    track_data = library['tracks'][track_id]

    # Load and prepare
    from pydub import AudioSegment
    music = AudioSegment.from_mp3(track_data['file_path'])
    music = music - 16

    # Loop to duration
    duration_ms = video_duration * 1000
    music = loop_music_for_duration(music, duration_ms)

    return music, track_data, track_id

# Usage
music, meta, track_id = select_music_smart(
    "youtube",
    "calm",
    180,
    previous_tracks=["abc123", "def456"]
)

print(f"Selected: {meta['title']} (avoiding previous tracks)")
```

### Batch Video Processing

```python
def process_video_batch(videos_config):
    """
    Process multiple videos with automatic music selection.

    Args:
        videos_config: List of video configurations

    Example:
        videos = [
            {"platform": "youtube", "category": "calm", "narration": "video1.mp3"},
            {"platform": "tiktok", "category": "high_energy", "narration": "video2.mp3"},
        ]
        process_video_batch(videos)
    """
    from use_platform_music import mix_narration_with_music

    results = []

    for idx, config in enumerate(videos_config):
        print(f"Processing video {idx+1}/{len(videos_config)}...")

        output_file = f"final_audio_{idx+1}.mp3"

        try:
            mix_narration_with_music(
                narration_file=config["narration"],
                platform=config["platform"],
                category=config["category"],
                output_file=output_file
            )

            results.append({
                "video_id": idx + 1,
                "success": True,
                "output": output_file
            })

        except Exception as e:
            print(f"Error processing video {idx+1}: {e}")
            results.append({
                "video_id": idx + 1,
                "success": False,
                "error": str(e)
            })

    return results
```

## Troubleshooting

### Issue: Authentication Failed

```
ERROR: Authentication failed. Cannot proceed.
```

**Solutions:**
1. Verify credentials are set correctly
2. Check environment variables are active in current session
3. Test credentials with curl:
   ```bash
   curl -X POST https://partner-content-api.epidemicsound.com/v0/partner-token \
     -H "Content-Type: application/json" \
     -d '{"accessKeyId":"YOUR_KEY","accessKeySecret":"YOUR_SECRET"}'
   ```

### Issue: No Tracks Found

```
WARNING: No tracks found for category
```

**Solutions:**
1. Search criteria might be too strict
2. Verify access to Epidemic Sound free tier
3. Check API status at https://status.epidemicsound.com
4. Modify search terms in script

### Issue: Download Timeout

```
ERROR: Download failed - Max retries exceeded
```

**Solutions:**
1. Check internet connection
2. Increase timeouts:
   ```python
   REQUEST_TIMEOUT = 60  # Increase from 30
   DOWNLOAD_TIMEOUT = 300  # Increase from 180
   ```
3. Reduce parallel downloads:
   ```python
   MAX_WORKERS = 2  # Reduce from 5
   ```
4. Run with `--resume` flag

### Issue: Library Index Corrupted

```
WARNING: Failed to load library index
```

**Solutions:**
1. Backup existing `library_index.json`
2. Delete corrupted file
3. Run downloader to rebuild

### Issue: Missing Dependencies

```
ERROR: pydub not installed
```

**Solution:**
```bash
pip install pydub requests
```

## Performance Tips

### Optimize Download Speed

1. **Use quick mode for testing:**
   ```bash
   python download_all_platform_music.py --quick
   ```

2. **Download platforms separately:**
   ```bash
   python download_all_platform_music.py --platforms youtube
   python download_all_platform_music.py --platforms tiktok
   ```

3. **Increase parallel downloads** (if bandwidth allows):
   ```python
   MAX_WORKERS = 10  # In download_all_platform_music.py
   ```

### Optimize Production Pipeline

1. **Pre-load library once:**
   ```python
   # Load library at startup, reuse
   library = load_library()
   ```

2. **Cache music in memory:**
   ```python
   music_cache = {}

   def get_cached_music(platform, category):
       key = f"{platform}_{category}"
       if key not in music_cache:
           music_cache[key] = get_background_music(platform, category)
       return music_cache[key]
   ```

3. **Batch audio operations:**
   ```python
   # Process multiple videos in parallel
   from concurrent.futures import ThreadPoolExecutor

   with ThreadPoolExecutor(max_workers=4) as executor:
       futures = [executor.submit(process_video, v) for v in videos]
       results = [f.result() for f in futures]
   ```

## Documentation Files

- **MUSIC_DOWNLOADER_GUIDE.md** - Complete downloader documentation
- **MUSIC_DOWNLOADER_QUICK_START.txt** - Quick reference card
- **MUSIC_SYSTEM_README.md** - This file (system overview)
- **EPIDEMIC_SOUND_API_COMPLETE_REFERENCE.md** - API documentation

## Files in This System

1. **download_all_platform_music.py** - Master orchestration downloader
2. **show_music_library.py** - Library browser and search tool
3. **use_platform_music.py** - Integration module for production
4. **library_index.json** - Generated track catalog
5. **download_log.json** - Generated download history

## License

Music downloaded from Epidemic Sound is subject to their licensing terms.
Ensure you have appropriate licensing for your use case.

## Support

For issues:
1. Check `download_log.json` for error details
2. Review API documentation
3. Verify credentials and connectivity
4. Check Epidemic Sound API status

## Next Steps

1. Download music library: `python download_all_platform_music.py --quick`
2. Verify library: `python show_music_library.py`
3. Test integration: `python use_platform_music.py`
4. Integrate into video pipeline
5. Set up automated updates (weekly/monthly)
