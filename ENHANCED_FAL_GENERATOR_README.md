# Enhanced FAL.ai Batch Image Generator

Production-ready Python script for batch image generation using FAL.ai's Flux API with advanced features including parallel processing, comprehensive error handling, and detailed performance tracking.

## Features

### Core Capabilities
- **High Quality Generation**: 1920x1080 resolution with optimized quality settings
- **Parallel Processing**: Generate 3-4 images concurrently for faster throughput
- **Smart Retry Logic**: Exponential backoff with configurable retry attempts
- **Progress Tracking**: Real-time progress bars and detailed logging
- **Metadata Storage**: Individual JSON metadata files for each generated image
- **Performance Metrics**: Comprehensive statistics and timing data
- **Error Handling**: Robust error handling with detailed logging
- **Resume Support**: Automatically skips already-generated images

### Production Features
- Structured logging to both file and console
- Cost estimation based on actual generation
- Dry-run mode for testing without generating
- Configurable workers, retries, and timeouts
- Batch metadata summary with all generation details
- Sanitized filenames for cross-platform compatibility

## Installation

### Prerequisites
```bash
# Python 3.8 or higher required
python --version

# Install required packages
pip install fal-client python-dotenv requests tqdm
```

### Environment Setup
Create a `.env` file in the project root:
```bash
FAL_API_KEY=your_fal_api_key_here
```

Get your FAL.ai API key from: https://fal.ai/dashboard/keys

## Usage

### Basic Usage
```bash
# Generate images from prompts.json with default settings
python enhanced_fal_batch_generator.py --prompts prompts.json

# Use sample prompts file
python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json
```

### Advanced Options
```bash
# Customize number of parallel workers (3-4 recommended)
python enhanced_fal_batch_generator.py --prompts prompts.json --workers 4

# Custom output directory
python enhanced_fal_batch_generator.py --prompts prompts.json --output ./my_images

# Increase retry attempts for unstable connections
python enhanced_fal_batch_generator.py --prompts prompts.json --max-retries 5

# Dry run to preview what will be generated
python enhanced_fal_batch_generator.py --prompts prompts.json --dry-run
```

### Full Command Reference
```
usage: enhanced_fal_batch_generator.py [-h] [--prompts PROMPTS] [--output OUTPUT]
                                       [--workers WORKERS] [--max-retries MAX_RETRIES]
                                       [--timeout TIMEOUT] [--dry-run]

Options:
  --prompts PROMPTS         Path to JSON file with prompts (default: prompts.json)
  --output OUTPUT           Output directory (default: ./output/generated_images)
  --workers WORKERS         Parallel workers, 3-4 recommended (default: 4)
  --max-retries MAX_RETRIES Maximum retry attempts (default: 3)
  --timeout TIMEOUT         Request timeout in seconds (default: 120)
  --dry-run                 Preview without generating
```

## Input Format

### Required JSON Structure
Your prompts JSON file should follow this structure:

```json
{
  "prompts": [
    {
      "section": "Section Name",
      "image_number": 1,
      "image_prompt": "Detailed prompt for image generation",
      "description": "Brief description for filename"
    },
    {
      "section": "Another Section",
      "image_number": 2,
      "image_prompt": "Another detailed prompt",
      "description": "Another description"
    }
  ]
}
```

### Field Descriptions
- **section**: Category or section name (used in filename)
- **image_number**: Numeric identifier for ordering
- **image_prompt**: The actual prompt text sent to FAL.ai
- **description**: Brief description (used in filename)

### Alternative Formats
The script also supports these fallback field names:
- `prompt`, `text` → `image_prompt`
- `id` → `image_number`
- `name` → `description`

## Output Structure

### Directory Layout
```
output/
└── generated_images/
    ├── Section_Name_001_Description.png
    ├── Section_Name_002_Description.png
    ├── batch_metadata.json
    └── metadata/
        ├── Section_Name_001_Description.png.json
        ├── Section_Name_002_Description.png.json
        └── ...
```

### Individual Metadata Files
Each image gets a metadata JSON file:
```json
{
  "section": "Introduction",
  "image_number": 1,
  "image_prompt": "A modern tech workspace...",
  "description": "Developer Workspace",
  "output_filename": "Introduction_001_Developer_Workspace.png",
  "generation_time": 12.5,
  "timestamp": "2025-12-10T14:30:45.123456",
  "model": "fal-ai/flux/dev",
  "resolution": "1920x1080",
  "success": true,
  "error_message": null,
  "retry_count": 0
}
```

### Batch Metadata File
A comprehensive summary of the entire batch:
```json
{
  "generated_at": "2025-12-10T14:45:30.123456",
  "total_images": 32,
  "successful": 31,
  "failed": 1,
  "total_generation_time": 385.2,
  "avg_generation_time": 12.4,
  "total_retries": 2,
  "images": [...]
}
```

## Performance Characteristics

### Throughput
- **Sequential**: ~1 image per 10-15 seconds
- **Parallel (4 workers)**: ~3-4 images per 15 seconds
- **Typical batch (30 images)**: ~5-8 minutes with parallel processing

### Cost Estimation
- FAL.ai Flux Dev: ~$0.03 per image
- 30 images: ~$0.90
- Cost displayed before generation starts

### Resource Usage
- **Memory**: ~200-500 MB
- **Network**: ~2-5 MB per image download
- **Disk**: ~1-3 MB per generated PNG image

## Error Handling

