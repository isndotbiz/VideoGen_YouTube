# Automated Video Generation Pipeline - Setup Guide

Complete setup for automated video creation from start to finish.

## 🚀 Quick Setup (15 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Copy Environment Template
```bash
cp .env.example .env
```

### 3. Get API Keys (details below)

### 4. Run Setup Script
```bash
python setup_apis.py
```
The script will:
- Prompt for each API key
- Test connections
- Save credentials to .env
- Create config.json

### 5. Verify Setup
```bash
python setup_apis.py --test
```

---

## 📋 API Keys - Where to Get Them

### FAL.ai (Flux Image Generation)
1. Go to: https://fal.ai/dashboard/keys
2. Sign up if needed
3. Copy your API Key
4. Paste into setup script

**Free Tier:** 100 API calls/month
**Cost after:** $0.001 per image generation

### ElevenLabs (Text-to-Speech)
1. Go to: https://elevenlabs.io/app/settings/api-keys
2. Sign up if needed
3. Copy your API Key
4. Paste into setup script

**Free Tier:** 10,000 characters/month
**Cost after:** Starter plan $5/month (up to 100k chars)

### Shotstack (Video Assembly)
1. Go to: https://dashboard.shotstack.io/settings/api-key
2. Sign up if needed
3. Copy your API Key
4. Paste into setup script

**Free Tier:** 20 credits/month (1 credit = 1 minute video)
**Cost after:** $0.20 per minute video

### YouTube (Publishing)
1. Go to: https://console.cloud.google.com
2. Create new project: "Video Pipeline"
3. Enable APIs:
   - YouTube Data API v3
4. Create OAuth 2.0 credentials:
   - Application type: Desktop application
5. Download JSON file
6. Copy Client ID and Client Secret
7. Paste into setup script

**Free Tier:** 10,000 units/day (≈6 videos/day)

### ComfyUI (Local Image Generation)
1. Install ComfyUI: https://github.com/comfyanonymous/ComfyUI
2. Install Flux Turbo model
3. Install Turbo LoRA
4. Start ComfyUI: `python main.py`
5. Default: http://localhost:8188

**Cost:** Free (runs locally)

---

## 🛠️ ComfyUI Setup (Optional but Recommended)

### For Fastest Local Generation:

```bash
# 1. Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download Flux Turbo model
# Place in: ComfyUI/models/checkpoints/flux-turbo.safetensors
# Download from: Hugging Face (requires account)

# 4. Download Turbo LoRA
# Place in: ComfyUI/models/loras/flux_turbo_lora.safetensors

# 5. Start ComfyUI server
python main.py --listen 0.0.0.0 --port 8188

# Server now running at: http://localhost:8188
```

---

## ✅ Verify Your Setup

### Test Each Component:
```bash
# Test FAL.ai
python -c "from fal_client import client; print('✓ FAL.ai OK')"

# Test ElevenLabs
python -c "from elevenlabs import client; print('✓ ElevenLabs OK')"

# Test Shotstack
python -c "import requests; print('✓ Requests OK')"

# Test ComfyUI connection
curl http://localhost:8188/api/auth
```

### Test Full Setup:
```bash
python setup_apis.py --test
```

Expected output:
```
✓ FAL.ai API key valid
✓ ElevenLabs API key valid
✓ Shotstack API key valid
✓ YouTube credentials configured
✓ ComfyUI server reachable
```

---

## 🚀 Running the Pipeline

### Full Pipeline (All Phases):
```bash
python video_pipeline.py \
  --prompts prompts.json \
  --script "VIDEO_SCRIPTS_ALL_VARIATIONS.md" \
  --title "Claude Code vs Codex: Why I Use Both" \
  --output ./output
```

### Individual Phases:

**Generate Images Only:**
```bash
python video_pipeline.py --phase images --prompts prompts.json
```

**Generate Narration Only:**
```bash
python video_pipeline.py --phase narration --script "script.txt"
```

**Assemble Video Only:**
```bash
python video_pipeline.py --phase assembly --images ./images --audio narration.mp3
```

**Upload to YouTube Only:**
```bash
python video_pipeline.py --phase upload --video video.mp4 --title "My Video"
```

---

## 📊 Cost Estimate (Per Video)

| Component | Cost | Notes |
|-----------|------|-------|
| FAL.ai (21 images) | ~$0.03 | $0.001 per image |
| ElevenLabs (TTS) | ~$0.02 | For ~2000 chars |
| Shotstack (17 min) | $3.40 | $0.20 per minute |
| YouTube | FREE | 10k units/day |
| **TOTAL** | **~$3.45** | Per complete video |

For bulk (100 videos/month):
- FAL.ai: ~$10-20
- ElevenLabs: ~$5-22 (Starter plan)
- Shotstack: ~$40 (200 credits)
- YouTube: Free
- **Total: ~$60-85/month**

---

## 🔐 Security Best Practices

### Protect Your Credentials:
1. **Never commit .env to git**
   ```bash
   # Add to .gitignore:
   .env
   .env.local
   *.env
   ```

2. **Use strong API keys**
   - Regenerate if compromised
   - Rotate quarterly

3. **Limit API key permissions**
   - YouTube: Only upload, not delete
   - Shotstack: Only render, not manage

4. **Separate dev/prod credentials**
   - Use .env.local for development
   - Use environment variables for production

---

## 🐛 Troubleshooting

### "API key invalid"
- Verify key was copied correctly
- Check API key hasn't been revoked
- Regenerate key in service dashboard
- Re-run: `python setup_apis.py`

### "ComfyUI server not reachable"
- Ensure ComfyUI is running: `python main.py`
- Check port 8188 is accessible
- Verify URL in .env: `http://localhost:8188`

### "Video assembly takes too long"
- Shotstack processes 1-2 minutes per minute of video
- 17-minute video takes ~30 minutes
- You can continue working while it renders

### "YouTube upload fails"
- Ensure OAuth credentials are correct
- First upload requires browser authentication
- Check YouTube quota: https://console.cloud.google.com

---

## 📚 Next Steps

1. **Copy .env.example → .env**
2. **Get API keys** (see section above)
3. **Run: python setup_apis.py**
4. **Run: python video_pipeline.py --help**
5. **Generate your first video!**

---

## ℹ️ More Information

- [FAL.ai Docs](https://docs.fal.ai)
- [ElevenLabs API](https://elevenlabs.io/docs/api-reference)
- [Shotstack Docs](https://shotstack.io/docs/api/)
- [YouTube API Docs](https://developers.google.com/youtube/v3)
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)

---

**Ready to automate video creation? Let's go!** 🎬
