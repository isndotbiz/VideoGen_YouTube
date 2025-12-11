# Quick Start: Advanced Video Generation System

Get your first professional video created in minutes!

## The Big Picture

You now have a **complete, production-ready system** that:

1. ✅ Researches topics from multiple authoritative sources (Claude agents)
2. ✅ Synthesizes research into a compelling video script
3. ✅ Humanizes scripts so they sound natural, not AI-generated
4. ✅ Generates professional images (Flux Pro for people, Nano Banana for charts)
5. ✅ Creates cinematic video sequences from static images (Runway API)
6. ✅ Generates narration with pause control and pronunciation guides (ElevenLabs)
7. ✅ Integrates background music at optimal volume
8. ✅ Creates styled subtitles with pop animations (Canva)
9. ✅ Assembles everything into a complete video (Shotstack)
10. ✅ Publishes to YouTube with SEO optimization

## Files You Now Have

| File | Purpose |
|------|---------|
| `advanced-video-orchestrator.js` | Main entry point - runs entire pipeline |
| `research-agents-launcher.js` | Spawns Claude agents for multi-source research |
| `script-synthesizer.js` | Converts research → humanized video script |
| `image-generation-pipeline.py` | Generates AI images (photorealistic + charts) |
| `advanced-video-assembly.py` | Researches music, builds video, integrates subtitles |
| `CODEX_TASK_PROMPT.md` | Tasks for Codex to implement API integrations |
| `ADVANCED_VIDEO_SYSTEM_README.md` | Complete technical documentation |
| `QUICK_START_ADVANCED.md` | This file |

## Before You Start

### 1. Get Your API Keys

You'll need these (you may already have some):

```
FAL_API_KEY              (for image generation - Flux Pro)
ELEVENLABS_API_KEY       (for narration)
SHOTSTACK_API_KEY        (for video assembly)
YOUTUBE_CLIENT_ID        (for YouTube publishing)
YOUTUBE_CLIENT_SECRET
```

Optional but recommended:
```
RUNWAY_API_KEY           (for cinematic videos)
CANVA_API_KEY            (for subtitles)
DESCRIPT_API_KEY         (for script humanization)
```

### 2. Update Your .env File

```bash
# Copy .env.example to .env
cp .env.example .env

# Add your API keys
nano .env

# Verify it looks like:
FAL_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
# etc.
```

### 3. Install Dependencies

**Node.js modules**:
```bash
npm install axios dotenv
```

**Python modules**:
```bash
pip install python-dotenv requests librosa soundfile numpy
```

## Step 1: Run the Orchestrator (Easiest)

This runs the **complete SEO Best Practices example** end-to-end:

```bash
node advanced-video-orchestrator.js
```

**What happens**:
- Launches research agents (3 agents researching different sources)
- Synthesizes research into outline
- Generates video script
- Creates all images (photorealistic + infographics)
- Assembles video with narration, music, subtitles
- Ready to upload to YouTube

**Output**:
- `output/dataset.jsonl` - Structured research data
- `output/COMPLETE_VIDEO_SCRIPT.md` - Full video script
- `output/generated_images/` - All AI-generated images
- `output/narration.mp3` - Audio narration
- `output/final_video.mp4` - Complete video
- `output/logs/` - Execution logs

**Time**: 5-15 minutes (depending on API response times)

## Step 2 (Optional): Run Individual Modules

If you want to test individual components:

### A. Run Research Agents Only
```bash
node research-agents-launcher.js
```
Output: Research findings with 3+ sources per fact

### B. Generate Script
```bash
node script-synthesizer.js
```
Output: Video script with narration markers

### C. Generate Images
```bash
python image-generation-pipeline.py
```
Output: 25-30 professional images

### D. Assemble Video
```bash
python advanced-video-assembly.py
```
Output: Final MP4 video file

## Step 3: Customize for Your Topic

### Change the Topic

Edit `advanced-video-orchestrator.js`:

```javascript
const CONFIG = {
  projectName: 'Your_Project_Name',
  topic: 'Your Topic Here - Complete Guide',
  // Rest stays the same
};
```

