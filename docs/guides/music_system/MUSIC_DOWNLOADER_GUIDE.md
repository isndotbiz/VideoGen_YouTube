# Master Music Downloader - Complete Guide

## Overview

The `download_all_platform_music.py` script is your one-click solution for downloading optimized background music for all video platforms. It downloads 60 curated tracks organized by platform and content type.

## Quick Start

### 1. Set Up Environment Variables

```bash
# Windows (PowerShell)
$env:EPIDEMIC_ACCESS_KEY_ID="your_access_key_id"
$env:EPIDEMIC_ACCESS_KEY_SECRET="your_access_key_secret"

# Linux/Mac
export EPIDEMIC_ACCESS_KEY_ID="your_access_key_id"
export EPIDEMIC_ACCESS_KEY_SECRET="your_access_key_secret"
```

### 2. Run the Downloader

```bash
# Download all 60 tracks (recommended)
python download_all_platform_music.py

# Quick test - 5 tracks per platform (20 total)
python download_all_platform_music.py --quick

# Download for specific platforms only
python download_all_platform_music.py --platforms youtube,tiktok

# Resume interrupted downloads
python download_all_platform_music.py --resume
```

## What Gets Downloaded

### Total: 60 Tracks

#### YouTube (20 tracks)
- **Calm (10 tracks)**: 60-80 BPM
  - Perfect for: Tutorial videos, educational content, vlogs
  - Moods: Calm, peaceful, relaxed, ambient
  - Genres: Ambient, acoustic, cinematic

- **Energetic (10 tracks)**: 120-140 BPM
  - Perfect for: Product reviews, tech videos, lifestyle content
  - Moods: Energetic, upbeat, happy, positive
  - Genres: Electronic, indie, pop

#### TikTok (15 tracks)
- **High Energy (15 tracks)**: 140-160 BPM
  - Perfect for: Quick cuts, transitions, viral content
  - Moods: Energetic, powerful, aggressive, exciting
  - Genres: Electronic, beats, hip-hop

#### Instagram (15 tracks)
- **Fitness (5 tracks)**: 130-150 BPM
  - Perfect for: Workout videos, fitness tips, gym content
  - Moods: Energetic, motivational, powerful
  - Genres: Electronic, hip-hop, rock

- **Beauty (5 tracks)**: 90-120 BPM
  - Perfect for: Makeup tutorials, skincare routines, fashion
  - Moods: Elegant, sophisticated, calm, dreamy
  - Genres: Pop, electronic, ambient

- **Travel (5 tracks)**: 80-110 BPM
  - Perfect for: Travel vlogs, destination guides, adventures
  - Moods: Adventurous, inspiring, uplifting
  - Genres: Cinematic, indie, world

#### Twitter (10 tracks)
- **Professional (10 tracks)**: 100-130 BPM
  - Perfect for: News commentary, professional updates, threads
  - Moods: Corporate, confident, minimal, positive
  - Genres: Corporate, electronic, indie

## Output Structure

```
background_music_epidemic/
├── youtube/
│   ├── calm/
│   │   ├── youtube_calm_01_Track_Title_trackid.mp3
│   │   ├── youtube_calm_02_Track_Title_trackid.mp3
│   │   └── ... (10 tracks)
│   └── energetic/
│       ├── youtube_energetic_01_Track_Title_trackid.mp3
│       └── ... (10 tracks)
├── tiktok/
│   └── high_energy/
│       └── ... (15 tracks)
├── instagram/
│   ├── fitness/
│   │   └── ... (5 tracks)
│   ├── beauty/
│   │   └── ... (5 tracks)
│   └── travel/
│       └── ... (5 tracks)
├── twitter/
│   └── professional/
│       └── ... (10 tracks)
├── library_index.json        # Master catalog
└── download_log.json         # Download history
```

## Features

### 1. Parallel Downloading
- Downloads 5 tracks simultaneously
- Significantly faster than sequential downloads
- ~10 minutes for all 60 tracks (with good connection)

### 2. Smart Deduplication
- Checks `library_index.json` before downloading
- Compares by track ID, not filename
- Skips already downloaded tracks automatically

### 3. Automatic Retry Logic
- Retries failed downloads up to 3 times
- Exponential backoff between attempts
- Logs all failures for review

### 4. Quality Filtering
- **Instrumental Only**: Filters out tracks with vocals
- **BPM Matching**: Ensures tracks match platform requirements
- **Mood Alignment**: Selects tracks matching content type
- **High Quality**: Downloads 320kbps MP3 files

### 5. Progress Tracking
- Real-time download progress
- Platform and category breakdown
- Time estimation
- Success/failure statistics

