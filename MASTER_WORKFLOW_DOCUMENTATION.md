# VideoGen YouTube - Master Workflow Documentation

## System Overview

This is a complete AI-powered video generation pipeline with 9 distinct stages. Each stage is independent but feeds into the next. The system uses 10+ APIs plus local GPU capability to create fully automated, professional YouTube videos.

---

## STAGE 1: RESEARCH & WEB SCRAPING
**Purpose:** Gather authoritative information about the topic

### Inputs:
- Topic/URL to create video about

### Process:
1. **Primary Source (Firecrawl):**
   - Use Firecrawl API to scrape website content
   - Crawl all relevant pages about the topic
   - Extract text, headings, structure

2. **Output Format:**
   - Save as JSONL file (one JSON object per line)
   - Each object: `{url, title, content, metadata}`
   - File location: `research/[topic]/crawled_data.jsonl`

3. **Secondary Research (Manual):**
   - Find 3 additional trusted sources on topic
   - Add their URLs and key info to research file
   - Curate high-quality, authoritative information

### Output:
- `research/[topic]/crawled_data.jsonl` - Raw scraped content
- `research/[topic]/sources.txt` - List of 4 sources used

### Status in System:
- ✓ Firecrawl API configured
- Check `.env` for `FIRECRAWL_API_KEY`

---

## STAGE 2: SCRIPT GENERATION
**Purpose:** Create a professional video script optimized for text-to-speech

### Inputs:
- JSONL file from Stage 1 (research data)
- Topic name

### Process:
1. **LLM Script Writing (Claude):**
   - Read JSONL research data
   - Generate natural, conversational script
   - ~3-5 minutes duration (~600-1000 words)
   - Structure with clear sections

2. **ElevenLabs Optimization:**
   - Format script for text-to-speech reading
   - **IMPORTANT:** Use timing markers instead of spoken instructions
   - Example format:
     ```
     "Welcome to our video. [PAUSE:2000ms]

     Here's the first point: This is the content...

     [PAUSE:1500ms]

     Now let's discuss the next topic..."
     ```
   - DO NOT include: "pause for 2 seconds", "read this slowly", etc.
   - ElevenLabs reads everything literally

3. **Metadata in Script:**
   - Add visual cues as comments:
     ```
     <!-- Show infographic of X here -->
     <!-- Transition to animation Y -->
     ```

### Output:
- `scripts/[topic]/script_final.txt` - Optimized script
- Duration estimate in metadata

### Status in System:
- ✓ Claude API configured for script generation
- Ready to use

---

## STAGE 3: COLOR PALETTE & DESIGN SYSTEM
**Purpose:** Create consistent, accessible visual design

### Process:
1. **Generate 5-Color Palette:**
   - Primary color (main brand color)
   - Secondary color (accents)
   - Tertiary color (additional elements)
   - Background color (usually dark for video)
   - Text/Accent color (usually white/light)

2. **WCAG Compliance:**
   - Ensure minimum contrast ratio of 4.5:1 for text
   - Use color blindness simulator to test
   - Verify readability on all colors
   - Document accessibility decisions

3. **Color Definition:**
   - HEX codes for all 5 colors
   - RGB values for design tools
   - Usage guidelines for each

### Output:
- `design/[topic]/color_palette.json`:
  ```json
  {
    "primary": "#1e3c72",
    "secondary": "#ff6b35",
    "tertiary": "#4ecdc4",
    "background": "#0a0e27",
    "text": "#ffffff",
    "wcag_checked": true
  }
  ```

### Status in System:
- ✓ Manual process, use online tools like Coolors.co
- ✓ Check WCAG with WebAIM Contrast Checker

---

## STAGE 4: IMAGE & INFOGRAPHIC GENERATION
**Purpose:** Create visual elements for the video

### Inputs:
- Script (from Stage 2)
- Color palette (from Stage 3)

### Process:
1. **Identify Visual Moments:**
   - Read script
   - Mark where visuals would help
   - List required images/infographics

2. **Generate Infographics:**
   - **Primary:** FAL.ai Nano Banana API
   - Input: Text description of infographic
   - Output: PNG/SVG infographic
   - Example: "Create infographic showing 5 benefits of X with color palette #1e3c72, #ff6b35..."

