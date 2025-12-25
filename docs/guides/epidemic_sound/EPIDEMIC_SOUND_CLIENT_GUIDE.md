# Epidemic Sound API Client - Complete Guide

A production-ready Python client for the Epidemic Sound Partner Content API with comprehensive features for music integration in your video generation workflow.

## Features

- **Authentication**: Partner token flow with automatic token refresh
- **Search**: Semantic search with genre, mood, BPM, and vocal filters
- **Download**: High-quality MP3 downloads (320kbps) with retry logic
- **Streaming**: HLS streaming support
- **Recommendations**: AI-powered similar track suggestions
- **Rate Limiting**: Exponential backoff with intelligent retry
- **Caching**: Built-in caching for search results
- **Error Handling**: Comprehensive exception handling
- **Logging**: Detailed logging for debugging
- **Batch Operations**: Download multiple tracks efficiently

---

## Installation

### Prerequisites

```bash
pip install requests
```

### Setup Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
EPIDEMIC_SOUND_ACCESS_KEY_ID=your_access_key_id
EPIDEMIC_SOUND_ACCESS_KEY_SECRET=your_access_key_secret
```

Get your credentials from:
https://developers.epidemicsite.com/

---

## Quick Start

### Basic Usage

```python
from epidemic_sound_client import EpidemicSoundClient

# Initialize client (uses env variables)
client = EpidemicSoundClient()

# Authenticate
client.authenticate()

# Search for tracks
results = client.search_tracks(
    query="upbeat energetic",
    mood=["happy", "energetic"],
    bpm_min=120,
    bpm_max=140,
    limit=10
)

# Print results
for track in results['tracks']:
    print(f"{track['title']} - {track['bpm']} BPM")

# Download a track
client.download_track(
    track_id=results['tracks'][0]['id'],
    output_path="music/track.mp3",
    quality="high"
)
```

### Using Context Manager (Recommended)

```python
from epidemic_sound_client import EpidemicSoundClient

with EpidemicSoundClient() as client:
    client.authenticate()

    results = client.search_tracks(query="cinematic epic")

    for track in results['tracks'][:5]:
        print(f"{track['title']} - {', '.join(track['mainArtists'])}")
```

---

## API Methods

### Authentication

#### `authenticate(force_refresh=False)`

Perform authentication and return user token. Automatically refreshes expired tokens.

```python
token = client.authenticate()
```

### Search & Discovery

#### `search_tracks(query, genre, mood, bpm_min, bpm_max, ...)`

Search tracks with semantic understanding and filters.

**Parameters:**
- `query` (str, optional): Natural language search query
- `genre` (list, optional): List of genre IDs
- `mood` (list, optional): List of mood IDs
- `bpm_min` (int, optional): Minimum BPM
- `bpm_max` (int, optional): Maximum BPM
- `sort` (str): "Relevance", "Date", or "Title"
- `order` (str): "asc" or "desc"
- `limit` (int): Results per page (max 60)
- `offset` (int): Pagination offset
- `use_cache` (bool): Use cached results

**Returns:** Dictionary with `tracks`, `pagination`, `links`, `aggregations`

**Example:**
```python
# Semantic search
results = client.search_tracks(query="calm beach sunset")

# Filter by mood and BPM
results = client.search_tracks(
    mood=["relaxed", "dreamy"],
    bpm_min=80,
    bpm_max=100,
    limit=20
)

# Complex filters
results = client.search_tracks(
    query="workout motivation",
    genre=["electronic", "hip-hop"],
    mood=["energetic", "powerful"],
    bpm_min=130,
    bpm_max=150,
    sort="Relevance",
    limit=50
)
```

#### `find_similar_tracks(track_id, limit, offset)`

Find tracks similar to a given track using AI recommendations.

```python
similar = client.find_similar_tracks("6rUPerw2po", limit=10)

for track in similar['tracks']:
    print(f"Similar: {track['title']}")
```

#### `get_track_metadata(track_id)`

Get detailed metadata for a specific track.

```python
metadata = client.get_track_metadata("6rUPerw2po")

print(f"Title: {metadata.title}")
print(f"BPM: {metadata.bpm}")
print(f"Duration: {metadata.length}s")
print(f"Vocals: {metadata.has_vocals}")
print(f"Moods: {[m['name'] for m in metadata.moods]}")
```

#### `get_moods(type_filter, sort, order, limit, offset)`

Browse available moods.

```python
moods = client.get_moods(type_filter="featured", limit=20)

