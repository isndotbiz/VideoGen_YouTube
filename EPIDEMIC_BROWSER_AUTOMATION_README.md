# Epidemic Sound Browser Automation

Comprehensive Playwright-based automation for searching and filtering music on Epidemic Sound's web interface.

## Overview

`epidemic_browser_search.py` is a production-ready browser automation script that provides:

- **Authentication**: Email/password login to Epidemic Sound
- **Advanced Search**: Keyword-based and AI-powered music discovery
- **Intelligent Filtering**: Genre, Mood, BPM, Vocals, Energy, Duration
- **Track Extraction**: Automated data scraping with metadata
- **Pagination**: Infinite scroll and "Load More" handling
- **Track Preview**: Click-to-preview functionality
- **JSON Export**: Save results for downstream processing

## Installation

### 1. Install Playwright

```bash
pip install playwright pandas
```

### 2. Install Browser Binaries

```bash
playwright install chromium
```

### 3. Set Environment Variables

Create a `.env` file or set system environment variables:

```bash
# Windows (PowerShell)
$env:EPIDEMIC_SOUND_EMAIL="your.email@example.com"
$env:EPIDEMIC_SOUND_PASSWORD="your_password"

# Linux/Mac
export EPIDEMIC_SOUND_EMAIL="your.email@example.com"
export EPIDEMIC_SOUND_PASSWORD="your_password"
```

## Usage

### Basic Search

Search for tracks with keyword query:

```bash
python epidemic_browser_search.py --query "chillstep" --limit 20
```

### BPM Filtering

Find tracks within specific BPM range:

```bash
python epidemic_browser_search.py --query "chillstep" --bpm-min 110 --bpm-max 130
```

### Advanced Filtering

Combine multiple filters:

```bash
python epidemic_browser_search.py \
  --query "electronic" \
  --genre "House" \
  --mood "Energetic" \
  --vocals instrumental \
  --bpm-min 120 \
  --bpm-max 140 \
  --duration-min 120 \
  --duration-max 240 \
  --limit 50
```

### AI-Powered Search

Use AI to describe the music you want:

```bash
python epidemic_browser_search.py \
  --ai-prompt "upbeat background music for tech tutorial video" \
  --limit 30
```

### Save Results to File

Export search results as JSON:

```bash
python epidemic_browser_search.py \
  --query "ambient" \
  --mood "Calm" \
  --output results/ambient_tracks.json
```

### Visual Mode (Non-Headless)

Run with visible browser for debugging:

```bash
python epidemic_browser_search.py \
  --query "cinematic" \
  --no-headless
```

### Preview Track

Automatically preview the first track result:

```bash
python epidemic_browser_search.py \
  --query "epic" \
  --preview
```

## Command-Line Arguments

### Search Parameters

| Argument | Type | Description |
|----------|------|-------------|
| `--query`, `-q` | string | Search query (keyword-based) |
| `--ai-prompt` | string | AI-powered search prompt |

### Filters

| Argument | Type | Description |
|----------|------|-------------|
| `--genre` | string | Genre filter (e.g., Electronic, Rock, Pop) |
| `--mood` | string | Mood filter (e.g., Energetic, Calm, Epic) |
| `--vocals` | choice | Vocals filter: `instrumental`, `with_vocals`, `both` |
| `--bpm-min` | integer | Minimum BPM (e.g., 60, 110, 120) |
| `--bpm-max` | integer | Maximum BPM (e.g., 140, 160, 180) |
| `--energy` | string | Energy level filter |
| `--duration-min` | integer | Minimum duration in seconds |
| `--duration-max` | integer | Maximum duration in seconds |

### Results

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--limit`, `-l` | integer | 50 | Maximum number of tracks to return |
| `--output`, `-o` | string | - | Output JSON file path |

### Browser Options

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--headless` | flag | True | Run browser in headless mode |
| `--no-headless` | flag | - | Run browser with visible UI |
| `--timeout` | integer | 30 | Timeout in seconds |
| `--skip-login` | flag | - | Skip authentication step |
| `--preview` | flag | - | Preview first track result |

## Output Format

The script returns a JSON object with the following structure:

```json
{
  "tracks": [
    {
      "id": "track123",
      "title": "Track Name",
      "artist": "Artist Name",
      "bpm": 125,
      "duration": 180,
      "url": "https://www.epidemicsound.com/track/...",
      "genres": ["Electronic", "Techno"],
      "moods": ["Energetic"],
      "vocals": "Instrumental",
      "energy_level": "High"
    }
  ],
  "total": 1,
  "filters": {
    "query": "chillstep",
    "bpm_min": 110,
    "bpm_max": 130
  },
  "timestamp": "2025-12-23T10:30:00"
}
```

## Programmatic Usage

You can also use the `EpidemicSoundBrowser` class in your Python code:

```python
import asyncio
from epidemic_browser_search import EpidemicSoundBrowser, SearchFilters

async def search_music():
    # Create filters
    filters = SearchFilters(
        query="chillstep",
        bpm_min=110,
        bpm_max=130,
        vocals="instrumental",
        limit=20
    )

    # Initialize browser
    async with EpidemicSoundBrowser(headless=True) as browser:
        # Login
        await browser.login()

        # Search
        tracks = await browser.search_tracks(filters)

        # Process results
        for track in tracks:
            print(f"{track.title} - {track.artist} ({track.bpm} BPM)")

        return tracks

# Run
results = asyncio.run(search_music())
```

## Features

### 1. Authentication

The browser automation handles login to Epidemic Sound:

```python
await browser.login(email="your@email.com", password="password")
```

Credentials can also be loaded from environment variables.

### 2. Standard Search

Keyword-based search with advanced filters:

