# Quick Start Integration Guide - VideoGen YouTube

## 🚀 What You Have & How to Use It

Your project has **all the pieces** - they just need to be **connected and tested end-to-end**.

---

## 📋 QUICK COMMAND REFERENCE

### Test Everything Works

```bash
# 1. Check Node.js
node --version   # Should be 14+

# 2. Check Python
python --version # Should be 3.8+

# 3. Check npm dependencies
npm install
npm list

# 4. Check environment variables
grep -E "FAL_API_KEY|ELEVENLABS_API_KEY|RUNWAY_API_KEY" .env
```

### Run Full Pipeline (End-to-End)

```bash
# OPTION A: All at once (recommended for testing)
node orchestrate.js "https://example.com/article"

# OPTION B: Step by step
node scrape-and-convert.js "https://example.com/article"
node clean-jsonl.js dataset.jsonl
node generate-video-script.js
python image-generation-nano-banana.py
python elevenlabs_narration_WORKING.py
node runway-video-generator.js --batch
# Then manually in Descript UI: import narration, build timeline, export
python upload_to_youtube.py --video output/final_video.mp4
```

### Run Individual Phases

```bash
# Phase 1: Scrape & Convert
node scrape-and-convert.js "https://your-article-url.com"
# Output: dataset.json, dataset.jsonl, cleaned version

# Phase 2: Clean Data
node clean-jsonl.js dataset.jsonl
# Output: dataset.jsonl.cleaned, clean-report.json

# Phase 3: Generate Script
node generate-video-script.js
# Output: COMPLETE_VIDEO_SCRIPT.md + 6 markdown files

# Phase 4: Generate Images
python image-generation-nano-banana.py
# Output: output/generated_images/*.png, metadata

# Phase 5: Generate Narration
python elevenlabs_narration_WORKING.py
# Output: output/narration.mp3, timing data

# Phase 6: Generate Videos
node runway-video-generator.js --batch
# Output: Task IDs, monitor at https://app.runwayml.com/queue

# Phase 7: Assembly (Manual in Descript)
node descript-video-editor.js --workflow ./output/narration.mp3 ProjectName
# Output: Import URL for Descript UI

# Phase 8: Upload to YouTube
python upload_to_youtube.py --video output/final_video.mp4 --title "Your Title"
# Output: YouTube URL
```

---

## 🔧 INTEGRATION CHECKLIST (What Needs to Be Done)

### Critical Fixes (Must Have for MVP)

- [ ] **Connect Research to Script**
  - Current: `generate-video-script.js` uses hardcoded data
  - Fix: Read from `dataset.jsonl`, generate script from actual content
  - File: `script-synthesizer.js` around line 31-79

- [ ] **Connect Script to Image Generation**
  - Current: `image-generation-nano-banana.py` uses fixed prompts
  - Fix: Parse script sections, generate image prompts dynamically
  - File: `image-generation-nano-banana.py` around line 33-100

- [ ] **Implement Research Agent Verification**
  - Current: `research-agents-launcher.js` is stubbed
  - Fix: Actually call web search APIs (Google, Bing, etc.)
  - File: `research-agents-launcher.js` around line 16-200

- [ ] **Automate Descript Step**
  - Current: Manual timeline building in Descript UI (20 min)
  - Option A: Full automation (complex, needs Descript API)
  - Option B: Use FFmpeg locally (simpler fallback)
  - File: `descript-video-editor.js` + new `automated-video-assembly.js`

- [ ] **Add Error Handling & Logging**
  - Current: Errors stop pipeline
  - Fix: Try-catch, retry logic, fallback services
  - Files: All phase scripts

- [ ] **Add Cost Tracking**
  - Current: No tracking of API costs
  - Fix: Log each API call with cost, sum per video
  - File: New `cost-tracker.js` utility

### Important Enhancements (Should Have for MVP+1)

- [ ] **Dynamic Duration Support** (3 min, 33 sec, 90 sec)
  - Current: Fixed script duration
  - Fix: Adjust section lengths based on target duration

- [ ] **Fallback Services**
  - Current: Single provider per service
  - Fix: Add ComfyUI, Replicate, alternative text-to-speech

- [ ] **Automated SEO Generation**
  - Current: Manual YouTube metadata
  - Fix: Generate title, description, tags, chapters automatically

- [ ] **Marker Processing**
  - Current: Markers inserted but not processed
  - Fix: Recognize [PAUSE], [EMPHASIS], [PRONUNCIATION]

- [ ] **Progress Tracking Dashboard**
  - Current: No visibility into what's happening
  - Fix: Simple log file or web dashboard

---

## 💡 HOW TO GIVE THE PROMPT TO CODEX MAX

Create a conversation with Codex Max and paste this:

