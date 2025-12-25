# Music Library Manager - Complete Guide

Comprehensive music library management system for Epidemic Sound tracks. Organizes, catalogs, and provides easy access to your downloaded music collection with intelligent platform-specific recommendations.

## Features

### Core Functionality
- **Smart Library Indexing**: Automatically scans and catalogs all MP3 tracks
- **Metadata Extraction**: Extracts audio metadata (duration, bitrate, sample rate)
- **Intelligent Mood Detection**: Infers mood from track titles using keyword analysis
- **BPM Estimation**: Estimates BPM based on mood characteristics
- **Platform-Specific Recommendations**: Optimized track selection for YouTube, TikTok, Instagram, etc.
- **Usage Tracking**: Records which tracks are used in which videos
- **Favorites System**: Mark and manage favorite tracks
- **Rating System**: Rate tracks 0-5 stars
- **Search & Discovery**: Fast search across titles, artists, moods, and tags

### Platform Support
- **YouTube**: Calm/uplifting tracks (60-90 BPM, 15% volume)
- **TikTok**: Energetic/upbeat tracks (100-140 BPM, 30% volume)
- **Instagram**: Trendy/uplifting tracks (90-120 BPM, 25% volume)
- **Podcast**: Ambient/background tracks (50-70 BPM, 10% volume)
- **Shorts**: Dynamic/energetic tracks (110-130 BPM, 20% volume)

## Installation

### Requirements
```bash
# Core requirement
pip install mutagen  # For audio metadata extraction

# Optional (for audio mixing)
pip install pydub
```

### Setup
```bash
# 1. Ensure your music is in the background_music/ directory
ls background_music/*.mp3

# 2. Run initial scan to build library index
python music_library_manager.py --scan

# 3. View library statistics
python music_library_manager.py --stats
```

## Quick Start

### 1. Scan Your Library
```bash
# Initial scan (indexes new tracks)
python music_library_manager.py --scan

# Force rescan (updates all metadata)
python music_library_manager.py --scan --force-rescan
```

**Output:**
```
======================================================================
SCANNING MUSIC LIBRARY
======================================================================

[FOUND] 87 MP3 files in background_music

[INDEXING] ES_Soar - Daniella Ljungsberg.mp3
  Title: Soar
  Artist: Daniella Ljungsberg
  Mood: uplifting
  BPM: 83
  Duration: 307.4s

======================================================================
[COMPLETE] Scan complete!
  New tracks: 87
  Updated tracks: 0
  Total indexed: 87
======================================================================
```

### 2. View Library Statistics
```bash
python music_library_manager.py --stats
```

**Output:**
```
======================================================================
MUSIC LIBRARY STATISTICS
======================================================================

OVERVIEW:
  Total Tracks: 87
  Total Duration: 4.6 hours
  Total Size: 507.6 MB
  Favorites: 0
  Total Usage: 0 times

MOOD DISTRIBUTION:
  Neutral: 80 (92.0%)
  Emotional: 2 (2.3%)
  Upbeat: 2 (2.3%)
  Energetic: 1 (1.1%)
  Uplifting: 1 (1.1%)
  Ambient: 1 (1.1%)

BPM DISTRIBUTION:
  80-100 BPM: 78 (89.7%)
  60-80 BPM: 3 (3.4%)
  100-120 BPM: 3 (3.4%)
  120+ BPM: 3 (3.4%)

TOP ARTISTS:
  Blue Saga: 4 tracks
  Nbhd Nick: 3 tracks
  Ave Air: 3 tracks
======================================================================
```

### 3. Get Platform Recommendations
```bash
# Get best track for YouTube video (300 seconds)
python music_library_manager.py --recommend youtube --duration 300

# Get recommendation with mood preference
python music_library_manager.py --recommend tiktok --mood energetic

# Get recommendation for Instagram
python music_library_manager.py --recommend instagram --duration 180
```