```python
filters = SearchFilters(
    query="electronic",
    genre="House",
    mood="Energetic",
    bpm_min=120,
    bpm_max=140
)

tracks = await browser.search_tracks(filters)
```

### 3. AI Music Discovery

AI-powered search that understands natural language:

```python
filters = SearchFilters(
    ai_prompt="upbeat background music for tech tutorial"
)

tracks = await browser.search_tracks(filters)
```

### 4. Robust Selectors

The automation uses multiple selector strategies:

- `data-*` attributes (preferred)
- CSS classes
- Element text content
- XPath selectors (fallback)

This ensures compatibility even if the UI changes.

### 5. Pagination Handling

Automatically handles:

- "Load More" buttons
- Infinite scroll
- Multi-page results

```python
# Extracts up to 100 tracks across multiple pages
tracks = await browser._extract_tracks(limit=100)
```

### 6. Track Preview

Click on tracks to preview:

```python
await browser.preview_track(track_id="abc123")
```

### 7. Error Recovery

Graceful handling of:

- Network timeouts
- Missing elements
- Login failures
- Rate limiting

## Architecture

### Class: `EpidemicSoundBrowser`

Main automation class with methods:

**Browser Lifecycle**
- `start()` - Initialize browser and context
- `close()` - Cleanup resources
- `__aenter__()` / `__aexit__()` - Context manager support

**Authentication**
- `login(email, password)` - Authenticate user
- `is_logged_in()` - Check authentication status

**Search & Filtering**
- `search_tracks(filters)` - Main search method
- `_standard_search(filters)` - Keyword search
- `_ai_search(prompt, filters)` - AI-powered search
- `_apply_filters(filters)` - Apply all filters
- `_apply_filter(name, value)` - Apply single filter
- `_apply_bpm_filter(min, max)` - BPM range filter
- `_apply_duration_filter(min, max)` - Duration filter

**Track Extraction**
- `_extract_tracks(limit)` - Extract track data
- `_extract_track_data(element)` - Parse single track
- `_extract_metadata(element)` - Extract BPM, duration, etc.
- `_load_more_results()` - Handle pagination

**Track Actions**
- `preview_track(track_id)` - Preview track

### Data Classes

**`TrackData`**
```python
@dataclass
class TrackData:
    id: str
    title: str
    artist: str
    bpm: Optional[int]
    duration: Optional[int]
    url: Optional[str]
    genres: Optional[List[str]]
    moods: Optional[List[str]]
    vocals: Optional[str]
    energy_level: Optional[str]
```

**`SearchFilters`**
```python
@dataclass
class SearchFilters:
    query: Optional[str]
    ai_prompt: Optional[str]
    genre: Optional[str]
    mood: Optional[str]
    vocals: Optional[str]
    bpm_min: Optional[int]
    bpm_max: Optional[int]
    energy_level: Optional[str]
    duration_min: Optional[int]
    duration_max: Optional[int]
    limit: int = 50
```

## Troubleshooting

### Playwright Not Installed

```bash
pip install playwright
playwright install chromium
```

### Login Fails

1. Verify credentials in environment variables
2. Run in non-headless mode to debug: `--no-headless`
3. Check if CAPTCHA is present (may require manual intervention)

### No Tracks Found

1. Verify search query is valid
2. Loosen filter constraints
3. Check if page structure has changed (selectors may need updating)

### Timeout Errors

Increase timeout:

```bash
python epidemic_browser_search.py --query "ambient" --timeout 60
```

### Element Not Found

The script uses multiple fallback selectors. If elements still aren't found:

1. Run with `--no-headless` to inspect page
2. Check browser console for JavaScript errors
3. Update selectors in code if UI has changed

## Integration with Video Generation

This automation integrates seamlessly with the VideoGen YouTube project:

```python
# 1. Search for background music
filters = SearchFilters(
    query="corporate background",
    vocals="instrumental",
    duration_min=180,
    duration_max=240,
    limit=10
)

tracks = await browser.search_tracks(filters)

# 2. Select best match
best_track = tracks[0]

# 3. Download using Epidemic Sound API
from epidemic_sound_client import EpidemicSoundClient

client = EpidemicSoundClient()
client.authenticate()
client.download_track(
    track_id=best_track.id,
    output_path=f"background_music/{best_track.title}.mp3",
    quality="high"
)

# 4. Use in video composition
# ... integrate with video pipeline
```

## Comparison: API vs Browser Automation

### Epidemic Sound API (`epidemic_sound_client.py`)

**Pros:**
- Fast and reliable
- Official API with rate limits
- Direct metadata access
- Download support

**Cons:**
- Requires API credentials
- Limited to API-supported features
- No AI search (API limitation)

### Browser Automation (`epidemic_browser_search.py`)

**Pros:**
- Access to full web UI features
- AI-powered search (if available on website)
- Visual preview capability
- No API credentials needed (just login)

**Cons:**
- Slower than API
- Brittle (UI changes can break it)
- No direct download (must use API after finding tracks)

### Best Practice

**Use both together:**

1. **Browser automation** for discovery and filtering
2. **API client** for downloading tracks

```python
# Discover with browser
tracks = await browser.search_tracks(filters)

# Download with API
client = EpidemicSoundClient()
for track in tracks[:5]:
    client.download_track(track.id, f"music/{track.id}.mp3")
```

## Security Notes

- Store credentials in environment variables, not in code
- Use `.env` files (excluded from version control)
- Avoid committing sensitive data

```bash
# .gitignore
.env
*.env
credentials.json
```

## License

Part of the VideoGen YouTube project.

## Support

For issues or questions, refer to the main project documentation.

---

**File:** `D:\workspace\VideoGen_YouTube\epidemic_browser_search.py`
**Created:** December 2025
**Author:** VideoGen YouTube Project
