# Adapt Music Automation - Usage Guide

## Overview

The `adapt_music_automation.py` script automates the **"Adapt Music"** feature in Epidemic Sound Labs Adapt. This is **Step 3** in the complete workflow (after Adapt Length).

## When to Use

Run this script **AFTER** `adapt_length_automation.py` has completed successfully. The music adaptation optimizes your 5-minute track for voiceover narration.

## Quick Start

### 1. Basic Usage (Default Description)

```bash
python adapt_music_automation.py
```

This uses the recommended description from EPIDEMIC_COMPLETE_WORKFLOW.md:
- Minimal, background-friendly for voiceover narration
- Reduces mid-range frequencies (200-800Hz) for voice clarity
- Keeps electronic energy but subtle
- Removes dramatic buildups
- Creates steady, hypnotic groove

### 2. Debug Mode (See What's Happening)

```bash
python adapt_music_automation.py --no-headless
```

Opens visible browser window so you can watch the automation.

### 3. Custom Description

```bash
python adapt_music_automation.py --description "Make it more ambient and atmospheric"
```

### 4. Shorter Description (Faster)

```bash
python adapt_music_automation.py --use-short-description
```

Uses condensed version that's quicker to type/process.

### 5. Custom Timeout (For Slow Processing)

```bash
python adapt_music_automation.py --timeout 180
```

Increases wait time to 3 minutes (default is 2 minutes).

## Complete Workflow Example

```bash
# Step 1: Adapt Length (run first)
python adapt_length_automation.py --duration 300

# Step 2: Adapt Music (run after length is done)
python adapt_music_automation.py

# Step 3: Download (next automation script)
python adapt_download_automation.py
```

## What the Script Does

### Step-by-Step Process:

1. **Finds "Adapt music" button**
   - Tries multiple selectors to find the button
   - Scrolls into view if needed
   - Clicks to open Adapt Music panel

2. **Enters description**
   - Finds text input field (textarea, input, or contenteditable)
   - Clears existing text
   - Enters your description

3. **Selects stems**
   - Finds stems dropdown
   - Selects "All stems"
   - Continues if dropdown not available (optional feature)

4. **Clicks process button**
   - Finds submit/arrow button
   - Clicks to start AI processing

5. **Waits for AI processing**
   - Monitors progress indicators
   - Logs updates every 10 seconds
   - Takes screenshots every 30 seconds
   - Maximum wait: 2 minutes (configurable)

6. **Verifies completion**
   - Checks for "Complete", "Done", or download button
   - Validates preview is available
   - Returns success status

## Debugging

### Screenshots

All screenshots are saved to: `debug_screenshots/`

Key screenshots:
- `01_before_adapt_music.png` - Initial state
- `02_adapt_music_panel_opened.png` - After clicking button
- `03_description_entered.png` - After entering text
- `04_stems_selected.png` - After selecting stems
- `05_processing_started.png` - Processing begins
- `06_processing_complete.png` - Processing done
- `07_verification_complete.png` - Final state
- `ERROR_*.png` - Any errors encountered

### Logs

The script logs detailed progress:
```
2025-12-23 10:00:00 - INFO - Looking for 'Adapt music' button...
2025-12-23 10:00:01 - INFO - Found 'Adapt music' button with selector: button:has-text("Adapt music")
2025-12-23 10:00:02 - INFO - Clicked 'Adapt music' button
2025-12-23 10:00:04 - INFO - Looking for description input field...
2025-12-23 10:00:05 - INFO - Description entered: 'Minimal, background-friendly for voiceover...'
...
2025-12-23 10:00:30 - INFO - Still processing... 20s elapsed (16%)
2025-12-23 10:00:40 - INFO - Still processing... 30s elapsed (25%)
...
2025-12-23 10:01:45 - INFO - AI MUSIC ADAPTATION COMPLETE!
```

## Troubleshooting

### Problem: "Adapt music button not found"

**Solution:**
1. Ensure you're on the Adapt tool page
2. Make sure a track is loaded
3. Run with `--no-headless` to see current state
4. Check screenshot: `ERROR_button_not_found.png`

### Problem: "Description input not found"

**Solution:**
1. Check if Adapt Music panel opened
2. Look at screenshot: `ERROR_description_input_not_found.png`
3. UI might have changed - report issue

### Problem: "Processing timeout"

**Solutions:**
1. Increase timeout: `--timeout 180`
2. Check internet connection
3. Epidemic might be slow - try again later
4. Look at progress screenshots to see if stuck

### Problem: Script runs but verification fails

**Solution:**
1. Check `07_verification_complete.png`
2. Processing might have succeeded but UI changed
3. Look for download button manually
4. Continue to next step anyway

## Advanced Usage

### Using with Existing Browser Session

```python
from playwright.sync_api import sync_playwright
from adapt_music_automation import AdaptMusicAutomation

# Your code that navigates to Adapt tool
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # ... your navigation code ...

    # Use existing page
    automation = AdaptMusicAutomation(page=page)
    result = automation.run()

    print(f"Success: {result['success']}")
```

### Custom Integration

```python
from adapt_music_automation import AdaptMusicAutomation

automation = AdaptMusicAutomation(
    headless=True,
    description="Your custom description here",
    stems="melody",  # or "bass", "drums", etc.
    timeout=150
)

result = automation.run()

if result['success']:
    print(f"Adaptation complete in {result['processing_time']:.1f}s")
    print(f"Steps: {result['steps_completed']}")
else:
    print(f"Failed: {result['error']}")
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `--description` | Default description | Custom text for AI adaptation |
| `--use-short-description` | False | Use shorter default description |
| `--stems` | "all" | Which stems to adapt |
| `--timeout` | 120 | Max wait time (seconds) |
| `--no-headless` | False | Show browser (debugging) |
| `--slow` | 500 | Slow down operations (ms) |

## Expected Output

### Success:

```
================================================================================
ADAPT MUSIC AUTOMATION - SUMMARY
================================================================================
Success: True
Processing time: 67.3s
Steps completed: 7
Steps: browser_started, adapt_music_button_clicked, description_entered, stems_selected, process_button_clicked, processing_complete, verification_complete

Verification:
  success: True
  preview_available: True
  download_available: True
  history_updated: True
================================================================================
```

### Failure:

```
================================================================================
ADAPT MUSIC AUTOMATION - SUMMARY
================================================================================
Success: False
Processing time: 125.8s
Steps completed: 5
Steps: browser_started, adapt_music_button_clicked, description_entered, stems_selected, process_button_clicked

Error: AI processing did not complete within 120 seconds. Check screenshots.
================================================================================
```

## Next Steps

After this script succeeds:

1. **Preview the result** (manually or with automation)
2. **Download the adapted track** (next automation script)
3. **Rename the file** properly: `{genre}_{mood}_{bpm}_adapted_5min.wav`
4. **Move to music library**: `background_music_epidemic/`

## Tips

1. **Default description works great** - tested with real tracks
2. **Be patient** - AI processing takes 30-120 seconds normally
3. **Use debug mode first time** - see what's happening
4. **Check screenshots** if any issues
5. **Run multiple tracks** in sequence for batch processing

## Support

If you encounter issues:
1. Check `debug_screenshots/` folder
2. Review script logs
3. Try with `--no-headless` to observe
4. Check Epidemic Sound UI hasn't changed
5. Report issues with screenshots

## References

- **EPIDEMIC_COMPLETE_WORKFLOW.md** - Full workflow documentation
- **adapt_length_automation.py** - Previous step (run first)
- **epidemic_browser_adapt.py** - Complete browser automation suite
