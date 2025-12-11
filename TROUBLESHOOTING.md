# Troubleshooting Guide

## Problem: "Firecrawl API error" or "scraping failed"

### Causes
- Firecrawl public API has rate limits
- Website blocks scraping
- Website requires authentication
- Poor internet connection

### Solutions

**Option 1: Install Firecrawl CLI** (Recommended)
```bash
npm install -g firecrawl
npx firecrawl scrape "https://your-url.com"
```

**Option 2: Manually create dataset.jsonl**
```bash
# Use Firecrawl web interface at https://app.firecrawl.dev
# 1. Go to website
# 2. Enter URL
# 3. Click Extract
# 4. Copy JSON output
# 5. Paste into article.json
# 6. Run: node clean-jsonl.js
```

**Option 3: Bypass with manual HTML**
```bash
# Save HTML from browser
# Save as: article.html
# Use online converter: https://turndown.joplin.app
# Convert to Markdown: article.md
# Create dataset.jsonl manually (see template below)
```

### Manual dataset.jsonl Template
```json
{
  "id": "my-article",
  "url": "https://example.com/article",
  "title": "Your Article Title",
  "description": "Brief description",
  "author": "Author Name",
  "publishDate": "2024-12-10",
  "content": "# Your Article Title\n\nArticle content here in markdown format...",
  "sections": [
    {"heading": "Section 1", "content": "..."},
    {"heading": "Section 2", "content": "..."}
  ],
  "extracted_at": "2024-12-10T00:00:00Z",
  "language": "en"
}
```

---

## Problem: "Cannot find module 'firecrawl-js'"

### Causes
- Dependencies not installed
- npm install failed

### Solution
```bash
# Clear cache and reinstall
rm -rf node_modules
npm cache clean --force
npm install
```

---

## Problem: "dataset.jsonl not found" when generating video script

### Causes
- Scraping step didn't complete
- Files saved in wrong directory
- Filename is different

### Solution
```bash
# Check what files exist
ls *.jsonl

# If you have article.jsonl instead:
mv article.jsonl dataset.jsonl

# If you have nothing, run scraping first:
node scrape-and-convert.js "https://your-url"
```

---

## Problem: Video script has blank sections or minimal content

### Causes
- Article is too short (< 500 words)
- Article has no clear structure/headings
- Scraping didn't capture full content

### Solutions

**1. Use a better article**
- Try articles with 2000+ words
- Articles with clear section headings work best
- Blog posts work better than product pages

**2. Manually edit the script**
```markdown
# Edit these files directly:
- COMPLETE_VIDEO_SCRIPT.md
- video-narration.md
- slide-deck.md

# Add more detail, sections, or examples
# It's okay to customize!
```

**3. Combine multiple articles**
```bash
# Create dataset.jsonl manually with content from multiple sources
# Combine sections from different articles
# The pipeline will work with mixed content
```

---

## Problem: Node.js not found

### Causes
- Node.js not installed
- Not in system PATH

### Solution
1. Download: https://nodejs.org
2. Install the LTS version (includes npm)
3. Restart terminal
4. Verify: `node --version`

---

## Problem: Firecrawl returns incomplete markdown

### Causes
- Website has complex formatting
- Heavy JavaScript content
- Behind paywall/authentication

### Solution

**Option 1: Use alternative scraper**
```bash
# Try Playwright scraper instead
npm install playwright
# Then create custom scraper script
```

**Option 2: Manual extraction**
```bash
# 1. Open website in browser
# 2. Select and copy text
# 3. Paste into text editor
# 4. Clean up formatting manually
# 5. Save as article.md
# 6. Manually create dataset.jsonl (see template above)
```

**Option 3: Use PDF if available**
```bash
# If article is available as PDF:
# 1. Download PDF
# 2. Use PDF-to-text converter
# 3. Paste content into dataset.jsonl
```

---

## Problem: Clean-report.json shows many warnings

### Causes
- Missing optional metadata
- Unusual formatting
- Not critical issues

### Solution
```bash
# Warnings are informational only
# Check what they say:
cat clean-report.json

# If content is present and valid:
# You can ignore warnings and proceed

# If there are actual ERRORS:
# Edit dataset.jsonl to fix required fields:
# - id (required)
# - url (required)
# - title (required)
# - content (required)
```

---

## Problem: Video script timing seems off

### Causes
- Content was longer/shorter than expected
- Algorithm estimated based on character count
- Your speaking pace differs

### Solution
```bash
# Adjust timing in video-storyboard.md:
# 1. Record narration first
# 2. Check actual duration
# 3. Update timestamps in storyboard

# General rule:
# - Slow, clear speech: ~100 chars per 10 seconds
# - Normal speech: ~150 chars per 10 seconds
# - Fast speech: ~200 chars per 10 seconds
```

