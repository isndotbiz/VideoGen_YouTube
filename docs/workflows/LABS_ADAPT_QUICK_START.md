# Labs Adapt Complete - Quick Start

**Get started in 60 seconds**

---

## Prerequisites

```bash
# 1. Install dependencies
pip install playwright
playwright install chromium

# 2. Create session file (one-time setup)
python epidemic_browser_login.py
```

---

## Basic Usage

### Download 3 tracks

```bash
python labs_adapt_complete.py --tracks "Neon Dreams" "Electric Pulse" "Digital Wave"
```

### Resume if interrupted

```bash
python labs_adapt_complete.py --resume
```

### Headless mode (faster)

```bash
python labs_adapt_complete.py --headless --tracks "Track 1" "Track 2"
```

---

## What Happens

For each track (5-8 minutes):
1. **Navigate** to Labs Adapt
2. **Search** for track by name
3. **Adapt Length** → 3 minutes, ducking enabled, steady section
4. **Adapt Music** → Minimal, background-friendly for voiceover
5. **Download** → WAV format

---

## Output

Files saved to:
```
background_music_epidemic/labs_adapt_complete/
```

Format:
```
adapt_001_Neon_Dreams_20251223_143022.wav
adapt_002_Electric_Pulse_20251223_144530.wav
```

---

## Expected Time

- **1 track**: 6 minutes
- **5 tracks**: 30 minutes
- **10 tracks**: 60 minutes

---

## Common Commands

```bash
# Download specific tracks
python labs_adapt_complete.py --tracks "Track A" "Track B" "Track C"

# Resume from checkpoint
python labs_adapt_complete.py --resume

# Headless mode
python labs_adapt_complete.py --headless --tracks "Track 1"
```

---

## Troubleshooting

**Session expired?**
```bash
python epidemic_browser_login.py
```

**Track not found?**
- Check spelling
- Try partial name
- Script selects first result

**Need help?**
- Check `labs_adapt_complete.log`
- Review `error_*.png` screenshots
- See full README: `LABS_ADAPT_COMPLETE_README.md`

---

## That's It!

You're ready to download optimized background music for voiceover videos.

For full documentation, see: **LABS_ADAPT_COMPLETE_README.md**
