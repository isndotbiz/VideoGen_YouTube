# CODEX MAX: Complete Video Generation Pipeline - Master Prompt

## 🎯 PROJECT OVERVIEW

You are building a **fully automated YouTube video generation platform** that transforms web articles into professional AI-generated videos. The system orchestrates:

- **Research & Content Extraction**: Scrape web pages → verify facts with 3+ sources → aggregate comprehensive summaries
- **AI Image Generation**: Create photorealistic and text-overlay images using FAL.ai (Flux Pro + Nano Banana)
- **Script Generation**: Convert research into compelling video scripts optimized for narration
- **Voice Generation**: Use ElevenLabs to create natural-sounding narration with pause markers and pronunciation guides
- **Video Creation**: Combine images + Runway ML API to create cinematic video clips
- **Professional Assembly**: Use Descript for auto-captioning, video editing, and timeline management
- **YouTube Publishing**: Auto-upload with SEO optimization (titles, descriptions, tags, chapters, timestamps)
- **Cost Optimization**: Keep per-video costs under $3, target 3-minute videos initially, expand to 33-second attention grabbers

## 📦 PROJECT STRUCTURE & DEPENDENCIES

### Available APIs & Services

```
FAL.ai:          Flux Pro (photorealistic), Nano Banana (text/charts)
ElevenLabs:      Text-to-Speech narration with pause markers
Runway ML:       AI video generation from images
Descript:        Video editing, auto-captions, timeline assembly
YouTube:         Video publishing with OAuth2 authentication
AWS S3:          Cloud storage for generated assets
OpenRouter:      LLM access (Claude, GPT, etc.) via API
Canva API:       (Optional) Additional design/text overlay options
ComfyUI:         (Optional) Local image generation fallback
Replicate:       (Optional) Alternative image generation service
```

### Environment Variables (in .env)

```
FAL_API_KEY=                    # FAL.ai API credentials
ELEVENLABS_API_KEY=             # ElevenLabs API key
RUNWAY_API_KEY=                 # Runway ML API key
DESCRIPT_API_KEY=               # Descript API token
YOUTUBE_CLIENT_ID=              # YouTube OAuth2 client ID
YOUTUBE_CLIENT_SECRET=           # YouTube OAuth2 secret
AWS_ACCESS_KEY_ID=              # AWS S3 access
AWS_SECRET_ACCESS_KEY=          # AWS S3 secret
AWS_REGION=                     # AWS region (us-east-1)
AWS_S3_BUCKET=                  # S3 bucket name
OPENROUTER_API_KEY=             # OpenRouter LLM API key
COMFYUI_SERVER_URL=             # ComfyUI local server (optional)
DEBUG=false                     # Enable debug logging
```

### File Organization

```
VideoGen_YouTube/
├── [ENTRY POINTS - Run These]
│   ├── orchestrate.js           # Original: Scrape → JSON → JSONL → Script
│   ├── research-agents-launcher.js  # Multi-agent research verification
│   ├── script-synthesizer.js    # Script generation + humanization
│   ├── image-generation-nano-banana.py  # Generate images (Flux + NanoBanana)
│   ├── elevenlabs_narration_WORKING.py  # Generate narration
│   ├── runway-video-generator.js  # Queue Runway video generation
│   ├── descript-video-editor.js # Send to Descript for assembly
│   └── upload_to_youtube.py     # Publish with SEO optimization
│
├── [UTILITIES]
│   ├── clean-jsonl.js           # Validate/clean JSONL data
│   ├── firecrawl-data-manager.js # URL scraping management
│   ├── video_pipeline.py        # Python orchestrator
│   └── setup.js / setup.py      # API configuration wizards
│
└── [OUTPUT DIRECTORIES]
    ├── output/
    │   ├── generated_images/    # Flux + NanoBanana images
    │   ├── runway_videos/       # Runway ML video clips
    │   ├── narration.mp3        # ElevenLabs audio
    │   ├── COMPLETE_VIDEO_SCRIPT.md
    │   └── final_video.mp4      # Final assembled video
    ├── logs/
    └── temp/
```

## 🔄 COMPLETE WORKFLOW (What Needs to Work Together)

### Phase 1: Research & Content Preparation
1. **Input**: Multiple article URLs or topics
2. **Scrape**: Use Firecrawl to extract page content
3. **Extract JSONL**: Convert to standardized JSON Lines format with metadata
4. **Verify Sources**: Launch research agents to find 3+ reliable sources per fact
5. **Aggregate**: Create comprehensive summary from multiple pages + forum/Reddit data
6. **Validate**: Ensure all major claims are verified by multiple sources
7. **Output**: `dataset.jsonl`, source citations, confidence scores

