# Advanced Video Generation System - Complete Guide

A comprehensive, production-ready system for generating professional YouTube videos from FireCrawl-sourced content using Claude-powered research, AI image generation, Runway cinematic sequences, and Canva subtitles.

## System Architecture

```
FireCrawl URLs
     ↓
Research Agents (Claude + Codex)
  - Official sources
  - Community forums
  - Case studies
     ↓
Script Synthesis & Humanization
  - Claude rewrites for natural sound
  - Add pronunciation guides
  - Pause markers for narration
     ↓
Parallel Image Generation
  ├─ Flux Pro (photorealistic people/environments)
  └─ Nano Banana / Leonardo.AI (charts/text/infographics)
     ↓
Runway API (Cinematic Videos)
  - Still images → short motion clips
  - Dynamic transitions
     ↓
ElevenLabs Narration
  - SSML pause control
  - Pronunciation guidance
  - Voice: Rachel (Multilingual v2)
     ↓
Background Music Integration
  - Epidemic Sound / Artlist / Pond5
  - Volume: -38dB (subtle background)
  - Genre: Melodic Techno/Dubstep
     ↓
Canva Subtitles
  - White text, Pink/Black border
  - Pop animation
  - Auto-synced with narration
     ↓
Shotstack Video Assembly
  - Complete timeline assembly
  - Audio ducking (music quieter during narration)
  - Transitions and effects
     ↓
YouTube Publication
  - SEO metadata optimization
  - Chapter timestamps
  - Thumbnail generation
     ↓
Published YouTube Video ✓
```

---

## Core Modules

### 1. **advanced-video-orchestrator.js** - Main Orchestrator
Central coordinator that runs the entire pipeline end-to-end.

**Entry Point**:
```bash
node advanced-video-orchestrator.js
```

**What it does**:
- Orchestrates all 10 pipeline stages
- Manages project configuration
- Handles directory structure
- Coordinates between Claude agents and Codex implementations
- Generates logging and progress tracking

**Key Functions**:
- `stage1_multiSourceResearch()` - Launch research agents
- `stage2_synthesizeContent()` - Combine research findings
- `stage3_generateAndHumanizeScript()` - Create video script
- `stage4_generateImages()` - Generate AI images
- `stage5_assembleVideo()` - Build video timeline
- `stage6_generateNarration()` - Create audio narration
- `stage7_integrateMusic()` - Add background music
- `stage8_createSubtitles()` - Generate subtitles
- `stage9_optimizeSEO()` - Optimize metadata
- `stage10_publishToYouTube()` - Upload to YouTube

---

### 2. **research-agents-launcher.js** - Multi-Source Research
Spawns parallel Claude agents to research your topic from multiple authoritative sources.

**Features**:
- **Agent 1: Official Sources** - Google, Moz, SEJ, Semrush
- **Agent 2: Community Research** - Reddit, forums, discussions
- **Agent 3: Case Studies** - Proven results, A/B tests, experiments
- **Supplementary Agents** - Deep dives on specific subtopics

**Usage**:
```bash
node research-agents-launcher.js
```

**Output**:
- Consolidated research findings
- At least 3 verified sources per fact
- Structured JSON with citations
- Disagreements and consensus highlighted

---

### 3. **script-synthesizer.js** - Script Generation & Humanization
Converts research findings into a natural-sounding video script.

**Pipeline**:
1. Generate raw script from outline
2. Humanize with Claude (sounds conversational, not robotic)
3. Add narration markers (pauses, pronunciation guides)
4. Export for TTS processing

**Usage**:
```bash
node script-synthesizer.js
```

**Output**:
- Humanized script for video
- SSML formatting for ElevenLabs
- Timing and pronunciation guides
- Script metadata (word count, estimated duration)

---

### 4. **image-generation-pipeline.py** - AI Image Generation
Generates professional images using two specialized approaches.

**Photorealistic Images (Flux Pro)**:
- Professional people/teams
- Office environments
- Technical workspaces
- Product demos
- ~15 images per 10-min video

**Text-Based Images (Nano Banana / Leonardo.AI)**:
- Charts and graphs
- Infographics
- Step-by-step diagrams
- Statistics visualizations
- ~10 images per 10-min video

**Usage**:
```bash
python image-generation-pipeline.py
```

