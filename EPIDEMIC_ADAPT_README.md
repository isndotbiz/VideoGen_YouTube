# Epidemic Sound Adapt Tool - Browser Automation

Complete Playwright-based automation for Epidemic Sound's Adapt Labs tool to customize and download background music tracks.

## Features

- **Automated Login** - Session persistence with 7-day validity
- **Track Selection** - By URL or search query
- **Length Adaptation** - AI-powered duration adjustment (automatic or manual selection)
- **Music Adaptation** - Customize musical characteristics with text descriptions
- **Smart Processing** - Waits for AI processing with progress tracking
- **Download Management** - WAV or MP3 format with automatic filename generation
- **Retry Logic** - Automatic retries with exponential backoff
- **Error Recovery** - Comprehensive error handling and logging
- **Session Reuse** - Saves and reuses browser sessions to avoid repeated logins

## File Structure

```
epidemic_browser_adapt.py       # Main automation module (Playwright-based)
epidemic_adapt_example.py       # Usage examples and demonstrations
epidemic_browser_login.py       # Async session manager (existing)
EPIDEMIC_ADAPT_README.md        # This file
```

## Installation

### 1. Install Dependencies

```bash
# Install Python packages
pip install playwright python-dotenv

# Install Playwright browsers
playwright install chromium
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
EPIDEMIC_SOUND_EMAIL=your_email@example.com
EPIDEMIC_SOUND_PASSWORD=your_password
```

Or set environment variables directly:

```bash
# Windows
set EPIDEMIC_SOUND_EMAIL=your_email@example.com
set EPIDEMIC_SOUND_PASSWORD=your_password

# Linux/Mac
export EPIDEMIC_SOUND_EMAIL=your_email@example.com
export EPIDEMIC_SOUND_PASSWORD=your_password
```

## Usage

### Command Line Interface

#### Basic Usage - Adapt by Track URL

```bash
python epidemic_browser_adapt.py --track-url "https://www.epidemicsound.com/track/XYZ123" --duration 300
```

#### Search and Adapt

```bash
python epidemic_browser_adapt.py --search "upbeat energetic" --duration 180
```

#### Adapt with Music Changes

```bash
python epidemic_browser_adapt.py \
    --track-url "https://..." \
    --duration 300 \
    --description "Minimal, calm background for voiceover"
```

#### Custom Format and Output

```bash
python epidemic_browser_adapt.py \
    --search "corporate background" \
    --duration 240 \
    --format mp3 \
    --output-dir ./music_library
```

#### Headless Mode

```bash
python epidemic_browser_adapt.py \
    --search "ambient calm" \
    --duration 120 \
    --headless
```

### Python API

#### Example 1: Basic Track Adaptation

```python
from epidemic_browser_adapt import EpidemicSoundBrowser, AdaptConfig

# Configure adaptation
config = AdaptConfig(
    duration=300,  # 5 minutes
    auto_select=True,
    download_format='wav',
    output_dir='background_music_epidemic'
)

# Run adaptation
with EpidemicSoundBrowser(headless=False) as browser:
    result = browser.adapt_track_complete(
        track_url="https://www.epidemicsound.com/track/XYZ123",
        config=config
    )

    if result['success']:
        print(f"Downloaded: {result['download_path']}")
    else:
        print(f"Failed: {result['error']}")
```

#### Example 2: Search and Adapt

```python
from epidemic_browser_adapt import EpidemicSoundBrowser, AdaptConfig

config = AdaptConfig(
    duration=180,
    description="Minimal background-friendly for voiceover",
    download_format='wav'
)

with EpidemicSoundBrowser() as browser:
    result = browser.adapt_track_complete(
        search_query="calm ambient background",
        config=config
    )
```

#### Example 3: Manual Step-by-Step Control

```python
from epidemic_browser_adapt import EpidemicSoundBrowser
from pathlib import Path

browser = EpidemicSoundBrowser(headless=False, slow_mo=500)
browser.start_browser()

try:
    # Login
    browser.login()

    # Navigate to Adapt
    browser.navigate_to_adapt()

    # Search and select track
    browser.search_and_select_track("upbeat", index=0)

    # Adapt length
    browser.adapt_length(duration=60, auto_select=True)

    # Optional: Adapt music
    browser.adapt_music(
        description="Minimal, calm background",
        stems="all"
    )

    # Download
    output_path = browser.download_adapted_track(
        output_dir=Path("music"),
        format="wav"
    )

    print(f"Success: {output_path}")

finally:
    browser.close_browser()
```

#### Example 4: Batch Processing

