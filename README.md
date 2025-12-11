# Firecrawl → JSONL → Video Pipeline

Complete automation for converting web articles into AI-ready datasets and video production materials.

## What This Does

```
Website URL
    ↓
[PART 1] Scrape with Firecrawl
    ↓
[PART 2] Save as JSON + JSONL
    ↓
[PART 3] Clean for AI ingestion
    ↓
[PART 4] Generate video scripts
    ↓
[PART 5] Create storyboards & graphs
    ↓
Video Production Ready (Pika Labs, Runway, Luma AI, etc.)
```

## Quick Start

### One-Command Pipeline

```bash
npm install
node orchestrate.js "https://example.com/article"
```

This runs all 5 steps automatically and generates:
- ✅ `dataset.jsonl` - AI-ready dataset
- ✅ `COMPLETE_VIDEO_SCRIPT.md` - Full production guide
- ✅ `video-narration.md` - What to say
- ✅ `video-storyboard.md` - Visual structure
- ✅ `slide-deck.md` - Presentation outline
- ✅ `video-graphs.md` - ASCII diagrams
- ✅ `video-editing-guide.md` - Post-production guide

### Or Run Steps Individually

**Step 1: Scrape & Convert**
```bash
node scrape-and-convert.js "https://example.com/article"
```
Outputs: `article.json`, `article.jsonl`, `dataset.jsonl`

**Step 2: Clean for AI**
```bash
node clean-jsonl.js dataset.jsonl
```
Outputs: `dataset.jsonl.cleaned`, `clean-report.json`

**Step 3: Generate Video Script**
```bash
node generate-video-script.js
```
Outputs: 6 markdown files with complete video production materials

## Generated Files Explained

### Core Data Files

| File | Purpose | Use Case |
|------|---------|----------|
| `dataset.jsonl` | AI-ready dataset (one JSON per line) | Feed into Claude, use for fine-tuning |
| `article.json` | Raw scraped data with metadata | Archive, debugging |

### Video Production Files

| File | Purpose | How to Use |
|------|---------|-----------|
| `COMPLETE_VIDEO_SCRIPT.md` | Master file with everything | Start here - contains all production info |
| `video-narration.md` | What to say | Record your voiceover using this |
| `video-storyboard.md` | Scene breakdown with timing | Plan your shots and B-roll |
| `slide-deck.md` | Slide outlines | Create visuals in Canva/Figma/PPT |
| `video-graphs.md` | ASCII diagrams and charts | Include in slides or use as reference |
| `video-editing-guide.md` | Transitions, timing, audio tips | Follow during editing |

## Production Workflow

### Option A: Manual Video Creation

1. **Record Narration** (5-10 min)
   - Read `video-narration.md` into microphone
   - Use: Audacity (free) or Adobe Audition
   - Export as MP3

2. **Create Visuals** (15-30 min per slide)
   - Use `slide-deck.md` as outline
   - Use `video-graphs.md` for diagrams
   - Tools: Figma (free), Canva, PowerPoint
   - Export slides as PNG/MP4

3. **Edit in Video Software** (30-60 min)
   - Follow `video-editing-guide.md` for timing
   - Sync audio with slides
   - Add transitions from guide
   - Tools: DaVinci Resolve (free), Adobe Premiere

### Option B: AI Video Generation (Fastest)

1. **Prep Materials**
   - Narration: Record from `video-narration.md`
   - Slides: Create from `slide-deck.md`
   - Storyboard: Use `video-storyboard.md`

2. **Use AI Video Tools**
   - **Pika Labs**: Text + images → video (fastest)
   - **Runway Gen-2**: Video generation with control
   - **Luma AI**: Cinematic quality

3. **Quick Process**
   ```
   1. Export slide images from Figma/Canva
   2. Upload storyboard to AI tool
   3. Paste narration
   4. Generate video (2-5 min per 1 min of content)
   5. Download and edit in DaVinci Resolve
   ```

## Example: Complete Workflow

### For the Claude Code vs Codex article:

