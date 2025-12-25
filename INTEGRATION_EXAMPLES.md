# Script Cleaning Integration Examples

Quick copy-paste examples for integrating script cleaning into your code.

## Example 1: Basic Integration (Minimal)

Replace this in your narration generator:
```python
# BEFORE - Sends cues to TTS!
script = "Get script somehow..."
audio = client.generate(text=script, voice="Rachel")

# AFTER - Clean first
from script_cleaner_for_tts import clean_script_for_tts
script = "Get script somehow..."
clean_script = clean_script_for_tts(script)
audio = client.generate(text=clean_script, voice="Rachel")
```

**That's literally all you need to do!**

---

## Example 2: With Validation (Recommended)

```python
from script_cleaner_for_tts import ScriptCleaner

# Get your script
script = "Your script with [VISUAL] cues here..."

# Clean it
cleaned = ScriptCleaner.clean_text(script)

# Validate
validation = ScriptCleaner.validate_cleaned_text(script, cleaned)
if not validation['is_valid']:
    print(f"WARNING: {validation['remaining_brackets']} patterns still found!")
else:
    print(f"✓ Cleaned {validation['cues_found']} cues")

# Send to ElevenLabs
audio = client.generate(text=cleaned, voice="Rachel")
```

---

## Example 3: Full Pipeline

```python
from script_cleaner_for_tts import ScriptCleaner
from pathlib import Path

def generate_narration_clean(script_path, output_path):
    # 1. Read script
    with open(script_path) as f:
        raw_script = f.read()

    # 2. Find cues (optional - for logging)
    cues = ScriptCleaner.find_cues(raw_script)
    print(f"Found {len(cues)} cues to remove")

    # 3. Clean
    clean_script = ScriptCleaner.clean_text(raw_script, verbose=True)

    # 4. Validate
    validation = ScriptCleaner.validate_cleaned_text(raw_script, clean_script)
    assert validation['is_valid'], "Cleaning failed!"

    # 5. Save cleaned version
    Path("output").mkdir(exist_ok=True)
    with open("output/cleaned_script.txt", 'w') as f:
        f.write(clean_script)

    # 6. Generate narration
    from elevenlabs import ElevenLabs
    client = ElevenLabs(api_key="your_key")

    audio = client.text_to_speech.convert(
        text=clean_script,
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_multilingual_v2"
    )

    # 7. Save audio
    with open(output_path, 'wb') as f:
        for chunk in audio:
            f.write(chunk)

    print(f"✓ Narration saved to {output_path}")
    print(f"✓ Cleaned script saved")

# Usage
generate_narration_clean(
    "VIDEO_SCRIPTS_ALL_VARIATIONS.md",
    "output/narration.mp3"
)
```

---

## Example 4: Batch Processing

```python
from script_cleaner_for_tts import ScriptCleaner
from pathlib import Path

# Clean all scripts in a directory
script_dir = Path("scripts")
output_dir = Path("cleaned_scripts")
output_dir.mkdir(exist_ok=True)

for script_file in script_dir.glob("*.md"):
    print(f"Cleaning {script_file.name}...")

    ScriptCleaner.clean_file(
        str(script_file),
        output_path=str(output_dir / script_file.name)
    )

print(f"✓ Cleaned {len(list(output_dir.glob('*.md')))} scripts")
```

---

## Example 5: Existing Code Updates

### Update `claude_codex_narration_generator.py`

**Current code (lines 28-94):**
```python
def clean_text_for_narration(text: str) -> str:
    """
    Clean and prepare text for TTS narration.
    """
    logger.info("Cleaning text for narration...")
    # ... lots of regex code ...
```

**Replace with:**
```python
def clean_text_for_narration(text: str) -> str:
    """
    Clean and prepare text for TTS narration.
    """
    from script_cleaner_for_tts import clean_script_for_tts
    logger.info("Cleaning text for narration...")
    return clean_script_for_tts(text, verbose=True)
```

Then update line 271:
```python
# OLD:
clean_text = clean_text_for_narration(raw_text)

# NEW: (same, but now uses our better cleaner)
clean_text = clean_text_for_narration(raw_text)
```

---

### Update `optimized_narration_generator.py`

**Current code (lines 14-63):**
```python
def generate_narration():
    api_key = os.getenv("ELEVENLABS_API_KEY")

    with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
        content = f.read()

    script = content[200:2500]  # ← RAW TEXT WITH CUES!

    audio_generator = elevenlabs_client.generate(
        api_key=api_key,
        text=script,  # ← SENDS CUES TO TTS!
        ...
    )
```

