# N8N Video - Complete Shotstack + S3 Production Pipeline

## Overview

This guide shows how to composite your N8N video using Shotstack and S3:
1. **Upload** all 10 infographics to S3
2. **Compose** video with Shotstack (professional rendering)
3. **Download** final video from S3
4. **Upload** to YouTube

---

## What You Have Ready

### ✅ 10 Custom Infographics
All generated and saved locally:
```
output/n8n_infographics_final/
├── 01_n8n_logo_overview.jpg
├── 02_400_app_integrations.jpg
├── 03_free_opensource_selfhosted.jpg
├── 04_integration_showcase.jpg
├── 05_scalability_simple_to_enterprise.jpg
├── 06_agency_contact_form_workflow.jpg
├── 07_ecommerce_order_automation.jpg
├── 08_automation_agency_business_opportunity.jpg
├── 09_getting_started_installation.jpg
└── 10_call_to_action_future.jpg
```

### ✅ Audio Files
- Narration: `output/n8n_3min_final/narration.mp3`
- Music: `background_music/ES_2 Broken Hearts (Instrumental Version) - Particle House.mp3`

### ✅ Subtitles (3 formats)
- SRT: `output/n8n_subtitles/n8n_3min_subtitles.srt`
- VTT: `output/n8n_subtitles/n8n_3min_subtitles.vtt`
- JSON: `output/n8n_subtitles/n8n_3min_subtitles.json`

---

## Step-by-Step: Using Shotstack + S3

### Step 1: Verify AWS Credentials

Check your `.env` file has:
```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket-name
```

### Step 2: Verify Shotstack API Key

Check your `.env` file has:
```
SHOTSTACK_API_KEY=your_key
```

### Step 3: Install Required Libraries

```bash
pip install boto3 requests
```

### Step 4: Run Complete Pipeline

```bash
python n8n_complete_production_pipeline.py
```

This will:
1. Upload all infographics to S3
2. Upload audio files to S3
3. Create Shotstack composition JSON
4. Submit render to Shotstack
5. Wait for rendering (2-5 minutes)
6. Download final video
7. Generate production report

### Step 5: Upload to YouTube

```bash
# Download final video
# File: output/n8n_shotstack/n8n_3min_shotstack_final.mp4
# Subtitles: output/n8n_subtitles/n8n_3min_subtitles.srt

# Go to YouTube Studio
# Upload video
# Add SRT file as captions
# Publish!
```

---

## Shotstack Composition Timeline

### Image Transitions (Synced to Audio):

```
0:00 - 0:15s   → [1] N8N Logo Overview
                ↓ (0.5s fade)
0:15 - 0:45s   → [2] 400+ App Integrations
                ↓ (0.5s fade)
0:45 - 1:15s   → [3] Free/Open-Source Benefits
                ↓ (0.5s fade)
1:15 - 1:45s   → [4] Integration Showcase
                ↓ (0.5s fade)
1:45 - 2:15s   → [5] Scalability Simple to Enterprise
                ↓ (0.5s fade)
2:15 - 2:45s   → [6] Agency Workflow Example
                ↓ (0.5s fade)
2:45 - 3:10s   → [7] E-Commerce Workflow
                ↓ (0.5s fade)
3:10 - 3:30s   → [8] Business Opportunity
                ↓ (0.5s fade)
3:30 - 3:45s   → [9] Getting Started
                ↓ (0.5s fade)
3:45 - 4:00s   → [10] Call to Action
```

### Audio Mix:
- **Narration:** 100% volume (narration.mp3)
- **Music:** 15% volume (background music)
- **Duration:** 180 seconds total

---

## Shotstack Video Specs

### Output Format:
- Format: MP4
- Resolution: 1920×1080
- Aspect Ratio: 16:9
- Frame Rate: 24 FPS
- Quality: High

### Video Encoding:
- Codec: H.264 (libx264)
- Audio: AAC
- Bitrate: Optimized

---

## File Flow