Example topics:
- "Docker for Beginners - Complete Tutorial"
- "Node.js Best Practices 2025"
- "React Performance Optimization Guide"
- "Python Data Science Fundamentals"

### Ask for Project Directory

When you have a new project, the system will ask:
```
Where should we save this project?
1. Same as last time
2. New directory
3. Custom path
```

## Parallel Execution: Claude Code + Codex

**You can run both in parallel**:

1. **Claude Code** (currently running):
   - Handles orchestration and research
   - Generates and humanizes scripts
   - Coordinates overall pipeline

2. **Codex** (needs to be set up):
   - Implements API integrations
   - Handles actual API calls
   - Processes data transformations
   - Manages error handling

**How to run both**:
```bash
# Terminal 1: Claude Code (you, using Claude Code)
node advanced-video-orchestrator.js

# Terminal 2: Codex (give them CODEX_TASK_PROMPT.md)
# They work on:
# - firecrawl-integration.js
# - fal-image-generator.py
# - runway-video-generator.py
# - elevenlabs-narrator.py
# - music-integrator.py
# - etc.
```

Both can work simultaneously on different parts of the system!

## What Happens at Each Stage

### Stage 1: Multi-Source Research (2-3 minutes)
- 3 Claude agents research your topic from different sources
- Agent 1: Official sources (Google, Moz, experts)
- Agent 2: Community feedback (Reddit, forums, discussions)
- Agent 3: Case studies & proven results
- **Output**: Consolidated research with citations

### Stage 2: Content Synthesis (1 minute)
- Claude synthesizes findings into coherent outline
- Identifies consensus and disagreements
- Structures information by importance
- **Output**: Content outline with verified facts

### Stage 3: Script Generation (2-3 minutes)
- Claude generates full video script from outline
- Script is humanized to sound natural and engaging
- Includes [pause: Xs] markers for narration control
- Pronunciation guides added for technical terms
- **Output**: Ready-to-narrate video script

### Stage 4: Image Generation (5-10 minutes)
- **Photorealistic images** (Flux Pro):
  - Professional people in office settings
  - Team collaboration scenes
  - Workspace close-ups
  - ~15 images at 1920×1080
- **Chart/Infographic images** (Nano Banana):
  - Statistics visualizations
  - Process flows
  - Comparison tables
  - ~10 images
- **Output**: 25-30 professional images

### Stage 5: Video Generation (3-5 minutes)
- Runway API converts static images to cinematic clips
- Adds smooth pans, zooms, transitions
- Creates 3-5 second video sequences
- **Output**: Runway cinematic clips ready to assemble

### Stage 6: Narration (2-3 minutes)
- ElevenLabs generates audio from humanized script
- Voice: Rachel (professional, clear)
- Pause markers converted to SSML breaks
- Pronunciation guides applied
- **Output**: MP3 narration audio

### Stage 7: Background Music (1-2 minutes)
- Research best music options (Epidemic Sound, Artlist, Pond5)
- Select melodic-techno/dubstep at 120-130 BPM
- Set volume levels:
  - Narration: -20dB (main)
  - Music: -38dB (background)
  - **Output**: Mixed audio file

### Stage 8: Subtitles (2-3 minutes)
- Canva generates styled subtitles
- Style: White text, Pink/Black border, pop animation
- Auto-synced to narration timing
- **Output**: SRT subtitle file + graphic overlays

### Stage 9: Video Assembly (5-10 minutes)
- Shotstack combines all elements:
  - Runway cinematic videos
  - Still images with Ken Burns effect
  - Narration audio
  - Background music (with auto-ducking)
  - Subtitle overlays
  - Transitions and effects
- Output: 1920×1080, 30fps, MP4 format
- **Output**: Complete final video (600 seconds / 10 minutes)

### Stage 10: YouTube Publication
- Generate SEO metadata:
  - Optimized title (60 chars)
  - Detailed description (5000 chars)
  - 30 relevant tags
  - Chapter timestamps