```python
from epidemic_browser_adapt import EpidemicSoundBrowser, AdaptConfig

tracks_to_process = [
    {'search': 'upbeat energetic', 'duration': 30},
    {'search': 'calm ambient', 'duration': 60},
    {'search': 'corporate motivational', 'duration': 45}
]

with EpidemicSoundBrowser() as browser:
    for i, track_info in enumerate(tracks_to_process, 1):
        config = AdaptConfig(
            duration=track_info['duration'],
            output_dir=f"music/batch_{i}"
        )

        result = browser.adapt_track_complete(
            search_query=track_info['search'],
            config=config
        )

        if result['success']:
            print(f"✓ Track {i}: {result['download_path']}")
        else:
            print(f"✗ Track {i}: {result['error']}")
```

## Configuration Options

### AdaptConfig Parameters

```python
AdaptConfig(
    duration: int = 300,              # Target duration in seconds
    start_time: Optional[int] = None, # Start time for manual selection
    auto_select: bool = True,         # Use automatic section selection
    description: Optional[str] = None,# Description for music adaptation
    stems: str = "all",               # Which stems to adapt
    mood: Optional[str] = None,       # Target mood
    download_format: str = "wav",     # "wav" or "mp3"
    output_dir: str = "..."           # Output directory
)
```

### Browser Options

```python
EpidemicSoundBrowser(
    email: Optional[str] = None,      # Override env variable
    password: Optional[str] = None,   # Override env variable
    headless: bool = False,           # Run without visible browser
    slow_mo: int = 0                  # Slow down by N milliseconds
)
```

## CLI Arguments

```
Track Selection:
  --track-url URL        URL to specific track
  --search QUERY         Search query for tracks

Adapt Settings:
  --duration SECONDS     Target duration (default: 300)
  --start-time SECONDS   Start time for manual selection
  --auto                 Use automatic selection (default)
  --manual               Use manual section selection

Music Adaptation:
  --description TEXT     Description for music adaptation
  --stems {all,melody,bass}  Stems to adapt
  --mood MOOD           Target mood

Download Settings:
  --format {wav,mp3}    Download format (default: wav)
  --output-dir DIR      Output directory

Browser Settings:
  --headless            Run browser in headless mode
  --slow MS             Slow down operations by N milliseconds
```

## How It Works

### 1. Authentication Flow

- Attempts to load saved session from `epidemic_session.json`
- Validates session by checking user menu indicators
- Performs fresh login if needed with credential entry
- Saves session state for reuse (7-day validity)

### 2. Track Selection

**By URL:**
- Navigates directly to track page
- Looks for "Adapt" button and clicks it
- Falls back to URL input if available

**By Search:**
- Uses search input in Adapt tool
- Waits for results to load
- Selects track by index (default: first result)

### 3. Length Adaptation

- Opens "Adapt length" panel
- Sets target duration in seconds
- Chooses automatic or manual section selection
- Clicks process button
- Waits for AI processing with progress monitoring (up to 2 minutes)

### 4. Music Adaptation (Optional)

- Opens "Adapt music" panel
- Enters text description of desired changes
- Selects stems to modify
- Processes with AI (can take 30-90 seconds)

### 5. Download

- Locates download button in History panel
- Selects format (WAV or MP3)
- Captures download event
- Saves with timestamped filename
- Verifies file size and returns path

## Wait Handling

The automation uses intelligent wait strategies:

- **Element Waits**: Waits for elements to be visible and clickable
- **Processing Waits**: Monitors for processing indicators (spinners, progress bars)
- **Completion Detection**: Looks for "Complete", "Done", or "Download" buttons
- **Progress Logging**: Updates every 10 seconds during processing
- **Timeout Protection**: 2-minute maximum for processing operations

## Error Recovery

### Retry Logic

- Adaptation operations retry up to 2 times on failure
- Uses exponential backoff between retries
- Continues if non-critical steps fail (e.g., preview)

### Error Types

- **LoginError**: Authentication issues
- **AdaptError**: Processing or AI failures
- **DownloadError**: File download problems
- **EpidemicBrowserError**: General browser issues

### Recovery Strategies

```python
try:
    with EpidemicSoundBrowser() as browser:
        result = browser.adapt_track_complete(...)
except LoginError as e:
    print(f"Check credentials: {e}")
except AdaptError as e:
    print(f"Retry with different settings: {e}")
except DownloadError as e:
    print(f"Check permissions and space: {e}")
```

## Troubleshooting

### Login Issues

**Problem**: "Login failed - incorrect credentials"
- Verify `.env` file has correct email/password
- Try running with `--headless` flag disabled to see errors
- Check for 2FA requirements (not fully supported)

**Problem**: "Session validation failed"
- Delete `epidemic_session.json` and try again
- Run with `--headless False` for first login

### Adaptation Issues

