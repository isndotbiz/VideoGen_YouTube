# Use This File for ElevenLabs

## The File You Need

**File:** `ELEVENLABS_CLEAN_NARRATION_30SEC.txt`

**Location:** `D:\workspace\VideoGen_YouTube\ELEVENLABS_CLEAN_NARRATION_30SEC.txt`

---

## What's In It

Just plain text. Only words. Nothing else.

```
Welcome to the 8 best free AI tools that will transform how you work. These powerful tools will save you time and boost your productivity. Let's dive in. First, we have ChatGPT. This advanced AI writes code, answers questions, and creates content in seconds. Next is Midjourney. Generate stunning images from text prompts. Perfect for creators and designers. ElevenLabs brings your text to life with natural sounding voices. Create professional narration instantly. Meet Claude. A powerful AI assistant for analysis, writing, and problem solving. Synthesys AI creates realistic AI avatars that speak naturally. Perfect for video content. Runway is the creative suite for video generation and editing powered by AI. Zapier connects your favorite tools and automates workflows without code. Finally, CapCut makes video editing simple with powerful AI-powered editing features. Start using these tools today. Transform your creative workflow now.
```

---

## How to Use

### Option 1: Using Python Script (Easiest)
```bash
cd D:\workspace\VideoGen_YouTube
python create_30_second_video_clean.py
```

The script automatically:
1. Reads `ELEVENLABS_CLEAN_NARRATION_30SEC.txt`
2. Sends it to ElevenLabs API
3. Generates narration.mp3 (30 seconds)
4. Saves the file

**Done!** You have your narration.

---

### Option 2: Using ElevenLabs Web Interface (Manual)

1. Go to: https://elevenlabs.io/app/text-to-speech
2. Open: `ELEVENLABS_CLEAN_NARRATION_30SEC.txt`
3. Copy ALL the text
4. Paste into ElevenLabs text box
5. Select Voice: **Rachel** (21m00Tcm4TlvDq8ikWAM)
6. Select Model: **eleven_turbo_v2**
7. Click: **Generate**
8. Download and save as: **narration.mp3**

**Done!** You have your narration.

---

### Option 3: Using ElevenLabs Python Directly (Advanced)

```python
from elevenlabs.client import ElevenLabs

# Read the clean script
with open('ELEVENLABS_CLEAN_NARRATION_30SEC.txt', 'r') as f:
    script = f.read()

# Create ElevenLabs client
client = ElevenLabs(api_key="YOUR_API_KEY")

# Generate speech
audio = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
    model_id="eleven_turbo_v2",
    text=script,
    voice_settings={
        "stability": 0.5,
        "similarity_boost": 0.75
    }
)

# Save to file
with open("narration.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

print("✓ Narration created!")
```

---

## That's It

- **No instructions** to read
- **No pause markers** to follow
- **No formatting** to interpret
- **Just plain words** for ElevenLabs to read

Copy the text. Paste it. Generate. Done.

---

## File Stats

- **Words:** 165
- **Duration:** 30 seconds (at 5.5 wps)
- **Formatting:** NONE
- **Asterisks:** NONE
- **Instructions:** NONE
- **Pauses:** Natural (commas, periods)
- **Ready for:** ElevenLabs API only

---

**That's your narration file. Use it.**
