# ElevenLabs Implementation Guide for VideoGen

## Complete Guide to Using ElevenLabs TTS with Proper Pauses and Timing

---

## 1. PROBLEM: Asterisks and Formatting in Narration

### Previous Issue
The current narration script includes formatting characters that get read aloud:
```
* ChatGPT - advanced AI tool
* Midjourney - image generation
# Section headers
```

When ElevenLabs TTS reads this, it says:
**"Asterisk ChatGPT dash advanced AI tool"** ❌ WRONG

### Solution: Clean Script Format
Remove ALL formatting characters before sending to ElevenLabs:
```
Welcome to ChatGPT, an advanced AI tool.
Next we have Midjourney for image generation.
```

When ElevenLabs TTS reads this:
**"Welcome to ChatGPT, an advanced AI tool"** ✓ CORRECT

---

## 2. ELEVENLABS API IMPLEMENTATION

### 2.1 Python Client Setup

```python
from elevenlabs.client import ElevenLabs

# Initialize client
client = ElevenLabs(api_key="YOUR_API_KEY")

# Convert text to speech
audio = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel - professional voice
    model_id="eleven_turbo_v2",        # Fast, natural sounding
    text="Your clean script here",
    voice_settings={
        "stability": 0.5,              # 0.0-1.0 (lower = more variation/emotion)
        "similarity_boost": 0.75       # 0.0-1.0 (higher = more consistent)
    }
)

# Save to MP3 file
with open("narration.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### 2.2 Key Parameters Explained

| Parameter | Value | Purpose | Range |
|-----------|-------|---------|-------|
| voice_id | 21m00Tcm4TlvDq8ikWAM | Rachel voice | Various |
| model_id | eleven_turbo_v2 | Fast/natural | eleven_monolingual_v1, eleven_turbo_v2 |
| stability | 0.5 | Natural variation | 0.0-1.0 |
| similarity_boost | 0.75 | Voice consistency | 0.0-1.0 |

### 2.3 Voice Options

**Rachel (21m00Tcm4TlvDq8ikWAM)** - Professional, clear (RECOMMENDED)
```
"Meet Claude, a powerful AI assistant"
→ Clear, professional tone
```

**Chris (iP3nJ5ADw2WC8gRTKzadsA)** - Friendly, conversational
```
"Check out Midjourney for amazing images"
→ Friendly, approachable tone
```

**Bella (EXAVITQu4vr4xnSDxMaL)** - Warm, engaging
```
"Let's explore these incredible tools"
→ Warm, enthusiastic tone
```

---

## 3. CREATING PROPER SCRIPTS FOR ELEVENLABS

### 3.1 Clean Script Formatting Rules

✓ DO: Use clean, natural language
```
Welcome to the 8 best free AI tools. These tools will transform your workflow.
ChatGPT is an advanced language model that helps with writing and coding.
Midjourney generates stunning images from text descriptions.
```

✗ DON'T: Use formatting characters
```
* ChatGPT - advanced AI
# Why Use These Tools
[Narrator: Pause for effect]
**Bold text** for emphasis
```

### 3.2 Handling Pauses

ElevenLabs interprets punctuation as natural pauses:

```python
# Natural pauses using punctuation
script = """
Welcome to the 8 best free AI tools.

First, ChatGPT.

This tool helps you write and code.

Next, Midjourney.

Generate images from text.
"""
```

**Pause Lengths (Automatic):**
- Period (.) = 0.3 seconds
- Comma (,) = 0.1 seconds
- Question mark (?) = 0.5 seconds
- Exclamation (!) = 0.4 seconds
- Paragraph break = 1.0 seconds

### 3.3 Script Length Calculation

**For 30-second video:**
- Speaking pace: 5.5 words/second (normal speed)
- Available time: 30 seconds
- Total words: 30 × 5.5 = 165 words

**For 60-second video:**
- Total words: 60 × 5.5 = 330 words

**For 120-second video:**
- Total words: 120 × 5.5 = 660 words

### 3.4 Example: Clean 30-Second Script

```python
clean_script_30_seconds = """
Welcome to the 8 best free AI tools that will transform how you work. These
powerful tools will save you time and boost your productivity. Let's dive in.

First, we have ChatGPT. This advanced AI writes code, answers questions, and
creates content in seconds.

Next is Midjourney. Generate stunning images from text prompts. Perfect for
creators and designers.

ElevenLabs brings your text to life with natural sounding voices. Create
professional narration instantly.

Meet Claude. A powerful AI assistant for analysis, writing, and problem solving.

Synthesys AI creates realistic AI avatars that speak naturally. Perfect for
video content.

Runway is the creative suite for video generation and editing powered by AI.

Zapier connects your favorite tools and automates workflows without code.

Finally, CapCut makes video editing simple with powerful AI-powered editing
features.

Start using these tools today. Transform your creative workflow now.
"""

