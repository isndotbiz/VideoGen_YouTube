# Example Usage: Enhanced Long-Form Video Assembly

## Current Setup (21 Images)

### Available Assets
```
output/generated_images/
├── flux_042.png → flux_062.png (21 total images)
output/
└── narration.mp3 (audio file)
```

### Current Video Configuration
- **Images**: 21
- **Duration**: 5.25 minutes (315 seconds)
- **Estimated Cost**: $1.05
- **Resolution**: 1080p @ 30fps

### Timing Breakdown
```
Image  0: 5.0s  (Title)
Images 1-3: 4.0s each × 3 = 12s (Intro-Fast)
Images 4-5: 9.0s each × 2 = 18s (Intro-Slow)
Images 6-15: 18.0s each × 10 = 180s (Main)
Images 16-20: 20.0s each × 5 = 100s (Conclusion)

Total: 5 + 12 + 18 + 180 + 100 = 315 seconds
```

## Recommended Setup (35 Images)

### Optimal Assets for 9-10 Minute Video
```
output/generated_images/
├── flux_001.png (Title card)
├── flux_002.png (Intro 1)
├── flux_003.png (Intro 2)
├── flux_004.png (Intro 3)
├── flux_005.png (Key point 1)
├── flux_006.png (Key point 2)
├── flux_007-030.png (Main content - 24 images)
├── flux_031-035.png (Conclusion - 5 images)
```

### Target Video Configuration
- **Images**: 35
- **Duration**: 9.45 minutes (567 seconds)
- **Estimated Cost**: $1.89
- **Resolution**: 1080p @ 30fps

### Timing Breakdown
```
Image  0: 5.0s  (Title)
Images 1-3: 4.0s each × 3 = 12s (Intro-Fast)
Images 4-5: 9.0s each × 2 = 18s (Intro-Slow)
Images 6-29: 18.0s each × 24 = 432s (Main)
Images 30-34: 20.0s each × 5 = 100s (Conclusion)

Total: 5 + 12 + 18 + 432 + 100 = 567 seconds
```

## Step-by-Step Example

### 1. Generate Images (Already Done)
```bash
# You already have 21 images
# For optimal results, generate 14 more images to reach 35

ls output/generated_images/*.png | wc -l
# Output: 21

# Need: 35 - 21 = 14 more images
```

### 2. Check Narration Duration
```bash
# Get narration duration
ffprobe -i output/narration.mp3 -show_entries format=duration -v quiet -of csv="p=0"
# Example output: 315.5

# If narration is ~5 minutes, you're good with 21 images
# If narration is ~9 minutes, generate more images to match
```

### 3. Upload Assets to S3
```bash
# Assuming you have upload_to_s3.py
python upload_to_s3.py

# OR manually with AWS CLI
aws s3 cp output/generated_images/ s3://your-bucket/video-generation/ --recursive
aws s3 cp output/narration.mp3 s3://your-bucket/video-generation/
```

### 4. Run Enhanced Video Assembly
```bash
cd D:/workspace/True_Nas/firecrawl-mdjsonl
python enhanced_video_assembly_longform.py
```

**Expected Output:**
```
============================================================
ENHANCED LONG-FORM VIDEO ASSEMBLY
============================================================

Found 21 images in output\generated_images
Generating signed URLs (24-hour expiry)...
[1/21] flux_042.png - Duration: 5.0s
[2/21] flux_043.png - Duration: 4.0s
[3/21] flux_044.png - Duration: 4.0s
[4/21] flux_045.png - Duration: 4.0s
[5/21] flux_046.png - Duration: 9.0s
[6/21] flux_047.png - Duration: 9.0s
[7/21] flux_048.png - Duration: 18.0s
...
[21/21] flux_062.png - Duration: 20.0s

Generated 21 signed URLs

Generating signed URL for narration: narration.mp3
Narration URL generated

============================================================
VIDEO ASSEMBLY CONFIGURATION
============================================================
Total Images: 21
Total Duration: 315.0s (5.25 minutes)
Resolution: 1080p (1920x1080)
Frame Rate: 30fps
Codec: H.264
Transition: 2.0s crossfade
============================================================

Building video clips with variable timing...
Created 21 video clips

============================================================
RENDER SUBMISSION
============================================================
Estimated Cost: $1.05
Estimated Render Time: 8 minutes
============================================================

Submitting render to Shotstack API...

============================================================
SUCCESS: RENDER JOB SUBMITTED
============================================================
Render ID: a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
Status: Queued on Shotstack servers
Duration: 5.25 minutes
Images: 21
============================================================

NEXT STEPS:
1. Monitor progress: https://dashboard.shotstack.io/renders/a1b2c3d4...
2. Check status: python check_render_status.py a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
3. Upload to YouTube: python optimized_youtube_uploader.py

Estimated completion: 8 minutes from now

Metadata saved to: output/render_metadata.json
```

