# Quick Start: Image Generation with Enhanced FAL Generator

Get started generating high-quality images in 5 minutes.

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] FAL.ai account created
- [ ] FAL.ai API key obtained
- [ ] `.env` file configured

## Step 1: Install Dependencies (1 minute)

```bash
# Install required packages
pip install fal-client python-dotenv requests tqdm

# Verify installation
python -c "import fal_client; print('✓ FAL client installed')"
```

## Step 2: Configure Environment (1 minute)

1. Get your FAL.ai API key from https://fal.ai/dashboard/keys

2. Ensure your `.env` file has:
   ```
   FAL_API_KEY=your_actual_api_key_here
   ```

3. Verify configuration:
   ```bash
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✓ API key loaded' if os.getenv('FAL_API_KEY') else '✗ API key missing')"
   ```

## Step 3: Prepare Your Prompts (2 minutes)

### Option A: Use Sample File
The `sample_image_prompts.json` is ready to use with 32 example prompts.

```bash
# Test with sample prompts (dry run first)
python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json --dry-run
```

### Option B: Create Custom File
Create `my_prompts.json`:
```json
{
  "prompts": [
    {
      "section": "Test",
      "image_number": 1,
      "image_prompt": "A beautiful sunset over mountains, photorealistic, 8k resolution",
      "description": "Mountain Sunset"
    },
    {
      "section": "Test",
      "image_number": 2,
      "image_prompt": "A futuristic cityscape at night with neon lights, cyberpunk aesthetic",
      "description": "Cyberpunk City"
    }
  ]
}
```

## Step 4: Generate Images (1 minute setup)

### Dry Run First (Recommended)
```bash
# Preview what will be generated
python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json --dry-run
```

Output:
```
=== DRY RUN MODE ===
Would generate 32 images:
  1. Introduction_001_Developer_Workspace_Overview.png
  2. Introduction_002_AI_Automation_Concept.png
  ...
Estimated cost: $0.96 USD
```

### Generate Images
```bash
# Generate with default settings (4 parallel workers)
python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json
```

You'll see:
```
Enhanced FAL Batch Generator initialized:
  Output directory: ./output/generated_images
  Max workers: 4
  Max retries: 3
  Timeout: 120s

Ready to generate 32 images
Estimated cost: $0.96 USD
Parallel workers: 4

Generating images: 100%|████████████████| 32/32 [06:24<00:00, 12.0s/image]
```

## Step 5: View Results

```bash
# Navigate to output directory
cd output/generated_images

# List generated images
ls -lh *.png

# View metadata
cat batch_metadata.json | python -m json.tool
```

## Common Commands

### Small Test Batch
```bash
# Create a test file with 3 prompts
echo '{
  "prompts": [
    {
      "section": "test",
      "image_number": 1,
      "image_prompt": "A serene lake at sunset",
      "description": "Lake Sunset"
    },
    {
      "section": "test",
      "image_number": 2,
      "image_prompt": "A modern tech office",
      "description": "Tech Office"
    },
    {
      "section": "test",
      "image_number": 3,
      "image_prompt": "A futuristic robot",
      "description": "Robot"
    }
  ]
}' > test_prompts.json

# Generate test batch
python enhanced_fal_batch_generator.py --prompts test_prompts.json
```

### Generate with More Workers
```bash
# Faster generation (if you have good network)
python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json --workers 6
```

### Generate with Custom Output
```bash
# Save to specific directory
python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json --output ./my_images
```

### Resume Failed Generation
```bash
# Just run again - automatically skips existing files
python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json
```

## Monitoring Progress

### Real-time Console
The script shows a live progress bar:
```
Generating images: 45%|████████▌         | 14/32 [02:54<03:30, 11.7s/image]
```

### Log File
Monitor the detailed log:
```bash
# In another terminal
tail -f batch_generation.log
```

### Check Generated Files
```bash
# Count generated images
ls output/generated_images/*.png | wc -l

# Check total size
du -sh output/generated_images/
```

## Understanding Output

### File Naming Convention
```
{Section}_{ImageNumber}_{Description}.png

Examples:
  Introduction_001_Developer_Workspace_Overview.png
  Cloud_Infrastructure_004_Cloud_Data_Center.png
  Security_010_Cybersecurity_Shield.png
```

### Metadata Files
Each image has a corresponding metadata file:
```bash
# View metadata for a specific image
cat output/generated_images/metadata/Introduction_001_Developer_Workspace_Overview.png.json
```

Contains:
- Original prompt
- Generation time
- Success/failure status
- Retry count
- Timestamp

### Batch Summary
```bash
# View complete batch summary
cat output/generated_images/batch_metadata.json | python -m json.tool
```

