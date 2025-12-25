# Labs Adapt Complete - Master Orchestration Script

**Production-ready automation for Epidemic Sound Labs Adapt**

Complete workflow that combines navigation, length adaptation, music adaptation, and WAV download into one seamless pipeline.

---

## Features

- **Full Automation**: Navigate → Search → Adapt Length → Adapt Music → Download WAV
- **Progress Tracking**: Real-time progress bar with ETA calculation
- **Checkpoint System**: Resume from where you left off if interrupted
- **Error Handling**: Automatic retry with configurable attempts
- **Production Ready**: Comprehensive logging and error recovery
- **Batch Processing**: Process multiple tracks in sequence

---

## Installation

### 1. Install Dependencies

```bash
pip install playwright
playwright install chromium
```

### 2. Create Session File

You must have a valid `epidemic_session.json` file. If you don't have one:

```bash
# Run the login script first
python epidemic_browser_login.py
```

This will create a session file that persists your login for 7 days.

---

## Usage

### Basic Usage - Download Specific Tracks

```bash
python labs_adapt_complete.py --tracks "Track Name 1" "Track Name 2" "Track Name 3"
```

### Example with Real Track Names

```bash
python labs_adapt_complete.py --tracks "Neon Dreams" "Electric Pulse" "Digital Wave"
```

### Resume from Checkpoint

If the script is interrupted (Ctrl+C or error), resume from where it left off:

```bash
python labs_adapt_complete.py --resume
```

### Headless Mode (Faster)

Run without GUI for faster execution:

```bash
python labs_adapt_complete.py --headless --tracks "Track 1" "Track 2"
```

---

## What It Does

For each track, the script automatically:

### 1. Navigate to Labs Adapt (1-2 min)
- Goes to https://www.epidemicsound.com/labs/adapt/
- Verifies Adapt interface loaded

### 2. Search & Select Track (30s)
- Searches for track by name
- Selects first matching result
- Loads track into Adapt tool

### 3. Adapt Length (1 min)
- Sets duration to **3 minutes (180 seconds)**
- Enables **ducking mix** for voiceover compatibility
- Selects **steady section** type
- Waits for AI processing (30-60s)

### 4. Adapt Music (1-2 min)
- Applies description: "Minimal, background-friendly for voiceover narration"
- Reduces mid-range frequencies (200-800Hz) where voice sits
- Removes buildups and drops
- Creates steady, consistent groove
- Processes all stems
- Waits for AI processing (30-90s)

### 5. Download WAV (1 min)
- Selects WAV format
- Downloads to `background_music_epidemic/labs_adapt_complete/`
- Saves with descriptive filename
- Verifies file size

**Total time per track: 5-8 minutes**

---

## Configuration

Edit `AdaptConfig` class in the script to customize:

### Length Adaptation
```python
LENGTH_DURATION_SECONDS = 180  # 3 minutes
LENGTH_ENABLE_DUCKING = True
LENGTH_SECTION_TYPE = "steady"  # steady, energetic, calm
```

### Music Adaptation
```python
MUSIC_DESCRIPTION = (
    "Minimal, background-friendly for voiceover narration. "
    "Reduce mid-range frequencies 200-800Hz where voice sits. "
    "Keep electronic energy but subtle. Remove buildups and drops. "
    "Create steady, consistent groove with narrow dynamic range. "
    "Optimize for ducking mix technology."
)
MUSIC_STEMS = "all"
```

### Download
```python
DOWNLOAD_FORMAT = "wav"
OUTPUT_DIR = Path("background_music_epidemic/labs_adapt_complete")
```

### Retry
```python
MAX_RETRY_ATTEMPTS = 2
RETRY_DELAY_SECONDS = 5
```

---

## Output

### Directory Structure
```
background_music_epidemic/
└── labs_adapt_complete/
    ├── adapt_001_Neon_Dreams_20251223_143022.wav
    ├── adapt_002_Electric_Pulse_20251223_144530.wav
    └── adapt_003_Digital_Wave_20251223_150045.wav
```

### Checkpoint File
```
labs_adapt_checkpoint.json
```

Saves progress after each track. Contains:
- Task status (pending, completed, failed)
- Download paths
- Error messages
- Timestamps

### Log File
```
labs_adapt_complete.log
```

Complete execution log with:
- Navigation steps
- Adaptation progress
- Download status
- Errors and warnings

---

## Progress Tracking

Real-time progress display:

