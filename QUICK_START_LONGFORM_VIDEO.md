# Quick Start: Long-Form Video Assembly

Generate 9-10 minute professional videos from 30+ images with synchronized narration.

## Prerequisites

```bash
# 1. Install dependencies
pip install boto3 requests python-dotenv

# 2. Set up .env file
cat > .env << EOF
SHOTSTACK_API_KEY=your_shotstack_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name
AWS_REGION=us-east-1
EOF
```

## File Structure

```
firecrawl-mdjsonl/
├── output/
│   ├── generated_images/
│   │   ├── flux_001.png  (Title card)
│   │   ├── flux_002.png  (Intro - fast)
│   │   ├── flux_003.png  (Intro - fast)
│   │   ├── flux_004.png  (Intro - fast)
│   │   ├── flux_005.png  (Key point)
│   │   ├── flux_006.png  (Key point)
│   │   ├── flux_007.png  (Section 2)
│   │   └── ... (30+ total images)
│   └── narration.mp3     (9-10 minute audio)
└── enhanced_video_assembly_longform.py
```

## Quick Command

```bash
# Run the entire pipeline
python enhanced_video_assembly_longform.py

# Output:
# Render ID: abc123-def456-ghi789
# Estimated time: 14 minutes
# Estimated cost: $1.87
```

## Timing Breakdown

| Image Range | Duration/Image | Section |
|-------------|---------------|---------|
| 1 (Title) | 5s | Opening |
| 2-4 | 4s each | Fast intro |
| 5-6 | 9s each | Key concepts |
| 7-29 | 18s each | Main content |
| 30+ | 20s each | Conclusion |

**Total**: ~9-10 minutes with 30-35 images

## Check Status

```bash
# After 10-15 minutes
python check_render_status.py abc123-def456-ghi789

# When done, output saved to:
# output/video_final.mp4
```

## Upload to YouTube

```bash
python optimized_youtube_uploader.py
```

## Common Issues

**Issue**: "Only 21 images found"
```bash
# Generate more images or edit timing in script:
SECTION_TIMINGS["section_normal"] = 25.0  # Longer per image
```

**Issue**: "Missing AWS credentials"
```bash
# Check .env file exists and has all required variables
cat .env
```

**Issue**: "Narration file not found"
```bash
# Ensure narration.mp3 exists in output/
ls -lh output/narration.mp3
```

## Cost Calculator

```python
# Formula: $0.20 per minute
images = 35
duration_per_image = 18  # average
total_minutes = (images * duration_per_image) / 60
cost = total_minutes * 0.20

print(f"Cost: ${cost:.2f}")
# Output: Cost: $2.10
```

## Custom Timing

Edit `SECTION_TIMINGS` in script:

```python
# For faster pacing (7-8 minutes)
SECTION_TIMINGS = {
    "title": 4.0,
    "intro_fast": 9.0,
    "intro_slow": 12.0,
    "section_normal": 14.0,
    "conclusion": 16.0,
    "transition": 2.0
}

# For slower, detailed (12-15 minutes)
SECTION_TIMINGS = {
    "title": 6.0,
    "intro_fast": 15.0,
    "intro_slow": 22.0,
    "section_normal": 22.0,
    "conclusion": 25.0,
    "transition": 2.5
}
```

## Pipeline Integration

```bash
# Full workflow
python generate_images.py       # Step 1: Create images
python generate_narration.py    # Step 2: Create audio
python upload_to_s3.py          # Step 3: Upload assets
python enhanced_video_assembly_longform.py  # Step 4: Render video
# Wait 10-15 minutes...
python check_render_status.py <render_id>   # Step 5: Download
python optimized_youtube_uploader.py        # Step 6: Publish
```

## Output Metadata

After submission, check `output/render_metadata.json`:

```json
{
  "render_id": "abc123...",
  "total_images": 35,
  "duration_seconds": 562,
  "duration_minutes": 9.37,
  "estimated_cost": 1.87,
  "image_metadata": {
    "0": {"filename": "flux_001.png", "duration": 5.0},
    ...
  }
}
```

## Troubleshooting

1. **Script fails immediately**
   - Check Python version: `python --version` (needs 3.7+)
   - Install dependencies: `pip install -r requirements.txt`

2. **AWS S3 errors**
   - Verify AWS credentials: `aws s3 ls`
   - Check bucket exists and has correct permissions

3. **Shotstack API errors**
   - Verify API key: https://dashboard.shotstack.io/
   - Check account has credits
   - Review error message for specific issues

4. **Video too short/long**
   - Adjust `SECTION_TIMINGS` values
   - Add/remove images
   - Change section boundaries in `SECTION_BOUNDARIES`

## Advanced: Variable Image Count

The script automatically adapts:

```python
# 15 images → 4 min video
# 21 images → 5.25 min video (current example)
# 35 images → 9.37 min video (recommended)
# 50 images → 14 min video (long-form)
```

## Support

- Shotstack Docs: https://shotstack.io/docs/
- AWS S3 Signed URLs: https://docs.aws.amazon.com/AmazonS3/
- GitHub Issues: Create issue with error logs
