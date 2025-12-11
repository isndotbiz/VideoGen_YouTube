# Runway ML Setup Guide

Complete guide to using Runway ML for cinematic video generation.

---

## What is Runway ML?

**Runway Gen-3** generates high-quality videos from:
- Still images → 3-5 second video clips
- Text prompts describing motion/camera movement
- Professional cinematic results
- Ultra HD quality (perfect for YouTube)

**Perfect for**:
- Opening/closing sequences
- Scene transitions
- Cinematic montages
- Dynamic content visualization

---

## Step 1: Get Your Runway API Key

### 1a. Go to Runway Dashboard

```
https://app.runwayml.com
```

### 1b. Sign Up (or Log In)

- Create account if needed
- Free plan available to test

### 1c. Find API Key

1. Click your **Profile** (bottom left)
2. Select **API**
3. Click **Create API Key**
4. Copy the key (looks like: `sk_xyz...`)

### 1d. Add to .env

```bash
# Edit .env
nano .env

# Add:
RUNWAY_API_KEY=sk_YOUR_KEY_HERE

# Save (Ctrl+X, Y, Enter)
```

### 1e. Test Connection

```bash
node runway-video-generator.js --test

# Should show:
# ✓ API Key found
# ✓ Token: sk_xyz...
# ✓ Ready to generate videos!
```

---

## Step 2: Understand Runway Pricing

### Cost per Video Generation

```
Image to Video (3-5 seconds):  $0.05-0.10 per video
Resolution: Up to 1920x1080
Processing time: 30-60 seconds per video
Quality: Ultra HD / Cinema grade
```

### Budget for 10 Minute Video

```
5 Runway videos (3-5s each):  $0.25-0.50
FAL.ai Flux images (5):       $0.30
FAL.ai Nano Banana (7):       $0.15
ElevenLabs narration:         $0.50

TOTAL:                        $1.20-1.45 per video
10 videos/month:              $12-15
```

---

## Step 3: Generate Video

### Quick Test

```bash
node runway-video-generator.js --batch
```

This will:
1. Create 5 example video generation tasks
2. Queue them with Runway
3. Show estimated completion time (5-10 minutes)

### Monitor Generation

Go to: https://app.runwayml.com/queue

- Watch videos process
- See progress for each
- Download when complete

### Check Specific Task

```bash
node runway-video-generator.js --status runway_task_seo_1
```

Shows:
- Current status (QUEUED, PROCESSING, COMPLETED)
- Progress percentage
- Output video URL

---

## Step 4: Use in Video Pipeline

### Option A: Manual Integration

```bash
# 1. Generate videos with Runway
node runway-video-generator.js --batch

# 2. Download videos from Runway dashboard
# 3. Import to Descript or Shotstack
# 4. Add images and narration
# 5. Export final video
```

### Option B: Automated Integration

Once videos are ready:

```bash
# Download from Runway
node runway-video-generator.js --status task_id

# Add to Descript project
node descript-video-editor.js --workflow output/runway_videos/video.mp4 ProjectName

# Add to timeline in Descript UI
# - Arrange runway videos between still images
# - Add narration and music
# - Export final video
```

---

## Video Generation Examples

### Example 1: Analytics Dashboard Zoom

```bash
node runway-video-generator.js --generate \
  "https://example.com/dashboard.png" \
  "Camera slowly zooms into analytics dashboard showing keywords and rankings.
   Professional cinematic movement." \
  3
```

### Example 2: Chart Growth Animation

```bash
node runway-video-generator.js --generate \
  "https://example.com/chart.png" \
  "Animated line chart showing upward growth trajectory.
   Chart line progressively draws. Data points appear with animations." \
  4
```

### Example 3: Workspace Pullout

```bash
node runway-video-generator.js --generate \
  "https://example.com/hands.png" \
  "Camera pulls back from extreme close-up of typing hands
   to reveal full professional workspace. Smooth cinematic motion." \
  3
```

---

## Prompt Engineering Tips

### What Works Well

✅ **Good prompts**:
- "Camera slowly zooms into analytics dashboard showing trending keywords"
- "Smooth camera pan across professional office with dual monitors"
- "Chart line progressively draws from left to right with data points"
- "Team members collaborating, dynamic camera movement, professional"

❌ **Bad prompts**:
- "Show analytics"
- "Nice chart"
- "Video"
- "Something cool"

### Best Practices

1. **Be specific about camera movement**:
   - "Camera zoom"
   - "Smooth pan"
   - "Pullout"
   - "Orbit around"

2. **Describe the scene**:
   - "Professional office"
   - "Modern workspace"
   - "Bright lighting"

3. **Include style references**:
   - "Cinematic quality"
   - "Professional production"
   - "Ultra HD"
   - "Film-like"

