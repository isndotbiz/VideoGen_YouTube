# Build Your SEO YouTube Video Library

Complete guide to generate 5+ high-ranking AI comparison videos using your existing Descript Creator Plan.

## ✅ What You Have Ready

- ✅ Article scraping (Firecrawl)
- ✅ Script generation (dynamic from content)
- ✅ Image prompt generation (Flux Pro + Nano Banana)
- ✅ Narration generation (ElevenLabs TTS)
- ✅ Descript API integration (with auto-captions)
- ✅ Batch processing (parallel video generation)
- ✅ 5 pre-selected high-SEO topics in `topics.json`

## 🎯 Your Content Topics (Ready to Generate)

All topics are high-volume, high-intent search queries:

| Video | Duration | SEO Value | Audience |
|-------|----------|-----------|----------|
| Claude vs ChatGPT | 4-5 min | Very High | Decision-makers |
| Claude vs Gemini | 4-5 min | High | Tech-savvy |
| Claude for Coding | 5-6 min | Very High | Developers ($ keywords) |
| Free AI Tools | 5-6 min | High | Budget-conscious |
| ChatGPT for Beginners | 6-7 min | Medium | Beginners (long watch-time) |

**Total content potential: 25-30 minutes = 5 videos for your channel**

## 📋 Pre-Requisites

### 1. Verify Your Descript API Key

Your `.env` file has `DESCRIPT_API_KEY` - verify it's valid:

```bash
# Test the API key
node descript-video-editor.js --test

# If it fails, get a new key:
# 1. Go to https://www.descript.com/account/api
# 2. Generate new API token
# 3. Replace DESCRIPT_API_KEY in .env
```

### 2. Install FFmpeg (if using FFmpeg assembly)

