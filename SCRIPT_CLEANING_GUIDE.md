# ElevenLabs Script Cleaning Guide

## Problem
Your video scripts contain production cues that should NOT be spoken by the TTS system:
- `[VISUAL: ...]` - Visual direction
- `[PAUSE: ...]` - Timing instructions
- `[TIME: ...]` - Timestamp markers
- `[LINK: ...]` - URL references
- `[AWARD: ...]` - Achievement cues
- `[EMPHASIS: ...]` - Emphasis markers
- `[OK]`, `[DONE]` - Status cues
- And many others

When sent to ElevenLabs as-is, the AI reads these aloud, creating unprofessional narration.

## Solution
Two Python modules handle complete script cleaning:

### 1. `script_cleaner_for_tts.py` - Core Cleaning Engine
Removes ALL cues and annotations from scripts.

**Main function:**
```python
from script_cleaner_for_tts import clean_script_for_tts

clean_text = clean_script_for_tts(raw_script)
```

**Comprehensive cue removal:**
- Visual/production cues: `[VISUAL]`, `[PAUSE]`, `[B-ROLL]`, `[AUDIO]`, `[MUSIC]`, etc.
- Timing cues: `[TIME]`, `[TIMESTAMP]`, `[CUT]`
- Navigation cues: `[LINK]`, `[URL]`
- Interaction cues: `[AWARD]`, `[OK]`, `[ACK]`, `[DONE]`, `[END]`, `[START]`
- Any `[WORD]` or `[WORD: content]` patterns
- Timestamp markers: `(HH:MM-HH:MM)`, `(HH:MM)`

### 2. `elevenlabs_with_script_cleaning.py` - Integrated Narration Generator
Complete narration pipeline with automatic script cleaning.

**Features:**
- Extracts script from markdown files
- Identifies all cues before cleaning
- Cleans text completely
- Validates cleaned text (ensures no cues remain)
- Generates professional narration with ElevenLabs
- Saves both audio and metadata

## Quick Start

### Option A: Just Clean Text
```python
from script_cleaner_for_tts import clean_script_for_tts

with open("my_script.txt") as f:
    raw_text = f.read()

clean_text = clean_script_for_tts(raw_text)

# Now send to ElevenLabs
```

### Option B: Full Pipeline (Recommended)
```bash
python elevenlabs_with_script_cleaning.py
```

This handles:
1. Script extraction
2. Cue detection and reporting
3. Complete cleaning
4. Validation
5. Narration generation
6. Metadata saving

## Integration with Your Existing Code

### Before: Problem Code
```python
def generate_narration():
    with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
        script = f.read()[200:2500]  # Raw text with cues!

    audio = client.generate(
        text=script,  # This includes [VISUAL], [PAUSE], etc!
        voice="Rachel"
    )
```

### After: Fixed Code
```python
from script_cleaner_for_tts import clean_script_for_tts

def generate_narration():
    with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
        raw_script = f.read()[200:2500]

    # Clean before sending to ElevenLabs
    clean_script = clean_script_for_tts(raw_script)

    audio = client.generate(
        text=clean_script,  # No more cues!
        voice="Rachel"
    )
```

## How It Works

### The Cleaning Process
1. **Find all cues** using 20+ regex patterns
2. **Remove each cue** pattern
3. **Clean whitespace** (normalize spacing, remove empty lines)
4. **Validate result** (ensure no bracket patterns remain)

### Cue Pattern Coverage

#### Visual/Production Cues
```
[VISUAL: Fade in title card]         → Removed
[PAUSE: 2 seconds]                   → Removed
[EMPHASIS: important point]          → Removed
[B-ROLL: show some footage]          → Removed
[AUDIO: background music fades in]   → Removed
[MUSIC: upbeat electronic]           → Removed
[SOUND: whoosh effect]               → Removed
[SFX: explosion]                     → Removed
[ANIMATION: zoom in]                 → Removed
[TRANSITION: fade]                   → Removed
[ON-SCREEN: text overlay]            → Removed
```

#### Timing Cues
```
[TIME: 00:30]                        → Removed
[TIMESTAMP: 1:45]                    → Removed
(0:30-1:00)                          → Removed
(2:15)                               → Removed
```

#### Navigation Cues
```
[LINK: https://example.com]          → Removed
[URL: https://example.com]           → Removed
[CUT: to scene B]                    → Removed
```

#### Interaction Cues
```
[AWARD: Best Tool]                   → Removed
[OK]                                 → Removed
[DONE]                               → Removed
[START]                              → Removed
[END]                                → Removed
```

## API Reference

### ScriptCleaner Class

#### `clean_text(text, verbose=False) -> str`
Remove all cues from text.
```python
from script_cleaner_for_tts import ScriptCleaner

cleaned = ScriptCleaner.clean_text(raw_text)
```