for mood in moods['moods']:
    print(f"{mood['name']} (ID: {mood['id']})")
```

**Type Filters:**
- `"all"`: Complete library
- `"featured"`: Featured moods on epidemicsound.com
- `"partner-tier"`: Available in your subscription

#### `get_genres(type_filter, sort, order, limit, offset)`

Browse available genres.

```python
genres = client.get_genres(type_filter="featured", limit=20)

for genre in genres['genres']:
    print(f"{genre['name']} (ID: {genre['id']})")
```

#### `get_collections(exclude_tracks, limit, offset)`

Get curated playlists.

```python
collections = client.get_collections(limit=10)

for collection in collections['collections']:
    print(f"{collection['name']} - {collection['trackCount']} tracks")
```

#### `get_suggestions(query)`

Get autocomplete suggestions for search.

```python
suggestions = client.get_suggestions("hap")
# Returns suggestions like "happy", "happiness", etc.
```

### Download & Streaming

#### `get_download_url(track_id, quality)`

Get signed download URL for a track.

**Parameters:**
- `track_id` (str): Track identifier
- `quality` (str): "normal" (128kbps) or "high" (320kbps)

**Returns:** Dictionary with `url` and `expires`

```python
download_info = client.get_download_url("6rUPerw2po", quality="high")

print(f"URL: {download_info['url']}")
print(f"Expires: {download_info['expires']}")
```

**URL Expiration:**
- Normal quality: 24 hours
- High quality: 1 hour

#### `download_track(track_id, output_path, quality, chunk_size)`

Download track to file with automatic retry.

```python
# Download single track
client.download_track(
    track_id="6rUPerw2po",
    output_path="music/epic_track.mp3",
    quality="high"
)

# Download with custom chunk size
client.download_track(
    track_id="6rUPerw2po",
    output_path="music/track.mp3",
    quality="high",
    chunk_size=16384  # 16KB chunks
)
```

#### `batch_download(track_ids, output_dir, quality, filename_template)`

Download multiple tracks efficiently.

```python
track_ids = ["track1", "track2", "track3"]

# Download with default naming
files = client.batch_download(
    track_ids=track_ids,
    output_dir="music/downloads/",
    quality="high"
)

# Download with custom naming
files = client.batch_download(
    track_ids=track_ids,
    output_dir="music/downloads/",
    quality="high",
    filename_template="{track_id}_epic.mp3"
)

print(f"Downloaded {len(files)} files")
```

#### `get_stream_url(track_id)`

Get HLS streaming URL for preview/playback.

```python
stream_info = client.get_stream_url("6rUPerw2po")
print(f"Stream URL: {stream_info['url']}")
```

**Benefits of HLS Streaming:**
- Smaller file transfers
- Adaptive quality (switches based on connection speed)
- AAC encoding (better compression than MP3)
- No subscription required for previews

### Advanced Features

#### `get_track_beats(track_id)`

Get beat timestamp data for video synchronization.

```python
beats = client.get_track_beats("6rUPerw2po")

for beat in beats['beats'][:10]:
    print(f"Beat at {beat['timestamp']}s")

# Use for video editing sync
```

#### `report_usage(track_id, platform, user_id)`

Report track usage (required for attribution).

```python
# Report single usage
client.report_usage(
    track_id="6rUPerw2po",
    platform="youtube"
)

# Report with custom user ID
client.report_usage(
    track_id="6rUPerw2po",
    platform="instagram",
    user_id="hashed-user-123"
)
```

**Supported Platforms:**
- `youtube`
- `tiktok`
- `instagram`
- `facebook`
- `twitch`
- `twitter`
- `local` (downloaded to device)
- `other`

#### `report_usage_bulk(events)`

Report multiple usage events efficiently.

```python
events = [
    {
        "trackId": "track1",
        "userId": "user123",
        "platform": "youtube",
        "timestamp": "2025-12-22T10:00:00Z"
    },
    {
        "trackId": "track2",
        "userId": "user123",
        "platform": "instagram",
        "timestamp": "2025-12-22T10:05:00Z"
    }
]

