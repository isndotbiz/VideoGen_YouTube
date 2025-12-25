# BACKGROUND MUSIC - 5-MINUTE QUICK START

Get royalty-free background music for your videos in under 5 minutes. Choose your method below.

---

## METHOD 1: EMERGENCY MUSIC (FASTEST - NO CREDENTIALS)

**Best for:** Quick testing, backup music, no-setup-required

**Time:** 5-10 minutes | **Tracks:** 20 | **Cost:** FREE

### What to Run

```bash
python emergency_music_downloader.py
```

That's it! No API keys, no credentials, no browser automation.

### What You Get

```
background_music_emergency/
├── calm/          (10 ambient/calm tracks)
├── energetic/     (10 upbeat/energetic tracks)
├── MASTER_INDEX.json
└── README.md
```

### Using the Music

```python
import json
import random

# Load music library
with open("background_music_emergency/MASTER_INDEX.json", "r") as f:
    music = json.load(f)

# Pick random calm track
track = random.choice(music["tracks"]["calm"])
music_path = track["path"]
attribution = track["metadata"]["attribution"]

print(f"Music: {music_path}")
print(f"Add to video description: {attribution}")
```

### Example Integration

```bash
# Add music to existing video
python example_use_emergency_music.py
```

### Music Source

- **Source:** Jamendo API (no signup required)
- **License:** CC-BY-NC
- **Attribution:** Required (auto-included in metadata)
- **Quality:** Professional royalty-free music

### Attribution Required

Add to your YouTube description:

```
Music by [Artist Name] from Jamendo
```

The exact text is in each track's `.json` file.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| No tracks found | Check internet connection, retry |
| Download failed | Wait a few minutes, script auto-retries |
| Encoding errors | Update Python to 3.7+ |

---

## METHOD 2: YOUTUBE MUSIC (BEST FOR YOUTUBE)

**Best for:** YouTube long-form content with proper licensing

**Time:** 10-15 minutes | **Tracks:** 20-60 | **Credentials:** Epidemic Sound API

### Setup (One-time)

1. Get Epidemic Sound API credentials:
   - Visit: https://www.epidemicsound.com/
   - Sign up for account
   - Get API access key

2. Set environment variables:

**Windows (PowerShell):**
```powershell
$env:EPIDEMIC_ACCESS_KEY_ID="your_access_key_id"
$env:EPIDEMIC_ACCESS_KEY_SECRET="your_access_key_secret"
```

**Linux/Mac:**
```bash
export EPIDEMIC_ACCESS_KEY_ID="your_access_key_id"
export EPIDEMIC_ACCESS_KEY_SECRET="your_access_key_secret"
```

**Or create `.env` file:**
```
EPIDEMIC_ACCESS_KEY_ID=your_access_key_id
EPIDEMIC_ACCESS_KEY_SECRET=your_access_key_secret
```

### What to Run

**Quick test (20 tracks):**
```bash
python download_all_platform_music.py --quick
```

**Full download (60 tracks):**
```bash
python download_all_platform_music.py
```

**YouTube only (20 tracks):**
```bash
python download_all_platform_music.py --platforms youtube
```

### What You Get

```
background_music_epidemic/
├── youtube/
│   ├── calm/          (10 tracks, 60-80 BPM)
│   ├── energetic/     (10 tracks, 120-140 BPM)
│   └── metadata/
├── library_index.json
└── download_log.json
```

### Music Specs

- **Calm:** 60-80 BPM, ambient, minimal, perfect for tutorials
- **Energetic:** 120-140 BPM, upbeat, good for intros/outros
- **Genre:** Electronic, Ambient, Corporate
- **Quality:** 320kbps MP3
- **Duration:** 5+ minutes per track

### Using the Music

```python
import json
import random

# Load library
with open("background_music_epidemic/library_index.json") as f:
    library = json.load(f)

# Get random YouTube calm track
track_ids = library['platforms']['youtube']['calm']
track_id = random.choice(track_ids)
track_data = library['tracks'][track_id]

music_path = track_data['file_path']
print(f"Using: {track_data['title']} ({track_data['bpm']} BPM)")
```