**Configuration**:
```python
# Flux Pro settings
model: 'flux-pro'
guidance: 8.5  # Strength of prompt adherence
quality: 'high'

# Nano Banana settings (for text/charts)
model: 'nano-banana'
requires_text: True
```

**Research Included**:
- Leonardo.AI comparison
- DALL-E 3 alternative
- Replicate.com options
- Cost analysis per service

---

### 5. **advanced-video-assembly.py** - Video Assembly
Combines all elements (images, videos, audio, music, subtitles) into final video.

**Components**:

**A. Runway API (Cinematic Videos)**:
- Converts still images into short cinematic clips
- Smooth pans, zooms, transitions
- Duration: 3-5 seconds per clip
- Motion types: zoom-pan, chart-animate, camera-pullout, montage

**B. Background Music**:
- Researches available platforms:
  - Epidemic Sound (30k+ tracks, $99-199/month)
  - Artlist ($99-129/month)
  - Pond5 (pay-per-track, $5-50)
  - Premium Beat, Soundly
- Recommends: Melodic Techno/Dubstep at 120-130 BPM

**C. Audio Level Optimization**:
- Narration: -20 dB (primary)
- Background music: -38 dB (subtle, underneath)
- Music drops: -15 dB (transitions only)
- Target loudness: -14 LUFS (YouTube standard)

**D. Canva Subtitles**:
- White text with Pink/Black border
- Pop-in/out animation
- Auto-synced to narration timing
- SRT format for compatibility

**E. Shotstack Assembly**:
- Builds complete video timeline
- Runway clips + still images
- Audio ducking (music quieter when narrator speaks)
- Transitions, effects, Ken Burns zoom
- Outputs: MP4, 1920x1080, 30fps, high quality

**Usage**:
```bash
python advanced-video-assembly.py
```

---

## Project Structure

```
VideoGen_YouTube/
├── advanced-video-orchestrator.js          # Main entry point
├── research-agents-launcher.js              # Multi-source research
├── script-synthesizer.js                    # Script generation
├── image-generation-pipeline.py             # AI image generation
├── advanced-video-assembly.py               # Video assembly
├── CODEX_TASK_PROMPT.md                     # Codex implementation guide
├── ADVANCED_VIDEO_SYSTEM_README.md          # This file
│
├── output/
│   ├── generated_images/                    # AI-generated images
│   │   ├── photorealistic/                  # Flux Pro outputs
│   │   ├── infographic/                     # Nano Banana outputs
│   │   └── metadata.json                    # Image metadata
│   ├── runway_videos/                       # Cinematic video clips
│   ├── narration.mp3                        # ElevenLabs output
│   ├── background_music.mp3                 # Licensed music
│   ├── audio_mixed.mp3                      # Mixed narration + music
│   ├── subtitles.srt                        # Subtitle timing file
│   ├── final_video.mp4                      # Complete final video
│   └── logs/                                # Execution logs
│
├── .env                                      # API keys (NOT in git)
├── config.json                               # Video settings
└── package.json                              # Node dependencies
```

---

## Setup & Getting Started

### 1. Install Dependencies

**Node.js**:
```bash
npm install
```

**Python**:
```bash
pip install python-dotenv requests pyyaml
# For audio processing:
pip install librosa soundfile numpy
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
# Required APIs
FAL_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
SHOTSTACK_API_KEY=your_key
YOUTUBE_CLIENT_ID=your_id
YOUTUBE_CLIENT_SECRET=your_secret

# Optional but recommended
RUNWAY_API_KEY=your_key
CANVA_API_KEY=your_key
DESCRIPT_API_KEY=your_key
```

### 3. Update Configuration

Edit `config.json` with your preferences:

```json
{
  "video": {
    "resolution": "1920x1080",
    "framerate": 30,
    "duration": 600
  },
  "music": {
    "genre": "melodic-techno-dubstep",
    "bpm": "120-130"
  }
}
```

### 4. Test API Connections

```bash
# Test each API before running full pipeline
node test-apis.js
python test_api_connections.py
```

---

## Usage: Complete Workflow

### Option A: SEO Best Practices Example (MVP)

```bash
# Run the complete SEO example
node advanced-video-orchestrator.js

# This will:
# 1. Launch research agents for "SEO Best Practices"
# 2. Generate script
# 3. Create images
# 4. Assemble video
# 5. Upload to YouTube
```

### Option B: Custom Topic