client.report_usage_bulk(events)
```

### Cache Management

#### `clear_cache()`

Clear all cached search results.

```python
client.clear_cache()
```

#### `cleanup_cache()`

Remove only expired items from cache.

```python
client.cleanup_cache()
```

#### `get_cache_stats()`

Get cache statistics.

```python
stats = client.get_cache_stats()
print(f"Cached items: {stats['total_items']}")
print(f"TTL: {stats['ttl_seconds']}s")
```

---

## Complete Workflow Examples

### Example 1: Search and Download for Video Background Music

```python
from epidemic_sound_client import EpidemicSoundClient

with EpidemicSoundClient() as client:
    client.authenticate()

    # Search for upbeat background music
    results = client.search_tracks(
        query="upbeat corporate background",
        mood=["happy", "inspiring"],
        bpm_min=115,
        bpm_max=130,
        limit=10
    )

    # Filter for tracks without vocals
    instrumental_tracks = [
        track for track in results['tracks']
        if not track['hasVocals']
    ]

    # Download top 3 tracks
    for track in instrumental_tracks[:3]:
        filename = f"{track['id']}_{track['title'].replace(' ', '_')}.mp3"
        client.download_track(
            track_id=track['id'],
            output_path=f"background_music/{filename}",
            quality="high"
        )

        # Report usage
        client.report_usage(track['id'], platform="youtube")

        print(f"Downloaded: {track['title']}")
```

### Example 2: Find Music by Mood and BPM Range

```python
from epidemic_sound_client import EpidemicSoundClient

def find_music_by_vibe(vibe, bpm_range, output_dir, count=5):
    """Find and download music matching a specific vibe."""

    # Map vibes to moods
    vibe_map = {
        "energetic": ["energetic", "powerful", "exciting"],
        "calm": ["relaxed", "peaceful", "dreamy"],
        "epic": ["epic", "dramatic", "triumphant"],
        "happy": ["happy", "uplifting", "playful"]
    }

    moods = vibe_map.get(vibe, [vibe])

    with EpidemicSoundClient() as client:
        client.authenticate()

        # Search
        results = client.search_tracks(
            mood=moods,
            bpm_min=bpm_range[0],
            bpm_max=bpm_range[1],
            limit=count
        )

        # Download
        track_ids = [track['id'] for track in results['tracks']]
        files = client.batch_download(track_ids, output_dir, quality="high")

        return files

# Use it
files = find_music_by_vibe(
    vibe="epic",
    bpm_range=(90, 120),
    output_dir="music/epic/",
    count=5
)
```

### Example 3: Build a Music Library by Genre

```python
from epidemic_sound_client import EpidemicSoundClient
import json

def build_genre_library(genres, tracks_per_genre=10):
    """Build a categorized music library."""

    library = {}

    with EpidemicSoundClient() as client:
        client.authenticate()

        for genre in genres:
            print(f"Fetching {genre} tracks...")

            results = client.search_tracks(
                genre=[genre],
                limit=tracks_per_genre
            )

            library[genre] = []

            for track in results['tracks']:
                library[genre].append({
                    'id': track['id'],
                    'title': track['title'],
                    'artists': track['mainArtists'],
                    'bpm': track['bpm'],
                    'duration': track['length'],
                    'moods': [m['name'] for m in track['moods']],
                    'has_vocals': track['hasVocals']
                })

        # Save library index
        with open('music_library.json', 'w') as f:
            json.dump(library, f, indent=2)

        return library

# Build library
library = build_genre_library(
    genres=['electronic', 'acoustic', 'cinematic', 'hip-hop'],
    tracks_per_genre=20
)
```

### Example 4: Smart Music Selection for Video Duration

```python
from epidemic_sound_client import EpidemicSoundClient

def find_music_for_video_duration(
    video_duration_seconds,
    mood,
    tolerance=10
):
    """Find music that closely matches video duration."""

    with EpidemicSoundClient() as client:
        client.authenticate()

        # Search with mood
        results = client.search_tracks(
            mood=mood,
            limit=100  # Get more options
        )

        # Filter by duration (within tolerance)
        suitable_tracks = [
            track for track in results['tracks']
            if abs(track['length'] - video_duration_seconds) <= tolerance
        ]

        # Sort by closest match
        suitable_tracks.sort(
            key=lambda t: abs(t['length'] - video_duration_seconds)
        )

        return suitable_tracks

# Find music for 3-minute video
tracks = find_music_for_video_duration(
    video_duration_seconds=180,
    mood=["inspiring", "uplifting"],
    tolerance=15  # ±15 seconds
)

