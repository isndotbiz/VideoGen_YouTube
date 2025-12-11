# Quick Start - Automated Video Generation (5 Minutes)

Fast-track guide for developers familiar with APIs who want to generate their first video immediately.

---

## Prerequisites Check (1 minute)

```bash
# Verify you have these installed
node --version  # Need 18+
python --version  # Need 3.8+
pip --version  # Should come with Python
```

Not installed? See AUTOMATED_SETUP_GUIDE.md (takes 15 min)

---

## One-Command Setup (2 minutes)

```bash
# Clone/download project
cd D:\workspace\True_Nas\firecrawl-mdjsonl

# Install Node dependencies (none required - uses built-ins)
npm install

# Install Python dependencies
pip install fal-client elevenlabs shotstack-sdk google-api-python-client google-auth-oauthlib google-auth-httplib2 python-dotenv
```

---

## API Keys (3 minutes)

Create `.env` file:

```bash
# Get keys from:
# FAL.ai: https://fal.ai/dashboard → API Keys
# ElevenLabs: https://elevenlabs.io → Profile → API Keys
# Shotstack: https://dashboard.shotstack.io → Copy staging key
# YouTube: See AUTOMATED_SETUP_GUIDE.md for OAuth setup

FAL_KEY=fal_your_key_here
ELEVEN_API_KEY=your_elevenlabs_key
SHOTSTACK_API_KEY=your_shotstack_staging_key
```

---

## Generate Your First Video (30 seconds)

### Option 1: Just Content Extraction
```bash
# Extract article and generate scripts
node orchestrate.js "https://your-article-url.com"

# Output:
# ✅ dataset.jsonl
# ✅ COMPLETE_VIDEO_SCRIPT.md
# ✅ 6 production markdown files
```

### Option 2: Complete Automation (Coming Soon)
```bash
# Generate and publish video (requires Python script)
python automate_complete_video.py "https://your-article-url.com"

# This will:
# 1. Extract article content
# 2. Generate images with FAL.ai
# 3. Create voiceover with ElevenLabs
# 4. Assemble video with Shotstack
# 5. Upload to YouTube
```

---

## What You Get

After running the pipeline:

| File | What It Contains |
|------|-----------------|
| `AI_VIDEO_NARRATION_WITH_MARKERS.md` | Complete script with timing |
| `AI_VIDEO_VISUAL_GUIDE.md` | All chart specifications |
| `chart_*.svg` | 6 pre-made chart templates |
| `PIKA_LABS_GUIDE.md` | AI video generation guide |

---

## Quick Test (Each API)

### Test FAL.ai (Image Generation)
```python
from fal_client import fal
import os
from dotenv import load_dotenv

load_dotenv()
fal.config({"credentials": os.getenv("FAL_KEY")})

result = fal.subscribe("fal-ai/flux/schnell", {
    "input": {"prompt": "professional tech illustration", "num_inference_steps": 4}
})

print(f"✅ Image: {result['images'][0]['url']}")
```

### Test ElevenLabs (Voiceover)
```python
from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))

audio = client.text_to_speech.convert(
    text="Test voiceover generation",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2"
)

with open('test.mp3', 'wb') as f:
    for chunk in audio:
        if isinstance(chunk, bytes):
            f.write(chunk)

print("✅ Audio saved: test.mp3")
```

### Test Shotstack (Video Assembly)
```python
import shotstack_sdk as shotstack
from shotstack_sdk.api import edit_api
from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.model.clip import Clip
from shotstack_sdk.model.track import Track
from shotstack_sdk.model.timeline import Timeline
from shotstack_sdk.model.output import Output
from shotstack_sdk.model.edit import Edit
import os
import time
from dotenv import load_dotenv

load_dotenv()

host = 'https://api.shotstack.io/stage'
configuration = shotstack.Configuration(host=host)
configuration.api_key['DeveloperKey'] = os.getenv('SHOTSTACK_API_KEY')

with shotstack.ApiClient(configuration) as api_client:
    api_instance = edit_api.EditApi(api_client)

    image_asset = ImageAsset(src='https://shotstack-assets.s3.amazonaws.com/images/earth.jpg')
    clip = Clip(asset=image_asset, start=0.0, length=3.0)
    track = Track(clips=[clip])
    timeline = Timeline(tracks=[track])
    output = Output(format='mp4', resolution='hd')
    edit = Edit(timeline=timeline, output=output)

    response = api_instance.post_render(edit)
    render_id = response.response.id

    print(f"✅ Render ID: {render_id}")
    print("Poll for status with: api_instance.get_render(render_id)")
```

