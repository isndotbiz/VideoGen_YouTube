# Epidemic Sound Auto Downloader

Production-ready browser automation system for downloading music from Epidemic Sound for all video platforms.

## Features

- **Multi-Platform Support**: YouTube, TikTok, Instagram, Twitter
- **Smart Filtering**: Automatic BPM, mood, and duration filtering per platform
- **Resume Capability**: Checkpoint system to resume interrupted downloads
- **Error Recovery**: Automatic retry with 3 attempts per track
- **Progress Tracking**: Real-time progress with ETA calculation
- **Auto Organization**: Files automatically organized by platform/category
- **Metadata Generation**: JSON metadata for every track + master index

## Quick Start

### 1. Install Dependencies

```bash
pip install playwright
playwright install chromium
```

### 2. Set Environment Variables

Create a `.env` file or set environment variables:

```bash
export EPIDEMIC_EMAIL="your_email@example.com"
export EPIDEMIC_PASSWORD="your_password"
```

**Windows:**
```cmd
set EPIDEMIC_EMAIL=your_email@example.com
set EPIDEMIC_PASSWORD=your_password
```

### 3. First Run (Interactive Login)

```bash
# Test login first (NOT headless - you need to see the browser)
python epidemic_browser_login.py --test

# Once login works, start downloading
python epidemic_auto_downloader.py --quick
```

### 4. Production Run

```bash
# Download everything (35 tracks, ~2-3 hours)
python epidemic_auto_downloader.py

# Download for specific platforms only
python epidemic_auto_downloader.py --platforms youtube,tiktok

# Resume interrupted download
python epidemic_auto_downloader.py --resume

# Run in background (headless mode)
python epidemic_auto_downloader.py --headless
```

## Platform Configurations

The system automatically downloads music optimized for each platform:

### YouTube
- **Calm** (5 tracks): 60-80 BPM, calm mood, 5 minutes, ambient
- **Energetic** (5 tracks): 120-140 BPM, energetic mood, 5 minutes, electronic

### TikTok
- **High Energy** (5 tracks): 140-160 BPM, energetic mood, 45 seconds, dance

### Instagram
- **Fitness** (3 tracks): 130-150 BPM, energetic mood, 60 seconds, workout
- **Beauty** (3 tracks): 90-120 BPM, elegant mood, 60 seconds, pop
- **Travel** (3 tracks): 80-110 BPM, cinematic mood, 60 seconds, cinematic

### Twitter
- **Professional** (5 tracks): 100-130 BPM, corporate mood, 90 seconds, corporate

**Total: 35 tracks across 7 categories**

## Directory Structure

```
epidemic_music_library/
├── youtube/
│   ├── calm/
│   │   ├── youtube_calm_60-80bpm_300s_1.wav
│   │   ├── youtube_calm_60-80bpm_300s_2.wav
│   │   └── ...
│   └── energetic/
│       └── ...
├── tiktok/
│   └── high_energy/
│       └── ...
├── instagram/
│   ├── fitness/
│   ├── beauty/
│   └── travel/
├── twitter/
│   └── professional/
├── metadata/
│   ├── youtube_calm_0.json
│   ├── youtube_calm_1.json
│   └── ...
└── library_index.json
```

## Command Reference

### epidemic_browser_login.py

Test and manage login sessions:

```bash
# Test login (first time)
python epidemic_browser_login.py --test

# Force refresh session
python epidemic_browser_login.py --refresh

# Clear saved session
python epidemic_browser_login.py --clear

# Run headless (not recommended for first login)
python epidemic_browser_login.py --test --headless
```

### epidemic_auto_downloader.py

Main orchestration script:

```bash
# Quick mode: 2 tracks per category (14 total, ~30 min)
python epidemic_auto_downloader.py --quick

# Full download: all configured tracks
python epidemic_auto_downloader.py

# Specific platforms only
python epidemic_auto_downloader.py --platforms youtube
python epidemic_auto_downloader.py --platforms youtube,instagram

# Resume from checkpoint
python epidemic_auto_downloader.py --resume

# Background mode (headless)
python epidemic_auto_downloader.py --headless

# Quick test on specific platform
python epidemic_auto_downloader.py --platforms tiktok --quick
```

## How It Works

### 1. Login Phase
- Uses Playwright to launch Chrome
- Logs into Epidemic Sound
- Saves session cookies to `epidemic_session.json`
- Session valid for 7 days

### 2. Download Phase
For each platform category:
1. Navigate to music search
2. Apply filters (BPM, mood, duration)
3. Get search results
4. For each track:
   - Open track page
   - Click "Adapt" tool
   - Configure duration and version
   - Click download
   - Wait for download completion
   - Move to organized folder
   - Rename with metadata
   - Save JSON metadata
5. Save checkpoint

### 3. Error Recovery
- Each download has 3 retry attempts
- Screenshots saved on errors: `error_<platform>_<category>_<index>.png`
- Checkpoint saved after every successful download
- Can resume from any point

### 4. Progress Tracking
Real-time display shows:
- Completed/Total tasks with percentage
- Current platform > category > track
- Elapsed time
- Estimated time remaining (ETA)
- Failed download count

## Checkpoint System

The system saves progress to `epidemic_download_checkpoint.json` after each download:

```json
{
  "timestamp": "2025-12-23T10:30:00",
  "tasks": [
    {
      "platform": "youtube",
      "category": "calm",
      "track_index": 0,
      "status": "completed",
      "download_path": "epidemic_music_library/youtube/calm/youtube_calm_60-80bpm_300s_1.wav",
      "track_title": "Peaceful Morning",
      "track_artist": "Relaxing Artist"
    }
  ]
}
```

