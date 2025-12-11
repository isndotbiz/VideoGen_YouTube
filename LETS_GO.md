# 🚀 LET'S GO! Complete Video Generation in 2-3 Hours

Your step-by-step guide to making your first professional YouTube video.

---

## 📋 CHECKLIST: What You Need

### API Keys You Already Have ✅

- [x] `FAL_API_KEY` (Flux Pro + Nano Banana images)
- [x] `ELEVENLABS_API_KEY` (narration)
- [x] `SHOTSTACK_API_KEY` (backup video assembly)
- [x] `YOUTUBE_CLIENT_ID` & `YOUTUBE_CLIENT_SECRET` (YouTube upload)

### API Keys You Need to Get 🔑

- [ ] `DESCRIPT_API_KEY` (video editing + captions)
- [ ] `RUNWAY_API_KEY` (cinematic videos)

### Dependencies ✅

- [x] Node.js installed
- [x] Python 3 installed
- [x] npm packages: `npm install axios dotenv`

---

## ⏱️ Timeline

```
Step 1: Get API Keys          (10 minutes)
Step 2: Test Connections      (5 minutes)
Step 3: Clean Old Images      (2 minutes)
Step 4: Generate Images       (15 minutes - runs in background)
Step 5: Generate Script       (5 minutes)
Step 6: Generate Narration    (5 minutes)
Step 7: Generate Runway Videos (15 minutes - runs in background)
Step 8: Descript Assembly     (20 minutes - in Descript UI)
Step 9: Upload to YouTube     (5 minutes)

TOTAL: 1.5-2.5 hours
(Most is waiting for AI generation in background)
```

---

## 🎯 STEP-BY-STEP GUIDE

### STEP 1: Get Your API Keys (10 minutes)

#### 1a. Descript API Key

**Email Descript:**
```
To: support@descript.com

Subject: Request API Access - Personal Token

Body:
I have a $30/month Descript account and need API access
for my video generation project. Can you provide my personal token?
```

**OR use contact form:** https://www.descript.com/contact

**Response time:** 24-48 hours

#### 1b. Runway API Key (Get This Now!)

1. Go to: https://app.runwayml.com
2. Sign up or login
3. Click **Profile** (bottom left)
4. Select **API**
5. Click **Create API Key**
6. Copy the key: `sk_xxx...`

#### 1c. Add to .env File

```bash
# Open .env
nano .env

# Scroll to bottom and add:
DESCRIPT_API_KEY=sk_YOUR_DESCRIPT_TOKEN_FROM_EMAIL
RUNWAY_API_KEY=sk_YOUR_RUNWAY_KEY_FROM_DASHBOARD

# Save: Ctrl+X, then Y, then Enter
```

#### 1d. Verify Keys Are Added

```bash
# Check they're in .env
grep -E "DESCRIPT|RUNWAY" .env

# Should show:
# DESCRIPT_API_KEY=sk_...
# RUNWAY_API_KEY=sk_...
```

---

### STEP 2: Test All Connections (5 minutes)

```bash
# Test Runway
node runway-video-generator.js --test

# Test Descript (will fail if waiting for token - that's ok)
node descript-video-editor.js --test

# Test FireCrawl
node firecrawl-data-manager.js --list

# Test image generation
python image-generation-nano-banana.py --test 2>/dev/null || echo "Ready for full run"
```

---

### STEP 3: Clean Old Images (2 minutes)

Remove old text-based images that used Flux Pro (low quality):

```bash
# Delete old infographic directory
rm -rf output/generated_images/infographic/

# Delete old metadata
rm -f output/generated_images/metadata.json

# Verify what's left (should be photorealistic only)
ls output/generated_images/
```

**Should show**: `flux_people_1.png`, `flux_team_1.png`, `flux_closeup_1.png`, `flux_workspace_1.png`

---

### STEP 4: Generate Images (15 minutes - Background)

**Run in background** while you continue with other steps:

```bash
# Terminal 1: Start image generation
python image-generation-nano-banana.py &
```

**What happens**:
- 5 Flux Pro photorealistic images (people, teams, workspaces)
- 7 Nano Banana text-based images (charts, infographics, diagrams)
- Saves to: `output/generated_images/`
- Creates: `metadata_nano_banana.json`

