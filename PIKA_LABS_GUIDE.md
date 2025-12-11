# AI VIDEO GENERATION GUIDE
## Using Pika Labs, Runway, or Luma AI

---

## OPTION 1: PIKA LABS (Recommended - Fastest & Easiest)

### What You'll Need
- Narration MP3 (from video-narration.md)
- Chart PNG files (generated from SVG files)
- Free account at https://pika.art

### Step-by-Step Process

**Step 1: Create Project**
1. Go to https://pika.art
2. Sign up (free account includes credits)
3. Click "New Project"
4. Name it: "Claude Code vs Codex"

**Step 2: Set Up Timeline**
1. Click "Create video"
2. Select "Duration: 17 minutes" OR "Custom: 1020 seconds"
3. Frame rate: 30 fps
4. Resolution: 1920x1080

**Step 3: Upload Your Assets**
1. Upload all PNG chart files (chart_01 through chart_25)
2. Upload narration.mp3
3. Tag each image with timing (00:05, 00:10, etc.)

**Step 4: Create Scenes**

For each scene:
- Select chart image
- Set duration (from VIDEO NARRATION WITH MARKERS)
- Add audio segment (copy from narration)
- Add transition (fade recommended)

**Example Scene 1:**
- Image: chart_01_question.png
- Duration: 5 seconds (00:00 to 00:05)
- Audio: "Hey everyone! Have you ever wondered about Claude Code or Codex?"
- Transition: Fade in

**Example Scene 2:**
- Image: chart_02_vs.png
- Duration: 5 seconds (00:05 to 00:10)
- Audio: "You're probably asking the wrong question."
- Transition: Fade

(Continue for all 25 charts...)

**Step 5: Add Narration**
1. Upload video-narration.mp3 as full background audio
2. Sync with chart transitions
3. Adjust volume (narration: 100%, background music: 50%)

**Step 6: Add Transitions**
- Between each scene: Fade (0.5 seconds)
- Duration: Check timing in visual guide

**Step 7: Generate**
1. Click "Generate Video"
2. Wait 5-10 minutes
3. Download as MP4 (1920x1080)

**Step 8: Download & Edit**
1. Download as video.mp4
2. (Optional) Import into DaVinci Resolve for final polish
3. Upload to YouTube

### Timeline Example for Pika Labs

```
00:00-00:05: chart_01_question.png + narration "Hey everyone..."
00:05-00:10: chart_02_vs.png + narration "You're asking..."
00:10-00:15: chart_03_team.png + narration "They're not competitors..."
00:15-00:30: [continue pattern...]
...
17:00: End
```

---

## OPTION 2: RUNWAY GEN-2 (More Control)

### Advantages
- Better control over transitions
- Multiple generation models
- Better for complex animations

### Process

**Step 1: Prepare Assets**
- Export all charts as PNG (1920x1080)
- Prepare narration.mp3
- Create a shot list (see next section)

**Step 2: Upload to Runway**
1. Go to https://app.runwayml.com
2. Create new project
3. Upload images and audio

**Step 3: Create Storyboard**
For each chart image:
- Add text prompt: "Professional chart showing [description], fade transition"
- Duration: 3-5 seconds
- Add previous image: Link to next chart

**Step 4: Generate**
1. Select "Gen-2" model
2. Click generate for each transition
3. Takes 2-3 minutes per transition

**Step 5: Compile**
1. Use Runway's timeline editor
2. Import all generated clips
3. Add narration track
4. Export as final video

---

## OPTION 3: LUMA AI (Most Cinematic)

### Advantages
- Best visual quality
- Realistic transitions
- Most cinematic results

### Process

**Step 1: Prepare**
- Same chart assets as Pika
- Narration ready

**Step 2: Upload**
1. Go to https://lumalabs.ai
2. Create project
3. Upload images

**Step 3: Configure**
- Set video style: "Professional presentation"
- Quality: 4K (optional)
- Duration: Match your narration timing

**Step 4: Generate**
- Takes longer (10-15 min) but results are cinematic
- Download as 4K MP4