```
You are Codex, based on GPT-5. You are running as a coding agent in the Codex CLI.

I have a VideoGen YouTube project with 60+ scripts that form a complete video generation pipeline:

[PASTE: CODEX_MAX_MASTER_PROMPT.md]

Project status: Core architecture complete, needs integration and error handling.

Your mission: Make this system work end-to-end, starting with a single 3-minute test video.

Focus areas:
1. Connect research → script → images → narration → video → YouTube
2. Implement research agent verification (actual web scraping)
3. Automate Descript video assembly (or provide FFmpeg fallback)
4. Add error handling and retry logic to all phases
5. Implement cost tracking for all API calls
6. Create progress tracking/logging system

Success = User provides URL, gets uploaded YouTube video in <1 hour (mostly automated)

All relevant files are in D:\workspace\VideoGen_YouTube\
Environment variables configured in .env file.
Multiple APIs already integrated (FAL.ai, ElevenLabs, Runway, YouTube, AWS, etc.)

Start by testing the current pipeline end-to-end, identifying failure points, then fix.
```

---

## 🎯 3-STEP TEST PLAN (Do This First)

### Step 1: Verify All APIs Work (5 min)

```bash
# Test FAL.ai
curl -H "Authorization: Bearer $FAL_API_KEY" \
  https://api.fal.ai/v1/health

# Test ElevenLabs
python -c "from elevenlabs import ElevenLabs; \
  client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY')); \
  print('✓ ElevenLabs connected')"

# Test Runway
node -e "const axios = require('axios'); \
  const key = process.env.RUNWAY_API_KEY; \
  console.log(key ? '✓ Runway key found' : '✗ Runway key missing')"

# Test YouTube OAuth
python -c "from google.auth.transport.requests import Request; \
  print('✓ Google auth available')"
```

### Step 2: Run Single Phase (10 min)

```bash
# Just scrape one article
node scrape-and-convert.js "https://www.example.com/article"

# Check output exists
ls -la dataset.json dataset.jsonl
```

### Step 3: Run Full Pipeline (60 min)

```bash
# Full test with one article
node orchestrate.js "https://www.example.com/article"

# Monitor progress
tail -f output/logs/pipeline.log

# Check outputs
ls -la output/generated_images/*.png
ls -la output/narration.mp3
ls -la output/runway_videos/*.mp4
```

---

## 📁 KEY FILES TO UNDERSTAND

### If You Want to Fix Script Generation
Read: `script-synthesizer.js` (lines 1-100)

Issue: Hardcoded script data (line 34-79)
Fix: Read from JSONL dataset instead

### If You Want to Fix Image Generation
Read: `image-generation-nano-banana.py` (lines 1-150)

Issue: Fixed prompts regardless of topic
Fix: Parse script sections, generate prompts dynamically

### If You Want to Fix Research Verification
Read: `research-agents-launcher.js` (lines 1-200)

Issue: Stubbed agent definitions, no actual search
Fix: Call Google Search API, Bing, or similar

### If You Want to Automate Descript
Read: `descript-video-editor.js` (entire file)

Issue: Returns import URL only, no timeline automation
Fix: Use Descript API for timeline building, or use FFmpeg

### If You Want to Fix Error Handling
Read: All phase scripts - look for:
```javascript
try {
  // implementation
} catch (error) {
  console.error(error.message);  // ← This is weak
  // Add: retry logic, logging, fallback service
}
```

---

## 🔄 DATA FLOW (How Data Moves Through System)

```
URL Input
  ↓
[scrape-and-convert.js]
  ├── HTTP GET
  ├── Parse HTML
  └─→ dataset.jsonl

JSONL File
  ↓
[generate-video-script.js]
  ├── Read JSONL
  ├── Structure sections
  └─→ COMPLETE_VIDEO_SCRIPT.md

Script File
  ↓
[image-generation-nano-banana.py]
  ├── Parse sections
  ├── Generate prompts
  ├── Call FAL.ai
  └─→ *.png files

Script File + Prompt List
  ↓
[elevenlabs_narration_WORKING.py]
  ├── Read script with markers
  ├── Call ElevenLabs
  └─→ narration.mp3

Images + Prompts
  ↓
[runway-video-generator.js]
  ├── Queue with Runway
  ├── Poll for completion
  └─→ *.mp4 files

Narration + Images + Videos
  ↓
[Descript UI] (MANUAL STEP - automate this!)
  ├── Import narration
  ├── Build timeline
  ├── Add background music
  └─→ final_video.mp4

Final Video + Metadata
  ↓
[upload_to_youtube.py]
  ├── Prepare metadata
  ├── Call YouTube API
  └─→ YouTube URL

┌─→ YouTube Video Live! 🎉
```

---

## 🐛 COMMON ISSUES & FIXES