```
================================================================================
PROGRESS: 2/5 (40.0%) | Failed: 0
Current: Electric Pulse
Status: Adapting music (minimal)...
Elapsed: 0:12:34 | ETA: 0:18:51
================================================================================
```

Shows:
- Tracks completed / total
- Completion percentage
- Failed track count
- Current track name
- Current operation
- Time elapsed
- Estimated time remaining

---

## Error Handling

### Automatic Retry
- Each track gets 3 attempts (1 initial + 2 retries)
- 5-second delay between retries
- Screenshots saved on errors: `error_adapt_length.png`, `error_download.png`

### Checkpoint Resume
If interrupted:
```bash
python labs_adapt_complete.py --resume
```

Resumes from last successful track.

### Common Issues

**Session expired:**
```bash
python epidemic_browser_login.py  # Re-create session
```

**Track not found:**
- Check track name spelling
- Try partial name (script selects first result)

**Download timeout:**
- Check internet connection
- Increase timeout in config: `TIMEOUT_DOWNLOAD = 180000`

---

## CLI Reference

```bash
python labs_adapt_complete.py [OPTIONS]
```

### Required (one of):
- `--tracks TRACK1 TRACK2 ...` - List of track names
- `--count N` - Download first N tracks (not yet implemented)
- `--resume` - Resume from checkpoint

### Optional:
- `--headless` - Run without GUI (faster, less resource intensive)

---

## Example Workflow

### Single Track
```bash
python labs_adapt_complete.py --tracks "Neon Dreams"
```

### Multiple Tracks
```bash
python labs_adapt_complete.py --tracks \
  "Neon Dreams" \
  "Electric Pulse" \
  "Digital Wave" \
  "Cyber Horizon" \
  "Future Bass"
```

### Batch Processing with Resume
```bash
# Start processing 10 tracks
python labs_adapt_complete.py --tracks \
  "Track 1" "Track 2" "Track 3" "Track 4" "Track 5" \
  "Track 6" "Track 7" "Track 8" "Track 9" "Track 10"

# If interrupted after track 5, resume:
python labs_adapt_complete.py --resume
```

---

## Performance

### Expected Runtime
- **1 track**: 5-8 minutes
- **5 tracks**: 25-40 minutes
- **10 tracks**: 50-80 minutes

### Optimization Tips
1. Use `--headless` for faster execution
2. Run during off-peak hours (better API response)
3. Ensure stable internet connection
4. Close other browser tabs/applications

---

## Advanced Usage

### Integrate with Other Scripts

```python
from labs_adapt_complete import LabsAdaptOrchestrator

# Create orchestrator
orchestrator = LabsAdaptOrchestrator(
    track_names=["Track 1", "Track 2"],
    headless=True,
    resume=False,
)

# Run
await orchestrator.run()
```

### Modify Adaptation Settings

Edit the `AdaptConfig` class to change:
- Duration (e.g., 5 minutes instead of 3)
- Music description (e.g., more aggressive vs. more ambient)
- Ducking settings
- Output format (WAV vs. MP3)

---

## Troubleshooting

### Script hangs during processing

**Cause**: AI processing taking longer than expected

**Solution**: Increase timeout in config:
```python
TIMEOUT_ADAPT_PROCESSING = 180000  # 3 minutes
```

### Download button not found

**Cause**: Adapt interface changed or not fully loaded

**Solution**: Check screenshots in `error_*.png` files

### Session invalid

**Cause**: Session file expired (>7 days old)

**Solution**: Re-create session:
```bash
python epidemic_browser_login.py
```

---

## Related Scripts

- **epidemic_browser_login.py** - Create session file
- **epidemic_browser_search.py** - Search and browse tracks
- **epidemic_browser_adapt.py** - Low-level Adapt automation
- **epidemic_ai_search_adapt.py** - AI-powered search + Adapt

---

## Production Checklist

Before running large batches:

- [ ] Valid session file exists (`epidemic_session.json`)
- [ ] Output directory has sufficient space (50 MB per track)
- [ ] Internet connection is stable
- [ ] Test with 1-2 tracks first
- [ ] Review adaptation settings
- [ ] Monitor first few tracks for quality

---

## Support

For issues or questions:
1. Check `labs_adapt_complete.log` for errors
2. Review screenshot files (`error_*.png`)
3. Try running with `--headless` disabled to see browser
4. Verify session is valid (re-run login script)

---

## License

Part of VideoGen YouTube Project

---

## Changelog

### v1.0 (2025-12-23)
- Initial release
- Full automation pipeline
- Checkpoint system
- Progress tracking
- Error handling with retry
- WAV download support