### 6. Comprehensive Logging
- All downloads logged to `download_log.json`
- Track metadata saved to `library_index.json`
- Error messages for failed downloads
- Timestamps for all operations

## Usage Examples

### Example 1: First Time Setup
```bash
# Set credentials (one-time)
$env:EPIDEMIC_ACCESS_KEY_ID="your_key"
$env:EPIDEMIC_ACCESS_KEY_SECRET="your_secret"

# Download all tracks
python download_all_platform_music.py

# Expected output:
# - 60 tracks downloaded
# - ~10-15 minutes total time
# - Organized by platform and category
```

### Example 2: Add More Tracks Later
```bash
# Script automatically skips existing tracks
python download_all_platform_music.py

# Output: "All tracks already downloaded"
```

### Example 3: Test Before Full Download
```bash
# Quick mode - 5 tracks per platform
python download_all_platform_music.py --quick

# Downloads 20 tracks total (5 per platform)
# Takes ~2-3 minutes
```

### Example 4: Platform-Specific Downloads
```bash
# Only YouTube
python download_all_platform_music.py --platforms youtube

# Multiple platforms
python download_all_platform_music.py --platforms youtube,instagram

# Single category (modify script if needed)
python download_all_platform_music.py --platforms tiktok
```

### Example 5: Resume After Failure
```bash
# If download was interrupted
python download_all_platform_music.py --resume

# Continues from where it stopped
# Skips successfully downloaded tracks
```

## Library Management

### Checking Your Library
```python
import json

# Load library index
with open("background_music_epidemic/library_index.json") as f:
    library = json.load(f)

# Print statistics
print(f"Total tracks: {len(library['tracks'])}")
print(f"Platforms: {list(library['platforms'].keys())}")

# List tracks for a platform
youtube_tracks = library['platforms']['youtube']
for category, track_ids in youtube_tracks.items():
    print(f"{category}: {len(track_ids)} tracks")
```

### Finding Tracks
```python
# Search by BPM range
tracks = library['tracks']
calm_tracks = [t for t in tracks.values() if 60 <= t['bpm'] <= 80]

# Search by platform
youtube_tracks = [t for t in tracks.values() if t['platform'] == 'youtube']

# Search by category
fitness_tracks = [t for t in tracks.values() if t['category'] == 'fitness']
```

### Using Tracks in Videos
```python
from pathlib import Path

# Get all tracks for a category
library_index = Path("background_music_epidemic/library_index.json")
with open(library_index) as f:
    library = json.load(f)

# Get random track from category
import random
youtube_calm = library['platforms']['youtube']['calm']
track_id = random.choice(youtube_calm)
track_data = library['tracks'][track_id]

# Get file path
music_file = Path(track_data['file_path'])
print(f"Using: {music_file}")
```

## Troubleshooting

### Problem: Authentication Failed
```
ERROR: Authentication failed. Cannot proceed.
```

**Solution:**
1. Verify credentials are correct
2. Check if credentials are expired
3. Test credentials manually:
   ```bash
   curl -X POST https://partner-content-api.epidemicsound.com/v0/partner-token \
     -H "Content-Type: application/json" \
     -d '{"accessKeyId":"YOUR_KEY","accessKeySecret":"YOUR_SECRET"}'
   ```

### Problem: No Tracks Found
```
WARNING: No tracks found for category
```

**Solution:**
1. Search criteria might be too strict
2. Try broader search terms in the script
3. Check Epidemic Sound API status
4. Verify you have access to free tracks

### Problem: Download Timeout
```
ERROR: Download failed - Max retries exceeded
```

**Solution:**
1. Check internet connection
2. Increase `DOWNLOAD_TIMEOUT` in script (default: 180s)
3. Reduce `MAX_WORKERS` (default: 5)
4. Run `--resume` to continue

### Problem: Library Index Corrupted
```
WARNING: Failed to load library index
```

**Solution:**
1. Backup `library_index.json`
2. Delete corrupted file
3. Run script again to rebuild index

## Performance Optimization

### Speed Up Downloads
```python
# In the script, modify these constants:
MAX_WORKERS = 10  # More parallel downloads (default: 5)
REQUEST_TIMEOUT = 15  # Faster timeout (default: 30)
```

### Reduce API Calls
```python
# Download in batches
python download_all_platform_music.py --platforms youtube
python download_all_platform_music.py --platforms tiktok
# etc.
```

### Handle Rate Limits
```python
# Add delay between requests
import time
time.sleep(1)  # Add to download_single_track function
```

## Advanced Usage

