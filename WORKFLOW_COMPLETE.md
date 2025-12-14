# VideoGen YouTube - Complete Workflow

## Overview
This is a complete AI-powered video generation pipeline for YouTube using multiple APIs.

## Workflow Stages

### Stage 1: Script & Narration Generation
**Tools Used:**
- ElevenLabs API: Text-to-speech narration generation
- Input: Video script (text)
- Output: High-quality MP3 narration (2.3MB)
- Status: ✓ COMPLETE

**Files:**
- `elevenlabs_narration_WORKING.py` - Generates professional narration
- Output: `output/free-ai-tools-course/video_1_the_8_tools/narration.mp3`

### Stage 2: Subtitle Generation
**Option A: Assembly AI (Recommended)**
- Uses speech-to-text on narration to generate accurate subtitles
- Converts to SRT format automatically
- Script: `get_subtitles_assembly.py`
- Command: `python get_subtitles_assembly.py`

**Option B: Pre-generated (Already done)**
- SRT file exists: `output/free-ai-tools-course/video_1_the_8_tools/subtitles.srt`
- Status: ✓ COMPLETE

### Stage 3: Background Music
**Option A: Pexels API (Recommended)**
- Fetches royalty-free background music from Pexels
- Script: `fetch_pexels_music.py`
- Command: `python fetch_pexels_music.py`
- Output: `output/pexels_ambient_bgm.mp3`

**Option B: Placeholder (Already done)**
- Fallback music: `output/placeholder_bgm.mp3`
- Status: ✓ READY

### Stage 4: Video Base Creation (THIS STAGE)
**What it does:**
1. Create a solid-color video (1920x1080, dark blue-gray background)
2. Mix narration + background music (15% volume)
3. Combine video and audio into MP4
4. Apply optional subtitles

**Tools Used:**
- OpenCV (cv2): Video frame creation
- pydub or ffmpeg: Audio mixing
- ffmpeg: Final video composition

**Script:** `compose_with_opencv.py`
**Command:** `python compose_with_opencv.py`
**Output:** `output/free-ai-tools-course/video_1_the_8_tools/video_1_COMPLETE.mp4`

**What is MoviePy?**
- MoviePy is a Python library for video editing/composition
- It wraps FFmpeg and provides high-level Python APIs
- Alternative to OpenCV for video generation
- Has import issues in this environment, so using OpenCV instead

### Stage 5: Animation Generation
**Tool:** FAL.ai WAN-25 Image-to-Video

**Process:**
1. Generate image with Flux model from text prompt
2. Convert image to 4-second video animation with WAN-25
3. Download and save animation clip

**Scripts:**
- `generate_animations_with_fal.py` - Main animation generator
- Uses FAL_KEY environment variable (automatically set)
- Generates 8 animations (1 for each AI tool)

**Command:** `python generate_animations_with_fal.py`
**Output:** 8 MP4 files in `output/free-ai-tools-course/video_1_the_8_tools/animations/`
**Duration:** ~20-30 minutes total (2-3 minutes per animation)

### Stage 6: Video Composition with Animations
**Process:**
1. Load base video (from Stage 4)
2. Load 8 animation clips
3. Position animations at specific timestamps
4. Add subtitles as text overlays
5. Export final video

**Tools:** OpenCV + FFmpeg

### Stage 7: Platform-Specific Versions
**Creates optimized versions for:**
- YouTube: 16:9 aspect ratio (1920x1080)
- TikTok: 9:16 aspect ratio (1080x1920)
- Instagram Reels: 9:16 aspect ratio with padding
- Twitter/X: 16:9 aspect ratio

**Script:** `multi_platform_generator.py`

### Stage 8: Upload
**Platform:** YouTube
**Requirements:**
- YouTube API credentials
- Video title, description, tags
- Thumbnail image

## API Integration

### Configured APIs (22 total):
1. **ElevenLabs** - Text-to-speech narration ✓ ACTIVE
2. **Assembly AI** - Speech-to-text for subtitles ✓ ACTIVE
3. **Pexels** - Royalty-free music/videos ✓ ACTIVE
4. **FAL.ai** - Image generation (Flux) & video generation (WAN-25) ✓ ACTIVE
5. **Replicate** - Alternative AI model API ✓ ACTIVE
6. **Runway ML** - Video generation alternative ✓ ACTIVE
7. **OpenAI** - Text generation & image generation ✓ ACTIVE
8. And 15+ more APIs configured in `config.py`

All API keys stored in `.env` file and accessible via `config.py`.

## Status & Next Steps

### Current Status:
- [x] Narration generated with ElevenLabs
- [x] Subtitles created (SRT format)
- [x] Background music available
- [ ] Base video creation (IN PROGRESS)
- [ ] Animations generation (PENDING)
- [ ] Final composition with subtitles & animations (PENDING)
- [ ] Platform-specific versions (PENDING)

