# Cleanup Guide: Remove Old Text-Based Images

This guide shows you which images to delete because they were generated with Flux Pro for text (which doesn't work well).

## Images to DELETE

All images that have text, charts, or infographics generated with Flux Pro:

```bash
# Navigate to output directory
cd output/generated_images

# DELETE these categories:
rm -rf infographic/              # All Flux Pro charts/infographics
rm metadata.json                 # Old metadata file
```

### Specific Images to Delete (if organized by name)

If your images are named, DELETE these patterns:

```
flux_chart_*
flux_timeline_*
flux_infographic_*
flux_table_*
flux_comparison_*
flux_steps_*
flux_process_*
flux_funnel_*
flux_diagram_*
flux_myths_*
```

### Full List to Delete

- `flux_chart_ranking_factors.png` ← Bar chart (DELETE)
- `flux_timeline_updates.png` ← Timeline (DELETE)
- `flux_table_comparison.png` ← Table (DELETE)
- `flux_steps_implementation.png` ← Numbered steps (DELETE)
- `flux_comparison_seo_ppc.png` ← Comparison (DELETE)
- `flux_myths_reality.png` ← Myth/reality cards (DELETE)
- `flux_funnel_conversion.png` ← Funnel diagram (DELETE)
- `flux_keywords_matrix.png` ← Matrix grid (DELETE)

### Images to KEEP

Keep ALL photorealistic images:

```
flux_people_1.png           ← Woman at desk (KEEP)
flux_people_2.png           ← Another person (KEEP)
flux_team_1.png            ← Team collaborating (KEEP)
flux_team_2.png            ← Another team shot (KEEP)
flux_closeup_1.png         ← Hands typing (KEEP)
flux_workspace_1.png       ← Desk setup (KEEP)
flux_workspace_2.png       ← Another workspace (KEEP)
flux_environment_*.png     ← Office/workspace (KEEP)
flux_presentation_*.png    ← Person presenting (KEEP)
```

---

## Step-by-Step Cleanup

### 1. Check What You Have

```bash
# List all images
ls -la output/generated_images/

# Show only PNG files with dates
ls -lh output/generated_images/*.png | awk '{print $6, $7, $8, $9}'
```

### 2. Identify Text-Based Images

```bash
# Find all files with these keywords
grep -l "chart\|timeline\|table\|infographic" output/generated_images/metadata.json

# Or manually check:
cat output/generated_images/metadata.json | grep -E "chart|timeline|table"
```

### 3. Delete Old Images

**Option A: Delete entire directory (cleanest)**

```bash
# Remove old image directory
rm -rf output/generated_images/infographic/

# Remove old metadata
rm output/generated_images/metadata.json
```

**Option B: Selective delete (if mixed)**

```bash
# Delete individual files
rm output/generated_images/flux_chart_*.png
rm output/generated_images/flux_timeline_*.png
rm output/generated_images/flux_table_*.png
rm output/generated_images/flux_steps_*.png
rm output/generated_images/flux_comparison_*.png
rm output/generated_images/flux_myths_*.png
rm output/generated_images/flux_funnel_*.png
```

**Option C: Backup first (safest)**

```bash
# Create backup
mkdir output/generated_images_backup_old
cp output/generated_images/flux_chart_*.png output/generated_images_backup_old/
cp output/generated_images/flux_timeline_*.png output/generated_images_backup_old/

# Then delete
rm output/generated_images/flux_chart_*.png
rm output/generated_images/flux_timeline_*.png
```

### 4. Verify Cleanup

```bash
# List remaining images
ls output/generated_images/*.png

# Should show ONLY photorealistic images:
# flux_people_*.png
# flux_team_*.png
# flux_closeup_*.png
# flux_workspace_*.png
# flux_environment_*.png
# flux_presentation_*.png

# Check count
ls output/generated_images/*.png | wc -l
# Should be around 5-8 (photorealistic only)
```

### 5. Generate New Images with Nano Banana

```bash
# Run the new image pipeline
python image-generation-nano-banana.py

# This will create:
# - Old flux_*.png images (keep these)
# - New nano_*.png images (these are the good ones with text)
```

### 6. Verify New Images

```bash
# List all images
ls -la output/generated_images/*.png

# Should now have:
# Flux Pro (photorealistic): 5-8 images
# Nano Banana (text/charts): 7-8 images
# Total: 12-16 images

# Check metadata
cat output/generated_images/metadata_nano_banana.json | grep -E "summary|flux_pro|nano_banana"
```

---

## Checklist

- [ ] Backed up old images (optional but recommended)
- [ ] Identified text-based Flux images
- [ ] Deleted old text-based images
- [ ] Verified photorealistic images remain
- [ ] Generated new Nano Banana images
- [ ] Verified both image types exist
- [ ] Updated references in orchestrator.js
- [ ] Tested image display in video pipeline

---

## Verify Images Are Correct

### Check Image Quality

```bash
# On macOS
open output/generated_images/flux_people_1.png  # Should show person
open output/generated_images/nano_chart_ranking_factors.png  # Should show chart with text

# On Linux
display output/generated_images/flux_people_1.png

# On Windows
start output/generated_images/flux_people_1.png
```

### Check Metadata

```bash
# View image metadata
cat output/generated_images/metadata_nano_banana.json | jq '.models'

# Should show:
# - flux_pro: 5-8 images
# - nano_banana: 7-8 images
```

---

## Why Delete Old Text Images?

### Problems with Flux Pro + Text

- ❌ Text is blurry/unreadable
- ❌ Numbers are incorrect or hallucinated
- ❌ Charts don't align with prompts
- ❌ Labels are misspelled
- ❌ Looks unprofessional

### Nano Banana is Better

- ✓ Text is crisp and clear
- ✓ Numbers render correctly
- ✓ Charts look professional
- ✓ Infographics are polished
- ✓ Video quality improves significantly

---

## File Organization After Cleanup

```
output/
├── generated_images/
│   ├── flux_people_1.png          ← Photorealistic (KEPT)
│   ├── flux_people_2.png
│   ├── flux_team_1.png
│   ├── flux_closeup_1.png
│   ├── flux_workspace_1.png
│   ├── nano_chart_ranking_factors.png      ← Text-based (NEW)
│   ├── nano_timeline_algo_updates.png
│   ├── nano_comparison_table.png
│   ├── nano_steps_implementation.png
│   ├── nano_myths_reality.png
│   ├── nano_funnel_conversion.png
│   ├── nano_keywords_priority.png
│   └── metadata_nano_banana.json           ← NEW metadata
├── projects/
│   └── SEO_Best_Practices/
│       ├── dataset.jsonl
│       └── metadata.json
└── [other directories remain unchanged]
```

---

## Troubleshooting

### "I deleted images but pipeline still uses old ones"

Update the orchestrator to use new metadata:

```bash
# In advanced-video-orchestrator.js, change:
const metadataPath = './output/generated_images/metadata.json'

# To:
const metadataPath = './output/generated_images/metadata_nano_banana.json'
```

### "I accidentally deleted Flux Pro images"

Don't worry! Just regenerate:

```bash
python image-generation-nano-banana.py
```

It will recreate both Flux and Nano Banana images.

### "Directory structure is confusing"

Create clear subdirectories:

```bash
# Organize by model type
mkdir -p output/generated_images/flux-pro
mkdir -p output/generated_images/nano-banana

# Move images
mv output/generated_images/flux_*.png output/generated_images/flux-pro/
mv output/generated_images/nano_*.png output/generated_images/nano-banana/
```

---

## Quick Commands

```bash
# One-command cleanup and regeneration
rm -rf output/generated_images/infographic/ && \
rm output/generated_images/metadata.json && \
python image-generation-nano-banana.py && \
echo "✓ Cleanup and regeneration complete!"
```

---

**After cleanup, your images will look professional and text will be readable!**
