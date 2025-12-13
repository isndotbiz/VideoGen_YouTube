# Descript API Integration Guide

## Overview

This guide explains how to use the Descript API for professional video assembly with auto-captions, speaker detection, and effects.

## Current Status

✅ **Descript API Key**: Already configured in `.env`
- Key: `DESCRIPT_API_KEY` (JWT token, valid through 2157)
- Status: Ready to use

## What You Get with Descript

### Automatic Features
- ✅ **Auto-Captions** - Generates captions from narration (English support)
- ✅ **Speaker Detection** - Identifies different speakers
- ✅ **Background Noise Removal** - Cleans up audio
- ✅ **Transcription** - Full text transcript of video
- ✅ **Caption Styling** - Professional animated captions (white-pop style)

### Manual Features
- Subtitle customization
- Music/background sound ducking
- Ken Burns effects (zoom/pan on static images)
- Color grading
- Transitions

## Usage

### Option 1: Use Descript Assembly (Recommended for Quality)

```bash
# Full pipeline with Descript
node pipeline-complete.js "https://your-article.com" --use-descript
```

This will:
1. Generate script from article
2. Create images (Flux Pro + Nano Banana)
3. Generate narration (ElevenLabs)
4. Queue videos (Runway)
5. **Upload to Descript for assembly**
6. Auto-generate captions
7. Export with captions and effects

### Option 2: Just Test Descript

```bash
# Test Descript API connection
node descript-video-editor.js --test

# Run full Descript workflow with existing narration
node descript-video-editor.js --workflow s3://bucket/narration.mp3 MyProject
```

### Option 3: Use FFmpeg (Default - Keep Costs Low)

```bash
# Use FFmpeg instead (free)
node pipeline-complete.js "https://your-article.com"
```

## How Descript Integration Works

### Phase 7B: Descript Assembly

The pipeline executes this workflow:

```
1. CREATE PROJECT
   ↓ Calls: POST /v1/projects
   ↓ Creates: New Descript project

2. IMPORT MEDIA (Optional)
   ↓ Calls: POST /v1/edit_in_descript/schema
   ↓ Creates: Import URL (3-hour link to edit in Descript UI)

3. AUTO-TRANSCRIPTION
   ↓ Descript automatically transcribes narration
   ↓ Result: Full transcript available

4. AUTO-CAPTIONS
   ↓ Descript generates SRT captions from transcript
   ↓ Style: White pop-in animation
   ↓ Result: Professional subtitles

5. EXPORT VIDEO
   ↓ Calls: POST /v1/projects/{id}/export
   ↓ Creates: MP4 with captions, effects applied
   ↓ Result: Download URL available in Descript dashboard

6. RETRIEVE TRANSCRIPT
   ↓ Calls: GET /v1/projects/{id}/transcript
   ↓ Result: Full transcript + caption data
```

## Costs

### Descript Pricing (as of Dec 2024)

| Feature | Cost |
|---------|------|
| Video Export | ~$10-20 per video |
| Auto-Captions | Included |
| Background Removal | +$5/video |
| Speaker Detection | Included |
| Transcription | Included |

**Estimated cost per video with full Descript assembly: ~$15**

For comparison:
- FFmpeg assembly: $0
- Descript assembly: ~$15
- Total pipeline cost (Descript): ~$16/video

## File Structure

### Files Updated

**descript-video-editor.js** (Enhanced)
- `importMediaToDescript()` - Create edit-in-Descript link
- `createProjectWithCaptions()` - Create project + enable auto-captions (NOW with real API calls)
- `exportFinalVideo()` - Export video with captions (NOW with real API calls)
- `getTranscriptAndCaptions()` - Retrieve transcript & captions (NOW with real API calls)
- `humanizeNarration()` - Analyze narration quality
- `fullWorkflow()` - Complete pipeline orchestration

**pipeline-complete.js** (Enhanced)
- `phase7Assemble(useDescript)` - Choose assembly method
- `phase7AssembleFFmpeg()` - FFmpeg route (free)
- `phase7AssembleDescript()` - Descript route (paid)
- Added `--use-descript` flag support

### API Endpoints Used

```javascript
// Projects
POST   /v1/projects                           // Create project
GET    /v1/projects/{id}                      // Get project status
DELETE /v1/projects/{id}                      // Delete project

// Media
POST   /v1/edit_in_descript/schema            // Create edit link
POST   /v1/projects/{id}/media                // Upload media

// Export
POST   /v1/projects/{id}/export               // Export video

// Transcription
GET    /v1/projects/{id}/transcript           // Get transcript
GET    /v1/projects/{id}/captions             // Get captions
```

## Troubleshooting

### Error: "DESCRIPT_API_KEY not found"
- **Solution**: Check `.env` file has DESCRIPT_API_KEY set
- **Current value**: Already in .env (checked ✓)

### Error: "Failed to create project"
- **Possible causes**:
  - API key expired (check expiration time)
  - Descript account issue
  - Network connectivity
- **Solution**: Run `node descript-video-editor.js --test`

### Error: "Export failed"
- **Possible causes**:
  - Project not fully processed
  - Audio/video format issue
  - API call error
- **Workaround**: Download from Descript dashboard manually
- **Solution**: Check logs in `./logs/pipeline-*.log`

### Video exported but no captions
- **Cause**: Auto-transcription may still be processing
- **Solution**: Wait 2-5 minutes, re-export from Descript dashboard
- **Workaround**: Use FFmpeg instead for immediate results

## Next Steps

1. **Decide on assembly method**:
   - Use FFmpeg for: Budget builds, batch processing, fast turnaround
   - Use Descript for: Professional videos, client work, captions needed

2. **If using Descript**:
   ```bash
   node pipeline-complete.js "https://example.com" --use-descript
   ```

3. **Monitor the video**:
   - Descript will process in background
   - Check `logs/pipeline-*.log` for project ID
   - Visit https://app.descript.com to download final video

4. **Download final video**:
   - Descript dashboard: https://app.descript.com
   - Look for project: `VideoGen_YYYYMMDD`
   - Download MP4 with captions

## Advanced: Custom Caption Styling

To customize captions, edit `descript-video-editor.js` line 134-145:

```javascript
const brandingConfig = {
  subtitles: {
    style: 'white-pop',           // Change style
    font: 'Bold Sans-Serif',       // Change font
    size: '48px',                  // Change size
    text_color: '#FFFFFF',         // Change color
    border_color: '#FF1493',       // Accent color
    border_width: '3px',
    background: 'rgba(0,0,0,0.3)',
    animation: 'pop-in-out',       // Animation
    animation_duration: '0.3s',
  }
};
```

Supported styles:
- `white-pop` - White text with pop-in
- `black-outline` - Black outline style
- `gradient` - Gradient background
- `minimal` - Minimal design

## Support

For Descript API issues:
- Official docs: https://www.descript.com/api
- Check logs: `tail -f logs/pipeline-*.log`
- Debug mode: Set `DEBUG=true` in .env

---

**Summary**: You now have both FFmpeg (free) and Descript (paid) options for video assembly. Choose FFmpeg for budget/batch work, choose Descript for professional quality with auto-captions.