### Features

- Parallel downloading (5 tracks at once)
- Smart deduplication (skips existing)
- Auto-retry on failure (3 attempts)
- Instrumental only (no vocals)
- BPM-matched for platform

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Check API credentials are correct |
| No tracks found | Verify API access to free tracks |
| Download timeout | Check internet, run with --resume |

---

## METHOD 3: SOCIAL MEDIA MUSIC

**Best for:** Instagram Reels, TikTok, Twitter/X content

**Time:** 5-10 minutes | **Tracks:** 15-25 | **Credentials:** Epidemic Sound API

### Setup

Same as Method 2 (Epidemic Sound API credentials)

### What to Run

**Instagram (all types, 15 tracks):**
```bash
python download_social_music.py --platform instagram --content-type all
```

**Instagram Fitness (5 tracks, 130-150 BPM):**
```bash
python download_social_music.py --platform instagram --content-type fitness
```

**Twitter (10 tracks, 100-130 BPM):**
```bash
python download_social_music.py --platform twitter
```

**Everything (25 tracks):**
```bash
python download_social_music.py --platform both
```

### What You Get

```
background_music_epidemic/
├── instagram/
│   ├── fitness/    (5 high-energy, 130-150 BPM)
│   ├── beauty/     (5 elegant, 90-120 BPM)
│   └── travel/     (5 cinematic, 80-110 BPM)
├── twitter/        (10 professional, 100-130 BPM)
└── music_metadata.json
```

### Platform Specs

- **Instagram Fitness:** 30-60s, 130-150 BPM, high energy
- **Instagram Beauty:** 30-60s, 90-120 BPM, elegant
- **Instagram Travel:** 30-60s, 80-110 BPM, cinematic
- **Twitter/X:** 60-120s, 100-130 BPM, professional

---

## METHOD 4: BATCH DOWNLOAD (50+ TRACKS)

**Best for:** Building a large music library

**Time:** 15 minutes | **Tracks:** 50 | **Credentials:** Epidemic Sound API + Browser Login

### Setup

1. Install Playwright:
```bash
pip install playwright python-dotenv
playwright install chromium
```

2. Login to Epidemic Sound:
```bash
python epidemic_login.py
```

3. Verify session works:
```bash
python download_10_tracks_auto.py
```

### What to Run

**Sequential (recommended, 15 min):**
```bash
python download_50_tracks_batch.py
```

**Parallel (faster, 5-7 min):**
```bash
python download_50_tracks_parallel.py
```

**Batch script (simplest, Windows):**
```bash
download_50_tracks_batch.bat
```

### Check Results

```bash
ls background_music_epidemic/batch_download/
cat MASTER_LIBRARY_SUMMARY.json
```

---

## USING MUSIC IN VIDEOS

### Quick FFmpeg Example

```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a]volume=1.0[narration];[1:a]volume=0.15[music];[narration][music]amix=inputs=2:duration=first[audio]" \
  -map 0:v:0 -map "[audio]" \
  -c:v copy -c:a aac \
  -shortest -y output.mp4
```

### Python Integration

```python
import subprocess

def add_background_music(video_path, music_path, output_path, music_volume=0.15):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", music_path,
        "-filter_complex",
        f"[0:a]volume=1.0[narration];[1:a]volume={music_volume}[music];[narration][music]amix=inputs=2:duration=first[audio]",
        "-map", "0:v:0",
        "-map", "[audio]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "-y",
        output_path
    ]
    subprocess.run(cmd)
    print(f"Created: {output_path}")

# Usage
add_background_music(
    video_path="my_video.mp4",
    music_path="background_music_emergency/calm/track1.mp3",
    output_path="my_video_with_music.mp4",
    music_volume=0.15  # 15% volume
)
```