```javascript
// Edit config in advanced-video-orchestrator.js
const CONFIG = {
  projectName: 'My_Topic',
  topic: 'Your topic here',
  // ... rest of config
};
```

### Option C: Step-by-Step (Debug Mode)

```bash
# 1. Research
node research-agents-launcher.js

# 2. Generate Script
node script-synthesizer.js

# 3. Generate Images
python image-generation-pipeline.py

# 4. Assemble Video
python advanced-video-assembly.py
```

---

## Parallel Execution with Claude Code & Codex

**Claude Code** handles:
- Orchestration (`advanced-video-orchestrator.js`)
- Research coordination (`research-agents-launcher.js`)
- Script synthesis (`script-synthesizer.js`)

**Codex** handles (see `CODEX_TASK_PROMPT.md`):
- FireCrawl integration (`firecrawl-integration.js`)
- Image generation (`fal-image-generator.py`)
- Runway API (`runway-video-generator.py`)
- Canva subtitles (`canva-subtitle-generator.py`)
- ElevenLabs narration (`elevenlabs-narrator.py`)
- Music integration (`music-integrator.py`)
- Video assembly (`shotstack-assembler.py`)
- YouTube publication (`youtube-seo-publisher.py`)

---

## Video Production Specifications

### Resolution & Quality
- **Output**: 1920 × 1080 (Full HD)
- **FPS**: 30 frames per second
- **Codec**: H.264
- **Bitrate**: 8 Mbps
- **Format**: MP4

### Audio
- **Narrator**: ElevenLabs, Rachel voice
- **Music**: Royalty-free, melodic techno/dubstep
- **Volume Mixing**:
  - Narration: -20 dB (primary)
  - Music: -38 dB (background)
  - Drops: -15 dB (transitions)
- **Loudness**: -14 LUFS (YouTube standard)
- **Sample Rate**: 48 kHz
- **Channels**: Stereo

### Images
- **Photorealistic**: Flux Pro (FAL.ai)
- **Text/Charts**: Nano Banana or Leonardo.AI
- **Resolution**: 1920 × 1080 (match video)
- **Format**: PNG with alpha channel
- **Count**: 25-30 images per 10-minute video

### Video Duration
- **Target**: 10 minutes (600 seconds)
- **Narration**: ~1,300-1,500 words at 130 WPM
- **Scene Distribution**:
  - Intro: 45 seconds
  - Main content: ~500 seconds (6-7 sections)
  - Conclusion: 25 seconds