# This is exactly 165 words = 30 seconds at 5.5 wps
```

---

## 4. IMPLEMENTATION: COMPLETE EXAMPLE

### 4.1 Full Python Script

```python
#!/usr/bin/env python3
"""Generate clean 30-second narration for video"""

import os
from elevenlabs.client import ElevenLabs
from datetime import datetime

# Load API key from environment
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Clean script with proper formatting (NO ASTERISKS!)
CLEAN_SCRIPT = """
Welcome to the 8 best free AI tools that will transform how you work. These
powerful tools will save you time and boost your productivity. Let's dive in.

First, we have ChatGPT. This advanced AI writes code, answers questions, and
creates content in seconds.

Next is Midjourney. Generate stunning images from text prompts. Perfect for
creators and designers.

ElevenLabs brings your text to life with natural sounding voices. Create
professional narration instantly.

Meet Claude. A powerful AI assistant for analysis, writing, and problem solving.

Synthesys AI creates realistic AI avatars that speak naturally. Perfect for
video content.

Runway is the creative suite for video generation and editing powered by AI.

Zapier connects your favorite tools and automates workflows without code.

Finally, CapCut makes video editing simple with powerful AI-powered editing
features.

Start using these tools today. Transform your creative workflow now.
"""

def generate_narration(script, output_file="narration_clean.mp3"):
    """Generate narration from clean script using ElevenLabs"""

    print(f"[{datetime.now()}] Generating narration...")
    print(f"Script length: {len(script)} characters")
    print(f"Estimated word count: {len(script.split())} words")

    try:
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        # Generate speech
        print("Calling ElevenLabs API...")
        audio = client.text_to_speech.convert(
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
            model_id="eleven_turbo_v2",        # Fast and natural
            text=script.strip(),               # Remove extra whitespace
            voice_settings={
                "stability": 0.5,              # Natural variation
                "similarity_boost": 0.75       # Voice consistency
            }
        )

        # Save to file
        output_path = os.path.join("output", output_file)
        os.makedirs("output", exist_ok=True)

        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        # Get file stats
        file_size_mb = os.path.getsize(output_path) / 1024 / 1024

        print(f"[{datetime.now()}] ✓ Narration generated successfully!")
        print(f"File: {output_path}")
        print(f"Size: {file_size_mb:.2f} MB")

        return output_path

    except Exception as e:
        print(f"[ERROR] Failed to generate narration: {e}")
        raise

if __name__ == "__main__":
    generate_narration(CLEAN_SCRIPT)
```

### 4.2 Running the Script

```bash
# Set API key
export ELEVENLABS_API_KEY="your_api_key_here"

# Run script
python generate_narration_clean.py

# Output:
# [2025-12-16 10:30:45] Generating narration...
# Script length: 1047 characters
# Estimated word count: 165 words
# Calling ElevenLabs API...
# [2025-12-16 10:30:48] ✓ Narration generated successfully!
# File: output/narration_clean.mp3
# Size: 2.31 MB
```

---

## 5. TIMING AND SYNCHRONIZATION

### 5.1 Audio Timing with Video

```
Video Timeline (30 seconds)
├─ 0-5s: Introduction + Title card
├─ 5-8s: ChatGPT animation
├─ 8-11s: Midjourney animation
├─ 11-14s: ElevenLabs animation
├─ 14-17s: Claude animation
├─ 17-20s: Synthesys animation
├─ 20-23s: Runway animation
├─ 23-26s: Zapier animation
├─ 26-29s: CapCut animation
└─ 29-30s: Outro/Credits

Audio Timeline (same)
├─ 0-5s: "Welcome to 8 AI tools..."
├─ 5-8s: "First, ChatGPT..."
├─ 8-11s: "Next, Midjourney..."
├─ 11-14s: "ElevenLabs brings..."
├─ 14-17s: "Meet Claude..."
├─ 17-20s: "Synthesys AI..."
├─ 20-23s: "Runway is..."
├─ 23-26s: "Zapier connects..."
├─ 26-29s: "CapCut makes..."
└─ 29-30s: "Start using..."
```

### 5.2 Verifying Timing with FFprobe

```bash
# Check narration duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 narration_clean.mp3

# Output should be close to 30 seconds:
# 30.248

# If it's off, adjust script length:
# - Too long (>31s): Remove sentences
# - Too short (<29s): Add sentences
```

---

## 6. INTEGRATING WITH VIDEO COMPOSITION

### 6.1 Shotstack Integration

```json
{
  "timeline": {
    "tracks": [
      {
        "clips": [
          // Video clips (animations)
        ]
      },
      {
        "clips": [
          {
            "type": "audio",
            "asset": {
              "type": "audio",
              "src": "s3://bucket/narration_clean.mp3"
            },
            "start": 0,
            "length": 30,
            "volume": 1.0
          }
        ]
      }
    ]
  }
}
```

### 6.2 FFmpeg Integration

```bash
# Mix narration with background music at 40% volume
ffmpeg \
  -i animation.mp4 \
  -i narration_clean.mp3 \
  -i background_music.mp3 \
  -filter_complex "[1:a][2:a]amix=inputs=2:duration=first[aout]" \
  -map 0:v \
  -map "[aout]" \
  -c:v libx264 \
  -c:a aac \
  output.mp4