**Fix it:**
```python
def generate_narration():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    from script_cleaner_for_tts import clean_script_for_tts

    with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
        content = f.read()

    raw_script = content[200:2500]
    script = clean_script_for_tts(raw_script)  # ← CLEAN FIRST!

    audio_generator = elevenlabs_client.generate(
        api_key=api_key,
        text=script,  # ← NOW SENDS CLEAN TEXT!
        ...
    )
```

---

## Example 6: Update to `tts_generator.py`

**Current code (line 79-95):**
```python
async def generate_audio(self, text: str, voice_id: Optional[str] = None,
                       output_filename: Optional[str] = None) -> Path:
    """
    Generate audio from text
    """
    voice_id = voice_id or self.voice_id

    logger.info(f"Generating audio with voice {voice_id}: '{text[:100]}...'")

    # Prepare request payload
    payload = {
        "text": text,  # ← RAW TEXT WITH CUES!
        ...
    }
```

**Fix it:**
```python
async def generate_audio(self, text: str, voice_id: Optional[str] = None,
                       output_filename: Optional[str] = None) -> Path:
    """
    Generate audio from text
    """
    from script_cleaner_for_tts import clean_script_for_tts

    voice_id = voice_id or self.voice_id

    # Clean text before sending to API
    text = clean_script_for_tts(text)

    logger.info(f"Generating audio with voice {voice_id}: '{text[:100]}...'")

    # Prepare request payload
    payload = {
        "text": text,  # ← NOW CLEAN TEXT!
        ...
    }
```

---

## Example 7: Test Your Integration

After updating your code, test it:

```python
# test_script_cleaning.py
from script_cleaner_for_tts import ScriptCleaner

# Test script with cues
test_script = """
[VISUAL: Title card appears]
"Welcome to the video!"
[PAUSE: 2 seconds]
"Let's get started."
[TIME: 00:30]
"Thanks for watching!"
[END]
"""

# Run cleaner
cleaned = ScriptCleaner.clean_text(test_script)
print("Cleaned:", cleaned)

# Validate
validation = ScriptCleaner.validate_cleaned_text(test_script, cleaned)
print("Valid:", validation['is_valid'])
print("Cues removed:", validation['cues_found'])

assert validation['is_valid'], "FAILED: Cues remain!"
print("✓ TEST PASSED")
```

Run it:
```bash
python test_script_cleaning.py
```

Expected output:
```
Cleaned:
"Welcome to the video!"

"Let's get started."

"Thanks for watching!"

Valid: True
Cues removed: 5
✓ TEST PASSED
```

---

## Example 8: Debugging

If cleaning doesn't work as expected:

```python
from script_cleaner_for_tts import ScriptCleaner

script = "Your problematic script..."

# Step 1: Find what cues exist
cues = ScriptCleaner.find_cues(script)
print(f"Found {len(cues)} cues:")
for cue_text, pos, pattern in cues:
    print(f"  Position {pos}: {cue_text[:50]}")

# Step 2: Clean
cleaned = ScriptCleaner.clean_text(script, verbose=True)

# Step 3: Check what remains
remaining = ScriptCleaner.find_cues(cleaned)
if remaining:
    print(f"ERROR: {len(remaining)} cues remain after cleaning!")
    for cue_text, pos, pattern in remaining:
        print(f"  Pattern: {pattern}")
        print(f"  Text: {cue_text}")
else:
    print("✓ All cues removed successfully!")
```

---

## Checklist for Integration

- [ ] Copy `script_cleaner_for_tts.py` to your project root
- [ ] Update your narration generator imports
- [ ] Add `clean_script_for_tts()` call before sending to ElevenLabs
- [ ] Test with your actual scripts
- [ ] Verify no cues in generated audio
- [ ] Update any other TTS code that sends scripts
- [ ] Commit the changes

---

## Performance Tips

If you're cleaning many scripts:

```python
# Good: Clean once, use many times
clean_script = clean_script_for_tts(script)
audio1 = generate_with_voice(clean_script, "Rachel")
audio2 = generate_with_voice(clean_script, "Adam")

# Avoid: Cleaning the same script multiple times
audio1 = generate_with_voice(clean_script_for_tts(script), "Rachel")  # Cleaned here
audio2 = generate_with_voice(clean_script_for_tts(script), "Adam")    # Cleaned again!
```

---

## Need More Help?

1. **For basic usage**: See `SCRIPT_CLEANING_GUIDE.md`
2. **For API reference**: See `script_cleaner_for_tts.py` docstrings
3. **To test**: Run `python script_cleaner_for_tts.py`
4. **Full pipeline**: Run `python elevenlabs_with_script_cleaning.py`
