# Subtitle/Caption Services - Complete Guide

Add professional captions to your videos for better SEO and accessibility.

## 🎯 Your Options (Ranked by Best Fit)

### Option 1: **Descript** ⭐ BEST (Already in Your Plan)
```bash
node pipeline-complete.js "url" --use-descript
```
**Features:**
- ✅ Auto-generates captions from narration
- ✅ Speaker detection
- ✅ Noise removal
- ✅ Professional SRT files
- ✅ FREE (included in Creator Plan)

**Cost:** $0 (you already have it!)
**Quality:** ⭐⭐⭐⭐⭐
**Speed:** 5-10 min processing

**Why:** You literally already paid for this in your Creator Plan. Just use it.

---

### Option 2: **OpenAI Whisper** (Open Source, FREE)
```bash
pip install openai-whisper
node generate-whisper-subtitles.js output/narration.mp3
```
**Features:**
- ✅ Completely FREE and open source
- ✅ Works offline
- ✅ Very accurate
- ✅ Generates SRT files
- ✅ No API keys needed

**Cost:** $0 (open source)
**Quality:** ⭐⭐⭐⭐
**Speed:** 2-5 min (depends on audio length)

**Why:** Best free option if you want local processing.

**Output:** `output/subtitles.srt` (ready to add to video)

---

### Option 3: **AssemblyAI** (Simple API, Cheap)
```bash
# Add ASSEMBLYAI_API_KEY to .env
node generate-assemblyai-subtitles.js output/narration.mp3
```
**Features:**
- ✅ Simple API integration
- ✅ Fast processing (1 minute audio = 30 seconds)
- ✅ High accuracy
- ✅ Generates SRT files
- ✅ Cheap ($0.000125 per second of audio)

**Cost:** ~$0.10 per video (very cheap!)
**Quality:** ⭐⭐⭐⭐
**Speed:** 30 sec - 2 min

**Why:** Good balance of cost and quality.

**Typical cost for 5 min video:** $0.0375

---

### Option 4: **Google Speech-to-Text** (Professional, Moderate Cost)
```bash
# Add GOOGLE_APPLICATION_CREDENTIALS to .env
node generate-google-subtitles.js output/narration.mp3
```
**Features:**
- ✅ Excellent accuracy
- ✅ Multiple language support
- ✅ Professional quality
- ✅ Generates SRT files

**Cost:** ~$0.04 per minute audio
**Quality:** ⭐⭐⭐⭐⭐
**Speed:** 1-3 min

**Why:** If you want top-tier accuracy.

**Typical cost for 5 min video:** $0.20

---

### Option 5: **Rev.com** (Professional Service, Best Quality)
```bash
# Manual upload to https://www.rev.com
# Or API integration for batch
```
**Features:**
- ✅ Human transcribers (100% accurate)
- ✅ Multiple language support
- ✅ Professional SRT formatting
- ✅ Quick turnaround (1-2 hours)

**Cost:** $1.10 per minute audio
**Quality:** ⭐⭐⭐⭐⭐⭐
**Speed:** 1-2 hours (human service)

**Why:** Only if you need 100% accuracy and have budget.

**Typical cost for 5 min video:** $5.50 (expensive!)

---

### Option 6: **Subly** (Simple Web Tool, Budget)
```bash
# Upload MP3 to https://www.subly.ai
# Download SRT file
```
**Features:**
- ✅ Simple web interface
- ✅ AI auto-generation
- ✅ Manual editing available
- ✅ SRT export

**Cost:** Free (limited), or $5-10/month
**Quality:** ⭐⭐⭐
**Speed:** 2-5 min

**Why:** Good for manual tweaking before upload.

---

## 💰 Cost Summary

| Service | Per 5-Min Video | Best For |
|---------|-----------------|----------|
| **Descript** | $0 (your plan) | Professional videos (captions included) |
| **Whisper** | $0 (free) | Budget, local processing |
| **AssemblyAI** | ~$0.04 | Cheap, fast, good accuracy |
| **Google** | ~$0.20 | Professional accuracy |
| **Rev.com** | $5.50 | Perfect accuracy (human) |
| **Subly** | $0-10/mo | Simple manual editing |

---

## 🎯 My Recommendation

### Use **Descript** (Already in Your Plan!)

```bash
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/" --use-descript
```