```

---

## 7. VOICE SETTINGS GUIDE

### 7.1 Stability Settings

**Low Stability (0.0-0.3):** More variation, emotional
```
"ChatGPT is AMAZING! It completely transforms how you work!"
→ More dramatic, emotional delivery
```

**Medium Stability (0.4-0.6):** Balanced
```
"ChatGPT is an advanced AI tool that helps with writing and coding."
→ Natural, conversational tone (RECOMMENDED for educational content)
```

**High Stability (0.7-1.0):** Consistent, monotone
```
"Meet Claude, a powerful AI assistant."
→ Consistent, professional tone (good for formal content)
```

### 7.2 Similarity Boost Settings

**Low Similarity (0.0-0.3):** Varied, dynamic
```
→ Voice changes tone and rhythm throughout
```

**Medium Similarity (0.6-0.8):** Balanced consistency
```
→ Maintains voice identity while sounding natural (RECOMMENDED)
```

**High Similarity (0.9-1.0):** Very consistent
```
→ Voice stays very similar across all text
```

### 7.3 Recommended Settings by Content Type

| Content Type | Stability | Similarity | Voice |
|---|---|---|---|
| Educational | 0.5 | 0.75 | Rachel |
| Marketing | 0.3 | 0.7 | Bella |
| Technical | 0.7 | 0.8 | Chris |
| Entertainment | 0.4 | 0.6 | Bella |
| YouTube Videos | 0.5 | 0.75 | Rachel |

---

## 8. QUALITY CHECKLIST

### Before Uploading Video

```
✓ Script has NO asterisks, hashes, or formatting
✓ Script word count: 165 words for 30s (±10 words)
✓ Narration duration: 30 seconds (±0.5s)
✓ Audio quality: 44.1 kHz, Stereo
✓ File format: MP3 or WAV
✓ No background noise in narration
✓ Volume level: Not too loud or quiet (-20dB to -10dB)
✓ Timing matches animations (narration changes sync with video cuts)
✓ No spoken artifacts (um, uh, repeated words)
✓ Professional tone maintained throughout
```

---

## 9. COST CALCULATION

**ElevenLabs Pricing:**
- **Free tier:** 10,000 characters/month
- **Paid tier:** $5/month (100,000 characters/month)

**For 30-second narration:**
- Characters: ~1,000
- Cost: ~$0.03

**For 100 videos per month:**
- Total characters: 100,000
- Cost: ~$3/month

---

## 10. TROUBLESHOOTING

### Issue: Narration sounds robotic

**Cause:** Stability too high
**Solution:** Lower stability to 0.4-0.5

### Issue: Narration is too quiet

**Cause:** Volume level too low
**Solution:** Increase audio volume in FFmpeg or Shotstack

### Issue: Asterisks are being read as "asterisk"

**Cause:** Formatting characters in script
**Solution:** Remove all *, #, @, [, ], (, ), {, } from script

### Issue: Narration is too fast or too slow

**Cause:** Script too short or too long
**Solution:** Adjust script length to target word count

### Issue: Speech sounds unnatural between sentences

**Cause:** Missing punctuation or paragraph breaks
**Solution:** Add periods and blank lines between major sections

---

## 11. FINAL CLEAN SCRIPT TEMPLATE

Use this template for any clean script:

```python
clean_script_template = """
[INTRO - 5 seconds]
Opening statement that hooks the viewer.

[SECTION 1 - 3 seconds per animation]
Information about first tool or concept.

[SECTION 2 - 3 seconds per animation]
Information about second tool or concept.

[SECTION 3 - 3 seconds per animation]
Information about third tool or concept.

[OUTRO - 1 second]
Call to action or closing statement.
"""

# Rules:
# 1. No asterisks, hashes, or brackets in actual script
# 2. Comments only for timing reference
# 3. Use periods for natural pauses
# 4. Blank lines between major sections
# 5. Keep word count: 165 words for 30 seconds
```

---

## SUMMARY

✓ Use **clean scripts** with NO formatting characters
✓ Let **punctuation** handle natural pauses (. , ? !)
✓ Use **Rachel voice** with stability 0.5, similarity 0.75
✓ Target **5.5 words/second** speaking pace
✓ Match **narration duration** to video duration exactly
✓ Verify **no asterisks** or special characters are read aloud
✓ Test with **ffprobe** to confirm audio length

**Result:** Professional, natural-sounding narration for your videos! 🎬
