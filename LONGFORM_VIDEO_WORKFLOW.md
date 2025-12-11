# Long-Form Video Assembly Workflow

## Visual Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT PREPARATION                              │
├─────────────────────────────────────────────────────────────────┤
│  1. Generate Images (30+ PNG files)                              │
│     output/generated_images/flux_001.png ... flux_035.png        │
│                                                                   │
│  2. Generate Narration (9-10 min MP3)                            │
│     output/narration.mp3                                         │
│                                                                   │
│  3. Upload to S3                                                 │
│     s3://bucket/video-generation/*.png                           │
│     s3://bucket/video-generation/narration.mp3                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│            ENHANCED VIDEO ASSEMBLY (Main Script)                 │
├─────────────────────────────────────────────────────────────────┤
│  Step 1: Generate S3 Signed URLs (24hr expiry)                  │
│    • Scan output/generated_images/ for PNG files                │
│    • Create signed URL for each image                           │
│    • Create signed URL for narration.mp3                        │
│                                                                  │
│  Step 2: Calculate Dynamic Timing                               │
│    • Image 0 (Title):        5s                                 │
│    • Images 1-3 (Intro):     4s each (fast pacing)             │
│    • Images 4-5 (Key):       9s each (emphasis)                │
│    • Images 6-29 (Main):     18s each (standard)               │
│    • Images 30+ (Outro):     20s each (conclusion)             │
│                                                                  │
│  Step 3: Build Shotstack Timeline                               │
│    • Create video track with image clips                        │
│    • Add fade transitions (in/out)                              │
│    • Overlap clips by 2s for smooth transitions                │
│    • Add audio track with narration                             │
│                                                                  │
│  Step 4: Submit to Shotstack API                                │
│    • Resolution: 1080p (1920x1080)                              │
│    • Frame Rate: 30fps                                          │
│    • Codec: H.264 (high quality)                                │
│    • Format: MP4                                                │
│                                                                  │
│  OUTPUT: Render ID (abc123-def456-ghi789)                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    SHOTSTACK RENDERING                           │
├─────────────────────────────────────────────────────────────────┤
│  Status: Queued → Processing → Rendering → Done                 │
│  Duration: ~10-15 minutes (1.5x video length)                   │
│  Monitor: https://dashboard.shotstack.io/renders/{id}           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CHECK RENDER STATUS                            │
├─────────────────────────────────────────────────────────────────┤
│  python check_render_status.py {render_id}                      │
│                                                                  │
│  • Query Shotstack API for status                               │
│  • Display progress percentage                                  │
│  • When done: Download video                                    │
│                                                                  │
│  OUTPUT: output/video_final.mp4                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    YOUTUBE UPLOAD                                │
├─────────────────────────────────────────────────────────────────┤
│  python optimized_youtube_uploader.py                            │
│                                                                  │
│  OUTPUT: Published YouTube video                                │
└─────────────────────────────────────────────────────────────────┘
```

## Timing Strategy

### Section-Based Pacing

```
Video Timeline (35 images, 9.45 minutes total):

0:00 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 9:27

┌──────┬─────────────┬──────────┬──────────────────────┬────────────┐
│Title │   Intro     │   Key    │    Main Content      │  Conclusion│
│ 5s   │  3×4s=12s   │ 2×9s=18s │   24×18s = 432s     │  5×20s=100s│
└──────┴─────────────┴──────────┴──────────────────────┴────────────┘
  1 img    3 imgs      2 imgs          24 imgs            5 imgs

Total: 5 + 12 + 18 + 432 + 100 = 567 seconds (9.45 minutes)
```

### Transition Overlap

```
Image 1     Image 2     Image 3
├───────┤   ├───────┤   ├───────┤
│  18s  │   │  18s  │   │  18s  │
│       ├───┤       ├───┤       │
│       │ 2s│       │ 2s│       │
│       │out│       │out│       │
└───────┴───┴───────┴───┴───────┘
         └in┘        └in┘

Actual timeline:
0s      16s     34s     52s
├───────┤├──────┤├──────┤
  Img1    Img2    Img3
```

## File Structure

```
firecrawl-mdjsonl/
│
├── enhanced_video_assembly_longform.py  (Main script - 13KB)
│   ├── generate_signed_urls()           → S3 signed URLs (24hr)
│   ├── calculate_image_duration()       → Variable timing logic
│   ├── build_video_clips()              → Shotstack timeline
│   └── assemble_longform_video()        → API submission
│
├── check_render_status.py               (Status checker)
│   └── check_render_status(render_id)   → Download completed video
│
├── README_LONGFORM_VIDEO.md             (Full documentation - 8.4KB)
│   ├── Features
│   ├── Prerequisites
│   ├── Usage examples
│   ├── Timing configuration
│   ├── Troubleshooting
│   └── Advanced configuration
│
├── QUICK_START_LONGFORM_VIDEO.md        (Quick reference - 4.6KB)
│   ├── 5-minute setup
│   ├── Command reference
│   ├── Common issues
│   └── Cost calculator
│
└── output/
    ├── generated_images/                 (Input: 30+ PNG files)
    │   ├── flux_001.png - flux_035.png
    │   └── ...
    ├── narration.mp3                     (Input: 9-10 min audio)
    ├── render_metadata.json              (Output: Render details)
    └── video_final.mp4                   (Output: Final video)
