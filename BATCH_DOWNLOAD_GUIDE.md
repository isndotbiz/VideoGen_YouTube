# 50-Track Batch Download Guide

## Overview

Build a comprehensive 50-track music library by running the proven `download_10_tracks_auto.py` script 5 times.

**Success Rate:** 10/10 per batch (100%)
**Time per Batch:** ~3 minutes
**Total Time:** ~15 minutes
**Total Tracks:** 50

---

## Two Options Available

### Option 1: Python Orchestrator (Recommended)

**File:** `download_50_tracks_batch.py`

**Features:**
- Automatic session validation between batches
- Progress tracking (10/50, 20/50, etc.)
- Master library summary at end
- Error handling with continue/abort prompts
- Detailed JSON reports

**Usage:**
```bash
python download_50_tracks_batch.py
```

**Output:**
- `background_music_epidemic/batch_download/` - All tracks organized by platform
- `MASTER_LIBRARY_SUMMARY.json` - Complete library manifest

---

### Option 2: Simple Batch Script

**File:** `download_50_tracks_batch.bat` (Windows)

**Features:**
- Simple sequential execution
- 5-second delays between batches
- Progress display
- Stops on first error

**Usage:**
```bash
download_50_tracks_batch.bat
```

**or double-click the .bat file**

---

## Prerequisites

1. **Active Epidemic Sound session:**
   ```bash
   python epidemic_login.py
   ```
   This creates `epidemic_session.json`

2. **Verify session works:**
   ```bash
   python download_10_tracks_auto.py
   ```
   Should download 10 tracks successfully

---

## How It Works

Each batch downloads 10 tracks:

**Batch 1:** Tracks 1-10 (Electronic, various moods)
**Batch 2:** Tracks 11-20 (Different track indices)
**Batch 3:** Tracks 21-30
**Batch 4:** Tracks 31-40
**Batch 5:** Tracks 41-50

The script uses different track indices on each run to ensure variety.

---

## Expected Output

```
background_music_epidemic/batch_download/
├── youtube_calm/
│   ├── youtube_calm_calm_01.mp3
│   ├── youtube_calm_peaceful_02.mp3
│   └── youtube_calm_ambient_03.mp3
├── youtube_energetic/
│   ├── youtube_energetic_energetic_04.mp3
│   ├── youtube_energetic_uplifting_05.mp3
│   └── youtube_energetic_upbeat_06.mp3
├── tiktok_high_energy/
│   └── tiktok_high_energy_energetic_07.mp3
├── instagram_fitness/
│   └── instagram_fitness_energetic_08.mp3
├── instagram_beauty/
│   └── instagram_beauty_elegant_09.mp3
├── instagram_travel/
│   └── instagram_travel_cinematic_10.mp3
├── download_summary.json (from each batch)
└── MASTER_LIBRARY_SUMMARY.json (final report)
```

---

## Troubleshooting

### Session Expired
```
ERROR: Session validation failed!
```

**Solution:** Re-login
```bash
python epidemic_login.py
```

### Batch Failed
The Python version will ask:
```
Batch 2 failed. Continue with remaining batches? (y/n):
```

- Press `y` to continue with next batch
- Press `n` to stop

### Downloads Not Starting
- Check that `download_10_tracks_auto.py` works standalone first
- Verify you're in the correct directory
- Ensure Epidemic Sound session is active

---

## Performance Notes

**Proven Stats (per batch):**
- Success Rate: 10/10 (100%)
- Runtime: ~3 minutes
- File Size: ~30-50 MB total

**For 5 batches:**
- Expected Success: 50/50 tracks
- Total Runtime: ~15 minutes
- Total Size: ~150-250 MB

---

## After Download

### Verify Library
```bash
# Check MASTER_LIBRARY_SUMMARY.json for:
- Total tracks downloaded
- Size breakdown by platform
- File paths and metadata
```

### Use in Videos
The tracks are now organized by platform and ready to use:

```python
# Example: Get calm YouTube tracks
youtube_calm_dir = Path("background_music_epidemic/batch_download/youtube_calm")
calm_tracks = list(youtube_calm_dir.glob("*.mp3"))
```

---

## Tips

1. **Run during off-peak hours** - Less network congestion
2. **Don't interrupt** - Let all 5 batches complete
3. **Check summaries** - Each batch creates a summary JSON
4. **Session lasts 24-48 hours** - No need to re-login between batches
5. **Variety guaranteed** - Different track indices ensure no duplicates

---

## Next Steps

After building your 50-track library:

1. **Test tracks:** Listen to ensure quality
2. **Categorize further:** Create playlists by mood/energy
3. **Integrate into pipeline:** Use with video generation scripts
4. **Scale up:** Run again for 100+ track library

---

## Quick Commands

```bash
# Option 1: Python orchestrator (recommended)
python download_50_tracks_batch.py

# Option 2: Batch script (simple)
download_50_tracks_batch.bat

# Check results
dir background_music_epidemic\batch_download /s

# View summary
type background_music_epidemic\batch_download\MASTER_LIBRARY_SUMMARY.json
```

---

**Status:** Ready to use
**Last Updated:** 2025-12-23
