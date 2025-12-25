# ElevenLabs Script Cleaning - Deployment Guide

## Quick Deploy (5 Minutes)

### Step 1: Copy Files (1 minute)
Copy these files to your project:
- `script_cleaner_for_tts.py` (core module)
- `elevenlabs_with_script_cleaning.py` (optional: full pipeline)

### Step 2: Test Installation (1 minute)
```bash
python script_cleaner_for_tts.py
```

Expected output:
```
ORIGINAL SCRIPT: [shows test script]
FOUND CUES: [shows 20 cues found]
CLEANED SCRIPT: [shows clean text]
VALIDATION: original_length=504, cleaned_length=230, is_valid=True
READY FOR TTS? YES
```

### Step 3: Update Your Code (3 minutes)

Find your narration generation code. It probably looks like:

**File: `optimized_narration_generator.py` or `claude_codex_narration_generator.py`**

```python
# CURRENT CODE (line ~20-30)
def generate_narration():
    with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
        content = f.read()

    script = content[200:2500]

    audio_generator = elevenlabs_client.generate(
        api_key=api_key,
        text=script,  # ← PROBLEM: Has cues!
        ...
    )
```

**Replace with:**

```python
def generate_narration():
    from script_cleaner_for_tts import clean_script_for_tts  # ← ADD THIS

    with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
        content = f.read()

    script = content[200:2500]
    script = clean_script_for_tts(script)  # ← ADD THIS LINE

    audio_generator = elevenlabs_client.generate(
        api_key=api_key,
        text=script,  # ← Now clean!
        ...
    )
```

That's it! Just **2 lines added** (import + cleaning call).

---

## Full Deployment Checklist

### Phase 1: Preparation (5 minutes)
- [ ] Copy `script_cleaner_for_tts.py` to project root
- [ ] Run test: `python script_cleaner_for_tts.py`
- [ ] Verify output: "READY FOR TTS? YES"

### Phase 2: Code Update (15 minutes)

Find all locations where scripts are sent to ElevenLabs:

1. **Find files**
   ```bash
   grep -r "elevenlabs\|generate.*text\|text_to_speech" --include="*.py"
   ```

2. **Update each file**
   - Add import: `from script_cleaner_for_tts import clean_script_for_tts`
   - Add cleaning: `script = clean_script_for_tts(script)` before API call

3. **Files to update:**
   - [ ] `optimized_narration_generator.py` (if using)
   - [ ] `claude_codex_narration_generator.py` (if using)
   - [ ] `video_pipeline/generators/tts_generator.py` (if using)
   - [ ] Any custom TTS generation code

### Phase 3: Testing (10 minutes)
- [ ] Run each updated script
- [ ] Generate test narration
- [ ] Listen to output for any spoken cues
- [ ] Verify no `[VISUAL]`, `[PAUSE]`, etc. in audio
- [ ] Check logs show cleaning happened

### Phase 4: Validation (5 minutes)
- [ ] Generate full narration with your script
- [ ] Compare old (bad) vs new (good) audio
- [ ] Confirm professional quality
- [ ] Verify no cues spoken

### Phase 5: Documentation (5 minutes)
- [ ] Update your project README
- [ ] Document where cleaning is applied
- [ ] Add note about script format requirements

### Phase 6: Commit (2 minutes)
- [ ] Stage changes: `git add script_cleaner_for_tts.py`
- [ ] Commit message: "Add script cleaning before ElevenLabs TTS"
- [ ] Push: `git push`

---

## Files Updated by Deployment

### If Using Standard Pipeline

1. **optimized_narration_generator.py**
   ```python
   # Line 8 (after imports)
   from script_cleaner_for_tts import clean_script_for_tts

   # Line 30 (in generate_narration function)
   script = clean_script_for_tts(content[200:2500])
   ```

2. **video_pipeline/generators/tts_generator.py**
   ```python
   # Line 5 (after imports)
   from script_cleaner_for_tts import clean_script_for_tts

   # Line 100 (in generate_audio method)
   text = clean_script_for_tts(text)
   ```

3. **Any custom TTS code**
   - Add import
   - Add cleaning call before API

### If Using Full Pipeline

Run the included integrated version:
```bash
python elevenlabs_with_script_cleaning.py
```

This automatically:
- Extracts script
- Cleans cues
- Validates
- Generates narration

---

## Verification Steps

### Step 1: Verify Module Works
```bash
python script_cleaner_for_tts.py
```

Check output:
- ✓ Test script shown
- ✓ 20 cues found
- ✓ Cleaned script shown
- ✓ "READY FOR TTS? YES"

### Step 2: Test With Your Scripts
```python
from script_cleaner_for_tts import clean_script_for_tts, ScriptCleaner

# Read your actual script
with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
    script = f.read()

# Clean it
cleaned = clean_script_for_tts(script)

# Validate
validation = ScriptCleaner.validate_cleaned_text(script, cleaned)
print(f"Cues found and removed: {validation['cues_found']}")
print(f"Valid: {validation['is_valid']}")

# Optional: Check what was removed
cues = ScriptCleaner.find_cues(script)
print(f"First 5 cues removed:")
for cue_text, pos, _ in cues[:5]:
    print(f"  - {cue_text[:50]}")
```