### "ELEVENLABS_API_KEY not found"
```bash
# Check if .env exists
ls -la .env

# Check if key is there
grep ELEVENLABS .env

# If missing:
echo "ELEVENLABS_API_KEY=sk_..." >> .env
```

### "FAL.ai generation timed out"
```python
# Increase timeout in image-generation-nano-banana.py
response = requests.post(
  url,
  json=payload,
  timeout=60  # ← Increase from 30 to 60
)
```

### "Runway task stuck in pending"
```bash
# Check status manually
node runway-video-generator.js --status runway_task_seo_1

# Or at: https://app.runwayml.com/queue
```

### "Descript import URL expired"
```bash
# URL valid for 3 hours only
# Need to re-run: node descript-video-editor.js --workflow ...

# Fix: Make duration longer in code
```

### "YouTube upload fails with 403"
```bash
# Token expired, re-authenticate
python upload_to_youtube.py --auth

# OR check scope includes upload
# File: youtube_credentials.json
```

---

## 📊 EXPECTED OUTPUTS

After running full pipeline, you should have:

```
output/
├── generated_images/
│   ├── flux_people_1.png           (2.4 MB, photorealistic)
│   ├── flux_team_1.png             (2.2 MB)
│   ├── flux_closeup_1.png          (1.8 MB)
│   ├── flux_workspace_1.png        (2.1 MB)
│   ├── nano_chart_ranking.png      (1.2 MB, text-heavy)
│   ├── nano_timeline_algo.png      (1.1 MB)
│   ├── nano_comparison_table.png   (0.9 MB)
│   ├── nano_steps.png              (1.0 MB)
│   ├── nano_myths.png              (0.8 MB)
│   ├── nano_funnel.png             (1.1 MB)
│   ├── nano_keywords.png           (0.7 MB)
│   └── metadata_nano_banana.json   (2 KB)
│
├── runway_videos/
│   ├── runway_task_seo_1.mp4       (5.2 MB, 3 sec video)
│   ├── runway_task_seo_2.mp4       (4.8 MB)
│   ├── runway_task_seo_3.mp4       (5.5 MB)
│   ├── runway_task_seo_4.mp4       (4.9 MB)
│   └── runway_task_seo_5.mp4       (5.1 MB)
│
├── COMPLETE_VIDEO_SCRIPT.md        (15 KB, full script)
├── narration.mp3                   (12 MB, 3 min audio)
├── narration_timing.json           (5 KB, subtitle timing)
├── script_metadata.json            (2 KB, timing info)
│
└── final_video.mp4                 (150 MB, 1920x1080, 3 min)

Total: ~250-300 MB per video
Cost: ~$1.50-2.00 per video
Time: 60 minutes total (mostly automated)
```

---

## ✅ FINAL CHECKLIST (Before Handing to Codex Max)

- [ ] All environment variables in `.env` are filled (check with `grep`)
- [ ] Can import all npm packages (run `npm install`)
- [ ] Can import Python libraries (run `pip install -r requirements.txt`)
- [ ] Have tested at least one API (FAL.ai or ElevenLabs)
- [ ] Have read `CODEX_MAX_MASTER_PROMPT.md`
- [ ] Have read `PROJECT_ARCHITECTURE_REVIEW.md`
- [ ] Understand the 7-phase pipeline
- [ ] Understand which parts are working vs stubbed
- [ ] Ready to hand off to Codex Max

---

## 🎬 YOUR NEXT MOVE

1. **Copy the prompt**: CODEX_MAX_MASTER_PROMPT.md
2. **Add context**: PROJECT_ARCHITECTURE_REVIEW.md
3. **Give to Codex Max**: "Here's my project, make it work end-to-end"
4. **Codex will**:
   - Analyze current code
   - Identify failure points
   - Implement integration fixes
   - Add error handling
   - Test end-to-end
5. **You'll have**: Fully automated video generation in <1 hour

---

## 💬 What to Tell Codex Max

```
"I have a VideoGen YouTube project with 60 scripts forming a complete pipeline.
The architecture is solid but disconnected. I need you to:

1. Make research → script → images → narration → video → YouTube work end-to-end
2. Implement research agent verification (actual web scraping)
3. Automate all phases or provide fallbacks
4. Add error handling and retry logic
5. Implement cost tracking

Success = User provides URL, gets YouTube video uploaded in <1 hour.

Reference documents:
- CODEX_MAX_MASTER_PROMPT.md (detailed requirements)
- PROJECT_ARCHITECTURE_REVIEW.md (what currently works)
- QUICK_START_INTEGRATION_GUIDE.md (how to run tests)

Start with a 3-minute test video, then expand to 33-second versions.
All APIs already configured in .env, ready to use."
```

---

**You're ready. Go get Codex Max working on it! 🚀**

