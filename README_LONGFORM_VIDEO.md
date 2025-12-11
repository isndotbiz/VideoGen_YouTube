# Enhanced Long-Form Video Assembly

Automated video assembly for long-form content (9-10 minutes) using Shotstack API with intelligent pacing, transitions, and section-based timing.

## Overview

This script creates professional-quality long-form videos by:
- Processing 30+ PNG images with variable display times
- Adding smooth crossfade transitions (2-3 seconds)
- Synchronizing with 9-10 minute narration audio
- Using section-based pacing (intro, body, conclusion)
- Generating 1080p H.264 video at 30fps

## Features

### Intelligent Timing
- **Title Card**: 5 seconds
- **Intro Fast** (Images 1-3): 4 seconds each - Quick setup
- **Intro Slow** (Images 4-5): 9 seconds each - Key points
- **Main Sections** (Images 6-29): 18 seconds each - Standard narration pace
- **Conclusion** (Images 30+): 20 seconds each - Wrap-up and fade

### Smooth Transitions
- Crossfade transitions between all images (2 second overlap)
- Fade in on first image
- Fade out on last image
- Professional visual flow

### Output Specifications
- **Resolution**: 1080p (1920x1080)
- **Frame Rate**: 30fps
- **Codec**: H.264
- **Quality**: High
- **Audio**: Full narration with fade-out

## Prerequisites

### Required Files
```
output/
├── generated_images/
│   ├── flux_001.png
│   ├── flux_002.png
│   └── ... (30+ images)
└── narration.mp3
```

### Environment Variables (.env)
```bash
# Shotstack API
SHOTSTACK_API_KEY=your_shotstack_api_key

# AWS S3 (for signed URLs)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name
AWS_REGION=us-east-1
```

### Python Dependencies
```bash
pip install boto3 requests python-dotenv
```

## Usage

### Step 1: Prepare Assets

1. Generate 30+ images and save to `output/generated_images/`
2. Generate narration audio and save as `output/narration.mp3`
3. Upload assets to S3 (script will reference them via signed URLs)

### Step 2: Run Video Assembly

```bash
python enhanced_video_assembly_longform.py
```

**Output:**
```
============================================================
ENHANCED LONG-FORM VIDEO ASSEMBLY
============================================================

Found 35 images in output/generated_images
Generating signed URLs (24-hour expiry)...
[1/35] flux_001.png - Duration: 5.0s
[2/35] flux_002.png - Duration: 4.0s
...

============================================================
VIDEO ASSEMBLY CONFIGURATION
============================================================
Total Images: 35
Total Duration: 562.0s (9.37 minutes)
Resolution: 1080p (1920x1080)
Frame Rate: 30fps
Codec: H.264
Transition: 2.0s crossfade
============================================================

============================================================
RENDER SUBMISSION
============================================================
Estimated Cost: $1.87
Estimated Render Time: 14 minutes
============================================================

============================================================
SUCCESS: RENDER JOB SUBMITTED
============================================================
Render ID: abc123-def456-ghi789
Status: Queued on Shotstack servers
Duration: 9.37 minutes
Images: 35
============================================================

NEXT STEPS:
1. Monitor progress: https://dashboard.shotstack.io/renders/abc123-def456-ghi789
2. Check status: python check_render_status.py abc123-def456-ghi789
3. Upload to YouTube: python optimized_youtube_uploader.py

Estimated completion: 14 minutes from now
```

### Step 3: Check Render Status

```bash
python check_render_status.py abc123-def456-ghi789
```

**Output:**
```
Render Status: rendering
Progress: 45%
Still rendering... 45% complete
Check back in 1-2 minutes
```

When complete:
```
Render Status: done
Progress: 100%
SUCCESS: Video ready!
Download URL: https://shotstack-output.s3.amazonaws.com/...
Downloading video...
Downloaded: 100.0% (47.3MB)
Video saved to: output/video_final.mp4
```

### Step 4: Upload to YouTube

```bash
python optimized_youtube_uploader.py
```

## Timing Configuration

The script uses section-based timing to match narration pacing:

```python
SECTION_TIMINGS = {
    "title": 5.0,           # Title card
    "intro_fast": 12.0,     # Images 1-3: 4s each
    "intro_slow": 18.0,     # Images 4-5: 9s each
    "section_normal": 18.0, # Most images: 18s each
    "conclusion": 20.0,     # Final images: 20s each
    "transition": 2.0       # Crossfade duration
}
```