### Step 3: Generate Test Narration
```python
from script_cleaner_for_tts import clean_script_for_tts
from elevenlabs import ElevenLabs

with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
    script = f.read()[200:2500]

# Clean before sending
clean_script = clean_script_for_tts(script)

# Generate
client = ElevenLabs(api_key="your_key")
audio = client.text_to_speech.convert(
    text=clean_script,
    voice_id="21m00Tcm4TlvDq8ikWAM"
)

# Save
with open("test_narration.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### Step 4: Listen to Output
- Play `test_narration.mp3`
- Listen for any spoken cues
- Should only hear actual script, no "[VISUAL]" or "[PAUSE]"

---

## Rollback Plan

If something goes wrong:

### Immediate (2 minutes)
1. Remove the cleaning call from your code
2. Revert to original narration generation
3. Run the old code to regenerate

### Full Rollback (5 minutes)
```bash
git revert <commit_hash>
git push
```

This undoes all changes.

---

## Integration Patterns

### Pattern 1: Simple Integration
**Best for:** Small projects, single TTS call

```python
from script_cleaner_for_tts import clean_script_for_tts

# Before ElevenLabs API
clean_text = clean_script_for_tts(raw_text)
audio = generate_with_elevenlabs(clean_text)
```

### Pattern 2: Full Pipeline
**Best for:** Large projects, multiple scripts

```python
python elevenlabs_with_script_cleaning.py
# Handles everything automatically
```

### Pattern 3: With Validation
**Best for:** Critical production, need assurance

```python
from script_cleaner_for_tts import ScriptCleaner

cleaned = ScriptCleaner.clean_text(script)
validation = ScriptCleaner.validate_cleaned_text(script, cleaned)
assert validation['is_valid'], "Cleaning failed!"
audio = generate_with_elevenlabs(cleaned)
```

---

## Performance Expectations

| Operation | Time | Notes |
|-----------|------|-------|
| Clean 100-word script | <10ms | Instantaneous |
| Clean 1000-word script | <50ms | Still fast |
| Validate cleaned text | <10ms | Negligible overhead |
| Full ElevenLabs generation | 30-60s | No change from before |

**Total overhead:** <100ms (negligible)

---

## Troubleshooting During Deployment

### Issue: "ModuleNotFoundError: No module named 'script_cleaner_for_tts'"

**Solution:** Copy `script_cleaner_for_tts.py` to same directory as your code.

Verify:
```bash
ls -la script_cleaner_for_tts.py
python -c "import script_cleaner_for_tts"
```

### Issue: "Some bracket patterns remain"

**Solution:** Check the log for what patterns remain, add them to `CUE_PATTERNS`.

Debug:
```python
from script_cleaner_for_tts import ScriptCleaner
cues = ScriptCleaner.find_cues(your_script)
for cue_text, pos, pattern in cues:
    print(f"Pattern: {pattern}\nText: {cue_text}\n")
```

### Issue: "Text too short after cleaning"

**Solution:** Your script extraction is too aggressive or script is too short.

Check:
```python
with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
    content = f.read()
print(f"Total file: {len(content)} chars")
print(f"Slice [200:2500]: {len(content[200:2500])} chars")
```

Adjust slice as needed.

### Issue: Cues still spoken in audio

**Solution:** Cleaning didn't work or old code still being used.

Verify:
```python
from script_cleaner_for_tts import clean_script_for_tts
test = "[VISUAL: test]"
cleaned = clean_script_for_tts(test)
print(f"Original: {test}")
print(f"Cleaned: {cleaned}")
assert "[VISUAL" not in cleaned
```

---

## Success Criteria

Deployment is successful when:

- ✓ Module imports without errors
- ✓ Test script cleans properly
- ✓ Updated code runs without errors
- ✓ Generated audio plays
- ✓ NO spoken cues in audio
- ✓ Audio quality is professional

---

## Post-Deployment

### Monitor (First Week)
- Listen to generated narration regularly
- Watch logs for errors
- Verify consistent quality

### Maintain (Ongoing)
- Keep `script_cleaner_for_tts.py` up to date
- Use `SCRIPT_CLEANING_GUIDE.md` as reference
- Share with team if collaborative

### Improve (Optional)
- Add new cue patterns if needed
- Integrate into CI/CD pipeline
- Document your script format

---

## Support Resources

If you need help:

1. **Quick Reference**: `SCRIPT_CLEANING_QUICK_REFERENCE.txt`
2. **Full Guide**: `SCRIPT_CLEANING_GUIDE.md`
3. **Code Examples**: `INTEGRATION_EXAMPLES.md`
4. **Full Overview**: `SOLUTION_SUMMARY.md`
5. **Test Module**: `python script_cleaner_for_tts.py`

---

## Timeline

Typical deployment timeline:

| Phase | Time | Tasks |
|-------|------|-------|
| Preparation | 5 min | Copy files, test |
| Code Update | 10 min | Update 1-3 files |
| Testing | 10 min | Generate test audio |
| Validation | 5 min | Listen and verify |
| Documentation | 5 min | Update README |
| Commit | 2 min | Git commit/push |
| **Total** | **37 min** | **Full deployment** |

---

## After Deployment

Your narration will be:
- ✓ Professional (no spoken cues)
- ✓ Clean (only actual script)
- ✓ High-quality (same as before, just better)
- ✓ Ready for video (can compose immediately)

You're done! Your TTS now generates perfect narration.

---

## Questions?

Refer to documentation in this order:
1. This file (deployment)
2. `SOLUTION_SUMMARY.md` (overview)
3. `SCRIPT_CLEANING_QUICK_REFERENCE.txt` (quick answers)
4. `SCRIPT_CLEANING_GUIDE.md` (detailed)
5. `INTEGRATION_EXAMPLES.md` (code)

---

**Status:** READY TO DEPLOY
**Estimated Time:** 30-45 minutes
**Difficulty:** EASY (copy 1 file, update 1 function)
**Risk:** LOW (easy to rollback)