```

## Configuration Variables

### SECTION_TIMINGS
```python
{
    "title": 5.0,           # Opening card duration
    "intro_fast": 12.0,     # Total for images 1-3 (4s each)
    "intro_slow": 18.0,     # Total for images 4-5 (9s each)
    "section_normal": 18.0, # Standard image duration
    "conclusion": 20.0,     # Final images duration
    "transition": 2.0       # Fade overlap between images
}
```

### SECTION_BOUNDARIES
```python
{
    "title": (0, 1),        # Image 0
    "intro_fast": (1, 4),   # Images 1-3
    "intro_slow": (4, 6),   # Images 4-5
    "section_2": (6, 12),   # Images 6-11
    "section_3": (12, 18),  # Images 12-17
    "section_4": (18, 24),  # Images 18-23
    "section_5": (24, 30),  # Images 24-29
    "conclusion": (30, None)# Images 30+
}
```

## API Integration

### S3 Signed URLs (24-hour expiry)
```python
s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket, 'Key': s3_key},
    ExpiresIn=86400  # 24 hours
)
```

### Shotstack Render Request
```json
{
  "timeline": {
    "soundtrack": {
      "src": "https://s3.amazonaws.com/...narration.mp3?sig=...",
      "effect": "fadeOut",
      "volume": 1.0
    },
    "tracks": [{
      "clips": [
        {
          "asset": {"type": "image", "src": "https://s3...?sig=..."},
          "start": 0,
          "length": 5.0,
          "fit": "cover",
          "transition": {"in": "fade", "out": "fade"}
        },
        ...
      ]
    }]
  },
  "output": {
    "format": "mp4",
    "resolution": "1080",
    "fps": 30,
    "quality": "high"
  }
}
```

## Cost Analysis

### Shotstack Pricing
```
Base rate: $0.20 per minute of rendered video

Examples:
- 21 images (5.25 min):  $1.05
- 30 images (7.95 min):  $1.59
- 35 images (9.45 min):  $1.89  ← Recommended
- 50 images (13.95 min): $2.79
```

### AWS S3 Costs
```
Signed URL generation: $0.00 (free)
Storage (100MB images): ~$0.01/month
Data transfer: Included in Shotstack API
```

## Performance Metrics

| Metric | Value |
|--------|-------|
| Images processed | 30-35 (recommended) |
| Video duration | 9-10 minutes |
| Render time | 14-16 minutes (1.5x) |
| Output size | 45-55 MB |
| Resolution | 1920x1080 |
| Frame rate | 30fps |
| Codec | H.264 |
| Audio | AAC, 192kbps |

## Error Handling

The script handles:
- Missing AWS credentials → Clear error message
- Missing images directory → Path validation
- Missing narration file → File existence check
- S3 upload failures → Boto3 exception handling
- Shotstack API errors → HTTP status validation
- Invalid transitions → Shotstack-compatible values only

## Monitoring

### During Submission
```bash
python enhanced_video_assembly_longform.py

# Real-time output:
# - Image count and durations
# - Total video duration
# - Estimated cost
# - Render ID
```

### During Rendering
```bash
python check_render_status.py {render_id}

# Every 1-2 minutes:
# - Status: queued/processing/rendering/done
# - Progress percentage
# - ETA
```

### Shotstack Dashboard
```
https://dashboard.shotstack.io/renders/{render_id}

Features:
- Visual progress bar
- Detailed logs
- Preview thumbnail
- Error diagnostics
```

## Example Output

### Successful Submission
```
============================================================
ENHANCED LONG-FORM VIDEO ASSEMBLY
============================================================

Found 35 images in output/generated_images
Generating signed URLs (24-hour expiry)...
[1/35] flux_001.png - Duration: 5.0s
[2/35] flux_002.png - Duration: 4.0s
...
[35/35] flux_035.png - Duration: 20.0s

Generated 35 signed URLs

Generating signed URL for narration: narration.mp3
Narration URL generated

============================================================
VIDEO ASSEMBLY CONFIGURATION
============================================================
Total Images: 35
Total Duration: 567.0s (9.45 minutes)
Resolution: 1080p (1920x1080)
Frame Rate: 30fps
Codec: H.264
Transition: 2.0s crossfade
============================================================

Building video clips with variable timing...
Created 35 video clips

============================================================
RENDER SUBMISSION
============================================================
Estimated Cost: $1.89
Estimated Render Time: 14 minutes
============================================================

Submitting render to Shotstack API...

============================================================
SUCCESS: RENDER JOB SUBMITTED
============================================================
Render ID: d87db2b1-c823-440d-98c5-9deb57cabdf5
Status: Queued on Shotstack servers
Duration: 9.45 minutes
Images: 35
============================================================

NEXT STEPS:
1. Monitor progress: https://dashboard.shotstack.io/renders/d87db2b1...
2. Check status: python check_render_status.py d87db2b1...
3. Upload to YouTube: python optimized_youtube_uploader.py

Estimated completion: 14 minutes from now

Metadata saved to: output/render_metadata.json
```

## Next Steps

1. **Generate more images**: Create 30+ PNG files
2. **Record narration**: 9-10 minute audio file
3. **Upload to S3**: Use existing upload scripts
4. **Run assembly**: `python enhanced_video_assembly_longform.py`
5. **Monitor render**: Check Shotstack dashboard
6. **Download video**: `python check_render_status.py {id}`
7. **Publish**: Upload to YouTube or other platforms
