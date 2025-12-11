# Get Started: Descript + Nano Banana Integration

Your complete setup guide. Follow these steps in order.

## Step 1: Request Descript API Key (24-48 hours)

**Important**: Descript requires you to request API access directly.

### 1a. Email Descript Support

```
To: support@descript.com

Subject: Request API Access - Personal Token

Body:
I have a $30/month Descript account and need to enable API access
for my video automation project. Can you provide my personal API token?
```

Or use the contact form: https://www.descript.com/contact

### 1b. Wait for Response

- Check your email (24-48 hours)
- Descript support will send your personal token
- Token format: `descript_sk_xxxxxxxxxxxxxxxxxxxxx`

### 1c. Add to .env File

Once you receive the token:

```bash
# Open .env
nano .env

# Add this line:
DESCRIPT_API_KEY=descript_sk_YOUR_TOKEN_FROM_EMAIL

# Save (Ctrl+X, then Y, then Enter)
```

### 1d. Test It Works

```bash
node descript-video-editor.js --test
```

Should see:
```
✓ API Key found
✓ Token starts with: descript_sk_...
Ready to use Descript API!
```

**While waiting for API key** (24-48 hours), proceed to Step 2 below.

---

## Step 2: Clean Up Old Images (5 minutes)

### 2a. Remove Text-Based Images

These don't look good because they used Flux Pro (which can't render text well).

```bash
# Delete old image directory
rm -rf output/generated_images/infographic/

# Delete old metadata
rm output/generated_images/metadata.json

# List what remains
ls output/generated_images/
```

Should only show photorealistic images (people, workspaces, hands typing).

### 2b. Verify Cleanup

```bash
# Count remaining images
ls output/generated_images/*.png | wc -l

# Should be 5-8 images (photorealistic only)
```

---

## Step 3: Generate New Images with Nano Banana (10 minutes)

### 3a. Run Pipeline

```bash
python image-generation-nano-banana.py
```

This generates:
- **5 Flux Pro images**: People, teams, workspaces
- **7 Nano Banana images**: Charts, timelines, comparisons, infographics

### 3b. Verify Results

```bash
# List all images
ls -la output/generated_images/*.png

# Should show:
# flux_people_1.png through flux_workspace_1.png (Flux Pro)
# nano_chart_*.png through nano_keywords_priority.png (Nano Banana)

# View metadata
cat output/generated_images/metadata_nano_banana.json | head -30
```

---

## Step 4: Generate Video with New Setup (10-15 minutes)

### 4a. Scrape Your URLs (if new project)

```bash
# List projects
node firecrawl-data-manager.js --list

# Scrape a project
node firecrawl-data-manager.js --project SEO_Best_Practices
```

### 4b. Generate Script

```bash
node script-synthesizer.js
```

### 4c. Generate Narration

```bash
python elevenlabs-narrator.py
```

### 4d. Send to Descript

```bash
# Test Descript API
node descript-video-editor.js --test

# Import to Descript (replace URI with your actual file)
node descript-video-editor.js --workflow s3://bucket/narration.mp3 SEO_Best_Practices
```

### 4e. Complete in Descript UI

1. Copy the import URL from the output
2. Paste into browser or visit: https://www.descript.com
3. Descript will:
   - ✓ Import your narration
   - ✓ Auto-generate captions
   - ✓ Transcribe speech
   - ✓ Create SRT files
   - ✓ Apply styling (white text, pink border)
4. Add your images to the timeline
5. Export final video

---

## What You Need for This to Work

### API Keys Required

```bash
# .env file should have:
FIRECRAWL_API_KEY=your_key                    (you have this)
FAL_API_KEY=your_key                          (you have this)
ELEVENLABS_API_KEY=your_key                   (you have this)
DESCRIPT_API_KEY=your_token                   (JUST ADDED)
SHOTSTACK_API_KEY=your_key                    (you have this)
YOUTUBE_CLIENT_ID=your_id                     (you have this)
YOUTUBE_CLIENT_SECRET=your_secret             (you have this)
```

### Node Modules Installed

```bash
npm install
```

Should have:
- ✓ axios
- ✓ dotenv

---

## Files You Now Have

### New Files

```
DESCRIPT_API_SETUP.md                        ← Finding your API key
DESCRIPT_NANO_BANANA_INTEGRATION.md          ← Complete guide
CLEANUP_OLD_IMAGES.md                        ← How to clean up old images
GET_STARTED_DESCRIPT.md                      ← This file

descript-video-editor.js                     ← Descript API integration
image-generation-nano-banana.py              ← New image pipeline
```

