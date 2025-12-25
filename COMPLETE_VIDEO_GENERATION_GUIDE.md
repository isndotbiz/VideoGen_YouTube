# Complete Video Generation Guide

## Overview
This guide covers the entire video generation pipeline including:
- Text-to-video animation generation (FAL.ai)
- Audio/narration mixing
- Subtitle creation and embedding
- SEO optimization

## Quick Start

### Step 1: Generate Text-to-Video Content (FAL.ai)

```bash
python generate-video-falaiv2.py
```

**What it does:**
- Uses FAL.ai's Kling Video model for text-to-video
- Generates 5 animated videos (4-5 seconds each)
- Saves video URLs and metadata

**Video Prompts Generated:**
1. Professional analyst at desk with monitors (5s)
2. Animated bar chart showing ranking factors (4s)
3. Team collaboration scene (4s)
4. Algorithm timeline animation (5s)
5. Hands typing on keyboard (4s)

### Step 2: Download Videos & Prepare Assets

```bash
# Videos are downloaded from FAL.ai URLs
# Audio files available:
# - narration.wav (4.7MB) - Generated narration
# - narration_with_bgm.mp3 (341KB) - Narration + background music
# - placeholder_bgm.mp3 (337KB) - Background music only
```

### Step 3: Add Audio Track to Video

```bash
python add-audio-to-video.py
```

**Output:** `final_video_with_audio.mp4`
- Contains: Video + Narration + Background Music

### Step 4: Add Subtitle Overlays

```bash
python embed_subs_simple.py output/final_video_with_audio.mp4 output/subtitles.srt output/final_video_complete.mp4
```

**Output:** `final_video_complete.mp4`
- Contains: Video + Audio + Visible Subtitles

## Video Assets Workflow

### Image-to-Video Alternative
If you have static images, convert them to video:

```python
from moviepy.editor import ImageClip

# Create 3-5 second video clips from images
clip = ImageClip("image.png").set_duration(4)
clip.write_videofile("output.mp4")
```

### Text-to-Video with FAL.ai

**API Endpoint:** `https://api.falai.ai/text-to-video/submit`

**Parameters:**
```json
{
  "model_name": "kling-video",
  "prompt": "Professional woman at desk analyzing data charts",
  "duration": 5,
  "aspect_ratio": "16:9",
  "negative_prompt": "low quality, blurry, distorted"
}
```

**Supported Durations:** 4, 5, 6 seconds
**Cost:** ~$0.05 per video

## Audio Mixing

### Layer Configuration
```
Video Stream: final_video.mp4
├── Narration (Primary): narration.wav (0dB)
└── Background Music: placeholder_bgm.mp3 (-20dB / quieter)
```

### Audio File Details
- **Narration.wav**: 16-bit mono, 16kHz, ~43 seconds
- **BGM.mp3**: Looped background music, 337KB, ~10 seconds

## Subtitle Management

### SRT Format
```
1
00:00:00,160 --> 00:00:04,940
Claude Code versus Codecs the ultimate Coding duo the game

2
00:00:04,440 --> 00:00:09,660
changing Duo when it comes to coding, many ask Claude
```

### Subtitle Rendering Options

**Option 1: Hardcoded Overlay** (Recommended for YouTube)
```bash
python embed_subs_simple.py video.mp4 subtitles.srt output.mp4
```
- Text appears as overlay on video
- Works on all platforms
- Visible to everyone

**Option 2: SRT Format** (For platforms that support it)
- Keep `.srt` file separate
- Upload separately to YouTube
- Users can toggle on/off

## SEO Optimization

### Video Metadata (YouTube Upload)

```json
{
  "title": "Claude Code vs ChatGPT: Complete Comparison [2025]",
  "description": "In-depth comparison of Claude Code and ChatGPT for developers. Learn the differences, strengths, and best use cases for each AI tool.",
  "keywords": [
    "Claude Code", "ChatGPT", "AI comparison",
    "coding assistant", "LLM", "AI tools",
    "programming", "machine learning"
  ],
  "tags": ["claude", "chatgpt", "ai", "coding", "programming"],
  "category": "Education",
  "language": "English",
  "captions": "en"
}
```