**Why:**
- ✅ Already included in your Creator Plan
- ✅ No additional cost
- ✅ Professional quality
- ✅ Auto-captions = Better YouTube ranking
- ✅ One command does everything

**You're literally paying for it anyway, so use it!**

---

## Alternative: Free Local Subtitles with Whisper

If you prefer free, local processing:

```bash
# 1. Install Whisper
pip install openai-whisper

# 2. Generate subtitles from narration
whisper output/narration.mp3 --output_format srt --output_dir output

# 3. Add subtitles to video (FFmpeg)
ffmpeg -i output/final_video.mp4 -i output/narration.srt \
  -c:v copy -c:a copy -c:s mov_text output/final_with_subs.mp4
```

**Cost:** $0
**Quality:** ⭐⭐⭐⭐
**Time:** 2-5 minutes total

---

## Implementation Options

### Option A: Use Descript (Simplest)
```bash
node pipeline-complete.js "url" --use-descript
# Done! Video has captions automatically
```

### Option B: Use Whisper (Free)
```bash
# Generate subtitles
whisper output/narration.mp3 --output_format srt --output_dir output

# Add to video with FFmpeg
ffmpeg -i output/final_video.mp4 -i output/narration.srt \
  -c:v copy -c:a copy -c:s mov_text output/final_with_subs.mp4
```

### Option C: Use AssemblyAI (Cheap)
```bash
# Add API key to .env
ASSEMBLYAI_API_KEY=your_key_here

# Generate and embed
node generate-subtitles-assemblyai.js output/narration.mp3
```

---

## Quick Start: Generate One Video with Subtitles

### Method 1: Descript (Recommended - Includes Captions)
```bash
cd D:\workspace\VideoGen_YouTube

# Generates complete video with auto-captions
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/" --use-descript

# Output: output/final_video.mp4 (with captions embedded)
```

**Time:** ~15-20 minutes
**Cost:** ~$1.06 (images + narration + videos, assembly FREE)
**Quality:** ⭐⭐⭐⭐⭐ (professional captions included)

### Method 2: Whisper (Free Subtitles)
```bash
# 1. Generate video without captions first
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/"

# 2. Generate subtitles with Whisper
pip install openai-whisper
whisper output/narration.mp3 --output_format srt --output_dir output

# 3. Add subtitles to video
ffmpeg -i output/final_video.mp4 -i output/narration.srt \
  -c:v copy -c:a copy -c:s mov_text output/final_with_subs.mp4
```

**Time:** ~20-25 minutes
**Cost:** ~$1.06 (images + narration + videos only)
**Quality:** ⭐⭐⭐⭐ (good subtitles)

---

## Subtitle File Formats

After generation, you'll have:

```
output/
├── narration.srt (subtitle file)
├── final_video.mp4 (video without captions)
└── final_with_subs.mp4 (video with captions embedded)
```

**SRT Format Example:**
```
1
00:00:00,000 --> 00:00:05,000
This is the first subtitle

2
00:00:05,000 --> 00:00:10,000
And this is the second one
```

---

## YouTube Subtitle Options

When uploading to YouTube, you can:

1. **Embed captions** (in video file) - Recommended
2. **Upload SRT file** to YouTube - YouTube auto-matches timing
3. **Let YouTube auto-generate** - Free but less accurate

If you embed captions in the MP4 file, they appear automatically.

---

## Summary Table

| Task | Service | Cost | Time | Command |
|------|---------|------|------|---------|
| Full video + captions | Descript | $0 (plan) | 15 min | `--use-descript` |
| Just subtitles (free) | Whisper | $0 | 3 min | `whisper file.mp3` |
| Just subtitles (fast) | AssemblyAI | ~$0.04 | 1 min | API call |
| Full video no captions | FFmpeg | $0 | 5 min | (requires install) |

---

## What to Do Now

### **Recommended: Generate with Descript**
```bash
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/" --use-descript
```

This gives you:
- ✅ Complete video with images
- ✅ Professional narration
- ✅ Auto-generated captions
- ✅ Ready to upload to YouTube
- ✅ All in one command
- ✅ Cost: ~$1.06

---

**Which option appeals to you?**

1. **Descript** (easy, professional, FREE with your plan)
2. **Whisper** (free, local, open source)
3. **AssemblyAI** (cheap API, fast)
4. **Something else?**

Just let me know and I'll generate one video for you!