### 5. Monitor Render Progress
```bash
# Wait 8 minutes, then check status
python check_render_status.py a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6
```

**During Rendering:**
```
Render Status: rendering
Progress: 65%
Still rendering... 65% complete
Check back in 1-2 minutes
Monitor at: https://dashboard.shotstack.io/renders/a1b2c3d4...
```

**When Complete:**
```
Render Status: done
Progress: 100%
SUCCESS: Video ready!
Download URL: https://shotstack-output.s3.amazonaws.com/...
Downloading video...
Downloaded: 100.0% (47.3MB)
Video saved to: output\video_final.mp4
File size: 47.3 MB
```

### 6. Verify Video
```bash
# Check video properties
ffprobe -v error -show_entries format=duration,size,bit_rate -show_entries stream=codec_name,width,height,r_frame_rate output/video_final.mp4

# Expected output:
# codec_name=h264
# width=1920
# height=1080
# r_frame_rate=30/1
# duration=315.000000
# size=49614848
# bit_rate=1261209
```

### 7. Upload to YouTube
```bash
python optimized_youtube_uploader.py
```

## Real-World Scenarios

### Scenario 1: Educational Video (30 images, 8 minutes)
```python
# Content: Step-by-step tutorial
# Pacing: Standard (18s per image for main content)

Images:
- 1 title card
- 3 intro images (4s each) - Quick overview
- 2 key concept images (9s each) - Important principles
- 20 main tutorial images (18s each) - Step-by-step
- 4 conclusion images (20s each) - Summary and next steps

Total Duration: 5 + 12 + 18 + 360 + 80 = 475s (7.92 min)
Cost: $1.58
```

### Scenario 2: Documentary-Style (50 images, 14 minutes)
```python
# Content: In-depth exploration
# Pacing: Slower (22s per image for detailed narration)

Modify SECTION_TIMINGS:
SECTION_TIMINGS["section_normal"] = 22.0

Images:
- 1 title card (5s)
- 3 intro images (4s each = 12s)
- 2 key images (12s each = 24s)
- 40 main images (22s each = 880s)
- 4 conclusion images (25s each = 100s)

Total Duration: 5 + 12 + 24 + 880 + 100 = 1021s (17 min)
Cost: $3.40
```

### Scenario 3: Quick Explainer (15 images, 3 minutes)
```python
# Content: Fast-paced overview
# Pacing: Faster (12s per image)

Modify SECTION_TIMINGS:
SECTION_TIMINGS["section_normal"] = 12.0

Images:
- 1 title card (4s)
- 2 intro images (3s each = 6s)
- 10 main images (12s each = 120s)
- 2 conclusion images (15s each = 30s)

Total Duration: 4 + 6 + 120 + 30 = 160s (2.67 min)
Cost: $0.53
```

## Customization Examples

### Example 1: Adjust Timing for Specific Images
```python
# Edit calculate_image_duration() in enhanced_video_assembly_longform.py

def calculate_image_duration(image_index: int, total_images: int) -> float:
    """Calculate duration for each image based on section"""

    # Title card
    if image_index == 0:
        return SECTION_TIMINGS["title"]

    # Special case: Images 10-15 need extra time (complex diagrams)
    if 10 <= image_index <= 15:
        return 25.0  # Extra time for detailed explanation

    # Intro - fast section (images 1-3)
    if 1 <= image_index <= 3:
        return SECTION_TIMINGS["intro_fast"] / 3

    # ... rest of logic
```