**Problem**: "Adapt length button not found"
- Epidemic Sound UI may have changed
- Check selectors in source code
- Try navigating manually first

**Problem**: "Processing timeout"
- AI processing can take time (up to 2 minutes)
- Try again - might be temporary server load
- Check internet connection

### Download Issues

**Problem**: "Download button not found"
- Wait for processing to complete
- Check if download appears in History panel
- Try refreshing page and locating result

**Problem**: "Download timeout"
- Large files take time
- Check network speed
- Increase timeout in code

## Best Practices

### 1. First Run

```bash
# Run non-headless first time to verify login
python epidemic_browser_adapt.py --search "test" --duration 30
```

### 2. Session Management

- Sessions last 7 days
- Delete `epidemic_session.json` to force fresh login
- Keep credentials in `.env` file (not in code)

### 3. Rate Limiting

- Add delays between batch operations
- Don't run too many requests in parallel
- Use reasonable durations (avoid extremes)

### 4. Output Organization

```python
config = AdaptConfig(
    output_dir=f"music/{topic}/{datetime.now().strftime('%Y%m%d')}"
)
```

### 5. Error Logging

- Check `epidemic_*.log` files for debugging
- Save screenshots on critical failures
- Enable debug logging for development

## Examples

Run the examples script:

```bash
python epidemic_adapt_example.py
```

This provides interactive examples:
1. Basic track adaptation by URL
2. Search and adapt first result
3. Adapt length + music characteristics
4. Manual control (step-by-step)
5. Batch process multiple tracks
6. Error handling demonstration

## Comparison with API Client

### Browser Automation (`epidemic_browser_adapt.py`)

**Pros:**
- Access to Adapt tool (not in API)
- AI-powered customization
- Visual verification
- No API key needed

**Cons:**
- Slower than API
- Requires browser
- Less stable (UI changes)

### API Client (`epidemic_sound_client.py`)

**Pros:**
- Fast and reliable
- No browser required
- Better for production
- Programmatic access

**Cons:**
- No Adapt functionality
- Requires API keys
- Limited customization

### When to Use Each

**Use Browser Automation for:**
- Track length customization
- AI music adaptation
- Testing and exploration
- One-off customizations

**Use API Client for:**
- High-volume downloads
- Production pipelines
- Simple track retrieval
- Automated workflows

## Integration Example

Combine both approaches:

```python
from epidemic_sound_client import EpidemicSoundClient
from epidemic_browser_adapt import EpidemicSoundBrowser, AdaptConfig

# Step 1: Search with API (faster)
client = EpidemicSoundClient()
client.authenticate()
results = client.search_tracks(query="upbeat", mood=["energetic"], limit=5)

# Step 2: Adapt selected track with browser automation
track_url = f"https://www.epidemicsound.com/track/{results['tracks'][0]['id']}"

config = AdaptConfig(duration=180)
with EpidemicSoundBrowser() as browser:
    result = browser.adapt_track_complete(track_url=track_url, config=config)
```

## Performance Tips

### 1. Use Saved Sessions

```python
# Session persists across runs
browser = EpidemicSoundBrowser()
browser.start_browser()
browser.login()  # Fast if session exists

# Do multiple operations...
browser.close_browser()
```

### 2. Batch Operations

Process multiple tracks in one session to save login time.

### 3. Headless Mode

```python
# Faster and uses less resources
browser = EpidemicSoundBrowser(headless=True)
```

### 4. Parallel Processing

```python
# Use multiple browser instances (careful with rate limits)
from multiprocessing import Pool

def process_track(track_config):
    with EpidemicSoundBrowser(headless=True) as browser:
        return browser.adapt_track_complete(**track_config)

with Pool(3) as pool:
    results = pool.map(process_track, track_configs)
```

## Known Limitations

1. **Manual Selection**: Waveform manipulation for manual section selection is not fully implemented
2. **2FA**: Two-factor authentication requires manual intervention (non-headless mode)
3. **UI Changes**: Epidemic Sound UI changes may break selectors
4. **Processing Time**: AI adaptation can take 30-90 seconds
5. **Rate Limits**: Excessive requests may trigger rate limiting

## Future Enhancements

- [ ] Full manual section selection with waveform interaction
- [ ] 2FA automation (if possible)
- [ ] History panel management
- [ ] Multiple format downloads
- [ ] Stem-specific downloads
- [ ] Advanced retry strategies
- [ ] Webhook notifications
- [ ] Progress bars for CLI
- [ ] Integration with video editing tools

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review log files (`epidemic_*.log`)
3. Run examples with `--slow 1000` to debug
4. Take screenshots on failures

## License

Part of the VideoGen YouTube Project.

---

**Last Updated**: December 2025
**Python Version**: 3.8+
**Playwright Version**: 1.40+
