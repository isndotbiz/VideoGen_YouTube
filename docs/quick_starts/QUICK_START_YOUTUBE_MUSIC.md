# Quick Start: YouTube Music Downloader

## 1-Minute Setup

### Step 1: Get API Key (Choose One)

**Option A: Pixabay (FREE)**
```
1. Visit: https://pixabay.com/accounts/register/
2. Sign up for free account
3. Get API key from: https://pixabay.com/api/docs/
4. Copy your API key
```

**Option B: Epidemic Sound (Premium Quality)**
```
1. Subscribe at: https://www.epidemicsound.com/
2. Get API key from: https://www.epidemicsound.com/api/
3. Copy your API key
```

### Step 2: Set Environment Variable

**Windows (Command Prompt):**
```cmd
set PIXABAY_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:PIXABAY_API_KEY="your_api_key_here"
```

**Linux/Mac:**
```bash
export PIXABAY_API_KEY=your_api_key_here
```

### Step 3: Download Music

**Download 20 tracks (10 calm + 10 energetic):**
```bash
python download_youtube_music.py --count 10
```

**That's it!** Music will be in:
```
background_music_epidemic/youtube/calm/
background_music_epidemic/youtube/energetic/
```

## Common Commands

### Download More Calm Tracks
```bash
python download_youtube_music.py --count 15 --category calm
```

### Download More Energetic Tracks
```bash
python download_youtube_music.py --count 15 --category energetic
```

### Download Without Fallback (Epidemic Only)
```bash
python download_youtube_music.py --count 10 --no-fallback
```

## What You Get

### Calm Category (60-80 BPM)
- Ambient, corporate, cinematic
- Perfect for: intros, tutorials, conclusions
- Peaceful and minimal

### Energetic Category (120-140 BPM)
- Electronic, upbeat, inspiring
- Perfect for: main content, demos, CTAs
- Uplifting and futuristic

## File Format

```
ambient_calm_70bpm_305s_track123.mp3
└─┬──┘ └─┬─┘ └┬┘    └┬┘     └──┬──┘
  │     │    │      │         Track ID
  │     │    │      Duration (seconds)
  │     │    BPM
  │     Mood
  Genre
```

## Use in Your Videos

### For 15-minute video:

```
├─ 0:00-5:00   → calm track (intro)
├─ 5:00-10:00  → energetic track (main)
└─ 10:00-15:00 → calm track (outro)
```

### Mix at 15% volume:

```python
from pydub import AudioSegment

music = AudioSegment.from_mp3("calm_track.mp3")
music = music - 16  # Reduce to 15% volume
```

## Troubleshooting

### "No API key found"
→ Set environment variable (see Step 2)

### "Download failed"
→ Check internet connection
→ Verify API key is correct
→ Try again (script resumes automatically)

### "No tracks found"
→ API might be rate-limited
→ Wait a few minutes and retry

## Next Steps

1. **See full guide:** `YOUTUBE_MUSIC_GUIDE.md`
2. **View downloaded tracks:** `background_music_epidemic/youtube/`
3. **Check metadata:** `background_music_epidemic/youtube/metadata/`

## Pro Tips

- Download 20-30 tracks for variety
- Keep metadata files for reference
- Use calm tracks for 70% of tutorial videos
- Use energetic tracks for 70% of promotional videos
- Always start and end with calm tracks

---

**Need Help?** See `YOUTUBE_MUSIC_GUIDE.md` for detailed documentation.