#### `clean_file(input_path, output_path=None, verbose=False) -> str`
Clean a script file and optionally save result.
```python
cleaned = ScriptCleaner.clean_file(
    "input.md",
    output_path="cleaned.txt",
    verbose=True
)
```

#### `find_cues(text) -> List[Tuple]`
Find all cues in text without removing them (auditing).
```python
cues = ScriptCleaner.find_cues(raw_text)
for cue_text, position, pattern in cues:
    print(f"Found: {cue_text} at position {position}")
```

#### `validate_cleaned_text(original, cleaned) -> dict`
Verify cleaning was successful.
```python
results = ScriptCleaner.validate_cleaned_text(original, cleaned)
print(f"Cues removed: {results['cues_found']}")
print(f"Remaining brackets: {results['remaining_brackets']}")
print(f"Valid: {results['is_valid']}")
```

### Convenience Function

```python
from script_cleaner_for_tts import clean_script_for_tts

clean_text = clean_script_for_tts(script, verbose=True)
```

## Testing

### Test the Cleaning Module
```bash
python script_cleaner_for_tts.py
```

Output shows:
- Original script with cues
- All detected cues
- Cleaned script
- Validation results

### Test Full Pipeline
```bash
python elevenlabs_with_script_cleaning.py
```

Generates:
- Audio narration: `output/narration_cleaned.mp3`
- Cleaned script: `output/narration_script_cleaned.txt`
- Metadata: `output/narration_metadata.txt`

## Integration Checklist

- [ ] Copy `script_cleaner_for_tts.py` to your project
- [ ] Copy `elevenlabs_with_script_cleaning.py` to your project
- [ ] Update your narration generation code to use cleaning
- [ ] Test with your scripts
- [ ] Verify no cues are spoken in generated audio
- [ ] Update your pipeline to include cleaning step

## Common Use Cases

### Use Case 1: Clean Before Sending to API
```python
from script_cleaner_for_tts import clean_script_for_tts

def my_narration_function(script):
    clean_script = clean_script_for_tts(script)
    return generate_with_elevenlabs(clean_script)
```

### Use Case 2: Find What Will Be Removed
```python
from script_cleaner_for_tts import ScriptCleaner

cues = ScriptCleaner.find_cues(script)
print(f"Will remove {len(cues)} cues")
```

### Use Case 3: Validate Cleaning
```python
from script_cleaner_for_tts import ScriptCleaner

validation = ScriptCleaner.validate_cleaned_text(original, cleaned)
assert validation['is_valid'], "Cleaning failed!"
```

### Use Case 4: Batch Clean Multiple Scripts
```python
from script_cleaner_for_tts import ScriptCleaner
from pathlib import Path

for script_file in Path("scripts/").glob("*.md"):
    ScriptCleaner.clean_file(
        str(script_file),
        output_path=f"cleaned/{script_file.name}"
    )
```

## Troubleshooting

### Issue: "Remaining bracket patterns found!"
This means some `[...]` patterns weren't matched.

**Solution:**
1. Check what patterns remain: Look at the warning log
2. Add pattern to `CUE_PATTERNS` in `script_cleaner_for_tts.py`
3. Test with `ScriptCleaner.find_cues()`
4. Update and retry

### Issue: "Text too short after cleaning"
Not enough actual narration text in script.

**Solution:**
1. Verify your script extraction is correct
2. Check that you're not removing too much
3. Look at `output/narration_script_cleaned.txt` to see what remains

### Issue: "ElevenLabs API key missing"
API credentials not configured.

**Solution:**
1. Create `.env` file with: `ELEVENLABS_API_KEY=your_key_here`
2. Or: `export ELEVENLABS_API_KEY=your_key_here`
3. Verify with: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ELEVENLABS_API_KEY'))"`

## Performance

- **Cleaning speed**: <100ms for typical scripts (< 10,000 words)
- **Text extraction**: <50ms
- **Validation**: <50ms
- **ElevenLabs generation**: 30-60 seconds (depends on length)

## Files

| File | Purpose |
|------|---------|
| `script_cleaner_for_tts.py` | Core cleaning engine - use this |
| `elevenlabs_with_script_cleaning.py` | Full pipeline - use this for complete workflow |
| `SCRIPT_CLEANING_GUIDE.md` | This guide |

## Next Steps

1. **Test immediately**: `python script_cleaner_for_tts.py`
2. **Integrate into pipeline**: Add to your narration generation
3. **Verify audio**: Listen for any remaining cues
4. **Deploy**: Use in production

## Questions?

Check these in order:
1. Run the test: `python script_cleaner_for_tts.py`
2. Check validation output
3. Review logs in `narration_generation.log`
4. Verify script format matches examples in this guide