To resume:
```bash
python epidemic_auto_downloader.py --resume
```

## Metadata Files

Each downloaded track gets a metadata JSON file:

```json
{
  "platform": "youtube",
  "category": "calm",
  "track_index": 0,
  "title": "Peaceful Morning",
  "artist": "Relaxing Artist",
  "url": "https://www.epidemicsound.com/track/...",
  "download_path": "epidemic_music_library/youtube/calm/youtube_calm_60-80bpm_300s_1.wav",
  "config": {
    "bpm_min": 60,
    "bpm_max": 80,
    "mood": "calm",
    "duration_seconds": 300,
    "genre": "ambient"
  },
  "downloaded_at": "2025-12-23T10:30:00"
}
```

## Library Index

Master index at `epidemic_music_library/library_index.json`:

```json
{
  "generated_at": "2025-12-23T15:00:00",
  "total_tracks": 35,
  "platforms": {
    "youtube": {
      "calm": [
        {
          "title": "Peaceful Morning",
          "artist": "Relaxing Artist",
          "url": "https://...",
          "file": "epidemic_music_library/youtube/calm/youtube_calm_60-80bpm_300s_1.wav"
        }
      ]
    }
  }
}
```

## Troubleshooting

### Login fails
```bash
# Make sure environment variables are set
echo $EPIDEMIC_EMAIL
echo $EPIDEMIC_PASSWORD

# Try interactive login first (NOT headless)
python epidemic_browser_login.py --test

# Clear session and try again
python epidemic_browser_login.py --clear
python epidemic_browser_login.py --test
```

### 2FA Required
If Epidemic Sound requires 2FA:
1. **Do NOT use headless mode**
2. Run: `python epidemic_auto_downloader.py`
3. Complete 2FA in browser when prompted
4. Press ENTER to continue

### Downloads not starting
Check the logs:
```bash
tail -f epidemic_downloader.log
```

Common issues:
- Browser element selectors changed (Epidemic updated their UI)
- Network timeout
- Session expired

### Download interrupted
Always use `--resume`:
```bash
python epidemic_auto_downloader.py --resume
```

### Downloads going to wrong folder
Check Playwright download settings in the script. Default is `./downloads`

Make sure you have write permissions:
```bash
# Linux/Mac
chmod 755 downloads/
chmod 755 epidemic_music_library/

# Windows - check folder permissions
```

## Performance

### Expected Runtime
- **Quick mode** (2 per category): ~30-45 minutes
- **Full download** (35 tracks): ~2-3 hours

Timing depends on:
- Download speed
- Epidemic Sound server response
- Adapt processing time (typically 10-30 seconds per track)

### Resource Usage
- Chrome browser: ~500MB RAM
- Disk space: ~2-3GB for full library (WAV files)
- CPU: Light (mostly waiting)

## Logs

Two log files are created:

### epidemic_login.log
Login session management logs

### epidemic_downloader.log
Download progress and errors

View in real-time:
```bash
# Linux/Mac
tail -f epidemic_downloader.log

# Windows
Get-Content epidemic_downloader.log -Wait
```

## Customization

### Add New Platform Category

Edit `PLATFORM_CONFIGS` in `epidemic_auto_downloader.py`:

```python
PLATFORM_CONFIGS = {
    # ... existing configs ...

    "snapchat_creative": PlatformConfig(
        platform="snapchat",
        category="creative",
        bpm_min=110,
        bpm_max=130,
        mood="playful",
        duration_seconds=30,
        count=5,
        genre="indie"
    ),
}
```

### Adjust Download Counts

Change the `count` in platform configs:

```python
"youtube_calm": PlatformConfig(
    # ...
    count=10,  # Download 10 instead of 5
),
```

### Change File Format

Currently downloads WAV. To change to MP3, modify `_download_from_adapt()`:

```python
# Look for format selector before downloading
await self.page.select_option("select[name='format']", "mp3")
```

## Best Practices

1. **First run NOT headless**: Test login interactively first
2. **Use quick mode for testing**: Verify everything works with `--quick`
3. **Monitor first few downloads**: Watch the first category to ensure it's working
4. **Let it run uninterrupted**: Once started, let the full download complete
5. **Use resume if interrupted**: Don't restart from scratch
6. **Check logs if issues**: `tail -f epidemic_downloader.log`

## FAQ

**Q: Can I run this in the background?**
A: Yes, use `--headless` flag, but test login first without headless.

**Q: How do I stop the download?**
A: Press `Ctrl+C`. Progress is saved automatically.

**Q: Can I change platforms mid-download?**
A: No, but you can `Ctrl+C`, edit checkpoint file, and resume.

**Q: Does this violate Epidemic Sound TOS?**
A: This uses your authenticated session - same as manual downloading. But check Epidemic's terms to be sure.

**Q: What if selectors break?**
A: Epidemic Sound may update their UI. Check the code and update CSS selectors if needed.

**Q: Can I parallelize downloads?**
A: No - browser automation is sequential. But you could run multiple instances with different platforms.

## License

MIT License - See LICENSE file

## Support

For issues or questions:
1. Check logs: `epidemic_downloader.log`
2. Review screenshots: `error_*.png`
3. Try with `--quick` first
4. Clear session and re-login

---

**Expected Total Runtime**: 2-3 hours for full library (35 tracks)

**Status**: Production-ready with comprehensive error handling and resume capability