**Step 5: Edit**
- Optional: Import into DaVinci Resolve
- Add narration (overlay audio)
- Export and upload

---

## QUICK COMPARISON

| Feature | Pika Labs | Runway | Luma AI |
|---------|-----------|--------|---------|
| Speed | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐ Medium | ⭐⭐ Slow |
| Ease | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐ Medium | ⭐⭐⭐ Medium |
| Quality | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best |
| Control | ⭐⭐⭐ Basic | ⭐⭐⭐⭐ Advanced | ⭐⭐⭐ Good |
| Cost | Free tier | Free tier | Free tier |
| **Recommendation** | ✅ Best for beginners | For advanced users | For premium quality |

---

## RECOMMENDED WORKFLOW

### Fastest (30 minutes total)
1. Export all SVG → PNG (1920x1080)
2. Use Pika Labs
3. Upload images + narration
4. Let AI generate video
5. Download & upload to YouTube

### Best Quality (45 minutes total)
1. Create charts in Pika Labs
2. Generate video
3. Download
4. Import into DaVinci Resolve
5. Add background music
6. Final color grading
7. Export & upload

### Most Control (60+ minutes)
1. Generate with Runway Gen-2
2. Have fine-tune control over each transition
3. Compile in Runway
4. Export
5. Edit in DaVinci Resolve
6. Upload

---

## PRO TIPS

### For Pika Labs
- Keep narration clear and loud (normalize audio first)
- Chart images should have high contrast
- Use solid backgrounds (avoid busy patterns)
- Test with 2-3 scenes first before doing all 25

### For Runway
- Write detailed prompts for each transition
- Use same camera angle throughout
- Reference images help (show "before" and "after")
- Generate one transition at a time to monitor quality

### For Luma AI
- Cinematic style works best
- Wait for full generation (don't interrupt)
- 4K export is worth the wait
- Can upscale from lower resolution if needed

---

## COMMON ISSUES & FIXES

**"Video looks jerky"**
→ Increase number of frames between charts (add 1-2 second pauses)

**"Narration doesn't sync"**
→ Check timing in NARRATION_WITH_MARKERS.md
→ Manually adjust audio track position

**"Charts look pixelated"**
→ Ensure PNG files are 1920x1080 minimum
→ Regenerate from SVG at higher resolution

**"Audio is too quiet"**
→ Normalize audio in Audacity before uploading
→ Increase narration track volume to 100%

**"Transitions feel abrupt"**
→ Add fade effect (0.5-1 second) between scenes
→ Slow down chart change timing

---

## FINAL STEP: UPLOAD TO YOUTUBE

Once you have your final video.mp4:

1. **Title:** "Claude Code vs Codex: Why I Use Both (And You Should Too)"

2. **Description:**
```
Watch the full article: [Your Article URL]

In this video, I show you why Claude Code and Codex aren't competitors—they're collaborators.

Learn:
- Why using just one limits you
- How to use them together for bulletproof code
- A real-world example from my WordPress theme
- The exact workflow I use for every feature

Timestamps:
00:00 - Intro
01:00 - The Problem with Codex Alone
02:00 - The Problem with Claude Code Alone
03:15 - The Solution: Using Both
04:30 - Real World Example
09:30 - Final Results
10:30 - The Workflow
13:30 - Pro Tips
15:15 - Conclusion

Resources:
- Original Article: [Your Article URL]
- Newsletter: The Art of Vibe Coding
- GitHub: [Your GitHub]
- LinkedIn: [Your LinkedIn]

#ClaudeCode #Codex #AI #Development
```

3. **Tags:**
   - claude-code
   - codex
   - gpt-5
   - ai-development
   - code-review
   - programming
   - ai-tools

4. **Thumbnail:**
   - Use chart_02_vs.png (Claude Code vs Codex)
   - Add text: "Both, Not Either"
   - Add arrow pointing to "Watch Now"

5. **Category:** Education / How-To

6. **Visibility:** Public

Done! Your video is live.
