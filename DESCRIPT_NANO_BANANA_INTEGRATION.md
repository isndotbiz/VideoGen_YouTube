# Descript + Nano Banana Integration Guide

Complete guide to using **Descript** for video editing + **Nano Banana** for text-based images.

## Quick Overview

### What Changed

| Component | Old | New |
|-----------|-----|-----|
| **Text-to-Video Editing** | Manual Shotstack | **Descript API** |
| **Script Humanization** | Claude only | **Descript humanizer** |
| **Auto-Captions** | Manual Canva | **Descript auto-captions** |
| **Photorealistic Images** | Flux Pro | **Flux Pro** ✓ (same) |
| **Text/Charts** | Flux Pro (bad) | **Nano Banana** (excellent) |
| **Video Assembly** | Shotstack | **Descript** (integrated) |

### Why Descript?

✓ Auto-captions (saves hours)
✓ Humanizer (makes speech sound natural)
✓ Integrated video editing (no manual assembly)
✓ One-click subtitle styling
✓ Professional quality output

### Why Nano Banana?

✓ Excellent text rendering (Flux Pro can't do text)
✓ Charts look professional
✓ Clear infographics
✓ Cheaper than DALL-E 3
✓ Fast generation
✓ Built on FAL.ai (same place as Flux Pro)

---

## Step 1: Request Your Descript API Key

### How to Get It

Descript requires you to request API access directly (no self-service).

**Email Descript Support:**

```
To: support@descript.com

Subject: Request API Access - Personal Token

Body:
I have a $30/month Descript account and need to enable API access
for my video generation/automation project. Can you provide my
personal API token?
```

**Or use the contact form:**
https://www.descript.com/contact

### Wait for Response

- Response time: 24-48 hours
- They'll send your personal token via email
- Token format: `descript_sk_xxxxxxxxxxxxxxxxxxxxx`

### Add to .env

Once you receive your token:

```bash
# Edit .env file
nano .env

# Add this line:
DESCRIPT_API_KEY=descript_sk_YOUR_TOKEN_FROM_EMAIL

# Save and exit
```

### Test Your Key

```bash
node descript-video-editor.js --test
```

Should show:
```
✓ API Key found
✓ Token starts with: descript_sk_...
Ready to use Descript API!
```

---

## Step 2: Remove Old Text-Based Images

Delete images from the previous pipeline that had text:

### Images to DELETE

```bash
# These used Flux Pro for text (which doesn't work well)
rm output/generated_images/infographic/*.png
rm output/generated_images/metadata.json

# OR manually delete these image IDs:
# - flux_chart_* (any chart)
# - flux_timeline_* (any timeline)
# - flux_table_* (any table)
# - flux_steps_* (any numbered steps)
# - flux_comparison_* (any comparison)
```

### Keep These Images

```bash
# Keep photorealistic people/environment images:
output/generated_images/photorealistic/
  - people_* (teams, individuals)
  - environment_* (offices, workspaces)
  - detail_* (hands, close-ups)
  - workspace_* (desk setups)
```

### Clean Up

```bash
# See what's there:
ls -la output/generated_images/

# Verify metadata:
cat output/generated_images/metadata.json | grep -E "flux_chart|flux_table|flux_timeline"
```

---

## Step 3: Generate NEW Images with Nano Banana

Run the updated pipeline:

```bash
python image-generation-nano-banana.py
```

**What happens**:

1. **Flux Pro generates** (5 images):
   - Professional woman at desk
   - Diverse team collaborating
   - Hands typing (close-up)
   - Modern workspace
   - Woman presenting

2. **Nano Banana generates** (7 images):
   - Bar chart: Ranking factors
   - Timeline: Google updates
   - Comparison table: SEO vs PPC vs Social
   - 5-step implementation process
   - Myths vs Reality
   - Funnel diagram
   - Keyword priority matrix

**Total: 12 professional images** (vs. confusing mixed results)

**Output**:
```
output/generated_images/
├── flux_people_1.png              ← Photorealistic
├── flux_people_2.png
├── flux_team_1.png
├── flux_closeup_1.png
├── flux_workspace_1.png
├── nano_chart_ranking_factors.png ← Text/charts
├── nano_timeline_algo_updates.png
├── nano_comparison_table.png
├── nano_steps_implementation.png
├── nano_myths_reality.png
├── nano_funnel_conversion.png
├── nano_keywords_priority.png
└── metadata_nano_banana.json      ← Updated metadata
```

---

## Step 4: Updated Video Assembly with Descript

### New Workflow

```bash
# 1. Generate images (done above)
python image-generation-nano-banana.py

# 2. Generate narration
node script-synthesizer.js

# 3. Import to Descript for editing
node descript-video-editor.js --workflow s3://bucket/video.mp4 SEO_Best_Practices
```

### What Descript Does

**Automatically**:
- ✓ Transcribes narration
- ✓ Generates captions (SRT format)
- ✓ Syncs captions to video
- ✓ Detects speaker segments
- ✓ Identifies music/background noise
- ✓ Applies styling (white text, pink border)
- ✓ Exports final video

**In Descript UI** (optional):
- Edit transcription
- Adjust caption timing
- Add/remove filler words
- Adjust pacing
- Add effects

---

## Step 5: Complete Pipeline Workflow

### Option A: Full Automation

```bash
#!/bin/bash
# generate_video.sh

PROJECT="SEO_Best_Practices"

# 1. Scrape URLs
echo "Step 1: FireCrawl scraping..."
node firecrawl-data-manager.js --project $PROJECT

# 2. Generate images (Flux + Nano Banana)
echo "Step 2: Generating images..."
python image-generation-nano-banana.py

# 3. Generate script
echo "Step 3: Generating script..."
node script-synthesizer.js

# 4. Generate narration
echo "Step 4: Generating narration..."
python elevenlabs-narrator.py

# 5. Send to Descript
echo "Step 5: Descript editing..."
node descript-video-editor.js --workflow ./output/narration.mp3 $PROJECT

echo "Complete! Check Descript for final video."
```

### Option B: Step-by-Step Manual

```bash
# Step 1: Scrape
node firecrawl-data-manager.js --project SEO_Best_Practices

# Step 2: Images
python image-generation-nano-banana.py

# Step 3: Script
node script-synthesizer.js

# Step 4: Narration
python elevenlabs-narrator.py

# Step 5: Descript
node descript-video-editor.js --test  # Verify API key first
node descript-video-editor.js --humanize output/narration.mp3 output/script.md

# Step 6: Go to Descript UI and complete editing
open https://www.descript.com
```

---

## Descript API Endpoints You're Using

### 1. Edit in Descript (Import)

```
POST https://descriptapi.com/v1/edit_in_descript/schema
```

**What it does**: Creates import URL for Descript

**Request**:
```json
{
  "project_schema": {
    "schema_version": "1.0.0",
    "files": [
      {
        "uri": "s3://bucket/video.mp4",
        "name": "SEO_Best_Practices"
      }
    ]
  }
}
```

**Response**:
```json
{
  "url": "https://web.descript.com/import?nonce=..."
}
```

### 2. Getting Transcript & Captions

Once in Descript, it auto-generates:
- Transcription (text)
- SRT captions (timed)
- Speaker identification
- Scene detection

### 3. Export Video

After editing in Descript UI:
- Video with captions
- SRT caption file
- Transcript
- Metadata

---

## Image Selection Guide

### When to Use Flux Pro

✓ Opening scene with professional
✓ Team collaboration shots
✓ Hands working on keyboard
✓ Office workspace setup
✓ Presentation scenes
✓ Closing scene with person

**Show time**: 4-8 seconds each

### When to Use Nano Banana

✓ Bar charts (show data)
✓ Timelines (show history)
✓ Tables (show comparisons)
✓ Process flows (numbered steps)
✓ Myth/reality cards
✓ Funnels (show progression)
✓ Matrices (2x2 grids)

**Show time**: 6-10 seconds each (viewers need time to read)

### Alternating Pattern

```
Scene 1: Flux (Woman at desk) - 5s
Scene 2: Nano (Bar chart) - 8s
Scene 3: Flux (Team) - 5s
Scene 4: Nano (Timeline) - 8s
Scene 5: Flux (Hands typing) - 5s
Scene 6: Nano (Comparison) - 8s
...continues...
```

This keeps viewers engaged with variety!

---

## FAL.ai Nano Banana Details

### What is Nano Banana?

A text-to-image model specialized in:
- Text rendering (clear, readable)
- Diagrams and infographics
- Charts with legible text
- Professional design elements
- UI mockups

### How to Call It

```python
import requests

response = requests.post(
    'https://api.fal.ai/v1/nano-banana/text-to-image',
    headers={'Authorization': f'Key {FAL_API_KEY}'},
    json={
        'prompt': 'Create a bar chart showing...',
        'image_size': '1920x1080',
        'num_inference_steps': 30,
    }
)

image_url = response.json()['images'][0]['url']
```

### Cost Comparison

```
Flux Pro (photorealistic): $0.04-0.08 per image
Nano Banana (text): $0.02-0.04 per image
DALL-E 3 (text): $0.08-0.20 per image
Midjourney (text): ~$0.10 per image
```

**Nano Banana wins on cost + quality for text!**

---

## Complete File Reference

### New Files Created

```
DESCRIPT_API_SETUP.md                    ← How to find your API key
DESCRIPT_NANO_BANANA_INTEGRATION.md      ← This file
descript-video-editor.js                 ← Descript API integration
image-generation-nano-banana.py          ← Flux + Nano Banana pipeline
```

### Updated Files

```
.env                                     ← Add DESCRIPT_API_KEY
advanced-video-orchestrator.js           ← Can use Descript option
```

### Files to DELETE

```
old_image_generation_pipeline.py          ← Replace with nano-banana version
output/generated_images/infographic/      ← Old Flux text attempts
output/generated_images/metadata.json     ← Old metadata (use metadata_nano_banana.json)
```

---

## Troubleshooting

### "Descript API key not found"

```bash
# Check .env has the key
cat .env | grep DESCRIPT

# Should show:
# DESCRIPT_API_KEY=descript_sk_xxxxx

# If not, add it:
echo "DESCRIPT_API_KEY=your_token" >> .env
```

### "Nano Banana images look low quality"

- Increase prompt detail (more specific description)
- Use professional design terminology
- Include color scheme in prompt
- Add "professional infographic style" to prompt

### "Descript API returns 403 Forbidden"

- Check token is correct
- Verify token isn't expired
- Test at https://www.descript.com/settings/api
- Generate new token if needed

### "Images taking too long"

Nano Banana can take 10-30 seconds per image. This is normal. To speed up:
- Reduce num_inference_steps (quality may decrease)
- Use smaller image size (not recommended for video)
- Batch requests if possible

---

## Next Steps

### 1. Get Your API Key (Right Now)
```bash
# Go to: https://www.descript.com/settings/api
# Copy token
# Add to .env as DESCRIPT_API_KEY
```

### 2. Test Descript API
```bash
node descript-video-editor.js --test
```

### 3. Generate Images with Nano Banana
```bash
python image-generation-nano-banana.py
```

### 4. Test Full Workflow
```bash
node firecrawl-data-manager.js --project SEO_Best_Practices
python image-generation-nano-banana.py
node script-synthesizer.js
node descript-video-editor.js --workflow s3://bucket/video.mp4 SEO_Best_Practices
```

---

## Why This Setup is Better

✓ **Descript**: Professional captions automatically (no manual work)
✓ **Nano Banana**: Text looks good (unlike Flux Pro)
✓ **Combined**: Complete video pipeline in 2 tools instead of 4+
✓ **Cost**: Cheaper and faster than previous setup
✓ **Quality**: Better results for both people and charts
✓ **Integration**: Seamless workflow from script to YouTube

---

**You're ready to create professional videos with Descript + Nano Banana!**

Questions? See:
- `DESCRIPT_API_SETUP.md` - Finding your API key
- `descript-video-editor.js` - API integration code
- `image-generation-nano-banana.py` - Image generation with Nano Banana
