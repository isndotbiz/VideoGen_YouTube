# Complete API Reference Guide for Video Automation Pipeline
**Last Updated: December 10, 2025**

This comprehensive guide covers all APIs needed for automated video content generation and publishing, including authentication, setup, code examples, and pricing.

---

## Table of Contents
1. [FAL.ai (Flux Image Generation)](#1-falai-flux-image-generation)
2. [ElevenLabs (Text-to-Speech)](#2-elevenlabs-text-to-speech)
3. [SpeedSketch (Whiteboard Animation)](#3-speedsketch-whiteboard-animation)
4. [Video Assembly APIs](#4-video-assembly-apis)
5. [YouTube Data API (Publishing)](#5-youtube-data-api-publishing)
6. [Complete Workflow Example](#6-complete-workflow-example)

---

## 1. FAL.ai (Flux Image Generation)

### Overview
FAL.ai provides API access to FLUX image generation models, including FLUX.1 [dev], [schnell], [pro], and FLUX.2 [flex].

### API Endpoints
- **FLUX.1 [dev]**: `fal-ai/flux/dev` - 12B parameter text-to-image model
- **FLUX.1 [schnell]**: `fal-ai/flux/schnell` - Fastest variant (1-4 steps)
- **FLUX.1 [pro]**: `fal-ai/flux-pro` - Next generation model
- **FLUX.2 [flex]**: `fal-ai/flux-2-flex` - Advanced customizable model
- **Image-to-Image**: `fal-ai/flux/dev/image-to-image` - Transform existing images

### Authentication
**Method**: API Key

**Setup Process**:
1. Visit https://fal.ai and create an account
2. Navigate to your dashboard
3. Generate an API key
4. Set environment variable: `export FAL_KEY="your_api_key"`

**Alternative**: Pass API key directly in client configuration:
```python
fal.config({"credentials": "YOUR_FAL_KEY"})
```

### Python SDK Installation
```bash
pip install fal-client
```

### Code Examples

#### Basic Text-to-Image Generation
```python
from fal_client import fal

# Set API key
fal.config({"credentials": "YOUR_FAL_KEY"})

# Generate image with FLUX.1 [schnell] (fastest)
result = fal.subscribe("fal-ai/flux/schnell", {
    "input": {
        "prompt": "A serene mountain landscape at sunset, hyperrealistic style",
        "num_inference_steps": 4,
        "guidance_scale": 3.5,
        "seed": 42,
        "safety_checker": True
    }
})

# Access the generated image
image_url = result["images"][0]["url"]
print(f"Generated image: {image_url}")
```

#### Image-to-Image Transformation
```python
result = fal.subscribe("fal-ai/flux/dev/image-to-image", {
    "input": {
        "image_url": "https://your-image-url.com/image.jpg",
        "prompt": "Transform this into a watercolor painting style",
        "strength": 0.8,
        "num_inference_steps": 40
    }
})
```

#### Queue-based Request with Webhook
```python
# For asynchronous processing with webhook notification
result = fal.queue_submit(
    "fal-ai/flux/dev",
    arguments={
        "prompt": "A futuristic cityscape at night",
        "num_inference_steps": 50
    },
    webhook_url="https://your-domain.com/webhook-endpoint"
)

# Get request status
status = fal.queue_status("fal-ai/flux/dev", result.request_id)
```

### Key Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | required | Text description of desired image |
| `num_inference_steps` | integer | 40 | Number of denoising steps (4 for schnell) |
| `guidance_scale` | float | 3.5 | Prompt adherence strength |
| `width` | integer | 1024 | Image width in pixels |
| `height` | integer | 1024 | Image height in pixels |
| `seed` | integer | random | For reproducible results |
| `safety_checker` | boolean | true | Content safety filtering |

### Output Format
```json
{
  "images": [
    {
      "url": "https://fal.media/files/...",
      "width": 1024,
      "height": 1024,
      "content_type": "image/jpeg"
    }
  ],
  "seed": 42,
  "has_nsfw_concepts": [false]
}
```

### Rate Limits & Pricing
- **Free Tier**: Not explicitly documented; check FAL.ai dashboard
- **Pricing**: Usage-based; check https://fal.ai/pricing
- **Supports**: Queue-based processing, webhooks, streaming requests

### Node.js SDK
```bash
npm install @fal-ai/serverless-client
```

```javascript
import * as fal from "@fal-ai/serverless-client";

fal.config({
  credentials: "YOUR_FAL_KEY"
});

const result = await fal.subscribe("fal-ai/flux/schnell", {
  input: {
    prompt: "A serene mountain landscape at sunset"
  }
});
```

---

## 2. ElevenLabs (Text-to-Speech)

### Overview
ElevenLabs provides high-quality AI text-to-speech with multiple voices and languages.

### API Endpoint
**Base URL**: `https://api.elevenlabs.io/v1`

**Key Endpoints**:
- Text-to-Speech: `POST /text-to-speech/{voice_id}`
- Streaming TTS: `POST /text-to-speech/{voice_id}/stream`
- List Voices: `GET /voices`
- Speech-to-Text: `POST /speech-to-text`

### Authentication
**Method**: API Key (xi-api-key header)

**Setup Process**:
1. Visit https://elevenlabs.io and create account
2. Navigate to Settings → Profile → API Keys
3. Click "Developers" in sidebar
4. Select "API Keys" tab
5. Click "Create" to generate new API key
6. Set environment variable: `export ELEVEN_API_KEY="your_api_key"`

### Free Tier Limits
- **Free Plan**: Includes API access
- **Monthly Quota**: Limited character quota (check dashboard)
- **Features**: All standard voices and features
- **Per-generation Limit**: Up to 40,000 characters for Flash v2.5 and Turbo v2.5
- **Concurrency**: Limited concurrent requests (tier-dependent)

### Python SDK Installation
```bash
pip install elevenlabs
```

### Code Examples

#### Basic Text-to-Speech
```python
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save

load_dotenv()
client = ElevenLabs()  # Automatically reads ELEVEN_API_KEY from env

# Convert text to speech
audio = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # George voice
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128"
)

# Play audio
play(audio)

# Or save to file
save(audio, "output.mp3")
```

#### Streaming Text-to-Speech
```python
from elevenlabs import stream
from elevenlabs.client import ElevenLabs

client = ElevenLabs()

# Stream audio for real-time playback
audio_stream = client.text_to_speech.stream(
    text="This is a streaming test with real-time audio playback.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2"
)

# Option 1: Stream and play
stream(audio_stream)

# Option 2: Process chunks manually
for chunk in audio_stream:
    if isinstance(chunk, bytes):
        # Process audio bytes (write to file, send over network, etc.)
        print(f"Received {len(chunk)} bytes")
```

#### Async Operations
```python
import asyncio
from elevenlabs.client import AsyncElevenLabs

client = AsyncElevenLabs(api_key="YOUR_API_KEY")

async def generate_speech():
    audio = await client.text_to_speech.convert(
        text="Async text-to-speech generation",
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2"
    )
    return audio

audio = asyncio.run(generate_speech())
```

#### List Available Voices
```python
client = ElevenLabs()

# Get all available voices
voices = client.voices.get_all()

for voice in voices.voices:
    print(f"Voice: {voice.name}, ID: {voice.voice_id}")
    print(f"Category: {voice.category}, Language: {voice.labels.get('language', 'N/A')}")
```

### Key Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Text to convert to speech |
| `voice_id` | string | required | Voice identifier |
| `model_id` | string | required | TTS model (e.g., eleven_multilingual_v2) |
| `output_format` | string | mp3_44100_128 | Audio format (mp3, pcm, etc.) |
| `voice_settings` | object | null | Stability, similarity_boost, style, etc. |

### Popular Voice IDs
- **George**: `JBFqnCBsd6RMkjVDRZzb` - Warm, informative narrator
- **Rachel**: `21m00Tcm4TlvDq8ikWAM` - Calm, young, female
- **Adam**: `pNInz6obpgDQGcFmaJgB` - Deep, male voice

### Output Formats
- `mp3_44100_128` - MP3 at 44.1kHz, 128kbps
- `mp3_44100_192` - Higher quality MP3
- `pcm_16000` - Raw PCM audio
- `pcm_24000` - Higher sample rate PCM

### Rate Limits
- **Concurrency**: Depends on subscription tier
- **Monthly Quota**: Character-based limits
- **Enterprise**: Unlimited concurrent requests (custom plan)

### Node.js SDK
```bash
npm install elevenlabs
```

```javascript
import { ElevenLabsClient } from "elevenlabs";

const client = new ElevenLabsClient({
  apiKey: "YOUR_API_KEY"
});

const audio = await client.textToSpeech.convert({
  text: "Hello from ElevenLabs",
  voiceId: "JBFqnCBsd6RMkjVDRZzb",
  modelId: "eleven_multilingual_v2"
});
```

---

## 3. SpeedSketch (Whiteboard Animation)

### Overview
SpeedSketch is a free AI-powered whiteboard animation tool that converts images into hand-drawn videos.

### API Status
**PUBLIC API**: NOT CURRENTLY AVAILABLE

Based on research, SpeedSketch does not currently offer a public API or webhook integrations. The platform mentions that "API functionality is being considered as a potential premium feature" but is not documented as available.

### Current Capabilities
- Web-based tool at https://www.speedsketch.co.uk/app
- Transforms images into whiteboard animations
- Generates MP4 videos in under 2 minutes
- Free forever tier available
- Features: Realistic drawing effects, stroke variations, timing, natural hand movement

### Workarounds for Automation

#### Option 1: Web Scraping (Not Recommended)
Browser automation with Selenium/Playwright - violates ToS and unreliable.

#### Option 2: Alternative APIs with Whiteboard Features

**VideoScribe API** (if available):
- Commercial whiteboard animation software
- Contact VideoScribe sales for API access

**Custom Solution with Manim**:
```python
from manim import *

class WhiteboardAnimation(Scene):
    def construct(self):
        # Create hand-drawn effect
        text = Text("Your content here")
        self.play(Write(text), run_time=3)
```

#### Option 3: Contact SpeedSketch
Email SpeedSketch team to request:
- API beta access
- Bulk processing capabilities
- Enterprise/automation features

### Recommended Alternative: Doodly or VideoScribe
Both offer more mature platforms for automated whiteboard video generation, though API availability should be verified.

---

## 4. Video Assembly APIs

Since Canva has limited API capabilities requiring Enterprise accounts, here are the best alternatives for programmatic video assembly:

### 4.1 Shotstack (RECOMMENDED)

#### Overview
Cloud-based video editing API designed for scalable, programmatic video creation using JSON templates.

#### API Endpoint
**Base URL**: `https://api.shotstack.io/v1`

**Environments**:
- Staging: `https://api.shotstack.io/stage` (free testing)
- Production: `https://api.shotstack.io/v1` (paid)

#### Authentication
**Method**: API Key (x-api-key header)

**Setup**:
1. Visit https://dashboard.shotstack.io/register
2. Create account
3. Navigate to API Keys section
4. Copy staging or production key
5. Set environment variable: `export SHOTSTACK_API_KEY="your_key"`

#### Free Tier
- **20 credits/month** (1 credit = 1 minute of video or 10 images)
- **Watermarked output**
- Access to all core API features
- Staging environment for testing

#### Paid Pricing
- **$0.20/minute** (subscription plans)
- **$0.30/minute** (pay-as-you-go)
- Credit packs start at 200 credits
- No watermarks on paid renders

#### Python SDK Installation
```bash
pip install shotstack-sdk
```

#### Code Example - Basic Video Assembly
```python
import shotstack_sdk as shotstack
from shotstack_sdk.api import edit_api
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.model.title_asset import TitleAsset
from shotstack_sdk.model.clip import Clip
from shotstack_sdk.model.track import Track
from shotstack_sdk.model.timeline import Timeline
from shotstack_sdk.model.output import Output
from shotstack_sdk.model.edit import Edit

# Configure API
host = 'https://api.shotstack.io/stage'
configuration = shotstack.Configuration(host=host)
configuration.api_key['DeveloperKey'] = 'YOUR_SHOTSTACK_KEY'

with shotstack.ApiClient(configuration) as api_client:
    api_instance = edit_api.EditApi(api_client)

    # Create video asset
    video_asset = VideoAsset(
        src='https://example.com/video.mp4',
        trim=3.0  # Trim first 3 seconds
    )

    # Create image overlay
    image_asset = ImageAsset(
        src='https://example.com/logo.png'
    )

    # Create title text
    title_asset = TitleAsset(
        text='My Video Title',
        style='minimal',
        size='medium'
    )

    # Create clips
    video_clip = Clip(
        asset=video_asset,
        start=0.0,
        length=8.0
    )

    image_clip = Clip(
        asset=image_asset,
        start=0.0,
        length=8.0,
        position='top'
    )

    title_clip = Clip(
        asset=title_asset,
        start=0.0,
        length=3.0
    )

    # Assemble tracks (layers)
    track1 = Track(clips=[video_clip])
    track2 = Track(clips=[image_clip])
    track3 = Track(clips=[title_clip])

    # Create timeline
    timeline = Timeline(
        background='#000000',
        tracks=[track1, track2, track3]
    )

    # Define output
    output = Output(
        format='mp4',
        resolution='hd',  # 'sd', 'hd', or '1080'
        fps=25,
        quality='medium'
    )

    # Create edit
    edit = Edit(
        timeline=timeline,
        output=output
    )

    # Submit render
    response = api_instance.post_render(edit)
    render_id = response.response.id

    print(f"Render submitted: {render_id}")

    # Check render status
    import time
    while True:
        status = api_instance.get_render(render_id)
        print(f"Status: {status.response.status}")

        if status.response.status == 'done':
            print(f"Video URL: {status.response.url}")
            break
        elif status.response.status == 'failed':
            print("Render failed")
            break

        time.sleep(5)
```

#### Node.js SDK
```bash
npm install shotstack-sdk
```

```javascript
const Shotstack = require('shotstack-sdk');

const client = Shotstack.ApiClient.instance;
const DeveloperKey = client.authentications['DeveloperKey'];
DeveloperKey.apiKey = 'YOUR_API_KEY';

client.basePath = 'https://api.shotstack.io/stage';

const api = new Shotstack.EditApi();

const videoAsset = new Shotstack.VideoAsset()
  .setSrc('https://example.com/video.mp4')
  .setTrim(3);

const videoClip = new Shotstack.Clip()
  .setAsset(videoAsset)
  .setStart(0)
  .setLength(8);

const track = new Shotstack.Track().setClips([videoClip]);
const timeline = new Shotstack.Timeline().setTracks([track]);

const output = new Shotstack.Output()
  .setFormat('mp4')
  .setResolution('hd');

const edit = new Shotstack.Edit()
  .setTimeline(timeline)
  .setOutput(output);

api.postRender(edit).then((data) => {
  console.log('Render ID:', data.response.id);
});
```

### 4.2 JSON2Video

#### Overview
Simple, flexible video editing API built around JSON structure for scaling video content automation.

#### API Endpoint
**Base URL**: `https://api.json2video.com/v2`

#### Authentication
**Method**: API Key (x-api-key header)

**Setup**:
1. Visit https://json2video.com
2. Create account
3. Generate API key from dashboard
4. Use in requests as header

#### Free Tier
- **600 seconds (10 minutes)** of video for testing
- Full API access
- No watermarks

#### Pricing
- Pay-as-you-go or subscription plans
- Check https://json2video.com/pricing for details

#### Code Example
```python
import requests
import json

api_key = "YOUR_JSON2VIDEO_KEY"
url = "https://api.json2video.com/v2/movies"

# Define video structure in JSON
movie_data = {
    "resolution": "hd",
    "quality": "high",
    "scenes": [
        {
            "duration": 5,
            "background": {
                "type": "image",
                "src": "https://example.com/background.jpg"
            },
            "layers": [
                {
                    "type": "text",
                    "text": "Welcome to JSON2Video",
                    "style": "024",
                    "animation": "fade-in"
                }
            ]
        },
        {
            "duration": 8,
            "background": {
                "type": "video",
                "src": "https://example.com/video.mp4"
            },
            "layers": [
                {
                    "type": "audio",
                    "src": "https://example.com/voiceover.mp3"
                }
            ]
        }
    ]
}

headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}

# Create movie
response = requests.post(url, json=movie_data, headers=headers)
movie_id = response.json()["id"]

print(f"Movie ID: {movie_id}")

# Check status
status_url = f"https://api.json2video.com/v2/movies/{movie_id}"
status_response = requests.get(status_url, headers=headers)
print(status_response.json())
```

### 4.3 Creatomate

#### Overview
Programmatic video generation API with template-based and JSON-based approaches.

#### API Endpoint
**Base URL**: `https://api.creatomate.com/v1`

#### Authentication
**Method**: Bearer token

#### Free Trial
- **50 credits** on signup
- Can produce several hours of video depending on resolution/frame rate

#### Pricing
- Usage-based pricing
- Higher resolutions and frame rates cost more credits

#### Code Example
```python
import requests

api_key = "YOUR_CREATOMATE_KEY"
url = "https://api.creatomate.com/v1/renders"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Using template approach
render_data = {
    "template_id": "your-template-id",
    "modifications": {
        "Text-1": "Dynamic Text Here",
        "Image-1": "https://example.com/image.jpg"
    }
}

# Or using JSON approach for full control
json_data = {
    "output_format": "mp4",
    "width": 1920,
    "height": 1080,
    "frame_rate": 30,
    "elements": [
        {
            "type": "video",
            "source": "https://example.com/video.mp4",
            "duration": 10
        },
        {
            "type": "text",
            "text": "Hello World",
            "x": "50%",
            "y": "50%"
        }
    ]
}

response = requests.post(url, json=json_data, headers=headers)
print(response.json())
```

### 4.4 Remotion (Self-Hosted)

#### Overview
Framework for creating videos programmatically with React. Not a traditional API - you write React code and render videos.

#### Installation
```bash
npm install remotion
```

#### Code Example
```jsx
// MyVideo.jsx
import { useCurrentFrame, interpolate } from 'remotion';

export const MyVideo = () => {
  const frame = useCurrentFrame();

  const opacity = interpolate(
    frame,
    [0, 30],
    [0, 1],
    { extrapolateRight: 'clamp' }
  );

  return (
    <div style={{ flex: 1, backgroundColor: 'white', opacity }}>
      <h1>Frame {frame}</h1>
    </div>
  );
};
```

```javascript
// Render video
const { renderMedia } = require('@remotion/renderer');

await renderMedia({
  composition: 'MyVideo',
  output: 'out/video.mp4',
  inputProps: {},
});
```

#### Pros
- Full programmatic control
- Use React components
- Free (open source)

#### Cons
- Requires infrastructure to render
- Steeper learning curve
- Not a simple REST API

### 4.5 Comparison Table

| Feature | Shotstack | JSON2Video | Creatomate | Remotion |
|---------|-----------|------------|------------|----------|
| **API Type** | REST API | REST API | REST API | Framework |
| **Free Tier** | 20 credits | 600 seconds | 50 credits | Free (OSS) |
| **Pricing** | $0.20-0.30/min | Variable | Variable | Infrastructure costs |
| **Ease of Use** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Flexibility** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Templates** | Yes | Yes | Yes | Code-based |
| **Python SDK** | Yes | REST only | REST only | No |
| **Node SDK** | Yes | REST only | REST only | Native |
| **Best For** | Quick start | Simplicity | Templates | Full control |

### Recommendation
**For your use case**: **Shotstack** or **JSON2Video**
- Both have generous free tiers for testing
- Simple JSON-based configuration
- Good Python/REST API support
- Suitable for automated workflows

---

## 5. YouTube Data API (Publishing)

### Overview
Google's official API for uploading videos, managing channels, playlists, and video metadata.

### API Endpoint
**Base URL**: `https://www.googleapis.com/youtube/v3`

**Key Endpoints**:
- Upload: `POST /youtube/v3/videos`
- Update metadata: `PUT /youtube/v3/videos`
- List videos: `GET /youtube/v3/videos`
- Playlists: `/youtube/v3/playlists`

### Authentication
**Method**: OAuth 2.0

**Setup Process**:

#### 1. Create Google Cloud Project
```
1. Go to https://console.cloud.google.com
2. Click "New Project"
3. Name your project
4. Click "Create"
```

#### 2. Enable YouTube Data API v3
```
1. Navigate to "APIs & Services" > "Library"
2. Search for "YouTube Data API v3"
3. Click on it and press "Enable"
```

#### 3. Create OAuth 2.0 Credentials
```
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure OAuth consent screen (if first time)
4. Choose "Desktop app" or "Web application"
5. Download client_secrets.json
6. Save as client_secrets.json in your project
```

#### 4. OAuth Flow
The first time you run your script, it will:
1. Open a browser window
2. Ask you to log in to Google
3. Request permissions to manage YouTube
4. Generate access and refresh tokens
5. Save tokens for future use

### Quota System
- **Default Quota**: 10,000 units/day
- **Video Upload Cost**: 1,600 units (≈6 videos/day)
- **Quota Reset**: Midnight Pacific Time
- **Increase Requests**: Use [Quota Extension Request Form](https://support.google.com/youtube/contact/yt_api_form)

### Quota Calculator
| Operation | Cost |
|-----------|------|
| Upload video | 1,600 |
| Update video | 50 |
| List videos | 1 |
| Insert comment | 50 |
| Delete video | 50 |

### Python Setup

#### Install Dependencies
```bash
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

#### Code Example - Upload Video
```python
import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """Authenticate and return YouTube service object."""
    creds = None

    # Token file stores access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, video_file, title, description, category='22',
                 privacy='private', tags=None):
    """
    Upload a video to YouTube.

    Args:
        youtube: Authenticated YouTube service
        video_file: Path to video file
        title: Video title
        description: Video description
        category: Category ID (22 = People & Blogs, 28 = Science & Technology)
        privacy: 'public', 'private', or 'unlisted'
        tags: List of tags

    Returns:
        Video ID of uploaded video
    """
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags or [],
            'categoryId': category
        },
        'status': {
            'privacyStatus': privacy,
            'selfDeclaredMadeForKids': False
        }
    }

    # Create MediaFileUpload object
    media = MediaFileUpload(
        video_file,
        chunksize=1024*1024,  # 1MB chunks
        resumable=True
    )

    # Execute upload
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Upload complete! Video ID: {response['id']}")
    return response['id']

# Usage
if __name__ == '__main__':
    # Authenticate
    youtube = get_authenticated_service()

    # Upload video
    video_id = upload_video(
        youtube,
        video_file='my_video.mp4',
        title='My Automated Video',
        description='This video was uploaded programmatically using YouTube Data API',
        category='28',  # Science & Technology
        privacy='public',
        tags=['automation', 'python', 'youtube api']
    )

    print(f"Watch at: https://www.youtube.com/watch?v={video_id}")
```

#### Update Video Metadata
```python
def update_video_metadata(youtube, video_id, title=None, description=None, tags=None):
    """Update video title, description, or tags."""
    # First, get current video details
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    if not response['items']:
        print("Video not found")
        return

    snippet = response['items'][0]['snippet']

    # Update with new values or keep existing
    snippet['title'] = title or snippet['title']
    snippet['description'] = description or snippet['description']
    snippet['tags'] = tags or snippet.get('tags', [])

    # Update the video
    update_response = youtube.videos().update(
        part='snippet',
        body={
            'id': video_id,
            'snippet': snippet
        }
    ).execute()

    print(f"Updated video: {update_response['snippet']['title']}")
    return update_response

# Usage
update_video_metadata(
    youtube,
    video_id='YOUR_VIDEO_ID',
    title='Updated Title',
    description='Updated description with new info',
    tags=['new', 'tags']
)
```

#### Set Video Thumbnail
```python
def set_thumbnail(youtube, video_id, thumbnail_file):
    """Upload custom thumbnail for video."""
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_file)
    ).execute()

    print(f"Thumbnail set for video {video_id}")

# Usage
set_thumbnail(youtube, 'YOUR_VIDEO_ID', 'thumbnail.jpg')
```

### Node.js SDK
```bash
npm install googleapis
```

```javascript
const { google } = require('googleapis');
const fs = require('fs');

// OAuth2 client
const oauth2Client = new google.auth.OAuth2(
  'YOUR_CLIENT_ID',
  'YOUR_CLIENT_SECRET',
  'YOUR_REDIRECT_URL'
);

// Set credentials (after OAuth flow)
oauth2Client.setCredentials({
  access_token: 'YOUR_ACCESS_TOKEN',
  refresh_token: 'YOUR_REFRESH_TOKEN'
});

const youtube = google.youtube({
  version: 'v3',
  auth: oauth2Client
});

// Upload video
async function uploadVideo(filePath, title, description) {
  const response = await youtube.videos.insert({
    part: 'snippet,status',
    requestBody: {
      snippet: {
        title: title,
        description: description,
        categoryId: '22'
      },
      status: {
        privacyStatus: 'private'
      }
    },
    media: {
      body: fs.createReadStream(filePath)
    }
  });

  console.log('Video uploaded:', response.data.id);
  return response.data.id;
}
```

### Category IDs
Common category IDs for videos:
- `1` - Film & Animation
- `10` - Music
- `15` - Pets & Animals
- `17` - Sports
- `20` - Gaming
- `22` - People & Blogs
- `23` - Comedy
- `24` - Entertainment
- `25` - News & Politics
- `26` - Howto & Style
- `27` - Education
- `28` - Science & Technology

### Rate Limits
- Max 6 videos/day with default quota (10,000 units)
- Request quota increase for high-volume needs
- No explicit rate limiting on requests/second
- Reasonable use expected

---

## 6. Complete Workflow Example

Here's an end-to-end Python script that combines all APIs to:
1. Generate an image with FAL.ai
2. Create voiceover with ElevenLabs
3. Assemble video with Shotstack
4. Upload to YouTube

```python
import os
import time
from fal_client import fal
from elevenlabs.client import ElevenLabs
import shotstack_sdk as shotstack
from shotstack_sdk.api import edit_api
from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.model.audio_asset import AudioAsset
from shotstack_sdk.model.clip import Clip
from shotstack_sdk.model.track import Track
from shotstack_sdk.model.timeline import Timeline
from shotstack_sdk.model.output import Output
from shotstack_sdk.model.edit import Edit
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests

class VideoAutomationPipeline:
    """Complete video automation pipeline using multiple APIs."""

    def __init__(self, fal_key, eleven_key, shotstack_key, youtube_secrets):
        # API clients
        fal.config({"credentials": fal_key})
        self.eleven = ElevenLabs(api_key=eleven_key)

        # Shotstack config
        shotstack_host = 'https://api.shotstack.io/v1'
        shotstack_config = shotstack.Configuration(host=shotstack_host)
        shotstack_config.api_key['DeveloperKey'] = shotstack_key
        self.shotstack_client = shotstack.ApiClient(shotstack_config)

        # YouTube config
        self.youtube_secrets = youtube_secrets

    def generate_image(self, prompt):
        """Generate image using FAL.ai Flux."""
        print(f"Generating image: {prompt}")

        result = fal.subscribe("fal-ai/flux/schnell", {
            "input": {
                "prompt": prompt,
                "num_inference_steps": 4
            }
        })

        image_url = result["images"][0]["url"]
        print(f"Image generated: {image_url}")
        return image_url

    def generate_voiceover(self, text, output_file='voiceover.mp3'):
        """Generate voiceover using ElevenLabs."""
        print(f"Generating voiceover: {text[:50]}...")

        audio = self.eleven.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # George voice
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        # Save to file
        with open(output_file, 'wb') as f:
            for chunk in audio:
                if isinstance(chunk, bytes):
                    f.write(chunk)

        print(f"Voiceover saved: {output_file}")
        return output_file

    def upload_asset(self, file_path):
        """Upload asset to temporary hosting (example uses file.io)."""
        print(f"Uploading asset: {file_path}")

        with open(file_path, 'rb') as f:
            response = requests.post(
                'https://file.io',
                files={'file': f}
            )

        upload_url = response.json()['link']
        print(f"Asset uploaded: {upload_url}")
        return upload_url

    def assemble_video(self, image_url, audio_file, output_file='output.mp4'):
        """Assemble video using Shotstack."""
        print("Assembling video with Shotstack...")

        # Upload audio file
        audio_url = self.upload_asset(audio_file)

        # Create assets
        image_asset = ImageAsset(src=image_url)
        audio_asset = AudioAsset(src=audio_url)

        # Get audio duration (approximate - should use proper audio analysis)
        # For this example, assume 10 seconds
        duration = 10.0

        # Create clips
        image_clip = Clip(
            asset=image_asset,
            start=0.0,
            length=duration,
            effect='zoomIn'
        )

        audio_clip = Clip(
            asset=audio_asset,
            start=0.0,
            length=duration
        )

        # Create tracks
        video_track = Track(clips=[image_clip])
        audio_track = Track(clips=[audio_clip])

        # Create timeline
        timeline = Timeline(
            background='#000000',
            tracks=[video_track, audio_track]
        )

        # Define output
        output = Output(
            format='mp4',
            resolution='hd',
            fps=25
        )

        # Create edit
        edit = Edit(timeline=timeline, output=output)

        # Submit render
        api = edit_api.EditApi(self.shotstack_client)
        response = api.post_render(edit)
        render_id = response.response.id

        print(f"Render submitted: {render_id}")

        # Poll for completion
        while True:
            status = api.get_render(render_id)
            print(f"Render status: {status.response.status}")

            if status.response.status == 'done':
                video_url = status.response.url
                print(f"Video rendered: {video_url}")

                # Download video
                video_data = requests.get(video_url).content
                with open(output_file, 'wb') as f:
                    f.write(video_data)

                print(f"Video saved: {output_file}")
                return output_file

            elif status.response.status == 'failed':
                raise Exception("Render failed")

            time.sleep(5)

    def upload_to_youtube(self, video_file, title, description, tags=None):
        """Upload video to YouTube."""
        print("Uploading to YouTube...")

        # Authenticate
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        flow = InstalledAppFlow.from_client_secrets_file(
            self.youtube_secrets, SCOPES)
        creds = flow.run_local_server(port=0)

        youtube = build('youtube', 'v3', credentials=creds)

        # Upload
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': '28'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(video_file, resumable=True)

        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        video_id = response['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Upload complete: {video_url}")

        return video_id, video_url

    def create_and_publish_video(self, image_prompt, voiceover_text,
                                 title, description, tags=None):
        """Complete end-to-end workflow."""
        print("=" * 60)
        print("STARTING VIDEO AUTOMATION PIPELINE")
        print("=" * 60)

        # Step 1: Generate image
        image_url = self.generate_image(image_prompt)

        # Step 2: Generate voiceover
        audio_file = self.generate_voiceover(voiceover_text)

        # Step 3: Assemble video
        video_file = self.assemble_video(image_url, audio_file)

        # Step 4: Upload to YouTube
        video_id, video_url = self.upload_to_youtube(
            video_file, title, description, tags
        )

        print("=" * 60)
        print("PIPELINE COMPLETE!")
        print(f"Video URL: {video_url}")
        print("=" * 60)

        return {
            'video_id': video_id,
            'video_url': video_url,
            'image_url': image_url,
            'video_file': video_file
        }

# Usage example
if __name__ == '__main__':
    pipeline = VideoAutomationPipeline(
        fal_key=os.getenv('FAL_KEY'),
        eleven_key=os.getenv('ELEVEN_API_KEY'),
        shotstack_key=os.getenv('SHOTSTACK_API_KEY'),
        youtube_secrets='client_secrets.json'
    )

    result = pipeline.create_and_publish_video(
        image_prompt="A futuristic AI datacenter with glowing servers, cyberpunk style",
        voiceover_text="Welcome to the future of artificial intelligence. "
                      "In this video, we explore how AI is transforming our world.",
        title="The Future of AI - Automated Video",
        description="This video was created entirely using AI APIs:\n"
                   "- Image: FAL.ai Flux\n"
                   "- Voiceover: ElevenLabs\n"
                   "- Video Assembly: Shotstack\n"
                   "- Published: YouTube Data API",
        tags=['AI', 'automation', 'artificial intelligence', 'future tech']
    )

    print("\nFinal result:")
    print(result)
```

---

## Summary & Recommendations

### API Status Overview

| Tool | API Available | Auth Method | Free Tier | Best For |
|------|---------------|-------------|-----------|----------|
| **FAL.ai** | ✅ Yes | API Key | Check dashboard | Image generation |
| **ElevenLabs** | ✅ Yes | API Key | Limited quota | Text-to-speech |
| **SpeedSketch** | ❌ No | N/A | Free web app | Manual whiteboard |
| **Shotstack** | ✅ Yes | API Key | 20 credits/month | Video assembly |
| **JSON2Video** | ✅ Yes | API Key | 600 seconds | Simple videos |
| **Creatomate** | ✅ Yes | Bearer token | 50 credits | Template videos |
| **YouTube** | ✅ Yes | OAuth 2.0 | 10K units/day | Publishing |

### Recommended Stack

For a complete automated video pipeline:

1. **Image Generation**: FAL.ai Flux (fast, flexible, good API)
2. **Text-to-Speech**: ElevenLabs (high quality, good voices)
3. **Video Assembly**: Shotstack (best API, good docs, generous free tier)
4. **Publishing**: YouTube Data API (official, well-documented)
5. **Whiteboard Animation**: Manual upload to SpeedSketch or use alternative

### Cost Estimation (Monthly)

**Free Tier Maximums**:
- FAL.ai: TBD (check dashboard)
- ElevenLabs: ~10K characters/month (varies)
- Shotstack: 20 minutes of video
- YouTube: 6 videos/day (10K quota units)

**Paid Tier Example** (100 videos/month):
- FAL.ai: ~$10-20 (estimate)
- ElevenLabs: ~$5-22/month (Starter plan)
- Shotstack: ~$40 (200 minutes at $0.20/min)
- YouTube: Free or request quota increase
- **Total**: ~$60-85/month for 100 automated videos

### Next Steps

1. **Sign up for all services** and generate API keys
2. **Test individual APIs** with simple examples
3. **Build pipeline incrementally** (image → audio → video → upload)
4. **Handle errors and retries** for production use
5. **Monitor quota usage** to avoid hitting limits
6. **Consider caching** to reduce API costs

---

## Sources

### FAL.ai
- [FLUX API Overview](https://fal.ai/flux)
- [FLUX.1 [dev] API](https://fal.ai/models/fal-ai/flux/dev)
- [FAL.ai Quickstart](https://docs.fal.ai/quick-start/)

### ElevenLabs
- [Text-to-Speech API Reference](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
- [ElevenLabs Developer Documentation](https://elevenlabs.io/developers)
- [ElevenLabs Python SDK](https://github.com/elevenlabs/elevenlabs-python)
- [API Pricing](https://elevenlabs.io/pricing/api)

### SpeedSketch
- [SpeedSketch Homepage](https://www.speedsketch.co.uk/)
- [Whiteboard Animation Maker](https://www.speedsketch.co.uk/whiteboard-animation-maker)

### Video Assembly
- [Shotstack API Documentation](https://shotstack.io/docs/api/)
- [Shotstack Pricing](https://shotstack.io/pricing/)
- [Shotstack Python SDK](https://github.com/shotstack/shotstack-sdk-python)
- [Best Video Editing APIs 2025](https://www.plainlyvideos.com/blog/best-video-editing-api)
- [JSON2Video](https://json2video.com/)
- [Creatomate](https://creatomate.com/how-to/programmatic-video-editing)
- [Remotion](https://www.remotion.dev/)

### YouTube
- [YouTube Data API Overview](https://developers.google.com/youtube/v3/getting-started)
- [Python Quickstart](https://developers.google.com/youtube/v3/quickstart/python)
- [Upload Video Guide](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [Quota and Compliance](https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits)
- [YouTube API Samples](https://github.com/youtube/api-samples)

### Alternatives & Comparisons
- [7 Best AI Video Generator APIs](https://shotstack.io/learn/best-ai-video-generator-api/)
- [HeyGen API Review & Alternatives](https://www.tavus.io/post/heygen-api)
- [Best Synthesia Alternatives](https://www.heygen.com/blog/synthesia-alternatives-competitors)
- [Canva API Guide](https://zuplo.com/blog/2025/03/28/canva-api)

---

**Document Version**: 1.0
**Last Updated**: December 10, 2025
**Maintained By**: AI Infrastructure Team