### Automatic Retry
- Exponential backoff: 2s, 4s, 8s delays
- Configurable retry count (default: 3)
- Detailed error logging

### Common Issues

#### 1. API Key Not Found
```
ValueError: FAL_API_KEY not found in environment variables
```
**Solution**: Add `FAL_API_KEY=your_key` to `.env` file

#### 2. Network Timeout
```
Error generating image: timeout
```
**Solution**: Increase timeout: `--timeout 300`

#### 3. Rate Limiting
```
Error: Too many requests
```
**Solution**: Reduce workers: `--workers 2`

#### 4. Memory Issues
```
MemoryError or system slowdown
```
**Solution**: Reduce workers: `--workers 2`

## Advanced Usage

### Resuming Failed Batches
The script automatically skips existing images:
```bash
# Run again - only generates missing/failed images
python enhanced_fal_batch_generator.py --prompts prompts.json
```

### Monitoring Progress
Two log outputs:
1. **Console**: Real-time progress with tqdm progress bar
2. **batch_generation.log**: Complete log file

View live logs:
```bash
tail -f batch_generation.log
```

### Integration with Other Scripts
```python
from enhanced_fal_batch_generator import EnhancedFALBatchGenerator

# Initialize
generator = EnhancedFALBatchGenerator(
    output_dir="./custom_output",
    max_workers=4,
    max_retries=3
)

# Load and generate
prompts = generator.load_prompts("my_prompts.json")
stats = generator.generate_batch_parallel(prompts)

# Access results
print(f"Success rate: {stats.successful / stats.total * 100:.1f}%")
```

### Custom Filename Format
Modify the `generate_filename()` method for custom formats:
```python
def generate_filename(self, prompt_data: Dict) -> str:
    # Custom format: timestamp_section_number.png
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    section = self.sanitize_filename(prompt_data.get('section', 'img'))
    num = prompt_data.get('image_number', 0)
    return f"{timestamp}_{section}_{num:03d}.png"
```

## Optimization Tips

### For Best Quality
```bash
# Edit script to increase inference steps (line ~289):
"num_inference_steps": 75,  # Higher = better quality, slower
"guidance_scale": 9.0,      # Higher = more prompt adherence
```

### For Faster Generation
```bash
# Increase workers (requires good network)
python enhanced_fal_batch_generator.py --prompts prompts.json --workers 6

# Edit script for faster settings (line ~289):
"num_inference_steps": 30,  # Lower = faster, lower quality
```

### For Cost Savings
```bash
# Use dry-run first to verify prompts
python enhanced_fal_batch_generator.py --prompts prompts.json --dry-run

# Generate only specific sections (edit JSON file)
```

## API Configuration

### Current Settings
The script uses these FAL.ai Flux Dev parameters:

```python
{
    "prompt": prompt,
    "image_size": {"width": 1920, "height": 1080},
    "num_inference_steps": 50,      # Quality/speed balance
    "guidance_scale": 7.5,           # Prompt adherence
    "num_images": 1,
    "enable_safety_checker": False,
    "output_format": "png"
}
```

### Customization
Edit line ~289-298 in `enhanced_fal_batch_generator.py` to adjust:
- **num_inference_steps**: 20-100 (higher = better quality)
- **guidance_scale**: 1.0-15.0 (higher = follows prompt more)
- **image_size**: Any valid resolution
- **output_format**: "png" or "jpeg"

## Troubleshooting

### Import Errors
```bash
# Install missing dependencies
pip install fal-client python-dotenv requests tqdm
```

### Permission Errors
```bash
# Ensure output directory is writable
chmod 755 ./output/generated_images
```

### Slow Generation
1. Check network speed
2. Reduce workers if CPU/RAM limited
3. Check FAL.ai service status
4. Reduce inference steps

### Failed Images
Check `batch_generation.log` for detailed errors:
```bash
grep "ERROR" batch_generation.log
```

## Statistics Example

After completion, you'll see:
```
======================================================================
GENERATION STATISTICS
======================================================================
Total images:           32
Successfully generated: 31 (96.9%)
Failed:                 1 (3.1%)
Total retries:          2

PERFORMANCE METRICS
======================================================================
Total generation time:  385.2s
Average time per image: 12.4s
Throughput:             0.08 images/second

OUTPUT
======================================================================
Images directory:       D:\workspace\True_Nas\firecrawl-mdjsonl\output\generated_images
Metadata directory:     D:\workspace\True_Nas\firecrawl-mdjsonl\output\generated_images\metadata

Estimated cost:         $0.93 USD
======================================================================
```

## Best Practices

1. **Start with dry-run**: Always test with `--dry-run` first
2. **Check API quota**: Monitor your FAL.ai usage dashboard
3. **Use version control**: Keep prompt files in git
4. **Review metadata**: Check metadata files for quality issues
5. **Backup outputs**: Copy generated images to permanent storage
6. **Monitor costs**: Check batch_metadata.json for actual counts
7. **Test prompts**: Try a few images before running full batch

## Support

### FAL.ai Documentation
- API Docs: https://fal.ai/models/fal-ai/flux/dev
- Dashboard: https://fal.ai/dashboard
- Pricing: https://fal.ai/pricing

### Script Issues
Check the log file first:
```bash
cat batch_generation.log
```

## License

This script is part of the firecrawl-mdjsonl project and uses the same license.

## Version History

- **v1.0** - Initial enhanced version with parallel processing, retry logic, and comprehensive metadata