3. **Generate Beautiful Images:**
   - **Primary:** FAL.ai Flux Dev model
   - Input: Detailed visual prompt
   - Output: High-quality image
   - Example: "Professional photo of X, vibrant colors, 4K quality..."

4. **Local Alternative (Optional):**
   - Use local Comfy Flux server (3090 GPU)
   - For more control over image generation
   - Better quality than online APIs
   - Check `.env` for `COMFY_GPU_ENDPOINT`

5. **Backup Option:**
   - Replicate API if FAL.ai fails
   - Same models, different API

### Outputs:
- `assets/[topic]/images/image_01.png` - Generated image
- `assets/[topic]/infographics/infographic_01.png` - Generated infographic
- `assets/[topic]/metadata.json` - List of all images with prompts

### Required APIs:
- ✓ FAL_API_KEY (primary)
- ✓ REPLICATE_API_KEY (backup)
- Optional: Local Comfy with GPU

---

## STAGE 5: ANIMATION & VIDEO CLIP GENERATION
**Purpose:** Create short animated videos from static images

### Inputs:
- Static images from Stage 4
- Script timing from Stage 2

### Process:
1. **Image-to-Video Conversion:**
   - **Tool:** FAL.ai WAN 2.5 model
   - Input: Static image + motion prompt
   - Output: 4-second video clip with motion
   - Example prompt: "Camera slowly pans across the infographic, highlighting key points"

2. **Animation Settings:**
   - Duration: 4 seconds per clip
   - Aspect ratio: 16:9
   - Quality: 1080p

3. **Workflow:**
   - For each image that needs animation:
     - Write motion description
     - Call WAN 2.5 API
     - Download generated video
     - Save with metadata

### Outputs:
- `assets/[topic]/animations/animation_01.mp4` - 4-sec video
- `assets/[topic]/animations/animation_02.mp4` - 4-sec video
- etc.

### Time Estimate:
- 2-3 minutes per animation
- For 8 animations: 20-30 minutes total

### Required APIs:
- ✓ FAL_API_KEY (WAN 2.5 model)
- Backup: Replicate API

---

## STAGE 6: NARRATION GENERATION
**Purpose:** Create professional audio narration from script

### Inputs:
- Script from Stage 2 (with [PAUSE] markers)

### Process:
1. **Text Cleaning:**
   - Replace [PAUSE:XXXms] with actual silence in output
   - Remove visual cues/comments
   - Keep only spoken text

2. **ElevenLabs Text-to-Speech:**
   - API: `ELEVENLABS_API_KEY`
   - Voice: Rachel (professional, clear)
   - Settings:
     - Stability: 0.5
     - Similarity boost: 0.75
   - Output: MP3 file

3. **Quality Check:**
   - Verify duration matches script estimate
   - Listen for clarity
   - Check pronunciation of technical terms

### Output:
- `audio/[topic]/narration.mp3` (typically 2-3 MB for 3-5 min video)

### Time Estimate:
- 30 seconds API call + download

### Required API:
- ✓ ELEVENLABS_API_KEY (with sufficient credits)

---

## STAGE 7: BACKGROUND MUSIC & AUDIO MIXING
**Purpose:** Find royalty-free music and mix with narration

### Inputs:
- Narration from Stage 6
- Topic/mood description

### Process:
1. **Fetch Background Music:**
   - **Tool:** Pexels API
   - Search query: Topic-related ambient/background music
   - Download: Royalty-free music clip

2. **Audio Mixing:**
   - Narration: 100% volume (primary)
   - Background Music: 15% volume (subtle background)
   - Tool: pydub library or ffmpeg
   - Output: Mixed MP3 file

3. **Mixing Process:**
   - Load narration
   - Load background music
   - Reduce BGM to 15% volume (-16dB)
   - Loop BGM if shorter than narration
   - Overlay and export

### Output:
- `audio/[topic]/background_music.mp3` - Original music
- `audio/[topic]/mixed_audio.mp3` - Narration + BGM (15%)

### Time Estimate:
- 1 minute for Pexels fetch
- 1 minute for mixing

### Required API:
- ✓ PEXELS_API_KEY

### Backup:
- Placeholder music included in project
- Or generate music with Replicate API

---

## STAGE 8: SUBTITLE GENERATION
**Purpose:** Create synchronized subtitles from narration