**Output:**
```
[SEARCHING] Best track for YOUTUBE
  Duration target: 300s

[RECOMMENDED]
  Title: Soar
  Artist: Daniella Ljungsberg
  Mood: uplifting
  BPM: 83
  Duration: 307.4s
  Usage: 0 times
  Rating: ----- (0/5)
  Platform Match Score: 95.0/100

[ALTERNATIVES]
  1. Space Waves by Ben Elson (Score: 95.0)
  2. 2 Broken Hearts (Instrumental Version) by Particle House (Score: 70.0)
```

### 4. Search for Tracks
```bash
# Search by keyword
python music_library_manager.py --find "uplifting"

# Search by artist
python music_library_manager.py --find "Blue Saga"

# Search by mood
python music_library_manager.py --find "energetic"
```

**Output:**
```
[SEARCH] Found 1 tracks matching 'uplifting'

1. Soar by Daniella Ljungsberg
   Mood: uplifting | BPM: 83 | Duration: 307.4s
   Usage: 0 | Rating:  (0/5)
```

### 5. Get Track Rotation
```bash
# Get 5 different tracks for video series
python music_library_manager.py --rotation youtube --count 5

# Get rotation with mood filter
python music_library_manager.py --rotation tiktok --count 10 --mood upbeat
```

**Output:**
```
[ROTATION] 5 tracks for TIKTOK

1. Lava_Powers (Ooyy Remix) (Instrumental Version) by Janset
   Mood: energetic | BPM: 120 | Score: 95.0
   File: ES_Lava_Powers (Ooyy Remix) (Instrumental Version) - Janset.mp3

2. Sunny Daze by Sarah, the Illstrumentalist
   Mood: upbeat | BPM: 127 | Score: 95.0
   File: ES_Sunny Daze - Sarah, the Illstrumentalist.mp3

3. The Joy of the Lord Is My Strength by JOYSPRING
   Mood: upbeat | BPM: 126 | Score: 95.0
   File: ES_The Joy of the Lord Is My Strength - JOYSPRING.mp3
```

### 6. View Platform Configurations
```bash
python music_library_manager.py --list-platforms
```

**Output:**
```
======================================================================
SUPPORTED PLATFORMS
======================================================================

YOUTUBE
  Background Music Volume: 15% (-25 dB)
  Optimal BPM: 60-90
  Preferred Moods: calm, uplifting, ambient, motivational
  Energy Level: medium

TIKTOK
  Background Music Volume: 30% (-15 dB)
  Optimal BPM: 100-140
  Preferred Moods: energetic, upbeat, trendy, dynamic
  Energy Level: high
======================================================================
```

## Python API Usage

### Basic Integration

```python
from music_library_manager import MusicLibraryManager

# Initialize manager
manager = MusicLibraryManager(
    music_dir="background_music",
    metadata_file="music_library_metadata.json"
)

# Scan library
manager.scan_library()

# Get recommendation for YouTube
track = manager.get_music_for_platform(
    platform="youtube",
    duration=300,  # 5 minutes
    mood="uplifting"
)

print(f"Selected: {track['title']} by {track['artist']}")
print(f"File: {track['file_path']}")
```

### Get Random Track with Filters

```python
# Get random upbeat track between 100-130 BPM
track = manager.get_random_music(
    platform="tiktok",
    filters={
        "mood": "upbeat",
        "min_bpm": 100,
        "max_bpm": 130
    }
)
```

### Get Track Rotation for Video Series

```python
# Get 10 different tracks for video series
rotation = manager.get_music_rotation(
    platform="youtube",
    video_count=10,
    filters={
        "mood": "calm",
        "min_bpm": 60,
        "max_bpm": 90
    }
)

for i, track in enumerate(rotation, 1):
    print(f"Video {i}: {track['title']} ({track['bpm']} BPM)")
```

### Track Usage Statistics