### Customizing Timing

Edit `SECTION_TIMINGS` in the script to adjust pacing:

```python
# For faster pacing
SECTION_TIMINGS["section_normal"] = 15.0  # 15 seconds per image

# For slower, detailed explanations
SECTION_TIMINGS["section_normal"] = 22.0  # 22 seconds per image
```

## Section Boundaries

Images are organized into sections with different pacing:

| Section | Images | Duration/Image | Purpose |
|---------|--------|---------------|---------|
| Title | 0 | 5s | Opening card |
| Intro Fast | 1-3 | 4s | Quick setup |
| Intro Slow | 4-5 | 9s | Key concepts |
| Section 2 | 6-11 | 18s | Main content |
| Section 3 | 12-17 | 18s | Main content |
| Section 4 | 18-23 | 18s | Main content |
| Section 5 | 24-29 | 18s | Main content |
| Conclusion | 30+ | 20s | Wrap-up |

## Pricing

**Shotstack costs** (as of Dec 2024):
- $0.20 per minute of rendered video
- 9-10 minute video: ~$1.80-$2.00

**AWS S3 costs** (negligible):
- Signed URL generation: Free
- Storage: ~$0.01 for 100MB of images

## Technical Details

### S3 Signed URLs
- Generated with 24-hour expiration
- No public bucket access required
- Secure temporary access for Shotstack

### Video Codec
```
Format: MP4
Video Codec: H.264
Audio Codec: AAC
Resolution: 1920x1080
Frame Rate: 30fps
Bitrate: Automatic (high quality)
```

### Transition Effect
```
Type: Crossfade
Duration: 2 seconds
Overlap: Images overlap by 2s for smooth transitions
```

## Output Metadata

The script saves render metadata to `output/render_metadata.json`:

```json
{
  "render_id": "abc123-def456-ghi789",
  "total_images": 35,
  "duration_seconds": 562.0,
  "duration_minutes": 9.37,
  "estimated_cost": 1.87,
  "image_metadata": {
    "0": {
      "filename": "flux_001.png",
      "duration": 5.0,
      "s3_key": "video-generation/flux_001.png"
    },
    ...
  }
}
```

## Troubleshooting

### Issue: "Missing AWS credentials"
**Solution**: Check `.env` file has all required AWS variables

### Issue: "Images directory not found"
**Solution**: Ensure images are in `output/generated_images/`

### Issue: "Narration file not found"
**Solution**: Save narration as `output/narration.mp3`

### Issue: "Only X images found. Long-form videos typically need 30+"
**Solution**: Generate more images or adjust script for shorter videos

### Issue: "Render submission failed"
**Solution**:
1. Check Shotstack API key is valid
2. Verify S3 signed URLs are accessible
3. Check Shotstack dashboard for errors

## Example Workflow

```bash
# 1. Prepare environment
cp .env.example .env
# Edit .env with your API keys

# 2. Generate content
python generate_images.py  # Creates 35 images
python generate_narration.py  # Creates narration.mp3

# 3. Upload to S3
python upload_to_s3.py  # Uploads images and audio

# 4. Assemble video
python enhanced_video_assembly_longform.py
# Output: Render ID abc123...

# 5. Wait 10-15 minutes, then check status
python check_render_status.py abc123-def456-ghi789
# Output: video_final.mp4

# 6. Upload to YouTube
python optimized_youtube_uploader.py
```

## Advanced Configuration

### Variable Image Count
The script handles any number of images:
- **10-20 images**: Short-form video (3-5 minutes)
- **20-30 images**: Medium-form video (6-8 minutes)
- **30-50 images**: Long-form video (9-15 minutes)

### Custom Section Timing
Edit `calculate_image_duration()` to customize timing logic:

```python
def calculate_image_duration(image_index: int, total_images: int) -> float:
    # Custom logic for specific image ranges
    if 10 <= image_index <= 15:
        return 25.0  # Extra time for complex diagrams
    return 18.0  # Default
```

## Integration with Existing Pipeline

This script integrates with:
- `upload_to_s3.py` - Asset upload
- `check_render_status.py` - Status monitoring
- `optimized_youtube_uploader.py` - YouTube publishing

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check Shotstack documentation: https://shotstack.io/docs/
2. Review AWS S3 signed URL docs: https://docs.aws.amazon.com/
3. Open an issue in this repository
