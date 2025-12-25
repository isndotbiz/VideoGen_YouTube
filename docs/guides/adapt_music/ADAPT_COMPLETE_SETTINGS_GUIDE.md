# Epidemic Sound Adapt - Complete Settings Guide

## Complete Configuration Reference for Perfect Background Music

This guide documents ALL settings, values, and configurations for Epidemic Sound's Adapt Length and Adapt Music features, optimized for 3-minute video production with professional voiceover.

---

## Table of Contents

1. [Adapt Length Settings](#adapt-length-settings)
2. [Adapt Music Settings](#adapt-music-settings)
3. [Ducking Mix Configuration](#ducking-mix-configuration)
4. [Volume Settings](#volume-settings)
5. [Stems Configuration](#stems-configuration)
6. [Complete Workflow Settings](#complete-workflow-settings)
7. [Automation Configuration](#automation-configuration)

---

## Adapt Length Settings

### Duration Settings

#### For 3-Minute Videos (Recommended)
```
Duration: 180 seconds (3 minutes / 3:00)
```

#### Duration Format Options
The automation supports three formats:

**Format 1: Seconds**
```
180
```

**Format 2: Minutes:Seconds**
```
3:00
```

**Format 3: Minutes with Unit**
```
3 min
3 minutes
3 m
```

#### Duration Options by Video Length

| Video Length | Recommended Duration | Seconds | Format |
|--------------|---------------------|---------|--------|
| 30 seconds | 30 seconds | 30 | `30` or `0:30` |
| 1 minute | 60 seconds | 60 | `60` or `1:00` |
| 1.5 minutes | 90 seconds | 90 | `90` or `1:30` |
| 3 minutes | 180 seconds | 180 | `180` or `3:00` |
| 5 minutes | 300 seconds | 300 | `300` or `5:00` |
| 15 minutes | Use 3x 5-min tracks | 300 each | Multiple downloads |

### Section Selection Settings

#### Auto Selection (Recommended)
```
use_auto_selection: True
start_position_seconds: None
```

**What it does:**
- Epidemic AI automatically selects the best section
- Targets steady volume areas
- Avoids intros and outros
- No manual waveform manipulation needed

#### Manual Selection (Advanced)
```
use_auto_selection: False
start_position_seconds: 45  # Start at 0:45 into track
```

**Best practices for manual selection:**
- Start position: 30-60 seconds into track
- Avoid first 30s (intro/buildup)
- Avoid last 30s (outro/fadeout)
- Look for flattest waveform section
- Target areas with consistent height/amplitude

### Waveform Selection Guide

**Visual indicators to look for:**
- Consistent waveform height
- Minimal peaks and valleys
- Steady rhythm pattern
- Flat horizontal appearance
- No dramatic buildups or drops

**Avoid sections with:**
- Quiet intros (low amplitude)
- Dramatic buildups (increasing amplitude)
- Bass drops (sudden peaks)
- Fadeout outros (decreasing amplitude)
- Heavy frequency changes

### Processing Settings

```
max_processing_time: 90 seconds (default)
```

**Typical processing times:**
- Fast: 30-45 seconds
- Average: 45-60 seconds
- Slow: 60-90 seconds
- Timeout: 90+ seconds (increase limit if needed)

**Processing timeout configuration:**
```python
# Python
max_processing_time=90  # seconds

# CLI flag
--timeout 90
```

---

## Adapt Music Settings

### AI Description Settings

#### Default Description (Recommended for Voiceover)
```
Minimal, background-friendly for voiceover narration. Reduce mid-range
frequencies (200-800Hz) to make room for voice. Keep electronic energy
but make it subtle and consistent. Remove dramatic buildups. Create
steady, hypnotic groove suitable for extended background use.
```

**Why this works:**
- Reduces 200-800Hz range (vocal frequency space)
- Maintains energy but makes it subtle
- Removes buildups that compete with narration
- Creates consistent groove for long videos
- Optimized for ducking mix technology

#### Short Description (Alternative)
```
Minimal, background-friendly for voiceover narration. Reduce mid-range
frequencies, keep electronic energy but subtle. Remove buildups, create
steady groove.
```

**When to use:**
- Faster processing
- API character limits
- Quick testing

#### Custom Description Templates

**For Ambient/Minimal Style:**
```
Ultra-minimal atmospheric background. Maximum subtlety. Reduce all
frequencies that compete with voice. Create ambient texture that's
barely noticeable but adds professionalism.
```

**For Energetic but Controlled:**
```
Energetic electronic background optimized for narration. Keep tempo
and rhythm but reduce volume of melodic elements. Emphasize bass and
high frequencies, minimize mid-range (200-800Hz). Subtle but present.
```

**For Corporate/Professional:**
```
Professional corporate background. Minimal and unobtrusive. Reduce
mid-frequencies for voice clarity. Maintain subtle electronic energy.
No dramatic elements. Steady and consistent throughout.
```

**For Focus/Concentration:**
```
Deep focus background music. Hypnotic and repetitive. Minimal variation.
Reduce voice-range frequencies. Create meditative, loop-friendly groove
suitable for extended use with continuous narration.
```

### Stems Settings

#### All Stems (Recommended)
```
stems: "all"
stems: "All stems"
```

**What it adapts:**
- Bass
- Drums
- Melody
- Synths
- Pads
- All instrumental elements

**Why use all stems:**
- Complete optimization
- Balanced adaptation
- Best results for voiceover
- Consistent processing across all elements

#### Individual Stems (Advanced)

**Melody Only:**
```
stems: "melody"
```
- Adapts melodic elements
- Leaves rhythm section unchanged
- Use when bass/drums are already perfect

**Bass Only:**
```
stems: "bass"
```
- Adapts bass frequencies
- Leaves other elements unchanged
- Use when bass is too prominent

**Drums Only:**
```
stems: "drums"
```
- Adapts percussion
- Leaves melody/bass unchanged
- Use when drums are too aggressive

**Custom Combination:**
```
stems: "melody,bass"  # Multiple stems
```

### Processing Settings

```
timeout: 120 seconds (default)
```

**Typical AI processing times:**
- Fast: 35-50 seconds
- Average: 50-70 seconds
- Slow: 70-120 seconds
- Extended: 120-180 seconds (increase if needed)

**Configuration:**
```python
# Python
timeout=120  # seconds

# CLI
--timeout 120

# Extended timeout for complex tracks
--timeout 180
```

### Progress Monitoring Settings

```
check_interval: 2 seconds
log_interval: 10 seconds
```

**What gets logged:**
- Every 10 seconds: Progress update
- Every 30 seconds: Screenshot (debug mode)
- At completion: Success/failure status

---

## Ducking Mix Configuration

### What is Ducking Mix?

**Definition:** Automatically reduces music volume when voice is detected, then restores it during silence.

**Benefits:**
- Automatic voice-music balance
- No manual volume keyframing
- Professional podcast-style mixing
- Voice always clear and audible

### Ducking Mix Settings

#### Enable Ducking Mix (Recommended)
```
enable_ducking: True
```

**Python:**
```python
enable_ducking=True
```

**CLI:**
```bash
# Enabled by default in automation
python adapt_length_automation.py --duration 180
```

#### Disable Ducking Mix
```
enable_ducking: False
```

**When to disable:**
- Want constant music volume
- Manual mixing preferred
- Testing different approaches
- Music should never duck

### Ducking Mix Detection

**The automation searches for:**
1. `input[type="checkbox"][name*="duck"]`
2. `input[type="checkbox"][id*="duck"]`
3. `label:has-text("Ducking") input[type="checkbox"]`
4. `label:has-text("Ducking mix") input[type="checkbox"]`
5. `[data-testid="ducking-toggle"]`
6. `button[role="switch"][aria-label*="Ducking"]`

**Behavior:**
- If found: Enables checkbox/toggle
- If already enabled: Skips (no change)
- If not found: Continues without error (optional feature)
- Logs warning if not available

### Manual Ducking Mix Settings (In UI)

**If configuring manually in Epidemic UI:**

**Ducking Sensitivity:**
- Low: Music ducks less (more background volume)
- Medium: Balanced ducking (recommended)
- High: Music ducks more (maximum voice clarity)

**Ducking Depth:**
- -6 dB: Subtle reduction (music still present)
- -12 dB: Moderate reduction (recommended)
- -18 dB: Strong reduction (music very quiet)

**Note:** These fine-tuned settings are not yet exposed in automation (Epidemic uses defaults)

---

## Volume Settings

### Music Volume (Without Ducking Mix)

**Manual volume reduction if NOT using ducking mix:**

```python
# Reduce music to 15% of original volume
music_volume_reduction = -16  # dB

# Or percentage
music_volume_percentage = 0.15  # 15%
```

**Volume recommendations:**
| Narration Style | Music Volume | dB Reduction |
|-----------------|--------------|--------------|
| Continuous talking | 10-15% | -18 to -16 dB |
| Moderate talking | 15-20% | -16 to -14 dB |
| Minimal talking | 20-30% | -14 to -10 dB |
| Music-focused | 30-40% | -10 to -8 dB |

### Volume Consistency Settings

**The adapted music should have:**
- RMS level variation: < 3 dB
- Peak variation: < 6 dB
- Dynamic range: 6-10 dB (narrow)
- Compression: Moderate (prevents pumping)

**To verify volume consistency:**
```bash
python analyze_volume_consistency.py --file adapted_track.wav
```

**Target metrics:**
```
Average RMS: -20 to -15 dB
Peak level: -6 to -3 dB
Dynamic range: 6-10 dB
Variation: < 3 dB throughout
```

---

## Complete Workflow Settings

### Full Configuration (3-Minute Video)

```yaml
# Complete settings for 3-minute background music

ADAPT_LENGTH:
  duration_seconds: 180
  duration_format: "3:00"
  start_position_seconds: null  # Auto-select
  use_auto_selection: true
  enable_ducking: true
  screenshot_on_error: true
  max_processing_time: 90

ADAPT_MUSIC:
  description: |
    Minimal, background-friendly for voiceover narration. Reduce mid-range
    frequencies (200-800Hz) to make room for voice. Keep electronic energy
    but make it subtle and consistent. Remove dramatic buildups. Create
    steady, hypnotic groove suitable for extended background use.
  stems: "all"
  timeout: 120
  screenshot_on_error: true

DOWNLOAD:
  format: "wav"
  quality: "highest"

OUTPUT:
  naming_pattern: "{genre}_{mood}_{bpm}_adapted_3min.wav"
  directory: "background_music_epidemic/"
```

### Settings by Use Case

#### Use Case 1: Educational Tutorial (3-5 min)
```yaml
duration: 180-300 seconds
ducking: enabled
description: "Minimal, background-friendly for voiceover"
stems: "all"
volume: 15% (or use ducking)
```

#### Use Case 2: Short Social Media (30-60 sec)
```yaml
duration: 30-60 seconds
ducking: optional (short videos)
description: "Energetic but minimal for voiceover"
stems: "all"
volume: 20%
```

#### Use Case 3: Long-Form Content (15+ min)
```yaml
duration: 300 seconds (5 min max)
tracks_needed: 3+ (concatenate)
ducking: enabled
description: "Ultra-minimal, extended background use"
stems: "all"
volume: 12% (or use ducking)
```

#### Use Case 4: Podcast Style
```yaml
duration: 300 seconds
ducking: enabled (critical)
description: "Minimal atmospheric texture for podcast"
stems: "all"
volume: 10% (or rely on ducking)
```

---

## Automation Configuration

### Python Configuration

#### adapt_length_automation.py Settings

```python
from adapt_length_automation import adapt_length_automation

success, error = await adapt_length_automation(
    page=page,                          # Playwright page object
    duration_seconds=180,               # 3 minutes
    start_position_seconds=None,        # Auto-select
    enable_ducking=True,                # Enable ducking mix
    use_auto_selection=True,            # Auto section selection
    screenshot_on_error=True,           # Debug screenshots
    max_processing_time=90              # 90 second timeout
)
```

**Configuration class:**
```python
class AdaptLengthConfig:
    TIMEOUT_BUTTON = 5000           # 5s for button clicks
    TIMEOUT_INPUT = 5000            # 5s for input fields
    TIMEOUT_PROCESSING = 90000      # 90s for AI processing
    CHECK_INTERVAL_MS = 2000        # Check every 2 seconds
    LOG_INTERVAL_SEC = 10           # Log every 10 seconds
    SCREENSHOT_DIR = Path("epidemic_screenshots")
```

#### adapt_music_automation.py Settings

```python
from adapt_music_automation import AdaptMusicAutomation

automation = AdaptMusicAutomation(
    page=page,                          # Playwright page object
    headless=True,                      # Run in background
    slow_mo=500,                        # 500ms delay between actions
    description=None,                   # Use default description
    stems="all",                        # Adapt all stems
    timeout=120                         # 120 second timeout
)

result = automation.run()
```

**Configuration constants:**
```python
# Default description
DEFAULT_DESCRIPTION = (
    "Minimal, background-friendly for voiceover narration. Reduce mid-range "
    "frequencies (200-800Hz) to make room for voice. Keep electronic energy "
    "but make it subtle and consistent. Remove dramatic buildups. Create "
    "steady, hypnotic groove suitable for extended background use."
)

# Timeouts
TIMEOUT_DEFAULT = 30
TIMEOUT_AI_PROCESSING = 120
TIMEOUT_ELEMENT_SEARCH = 10

# Screenshots
SCREENSHOT_DIR = Path("debug_screenshots")
```

### CLI Configuration

#### adapt_length_automation.py CLI

```bash
# Basic usage (all defaults)
python adapt_length_automation.py

# Custom duration (3 minutes)
python adapt_length_automation.py --duration 180

# Disable ducking
python adapt_length_automation.py --duration 180 --no-ducking

# Extended timeout
python adapt_length_automation.py --duration 180 --timeout 120

# Debug mode
python adapt_length_automation.py --duration 180 --debug
```

**All CLI options:**
```
--duration SECONDS        Target duration (default: 180)
--start-position SECONDS  Manual start position (default: auto)
--no-ducking             Disable ducking mix
--no-auto                Disable auto selection
--timeout SECONDS        Max processing time (default: 90)
--debug                  Enable debug screenshots
```

#### adapt_music_automation.py CLI

```bash
# Basic usage (default description)
python adapt_music_automation.py

# Custom description
python adapt_music_automation.py --description "Your custom text"

# Short description
python adapt_music_automation.py --use-short-description

# Custom stems
python adapt_music_automation.py --stems "melody,bass"

# Extended timeout
python adapt_music_automation.py --timeout 180

# Debug mode (visible browser)
python adapt_music_automation.py --no-headless

# Slow motion (for watching)
python adapt_music_automation.py --slow 1000
```

**All CLI options:**
```
--description TEXT         Custom AI description
--use-short-description   Use shorter default
--stems CHOICE            Stems to adapt (default: all)
--timeout SECONDS         Max wait time (default: 120)
--no-headless            Show browser
--slow MILLISECONDS      Slow down operations (default: 500)
```

### Environment Variables

```bash
# .env file configuration

# Epidemic Sound credentials (if using login automation)
EPIDEMIC_EMAIL=your-email@example.com
EPIDEMIC_PASSWORD=your-password

# Session storage
EPIDEMIC_SESSION_FILE=epidemic_session.json

# Download settings
MUSIC_OUTPUT_DIR=background_music_epidemic/
SCREENSHOT_DIR=debug_screenshots/

# Processing timeouts
ADAPT_LENGTH_TIMEOUT=90
ADAPT_MUSIC_TIMEOUT=120

# Debug settings
DEBUG_MODE=false
HEADLESS_MODE=true
```

### Batch Processing Configuration

**Process multiple tracks:**
```python
tracks = [
    {"url": "track1_url", "duration": 180, "genre": "chillstep"},
    {"url": "track2_url", "duration": 180, "genre": "techno"},
    {"url": "track3_url", "duration": 180, "genre": "ambient"}
]

for track in tracks:
    # Adapt length
    success, error = await adapt_length_automation(
        page=page,
        duration_seconds=track["duration"],
        enable_ducking=True
    )

    if success:
        # Adapt music
        automation = AdaptMusicAutomation(page=page)
        result = automation.run()

        if result['success']:
            # Download and rename
            download_track(output_name=f"{track['genre']}_adapted_3min.wav")
```

---

## Quick Reference Tables

### Duration Quick Reference

| Video Type | Duration | Seconds | Command |
|------------|----------|---------|---------|
| TikTok/Reel | 30s | 30 | `--duration 30` |
| Instagram | 60s | 60 | `--duration 60` |
| YouTube Short | 60s | 60 | `--duration 60` |
| Short Tutorial | 3 min | 180 | `--duration 180` |
| Full Tutorial | 5 min | 300 | `--duration 300` |
| Long Video | 15 min | 3x 300 | Multiple tracks |

### Stems Quick Reference

| Stem Option | What Gets Adapted | Use Case |
|-------------|------------------|----------|
| `all` | All instruments | Recommended (complete optimization) |
| `melody` | Melodic elements | When rhythm is perfect |
| `bass` | Bass frequencies | When bass is too loud |
| `drums` | Percussion | When drums are aggressive |
| `melody,bass` | Multiple stems | Custom combination |

### Ducking Mix Quick Reference

| Setting | Music Behavior | Best For |
|---------|---------------|----------|
| Enabled | Auto-ducks for voice | Continuous narration |
| Disabled | Constant volume | Manual mixing |

### Volume Quick Reference

| Narration Amount | Music Volume | dB Reduction |
|------------------|--------------|--------------|
| 90%+ talking | 10-15% | -18 to -16 dB |
| 70-90% talking | 15-20% | -16 to -14 dB |
| 50-70% talking | 20-25% | -14 to -12 dB |
| <50% talking | 25-35% | -12 to -10 dB |

---

## Exact Command Examples

### Complete 3-Minute Video Workflow

```bash
# Step 1: Adapt length to 3 minutes with ducking
python adapt_length_automation.py --duration 180

# Step 2: Adapt music for voiceover
python adapt_music_automation.py

# Step 3: Download (via browser or automation)
# Manual: Click download button
# Auto: python adapt_download_automation.py
```

### Custom Workflow Examples

**Example 1: 30-Second Social Media**
```bash
python adapt_length_automation.py --duration 30
python adapt_music_automation.py --description "Energetic, minimal for voiceover"
```

**Example 2: 5-Minute Tutorial**
```bash
python adapt_length_automation.py --duration 300
python adapt_music_automation.py --use-short-description
```

**Example 3: Ultra-Minimal Background**
```bash
python adapt_length_automation.py --duration 180
python adapt_music_automation.py --description "Ultra-minimal atmospheric texture"
```

**Example 4: Debug Mode**
```bash
python adapt_length_automation.py --duration 180 --debug --timeout 120
python adapt_music_automation.py --no-headless --timeout 180
```

---

## Troubleshooting Settings

### If Processing is Slow

**Increase timeouts:**
```bash
python adapt_length_automation.py --duration 180 --timeout 120
python adapt_music_automation.py --timeout 180
```

**Python:**
```python
max_processing_time=120  # Length
timeout=180             # Music
```

### If Ducking Mix Not Working

**Check if available:**
```python
enable_ducking=True
```

**If not supported:**
- Use manual volume reduction
- Apply constant -16 dB to music
- Mix at 15% volume

### If Music Too Loud

**Option 1: Re-adapt with more minimal description:**
```bash
python adapt_music_automation.py --description "Ultra-minimal, maximum subtlety"
```

**Option 2: Post-process volume:**
```python
music = music - 6  # Reduce by additional 6 dB
```

### If Music Too Quiet

**Option 1: Less aggressive description:**
```bash
python adapt_music_automation.py --description "Balanced background, keep energy"
```

**Option 2: Increase post-processing:**
```python
music = music + 3  # Boost by 3 dB
```

---

## Summary: Perfect Settings for 3-Minute Videos

```yaml
RECOMMENDED_CONFIGURATION:

  ADAPT_LENGTH:
    duration: 180 seconds (3:00)
    selection: Auto
    ducking: Enabled
    timeout: 90 seconds

  ADAPT_MUSIC:
    description: "Minimal, background-friendly for voiceover narration.
                  Reduce mid-range frequencies (200-800Hz) to make room
                  for voice. Keep electronic energy but make it subtle
                  and consistent. Remove dramatic buildups. Create steady,
                  hypnotic groove suitable for extended background use."
    stems: All stems
    timeout: 120 seconds

  VOLUME:
    with_ducking: Automatic (handled by ducking mix)
    without_ducking: 15% (−16 dB)

  DOWNLOAD:
    format: WAV
    naming: "{genre}_adapted_3min.wav"

  USAGE:
    CLI: python adapt_length_automation.py --duration 180 &&
         python adapt_music_automation.py

    Python: adapt_length_automation(page, duration_seconds=180,
                                     enable_ducking=True)
            AdaptMusicAutomation(page, stems="all").run()
```

---

## Files Reference

**Configuration Files:**
- `D:\workspace\VideoGen_YouTube\adapt_length_automation.py` (Line 51-72: Config)
- `D:\workspace\VideoGen_YouTube\adapt_music_automation.py` (Line 74-96: Config)

**Documentation:**
- `D:\workspace\VideoGen_YouTube\ADAPT_LENGTH_AUTOMATION_GUIDE.md`
- `D:\workspace\VideoGen_YouTube\ADAPT_MUSIC_COMPLETE.md`
- `D:\workspace\VideoGen_YouTube\EPIDEMIC_COMPLETE_WORKFLOW.md`

**Quick Starts:**
- `D:\workspace\VideoGen_YouTube\ADAPT_LENGTH_QUICK_START.md`
- `D:\workspace\VideoGen_YouTube\ADAPT_MUSIC_QUICK_START.txt`

---

## Status: COMPLETE

All settings documented with exact values, configurations, and usage examples.

Last Updated: December 2025
Project: VideoGen YouTube