```python
# Record track usage
track_hash = "abc123def456"
manager.track_usage(
    track_hash=track_hash,
    video_title="How to Use AI Tools",
    platform="youtube"
)

# Set rating
manager.set_rating(track_hash, rating=5)

# Toggle favorite
manager.toggle_favorite(track_hash)
```

### Auto-Mix Audio for Video

```python
# Automatically mix background music with narration
# at platform-appropriate volume
mixed_audio_path = manager.prepare_audio_for_video(
    track_path="background_music/ES_Soar - Daniella Ljungsberg.mp3",
    narration_path="output/narration.mp3",
    platform="youtube",
    output_path="output/final_audio.mp3"
)

# Platform volumes:
# - YouTube: -25 dB (15% volume)
# - TikTok: -15 dB (30% volume)
# - Instagram: -18 dB (25% volume)
# - Podcast: -30 dB (10% volume)
```

### Search Library

```python
# Search for tracks
results = manager.search_tracks("calm ambient", limit=10)

for track in results:
    print(f"{track['title']} - {track['mood']} - {track['bpm']} BPM")
```

### Get Statistics

```python
# Get comprehensive library statistics
stats = manager.get_library_stats()

print(f"Total tracks: {stats['total_tracks']}")
print(f"Total duration: {stats['total_duration_hours']:.1f} hours")
print(f"Most used: {stats['most_used'][:5]}")
```

## Advanced Usage

### Custom Platform Configuration

```python
# Access platform configurations
config = manager.platform_configs["youtube"]
print(f"YouTube optimal BPM: {config['optimal_bpm']}")
print(f"Preferred moods: {config['preferred_moods']}")
print(f"Volume reduction: {config['bg_music_volume_db']} dB")
```

### Batch Processing

```python
# Process multiple videos with different tracks
video_titles = [
    "Introduction to AI Tools",
    "Advanced AI Features",
    "AI Tool Comparison"
]

# Get rotation
tracks = manager.get_music_rotation(
    platform="youtube",
    video_count=len(video_titles)
)

# Process each video with unique track
for video_title, track in zip(video_titles, tracks):
    print(f"Processing: {video_title}")
    print(f"Music: {track['title']}")

    # Mix audio
    mixed_audio = manager.prepare_audio_for_video(
        track_path=track['file_path'],
        narration_path=f"narration/{video_title}.mp3",
        platform="youtube",
        output_path=f"output/{video_title}_mixed.mp3"
    )

    # Record usage
    manager.track_usage(
        track_hash=track['file_hash'],
        video_title=video_title,
        platform="youtube"
    )
```

### Custom Mood Detection

The system automatically infers mood from track titles using keyword matching:

- **Calm**: "calm", "peace", "serene", "tranquil", "quiet", "gentle", "soft"
- **Uplifting**: "uplift", "inspire", "rise", "soar", "ascend", "elevate", "hope"
- **Energetic**: "energy", "power", "dynamic", "intense", "drive", "pulse", "vibrant"
- **Ambient**: "ambient", "atmosphere", "space", "drift", "float", "ether", "cosmic"
- **Motivational**: "motivate", "success", "achieve", "triumph", "victory", "champion"
- **Upbeat**: "upbeat", "happy", "joy", "cheerful", "bright", "sunny", "positive"
- **Dark**: "dark", "shadow", "night", "mysterious", "sinister", "ominous"
- **Epic**: "epic", "grand", "massive", "majestic", "heroic", "cinematic"
- **Emotional**: "emotion", "heart", "feel", "sentiment", "tender", "touch"
- **Background**: "background", "underscore", "subtle", "minimal", "simple"

## Metadata Storage

The system stores all metadata in `music_library_metadata.json`:

