# Epidemic Sound API Client - Quick Setup

Production-ready Python client for Epidemic Sound Partner Content API.

## Quick Start (5 minutes)

### 1. Get API Credentials

1. Go to https://developers.epidemicsite.com/
2. Sign up / Log in
3. Create a new application
4. Copy your **Access Key ID** and **Access Key Secret**

### 2. Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:EPIDEMIC_SOUND_ACCESS_KEY_ID = "your_access_key_id"
$env:EPIDEMIC_SOUND_ACCESS_KEY_SECRET = "your_access_key_secret"
```

**Windows (Command Prompt):**
```cmd
set EPIDEMIC_SOUND_ACCESS_KEY_ID=your_access_key_id
set EPIDEMIC_SOUND_ACCESS_KEY_SECRET=your_access_key_secret
```

**Linux/Mac:**
```bash
export EPIDEMIC_SOUND_ACCESS_KEY_ID="your_access_key_id"
export EPIDEMIC_SOUND_ACCESS_KEY_SECRET="your_access_key_secret"
```

**Or create `.env` file:**
```bash
EPIDEMIC_SOUND_ACCESS_KEY_ID=your_access_key_id
EPIDEMIC_SOUND_ACCESS_KEY_SECRET=your_access_key_secret
```

### 3. Install Dependencies

```bash
pip install requests
```

### 4. Test the Client

```bash
python epidemic_sound_examples.py
```

## Basic Usage (Copy & Paste)

```python
from epidemic_sound_client import EpidemicSoundClient

# Initialize and authenticate
with EpidemicSoundClient() as client:
    client.authenticate()

    # Search for tracks
    results = client.search_tracks(
        query="upbeat energetic",
        mood=["happy"],
        bpm_min=120,
        bpm_max=140,
        limit=10
    )

    # Download first track
    if results['tracks']:
        track = results['tracks'][0]
        client.download_track(
            track_id=track['id'],
            output_path="background_music.mp3",
            quality="high"  # 320kbps
        )
        print(f"Downloaded: {track['title']}")
```

## Common Use Cases

### 1. Get Background Music for Video

```python
from epidemic_sound_client import EpidemicSoundClient

def get_background_music(video_duration_seconds):
    with EpidemicSoundClient() as client:
        client.authenticate()

        # Search for instrumental tracks
        results = client.search_tracks(
            mood=["inspiring", "calm"],
            limit=50
        )

        # Filter by duration and no vocals
        candidates = [
            t for t in results['tracks']
            if not t['hasVocals']
            and abs(t['length'] - video_duration_seconds) <= 20
        ]

        # Get closest match
        best = min(candidates, key=lambda t: abs(t['length'] - video_duration_seconds))

        # Download
        client.download_track(best['id'], "background.mp3", quality="high")
        client.report_usage(best['id'], platform="youtube")

        return best

# Use it
track = get_background_music(180)  # 3-minute video
print(f"Selected: {track['title']}")
```

### 2. Search by Mood and Download

```python
from epidemic_sound_client import EpidemicSoundClient

with EpidemicSoundClient() as client:
    client.authenticate()

    # Search epic music
    results = client.search_tracks(
        mood=["epic", "dramatic"],
        bpm_min=90,
        bpm_max=120,
        limit=5
    )

    # Download all results
    for track in results['tracks']:
        filename = f"{track['id']}_{track['title']}.mp3"
        client.download_track(track['id'], filename, quality="high")
        print(f"Downloaded: {track['title']}")
```

### 3. Find Similar Tracks

```python
from epidemic_sound_client import EpidemicSoundClient

with EpidemicSoundClient() as client:
    client.authenticate()

    # Find similar to a track you like
    similar = client.find_similar_tracks("6rUPerw2po", limit=10)

    for track in similar['tracks']:
        print(f"{track['title']} - {track['bpm']} BPM")
```

## Files Created

| File | Description |
|------|-------------|
| `epidemic_sound_client.py` | Main API client (production-ready) |
| `epidemic_sound_examples.py` | 10+ practical examples |
| `EPIDEMIC_SOUND_CLIENT_GUIDE.md` | Complete documentation |
| `EPIDEMIC_SOUND_SETUP.md` | This file (quick setup) |

## Quick Reference

### Client Initialization

```python
from epidemic_sound_client import EpidemicSoundClient

# From environment variables
client = EpidemicSoundClient()

# With explicit credentials
client = EpidemicSoundClient(
    access_key_id="your_key",
    access_key_secret="your_secret"
)

# With custom settings
client = EpidemicSoundClient(
    user_id="custom-user-id",
    cache_ttl=7200  # 2 hours
)
```

### Search Methods

```python
# Text search
results = client.search_tracks(query="upbeat energetic")

# Filter by mood
results = client.search_tracks(mood=["happy", "exciting"])

# Filter by genre
results = client.search_tracks(genre=["electronic", "rock"])

# Filter by BPM
results = client.search_tracks(bpm_min=120, bpm_max=140)

# Combined filters
results = client.search_tracks(
    query="workout motivation",
    mood=["energetic"],
    bpm_min=130,
    limit=20
)
```

### Download Methods

```python
# Single download
client.download_track("track_id", "output.mp3", quality="high")