```bash
# 1. Run full pipeline (2-3 minutes)
node orchestrate.js "https://www.nathanonn.com/claude-code-vs-codex-why-i-use-both-and-you-should-too/"

# Output files ready:
# - dataset.jsonl (for AI training)
# - COMPLETE_VIDEO_SCRIPT.md (complete guide)
# - 6 markdown files for production

# 2. Record narration (10 minutes)
# Read: video-narration.md into Audacity
# Export: narration.mp3

# 3. Create slides (30 minutes)
# Open: Figma or Canva
# Reference: slide-deck.md
# Include: Diagrams from video-graphs.md
# Export: slide_1.png, slide_2.png, etc.

# 4. Generate AI video (5 minutes)
# Go to: Pika Labs / Runway / Luma
# Upload: slides + narration
# Generate: final_video.mp4

# 5. Final edit (15 minutes)
# Open: DaVinci Resolve
# Import: final_video.mp4
# Follow: video-editing-guide.md
# Add: intro/outro, music, effects
# Export: final_video_upload.mp4

# Total time: ~60-90 minutes for production-ready video
```

## File Structure

```
.
├── orchestrate.js              # Main pipeline orchestrator
├── scrape-and-convert.js       # Part 1-3: Scrape & convert
├── clean-jsonl.js              # Part 4: Clean for AI
├── generate-video-script.js    # Part 5: Generate scripts
├── package.json                # Dependencies
├── README.md                   # This file
│
└── [Generated Files]
    ├── dataset.jsonl           # AI-ready data
    ├── COMPLETE_VIDEO_SCRIPT.md
    ├── video-storyboard.md
    ├── video-narration.md
    ├── video-graphs.md
    ├── slide-deck.md
    ├── video-editing-guide.md
    └── clean-report.json
```

## Advanced Usage

### Custom URL
```bash
node orchestrate.js "https://your-site.com/custom-article"
```

### Just Scrape
```bash
node scrape-and-convert.js "https://example.com"
```

### Just Generate Video Script
```bash
# First create dataset.jsonl, then:
node generate-video-script.js
```

### Just Clean Data
```bash
node clean-jsonl.js your-file.jsonl
```

## Tips for Best Results

### Dataset Quality
- **Longer content = better structure** (aim for 5000+ words)
- Complex topics with sections generate better storyboards
- Clean URLs with good metadata = better titles

### Video Quality
- **Narration**: Speak naturally, use good microphone (USB mic ~$30)
- **Slides**: Keep text minimal (5-7 words per slide max)
- **Pacing**: Follow timing guide - don't rush explanations
- **Music**: Use royalty-free from YouTube Audio Library

### Distribution Tips
- Upload to YouTube Shorts, TikTok, Instagram Reels
- Use slide content as chapters in YouTube description
- Link back to original article
- Include dataset.jsonl in video description for attribution

## Troubleshooting

### Firecrawl scrape fails
- Check your internet connection
- Verify URL is accessible
- Some sites may block scraping (try a different URL)

### Blank sections in video script
- Article may have minimal structure
- Try a different article with more sections
- Manually edit COMPLETE_VIDEO_SCRIPT.md

### JSONL validation warnings
- Not critical - most warnings are about optional fields
- Check clean-report.json for details
- Manual edits acceptable for your use case

## Requirements

- Node.js 14+ (check: `node --version`)
- npm (included with Node.js)
- Internet connection (for Firecrawl API)
- ~50MB disk space for output files

## Installation

```bash
# Clone or copy files to your directory
cd your-directory

# Install dependencies
npm install

# Run pipeline
node orchestrate.js "YOUR_URL_HERE"
```

## Privacy & Scraping

- **Respect robots.txt** - Don't scrape sites that forbid it
- **Terms of Service** - Check ToS before scraping
- **Personal data** - Remove PII before sharing datasets
- **Attribution** - Always link back to original source

## Next Steps

1. ✅ Run the pipeline
2. ✅ Review `COMPLETE_VIDEO_SCRIPT.md`
3. ✅ Record narration
4. ✅ Create slides
5. ✅ Generate AI video
6. ✅ Edit and export
7. ✅ Upload and share

## Questions?

- Check the generated markdown files for detailed guidance
- Review `video-editing-guide.md` for technical details
- Experiment with different article URLs to see variations

---

**Ready to create?** Start with:
```bash
npm install && node orchestrate.js "https://your-article-url.com"
```

Happy video making! 🎬
