# How to Use ELEVENLABS_CLEAN_NARRATION_30SEC.txt

## The File

**File:** `ELEVENLABS_CLEAN_NARRATION_30SEC.txt`

**What It Contains:**
- Just plain text
- Only the words ElevenLabs should read
- 165 words exactly
- NO instructions
- NO pause markers
- NO formatting characters
- NO asterisks, hashes, brackets

**What To Do:**
1. Open the file
2. Copy ALL the text
3. Paste it into ElevenLabs API
4. Select voice: Rachel (21m00Tcm4TlvDq8ikWAM)
5. Select model: eleven_turbo_v2
6. Click generate
7. Save MP3 file as narration.mp3

---

## Using With ElevenLabs Python

```python
from elevenlabs.client import ElevenLabs

# Read the clean narration file
with open('ELEVENLABS_CLEAN_NARRATION_30SEC.txt', 'r') as f:
    script = f.read()

# Initialize ElevenLabs
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

print("✓ Narration created: narration.mp3")
```

---

## Using With ElevenLabs Web Interface

1. Go to: https://elevenlabs.io/app/text-to-speech
2. Select Voice: **Rachel**
3. Paste the text from: `ELEVENLABS_CLEAN_NARRATION_30SEC.txt`
4. Click: **Generate**
5. Download MP3 file
6. Save as: `narration.mp3`

---

## That's It!

Just:
- Copy text from file
- Paste into ElevenLabs
- Generate
- Done ✓

No instructions. No pauses. No formatting. Just pure narration text.