---

## COMPARISON TABLE

| Method | Time | Tracks | Credentials | Best For |
|--------|------|--------|-------------|----------|
| **Emergency** | 5-10 min | 20 | None | Quick testing, backup |
| **YouTube Music** | 10-15 min | 20-60 | Epidemic API | Long-form YouTube |
| **Social Media** | 5-10 min | 15-25 | Epidemic API | Reels, TikTok, Twitter |
| **Batch Download** | 15 min | 50 | Epidemic + Browser | Large library |

---

## QUICK DECISION TREE

**Start here:**

1. **Need music RIGHT NOW with zero setup?**
   - Run: `python emergency_music_downloader.py`
   - FREE, no credentials, works immediately

2. **Making YouTube videos and have Epidemic account?**
   - Run: `python download_all_platform_music.py --quick`
   - Best quality, proper licensing

3. **Making Instagram/TikTok content?**
   - Run: `python download_social_music.py --platform instagram`
   - Optimized for social media specs

4. **Building a large production library?**
   - Run: `python download_50_tracks_batch.py`
   - 50+ tracks in one go

---

## EXPECTED OUTPUT

### Success (Emergency)
```
Downloading calm music from Jamendo...
  1/10: Downloaded track (3.2 MB)
  2/10: Downloaded track (4.1 MB)
  ...
Downloading energetic music...
  1/10: Downloaded track (3.8 MB)
  ...
SUCCESS! Downloaded 20 tracks
Location: background_music_emergency/
```

### Success (YouTube)
```
Authenticating with Epidemic Sound...
Searching for YouTube calm music (60-80 BPM)...
  Found 10 tracks
Downloading track 1/10: Ambient Dreams
  Downloaded: ambient_dreams_70bpm.mp3 (15.2 MB)
...
SUCCESS! Downloaded 20 tracks
Check: background_music_epidemic/youtube/
```

---

## FILE LOCATIONS

All scripts are in:
```
D:\workspace\VideoGen_YouTube\
```

Key scripts:
- `emergency_music_downloader.py` - No credentials needed
- `download_all_platform_music.py` - YouTube + social platforms
- `download_social_music.py` - Instagram, TikTok, Twitter
- `download_50_tracks_batch.py` - Large batch download
- `example_use_emergency_music.py` - Integration examples

---

## NEXT STEPS

1. **Pick a method** from above (Emergency is fastest)
2. **Run the command** (one line)
3. **Wait 5-15 minutes** (downloads automatically)
4. **Use the music** (examples provided)
5. **Add attribution** (if required)

---

## SUPPORT & DOCS

- **Emergency Music:** `EMERGENCY_MUSIC_QUICK_START.md`
- **YouTube Music:** `MUSIC_DOWNLOADER_QUICK_START.txt`
- **Social Media:** `SOCIAL_MUSIC_QUICK_START.md`
- **Batch Download:** `BATCH_DOWNLOAD_GUIDE.md`
- **Complete Guide:** `BACKGROUND_MUSIC_COMPLETE_GUIDE.md`

---

## LICENSE SUMMARY

### Emergency (Jamendo)
- License: CC-BY-NC
- Attribution: Required
- Commercial: Requires paid license
- Free for: Testing, non-commercial

### Epidemic Sound
- License: Commercial OK (with subscription)
- Attribution: Appreciated but not required
- YouTube Safe: Yes (with active subscription)
- Monetization: Allowed

---

## RECOMMENDED: START HERE

**If you just want to test and get music NOW:**

```bash
# This will work immediately with zero setup:
python emergency_music_downloader.py

# Then integrate into your videos:
python example_use_emergency_music.py
```

**Total time: 5-10 minutes**
**Requirements: Just Python (no API keys, no credentials)**
**Output: 20 royalty-free tracks ready to use**

---

Generated: 2025-12-24
Location: D:\workspace\VideoGen_YouTube\BACKGROUND_MUSIC_QUICK_START.md