### Video Description Template
```
⏱️ Timestamps:
0:00 - Intro
0:15 - What is Claude Code?
1:30 - What is ChatGPT?
3:00 - Direct Comparison
4:30 - Best Use Cases
5:30 - Conclusion

📚 Resources:
- Claude Code: https://claude.com
- ChatGPT: https://openai.com/chatgpt

🔗 More Videos:
- Next: [Related Video]

❤️ Like, Subscribe, and Comment your thoughts!

#Claude #ChatGPT #AI #Coding #Programming
```

## Complete Pipeline Execution

### Full Workflow Command Sequence

```bash
# 1. Generate text-to-video animations
python generate-video-falaiv2.py

# 2. Download videos from FAL.ai URLs (manual or automated)
# 3. Combine videos in sequence (via Descript or FFmpeg)

# 4. Add audio to combined video
python add-audio-to-video.py

# 5. Add subtitle overlays
python embed_subs_simple.py \
  output/final_video_with_audio.mp4 \
  output/subtitles.srt \
  output/final_video_complete.mp4

# 6. Verify output
ls -lh output/final_video_complete.mp4

# 7. Upload to YouTube with SEO metadata
```

## Quality Checklist

Before uploading to YouTube, verify:

- [x] **Video Duration**: 40-60 seconds (optimal for watch time)
- [x] **Resolution**: 1920x1080 (Full HD)
- [x] **Bitrate**: 8000k (video), 128k (audio)
- [x] **Codec**: H.264 video, AAC audio
- [x] **Frame Rate**: 24-30 FPS
- [x] **Audio**: Clear narration + background music
- [x] **Subtitles**: Visible and accurate
- [x] **Content**: Animations + text-to-video + static images
- [x] **Thumbnail**: Custom 1280x720 image

## Troubleshooting

### No Sound in Video
```bash
# Check audio file exists and is valid
ffmpeg -i output/narration_with_bgm.mp3

# If using wrong audio file:
python add-audio-to-video.py  # Will use narration_with_bgm.mp3
```

### Subtitles Not Visible
```bash
# Use embed_subs_simple.py instead of other methods
python embed_subs_simple.py input.mp4 subtitles.srt output.mp4
```

### Text-to-Video Not Working
```bash
# Check FAL_API_KEY in .env
# Verify API quota hasn't been exceeded
# Try alternative: Use Runway ML or Stability AI
```

### Video Quality Issues
```bash
# Re-encode with higher bitrate
ffmpeg -i input.mp4 -b:v 10000k output.mp4

# Or use Handbrake GUI for optimization
```

## Cost Breakdown (Per Video)

| Service | Service | Cost | Notes |
|---------|---------|------|-------|
| FAL.ai Text-to-Video | 5 clips × $0.05 | $0.25 | High quality animations |
| ElevenLabs Narration | ~43s @ $0.00030/char | $0.02 | Voice synthesis |
| AssemblyAI Subtitles | 43s audio | $0.04 | Transcription |
| **TOTAL** | | **$0.31** | Per complete video |

## Advanced: Batch Video Generation

```bash
# Generate 5 videos in parallel
for topic in "Claude vs ChatGPT" "Claude for Coding" "Free AI Tools"; do
  node batch-video-generator.js --topic="$topic" --parallel &
done
```

## Resources

- **FAL.ai Docs**: https://www.fal.ai/models/kling-video/text-to-video
- **Subtitle Formats**: https://en.wikipedia.org/wiki/.srt
- **YouTube SEO Guide**: https://support.google.com/youtube/answer/7239739
- **Video Encoding Guide**: https://trac.ffmpeg.org/wiki/Encode/H.264

---

Generated: 2025-12-13
Status: Production Ready