4. **Keep it 1-2 sentences**:
   - Runway works better with concise prompts

---

## Integration with Other Tools

### With Descript

```bash
# Descript imports Runway videos directly
node descript-video-editor.js --workflow output/runway_videos/video.mp4 ProjectName

# Then in Descript UI:
# - Drag runway videos to timeline
# - Add images between videos
# - Add narration
# - Export final video
```

### With Shotstack

```bash
# Add Runway videos to Shotstack timeline
# Timeline structure:
# - Image (5s) → Runway video (3s) → Image (5s) → Runway video (4s)
# - Add narration audio track
# - Add background music
# - Render final video
```

### With FAL.ai Images

```
Video Timeline:
1. Flux Pro image (5s) ← Still
2. Runway video (3s)   ← Moving (dashboard zoom)
3. Nano Banana chart (6s) ← Still with text
4. Runway video (4s)   ← Moving (chart animation)
5. Flux Pro people (5s) ← Still
6. Runway video (3s)   ← Moving (celebration)
```

This mix keeps viewers engaged!

---

## Troubleshooting

### "API Key not found"

```bash
# Check .env has the key
cat .env | grep RUNWAY

# Should show:
# RUNWAY_API_KEY=sk_xxxx
```

### "Video generation failed"

1. Check Runway dashboard for errors
2. Try simpler prompt
3. Verify image URL is accessible
4. Check API key is valid

### "Videos taking too long"

Normal processing times:
- QUEUED: 0-2 minutes (in queue)
- PROCESSING: 30-60 seconds (generating)
- COMPLETED: Ready to download

If stuck, check dashboard at https://app.runwayml.com/queue

### "Downloaded video is corrupt"

- Re-download from Runway dashboard
- Check file size (should be 10-50 MB for 3-5 second video)
- Verify with: `ffprobe output/runway_videos/video.mp4`

---

## File Locations

### Input Files

```
Images you want to turn into videos:
- s3://bucket/dashboard.png
- s3://bucket/chart.png
- s3://bucket/workspace.png
- s3://bucket/team.png
```

### Output Files

```
output/runway_videos/
├── runway_task_seo_1.mp4
├── runway_task_seo_2.mp4
├── runway_task_seo_3.mp4
├── runway_task_seo_4.mp4
└── runway_task_seo_5.mp4
```

---

## Video Specifications

### Runway Output

```
Resolution:  1920 × 1080 (Full HD)
Format:      MP4 (H.264 codec)
Frame Rate:  24-30 fps
Bitrate:     ~5-8 Mbps
Duration:    3-5 seconds (configurable)
Quality:     Ultra HD / Cinema
```

### Usage in Video

```
Each Runway video: 3-5 seconds
Videos per 10-min video: 5-7 clips
Total Runway time: 20-35 seconds
Total video: 600 seconds (10 minutes)
```

---

## Cost Optimization

### Cheaper Alternative?

If Runway is too expensive, alternatives:

| Tool | Cost | Quality | Speed |
|------|------|---------|-------|
| **Runway Gen-3** | $0.05-0.10 | Excellent | 30-60s |
| **Replicate** | $0.02-0.05 | Good | 1-2min |
| **Leonardo.AI** | $0.01-0.03 | Good | 30s |
| **Stable Diffusion** | Free (self-hosted) | Okay | Variable |

**Recommendation**: Use Runway for hero videos, cheaper tools for fill-in videos.

---

## Complete Workflow

```bash
# 1. Prepare images (from FAL.ai)
python image-generation-nano-banana.py

# 2. Upload images to S3 or accessible URL
# 3. Generate Runway videos
node runway-video-generator.js --batch

# 4. Monitor generation
# Go to: https://app.runwayml.com/queue

# 5. Download completed videos
node runway-video-generator.js --status runway_task_seo_1

# 6. Import to Descript
node descript-video-editor.js --workflow output/runway_videos/video.mp4 ProjectName

# 7. In Descript UI: arrange videos with images and narration
# 8. Export final video

# 9. Upload to YouTube
python youtube-seo-publisher.py --video output/final_video.mp4
```

**Total time**: 15-20 minutes (mostly waiting for generation)

---

## Next Steps

1. [ ] Get Runway API key
2. [ ] Add to .env
3. [ ] Test: `node runway-video-generator.js --test`
4. [ ] Generate example videos: `node runway-video-generator.js --batch`
5. [ ] Monitor at: https://app.runwayml.com/queue
6. [ ] Download videos
7. [ ] Import to Descript
8. [ ] Create your first cinematic video!

---

## Support

- **Runway Docs**: https://docs.runwayml.com
- **API Reference**: https://docs.runwayml.com/api
- **Status Page**: https://status.runwayml.com

**Questions?** Check `RUNWAY_SETUP.md` or the Runway documentation.