Shows:
- Total images generated
- Success/failure counts
- Average generation time
- List of all images with metadata

## Troubleshooting Quick Fixes

### API Key Error
```
ValueError: FAL_API_KEY not found
```
**Fix:** Check your `.env` file exists and has `FAL_API_KEY=...`

### Import Error
```
ModuleNotFoundError: No module named 'fal_client'
```
**Fix:** `pip install fal-client`

### Connection Timeout
```
Error: timeout
```
**Fix:** Increase timeout: `--timeout 300`

### Too Many Failures
**Fix:** Reduce workers: `--workers 2`

## Next Steps

### Optimize for Your Needs

**For Higher Quality:**
Edit line ~289 in `enhanced_fal_batch_generator.py`:
```python
"num_inference_steps": 75,  # Increase from 50
"guidance_scale": 9.0,      # Increase from 7.5
```

**For Faster Generation:**
```python
"num_inference_steps": 30,  # Decrease from 50
"guidance_scale": 5.0,      # Decrease from 7.5
```

### Create Better Prompts

Good prompts include:
- Subject/scene description
- Style (photorealistic, illustration, 3D, etc.)
- Lighting/atmosphere
- Camera angle/perspective
- Quality keywords (8k, high detail, sharp)

Example:
```
"A professional data center with server racks, blue LED lighting,
wide angle shot, modern architecture, high detail, 8k resolution,
cinematic composition"
```

### Batch Processing Workflow

1. **Small test** (3-5 images)
2. **Review quality**
3. **Adjust settings** if needed
4. **Full batch** generation
5. **Backup** to permanent storage

## Cost Management

### Estimate Before Running
```bash
# Dry run shows cost
python enhanced_fal_batch_generator.py --prompts my_prompts.json --dry-run
```

### FAL.ai Pricing (as of 2024)
- Flux Dev: ~$0.03 per image
- 1920x1080 resolution
- No additional charges for retries

### Monthly Budget Planning
- 100 images: ~$3.00
- 500 images: ~$15.00
- 1000 images: ~$30.00

## Performance Expectations

### Generation Times (4 workers)
- **10 images**: ~2-3 minutes
- **30 images**: ~6-8 minutes
- **50 images**: ~10-13 minutes
- **100 images**: ~20-25 minutes

### System Requirements
- **CPU**: Any modern processor
- **RAM**: 512MB minimum, 1GB recommended
- **Network**: Stable broadband (2+ Mbps)
- **Storage**: ~2-3 MB per image

## Getting Help

### Check Logs
```bash
# View recent errors
grep ERROR batch_generation.log | tail -20

# View generation summary
grep "STATISTICS" batch_generation.log -A 20
```

### Verify Setup
```bash
# Run system check
python -c "
from dotenv import load_dotenv
import os
load_dotenv()

checks = [
    ('FAL API Key', bool(os.getenv('FAL_API_KEY'))),
    ('Output Dir', os.path.exists('output/generated_images')),
]

for name, status in checks:
    print(f'{'✓' if status else '✗'} {name}')
"
```

### Common Questions

**Q: Can I pause and resume?**
A: Yes! Just run the script again - it skips existing files.

**Q: How do I generate only failed images?**
A: Delete the successful images or check batch_metadata.json for failed ones.

**Q: Can I change the resolution?**
A: Yes, edit line ~289 in the script to change width/height.

**Q: What if I run out of API credits?**
A: The script will fail gracefully and save metadata for successful images.

## Success Checklist

After your first batch, you should have:

- [ ] Generated PNG files in `output/generated_images/`
- [ ] Individual metadata JSON files in `output/generated_images/metadata/`
- [ ] Batch summary in `output/generated_images/batch_metadata.json`
- [ ] Log file `batch_generation.log`
- [ ] Statistics showing success rate
- [ ] Cost estimate confirmed

## Example Complete Workflow

```bash
# 1. Prepare (one-time setup)
pip install fal-client python-dotenv requests tqdm
echo "FAL_API_KEY=your_key" >> .env

# 2. Test with small batch
python enhanced_fal_batch_generator.py --prompts test_prompts.json --dry-run
python enhanced_fal_batch_generator.py --prompts test_prompts.json

# 3. Review and adjust
ls -lh output/generated_images/
cat output/generated_images/batch_metadata.json

# 4. Run full batch
python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json

# 5. Backup results
cp -r output/generated_images/ ~/backups/images_$(date +%Y%m%d)/

# 6. Clean up
rm test_prompts.json
```

## You're Ready!

You now have a production-ready image generation pipeline. Start with a small test batch and scale up as needed.

Happy generating!