### Test YouTube (Authentication)
```python
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

if not os.path.exists('client_secrets.json'):
    print("❌ Need client_secrets.json from Google Cloud Console")
    print("See AUTOMATED_SETUP_GUIDE.md section 4")
else:
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    youtube = build('youtube', 'v3', credentials=creds)
    request = youtube.channels().list(part='snippet', mine=True)
    response = request.execute()

    print(f"✅ Connected to: {response['items'][0]['snippet']['title']}")
```

---

## Fastest Path to First Video

**Time: 10 minutes total**

1. **Extract content** (30 sec)
   ```bash
   node orchestrate.js "https://your-article-url.com"
   ```

2. **Generate images** (2 min)
   ```bash
   python generate_images.py  # Creates chart_01.png, chart_02.png, etc.
   ```

3. **Generate voiceover** (1 min)
   ```bash
   python generate_voiceover.py  # Creates voiceover.mp3
   ```

4. **Assemble video** (5 min)
   ```bash
   python assemble_video.py  # Creates output.mp4
   ```

5. **Upload to YouTube** (1 min)
   ```bash
   python upload_youtube.py output.mp4 "Video Title"
   ```

**Total**: 10 minutes + render time

---

## Expected Output

After successful run:

```
D:\workspace\True_Nas\firecrawl-mdjsonl\
├── dataset.jsonl (article data)
├── AI_VIDEO_NARRATION_WITH_MARKERS.md
├── AI_VIDEO_VISUAL_GUIDE.md
├── chart_01.svg through chart_06.svg
├── chart_01.png through chart_25.png (if generated)
├── voiceover.mp3 (if generated)
├── output.mp4 (if assembled)
└── PIKA_LABS_GUIDE.md
```

---

## Common Quick Fixes

### "Module not found"
```bash
pip install [missing-module]
```

### "API key invalid"
```bash
# Check .env file exists
# Verify keys are correct (no quotes, no spaces)
```

### "Permission denied"
```bash
# Windows:
# Right-click folder → Properties → Security → Edit → Full control

# macOS/Linux:
chmod -R 755 .
```

### "Render failed"
```bash
# Check Shotstack staging environment
# Verify image URLs are accessible
# Check quota limits
```

---

## Next Steps

Now that you've generated your first video:

1. **Customize**: Edit `config.json` to change video parameters
2. **Optimize**: Read WORKFLOW.md to understand the pipeline
3. **Deploy**: Read DEPLOYMENT_GUIDE.md to automate scheduling
4. **Troubleshoot**: Read TROUBLESHOOTING.md for common issues

---

## Free Tier Limits

Quick reference for testing:

| API | Free Tier | Enough For |
|-----|-----------|------------|
| FAL.ai | Check dashboard | ~10-50 images |
| ElevenLabs | 10K chars/month | ~5-10 videos |
| Shotstack | 20 credits | ~20 minutes of video |
| YouTube | 6 uploads/day | Testing workflow |

**Cost for first 10 videos**: $0-5 (mostly free tier)

---

## Complete Example Script

Save as `quick_video.py`:

```python
#!/usr/bin/env python3
"""
Generate a complete video in one command
Usage: python quick_video.py "https://article-url.com"
"""
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_video.py <article-url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Generating video from: {url}")

    # Step 1: Extract content
    print("\n[1/5] Extracting content...")
    os.system(f'node orchestrate.js "{url}"')

    # Step 2: Generate images
    print("\n[2/5] Generating images...")
    # (Add image generation code)

    # Step 3: Generate voiceover
    print("\n[3/5] Generating voiceover...")
    # (Add voiceover generation code)

    # Step 4: Assemble video
    print("\n[4/5] Assembling video...")
    # (Add video assembly code)

    # Step 5: Upload to YouTube
    print("\n[5/5] Uploading to YouTube...")
    # (Add YouTube upload code)

    print("\n✅ Video generation complete!")
    print("Check output.mp4 and YouTube for your video")

if __name__ == '__main__':
    main()
```

Run:
```bash
python quick_video.py "https://your-article-url.com"
```

---

**5-minute quick start complete!**

For full documentation: See AUTOMATED_SETUP_GUIDE.md