### Phase 2: Script Generation
1. **Input**: JSONL dataset + source verification data
2. **Synthesize**: Generate raw script structure (intro, sections, conclusion)
3. **Humanize**: Convert technical content to natural conversational tone
4. **Target Duration**: Create timing for 3-minute videos (~450-600 words)
   - Alternative: 33-second attention grabbers (~80-100 words)
5. **Add Markers**: Insert pause points, pronunciation guides for ElevenLabs
6. **Create Sections**: Break into visual scenes (one image/video per 10-15 seconds)
7. **Output**: `COMPLETE_VIDEO_SCRIPT.md`, `narration_markers.json`, timing data

### Phase 3: Image Generation
1. **Input**: Script sections + visual cues
2. **Generate Photorealistic Images** (Flux Pro):
   - Professional people working (analyst, team, presenter)
   - Office environments (workspace, meeting room, setup)
   - Hands/detail shots (typing, pointing, analyzing)
   - Generate 4-5 images per video
3. **Generate Text/Chart Images** (Nano Banana):
   - Charts and graphs extracted from research
   - Infographics summarizing key points
   - Comparison tables
   - Step-by-step diagrams
   - Generate 7-10 text-based images per video
4. **Save with Metadata**: Store image descriptions, usage notes, timing
5. **Output**: `output/generated_images/*.png`, `metadata_nano_banana.json`

