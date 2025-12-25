# Epidemic Sound Adapt Tool - Quick Start

Get started in 5 minutes.

## Setup (First Time Only)

### 1. Install Dependencies

```bash
pip install playwright python-dotenv
playwright install chromium
```

Or use the setup script:

```bash
python setup_epidemic_adapt.py
```

### 2. Configure Credentials

Create `.env` file in project root:

```env
EPIDEMIC_SOUND_EMAIL=your_email@example.com
EPIDEMIC_SOUND_PASSWORD=your_password
```

## Usage

### Command Line (Easiest)

```bash
# Adapt track by URL to 5 minutes (300 seconds)
python epidemic_browser_adapt.py \
    --track-url "https://www.epidemicsound.com/track/XYZ123" \
    --duration 300

# Search and adapt first result to 3 minutes
python epidemic_browser_adapt.py \
    --search "calm ambient background" \
    --duration 180

# With music customization
python epidemic_browser_adapt.py \
    --search "upbeat energetic" \
    --duration 240 \
    --description "Minimal, background-friendly for voiceover"

# Output as MP3 to custom directory
python epidemic_browser_adapt.py \
    --search "corporate" \
    --duration 120 \
    --format mp3 \
    --output-dir ./my_music
```

### Python Code

```python
from epidemic_browser_adapt import EpidemicSoundBrowser, AdaptConfig

# Configure adaptation
config = AdaptConfig(
    duration=300,                 # 5 minutes
    auto_select=True,             # Automatic section selection
    download_format='wav',        # WAV or MP3
    output_dir='background_music' # Output directory
)

# Run adaptation
with EpidemicSoundBrowser(headless=False) as browser:
    result = browser.adapt_track_complete(
        search_query="calm ambient",
        config=config
    )

    if result['success']:
        print(f"✅ Downloaded: {result['download_path']}")
    else:
        print(f"❌ Failed: {result['error']}")
```

## Common Options

### Track Selection

```bash
--track-url "URL"    # Use specific track URL
--search "query"     # Search and use first result
```

### Duration Settings

```bash
--duration 30       # 30 seconds
--duration 60       # 1 minute
--duration 180      # 3 minutes
--duration 300      # 5 minutes (default)
```

### Music Customization (Optional)

```bash
--description "Minimal background for voiceover"
--stems all         # Which stems to adapt
--mood calm         # Target mood
```

### Download Options

```bash
--format wav        # WAV format (default, higher quality)
--format mp3        # MP3 format (smaller size)
--output-dir PATH   # Custom output directory
```

### Browser Options

```bash
--headless          # Run without visible browser (faster)
--slow 500          # Slow down by 500ms (for debugging)
```

## Examples

### Example 1: Quick Adapt

```bash
python epidemic_browser_adapt.py --search "background" --duration 60
```

### Example 2: High Quality for Video

```bash
python epidemic_browser_adapt.py \
    --search "cinematic epic" \
    --duration 180 \
    --format wav \
    --output-dir ./video_music
```

### Example 3: Voiceover Friendly

```bash
python epidemic_browser_adapt.py \
    --search "minimal ambient" \
    --duration 240 \
    --description "Very quiet, background only" \
    --format wav
```

### Example 4: Batch Processing

```python
from epidemic_browser_adapt import EpidemicSoundBrowser, AdaptConfig

tracks = [
    {"query": "upbeat", "duration": 30},
    {"query": "calm", "duration": 60},
    {"query": "corporate", "duration": 45}
]

with EpidemicSoundBrowser() as browser:
    for track in tracks:
        config = AdaptConfig(duration=track['duration'])
        result = browser.adapt_track_complete(
            search_query=track['query'],
            config=config
        )
        print(f"Track: {result['download_path']}")
```

## Troubleshooting

### Issue: "Module not found"
```bash
pip install playwright python-dotenv
playwright install chromium
```

### Issue: "Login failed"
- Check `.env` file has correct credentials
- Try with `--headless` flag disabled to see browser

### Issue: "Processing timeout"
- AI processing can take 30-90 seconds
- Try again (might be temporary)
- Check internet connection

### Issue: "Download failed"
- Check disk space
- Verify output directory permissions
- Try different format (mp3 vs wav)

## Next Steps

1. **Read Full Documentation**: See `EPIDEMIC_ADAPT_README.md`
2. **Run Examples**: Try `python epidemic_adapt_example.py`
3. **Integrate with Pipeline**: Use in your video generation workflow

## Tips

- First run without `--headless` to verify login
- Sessions persist for 7 days (automatic reuse)
- Use WAV for high quality, MP3 for smaller files
- AI processing takes 30-90 seconds per track
- Add delays between batch operations

## File Locations

- **Downloaded tracks**: `background_music_epidemic/` (or custom `--output-dir`)
- **Session file**: `epidemic_session.json` (reused for 7 days)
- **Logs**: Check console output for real-time progress

## Support

Run setup to verify installation:
```bash
python setup_epidemic_adapt.py
```

Check full documentation:
```bash
cat EPIDEMIC_ADAPT_README.md
```

---

That's it! You're ready to automate track adaptation with Epidemic Sound.