### Next Command:
```bash
python compose_with_opencv.py
```

This will create the base video with narration and background music (15% volume).

### Then:
```bash
python generate_animations_with_fal.py
```

This will generate the 8 AI tool animations using FAL.ai.

### Finally:
```bash
python compose_final_video_with_animations.py
```

This will combine everything into the final video with subtitles and animations.

## Architecture

```
Video Generation Pipeline
│
├─ Stage 1: Narration (ElevenLabs)
│  └─ Output: narration.mp3
│
├─ Stage 2: Subtitles (Assembly AI)
│  └─ Output: subtitles.srt
│
├─ Stage 3: Background Music (Pexels)
│  └─ Output: bgm.mp3
│
├─ Stage 4: Base Video (OpenCV + ffmpeg)
│  └─ Output: video_base.mp4 (narration + BGM + color background)
│
├─ Stage 5: Animations (FAL.ai)
│  ├─ 1. ChatGPT Interface
│  ├─ 2. Midjourney Grid
│  ├─ 3. ElevenLabs Voice
│  ├─ 4. Claude Analysis
│  ├─ 5. Synthesys Avatar
│  ├─ 6. Runway Editing
│  ├─ 7. Zapier Workflow
│  └─ 8. CapCut Editing
│
├─ Stage 6: Composition (OpenCV + FFmpeg)
│  └─ Output: video_1_COMPLETE.mp4 (base + animations + subtitles)
│
├─ Stage 7: Platform Optimization
│  ├─ YouTube: video_1_youtube.mp4
│  ├─ TikTok: video_1_tiktok.mp4
│  ├─ Instagram: video_1_instagram.mp4
│  └─ Twitter: video_1_twitter.mp4
│
└─ Stage 8: Upload
   └─ YouTube, TikTok, Instagram, Twitter
```

## Running the Full Pipeline

```bash
# Stage 1: Generate Narration (already done)
# python elevenlabs_narration_WORKING.py

# Stage 2: Get Subtitles from Assembly AI
python get_subtitles_assembly.py

# Stage 3: Fetch Background Music
python fetch_pexels_music.py

# Stage 4: Create Base Video
python compose_with_opencv.py

# Stage 5: Generate 8 Animations (20-30 minutes)
python generate_animations_with_fal.py

# Stage 6: Compose Final Video with Animations
# python compose_final_video_with_animations.py

# Stage 7: Create Platform Versions
# python multi_platform_generator.py output/free-ai-tools-course/video_1_the_8_tools/video_1_COMPLETE.mp4

# Stage 8: Upload to YouTube
# python upload_to_youtube.py
```

## Files & Locations

### Input Files:
- Scripts: `*.py` in project root
- Config: `.env` (API keys), `config.py` (API loader)

### Output Directory:
```
output/
└─ free-ai-tools-course/
   └─ video_1_the_8_tools/
      ├─ narration.mp3 (2.3 MB)
      ├─ subtitles.srt
      ├─ subtitles_assembly.srt (optional, from Assembly AI)
      ├─ video_1_COMPLETE.mp4 (final video)
      ├─ animations/
      │  ├─ animation_01_chatgpt_interface.mp4
      │  ├─ animation_02_midjourney_image_grid.mp4
      │  ├─ ... (8 total)
      │  └─ animation_08_capcut_editing.mp4
      └─ versions/
         ├─ video_1_youtube.mp4
         ├─ video_1_tiktok.mp4
         ├─ video_1_instagram.mp4
         └─ video_1_twitter.mp4
```

## Troubleshooting

### Issue: MoviePy import error
**Solution:** Use OpenCV approach instead (done)

### Issue: FFmpeg not found
**Solution:** Install FFmpeg
```
# Windows (Chocolatey):
choco install ffmpeg

# Windows (manual): Download from https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

### Issue: API key errors
**Solution:** Check `.env` file has correct keys and `config.py` can load them

### Issue: Audio mixing failing
**Solution:** Install pydub and ffmpeg
```
pip install pydub
```

## Performance

- Narration generation: 30 seconds
- Subtitle generation: 1-2 minutes
- Base video creation: 2-3 minutes
- Animation generation: 2-3 minutes each (20-30 minutes total for 8)
- Final composition: 5-10 minutes
- Total time: 30-60 minutes for complete video

## Quality Settings

- Resolution: 1920x1080 (Full HD)
- FPS: 24 (suitable for online video)
- Video codec: H.264 (libx264)
- Audio codec: AAC
- Audio bitrate: 128k
- Video bitrate: Variable (set by ffmpeg)
- Format: MP4 (H.264 + AAC)
