# Automated Video Generation Workflow

Complete architecture documentation for the automated video generation pipeline.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Component Details](#component-details)
3. [Data Flow](#data-flow)
4. [Configuration Options](#configuration-options)
5. [Customization Guide](#customization-guide)
6. [Performance Optimization](#performance-optimization)
7. [Error Handling](#error-handling)

---

## Architecture Overview

### System Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────────┐
│                     AUTOMATED VIDEO PIPELINE                     │
└─────────────────────────────────────────────────────────────────┘

INPUT: Article URL
    │
    ├─> [PHASE 1: CONTENT EXTRACTION]
    │        │
    │        ├─> Firecrawl Scraper (Node.js)
    │        │   └─> Extracts: HTML → Markdown
    │        │
    │        ├─> JSON Converter
    │        │   └─> Converts: Markdown → JSONL
    │        │
    │        └─> Content Cleaner
    │            └─> Validates & sanitizes data
    │
    ├─> [PHASE 2: SCRIPT GENERATION]
    │        │
    │        ├─> Script Generator (Node.js)
    │        │   └─> Creates: Narration script
    │        │   └─> Creates: Storyboard
    │        │   └─> Creates: Visual guide
    │        │   └─> Creates: Timing markers
    │        │
    │        └─> AI Video Package
    │            └─> SVG chart templates
    │            └─> Complete production guide
    │
    ├─> [PHASE 3: ASSET GENERATION]
    │        │
    │        ├─> Image Generation (FAL.ai)
    │        │   └─> Input: Text prompts
    │        │   └─> Output: PNG images (1920x1080)
    │        │   └─> API: fal-ai/flux/schnell
    │        │
    │        ├─> Voiceover Generation (ElevenLabs)
    │        │   └─> Input: Narration script
    │        │   └─> Output: MP3 audio (44.1kHz)
    │        │   └─> Voice: Customizable (George default)
    │        │
    │        └─> [Optional] Whiteboard Animation
    │            └─> Manual: SpeedSketch
    │            └─> Programmatic: Manim alternative
    │
    ├─> [PHASE 4: VIDEO ASSEMBLY]
    │        │
    │        ├─> Video Editor API (Shotstack)
    │        │   └─> Inputs: Images + Audio + Text
    │        │   └─> Processing: JSON-based timeline
    │        │   └─> Output: MP4 video (1920x1080, 30fps)
    │        │
    │        └─> Rendering Pipeline
    │            ├─> Queue render job
    │            ├─> Monitor status (polling)
    │            ├─> Download rendered video
    │            └─> Save to local storage
    │
    └─> [PHASE 5: PUBLISHING]
             │
             ├─> YouTube Data API
             │   └─> OAuth authentication
             │   └─> Upload video
             │   └─> Set metadata (title, description, tags)
             │   └─> Set privacy (public/unlisted/private)
             │   └─> Upload thumbnail (optional)
             │
             └─> [Optional] Other Platforms
                 ├─> TikTok API
                 ├─> Instagram API
                 └─> Twitter/X API

OUTPUT: Published video with analytics tracking
```

---

## Component Details

### 1. Content Extraction Layer

**Technology**: Node.js (native modules only)

**Purpose**: Convert web articles into structured data for processing.

#### 1.1 Firecrawl Scraper

**File**: `scrape-and-convert.js`

**Process**:
```javascript
INPUT: URL string
  ↓
HTTP GET request (with user agent)
  ↓
HTML parsing (regex-based)
  ↓
Extract: <title>, <meta description>, <main>/<article>
  ↓
Remove: <script>, <style>, navigation elements
  ↓
Convert HTML → Markdown
  ↓
OUTPUT: JSON object
```

**Data Structure**:
```json
{
  "url": "https://example.com/article",
  "title": "Article Title",
  "description": "Meta description",
  "markdown": "# Article Title\n\nContent...",
  "metadata": {
    "title": "Article Title",
    "description": "Brief description",
    "source": "direct-html-parse"
  },
  "sections": []
}
```

**Error Handling**:
- Timeout: 10 seconds
- Retry: Not implemented (fail fast)
- Fallback: Manual JSONL creation

---

#### 1.2 JSONL Converter

**File**: `scrape-and-convert.js` (convertToJsonl function)

**Process**:
```javascript
INPUT: Raw JSON object
  ↓
Sanitize markdown (remove excessive newlines)
  ↓
Generate unique ID (from title + URL slug)
  ↓
Structure as JSONL (one JSON per line)
  ↓
Validate required fields
  ↓
OUTPUT: dataset.jsonl
```

**JSONL Format**:
```json
{
  "id": "article-slug-123",
  "url": "https://example.com/article",
  "title": "Article Title",
  "description": "Brief description",
  "author": "Author Name",
  "publishDate": "2024-12-10",
  "content": "Full markdown content",
  "sections": [
    {"heading": "Section 1", "content": "..."},
    {"heading": "Section 2", "content": "..."}
  ],
  "extracted_at": "2024-12-10T12:00:00Z",
  "language": "en"
}
```

---

#### 1.3 Content Cleaner

**File**: `clean-jsonl.js`

**Purpose**: Validate and sanitize JSONL data for AI consumption.

**Validation Rules**:
- Required fields: id, url, title, content
- Content length: > 100 characters
- Valid URL format
- No malicious content patterns
- UTF-8 encoding

**Output**: `clean-report.json` with validation results

---

### 2. Script Generation Layer

**Technology**: Node.js

**Purpose**: Transform article content into production-ready scripts.

#### 2.1 Video Script Generator

**File**: `generate-video-script.js`

**Creates**:
1. **COMPLETE_VIDEO_SCRIPT.md** - Master production document
2. **video-narration.md** - What to say (voiceover script)
3. **video-storyboard.md** - Visual planning with timing
4. **slide-deck.md** - Slide content and structure
5. **video-graphs.md** - ASCII diagrams and charts
6. **video-editing-guide.md** - Post-production instructions

**Generation Logic**:
```javascript
Read dataset.jsonl
  ↓
Parse article structure
  ↓
Identify key points (headings, paragraphs)
  ↓
Estimate timing (150 words/minute)
  ↓
Generate narration script
  ↓
Create storyboard with timestamps
  ↓
Design slide layouts
  ↓
Create ASCII diagrams
  ↓
Compile editing guide
  ↓
OUTPUT: 6 markdown files
```

---

#### 2.2 AI Video Package Generator

**File**: `generate-ai-video-package.js`

**Creates**:
1. **AI_VIDEO_NARRATION_WITH_MARKERS.md** - Script with timing cues
2. **AI_VIDEO_VISUAL_GUIDE.md** - Exact visual specifications
3. **SVG Chart Templates** - Pre-designed chart files
4. **PIKA_LABS_GUIDE.md** - AI video generation instructions

**SVG Chart Features**:
- Resolution: 1920x1080 (HD)
- Format: Scalable vector graphics
- Colors: Customizable palette
- Export: PNG for video tools

**Sample Charts Generated**:
- Question mark intro
- VS comparison
- Team collaboration
- Feature highlights
- Before/after comparisons
- Process workflows
- Pro tips lists
- Conclusion slides

---

### 3. Asset Generation Layer

**Technology**: Python 3.8+

**Purpose**: Generate images and audio from scripts using AI APIs.

#### 3.1 Image Generation (FAL.ai)

**Model**: FLUX.1 [schnell] (fastest variant)

**Process Flow**:
```python
Load image prompts from visual guide
  ↓
For each image prompt:
  ├─> Call FAL.ai API
  ├─> Model: fal-ai/flux/schnell
  ├─> Parameters:
  │   ├─> prompt: text description
  │   ├─> num_inference_steps: 4
  │   ├─> width: 1920
  │   ├─> height: 1080
  │   └─> seed: random (or fixed for consistency)
  ↓
Receive image URL
  ↓
Download image
  ↓
Save as PNG (chart_01.png, chart_02.png, etc.)
  ↓
OUTPUT: Image files in project directory
```

**Performance**:
- Generation time: ~10-20 seconds per image
- Concurrent requests: Limited by API tier
- Batch processing: Recommended for 10+ images

**Quality Settings**:
- Steps: 4 (fast), 20 (balanced), 50 (high quality)
- Guidance scale: 3.5 (default), 7.5 (more accurate)
- Safety filter: Enabled by default

---

#### 3.2 Voiceover Generation (ElevenLabs)

**Model**: eleven_multilingual_v2

**Process Flow**:
```python
Load narration script
  ↓
Split into chunks (if > 40,000 chars)
  ↓
For each chunk:
  ├─> Call ElevenLabs API
  ├─> Parameters:
  │   ├─> text: narration text
  │   ├─> voice_id: JBFqnCBsd6RMkjVDRZzb (George)
  │   ├─> model_id: eleven_multilingual_v2
  │   └─> output_format: mp3_44100_128
  ↓
Stream audio bytes
  ↓
Write to MP3 file
  ↓
OUTPUT: voiceover.mp3
```

**Voice Options**:
| Voice | ID | Style | Best For |
|-------|-----|-------|----------|
| George | JBFqnCBsd6RMkjVDRZzb | Warm, professional | Educational content |
| Rachel | 21m00Tcm4TlvDq8ikWAM | Young, calm | Lifestyle content |
| Adam | pNInz6obpgDQGcFmaJgB | Deep, authoritative | Documentary style |

**Audio Specifications**:
- Format: MP3
- Sample rate: 44.1 kHz
- Bitrate: 128 kbps
- Channels: Stereo
- Duration: Matches narration length

---

### 4. Video Assembly Layer

**Technology**: Python + Shotstack API

**Purpose**: Combine images, audio, and text into finished video.

#### 4.1 Shotstack Video Editor

**API Version**: v1

**Architecture**:
```
Timeline (container)
  │
  ├─> Track 1 (background)
  │   └─> Video/Image clips
  │
  ├─> Track 2 (overlays)
  │   └─> Logo, watermarks
  │
  ├─> Track 3 (text)
  │   └─> Titles, captions
  │
  └─> Audio Track
      └─> Voiceover, music
```

**Clip Structure**:
```python
Clip(
  asset=ImageAsset(src="https://example.com/image.png"),
  start=0.0,        # Start time in seconds
  length=5.0,       # Duration in seconds
  position="center", # Position on screen
  scale=1.0,        # Zoom level
  opacity=1.0,      # Transparency (0-1)
  transition=Transition(
    in="fade",      # Fade in
    out="fade"      # Fade out
  ),
  effect="zoomIn"   # Ken Burns effect
)
```

**Processing Pipeline**:
```
1. Create Timeline
     ↓
2. Add Tracks (layers)
     ↓
3. Add Clips to Tracks
     ↓
4. Set Output parameters
     ↓
5. Submit to API (POST /render)
     ↓
6. Receive render_id
     ↓
7. Poll for status (GET /render/:id)
     ├─> queued
     ├─> rendering (5-10 min)
     ├─> done → Download URL
     └─> failed → Error message
     ↓
8. Download video file
     ↓
9. Save as output.mp4
```

---

#### 4.2 Rendering Parameters

**Output Configuration**:
```python
Output(
  format="mp4",              # Video format
  resolution="hd",           # sd (960x540), hd (1280x720), 1080 (1920x1080)
  fps=30,                   # Frame rate
  quality="medium",         # low, medium, high
  aspectRatio="16:9",       # Video aspect ratio
  repeat=False              # Loop video
)
```

**Quality vs. Cost**:
| Quality | Resolution | File Size | Render Time | Cost |
|---------|-----------|-----------|-------------|------|
| SD | 960x540 | ~50MB/10min | 3-5 min | 0.5 credits/min |
| HD | 1280x720 | ~100MB/10min | 5-8 min | 0.8 credits/min |
| 1080p | 1920x1080 | ~200MB/10min | 8-12 min | 1.0 credit/min |

---

### 5. Publishing Layer

**Technology**: Python + Google API Client

**Purpose**: Upload finished videos to YouTube and other platforms.

#### 5.1 YouTube Data API Integration

**Authentication Flow**:
```
1. Load client_secrets.json
     ↓
2. Check for existing token.json
     ├─> Found: Load credentials
     └─> Not found: Run OAuth flow
         ├─> Open browser
         ├─> User logs in
         ├─> Grant permissions
         ├─> Receive token
         └─> Save to token.json
     ↓
3. Build YouTube service object
     ↓
4. Ready for API calls
```

**Upload Process**:
```python
1. Prepare video metadata
   ├─> title: string
   ├─> description: string (with timestamps)
   ├─> tags: list[string]
   ├─> category: integer (28 = Science & Tech)
   └─> privacy: "public" | "unlisted" | "private"
   ↓
2. Create MediaFileUpload object
   └─> chunksize: 1MB (resumable upload)
   ↓
3. Execute videos().insert()
   ↓
4. Upload in chunks
   ├─> Progress: 0% → 100%
   └─> Handle interruptions (resumable)
   ↓
5. Receive video ID
   ↓
6. [Optional] Set thumbnail
   └─> thumbnails().set()
   ↓
7. Return video URL
   └─> https://youtube.com/watch?v={video_id}
```

**Metadata Best Practices**:
```python
{
  "title": "Clear, engaging title (60 chars max)",
  "description": """
  Detailed description with:
  - Summary of video content
  - Timestamps for chapters
  - Links to resources
  - Social media links
  - Attribution to AI tools used

  Timestamps:
  0:00 - Introduction
  1:30 - Main topic
  5:00 - Key points
  10:00 - Conclusion

  Links:
  - Original article: [URL]
  - Newsletter: [URL]
  - GitHub: [URL]

  Made with:
  - Images: FAL.ai Flux
  - Voiceover: ElevenLabs
  - Video: Shotstack
  """,
  "tags": [
    "ai", "automation", "video production",
    "tutorial", "tech", "programming"
  ],
  "categoryId": "28"  # Science & Technology
}
```

---

## Data Flow

### Complete Pipeline Flow Diagram

```
┌────────────────┐
│  Article URL   │
└────────┬───────┘
         │
         ▼
┌────────────────────────────────────────┐
│         Content Extraction              │
│  (scrape-and-convert.js)               │
│  • HTTP request                         │
│  • HTML parsing                         │
│  • Markdown conversion                  │
└────────┬───────────────────────────────┘
         │
         ▼ [article.json, dataset.jsonl]
         │
         ▼
┌────────────────────────────────────────┐
│        Script Generation                │
│  (generate-video-script.js)            │
│  • Parse content structure              │
│  • Generate narration                   │
│  • Create storyboard                    │
│  • Design slides                        │
└────────┬───────────────────────────────┘
         │
         ▼ [6 markdown files, SVG templates]
         │
         ├─────────────┬─────────────┐
         │             │             │
         ▼             ▼             ▼
    ┌────────┐   ┌─────────┐   ┌────────┐
    │ Images │   │  Audio  │   │  Text  │
    │(FAL.ai)│   │(Eleven) │   │(Manual)│
    └───┬────┘   └────┬────┘   └───┬────┘
        │             │             │
        ▼             ▼             ▼
     [PNGs]        [MP3]         [Text]
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   Video Assembly        │
         │   (Shotstack API)       │
         │   • Create timeline     │
         │   • Add tracks & clips  │
         │   • Submit render       │
         │   • Poll for completion │
         │   • Download video      │
         └────────┬───────────────┘
                  │
                  ▼ [output.mp4]
                  │
                  ▼
         ┌────────────────────────┐
         │   Publishing            │
         │   (YouTube API)         │
         │   • Authenticate        │
         │   • Upload video        │
         │   • Set metadata        │
         │   • Set thumbnail       │
         └────────┬───────────────┘
                  │
                  ▼
         ┌────────────────────────┐
         │  Published Video URL    │
         └────────────────────────┘
```

---

## Configuration Options

### Global Configuration File

**File**: `config.json`

```json
{
  "pipeline": {
    "enabled_phases": ["extract", "script", "assets", "video", "publish"],
    "skip_on_error": false,
    "retry_attempts": 3,
    "log_level": "info"
  },

  "extraction": {
    "timeout": 10000,
    "user_agent": "Mozilla/5.0 (compatible; VideoBot/1.0)",
    "follow_redirects": true,
    "max_content_size": 5000000
  },

  "script_generation": {
    "narration_style": "professional",
    "words_per_minute": 150,
    "include_timestamps": true,
    "slide_duration": 5
  },

  "images": {
    "provider": "fal",
    "model": "fal-ai/flux/schnell",
    "width": 1920,
    "height": 1080,
    "steps": 4,
    "guidance_scale": 3.5,
    "style": "professional tech illustration"
  },

  "voiceover": {
    "provider": "elevenlabs",
    "voice_id": "JBFqnCBsd6RMkjVDRZzb",
    "model": "eleven_multilingual_v2",
    "stability": 0.5,
    "similarity_boost": 0.75,
    "output_format": "mp3_44100_128"
  },

  "video": {
    "provider": "shotstack",
    "resolution": "1080",
    "fps": 30,
    "quality": "high",
    "format": "mp4",
    "transitions": {
      "default": "fade",
      "duration": 0.5
    },
    "effects": {
      "ken_burns": true,
      "parallax": false
    }
  },

  "youtube": {
    "category": "28",
    "privacy": "public",
    "made_for_kids": false,
    "embeddable": true,
    "license": "youtube",
    "auto_chapters": true,
    "thumbnail": {
      "generate": true,
      "template": "default"
    }
  }
}
```

### Environment-Specific Configurations

**Development** (`config.dev.json`):
```json
{
  "images": {
    "steps": 4,
    "width": 1280,
    "height": 720
  },
  "video": {
    "provider": "shotstack",
    "environment": "stage",
    "quality": "medium"
  },
  "youtube": {
    "privacy": "unlisted"
  }
}
```

**Production** (`config.prod.json`):
```json
{
  "images": {
    "steps": 20,
    "width": 1920,
    "height": 1080
  },
  "video": {
    "provider": "shotstack",
    "environment": "v1",
    "quality": "high"
  },
  "youtube": {
    "privacy": "public"
  }
}
```

---

## Customization Guide

### 1. Custom Image Styles

**Edit**: `config.json` → `images.style`

**Options**:
- `"professional tech illustration"` (default)
- `"minimalist flat design"`
- `"3D rendered scene"`
- `"hand-drawn sketch"`
- `"photorealistic"`
- `"cyberpunk aesthetic"`

**Advanced Prompt Engineering**:
```python
base_prompt = config["images"]["style"]
custom_prompt = f"{base_prompt}, showing {scene_description}, {mood}, {lighting}"

# Example:
# "professional tech illustration, showing code on screen, energetic mood, bright lighting"
```

---

### 2. Custom Voice Settings

**Edit**: `config.json` → `voiceover`

**Voice Parameters**:
```json
{
  "voice_id": "JBFqnCBsd6RMkjVDRZzb",
  "stability": 0.5,           // 0 (variable) to 1 (stable)
  "similarity_boost": 0.75,   // 0 (low) to 1 (high)
  "style": 0.0,              // 0 (neutral) to 1 (exaggerated)
  "use_speaker_boost": true  // Enhance clarity
}
```

**Voice ID Reference**:
- George: `JBFqnCBsd6RMkjVDRZzb`
- Rachel: `21m00Tcm4TlvDq8ikWAM`
- Adam: `pNInz6obpgDQGcFmaJgB`
- Custom: Clone your own voice (paid feature)

---

### 3. Custom Video Transitions

**Edit**: `config.json` → `video.transitions`

**Available Transitions**:
```json
{
  "transitions": {
    "default": "fade",
    "duration": 0.5,
    "types": {
      "intro": "slideLeft",
      "outro": "slideRight",
      "scene_change": "crossfade",
      "emphasis": "zoom"
    }
  }
}
```

**Shotstack Transition Options**:
- `fade` - Gradual opacity change
- `wipe` - Directional wipe
- `slideLeft`, `slideRight`, `slideUp`, `slideDown`
- `zoom` - Scale in/out
- `crossfade` - Blend between clips

---

### 4. Custom Thumbnail Generation

**Option A: Automatic (First Frame)**
```json
{
  "youtube": {
    "thumbnail": {
      "generate": true,
      "source": "first_frame"
    }
  }
}
```

**Option B: Custom Template**
```python
# Create thumbnail from template
from PIL import Image, ImageDraw, ImageFont

img = Image.new('RGB', (1920, 1080), color='#3B82F6')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('Arial.ttf', 100)
draw.text((960, 540), "Video Title", fill='white', font=font, anchor='mm')
img.save('thumbnail.jpg')
```

---

## Performance Optimization

### 1. Parallel Processing

**Current**: Sequential processing
**Optimized**: Parallel asset generation

```python
import concurrent.futures

def generate_assets_parallel(prompts, scripts):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Generate images in parallel
        image_futures = [
            executor.submit(generate_image, prompt)
            for prompt in prompts
        ]

        # Generate voiceover in parallel
        audio_future = executor.submit(generate_voiceover, scripts)

        # Wait for all to complete
        images = [f.result() for f in image_futures]
        audio = audio_future.result()

    return images, audio

# Time saved: 50-70% for multiple assets
```

---

### 2. Caching Strategy

**Cache API Responses**:
```python
import hashlib
import json
import os

def cache_api_call(func):
    cache_dir = '.cache'
    os.makedirs(cache_dir, exist_ok=True)

    def wrapper(*args, **kwargs):
        # Create cache key from arguments
        cache_key = hashlib.md5(
            json.dumps([args, kwargs], sort_keys=True).encode()
        ).hexdigest()

        cache_file = f"{cache_dir}/{func.__name__}_{cache_key}.json"

        # Check cache
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)

        # Call API
        result = func(*args, **kwargs)

        # Save to cache
        with open(cache_file, 'w') as f:
            json.dump(result, f)

        return result

    return wrapper

@cache_api_call
def generate_image(prompt):
    # API call here
    pass
```

---

### 3. Resource Management

**Image Processing**:
```python
# Optimize images before upload
from PIL import Image

def optimize_image(input_path, output_path, max_size=(1920, 1080), quality=85):
    img = Image.open(input_path)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    img.save(output_path, 'JPEG', quality=quality, optimize=True)

    # Reduces file size by 40-60%
```

**Audio Compression**:
```python
# Compress audio without quality loss
from pydub import AudioSegment

def compress_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(
        output_path,
        format='mp3',
        bitrate='128k',
        parameters=['-ar', '44100', '-ac', '2']
    )

    # Reduces file size by 20-30%
```

---

## Error Handling

### Error Hierarchy

```
PipelineError (base)
  │
  ├─> ExtractionError
  │   ├─> NetworkError (timeout, connection)
  │   └─> ParsingError (invalid HTML)
  │
  ├─> APIError (base for API issues)
  │   ├─> FALError (image generation)
  │   ├─> ElevenLabsError (voiceover)
  │   ├─> ShotstackError (video rendering)
  │   └─> YouTubeError (upload)
  │
  └─> ValidationError
      ├─> ConfigError (invalid config)
      └─> DataError (invalid input data)
```

### Retry Strategy

```python
import time
from functools import wraps

def retry_with_backoff(max_attempts=3, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise

                    wait_time = backoff_factor ** attempt
                    print(f"Attempt {attempt} failed. Retrying in {wait_time}s...")
                    time.sleep(wait_time)

        return wrapper
    return decorator

@retry_with_backoff(max_attempts=3)
def call_api(endpoint, data):
    # API call here
    pass
```

### Graceful Degradation

```python
def generate_video_with_fallback(config):
    try:
        # Try primary video provider (Shotstack)
        video = generate_with_shotstack(config)
    except ShotstackError as e:
        print(f"Shotstack failed: {e}")
        try:
            # Fallback to JSON2Video
            video = generate_with_json2video(config)
        except Exception as e2:
            print(f"JSON2Video failed: {e2}")
            # Final fallback: local processing with FFmpeg
            video = generate_with_ffmpeg(config)

    return video
```

---

## Next Steps

Now that you understand the workflow:

1. **Read VIDEO_PARAMETERS.md** - Learn about all customizable settings
2. **Read DEPLOYMENT_GUIDE.md** - Set up automated scheduling
3. **Read TROUBLESHOOTING.md** - Handle common issues
4. **Experiment** - Modify config.json and test different settings

---

**Workflow documentation complete.**

For implementation details, see the Python and Node.js source files in this project.
