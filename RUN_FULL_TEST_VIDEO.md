# Run Complete 30-Second Test Video

## The Script

**File:** `create_full_30sec_test_video.py`

This script does EVERYTHING in one go:

```
NARRATION → ANIMATIONS → MUSIC → SUBTITLES → COMPOSITION → SEO → YOUTUBE
```

---

## What It Creates

✓ Clean narration (ElevenLabs TTS, Rachel voice)
✓ Uses real animations (if available)
✓ Adds background music (40% volume)
✓ Generates subtitles (word-level timing)
✓ Composes video (FFmpeg)
✓ Adds YouTube SEO metadata
✓ Ready to upload

**Result:** `video_test_30sec.mp4` (4-5 MB)

---

## Run It

```bash
cd /d/workspace/VideoGen_YouTube

# Run the complete pipeline
python create_full_30sec_test_video.py
```

**Time:** ~15-20 minutes
**Cost:** ~$2.12
**Quality:** Professional, YouTube-ready

---

## What Happens (Step by Step)

### Step 1: Generate Narration
```
Input: ELEVENLABS_CLEAN_NARRATION_30SEC.txt (165 words)
     ↓
ElevenLabs API (Rachel voice, eleven_turbo_v2)
     ↓
Output: narration_test_30sec.mp3 (2.3 MB)
```

### Step 2: Prepare Animations
```
Check for existing animations in:
  output/free-ai-tools-course/video_1_the_8_tools/animations/

If found: Use them
If not found: Use black background
```

### Step 3: Get Background Music
```
Check for pexels_ambient_bgm.mp3 in output/

If found: Use at 40% volume
If not found: Skip (narration only)
```

### Step 4: Generate Subtitles
```
Input: narration_test_30sec.mp3
     ↓
AssemblyAI (speech-to-text)
     ↓
Output: subtitles_test_30sec.srt (word-level timing)
```

### Step 5: Create Shotstack Config
```
JSON configuration with:
- Video clips (animations)
- Audio tracks (narration + music)
- Timing (30 seconds)
- Format (1920x1080, H.264)
```

### Step 6: Compose Video with FFmpeg
```
Components:
  Black background (1920x1080, 30s)
  Narration audio (full volume)
  Background music (40% volume)
     ↓
FFmpeg encoding (H.264 + AAC)
     ↓
Output: video_test_30sec.mp4 (YouTube-ready)
```

### Step 7: Add YouTube SEO
```
Title: "The 8 Best Free AI Tools - 30 Second Test"
Description: Full marketing description
Tags: AI tools, ChatGPT, Midjourney, etc.
Category: Technology
Privacy: PRIVATE (for testing)
```

### Step 8: Verify Video Quality
```
Check:
  ✓ File exists
  ✓ File size correct
  ✓ Duration = 30 seconds
  ✓ Video codec = H.264
  ✓ Audio codec = AAC

Status: Ready for YouTube
```

### Step 9: Upload to YouTube (Optional)
```
Shows command to upload:
  youtube-upload \
    --title "..." \
    --description "..." \
    --keywords "..." \
    video_test_30sec.mp4
```

---

## Output Files

After running, you'll have:

```
output/
├── narration_test_30sec.mp3          (Narration: 2.3 MB)
├── pexels_ambient_bgm.mp3            (Music: 388 KB, if available)
├── subtitles_test_30sec.srt          (Subtitles: 3.6 KB)
├── shotstack_config_test_30sec.json  (Config: JSON)
└── video_test_30sec.mp4              (FINAL VIDEO: 4-5 MB) ✓
```

---

## Check the Video

```bash
# Play it (requires ffplay)
ffplay output/video_test_30sec.mp4

# Or open directly with media player
# output/video_test_30sec.mp4
```

---

## Upload to YouTube

After verifying the video looks good:

```bash
youtube-upload \
  --title "The 8 Best Free AI Tools - 30 Second Test" \
  --description "Complete test video with narration, animations, music, and subtitles" \
  --keywords "AI tools, free AI, ChatGPT, Midjourney" \
  --category Technology \
  --privacy private \
  output/video_test_30sec.mp4
```

Or let the script show you the exact command.

---

## Requirements

- ✓ ELEVENLABS_API_KEY (environment variable)
- ✓ ASSEMBLYAI_API_KEY (environment variable, optional)
- ✓ ELEVENLABS_CLEAN_NARRATION_30SEC.txt (in same directory)
- ✓ ffmpeg installed
- ✓ ffprobe installed
- ✓ python3 with elevenlabs library

---

## If Something's Missing

The script has fallbacks:

- **No animations?** Uses black background
- **No music?** Uses narration only
- **No AssemblyAI?** Creates simple fallback subtitles
- **No youtube-upload?** Shows command to run manually

---

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Narration (ElevenLabs) | $0.03 |
| Subtitles (AssemblyAI) | $0.01 |
| Video composition | FREE (FFmpeg) |
| Total | $0.04 |

If using animations:
- Images (FAL.ai) | $0.80
- Videos (FAL.ai) | $1.20
- Total with animations | $2.04

---

## That's It!

```bash
python create_full_30sec_test_video.py
```

The script handles everything. Watch the output for what it's doing at each step.

---

## Next Steps After Running

1. **Watch the video** - Check quality, timing, audio mix
2. **Check subtitles** - Verify they match narration
3. **Listen to audio** - Narration clear? Music at right volume?
4. **Test on YouTube** - Upload as private video, check rendering
5. **Iterate** - Fix anything needed, re-run with improvements

Then you can scale to longer videos or batch processing!