```json
{
  "tracks": {
    "abc123def456": {
      "file_path": "D:\\workspace\\VideoGen_YouTube\\background_music\\ES_Soar.mp3",
      "filename": "ES_Soar - Daniella Ljungsberg.mp3",
      "file_hash": "abc123def456",
      "title": "Soar",
      "artist": "Daniella Ljungsberg",
      "source": "epidemic_sound",
      "mood": "uplifting",
      "bpm": 83,
      "duration": 307.4,
      "bitrate": 320000,
      "sample_rate": 44100,
      "channels": 2,
      "file_size_mb": 12.3,
      "indexed_date": "2025-12-22T10:30:00",
      "usage_count": 3,
      "rating": 5,
      "is_favorite": true,
      "tags": ["youtube", "calm"],
      "notes": "Perfect for educational videos"
    }
  },
  "usage": {
    "abc123def456_20251222_103000": {
      "track_hash": "abc123def456",
      "track_title": "Soar",
      "video_title": "How to Use AI Tools",
      "platform": "youtube",
      "date": "2025-12-22T10:30:00"
    }
  },
  "favorites": ["abc123def456"],
  "stats": {}
}
```

## Platform Scoring Algorithm

The system calculates a platform suitability score (0-100) based on:

1. **BPM Match** (+20 points): Track BPM within optimal range
2. **Close BPM** (+10 points): Track BPM near optimal range
3. **Mood Match** (+25 points): Track mood matches platform preferences
4. **Favorite Bonus** (+10 points): Track is marked as favorite
5. **Usage Penalty** (-2 per use): Reduces score for overused tracks

**Example:**
```python
# YouTube track scoring
# Optimal BPM: 60-90, Preferred moods: calm, uplifting, ambient

track = {
    "bpm": 83,
    "mood": "uplifting",
    "is_favorite": True,
    "usage_count": 1
}

score = 50  # Base score
score += 20  # BPM in optimal range
score += 25  # Mood matches
score += 10  # Is favorite
score -= 2   # Used once
# Final score: 103 (capped at 100) = 100.0
```

## Integration with Video Pipeline

### MoviePy Integration

```python
from moviepy.editor import VideoFileClip, AudioFileClip
from music_library_manager import MusicLibraryManager

# Initialize
manager = MusicLibraryManager()

# Get track for video
track = manager.get_music_for_platform("youtube", duration=300)

# Mix audio
mixed_audio = manager.prepare_audio_for_video(
    track_path=track['file_path'],
    narration_path="output/narration.mp3",
    platform="youtube",
    output_path="output/final_audio.mp3"
)

# Add to video
video = VideoFileClip("output/video.mp4")
audio = AudioFileClip(mixed_audio)
final_video = video.set_audio(audio)
final_video.write_videofile("output/final_video.mp4")

# Track usage
manager.track_usage(
    track_hash=track['file_hash'],
    video_title="My Video",
    platform="youtube"
)
```

### FFmpeg Integration

```python
import subprocess
from music_library_manager import MusicLibraryManager

# Get track
manager = MusicLibraryManager()
track = manager.get_music_for_platform("youtube", duration=300)

# Use FFmpeg to mix
cmd = [
    'ffmpeg', '-y',
    '-i', 'output/video.mp4',
    '-i', track['file_path'],
    '-filter_complex',
    f'[1:a]volume=-25dB[music];[0:a][music]amix=inputs=2:duration=first',
    '-c:v', 'copy',
    'output/final_video.mp4'
]
subprocess.run(cmd)
```

## Best Practices

### 1. Regular Library Scans
```bash
# Scan weekly when adding new tracks
python music_library_manager.py --scan
```

### 2. Track Your Usage
```python
# Always record usage to prevent track repetition
manager.track_usage(track_hash, video_title, platform)
```

### 3. Use Favorites
```python
# Mark great tracks as favorites for priority selection
manager.toggle_favorite(track_hash)
manager.set_rating(track_hash, 5)
```

### 4. Platform-Specific Selection
```python
# Always use platform parameter for optimal results
track = manager.get_music_for_platform(
    platform="youtube",  # Not "generic"
    duration=300,
    mood="uplifting"
)
```