**You can continue to next steps while this runs!**

---

### STEP 5: Generate Script (5 minutes)

```bash
# Terminal 2: Generate video script
node script-synthesizer.js
```

**Output**:
- `output/COMPLETE_VIDEO_SCRIPT.md` (full script)
- `output/script_metadata.json` (timing info)
- `output/narration_markers.json` (pause/pronunciation markers)

**What to expect**:
```
[SYNTHESIS] Generating raw video script...
[HUMANIZATION] Converting raw script to natural narration...
[NARRATION] Adding ElevenLabs pause and pronunciation markers...
✓ Script generation and humanization complete
```

---

### STEP 6: Generate Narration (5 minutes)

```bash
# Terminal 3: Generate audio narration
python elevenlabs-narrator.py
```

**Output**:
- `output/narration.mp3` (complete narration audio)
- `output/narration_timing.json` (subtitle timing)

**Cost**: ~$0.50 (1,500 words at $0.30/1000)

**Quality**:
- Voice: Rachel (multilingual)
- Stability: 0.75
- Auto-ducking ready (music quieter when speaking)

---

### STEP 7: Generate Runway Videos (15 minutes - Background)

**While waiting for images and narration:**

```bash
# Terminal 4: Start Runway video generation
node runway-video-generator.js --batch
```

**What happens**:
- Creates 5 cinematic video tasks
- Queues them with Runway API
- Returns task IDs to monitor

**Output**:
```
[RUNWAY] Generating cinematic video prompts...
[runway_seo_1] Analytics Dashboard Zoom
  Motion: cinematic-zoom
  Duration: 3s
  ✓ Task queued: runway_task_seo_1

[runway_seo_2] Growth Chart Animation
  Motion: animated-chart
  Duration: 4s
  ✓ Task queued: runway_task_seo_2

... etc for all 5 videos ...

Batch Generation Started
5 videos in queue
Estimated time: 1-2 minutes per video
```

**Monitor at**: https://app.runwayml.com/queue

---

### STEP 8: Check Progress (While Waiting)

```bash
# In a new terminal, check status
watch -n 5 'ls -lh output/generated_images/ output/runway_videos/ 2>/dev/null | tail -10'
```

This updates every 5 seconds showing:
- Images being generated
- Runway videos being created
- File sizes growing

---

### STEP 9: Verify Everything Is Ready

Once all tasks complete:

```bash
# Check images
ls -la output/generated_images/*.png | wc -l
# Should show: 12-16 images

# Check narration
ls -lh output/narration.mp3
# Should be: 10-20 MB

# Check Runway videos
ls -la output/runway_videos/*.mp4 2>/dev/null || echo "Still generating..."

# Check script
cat output/COMPLETE_VIDEO_SCRIPT.md | head -20
```

---

### STEP 10: Import to Descript (20 minutes in Descript UI)

**Once you have Descript API key:**

```bash
# Send narration to Descript for auto-captioning
node descript-video-editor.js --workflow ./output/narration.mp3 SEO_Best_Practices
```

**This will**:
- ✓ Create import URL (valid 3 hours)
- ✓ Show: `https://web.descript.com/import?nonce=...`

**In Descript UI**:
1. Click the import URL above
2. Descript auto-transcribes narration
3. Descript generates SRT captions
4. Captions are styled (white text, pink border)
5. Drag Runway videos into timeline
6. Arrange between still images
7. Add background music
8. Export final MP4

---

### STEP 11: Upload to YouTube (5 minutes)

```bash
# Upload to YouTube with SEO metadata
python youtube-seo-publisher.py --video output/final_video.mp4 --title "SEO Best Practices 2025" --description "Complete SEO guide..."
```

**What gets uploaded**:
- ✓ Video file (1920x1080, 10 minutes)
- ✓ Title (optimized for ranking)
- ✓ Description (5000 char with timestamps)
- ✓ Tags (30 most relevant)
- ✓ Chapters (from script sections)
- ✓ Thumbnail (auto-generated)

**Result**: Video live on YouTube! 🎉

---

## 🔄 COMPLETE COMMAND SEQUENCE

### All Commands Together (Copy & Paste)