### Inputs:
- Narration MP3 from Stage 6

### Process:
1. **Speech-to-Text Conversion:**
   - **Tool:** Assembly AI API
   - Upload: Narration MP3
   - Request: Word-level timing data
   - Output: Transcript with timestamps

2. **SRT File Creation:**
   - Convert transcript to SRT format
   - Group words into readable chunks (~10 words per subtitle)
   - Format: `index\nHH:MM:SS,mmm --> HH:MM:SS,mmm\ntext`
   - Example:
     ```
     1
     00:00:00,000 --> 00:00:05,000
     Welcome to our video about the topic

     2
     00:00:05,000 --> 00:00:10,000
     We'll explore five important points
     ```

### Output:
- `subtitles/[topic]/subtitles.srt` - SRT subtitle file

### Time Estimate:
- 1-2 minutes for API processing

### Required API:
- ✓ ASSEMBLYAI_API_KEY

---

## STAGE 9: VIDEO COMPOSITION & STITCHING
**Purpose:** Combine all elements into final video

### Inputs:
- Narration + BGM audio (Stage 7)
- Images & infographics (Stage 4)
- Animation clips (Stage 5)
- Subtitles (Stage 8)
- Color palette (Stage 3)

### Process:
1. **Base Video Creation:**
   - Tool: OpenCV (cv2) or FFmpeg
   - Create 1920x1080 video at 24 FPS
   - Duration: Match audio duration
   - Background: Use primary color from palette

2. **Layering (in order):**
   - Layer 1: Colored background video
   - Layer 2: Static images (timed to script)
   - Layer 3: Animation clips (timed to script)
   - Layer 4: Text overlays (subtitles)
   - Layer 5: Title card (first 2 seconds)

3. **Audio Insertion:**
   - Tool: FFmpeg command line
   - Mix: Mixed audio from Stage 7
   - Codec: AAC at 128kbps

4. **Stitching Tool - PRIMARY:**
   - **ShortStack API** (`SHORTSTACK_API_KEY`)
   - Automates composition
   - Takes all elements and outputs MP4

5. **Stitching Tool - BACKUP:**
   - **FFmpeg** (command line)
   - Manual stitching if ShortStack fails
   - Requires complex filter chains

### Output:
- `video/[topic]/video_COMPLETE.mp4` - Final video
- Specifications:
  - Resolution: 1920x1080 (Full HD)
  - Codec: H.264 (libx264)
  - Audio: AAC, 128kbps
  - FPS: 24
  - Format: MP4

### Time Estimate:
- 5-15 minutes depending on composition complexity

### Required APIs:
- ✓ SHORTSTACK_API_KEY (primary)
- ✓ FFmpeg installed (backup)
- Replicate API (if needed)

---

## STAGE 10: PLATFORM OPTIMIZATION (OPTIONAL)
**Purpose:** Create versions for different social platforms

### Outputs:
- **YouTube:** 16:9 aspect ratio (1920x1080)
- **TikTok:** 9:16 aspect ratio (1080x1920)
- **Instagram Reels:** 9:16 with safe area padding
- **Twitter/X:** 16:9 aspect ratio (1280x720)

### Tool:
- FFmpeg video scaling
- Or ShortStack API

---

## STAGE 11: CLOUD STORAGE (OPTIONAL)
**Purpose:** Store all files in cloud for backup/sharing

### Tool:
- **AWS S3 Bucket**
- Store:
  - Final video
  - Animation clips
  - Images
  - Audio files
  - Subtitles

### Configuration:
- Check `.env` for AWS credentials
- Bucket name: `videogen-assets`

---

## API CONFIGURATION REFERENCE