print(f"Found {len(tracks)} tracks within duration range")
for track in tracks[:5]:
    print(f"{track['title']} - {track['length']}s")
```

### Example 5: Integration with Video Generation Pipeline

```python
from epidemic_sound_client import EpidemicSoundClient
import json

def get_background_music_for_video(
    video_topic,
    video_duration,
    output_path="background_music.mp3"
):
    """
    Intelligent music selection for video generation pipeline.
    """

    # Map topics to moods
    topic_moods = {
        "tutorial": ["focused", "calm"],
        "product_demo": ["uplifting", "inspiring"],
        "explainer": ["friendly", "approachable"],
        "promotional": ["energetic", "exciting"],
        "documentary": ["dramatic", "epic"]
    }

    moods = topic_moods.get(video_topic, ["neutral"])

    with EpidemicSoundClient() as client:
        client.authenticate()

        # Search for instrumental tracks
        results = client.search_tracks(
            mood=moods,
            limit=50
        )

        # Filter: no vocals, similar duration
        candidates = [
            track for track in results['tracks']
            if not track['hasVocals']
            and abs(track['length'] - video_duration) <= 20
        ]

        if not candidates:
            print("No perfect match found, using closest")
            candidates = [
                track for track in results['tracks']
                if not track['hasVocals']
            ]

        # Get best match
        best_track = min(
            candidates,
            key=lambda t: abs(t['length'] - video_duration)
        )

        # Download
        client.download_track(
            track_id=best_track['id'],
            output_path=output_path,
            quality="high"
        )

        # Report usage
        client.report_usage(best_track['id'], platform="youtube")

        # Return metadata
        return {
            'track_id': best_track['id'],
            'title': best_track['title'],
            'duration': best_track['length'],
            'bpm': best_track['bpm'],
            'file_path': output_path
        }

# Use in video pipeline
music_info = get_background_music_for_video(
    video_topic="product_demo",
    video_duration=180,
    output_path="output/background_music.mp3"
)

print(f"Selected: {music_info['title']}")
```

---

## Error Handling

### Exception Types

```python
from epidemic_sound_client import (
    EpidemicSoundError,      # Base exception
    AuthenticationError,      # Auth failures
    RateLimitError,          # Rate limit exceeded
    DownloadError,           # Download failures
    APIError                 # General API errors
)

try:
    client = EpidemicSoundClient()
    client.authenticate()
    results = client.search_tracks(query="epic")

except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Check credentials

except RateLimitError as e:
    print(f"Rate limit hit: {e}")
    print(f"Reset time: {e.reset_time}")
    # Wait or retry later

except DownloadError as e:
    print(f"Download failed: {e}")
    # Retry download

except APIError as e:
    print(f"API error ({e.status_code}): {e}")
    print(f"Response: {e.response_data}")

except EpidemicSoundError as e:
    print(f"Epidemic Sound error: {e}")
```

### Retry Logic

The client automatically retries:
- **502 errors**: Exponential backoff (DDoS protection)
- **5xx errors**: Exponential backoff (server issues)
- **Network errors**: Exponential backoff

Does NOT retry:
- **401/403**: Authentication errors (fix credentials)
- **400**: Bad request (fix parameters)
- **429**: Rate limit (handled separately)

---

## Configuration

### Custom Configuration

```python
from epidemic_sound_client import EpidemicSoundClient
import requests

# Custom session with connection pooling
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20
)
session.mount('https://', adapter)

# Initialize with custom settings
client = EpidemicSoundClient(
    access_key_id="your_key",
    access_key_secret="your_secret",
    user_id="hashed-user-id",
    cache_ttl=7200,  # 2 hours
    session=session
)
```

### Logging Configuration

```python
import logging

# Set log level
logging.getLogger('epidemic_sound_client').setLevel(logging.DEBUG)

