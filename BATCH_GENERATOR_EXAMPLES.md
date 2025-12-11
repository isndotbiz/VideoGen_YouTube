# Enhanced FAL Batch Generator - Usage Examples

Real-world examples and use cases for the Enhanced FAL.ai Batch Image Generator.

## Table of Contents
- [Quick Examples](#quick-examples)
- [Real-World Scenarios](#real-world-scenarios)
- [Advanced Configurations](#advanced-configurations)
- [Prompt Engineering](#prompt-engineering)
- [Workflow Integration](#workflow-integration)

---

## Quick Examples

### Example 1: First Time Setup and Test

```bash
# Step 1: Verify setup
python test_fal_setup.py

# Step 2: Preview what will be generated
python enhanced_fal_batch_generator.py \
  --prompts sample_image_prompts.json \
  --dry-run

# Step 3: Generate a small test batch
# Create test_batch.json with 3 prompts first
python enhanced_fal_batch_generator.py \
  --prompts test_batch.json

# Step 4: If successful, run the full batch
python enhanced_fal_batch_generator.py \
  --prompts sample_image_prompts.json \
  --workers 4
```

### Example 2: Fast Generation (Good Network)

```bash
# Use more workers for faster generation
python enhanced_fal_batch_generator.py \
  --prompts sample_image_prompts.json \
  --workers 6 \
  --max-retries 2
```

### Example 3: Conservative Generation (Slow Network)

```bash
# Fewer workers, more retries for stability
python enhanced_fal_batch_generator.py \
  --prompts sample_image_prompts.json \
  --workers 2 \
  --max-retries 5 \
  --timeout 300
```

### Example 4: Custom Output Directory

```bash
# Generate to specific location
python enhanced_fal_batch_generator.py \
  --prompts my_prompts.json \
  --output ~/Documents/ai_images \
  --workers 4
```

---

## Real-World Scenarios

### Scenario 1: YouTube Video Thumbnail Generation

**Goal**: Generate 10 eye-catching thumbnails for a YouTube series

**Prompts File** (`youtube_thumbnails.json`):
```json
{
  "prompts": [
    {
      "section": "Episode_Thumbnails",
      "image_number": 1,
      "image_prompt": "Bold text 'AI REVOLUTION' on futuristic tech background, dramatic lighting, blue and orange color scheme, YouTube thumbnail style, high contrast, 8k resolution",
      "description": "Ep1_AI_Revolution"
    },
    {
      "section": "Episode_Thumbnails",
      "image_number": 2,
      "image_prompt": "Shocked person looking at computer screen showing code, dramatic expression, vibrant colors, YouTube thumbnail aesthetic, professional photography, 8k",
      "description": "Ep2_Code_Secrets"
    }
  ]
}
```

**Command**:
```bash
python enhanced_fal_batch_generator.py \
  --prompts youtube_thumbnails.json \
  --output ./youtube_assets/thumbnails \
  --workers 3
```

**Expected Output**:
- `Episode_Thumbnails_001_Ep1_AI_Revolution.png`
- `Episode_Thumbnails_002_Ep2_Code_Secrets.png`
- Individual metadata for each thumbnail
- ~2-3 minutes total generation time

---

### Scenario 2: Blog Post Header Images

**Goal**: Create consistent header images for a tech blog series

**Prompts File** (`blog_headers.json`):
```json
{
  "prompts": [
    {
      "section": "Blog_Headers",
      "image_number": 1,
      "image_prompt": "Abstract representation of cloud computing with floating servers and data streams, minimalist design, blue gradient background, modern tech illustration, wide banner format, 8k resolution",
      "description": "Cloud_Computing_101"
    },
    {
      "section": "Blog_Headers",
      "image_number": 2,
      "image_prompt": "Cybersecurity concept with digital shield and lock icons, professional tech aesthetic, dark blue background with green accents, banner format, 8k resolution",
      "description": "Security_Best_Practices"
    }
  ]
}
```

**Command**:
```bash
python enhanced_fal_batch_generator.py \
  --prompts blog_headers.json \
  --output ./blog_assets/headers \
  --workers 4
```

---

### Scenario 3: Product Marketing Assets

**Goal**: Generate diverse product visualization images

**Prompts File** (`product_images.json`):
```json
{
  "prompts": [
    {
      "section": "Product_Hero",
      "image_number": 1,
      "image_prompt": "Modern SaaS dashboard interface with analytics graphs and clean UI, professional product photography style, bright lighting, white background, high detail, 8k resolution",
      "description": "Dashboard_Hero"
    },
    {
      "section": "Product_Features",
      "image_number": 2,
      "image_prompt": "Smartphone displaying mobile app interface, hands holding device, professional product photo, soft lighting, blurred background, 8k resolution, commercial photography",
      "description": "Mobile_App_Demo"
    },
    {
      "section": "Product_Features",
      "image_number": 3,
      "image_prompt": "Team collaboration scene with people using software on laptops, modern office setting, natural lighting, diverse team, professional corporate photography, 8k",
      "description": "Team_Collaboration"
    }
  ]
}
```

**Command**:
```bash
python enhanced_fal_batch_generator.py \
  --prompts product_images.json \
  --output ./marketing/product_images \
  --workers 4 \
  --max-retries 3
```

---

### Scenario 4: Educational Course Materials

**Goal**: Create consistent visual assets for an online course

**Prompts File** (`course_visuals.json`):
```json
{
  "prompts": [
    {
      "section": "Module_1",
      "image_number": 1,
      "image_prompt": "Professional diagram showing the basics of programming, colorful flowchart with code blocks, educational illustration style, clean design, 8k resolution",
      "description": "Programming_Basics"
    },
    {
      "section": "Module_1",
      "image_number": 2,
      "image_prompt": "Visualization of data structures - arrays, linked lists, trees - in 3D isometric style, educational tech illustration, blue and purple color scheme, 8k",
      "description": "Data_Structures"
    },
    {
      "section": "Module_2",
      "image_number": 3,
      "image_prompt": "Algorithm visualization showing sorting process, animated-style illustration with numbered blocks, clear educational design, bright colors, 8k resolution",
      "description": "Sorting_Algorithms"
    }
  ]
}
```

**Command**:
```bash
python enhanced_fal_batch_generator.py \
  --prompts course_visuals.json \
  --output ./course_materials/module_images \
  --workers 3
```

---

## Advanced Configurations

### Configuration 1: High Quality, Slow Generation

For maximum quality when time isn't critical:

**Edit Script** (lines ~289-298):
```python
arguments={
    "prompt": prompt,
    "image_size": {"width": 1920, "height": 1080},
    "num_inference_steps": 100,      # Maximum quality
    "guidance_scale": 12.0,           # Strong prompt adherence
    "num_images": 1,
    "enable_safety_checker": False,
    "output_format": "png"
}
```

**Run with conservative settings**:
```bash
python enhanced_fal_batch_generator.py \
  --prompts critical_images.json \
  --workers 2 \
  --timeout 300
```

---

### Configuration 2: Fast Generation, Good Quality

For quick turnaround with acceptable quality:

**Edit Script**:
```python
arguments={
    "prompt": prompt,
    "image_size": {"width": 1920, "height": 1080},
    "num_inference_steps": 35,       # Faster
    "guidance_scale": 6.0,            # Moderate adherence
    "num_images": 1,
    "enable_safety_checker": False,
    "output_format": "png"
}
```

**Run with aggressive parallelization**:
```bash
python enhanced_fal_batch_generator.py \
  --prompts quick_batch.json \
  --workers 6 \
  --max-retries 2
```

---

### Configuration 3: Different Aspect Ratios

**Square Images (1:1)**:
```python
"image_size": {"width": 1024, "height": 1024}
```

**Portrait (9:16)**:
```python
"image_size": {"width": 1080, "height": 1920}
```

**Ultrawide (21:9)**:
```python
"image_size": {"width": 2560, "height": 1080}
```

---

## Prompt Engineering

### Pattern 1: Consistent Style Series

For maintaining visual consistency across multiple images:

```json
{
  "prompts": [
    {
      "section": "Brand_Assets",
      "image_number": 1,
      "image_prompt": "Corporate office building exterior, modern glass architecture, blue sky, professional photography style, Canon EF 24-70mm, golden hour lighting, 8k resolution, commercial real estate photography",
      "description": "Office_Exterior"
    },
    {
      "section": "Brand_Assets",
      "image_number": 2,
      "image_prompt": "Modern office interior lobby, marble floors, large windows, professional photography style, Canon EF 24-70mm, natural lighting, 8k resolution, commercial real estate photography",
      "description": "Office_Lobby"
    }
  ]
}
```

**Key**: Repeat style descriptors ("professional photography style, Canon EF 24-70mm, 8k resolution")

---

### Pattern 2: Technical Diagrams

For clear, educational technical illustrations:

```json
{
  "section": "Technical_Docs",
  "image_number": 1,
  "image_prompt": "Clean technical diagram of client-server architecture, simplified illustration style, blue and gray color scheme, arrows showing data flow, labeled components, technical documentation aesthetic, high contrast, 8k resolution",
  "description": "Client_Server_Architecture"
}
```

**Key**: Use "technical diagram", "illustration style", "labeled components"

---

### Pattern 3: Photorealistic Scenes

For realistic, photograph-like images:

```json
{
  "section": "Lifestyle",
  "image_number": 1,
  "image_prompt": "Professional woman working on laptop in modern coffee shop, natural window lighting, shallow depth of field, shot with Sony A7III 85mm f/1.8, candid moment, warm color grading, 8k resolution, lifestyle photography",
  "description": "Remote_Work_Scene"
}
```

**Key**: Specify camera, lens, lighting conditions, photography style

---

### Pattern 4: Abstract Concepts

For visualizing intangible ideas:

```json
{
  "section": "Concepts",
  "image_number": 1,
  "image_prompt": "Abstract visualization of machine learning neural network, flowing data particles forming network nodes, blue and purple holographic effects, futuristic tech aesthetic, floating in dark space, particle effects, 8k resolution, concept art",
  "description": "ML_Neural_Network"
}
```

**Key**: Use "abstract visualization", "concept art", describe mood and color

---

## Workflow Integration

### Workflow 1: Automated Video Production Pipeline

```bash
#!/bin/bash
# generate_video_assets.sh

echo "=== Video Asset Generation Pipeline ==="

# Step 1: Generate images
echo "Step 1: Generating images..."
python enhanced_fal_batch_generator.py \
  --prompts video_prompts.json \
  --output ./video_assets/images \
  --workers 4

# Step 2: Check success rate
SUCCESS_RATE=$(python -c "
import json
with open('./video_assets/images/batch_metadata.json') as f:
    data = json.load(f)
    rate = (data['successful'] / data['total_images']) * 100
    print(f'{rate:.1f}')
")

echo "Success rate: ${SUCCESS_RATE}%"

if (( $(echo "$SUCCESS_RATE >= 95" | bc -l) )); then
    echo "✓ Image generation successful, proceeding to video assembly"
    # Continue with video assembly
    # python video_assembly.py ...
else
    echo "✗ Too many failures, check batch_generation.log"
    exit 1
fi
```

---

### Workflow 2: Scheduled Batch Generation

```bash
#!/bin/bash
# scheduled_generation.sh
# Run with cron: 0 2 * * * /path/to/scheduled_generation.sh

DATE=$(date +%Y%m%d)
OUTPUT_DIR="./daily_images/${DATE}"

# Generate daily social media assets
python enhanced_fal_batch_generator.py \
  --prompts daily_prompts.json \
  --output "${OUTPUT_DIR}" \
  --workers 4

# Upload to cloud storage
# aws s3 sync "${OUTPUT_DIR}" "s3://my-bucket/images/${DATE}/"

# Send notification
# curl -X POST "webhook_url" -d "Generated ${DATE} images"
```

---

### Workflow 3: Quality Control Pipeline

```bash
#!/bin/bash
# generate_with_qc.sh

# Generate images
python enhanced_fal_batch_generator.py \
  --prompts prompts.json \
  --output ./output/generated_images

# Extract metadata for failed images
python -c "
import json
from pathlib import Path

with open('./output/generated_images/batch_metadata.json') as f:
    data = json.load(f)

failed = [img for img in data['images'] if not img['success']]

if failed:
    print(f'\\n{len(failed)} images failed:')
    for img in failed:
        print(f\"  - {img['output_filename']}: {img['error_message']}\")

    # Save failed prompts for retry
    retry_prompts = {
        'prompts': [
            {
                'section': img['section'],
                'image_number': img['image_number'],
                'image_prompt': img['image_prompt'],
                'description': img['description']
            }
            for img in failed
        ]
    }

    with open('./retry_prompts.json', 'w') as f:
        json.dump(retry_prompts, f, indent=2)

    print(f'\\nSaved retry prompts to: retry_prompts.json')
else:
    print('\\n✓ All images generated successfully!')
"
```

---

### Workflow 4: A/B Testing Different Prompts

```python
#!/usr/bin/env python3
# ab_test_prompts.py
"""Generate variations of prompts for A/B testing"""

import json
from pathlib import Path
import subprocess

# Base prompt
base = "A modern tech office with developers working"

# Variations
variations = {
    "photorealistic": f"{base}, photorealistic, professional photography, 8k",
    "illustrated": f"{base}, digital illustration, clean modern style, 8k",
    "cinematic": f"{base}, cinematic composition, dramatic lighting, film photography, 8k",
}

for style, prompt in variations.items():
    # Create prompt file
    prompt_data = {
        "prompts": [{
            "section": "AB_Test",
            "image_number": 1,
            "image_prompt": prompt,
            "description": f"test_{style}"
        }]
    }

    prompt_file = f"test_{style}.json"
    with open(prompt_file, 'w') as f:
        json.dump(prompt_data, f, indent=2)

    # Generate
    print(f"\nGenerating {style} variation...")
    subprocess.run([
        "python", "enhanced_fal_batch_generator.py",
        "--prompts", prompt_file,
        "--output", f"./ab_test/{style}"
    ])

print("\n✓ A/B test variations generated!")
print("Compare images in: ./ab_test/")
```

---

## Monitoring and Maintenance

### Monitor Generation Progress

```bash
# In one terminal: run generation
python enhanced_fal_batch_generator.py --prompts large_batch.json

# In another terminal: monitor logs
watch -n 5 'tail -20 batch_generation.log | grep "Generated\|Error"'

# Check current progress
python -c "
import json
from pathlib import Path
from glob import glob

total = len(json.load(open('large_batch.json'))['prompts'])
generated = len(glob('output/generated_images/*.png'))
progress = (generated / total) * 100

print(f'Progress: {generated}/{total} ({progress:.1f}%)')
"
```

---

### Cost Tracking

```bash
# Calculate actual costs from metadata
python -c "
import json
with open('output/generated_images/batch_metadata.json') as f:
    data = json.load(f)
    cost = data['successful'] * 0.03
    print(f'Total cost: \${cost:.2f}')
    print(f'Images generated: {data[\"successful\"]}')
    print(f'Failed: {data[\"failed\"]}')
    print(f'Average time: {data[\"avg_generation_time\"]:.1f}s')
"
```

---

## Tips for Success

1. **Start Small**: Test with 3-5 images before large batches
2. **Use Dry-Run**: Always preview with `--dry-run` first
3. **Monitor Logs**: Keep `batch_generation.log` open during generation
4. **Optimize Workers**: 3-4 workers is optimal for most connections
5. **Version Control**: Keep prompt files in git for tracking changes
6. **Backup Outputs**: Copy generated images to permanent storage
7. **Cost Control**: Use dry-run to estimate costs before running
8. **Prompt Consistency**: Reuse style descriptors for consistent results
9. **Error Recovery**: The script auto-skips existing files for easy retry
10. **Quality Check**: Review first few images before generating full batch

---

## Getting Help

### Check System Status
```bash
python test_fal_setup.py
```

### Review Generation Logs
```bash
# Recent errors
grep ERROR batch_generation.log | tail -20

# Recent successes
grep "Generated" batch_generation.log | tail -20

# Performance stats
grep "STATISTICS" batch_generation.log -A 15
```

### Debug Failed Images
```bash
# List failed image metadata
python -c "
import json
with open('output/generated_images/batch_metadata.json') as f:
    data = json.load(f)
    for img in data['images']:
        if not img['success']:
            print(f\"{img['output_filename']}: {img['error_message']}\")
"
```

---

Happy generating!