### Updated Files

```
.env                    ← Add DESCRIPT_API_KEY
```

---

## Complete Workflow Example

### Project: "Node.js Best Practices"

```bash
# 1. Add URLs to firecrawl-urls.json
#    (edit file, add project with URLs)

# 2. Scrape URLs
node firecrawl-data-manager.js --project Node_JS_Best_Practices

# 3. Generate images
python image-generation-nano-banana.py

# 4. Generate script
node script-synthesizer.js

# 5. Generate narration (optional - Descript can import MP3s)
python elevenlabs-narrator.py

# 6. Send to Descript
node descript-video-editor.js --workflow ./output/narration.mp3 Node_JS_Best_Practices

# 7. In Descript UI:
#    - Review captions
#    - Add images to timeline
#    - Adjust timing
#    - Export video

# 8. Upload to YouTube
python youtube-seo-publisher.py --video output/final_video.mp4
```

---

## Cost Breakdown

### Monthly Costs (Approximate)

```
Descript:                    $30/month (your plan)
FAL.ai (Flux Pro):           $2-3 per video (5 images @ $0.04-0.08)
FAL.ai (Nano Banana):        $1-2 per video (7 images @ $0.02-0.04)
ElevenLabs:                  $0.50 per video (~1,500 chars @ $0.30/1000)
Epidemic Sound (music):      $9/month or $0.05-0.20 per track

TOTAL PER VIDEO:            ~$3-6 per video
TOTAL MONTHLY (10 videos):  ~$30-60
```

---

## Troubleshooting

### "Descript API returns 403 error"

```bash
# Check your token
cat .env | grep DESCRIPT

# If wrong format or empty:
# 1. Go to https://www.descript.com/settings/api
# 2. Generate new token
# 3. Update .env
# 4. Test: node descript-video-editor.js --test
```

### "Nano Banana images look low quality"

Images taking 10-30 seconds is normal. If quality is poor:
- Add "professional" to prompt
- Specify colors and design style
- Add "clean design" or "business infographic"
- Increase inference steps

### "Can't find old image directory"

```bash
# Check what exists
ls -la output/generated_images/

# Show all files
find output -name "*.png" -type f

# Delete by pattern if needed
rm -f output/generated_images/*chart*
rm -f output/generated_images/*timeline*
```

### "Images and narration don't sync"

Descript handles this automatically! But if needed:
1. Open in Descript UI
2. Adjust caption timing
3. Add/remove pauses in script
4. Re-export

---

## Next Steps After Setup

### Option 1: Quick Test (30 minutes)

```bash
# Test everything works
node firecrawl-data-manager.js --list
python image-generation-nano-banana.py
node descript-video-editor.js --test
```

### Option 2: Make Your First Video (1-2 hours)

```bash
# Follow "Complete Workflow Example" above
# Make a video on any topic
# Upload to YouTube
```

### Option 3: Set Up Automation (2-3 hours)

```bash
# Create batch processing script
# Generate 5-10 videos automatically
# Schedule daily/weekly runs
```

---

## Video Quality Checklist

After generating video in Descript, verify:

- [ ] Captions are white with pink/black border
- [ ] Text is readable and timed to narration
- [ ] Images alternate between people and charts
- [ ] Transitions are smooth
- [ ] Audio is clear (narration at -20dB, music at -38dB)
- [ ] Duration is 10 minutes (600 seconds)
- [ ] Resolution is 1920x1080
- [ ] No artifacts or errors in video

---

## Support Resources

| Issue | Resource |
|-------|----------|
| Descript API key | `DESCRIPT_API_SETUP.md` |
| Image generation | `image-generation-nano-banana.py` |
| Workflow integration | `DESCRIPT_NANO_BANANA_INTEGRATION.md` |
| Cleanup old images | `CLEANUP_OLD_IMAGES.md` |
| Full documentation | `ADVANCED_VIDEO_SYSTEM_README.md` |

---

## You're Ready! 🎬

**Right now**:
1. Get your Descript API key (5 min)
2. Add to .env
3. Run: `python image-generation-nano-banana.py`
4. Make your first video!

**Questions?** Check the relevant .md file above.

Let's make some amazing videos! 🚀
