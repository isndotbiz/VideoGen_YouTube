# ComfyUI Setup Guide for Flux Turbo Batch Generation

Complete guide for installing ComfyUI, Flux Turbo model, and running batch image generation.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [ComfyUI Installation](#comfyui-installation)
3. [Installing Flux Turbo Model](#installing-flux-turbo-model)
4. [Installing Turbo LoRA](#installing-turbo-lora)
5. [Running ComfyUI Server](#running-comfyui-server)
6. [Using the Batch Generator](#using-the-batch-generator)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **GPU:** NVIDIA RTX 3060 (12GB VRAM) or better
- **RAM:** 16GB system memory
- **Storage:** 50GB free space (for models and outputs)
- **OS:** Windows 10/11, Linux, or macOS

### Recommended Requirements
- **GPU:** NVIDIA RTX 4060 Ti (16GB VRAM) or RTX 4070
- **RAM:** 32GB system memory
- **Storage:** 100GB+ SSD storage
- **OS:** Windows 11 or Ubuntu 22.04 LTS

### For Your TrueNAS Setup
Based on your infrastructure:
- **GPU:** RTX 4060 Ti 16GB (excellent for Flux Turbo)
- **Models Location:** Transfer from `D:\models\rtx4060ti-16gb` to TrueNAS
- **Storage:** Use ZFS dataset for model storage and outputs

---

## ComfyUI Installation

### Option 1: Standalone Portable (Windows - Recommended)

1. **Download ComfyUI Portable:**
   ```bash
   # Visit: https://github.com/comfyanonymous/ComfyUI/releases
   # Download: ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z
   ```

2. **Extract and Run:**
   ```bash
   # Extract to a location with plenty of space
   cd ComfyUI_windows_portable

   # Run the portable version
   run_nvidia_gpu.bat
   ```

3. **Access Web UI:**
   - Open browser to: `http://localhost:8188`

### Option 2: Git Clone (All Platforms)

1. **Clone Repository:**
   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI.git
   cd ComfyUI
   ```

2. **Create Virtual Environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   pip install -r requirements.txt
   ```

4. **Run ComfyUI:**
   ```bash
   python main.py
   ```

### Option 3: Docker Installation

1. **Using Docker Compose:**
   ```yaml
   # docker-compose.yml
   version: '3.8'

   services:
     comfyui:
       image: comfyanonymous/comfyui:latest
       container_name: comfyui
       ports:
         - "8188:8188"
       volumes:
         - ./models:/app/models
         - ./outputs:/app/output
       environment:
         - NVIDIA_VISIBLE_DEVICES=all
       deploy:
         resources:
           reservations:
             devices:
               - driver: nvidia
                 count: 1
                 capabilities: [gpu]
   ```

2. **Start Container:**
   ```bash
   docker-compose up -d
   ```

---

## Installing Flux Turbo Model

### Model Download

1. **Download Flux Turbo (FP8 version recommended):**
   ```bash
   # Visit Hugging Face:
   # https://huggingface.co/black-forest-labs/FLUX.1-turbo

   # Or use wget/curl:
   cd ComfyUI/models/checkpoints

   # FP8 version (smaller, faster, less VRAM)
   wget https://huggingface.co/black-forest-labs/FLUX.1-turbo/resolve/main/flux1-turbo-dev-fp8.safetensors

   # Full precision version (larger, higher quality)
   wget https://huggingface.co/black-forest-labs/FLUX.1-turbo/resolve/main/flux1-turbo-dev.safetensors
   ```

2. **Alternative: Download from Browser:**
   - Visit: https://huggingface.co/black-forest-labs/FLUX.1-turbo
   - Download `flux1-turbo-dev-fp8.safetensors`
   - Place in: `ComfyUI/models/checkpoints/`

### Model File Structure

```
ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── flux1-turbo-dev-fp8.safetensors  (Main model)
│   ├── loras/
│   │   └── flux_turbo_lora.safetensors       (Turbo LoRA)
│   ├── vae/
│   └── clip/
├── output/
└── input/
```

---

## Installing Turbo LoRA

### What is Turbo LoRA?

Turbo LoRA is a Low-Rank Adaptation that optimizes Flux for faster inference with fewer steps while maintaining quality.

### Download and Install

1. **Download Turbo LoRA:**
   ```bash
   cd ComfyUI/models/loras

   # Download from Hugging Face
   wget https://huggingface.co/ByteDance/Hyper-SD/resolve/main/Hyper-FLUX.1-dev-8steps-lora.safetensors -O flux_turbo_lora.safetensors
   ```

2. **Verify Installation:**
   ```bash
   ls -lh ComfyUI/models/loras/
   # Should show: flux_turbo_lora.safetensors
   ```

### LoRA Settings

- **Strength:** 0.8 - 1.0 (recommended: 1.0)
- **Steps:** 15-30 (turbo optimized: 20)
- **CFG Scale:** 2.5 - 4.5 (recommended: 3.5)

---

## Running ComfyUI Server

### Start the Server

```bash
# Default (port 8188)
python main.py

# Custom port
python main.py --port 8080

# Listen on all interfaces (for remote access)
python main.py --listen 0.0.0.0

# With CUDA optimizations
python main.py --use-split-cross-attention --use-quad-cross-attention
```

### For TrueNAS Deployment

If running on your TrueNAS VM:

```bash
# Run with network access for remote use
python main.py --listen 0.0.0.0 --port 8188

# Access from other machines via:
# http://<truenas-ip>:8188
```

### Verify Server is Running

```bash
# Test endpoint
curl http://localhost:8188/system_stats

# Should return JSON with system info
```

---

## Using the Batch Generator

### Installation

1. **Install Python Dependencies:**
   ```bash
   pip install requests websocket-client pillow
   ```

2. **Verify Files:**
   ```bash
   ls -la
   # Should have:
   # - flux_turbo_batch.json
   # - batch_generator.py
   # - prompts.json
   ```

### Basic Usage

```bash
# Generate all images from prompts.json
python batch_generator.py

# Specify custom host/port
python batch_generator.py --host 192.168.1.100 --port 8188

# Use fast mode (15 steps, CFG 3.0)
python batch_generator.py --mode fast

# Generate only first 5 images
python batch_generator.py --limit 5

# Custom output directory
python batch_generator.py --output my_outputs
```

### Generation Modes

```bash
# Fast Mode - Quick generation, good quality
python batch_generator.py --mode fast
# Steps: 15, CFG: 3.0
# ~8-10 seconds per image on RTX 4060 Ti

# Balanced Mode - Recommended default
python batch_generator.py --mode balanced
# Steps: 20, CFG: 3.5
# ~12-15 seconds per image on RTX 4060 Ti

# Quality Mode - Highest quality, slower
python batch_generator.py --mode quality
# Steps: 30, CFG: 4.0
# ~20-25 seconds per image on RTX 4060 Ti
```

### Workflow in ComfyUI UI

1. **Import Workflow:**
   - Open ComfyUI in browser: `http://localhost:8188`
   - Click "Load" button
   - Select `flux_turbo_batch.json`

2. **Modify Settings:**
   - Edit positive prompt in CLIPTextEncode node
   - Adjust steps/CFG in KSampler node
   - Change resolution in EmptyLatentImage node

3. **Queue Single Generation:**
   - Click "Queue Prompt" button
   - Monitor progress in browser
   - Images save to `ComfyUI/output/`

---

## Performance Optimization

### GPU Optimization

#### For RTX 4060 Ti 16GB

```bash
# Use FP8 model to save VRAM
# flux1-turbo-dev-fp8.safetensors (~8GB VRAM)

# Optimal settings for RTX 4060 Ti:
- Resolution: 1920x1080 (recommended)
- Batch size: 1
- Steps: 20
- CFG: 3.5
- Use xFormers attention: --use-split-cross-attention
```

#### VRAM Usage Guide

| Model Version | VRAM Usage | Quality | Speed |
|--------------|------------|---------|-------|
| FP8 | 8-10GB | Very Good | Fastest |
| FP16 | 14-18GB | Excellent | Fast |
| Full Precision | 20-24GB | Best | Slower |

### Speed Optimization Tips

1. **Lower Steps for Turbo:**
   ```python
   # In prompts.json, adjust:
   "generation_settings": {
     "steps": 15,  # Lower for faster (min 10)
     "cfg_scale": 3.0
   }
   ```

2. **Use Smaller Resolutions:**
   ```json
   {
     "width": 1280,
     "height": 720
   }
   ```
   - 1920x1080: ~15 sec/image
   - 1280x720: ~8 sec/image
   - 1024x1024: ~10 sec/image

3. **Batch Processing Strategy:**
   ```bash
   # Process during off-hours
   nohup python batch_generator.py --mode fast > generation.log 2>&1 &

   # Or use screen/tmux for long batches
   screen -S flux_gen
   python batch_generator.py
   # Ctrl+A, D to detach
   ```

### Quality vs Speed Trade-offs

```
Maximum Speed (5-8 sec/image):
- Steps: 10-12
- CFG: 2.5
- Resolution: 1024x1024
- Quality: Good for previews

Balanced (12-15 sec/image):
- Steps: 20
- CFG: 3.5
- Resolution: 1920x1080
- Quality: Excellent for production

Maximum Quality (25-30 sec/image):
- Steps: 30-35
- CFG: 4.0-4.5
- Resolution: 1920x1080
- Quality: Best for final renders
```

---

## Troubleshooting

### Common Issues

#### 1. "Cannot connect to ComfyUI server"

**Solution:**
```bash
# Check if server is running
curl http://localhost:8188/system_stats

# Start server if not running
cd ComfyUI
python main.py

# Check firewall rules (Windows)
netsh advfirewall firewall add rule name="ComfyUI" dir=in action=allow protocol=TCP localport=8188
```

#### 2. "Out of VRAM" Error

**Solution:**
```bash
# Use FP8 model instead of full precision
# OR lower resolution in workflow:

# In flux_turbo_batch.json, find EmptyLatentImage node:
"widgets_values": [
  1280,  # width (was 1920)
  720,   # height (was 1080)
  1
]

# OR use --lowvram flag:
python main.py --lowvram
```

#### 3. "Model not found" Error

**Solution:**
```bash
# Check model exists
ls ComfyUI/models/checkpoints/

# Ensure exact filename matches workflow:
# flux1-turbo-dev-fp8.safetensors

# Download if missing:
cd ComfyUI/models/checkpoints
wget https://huggingface.co/black-forest-labs/FLUX.1-turbo/resolve/main/flux1-turbo-dev-fp8.safetensors
```

#### 4. Slow Generation Speed

**Solutions:**
1. Use FP8 model
2. Lower steps to 15
3. Enable GPU optimizations:
   ```bash
   python main.py --use-split-cross-attention
   ```
4. Close other GPU applications
5. Update NVIDIA drivers

#### 5. "LoRA not applying" Error

**Solution:**
```bash
# Verify LoRA file exists
ls ComfyUI/models/loras/

# Check LoRA filename matches workflow
# Should be: flux_turbo_lora.safetensors

# Restart ComfyUI to reload models
```

### Performance Diagnostics

```bash
# Check GPU usage
nvidia-smi

# Monitor during generation
watch -n 1 nvidia-smi

# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
```

---

## Advanced Configuration

### Custom Workflow Modifications

#### Change Sampler

In `flux_turbo_batch.json`, find KSampler node:
```json
"widgets_values": [
  42,                    // seed
  "randomize",          // seed control
  20,                   // steps
  3.5,                  // cfg_scale
  "dpmpp_2m_sde",      // sampler (change this)
  "karras",            // scheduler
  1.0                  // denoise
]
```

**Recommended Samplers for Flux Turbo:**
- `dpmpp_2m_sde` - Best quality/speed balance
- `euler_a` - Faster, slightly different style
- `dpmpp_2s_ancestral` - More creative variations

#### Add Multiple LoRAs

You can stack LoRAs by adding more LoraLoader nodes:
1. Duplicate node 2 (LoraLoader)
2. Connect output MODEL from first LoRA to input of second
3. Load different LoRA file
4. Adjust strengths as needed

### Automation Scripts

#### Windows Batch Script

Create `run_batch_generation.bat`:
```batch
@echo off
echo Starting ComfyUI Batch Generation
echo.

REM Activate virtual environment if using one
REM call venv\Scripts\activate

REM Run batch generator
python batch_generator.py --mode balanced --output outputs\%date:~-4,4%%date:~-10,2%%date:~-7,2%

echo.
echo Generation complete! Press any key to exit.
pause
```

#### Linux/Mac Shell Script

Create `run_batch_generation.sh`:
```bash
#!/bin/bash

echo "Starting ComfyUI Batch Generation"

# Activate virtual environment if using one
# source venv/bin/activate

# Create output directory with timestamp
OUTPUT_DIR="outputs/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# Run batch generator
python batch_generator.py \
  --mode balanced \
  --output "$OUTPUT_DIR"

echo "Generation complete! Check: $OUTPUT_DIR"
```

Make executable:
```bash
chmod +x run_batch_generation.sh
./run_batch_generation.sh
```

---

## Integration with TrueNAS

### Store Models on TrueNAS

1. **Create Dataset:**
   ```bash
   # On TrueNAS
   zfs create tank/ai-models
   zfs set compression=lz4 tank/ai-models
   ```

2. **Mount via SMB/NFS:**
   ```bash
   # Windows - Map network drive
   net use M: \\truenas\ai-models

   # Create symlink in ComfyUI
   mklink /D "ComfyUI\models\checkpoints" "M:\flux\checkpoints"
   ```

3. **Linux/Docker:**
   ```yaml
   # docker-compose.yml
   volumes:
     - /mnt/truenas/ai-models:/app/models
   ```

### Remote Generation

Run ComfyUI on TrueNAS VM, generate from workstation:

```bash
# On workstation
python batch_generator.py --host truenas.local --port 8188
```

---

## Quick Reference

### File Locations

```
flux_turbo_batch.json       - Main ComfyUI workflow
batch_generator.py          - Python automation script
prompts.json               - Image prompts list
flux_turbo_workflow.js     - JavaScript generator
COMFYUI_SETUP_GUIDE.md    - This file
```

### Key Commands

```bash
# Start ComfyUI
python main.py --listen 0.0.0.0

# Generate all images (balanced mode)
python batch_generator.py

# Fast batch generation
python batch_generator.py --mode fast

# Check server status
curl http://localhost:8188/system_stats
```

### Default Settings

| Setting | Value | Description |
|---------|-------|-------------|
| Steps | 20 | Inference steps |
| CFG | 3.5 | Guidance scale |
| Resolution | 1920x1080 | Output size |
| Sampler | DPM++ 2M SDE | Sampling method |
| Scheduler | Karras | Noise schedule |

---

## Next Steps

1. **Install ComfyUI** using preferred method
2. **Download Flux Turbo model** (FP8 version recommended)
3. **Download Turbo LoRA** from Hugging Face
4. **Start ComfyUI server** and verify it's running
5. **Test single generation** by loading workflow in UI
6. **Run batch generator** with sample prompts
7. **Customize prompts.json** for your needs

---

## Resources

- **ComfyUI GitHub:** https://github.com/comfyanonymous/ComfyUI
- **Flux Turbo Model:** https://huggingface.co/black-forest-labs/FLUX.1-turbo
- **Hyper-SD LoRA:** https://huggingface.co/ByteDance/Hyper-SD
- **ComfyUI Documentation:** https://docs.comfy.org
- **Workflow Sharing:** https://comfyworkflows.com

---

## Support

For issues specific to this batch generator:
1. Check this guide's Troubleshooting section
2. Verify all files are in place
3. Ensure ComfyUI server is accessible
4. Check `generation.log` for detailed errors

For ComfyUI issues:
- GitHub Issues: https://github.com/comfyanonymous/ComfyUI/issues
- Discord: https://discord.gg/comfyui

---

**Happy Generating!**

Generated for TrueNAS Infrastructure Project