```bash
#!/bin/bash

# Set your project name
PROJECT="SEO_Best_Practices"

echo "🚀 STARTING VIDEO GENERATION FOR: $PROJECT"
echo ""

# Step 1: Scrape URLs
echo "Step 1: Scraping URLs with FireCrawl..."
node firecrawl-data-manager.js --project $PROJECT
echo "✓ URLs scraped"
echo ""

# Step 2: Clean old images
echo "Step 2: Cleaning old images..."
rm -rf output/generated_images/infographic/
rm -f output/generated_images/metadata.json
echo "✓ Old images removed"
echo ""

# Step 3: Generate images (background)
echo "Step 3: Generating images (Flux Pro + Nano Banana)..."
python image-generation-nano-banana.py > /tmp/images.log 2>&1 &
IMAGE_PID=$!
echo "✓ Image generation started (PID: $IMAGE_PID)"
echo ""

# Step 4: Generate script
echo "Step 4: Generating video script..."
node script-synthesizer.js
echo "✓ Script generated"
echo ""

# Step 5: Generate narration
echo "Step 5: Generating narration with ElevenLabs..."
python elevenlabs-narrator.py
echo "✓ Narration generated"
echo ""

# Step 6: Generate Runway videos (background)
echo "Step 6: Generating Runway cinematic videos..."
node runway-video-generator.js --batch > /tmp/runway.log 2>&1 &
RUNWAY_PID=$!
echo "✓ Runway videos queued (PID: $RUNWAY_PID)"
echo ""

# Wait for image generation to complete
echo "Waiting for image generation to complete..."
wait $IMAGE_PID
echo "✓ Images ready!"
echo ""

# Wait for Runway generation to complete
echo "Waiting for Runway videos to complete..."
echo "(Monitor at: https://app.runwayml.com/queue)"
wait $RUNWAY_PID
echo "✓ Runway videos ready!"
echo ""

echo "🎬 READY FOR VIDEO ASSEMBLY!"
echo ""
echo "Next steps:"
echo "1. Go to: https://app.runwayml.com/queue"
echo "2. Download all completed Runway videos"
echo "3. Run: node descript-video-editor.js --workflow ./output/narration.mp3 $PROJECT"
echo "4. Complete assembly in Descript UI"
echo "5. Export and upload to YouTube"
echo ""
```

**Save this as `generate_video.sh`**:

```bash
# Make executable
chmod +x generate_video.sh

# Run it
./generate_video.sh
```

---

## 📊 What You'll Have After

```
output/
├── generated_images/
│   ├── flux_people_1.png          (professional woman)
│   ├── flux_team_1.png            (team collaborating)
│   ├── flux_closeup_1.png         (hands typing)
│   ├── flux_workspace_1.png       (desk setup)
│   ├── nano_chart_ranking_factors.png
│   ├── nano_timeline_algo_updates.png
│   ├── nano_comparison_table.png
│   ├── nano_steps_implementation.png
│   ├── nano_myths_reality.png
│   ├── nano_funnel_conversion.png
│   ├── nano_keywords_priority.png
│   └── metadata_nano_banana.json
│
├── runway_videos/
│   ├── runway_task_seo_1.mp4      (dashboard zoom)
│   ├── runway_task_seo_2.mp4      (chart animation)
│   ├── runway_task_seo_3.mp4      (workspace pullout)
│   ├── runway_task_seo_4.mp4      (team montage)
│   └── runway_task_seo_5.mp4      (success celebration)
│
├── COMPLETE_VIDEO_SCRIPT.md       (full script with timing)
├── narration.mp3                  (audio narration)
├── narration_timing.json          (subtitle timing)
│
└── final_video.mp4                (FINAL VIDEO - ready for YouTube!)
```

---

## 💰 TOTAL COST FOR ONE VIDEO

```
FireCrawl (3 URLs):           $0.01
Flux Pro (5 images):          $0.30
Nano Banana (7 images):       $0.15
ElevenLabs (1,500 words):     $0.50
Runway (5 videos @ $0.08):    $0.40
Descript:                     $0.00 (included in $30/month)
Music (Epidemic Sound):       $0.15

TOTAL:                        $1.51

Per month (10 videos):        $15.10
Per year (120 videos):        $181.20
```

**Very affordable for professional quality videos!**

---

## ⚡ QUICK REFERENCE