### 5. Use Rotation for Series
```python
# For video series, use rotation to ensure variety
tracks = manager.get_music_rotation("youtube", 10)
```

## Troubleshooting

### Issue: "No suitable tracks found"
**Solution:** Check filters - duration/mood may be too restrictive
```python
# Too restrictive
track = manager.get_music_for_platform("youtube", duration=30, mood="energetic")

# Better
track = manager.get_music_for_platform("youtube", duration=None, mood=None)
```

### Issue: "Unicode error on Windows"
**Solution:** Already fixed - uses ASCII-safe characters (*, -)

### Issue: "Mutagen not installed"
**Solution:**
```bash
pip install mutagen
```
System will work without it but with limited metadata extraction.

### Issue: "Track always returns same music"
**Solution:** Use rotation or set usage tracking
```python
# Record usage to prevent repeats
manager.track_usage(track['file_hash'], video_title, platform)
```

## Performance Tips

1. **Cache metadata**: Metadata file is cached - no need to rescan unless adding new tracks
2. **Use filters**: Narrow search with BPM/mood filters for faster results
3. **Batch operations**: Process multiple videos in one session
4. **Index once**: Run `--scan` only when library changes

## CLI Reference

### Scan Commands
```bash
python music_library_manager.py --scan                    # Scan new tracks
python music_library_manager.py --scan --force-rescan     # Rescan all tracks
```

### Query Commands
```bash
python music_library_manager.py --stats                   # Show statistics
python music_library_manager.py --find "query"            # Search tracks
python music_library_manager.py --list-platforms          # List platforms
```

### Recommendation Commands
```bash
python music_library_manager.py --recommend PLATFORM      # Get recommendation
python music_library_manager.py --recommend PLATFORM --duration SEC
python music_library_manager.py --recommend PLATFORM --mood MOOD
```

### Rotation Commands
```bash
python music_library_manager.py --rotation PLATFORM       # Get 5 tracks
python music_library_manager.py --rotation PLATFORM --count N
python music_library_manager.py --rotation PLATFORM --mood MOOD
```

### Custom Paths
```bash
python music_library_manager.py --music-dir PATH --metadata-file FILE.json
```

## Library Statistics

Your current library:
- **Total Tracks**: 87
- **Total Duration**: 4.6 hours
- **Total Size**: 507.6 MB
- **Primary Source**: Epidemic Sound
- **Top Moods**: Neutral (80), Emotional (2), Upbeat (2)
- **BPM Range**: Mostly 80-100 BPM (89.7%)

## Future Enhancements

Potential features to add:
- AI-based mood detection using audio analysis
- Automatic BPM detection using librosa
- Genre classification
- Energy level detection
- Vocal detection
- Key signature detection
- Similar track recommendations
- Playlist generation
- Export to CSV/Excel

## License

This tool is designed for managing Epidemic Sound tracks. Ensure you have proper Epidemic Sound licensing for your videos.

## Support

For issues or questions:
1. Check this README
2. Review the metadata JSON file
3. Run `--stats` to verify library state
4. Test with `--find` to check search functionality

---

**Quick Reference Card**

```bash
# Most Common Commands
python music_library_manager.py --scan                          # Index library
python music_library_manager.py --stats                         # View stats
python music_library_manager.py --recommend youtube             # Get YouTube track
python music_library_manager.py --rotation tiktok --count 5     # Get 5 TikTok tracks
python music_library_manager.py --find "uplifting"              # Search library
```

**File Structure**
```
VideoGen_YouTube/
├── background_music/                      # Music library (87 tracks)
│   ├── ES_Soar - Daniella Ljungsberg.mp3
│   └── ...
├── music_library_manager.py               # Main script
├── music_library_metadata.json            # Metadata database
└── MUSIC_LIBRARY_MANAGER_README.md        # This file
```