```
Local Files
    ↓
[S3 Upload]
    ↓
S3 Bucket (Infographics + Audio)
    ↓
[Shotstack Composition]
    ↓
Shotstack API
    ↓
Render Server
    ↓
[Polling for completion]
    ↓
Complete Video (S3)
    ↓
[Download]
    ↓
output/n8n_shotstack/n8n_3min_shotstack_final.mp4
    ↓
[Upload to YouTube]
    ↓
YouTube (Published!)
```

---

## Cost Breakdown

| Service | Cost |
|---------|------|
| ElevenLabs Narration | $0.10 |
| FAL.ai Infographics (10) | $0.60 |
| Shotstack Rendering | ~$0.50 |
| S3 Storage | ~$0.01 |
| **Total** | **~$1.21 USD** |

**Agency equivalent: $2,000-$5,000**
**Your savings: 99.94%**

---

## Troubleshooting

### S3 Upload Fails
- Check AWS credentials in .env
- Verify S3 bucket exists and you have access
- Ensure AWS_REGION is correct (e.g., us-east-1)

### Shotstack Rendering Fails
- Check SHOTSTACK_API_KEY in .env
- Verify Shotstack account has credits
- Check file paths in composition JSON

### Video Quality Issues
- Shotstack quality setting: "high"
- Resolution: 1920×1080 confirmed
- Frame rate: 24 FPS confirmed

### Timeout Issues
- Shotstack renders typically take 2-5 minutes
- Max wait time set to 10 minutes
- Check Shotstack dashboard for status

---

## Alternative: Direct FFmpeg (Faster, Local)

If you want to skip Shotstack and use local FFmpeg instead:

```bash
python create_3min_n8n_final.py
```

This creates the video locally (much faster) without using Shotstack/S3.

---

## Files You'll Get

After running the complete pipeline:

```
output/n8n_shotstack/
├── n8n_3min_shotstack_final.mp4 ← MAIN VIDEO
└── [download logs]

output/n8n_subtitles/
├── n8n_3min_subtitles.srt ← Use this on YouTube
├── n8n_3min_subtitles.vtt
└── n8n_3min_subtitles.json

output/n8n_infographics_final/
├── 01_n8n_logo_overview.jpg
├── 02_400_app_integrations.jpg
├── [... 8 more images ...]
└── 10_call_to_action_future.jpg

output/N8N_PRODUCTION_REPORT.json ← Full report
output/n8n_s3_urls.json ← S3 URLs for reference
```

---

## YouTube Upload

1. Go to YouTube Studio
2. Click "Create" → "Upload Video"
3. Select: `output/n8n_shotstack/n8n_3min_shotstack_final.mp4`
4. Title: "N8N Workflow Automation Mastery - 3 Minute Guide"
5. Add caption file: `output/n8n_subtitles/n8n_3min_subtitles.srt`
6. Category: Education
7. Publish!

---

## Complete Cost Summary

### What You Get:
✅ 3-minute professional video
✅ 10 custom AI infographics
✅ Professional narration (ElevenLabs)
✅ Background music (instrumental)
✅ Subtitles (3 formats)
✅ Professional rendering (Shotstack)
✅ Cloud storage (S3)

### Total Cost:
**~$1.21 USD**

### Agency Cost:
**$2,000-$5,000**

### Your Savings:
**99.94%** 🎉

---

## Next Videos

Using the same pipeline, you can produce:
- FLUX AI (Image generation)
- ComfyUI (Workflows)
- SEO Best Practices
- Any other topic

Each video production will cost ~$1.20 USD.

---

## Support

For issues:
1. Check Shotstack dashboard: https://dashboard.shotstack.io
2. Check AWS S3 console: https://console.aws.amazon.com/s3
3. Review your .env file credentials
4. Check API usage limits

---

**Status: READY TO PRODUCE**

Run the complete pipeline now:
```bash
python n8n_complete_production_pipeline.py
```

Your professional video will be ready in 5-10 minutes! 🚀