### Commands by Task

```bash
# Scrape URLs
node firecrawl-data-manager.js --project ProjectName

# Generate images
python image-generation-nano-banana.py

# Generate script
node script-synthesizer.js

# Generate narration
python elevenlabs-narrator.py

# Generate Runway videos
node runway-video-generator.js --batch

# Check Runway status
node runway-video-generator.js --status runway_task_seo_1

# Send to Descript
node descript-video-editor.js --workflow ./output/narration.mp3 ProjectName

# Upload to YouTube
python youtube-seo-publisher.py --video output/final_video.mp4
```

---

## 🎓 WHAT EACH TOOL DOES

| Tool | Input | Output | Time |
|------|-------|--------|------|
| **FireCrawl** | URLs | JSONL articles | 30s |
| **Flux Pro** | Prompt | Photorealistic image | 5s |
| **Nano Banana** | Prompt | Chart/diagram image | 10s |
| **Script Synthesizer** | Research | Video script | 2m |
| **ElevenLabs** | Script | Narration MP3 | 3m |
| **Runway** | Image + prompt | Video clip | 45s |
| **Descript** | Audio + images | Final video | 10m |
| **YouTube** | Video file | Published | 5m |

---

## 🚨 TROUBLESHOOTING

### "Image generation stuck"
```bash
# Check if process is running
ps aux | grep python

# Kill and restart
pkill -f image-generation
python image-generation-nano-banana.py
```

### "Runway videos not ready"
```bash
# Check status
node runway-video-generator.js --status runway_task_seo_1

# Or go to: https://app.runwayml.com/queue
# Videos take 30-60 seconds each
```

### "Descript token not working"
```bash
# Verify key is correct
grep DESCRIPT .env

# Re-request from Descript if needed
# Email: support@descript.com
```

### "YouTube upload fails"
```bash
# Check YouTube credentials
cat youtube_credentials.json

# Re-authenticate if needed
python youtube-seo-publisher.py --auth
```

---

## ✅ FINAL CHECKLIST

Before you start:

- [ ] Got Runway API key
- [ ] Got (or requested) Descript API key
- [ ] Added both to .env
- [ ] npm dependencies installed
- [ ] Python dependencies installed
- [ ] All API keys tested with `--test` commands
- [ ] Old images cleaned up
- [ ] URLs ready to scrape (optional - can use SEO_Best_Practices example)

---

## 🎬 YOU'RE READY!

**Start here:**

```bash
# Terminal 1: Run everything
./generate_video.sh

# Or manually run step by step:
node firecrawl-data-manager.js --project SEO_Best_Practices
python image-generation-nano-banana.py &
node script-synthesizer.js
python elevenlabs-narrator.py
node runway-video-generator.js --batch
```

**Then in 20 minutes:**

```bash
# Import to Descript
node descript-video-editor.js --workflow ./output/narration.mp3 SEO_Best_Practices

# Go to: https://web.descript.com/import?nonce=...
# Complete video assembly in UI
# Export video
# Upload to YouTube!
```

---

## 🎯 Your First Video Timeline

```
T+0:00   Start: Run all generation commands
T+2:00   Images generating in background
T+3:00   Script ready
T+4:00   Narration generating
T+7:00   Narration complete
T+8:00   Runway videos queued
T+10:00  Images complete
T+15:00  Runway videos complete
T+15:30  Send to Descript
T+16:00  Start Descript assembly
T+36:00  Video exported from Descript
T+37:00  Upload to YouTube
T+40:00  VIDEO LIVE! 🎉
```

**Total time: ~40 minutes (mostly automated)**

---

## 💡 Pro Tips

1. **Use background processes** - Let image/video generation run while you do other things
2. **Monitor dashboard** - Watch Runway progress at https://app.runwayml.com/queue
3. **Plan your images** - Think about which images should have Runway videos (every other one)
4. **Test with SEO example** - First video uses pre-built SEO_Best_Practices project
5. **Customize after** - In Descript UI, you can adjust timing, add effects, re-arrange

---

## 🚀 GO TIME!

**Let's make your first professional YouTube video:**

```bash
./generate_video.sh
```

**Then check back in 20 minutes to assemble in Descript!**

Good luck! 🎬✨