**Windows (via Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (Manual):**
1. Download from: https://ffmpeg.org/download.html
2. Add to PATH

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 3. Verify API Keys

All major APIs are already in `.env`:
- ✅ Brave Search (research)
- ✅ FAL.ai (images)
- ✅ ElevenLabs (narration)
- ✅ Runway (videos - optional)
- ✅ Descript (assembly)

## 🚀 Quick Start: Generate Videos

### Option A: Generate All 5 Videos (Recommended)

**With Descript (professional captions):**
```bash
node batch-video-generator.js topics.json --use-descript
```

**With FFmpeg only (no captions):**
```bash
node batch-video-generator.js topics.json
```

**Sequential (one at a time):**
```bash
node batch-video-generator.js topics.json --use-descript --sequential
```

### Option B: Generate Single Video (for testing)

```bash
# Full pipeline with Descript
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/" --use-descript

# Or just FFmpeg
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/"
```

### Option C: Custom Topics

Create `my-topics.json`:
```json
[
  {
    "id": "topic-1",
    "title": "My Topic Title",
    "url": "https://example.com/article",
    "tags": ["AI", "Tutorial"],
    "duration": "4-5 min"
  }
]
```

Then run:
```bash
node batch-video-generator.js my-topics.json --use-descript
```

## 📊 Cost Breakdown (Per Video)

### With Descript (Recommended - Your Plan)

| Component | Cost | Notes |
|-----------|------|-------|
| Images (Flux + Nano) | $0.21 | FAL.ai |
| Narration | $0.45 | ElevenLabs |
| Runway videos | $0.40 | Video generation |
| Descript assembly | FREE | Included in Creator Plan |
| **TOTAL** | **~$1.06** | **All-in** |

### With FFmpeg Only

| Component | Cost | Notes |
|-----------|------|-------|
| Images | $0.21 | FAL.ai |
| Narration | $0.45 | ElevenLabs |
| Runway videos | $0.40 | Video generation |
| Assembly | FREE | Local FFmpeg |
| **TOTAL** | **~$1.06** | **No captions** |

### Descript Plan Details

Your Creator Plan includes:
- **1,800 media minutes/month** = ~36 hours = Can handle 100+ videos
- **800 AI credits/month** = Extra effects/features
- **Auto-captions** = Included (FREE)
- **No pay-per-video cost** = It's all in your monthly plan!

**For 5 videos (25 minutes total):**
- Uses: ~25 media minutes out of 1,800 (1.4% of quota)
- Cost: Included in your plan
- Status: COMPLETELY FREE

## ⏱️ Timeline

### Full Pipeline (with all phases):
- Per video: ~10-15 minutes automated
- 5 videos: ~50-75 minutes total (parallel: ~25-30 minutes)
- Runway download: Manual (can be automated)

### Phases:
1. **Scrape** (1-2 min) - Fetch article
2. **Clean** (1 min) - Validate data
3. **Script** (1-2 min) - Generate video script
4. **Images** (3-5 min) - Generate via FAL.ai
5. **Narration** (5-10 min) - Generate TTS
6. **Runway** (1 min) - Queue videos
7. **Descript** (5-10 min) - Assembly + captions
8. **YouTube** (optional) - Upload

## 🎬 Next Steps

### Step 1: Test Descript API
```bash
node descript-video-editor.js --test
```

### Step 2: Verify Your Topics
```bash
cat topics.json
```

### Step 3: Generate First Video
```bash
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/" --use-descript
```

### Step 4: Check Output
```bash
ls -lah output/final_video.mp4
# Will show your video with captions from Descript
```

### Step 5: Batch Generate All 5
```bash
node batch-video-generator.js topics.json --use-descript
```

### Step 6: Upload to YouTube

Videos will be in `output/final_video.mp4` for each run.

**Manual upload:**
1. Go to YouTube Studio
2. Create new video
3. Upload `final_video.mp4`
4. Add title, description, tags
5. Publish

**Automated upload (optional):**
```bash
python upload_to_youtube.py --video output/final_video.mp4
```

## 📁 Output Structure

After batch processing:
```
output/
├── final_video.mp4          # Latest video (ready for upload)
├── COMPLETE_VIDEO_SCRIPT.md # What was narrated
├── video-storyboard.md      # Visual breakdown
├── image-prompts.json       # Image specifications
├── generated_images/        # All images used
│   ├── flux_*.png          # Photorealistic
│   └── nano_*.png          # Infographics
├── narration.mp3            # Audio file
└── captions.srt             # Generated captions
```

## 🔍 Monitoring Progress

Watch logs in real-time:
```bash
tail -f logs/pipeline-*.log
```

Check costs:
```bash
grep "API" logs/pipeline-*.log | tail -20
```

## 🆘 Troubleshooting

### "FFmpeg not installed"
```bash
apt-get install ffmpeg  # Linux
brew install ffmpeg     # Mac
```

### "Descript API failed (401)"
1. Get new token: https://www.descript.com/account/api
2. Update `.env`: `DESCRIPT_API_KEY=your_new_token`
3. Test: `node descript-video-editor.js --test`

### "Image generation failed"
- Check FAL.ai API key in `.env`
- Verify credit balance at https://fal.ai/dashboard

### "Narration generation failed"
- Check ElevenLabs API key in `.env`
- Verify credit balance at https://elevenlabs.io/app/settings/billing

## 💡 Pro Tips

### Tip 1: Use Descript by Default
Since you have the Creator Plan, **always use `--use-descript`**:
- Auto-captions boost SEO ranking
- Included in your plan (FREE)
- No extra cost

### Tip 2: Batch on Parallel
Generate multiple videos simultaneously:
```bash
# Generate 2 videos at a time (4x faster)
node batch-video-generator.js topics.json --use-descript --parallel=2
```

### Tip 3: Build a Library
Generate 20-30 videos across different AI topics to build authority:
```bash
# Week 1: 5 comparison videos
node batch-video-generator.js topics.json --use-descript

# Week 2: 5 tutorial videos
node batch-video-generator.js tutorials.json --use-descript

# Week 3: 5 news/update videos
node batch-video-generator.js updates.json --use-descript
```

### Tip 4: Track SEO Performance
After uploading to YouTube:
1. Monitor watch time
2. Check comments for feedback
3. Iterate on topics

## 🎓 Advanced: Custom Prompts

Edit `image-prompt-generator.js` to customize image generation:

```javascript
// Change to your preferred style
const defaultPrompts = [
  {
    id: 'flux_0',
    section: 'Your Custom Scene',
    prompt: 'Your detailed image prompt here...',
  }
];
```

## 📞 Support

Check logs for errors:
```bash
cat logs/pipeline-*.log
```

Verify dependencies:
```bash
npm install
pip install -r requirements.txt
```

Test individual phases:
```bash
node scrape-and-convert.js "https://example.com"
node clean-jsonl.js dataset.jsonl
node generate-video-script.js
```

## Summary

You have everything needed to generate a professional YouTube video library:

✅ **Automated pipeline** - From article to video in 10-15 min
✅ **Multiple topics** - 5 pre-selected high-SEO videos ready
✅ **Free captions** - Descript auto-captions (included in your plan)
✅ **Batch processing** - Generate multiple videos in parallel
✅ **Quality output** - Professional 1080p videos with captions
✅ **Low cost** - ~$1/video (just APIs, no software)

**Ready to launch your AI education channel!**

---

**Next: Run this command to generate your first video:**
```bash
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/" --use-descript
```

Good luck! 🚀