### All Available APIs (from .env):
```
PRIMARY (ACTIVELY USED):
1. ELEVENLABS_API_KEY       → Text-to-speech narration
2. FAL_API_KEY              → Image generation (Flux), Animation (WAN 2.5)
3. ASSEMBLYAI_API_KEY       → Subtitle generation (speech-to-text)
4. PEXELS_API_KEY           → Royalty-free music/videos
5. SHORTSTACK_API_KEY       → Video composition/stitching
6. FIRECRAWL_API_KEY        → Web scraping

BACKUP/ALTERNATIVE:
7. REPLICATE_API_KEY        → Alternative image/animation generation
8. OPENAI_API_KEY           → Script writing, backup TTS
9. ANTHROPIC_API_KEY        → Script writing (Claude)
10. BRAVE_API_KEY           → Search capability
11. RUNWAY_API_KEY          → Video generation alternative
12. AWS_ACCESS_KEY_ID       → Cloud storage
13. AWS_SECRET_ACCESS_KEY   → Cloud storage
14. DESCRIPT_API_KEY        → Video editing/captioning alternative
15. SQUADBOX_API_KEY        → Content moderation/feedback

LOCAL:
16. COMFY_GPU_ENDPOINT      → Local GPU (3090) for Flux
17. FFmpeg (system)         → Video composition fallback
```

---

## COMPLETE WORKFLOW SEQUENCE

### Command Execution Order:
```bash
# 1. Web Scraping & Research
python firecrawl_scraper.py --topic "your-topic"
# Output: research/[topic]/crawled_data.jsonl

# 2. Generate Script
python generate_script.py --topic "your-topic" --research research/[topic]/crawled_data.jsonl
# Output: scripts/[topic]/script_final.txt

# 3. Design Color Palette
python create_color_palette.py --topic "your-topic"
# Output: design/[topic]/color_palette.json

# 4. Generate Images & Infographics
python generate_images.py --script scripts/[topic]/script_final.txt --colors design/[topic]/color_palette.json
# Output: assets/[topic]/images/*.png, assets/[topic]/infographics/*.png

# 5. Create Animations
python generate_animations.py --images assets/[topic]/images/ --script scripts/[topic]/script_final.txt
# Output: assets/[topic]/animations/*.mp4
# Time: 20-30 minutes

# 6. Generate Narration
python generate_narration.py --script scripts/[topic]/script_final.txt
# Output: audio/[topic]/narration.mp3

# 7. Mix Audio (Narration + Background Music at 15%)
python mix_audio.py --narration audio/[topic]/narration.mp3 --topic "your-topic"
# Output: audio/[topic]/mixed_audio.mp3

# 8. Generate Subtitles
python generate_subtitles.py --narration audio/[topic]/narration.mp3
# Output: subtitles/[topic]/subtitles.srt

# 9. Compose Final Video
python compose_video.py \
  --images assets/[topic]/images/ \
  --animations assets/[topic]/animations/ \
  --audio audio/[topic]/mixed_audio.mp3 \
  --subtitles subtitles/[topic]/subtitles.srt \
  --colors design/[topic]/color_palette.json \
  --script scripts/[topic]/script_final.txt
# Output: video/[topic]/video_COMPLETE.mp4
# Time: 5-15 minutes

# 10. (Optional) Create Platform Versions
python create_platform_versions.py --video video/[topic]/video_COMPLETE.mp4
# Output: video/[topic]/platforms/*.mp4

# TOTAL TIME: 30-60 minutes for complete video (minus animations: 10-15 min)
```

---

## FILE STRUCTURE
```
project/
├── .env                                 # API keys
├── config.py                           # API configuration loader
├── scripts/
│   └── [topic]/
│       ├── script_final.txt            # Generated script with timing
│       └── metadata.json
├── research/
│   └── [topic]/
│       ├── crawled_data.jsonl          # Firecrawl output
│       └── sources.txt                 # 4 source URLs
├── design/
│   └── [topic]/
│       └── color_palette.json          # 5 colors + WCAG compliance
├── assets/
│   └── [topic]/
│       ├── images/                     # Generated images from Flux
│       ├── infographics/               # Generated from Nano Banana
│       ├── animations/                 # 4-sec clips from WAN 2.5
│       └── metadata.json
├── audio/
│   └── [topic]/
│       ├── narration.mp3               # ElevenLabs output
│       ├── background_music.mp3        # Pexels download
│       └── mixed_audio.mp3             # 15% BGM + narration
├── subtitles/
│   └── [topic]/
│       └── subtitles.srt               # Assembly AI output
├── video/
│   └── [topic]/
│       ├── video_COMPLETE.mp4          # Final video (ShortStack)
│       └── platforms/
│           ├── video_youtube.mp4       # 16:9
│           ├── video_tiktok.mp4        # 9:16
│           └── video_instagram.mp4     # 9:16
└── *.py                                # All Python scripts
```