### Example 2: Different Transition Effects
```python
# Edit build_video_clips() in enhanced_video_assembly_longform.py

# For dramatic section breaks, use wipe transitions
if image_index in [6, 12, 18, 24]:  # Section boundaries
    transition = {
        "in": "wipeRight",
        "out": "fade"
    }
else:
    transition = {
        "in": "fade",
        "out": "fade"
    }
```

### Example 3: Custom Section Boundaries
```python
# For a different content structure:

SECTION_BOUNDARIES = {
    "title": (0, 1),        # Image 0
    "overview": (1, 5),     # Images 1-4 (quick overview)
    "problem": (5, 10),     # Images 5-9 (problem definition)
    "solution": (10, 25),   # Images 10-24 (solution details)
    "results": (25, 30),    # Images 25-29 (results)
    "conclusion": (30, None) # Images 30+
}
```

## Troubleshooting Examples

### Issue: Video Too Short
```bash
# Current: 21 images = 5.25 minutes
# Target: 9-10 minutes

# Solution 1: Generate more images
# Need: ~35 images for 9-10 minutes

# Solution 2: Increase timing per image
# Edit enhanced_video_assembly_longform.py:
SECTION_TIMINGS["section_normal"] = 25.0  # Instead of 18.0
```

### Issue: Audio/Video Mismatch
```bash
# Problem: Narration is 9 minutes, video is 5 minutes

# Solution: Match image count to narration duration
python -c "
narration_duration = 540  # 9 minutes in seconds
avg_duration_per_image = 18  # seconds
needed_images = narration_duration / avg_duration_per_image
print(f'Need {int(needed_images)} images for {narration_duration/60:.1f} min narration')
"
# Output: Need 30 images for 9.0 min narration
```

### Issue: Render Failed
```bash
# Check error in Shotstack dashboard
# Common causes:
# 1. Invalid S3 URLs (expired after 24 hours)
# 2. Missing audio file
# 3. Invalid transition names

# Solution: Re-run with fresh signed URLs
python enhanced_video_assembly_longform.py
```

## Performance Benchmarks

### Render Time vs Video Duration
```
Video Duration | Render Time | Cost
---------------|-------------|------
3 minutes      | 4-5 min     | $0.60
5 minutes      | 7-8 min     | $1.00
7 minutes      | 10-11 min   | $1.40
9 minutes      | 13-14 min   | $1.80
12 minutes     | 18-20 min   | $2.40
15 minutes     | 22-25 min   | $3.00
```

### File Size Estimates
```
Resolution | Duration | File Size
-----------|----------|----------
1080p      | 5 min    | ~45 MB
1080p      | 9 min    | ~80 MB
1080p      | 12 min   | ~110 MB
1080p      | 15 min   | ~135 MB
```

## Integration with Existing Scripts

### Full Pipeline
```bash
# 1. Generate content
python generate_images.py --count 35
python generate_narration.py --duration 9

# 2. Upload to S3
python upload_to_s3.py --directory output/generated_images
python upload_to_s3.py --file output/narration.mp3

# 3. Assemble video
python enhanced_video_assembly_longform.py
# Save the render ID from output

# 4. Wait for render
sleep 600  # Wait 10 minutes

# 5. Check and download
python check_render_status.py <render_id>

# 6. Upload to YouTube
python optimized_youtube_uploader.py --file output/video_final.mp4 --title "My Video" --description "..."
```

## Summary

The enhanced long-form video assembly script provides:

1. **Flexible Timing**: Adapts to any number of images (10-50+)
2. **Section-Based Pacing**: Different speeds for intro/main/conclusion
3. **Smooth Transitions**: Professional fade effects between images
4. **Cost Effective**: ~$0.20 per minute of rendered video
5. **High Quality**: 1080p H.264 at 30fps
6. **Easy Integration**: Works with existing S3 and YouTube upload scripts

For questions or issues, refer to:
- Full documentation: `README_LONGFORM_VIDEO.md`
- Quick reference: `QUICK_START_LONGFORM_VIDEO.md`
- Visual workflow: `LONGFORM_VIDEO_WORKFLOW.md`