---

## Problem: Cannot record narration (no microphone)

### Solutions

**Option 1: Use Text-to-Speech**
```bash
# Windows: Built-in narrator
# Mac: System Preferences > Accessibility > Speech
# Linux: espeak command

# Or use online TTS:
# - Google TTS (free)
# - Natural Reader (free trial)
# - ElevenLabs (AI voices, paid)

# Then use MP3 as narration.mp3
```

**Option 2: Hire voice actor**
```bash
# Fiverr: $5-20 for narration
# Upwork: $15-100 depending on quality
# Paste video-narration.md, get MP3 back
```

---

## Problem: Slides don't look professional

### Tips

**Use templates:**
- Canva templates (free)
- Figma community templates (free)
- Google Slides templates (free)

**Good slide design:**
- Consistent colors (2-3 colors max)
- Large text (24pt+ minimum)
- High-contrast backgrounds
- One idea per slide
- Minimal text (5-7 words)

**Resources:**
- Font pairing: https://fontpair.co
- Color palette: https://coolors.co
- Icons: https://feathericons.com (free)

---

## Problem: AI video tool not producing good quality

### Troubleshooting

**Pika Labs tips:**
- Images must be clear and readable
- Narration should be clear (no background noise)
- Follow timing guide closely
- Try 30-second clips first

**Runway Gen-2 tips:**
- Detailed descriptions help
- Reference images improve output
- Shorter prompts often work better
- Longer processing = better quality

**Luma AI tips:**
- Best for cinematic quality
- Slower than others (5-10 min)
- Handles motion better
- Free credits every month

---

## Problem: YouTube upload fails

### Common issues

**Too large file:**
```bash
# Reduce bitrate in DaVinci Resolve
# Export settings:
# - Resolution: 1080p (1920x1080)
# - Bitrate: 5-8 Mbps (not 20+)
# - Format: H.264
```

**Missing required info:**
- Title (required)
- Description (required for monetization)
- Thumbnail (recommended)
- Category (required)

**Copyright issues:**
- Verify all music is royalty-free
- Verify all images are free to use
- Original article link required

---

## Problem: "Out of memory" or script crashes

### Causes
- Very large articles (5000+ words)
- Running on limited system RAM
- Too many files open

### Solution
```bash
# Increase Node.js memory limit
node --max-old-space-size=4096 orchestrate.js "URL"

# Or process in parts:
# 1. Scrape only: node scrape-and-convert.js "URL"
# 2. Wait 1 minute
# 3. Clean: node clean-jsonl.js dataset.jsonl
# 4. Wait 1 minute
# 5. Video script: node generate-video-script.js
```

---

## Problem: Unsure how to proceed after pipeline completes

### Step-by-step

```
1. Pipeline creates: COMPLETE_VIDEO_SCRIPT.md ✅
   └─> Open this file first!

2. You read: video-narration.md
   └─> Record into Audacity (mic or TTS)

3. You create: slides from slide-deck.md
   └─> Use Canva (easiest for beginners)
   └─> Add diagrams from video-graphs.md

4. You upload: slides + narration to AI video tool
   └─> Pika Labs (fastest, free credits)
   └─> Get video.mp4 back

5. You edit: video.mp4 in DaVinci Resolve
   └─> Follow video-editing-guide.md
   └─> Add music, intro, outro, effects

6. You upload: to YouTube
   └─> Add link to original article
   └─> Share on social media
```

---

## Still Stuck?

### Resources
- Read: README.md (full documentation)
- Check: EXAMPLE_OUTPUT.md (see what you should get)
- Follow: QUICK_START.md (simplified version)
- Review: Generated markdown files (they have instructions)

### Manual Help
1. Look at your generated `COMPLETE_VIDEO_SCRIPT.md`
2. Each section has detailed instructions
3. You can edit these files directly
4. Manual customization is acceptable

### Online Tools
- Firecrawl web interface: https://app.firecrawl.dev
- Free video tools: https://tools.google.com/dlpage/gaiad
- Online converters: https://cloudconvert.com
- AI voice generation: https://ttsmaker.com

---

## Quick Checklist

If something breaks:

- [ ] Check internet connection
- [ ] Verify Node.js is installed (`node --version`)
- [ ] Verify npm is installed (`npm --version`)
- [ ] Run `npm install` again
- [ ] Delete bad files and start over
- [ ] Try with different article URL
- [ ] Read generated markdown files (they have guidance)
- [ ] Check file permissions (write access)
- [ ] Try with simpler article first
- [ ] Create dataset.jsonl manually if scraping fails

---

**Need more help?** See the generated markdown files - they contain detailed production guidance!