### Custom Platform Configuration
```python
# Add new platform in PLATFORM_SPECS
PLATFORM_SPECS["linkedin"] = [
    TrackSpec(
        platform="linkedin",
        category="professional",
        bpm_min=90,
        bpm_max=110,
        moods=["corporate", "confident"],
        genres=["corporate", "electronic"],
        count=10,
        search_terms="professional business"
    )
]
```

### Filter by Custom Criteria
```python
# Modify search_tracks method to add custom filters
def search_tracks(self, spec: TrackSpec, limit: int = 60):
    # Add custom filtering logic here
    # Example: Only tracks longer than 2 minutes
    filtered_tracks = [t for t in tracks if t['length'] > 120]
```

### Batch Processing
```python
# Download tracks in smaller batches
for platform in platforms:
    download_platform_music(api, library, platform)
    time.sleep(60)  # Pause between platforms
```

## Integration with Video Pipeline

### Using Downloaded Music
```python
from pydub import AudioSegment
import random
import json

def get_background_music(platform: str, category: str):
    """Get random background music for platform/category"""

    # Load library
    with open("background_music_epidemic/library_index.json") as f:
        library = json.load(f)

    # Get tracks for category
    track_ids = library['platforms'][platform][category]
    track_id = random.choice(track_ids)
    track_data = library['tracks'][track_id]

    # Load audio file
    music = AudioSegment.from_mp3(track_data['file_path'])

    # Reduce volume to 15% for background use
    music = music - 16  # -16dB ≈ 15% volume

    return music, track_data

# Example usage
music, metadata = get_background_music("youtube", "calm")
print(f"Using: {metadata['title']} ({metadata['bpm']} BPM)")
```

### Loop Music for Longer Videos
```python
def loop_music(music: AudioSegment, target_duration_ms: int):
    """Loop music to match video duration"""

    if len(music) >= target_duration_ms:
        return music[:target_duration_ms]

    loops_needed = target_duration_ms // len(music) + 1
    looped = music * loops_needed
    return looped[:target_duration_ms]

# Example
music, _ = get_background_music("youtube", "energetic")
video_duration_ms = 180000  # 3 minutes
looped_music = loop_music(music, video_duration_ms)
```

### Mix with Narration
```python
def mix_narration_and_music(
    narration_file: str,
    platform: str,
    category: str,
    output_file: str
):
    """Mix narration with background music"""

    # Load narration
    narration = AudioSegment.from_mp3(narration_file)

    # Get background music
    music, _ = get_background_music(platform, category)

    # Loop music to match narration
    music = loop_music(music, len(narration))

    # Mix (music is already at 15% volume)
    final = narration.overlay(music)

    # Export
    final.export(output_file, format='mp3', bitrate='192k')

    return output_file

# Example
mix_narration_and_music(
    "narration.mp3",
    "youtube",
    "calm",
    "final_audio.mp3"
)
```

## Cost and API Usage

### Epidemic Sound API
- **Free Tier**: Access to curated free tracks
- **API Calls**: No rate limits documented
- **Download Limits**: Track URL expires after 1 hour (high quality)

### Expected API Usage
- **Authentication**: 2 calls (partner + user token)
- **Search**: 1 call per category (8 categories total)
- **Download URL**: 1 call per track (60 tracks)
- **Total**: ~70 API calls for full download

### Storage Requirements
- **Per Track**: ~8-12 MB (320kbps MP3)
- **Total**: ~500-700 MB for 60 tracks
- **With metadata**: ~700 MB total

## Best Practices

1. **Run Quick Mode First**: Test with `--quick` before full download
2. **Verify Credentials**: Test authentication before bulk download
3. **Use Resume**: If interrupted, use `--resume` to continue
4. **Backup Library Index**: Keep backup of `library_index.json`
5. **Monitor Disk Space**: Ensure 1GB+ free space
6. **Check Downloads**: Verify files aren't corrupted
7. **Update Regularly**: Re-run to get new tracks from Epidemic Sound

## Next Steps

After downloading music:
1. Test tracks in your video pipeline
2. Verify audio quality and volume levels
3. Create playlists for different content types
4. Integrate with automated video generation
5. Set up regular updates (weekly/monthly)

## Support

For issues:
1. Check `download_log.json` for error details
2. Verify API credentials and connectivity
3. Review Epidemic Sound API documentation
4. Check file permissions and disk space

## References

- Epidemic Sound API: https://developers.epidemicsite.com/docs/
- Project Documentation: See `EPIDEMIC_SOUND_API_COMPLETE_REFERENCE.md`
- Audio Processing: See `curate_background_music.py`
