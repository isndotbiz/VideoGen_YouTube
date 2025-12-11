# Quick Start: Generate 6 Animated Videos with Runway ($5 Budget)

## Budget Breakdown
- **Total Budget**: $5.00
- **Cost per video**: ~$0.80-$1.00
- **Expected videos**: 5-6 animated loops (5-10 seconds each)

## Step-by-Step Guide

### 1. Go to Runway's Web Interface
- Visit: https://runwayml.com
- Sign in with your account (you have API access, web access should work too)
- Click **"Create Project"** or go to the studio

### 2. Select Gen-3 Motion
- Choose **"Gen-3 Motion"** from the available models
- This converts images → animated video loops

### 3. Upload & Animate (Repeat for each image below)

For each animation, you'll:
1. Upload the image from `output/generated_images/`
2. Paste the motion prompt
3. Click **Generate**
4. Wait 2-3 minutes
5. Download the video

---

## 6 Recommended Animations (Priority Order)

### Animation 1: Neural Networks Title
**File**: `Claude_Code_Showcase_006_image.png` (or similar intro image)

**Motion Prompt**:
```
Camera slowly dollies forward through the center of the split screen while
both neural networks pulse with energy, particles flowing between them,
subtle rotation of the network structures, seamless loop returning to
starting position
```

**Expected**: High-impact title animation


### Animation 2: Golden Thread Code
**File**: `Claude_Code_Showcase_007_image.png`

**Motion Prompt**:
```
Golden thread continuously weaves through the code structure, starting from
bottom left and traveling to top right, code blocks light up in sequence as
thread passes through them, gentle rotation of entire structure, thread
leaves brief light trail that fades
```

**Expected**: Shows Claude Code's sequential processing


### Animation 3: Parallel Execution
**File**: `Codex_Showcase_012_image.png`

**Motion Prompt**:
```
Six threads flow continuously from left to right at different speeds, files
move along conveyor-like paths, completion checkmarks appear on finished
files, new files queue up on the left, threads occasionally split and merge,
industrial mechanical rhythm
```

**Expected**: Illustrates Codex's parallel power


### Animation 4: Comparison Table
**File**: `Comparison_Visuals_018_image.png`

**Motion Prompt**:
```
Features illuminate one by one from top to bottom, icons animate to
demonstrate their function, highlighting sweeps down each column, checkmarks
appear next to applicable use cases, subtle gradient background shifts
between amber and blue zones
```

**Expected**: Feature comparison comes alive


### Animation 5: Interactive Debugging
**File**: `Use_Cases_024_image.png`

**Motion Prompt**:
```
Developer types questions, Claude appears on screen with explanations,
cursor highlights relevant code sections, developer nods and makes notes,
rubber duck appears to listen, screen content updates showing progress
```

**Expected**: Real-world use case


### Animation 6: Bulk Automation
**File**: `Use_Cases_025_image.png`

**Motion Prompt**:
```
Files change from gray (pending) to blue (processing) to green (complete)
in waves, multiple worker bots move between files, progress counter
rapidly increments, dashboard charts update showing completion percentage
```

**Expected**: Automation at scale

---

## Alternative: If Using API

If you want to use the Runway API directly, here's the correct format:

```bash
# 1. Create an upload
curl -X POST https://api.dev.runwayml.com/v1/uploads \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "image.png",
    "type": "image"
  }'

# 2. Get the upload URL and upload your file
# 3. Use the asset ID to create generation task
curl -X POST https://api.dev.runwayml.com/v1/image_to_video \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "promptImage": "ASSET_ID_FROM_STEP_1",
    "motionPrompt": "YOUR_MOTION_PROMPT",
    "duration": 5,
    "model": "gen3",
    "quality": "high"
  }'
```

---

## Pro Tips

1. **Start with Animation 1**: Most visually impactful for testing
2. **Length**: Keep under 10 seconds for smooth loops
3. **Quality**: Use "high" for best results on your budget
4. **Format**: Download as MP4 when complete
5. **Naming**: Save as `animation_01_title.mp4`, `animation_02_thread.mp4`, etc.

---

## What to Do After

Once you have all 6 videos:

1. **Place in project folder**: `output/animated_loops/`
2. **Update main video**: Replace static images with these in your Shotstack render
3. **Or create highlights video**: Combine into a 1-minute promo

---

## Tracking Your Spend

| Animation | Cost | Status |
|-----------|------|--------|
| Neural Networks | $0.80 | ___ |
| Golden Thread | $0.80 | ___ |
| Parallel Flow | $0.80 | ___ |
| Comparison | $0.80 | ___ |
| Debugging | $0.80 | ___ |
| Automation | $0.80 | ___ |
| **TOTAL** | **$4.80** | ___ |

Budget remaining: $0.20 (save for retries/improvements)

---

## Questions?

- Check: https://docs.dev.runwayml.com/
- Dashboard: https://runwayml.com/dashboard
- Your API key has been added to `.env`