### Phase 4: Narration Generation
1. **Input**: Script with ElevenLabs markers (pauses, pronunciation, emphasis)
2. **API Call**: Use ElevenLabs TTS with:
   - Voice: Rachel (or user's voice when ready)
   - Model: Multilingual v1
   - Stability: 0.75 (natural variation)
   - Auto-ducking ready (for music later)
3. **Recognize Markers**: Skip/pause sections marked as instructions, not speech
4. **Generate Audio**: Create MP3 narration (~3-5 minutes for short videos)
5. **Extract Timing**: Generate subtitle timings in SRT format
6. **Output**: `narration.mp3`, `narration_timing.json`, `narration.srt`

### Phase 5: Video Generation
1. **Input**: Generated images + scene descriptions
2. **Queue with Runway**: Send image + motion prompt for each scene:
   - Cinematic zoom (dashboard, workspace views)
   - Animated charts (growth, rankings, metrics)
   - Pan and tracking (across people, teams)
   - Transitions (fade, dissolve between scenes)
3. **Duration**: 3-5 seconds per Runway video
4. **Wait for Completion**: Poll Runway API for finished videos
5. **Batch Processing**: Queue all 5-7 videos in parallel
6. **Output**: `output/runway_videos/*.mp4`, task status tracking

### Phase 6: Professional Assembly (Descript)
1. **Input**:
   - Narration MP3
   - Generated images
   - Runway video clips
   - Script timing guide
2. **Auto-Transcribe**: Descript converts narration to text (auto-captioning)
3. **Generate Captions**: Styled SRT captions (white text, pink border)
4. **Timeline Building**:
   - Import narration audio
   - Place images at corresponding timestamps
   - Insert Runway video clips for dynamic sequences
   - Add background music (Epidemic Sound or YouTube Audio Library)
5. **Video Composition**: 1920x1080, 24fps, H.264 codec
6. **Export**: Final MP4 video with embedded captions
7. **Output**: `output/final_video.mp4`

### Phase 7: YouTube Publishing
1. **Input**: Final video file + script data
2. **Generate SEO Content**:
   - Title: Optimized for search ranking (includes keywords from research)
   - Description: 5000 characters with timestamps, source links, hashtags
   - Tags: 30 most relevant terms
   - Chapters: Auto-generated from script sections
3. **OAuth Authentication**: Use stored YouTube credentials
4. **Upload**: Post to YouTube with metadata
5. **Visibility**: Set to unlisted/private initially, then public
6. **Output**: YouTube video URL, upload confirmation, performance metrics

## 🎬 THREE VIDEO TYPES TO SUPPORT

### Type 1: Full Research Video (3 minutes)
- Complete overview of topic
- 4-5 sections with depth
- Mix of photorealistic + chart images
- 2-3 Runway video clips
- Full narration
- Ideal for educational/explanatory content

### Type 2: Attention Grabber (33 seconds)
- Hook in first 3 seconds
- Single key insight or trend
- 2-3 dynamic images
- Quick narration
- Designed for YouTube Shorts/TikTok/Reels
- Can be repurposed from longer video

### Type 3: Deep Dive Section (90 seconds)
- Single topic from larger research
- Focused exploration
- 2-3 images + 1 Runway video
- Targeted audience
- Can be used as series or playlist

## 📋 IMPLEMENTATION CHECKLIST

### Core Requirements (Must Have)

- [ ] **Firecrawl Integration**: Scrape multiple URLs, extract structured content
- [ ] **Research Agent Multi-Verification**: Launch 3 parallel agents verifying facts from official/community/case-study sources
- [ ] **JSONL Pipeline**: Convert scraped content to standardized format with metadata
- [ ] **Script Synthesis**: Generate scripts with proper structure, timing, and natural language flow
- [ ] **Marker System**: Scripts must recognize ElevenLabs pause markers, pronunciation guides, instruction-vs-narration
- [ ] **FAL.ai Image Generation**:
  - Flux Pro for photorealistic images only (people, spaces, objects)
  - Nano Banana for text/chart images (infographics, diagrams, comparisons)
- [ ] **ElevenLabs Narration**: Generate MP3 with pause markers recognized and acted upon
- [ ] **Runway ML Video Generation**: Convert static images to cinematic 3-5 second clips with motion
- [ ] **Descript Integration**: Auto-caption, generate SRT, and export final video
- [ ] **YouTube Publishing**: OAuth2 auth, upload with SEO metadata (title, description, tags, chapters)
- [ ] **AWS S3 Upload**: Store assets in cloud, use signed URLs for Descript import
- [ ] **Cost Tracking**: Log per-video costs, aim for <$3/video for 3-minute content

### Enhanced Features (Nice to Have, Post-MVP)

- [ ] **Canva API**: For additional text overlay and design options
- [ ] **Custom Voice**: Integration with user's own voice recording
- [ ] **Video Watermarks**: Branded intro/outro overlay
- [ ] **Playlist Management**: Auto-group related videos into playlists
- [ ] **Performance Analytics**: Track views, engagement, rankings over time
- [ ] **Thumbnail Generation**: AI-generated or extracted from video
- [ ] **Multi-Language Support**: Translate scripts and generate multilingual narration
- [ ] **FFmpeg Integration**: Local video processing for transitions, effects
- [ ] **ComfyUI Local Fallback**: Generate images locally if FAL.ai quota exhausted
- [ ] **Replicate Integration**: Alternative image generation provider

### Quality Assurance

- [ ] **Script Quality**: Natural language, proper pacing, no technical jargon without explanation
- [ ] **Image Quality**: Photorealistic images > 2MB each, text images readable at 1080p
- [ ] **Narration Quality**: Clear voice, no skipped sections, proper pause timing
- [ ] **Video Quality**: 1920x1080 minimum, H.264 codec, AAC audio
- [ ] **Metadata Quality**: All SEO fields filled, timestamps accurate, descriptions helpful
- [ ] **Fact Accuracy**: All claims verified by 3+ sources, citations included
- [ ] **Timing**: Videos complete within planned duration (3 min ±10 sec)

## 🚀 EXECUTION STRATEGY

### For Claude Max Agent (Your Instructions)

1. **Parallel Processing**: Start multiple agents simultaneously
   - Agent 1: Research verification (fact-checking across sources)
   - Agent 2: Image prompt generation (visual planning for scenes)
   - Agent 3: Script synthesis (story structure and timing)
   - Agent 4: Metadata preparation (SEO, descriptions, tags)

2. **Error Handling**: Implement fallback strategies
   - If Flux Pro unavailable → use Nano Banana or Replicate
   - If Runway fails → queue for retry with exponential backoff
   - If Descript API unresponsive → queue for manual assembly
   - If YouTube upload fails → save file locally, retry with new token

3. **Cost Optimization**:
   - Reuse images across videos when appropriate (reduced generation)
   - Batch queue Runway videos (parallel processing discounts)
   - Cache research results for similar topics
   - Use lower-cost image models for simple graphics
   - Monitor quota usage real-time, alert at 80% threshold

4. **Progress Tracking**:
   - Log all major milestones with timestamps
   - Save intermediate outputs (enables resume from failure)
   - Display progress percentage to user
   - Email or webhook alerts for completion

5. **Video Duration Target**:
   - Initial target: 3-minute videos (start here to debug issues)
   - Then: 33-second attention grabbers (format for YouTube Shorts)
   - Then: 90-second deep dives (topical breakdowns)
   - Scale to longer-form (10+ min) after core system proven

## 🔑 CRITICAL SUCCESS FACTORS

1. **Source Verification**: At least 3 reliable sources per major claim (no hallucinations)
2. **Image Consistency**: Style remains coherent across video (no jarring transitions)
3. **Audio Quality**: Narration must be clear, properly paced, no robotic/unnatural tone
4. **Timing Accuracy**: Script duration matches intended video length (±5%)
5. **Cost Control**: Each video costs <$3 in API calls
6. **Reproducibility**: Same input should always produce similar (not identical) output
7. **Automation**: Minimal user intervention after initial setup (click → video ready)

## 📊 SUCCESS METRICS (How We Know It Works)

- ✅ First 3-minute test video completes end-to-end in <1 hour
- ✅ All generated images are relevant to script (no mismatches)
- ✅ Narration audio is clear, properly timed, no skipped sections
- ✅ Final video is 1920x1080, H.264, with proper captions
- ✅ YouTube upload succeeds with all SEO metadata populated
- ✅ Total cost per video is $1-3 (track and optimize continuously)
- ✅ User can generate 2-3 videos in a single workday

## 🎯 START HERE: Minimum Viable Product (MVP)

### Week 1 Goals:
1. Get 3-minute video generation working end-to-end
2. Single topic, single source (verify concept)
3. Manual research verification (agent verification can come later)
4. Local image generation possible (as backup)
5. YouTube upload working with basic metadata

### Week 2 Goals:
1. Add multi-source research verification
2. Generate 33-second attention grabber versions
3. Implement cost tracking and optimization
4. Create 5-10 test videos with different topics
5. Refine image prompts based on quality feedback

### Week 3+ Goals:
1. Automate research agent verification
2. Reddit/forum scanning for additional sources
3. Advanced SEO optimization
4. Performance analytics integration
5. Multi-language support

---

## 📚 KEY IMPLEMENTATION NOTES

### Script with Markers Format

```markdown
# SEO Best Practices - Complete Guide for 2025

## [SECTION] Introduction
[TIMING: 0:00-0:30]
[IMAGE: professional-woman-analyzing.png]
[NARRATION]
Today we're covering seven essential SEO practices that will transform your rankings in 2025.
[PAUSE: 2s]
Whether you're starting from scratch or optimizing existing content, these strategies work.
[EMPHASIS: "strategies work" - increase pitch/volume slightly]

## [SECTION] Technical SEO
[TIMING: 0:30-2:00]
[IMAGE: workspace-dual-monitors.png]
[RUNWAY_VIDEO: runway_task_seo_1.mp4]
[CHART_IMAGE: nano_chart_ranking_factors.png]
[NARRATION]
First, let's talk about technical SEO. This is the foundation everything else builds on.
[PRONUNCIATION: "robots.txt" -> "row-bots dot text file"]
Your robots.txt file, XML sitemap, and crawl budget are critical.
[PAUSE: 1.5s]
(Runway video shows dashboard analytics with zoom effect - 3 seconds)

## [INSTRUCTION - DO NOT READ]
[Camera focus on chart showing ranking factors]

```

### Image Metadata JSON Format

```json
{
  "images": [
    {
      "id": "flux_people_1",
      "type": "photorealistic",
      "model": "flux-pro",
      "description": "Professional woman analyzing analytics at desk",
      "usage_in_video": "Opening scene - establish setting",
      "timing": "0:00-0:15",
      "file_path": "output/generated_images/flux_people_1.png",
      "file_size_bytes": 2400000,
      "generation_cost": 0.06,
      "quality_notes": "Sharp focus, professional lighting, suitable for 4K"
    }
  ],
  "total_generation_cost": 0.75,
  "estimated_video_minutes": 3.0
}
```

### Runway Video Batch Format

```javascript
{
  "batch_id": "batch_seo_2025_001",
  "videos": [
    {
      "task_id": "runway_task_seo_1",
      "image": "flux_workspace_1.png",
      "prompt": "Cinematic zoom into analytics dashboard, showing graphs updating in real-time, professional office setting, duration 3 seconds",
      "motion_type": "cinematic-zoom",
      "duration": 3,
      "status": "pending",
      "estimated_cost": 0.08
    }
  ],
  "total_estimated_cost": 0.40,
  "submit_in_parallel": true
}
```

---

## ✅ FINAL INSTRUCTION FOR CODEX MAX

**Your mission**: Build a system where a user can provide a topic/URL, and 40 minutes later have a professional, researched, SEO-optimized YouTube video ready to upload.

Start with 3-minute videos as proof of concept, then expand to shorter formats. Focus on automation and cost efficiency. Every decision should optimize for either quality, speed, or cost (in that priority order).

**Go build it.**