---

## KEY PARAMETERS & SETTINGS

### Video Specifications:
- Resolution: 1920x1080 (Full HD)
- Frame Rate: 24 FPS
- Duration: 3-5 minutes (typical)
- Format: MP4 (H.264 + AAC)

### Audio Specifications:
- Narration: 100% volume (primary)
- Background Music: 15% volume (0.15 multiplier or -16dB)
- Audio Codec: AAC
- Sample Rate: 44100 Hz
- Bitrate: 128 kbps

### Image Specifications:
- Resolution: 1920x1080 minimum
- Format: PNG for transparency, JPG for photos
- Color Space: RGB
- Aspect Ratio: 16:9 preferred

### Animation Specifications:
- Duration: 4 seconds per clip
- Aspect Ratio: 16:9
- Codec: H.264
- Resolution: 1080p minimum

### Script Specifications:
- Duration: 3-5 minutes = 600-1000 words
- Pacing: 120 words per minute (conversational)
- Timing Markers: [PAUSE:XXXms] format
- Visual Cues: <!-- comment --> format

### Color Palette:
- 5 colors total
- WCAG AA contrast minimum 4.5:1 for text
- Test with WebAIM Contrast Checker

---

## TROUBLESHOOTING QUICK REFERENCE

| Problem | Solution |
|---------|----------|
| ElevenLabs reads "pause" as word | Use [PAUSE:2000ms] format instead |
| Subtitles out of sync | Verify narration duration matches script |
| Images not matching color palette | Regenerate with explicit color codes in prompt |
| Audio distorted | Check mixing levels, ensure normalization |
| Video composition fails | Verify all input files exist and formats correct |
| FAL.ai API timeout | Use local Comfy Flux or Replicate API |
| ShortStack stitching slow | Break video into shorter segments |
| WCAG compliance failed | Increase contrast or change colors |

---

## SUCCESS CRITERIA FOR EACH STAGE

✓ **Stage 1:** JSONL file with scraped content + 3 source URLs
✓ **Stage 2:** Script with [PAUSE] markers, ~600-1000 words, 3-5 min read time
✓ **Stage 3:** JSON with 5 colors, all verified for WCAG AA compliance
✓ **Stage 4:** 5-10 high-quality PNG images + 3-5 infographics
✓ **Stage 5:** 4-8 animation clips, each 4 seconds, smooth motion
✓ **Stage 6:** Clear MP3 narration, professional quality
✓ **Stage 7:** Mixed audio with discernible narration + subtle BGM
✓ **Stage 8:** SRT file with properly timed, readable subtitles
✓ **Stage 9:** MP4 video with all elements synchronized
✓ **Stage 10:** Videos created for all target platforms

---

## NOTES FOR CLAUDE

When working on this system:
1. Always check .env for available APIs before defaulting to alternatives
2. Timing is critical - track [PAUSE] markers through every stage
3. Color consistency must be maintained across all visual elements
4. Audio mixing is subtle - BGM should not overpower narration
5. All files should be organized by topic for easy future reference
6. Subtitle timing must match actual narration audio
7. Error handling: Use backup APIs if primary fails
8. Local Comfy GPU is available for more control over image generation
9. Test WCAG compliance at Stage 3 before generating images
10. Each stage is independent but should follow this exact sequence

---

## QUICK START FOR TEST VIDEO

To create your first test video (few minutes long):

```bash
# Setup (one time)
pip install -r requirements.txt
# Verify .env has: ELEVENLABS_API_KEY, FAL_API_KEY, ASSEMBLYAI_API_KEY, PEXELS_API_KEY

# Create test video
python firecrawl_scraper.py --topic "test-topic" --max-depth 2
python generate_script.py --topic "test-topic" --length short
python generate_images.py --topic "test-topic" --count 5 --skip-animations
python generate_narration.py --topic "test-topic"
python mix_audio.py --topic "test-topic"
python generate_subtitles.py --topic "test-topic"
python compose_video.py --topic "test-topic" --skip-animations

# Result: video/test-topic/video_COMPLETE.mp4 (1-2 minutes)
# Time: 5-10 minutes
```

Then once verified and working, add animations and create production videos.