# Custom handler
handler = logging.FileHandler('epidemic_sound.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

logger = logging.getLogger('epidemic_sound_client')
logger.addHandler(handler)
```

---

## Best Practices

### 1. Use Context Manager

```python
# Good: Automatically closes session
with EpidemicSoundClient() as client:
    client.authenticate()
    results = client.search_tracks(query="epic")

# Bad: Manual session management
client = EpidemicSoundClient()
try:
    results = client.search_tracks(query="epic")
finally:
    client.close()
```

### 2. Cache Wisely

```python
# Enable caching for repeated searches
results = client.search_tracks(query="epic", use_cache=True)

# Disable for real-time data
results = client.search_tracks(query="epic", use_cache=False)

# Clear cache periodically
client.cleanup_cache()
```

### 3. Handle Rate Limits

```python
import time

try:
    results = client.search_tracks(query="epic")
except RateLimitError as e:
    print(f"Rate limited. Waiting...")
    time.sleep(60)  # Wait before retry
```

### 4. Report Usage

```python
# Always report usage for downloaded tracks
track_id = results['tracks'][0]['id']
client.download_track(track_id, "music.mp3")
client.report_usage(track_id, platform="youtube")
```

### 5. Filter Intelligently

```python
# Combine filters for better results
results = client.search_tracks(
    query="workout motivation",
    mood=["energetic", "powerful"],
    bpm_min=130,
    bpm_max=150,
    limit=20
)

# Filter results further
no_vocals = [t for t in results['tracks'] if not t['hasVocals']]
free_tier = [t for t in results['tracks'] if t['tierOption'] == 'FREE']
```

---

## API Limits

### Rate Limits

- **Daily quota**: Varies by account (contact Epidemic Sound for details)
- **Headers**: `X-RateLimit-Reset`, `X-RateLimit-Reached`
- **Handling**: Automatic exponential backoff

### Pagination Limits

| Endpoint | Default | Maximum |
|----------|---------|---------|
| Search   | 50      | 60      |
| Tracks   | 50      | 100     |
| Collections | 10   | 20      |
| Moods/Genres | 20  | 20      |

### Download URL Expiration

- **Normal quality (128kbps)**: 24 hours
- **High quality (320kbps)**: 1 hour

---

## Troubleshooting

### Authentication Fails

```python
# Check credentials
print(os.getenv('EPIDEMIC_SOUND_ACCESS_KEY_ID'))
print(os.getenv('EPIDEMIC_SOUND_ACCESS_KEY_SECRET'))

# Force refresh
client.authenticate(force_refresh=True)
```

### No Results Found

```python
# Check filters
results = client.search_tracks(
    query="epic",
    mood=["dramatic"]
)

# Check aggregations
print(results.get('aggregations'))

# Browse available moods
moods = client.get_moods(type_filter="featured")
```

### Download Fails

```python
# Check track tier
track = results['tracks'][0]
if track['tierOption'] == 'PAID':
    print("Requires subscription")

# Check file path
output_path = Path("music/downloads/track.mp3")
output_path.parent.mkdir(parents=True, exist_ok=True)

# Retry download
try:
    client.download_track(track['id'], output_path, quality="high")
except DownloadError as e:
    print(f"Download failed: {e}")
    # Try normal quality
    client.download_track(track['id'], output_path, quality="normal")
```

---

## Advanced Topics

### Token Management

```python
# Check token status
if client._user_token:
    print(f"Token expires at: {client._user_token.expires_at}")
    print(f"Is expired: {client._user_token.is_expired()}")

# Manual refresh
client.authenticate(force_refresh=True)
```

### Custom User IDs

```python
import hashlib

def anonymize_user_id(user_email):
    """Create GDPR-compliant anonymized user ID."""
    return hashlib.sha256(user_email.encode()).hexdigest()

user_id = anonymize_user_id("user@example.com")
client = EpidemicSoundClient(user_id=user_id)
```

### Batch Operations with Progress

```python
from tqdm import tqdm

def batch_download_with_progress(client, track_ids, output_dir):
    """Download with progress bar."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    downloaded = []

    for track_id in tqdm(track_ids, desc="Downloading"):
        try:
            output_path = output_dir / f"{track_id}.mp3"
            client.download_track(track_id, output_path, quality="high")
            downloaded.append(output_path)
        except Exception as e:
            print(f"Failed: {track_id} - {e}")

    return downloaded
```

---

## Resources

- **API Documentation**: https://developers.epidemicsite.com/docs/
- **Complete Reference**: D:\workspace\VideoGen_YouTube\EPIDEMIC_SOUND_API_COMPLETE_REFERENCE.md
- **Support**: Contact via developer portal

---

## License

This client is for use with the Epidemic Sound Partner Content API. Review the Epidemic Sound Terms of Service and Acceptable Use Policy before use.

**Important Notes:**
- Do NOT cache metadata (violates Acceptable Use Policy)
- DO report usage for all downloaded tracks
- Use anonymized, GDPR-compliant user identifiers
- Respect rate limits