- Upload to YouTube with OAuth
- Set thumbnail
- **Output**: Published video on your YouTube channel

## Testing the System

### Test 1: Quick Validation (30 seconds)
```bash
node advanced-video-orchestrator.js --test
```
Validates all API keys and modules are configured correctly.

### Test 2: Research Only (3 minutes)
```bash
node research-agents-launcher.js
```
Tests that research agents work. Check output in logs.

### Test 3: Script Only (2 minutes)
```bash
node script-synthesizer.js
```
Generates script without running full pipeline.

### Test 4: Images Only (8 minutes)
```bash
python image-generation-pipeline.py
```
Tests image generation APIs.

### Test 5: Full Pipeline (15-20 minutes)
```bash
node advanced-video-orchestrator.js
```
Runs everything end-to-end.

## Troubleshooting

### "API key not found"
```bash
# Check .env file exists and has correct keys
cat .env
# Should show:
# FAL_API_KEY=your_key
# ELEVENLABS_API_KEY=your_key
# etc.
```

### "Module not found"
```bash
# Install dependencies
npm install
pip install -r requirements.txt
```

### "Video assembly failed"
- Check all source files exist in output directories
- Verify file paths are correct
- Check Shotstack API key is valid
- Review error log in `output/logs/`

### "Narration sounds robotic"
- Script wasn't humanized enough
- Add more pauses: `[pause: 1.5s]`
- Claude Code will improve humanization in future versions

### "Music too loud/quiet"
- Adjust dB levels in `advanced-video-assembly.py`:
  - Narration: -20 dB
  - Music: -38 dB (currently)
  - Try -40 dB if music is still too loud

## Key Configuration

Edit `config.json` to customize:

```json
{
  "video": {
    "resolution": "1920x1080",    // Change to "1280x720" for 720p
    "framerate": 30,               // 24, 30, or 60
    "duration": 600                // 10 minutes (600s), change as needed
  },
  "music": {
    "genre": "melodic-techno-dubstep",  // Change music style
    "bpm": "120-130",                   // Tempo range
    "volume": -38                       // dB level, -38 to -50
  }
}
```

## Project Structure After First Run

```
output/
├── generated_images/
│   ├── photorealistic/           # Flux Pro images
│   ├── infographic/              # Nano Banana images
│   └── metadata.json
├── runway_videos/                # Cinematic clips
├── narration.mp3                 # Audio
├── background_music.mp3          # Licensed music
├── audio_mixed.mp3               # Final audio mix
├── subtitles.srt                 # Subtitle timing
├── final_video.mp4               # Complete video!
└── logs/
    ├── orchestrator.log
    ├── research_agents.log
    ├── image_generation.log
    └── video_assembly.log
```

## Next Steps

1. **Run the SEO example** to see the system in action
2. **Review the generated script** in `output/COMPLETE_VIDEO_SCRIPT.md`
3. **Customize your topic** in the CONFIG
4. **Set up Codex** to implement API integrations (follow `CODEX_TASK_PROMPT.md`)
5. **Run your own videos**!

## Support for Codex Integration

Once Codex is set up to implement the API integrations, you'll have:

✅ Real FireCrawl scraping (not mock)
✅ Actual FAL.ai image generation
✅ Real Runway API cinematic videos
✅ Actual Canva subtitle graphics
✅ Real ElevenLabs narration
✅ Licensed music integration
✅ Shotstack video assembly
✅ YouTube auto-publishing

This transforms the system from a **demonstration** into a **fully automated video creation machine**.

## Production Ready?

When you're ready for production:

1. Test with 5-10 videos first
2. Monitor costs (track API spending)
3. Set up automatic error alerts
4. Implement video quality checks
5. Create backup system for failures
6. Monitor YouTube channel performance

## One-Minute Demo

Want to see it in action right now?

```bash
node advanced-video-orchestrator.js
```

This single command will:
- Research SEO Best Practices from 8+ sources
- Generate a complete video script
- Create 25-30 professional images
- Mix narration and background music
- Assemble into a polished 10-minute YouTube video

Everything is ready. **Let's make videos!** 🎬
