# Run Image-Focused 30-Second Video

## What This Does (NEW APPROACH)

✅ **30-second snippet** from much longer script (slow paced)
✅ **Mostly images**: Flux 2 + Nano Banana infographics
✅ **ONE animation video** (WAN 2.5 test only)
✅ **15% background music** throughout (never changes)
✅ **Properly synced subtitles** with narration
✅ **Perfect timing** - everything lines up

---

## The Structure

```
0-5 seconds:   Intro + Image 1 (AI Transformation)
               Narration: "Artificial intelligence is transforming..."

5-13 seconds:  ChatGPT + Infographic (Nano Banana)
               Narration: "ChatGPT helps you write better..."

13-20 seconds: Midjourney + Image 2
               Narration: "Midjourney creates beautiful images..."

20-30 seconds: Closing + WAN 2.5 Test Video
               Narration: "These tools are changing everything"

Background:    15% music (constant throughout all 30 seconds)
```

---

## Run It

```bash
cd /d/workspace/VideoGen_YouTube

python create_30sec_image_focused_video.py
```

**Time:** 20-30 minutes
**Cost:** ~$1.00 (2 Flux images + 1 Nano Banana + 1 WAN video)

---

## What Gets Generated

### Images
- `image_1_ai_transformation.jpg` (Flux 2)
- `image_2_chatgpt_infographic.jpg` (Nano Banana - clean infographic)
- `image_3_midjourney.jpg` (Flux 2)

### Video
- `animation_01_wan_test.mp4` (WAN 2.5, 5 seconds, for testing)

### Audio
- `narration_30sec.mp3` (ElevenLabs, exactly 30 seconds)
- `subtitles_30sec.srt` (perfectly synced, 4 blocks)

### Final Output
- **`video_30sec_final.mp4`** (YouTube-ready, 4-5 MB)

---

## Key Differences From Before

### OLD Approach (Wrong)
❌ 8 animations/videos
❌ Individual background music per video
❌ Rushed pacing
❌ Subtitles not synced
❌ Audio didn't match video

### NEW Approach (Right)
✅ Mostly IMAGES (cheaper, faster)
✅ ONE test video (WAN 2.5)
✅ 15% background music ONLY (continuous, never changes)
✅ Slow, proper pacing
✅ Manually timed subtitles (perfect sync)
✅ Everything aligned correctly

---

## Timing Breakdown

```
Narration (30 seconds total):
  0-5s:   "Artificial intelligence is transforming..."
  5-13s:  "ChatGPT helps you write better..."
  13-20s: "Midjourney creates beautiful images..."
  20-30s: "These tools are changing everything"

Subtitles (synced to narration):
  00:00 --> 00:05 (intro)
  00:05 --> 00:13 (chatgpt)
  00:13 --> 00:20 (midjourney)
  00:20 --> 00:30 (closing)

Images (displayed during narration):
  0-5s:   Image 1 (AI Transformation)
  5-13s:  Image 2 (ChatGPT Infographic)
  13-20s: Image 3 (Midjourney)
  20-30s: WAN Video (+ Image 3 continues)

Background Music (15% volume):
  0-30s:  Continuous, never changes
```

---

## Audio Mix

```
Narration Audio: 100% volume (clear, prominent)
Background Music: 15% volume (subtle, underneath)

Result: You hear narration clearly, music is just background
```

---

## Verify The Video

After running, watch it:

```bash
ffplay output/video_30sec_final.mp4
```

Check:
✓ Narration is clear and 30 seconds
✓ Images display during correct narration sections
✓ Subtitles appear and match narration exactly
✓ Background music at 15% (quiet)
✓ WAN video appears at 20-30 second mark
✓ Everything is in sync

---

## Cost Breakdown

| Component | Cost |
|-----------|------|
| 2x Flux 2 images | $0.20 |
| 1x Nano Banana infographic | $0.08 |
| 1x WAN 2.5 video (5 sec) | $0.25 |
| Narration (ElevenLabs) | $0.03 |
| Subtitles (AssemblyAI) | $0.01 |
| **Total** | **$0.57** |

(Much cheaper than before!)

---

## What's Different

### No Per-Video Music
Before: Each video had its own background music
Now: ONE 15% background music for entire 30 seconds

### Proper Pacing
Before: Rushed (5.5 words/second)
Now: Slow (3 words/second) - easier to read

### Real Subtitles
Before: Attempted auto-generation, didn't sync
Now: Manually timed, perfect sync guaranteed

### Image-First Approach
Before: Animation videos first
Now: Images first, videos only as test

---

## Requirements

Environment variables:
```bash
export ELEVENLABS_API_KEY="your_key"
export FAL_API_KEY="your_key"
export ASSEMBLYAI_API_KEY="your_key"  # Optional
```

Tools needed:
- ffmpeg (for encoding)
- ffprobe (for verification)
- curl (for downloading)

Python libraries:
```bash
pip install elevenlabs fal-client
```

---

## Next Steps

1. Run the script
2. Watch output video
3. Verify timing and sync
4. If good: modify script for other topics
5. If issues: let me know what's wrong

---

That's it! Much simpler, cheaper, and properly synced.