### Subtitles
- **Style**: White (#FFFFFF) text
- **Border**: Pink (#FF1493) + Black (#000000)
- **Font**: Bold sans-serif, 48pt
- **Animation**: Pop-in/out (0.3 seconds)
- **Timing**: Synced to narration with 100ms lead

---

## API Integration Details

### FireCrawl
- Input: URLs (1-100+)
- Output: JSONL articles with metadata
- Retry: 3 attempts, exponential backoff
- Cost: ~$0.10 per 1000 pages

### FAL.ai (Image Generation)
- Model: `flux-pro` for photorealistic
- Model: `nano-banana` for text/charts
- Cost: $0.03-0.08 per image depending on model
- Speed: 2-5 seconds per image

### ElevenLabs (Narration)
- Model: `eleven_multilingual_v2`
- Voice: Rachel
- Cost: $0.30 per 1000 characters
- Features: SSML, pause control, pronunciation guides

### Runway API (Video)
- Input: Static image + motion prompt
- Output: MP4 video clip
- Duration: 3-5 seconds per clip
- Cost: ~$1-5 per clip (varies by length)
- Speed: 30-60 seconds per clip

### Shotstack (Video Assembly)
- Input: Timeline (images, video, audio, text)
- Output: Final MP4
- Cost: $0.75 per render
- Resolution: Up to 4K
- Speed: 2-10 minutes depending on length

### YouTube API
- Authentication: OAuth 2.0
- Upload: Video + metadata + chapters
- Publishing: Public/unlisted/private
- Metadata: Title, description, tags, category, thumbnail

---

## Troubleshooting

### Images not generating
- Check FAL API key in `.env`
- Verify image prompts are specific and detailed
- Check account credits/quota on FAL.ai dashboard

### Narration sounds robotic
- Ensure script is humanized through Claude rewrite
- Add more pause markers `[pause: 1.5s]`
- Adjust stability (currently 0.75) if needed
- Check pronunciation guides are correct

### Video assembly failing
- Verify all source files exist (images, audio, video)
- Check Shotstack API key and owner ID
- Ensure file paths are correct
- Check JSON timeline structure

### YouTube upload rejected
- Verify title, description, tags are appropriate
- Check YouTube guidelines (no copyright content)
- Ensure video has proper metadata
- Check account isn't rate-limited

### Music volume too loud/quiet
- Adjust dB levels in `audio-mix` settings
- Target: Narration at -20dB, Music at -38dB
- Use audio analyzer to verify final mix
- Re-render video assembly after adjusting

---

## Best Practices

### Content Quality
1. **Research**: Use at least 3 verified sources per fact
2. **Script**: Make it conversational, not academic
3. **Pacing**: 150-160 words per minute is optimal for narration
4. **Variety**: Mix images, charts, video to maintain viewer interest

### Video Production
1. **Consistency**: Use same aspect ratio, color scheme throughout
2. **Timing**: Each image on screen 3-8 seconds for comprehension
3. **Transitions**: Use 0.5-1 second transitions between scenes
4. **Music**: Keep music subtle so narration is always clear

### SEO Optimization
1. **Title**: Include target keyword, 60 characters max
2. **Description**: 5000 characters max, include timestamps
3. **Tags**: 30 most relevant, long-tail keywords
4. **Chapters**: Add timestamps for each major section
5. **Thumbnail**: Include text, use contrasting colors

### Accessibility
1. **Subtitles**: Always include, properly synced
2. **Captions**: Use descriptive, not just transcription
3. **Audio**: Clear narration, no background noise
4. **Contrast**: Text readable on all backgrounds

---

## Performance Optimization

### Speed
- Run image generation in parallel (max 3 concurrent)
- Use batch processing where available
- Cache research results for reuse

### Cost
- Start with Nano Banana for charts (cheaper than DALL-E 3)
- Use Artlist instead of Epidemic Sound if on budget
- Render test videos before final render

### Quality
- Always use Flux Pro for photorealistic images
- Test audio mix before final assembly
- Generate multiple thumbnail options

---

## Environment Variables Reference

```bash
# Image Generation
FAL_API_KEY=                          # For Flux Pro & Nano Banana

# Audio
ELEVENLABS_API_KEY=                   # For text-to-speech

# Video Assembly
SHOTSTACK_API_KEY=                    # For final video rendering
SHOTSTACK_OWNER_ID=                   # Shotstack account ID

# Specialized Video
RUNWAY_API_KEY=                       # For cinematic sequences

# Graphics & Subtitles
CANVA_API_KEY=                        # For subtitle generation

# Script Humanization (optional)
DESCRIPT_API_KEY=                     # For advanced humanization

# YouTube Publishing
YOUTUBE_CLIENT_ID=                    # From Google Cloud Console
YOUTUBE_CLIENT_SECRET=                # From Google Cloud Console
YOUTUBE_REDIRECT_URI=http://localhost:8888/callback

# Application
DEBUG=false
LOG_LEVEL=INFO
OUTPUT_DIR=./output
```

---

## Next Steps

1. **For Claude Code**: Start with the orchestrator and research agents
2. **For Codex**: Follow `CODEX_TASK_PROMPT.md` for API implementations
3. **Test**: Run with SEO example first, then customize for your topics
4. **Scale**: Once working, set up scheduled runs for regular video generation

---

## Support & Troubleshooting

- Check logs in `output/logs/`
- Run individual modules for debugging
- Test each API connection separately
- Verify all `.env` variables are correct
- Review API documentation for rate limits and quotas

---

## Advanced Topics

### Custom Voices
ElevenLabs supports multiple voices. To use a different voice:
```python
VOICE_ID = 'your_voice_id'  # Get from ElevenLabs API
```

### Custom Music
To use your own music instead of library:
```python
background_music = 'path/to/your/music.mp3'
# System will mix it at optimal levels
```

### Multiple Languages
ElevenLabs supports 29+ languages. To create videos in other languages:
```python
language = 'es'  # Spanish, 'fr' for French, etc.
voice_id = get_multilingual_voice(language)
```

### Longer Videos
For videos longer than 10 minutes, adjust:
```python
duration = 1200  # 20 minutes in seconds
script_sections += more_sections
image_count *= 2
```

---

**Ready to create your first video?** Start with `node advanced-video-orchestrator.js`!