# Batch download
track_ids = ["id1", "id2", "id3"]
client.batch_download(track_ids, "downloads/", quality="high")

# Get download URL only
info = client.get_download_url("track_id", quality="high")
print(info['url'])  # Signed URL
print(info['expires'])  # Expiration time
```

### Browse Methods

```python
# Get moods
moods = client.get_moods(type_filter="featured")

# Get genres
genres = client.get_genres(type_filter="featured")

# Get collections (playlists)
collections = client.get_collections(limit=10)

# Get suggestions (autocomplete)
suggestions = client.get_suggestions("hap")
```

## Search Filters Reference

### Moods
Common mood IDs:
- `happy`, `sad`, `energetic`, `calm`, `relaxed`
- `epic`, `dramatic`, `triumphant`, `powerful`
- `inspiring`, `uplifting`, `motivational`
- `playful`, `fun`, `exciting`
- `dark`, `mysterious`, `suspenseful`
- `romantic`, `dreamy`, `peaceful`

### Genres
Common genre IDs:
- `electronic`, `rock`, `hip-hop`, `acoustic`
- `cinematic`, `ambient`, `jazz`, `classical`
- `pop`, `indie`, `folk`, `world`

### BPM Ranges
- **Slow**: 60-90 BPM (ballads, ambient)
- **Medium**: 90-120 BPM (pop, hip-hop)
- **Upbeat**: 120-140 BPM (dance, electronic)
- **Fast**: 140-180 BPM (drum & bass, metal)

### Quality Options
- `"normal"`: 128kbps MP3 (24-hour expiration)
- `"high"`: 320kbps MP3 (1-hour expiration)

## Integration with Video Pipeline

```python
from epidemic_sound_client import EpidemicSoundClient

def add_music_to_video_pipeline(video_duration, video_mood):
    """Integrate with video generation pipeline."""

    # Mood mapping
    mood_map = {
        "professional": ["inspiring", "uplifting"],
        "energetic": ["energetic", "powerful"],
        "calm": ["relaxed", "peaceful"],
        "epic": ["epic", "dramatic"]
    }

    with EpidemicSoundClient() as client:
        client.authenticate()

        # Search
        results = client.search_tracks(
            mood=mood_map.get(video_mood, ["neutral"]),
            limit=50
        )

        # Filter
        tracks = [
            t for t in results['tracks']
            if not t['hasVocals']
            and abs(t['length'] - video_duration) <= 20
        ]

        # Select best
        best = min(tracks, key=lambda t: abs(t['length'] - video_duration))

        # Download
        output_path = "background_music.mp3"
        client.download_track(best['id'], output_path, quality="high")
        client.report_usage(best['id'], platform="youtube")

        return {
            'file_path': output_path,
            'title': best['title'],
            'duration': best['length'],
            'bpm': best['bpm']
        }

# Use in pipeline
music_info = add_music_to_video_pipeline(
    video_duration=180,
    video_mood="professional"
)

print(f"Added music: {music_info['title']}")
```

## Error Handling

```python
from epidemic_sound_client import (
    EpidemicSoundClient,
    AuthenticationError,
    RateLimitError,
    DownloadError,
    APIError
)

try:
    with EpidemicSoundClient() as client:
        client.authenticate()
        results = client.search_tracks(query="epic")

except AuthenticationError:
    print("Authentication failed - check credentials")

except RateLimitError as e:
    print(f"Rate limited - retry after {e.reset_time}")

except DownloadError:
    print("Download failed - retry or use different quality")

except APIError as e:
    print(f"API error ({e.status_code}): {e}")
```

## Best Practices

1. **Always use context manager** (`with` statement)
2. **Filter for instrumental** tracks if using as background music
3. **Match video duration** for seamless integration
4. **Report usage** after downloading tracks
5. **Handle rate limits** gracefully
6. **Use caching** for repeated searches

## Troubleshooting

### "Authentication failed"
- Check environment variables are set correctly
- Verify credentials at https://developers.epidemicsite.com/

### "No tracks found"
- Try broader search (fewer filters)
- Check available moods/genres: `client.get_moods()`
- Use `use_cache=False` for fresh results

### "Download failed"
- Check if track requires subscription (`tierOption: "PAID"`)
- Try `quality="normal"` instead of `"high"`
- Ensure output directory exists

### "Rate limit exceeded"
- Wait for rate limit reset (check email for notifications)
- Implement delays between requests
- Contact Epidemic Sound for higher limits

## Resources

- **Full Documentation**: `EPIDEMIC_SOUND_CLIENT_GUIDE.md`
- **Examples**: `epidemic_sound_examples.py`
- **API Reference**: `EPIDEMIC_SOUND_API_COMPLETE_REFERENCE.md`
- **Official Docs**: https://developers.epidemicsite.com/docs/

## Support

For API issues:
1. Check official documentation
2. Review error messages in logs
3. Contact via developer portal

## Next Steps

1. Run examples: `python epidemic_sound_examples.py`
2. Read full guide: `EPIDEMIC_SOUND_CLIENT_GUIDE.md`
3. Integrate into your video pipeline
4. Explore advanced features (similar tracks, beats, etc.)

---

**Ready to use!** Start with the examples and customize for your needs.
