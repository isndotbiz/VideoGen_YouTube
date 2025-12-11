# ElevenLabs API Key Permission Error - FIX GUIDE

## Problem
```
Error: 401 Unauthorized
Message: "The API key you used is missing the permission text_to_speech to execute this operation."
```

## Diagnosis
Your current API key (`sk_1d468f1e09ecc177b...`) is valid but **lacks text_to_speech permissions**.

This happens when:
- API key was generated with limited/restricted scopes
- Key is from a limited access tier
- Key permissions were revoked or restricted

## Solution: Regenerate API Key with Full Permissions

### Step 1: Go to ElevenLabs Dashboard
https://elevenlabs.io/app/settings/api-keys

### Step 2: Delete the Current Key
- Click the trash/delete icon next to your current key
- Confirm deletion

### Step 3: Create New API Key
Click **"Create new API key"**

**IMPORTANT**: When creating, ensure you have these scopes selected:
- [x] text_to_speech (REQUIRED)
- [x] voices.read
- [x] models.read
- [x] tts.all (if available)
- [x] All permissions (if "select all" option available)

### Step 4: Copy New Key
```
sk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 5: Update Your .env File
```bash
# Edit: .env
ELEVENLABS_API_KEY=sk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 6: Test the New Key
```bash
python elevenlabs_narration_WORKING.py
```

You should see:
```
2025-12-10 11:06:18,781 - ElevenLabs client initialized
2025-12-10 11:06:18,781 - Script extracted: 2300 characters
2025-12-10 11:06:19,012 - Generating narration...
...
SUCCESS: Narration saved to output/narration.mp3
```

---

## Why This Happens

ElevenLabs API v2.0 uses **scope-based permissions** for security. Each API key is created with specific permissions:

- **text_to_speech**: Generate audio from text (what we need)
- **voices.read**: List available voices
- **models.read**: Access model information
- **audio.edit**: Edit/process audio
- **etc.**

Your current key is missing the `text_to_speech` scope, so the API rejects the request.

---

## Quick Fix Commands

After regenerating your key, update and test:

```bash
# 1. Update .env with new key
nano .env  # or edit in your text editor

# 2. Test immediately
python elevenlabs_narration_WORKING.py

# 3. If successful, run full pipeline
python run_video_pipeline.py
```

---

## Verification

Once you have the new key, this command should work:

```bash
python -c "
from elevenlabs import ElevenLabs
import os
from dotenv import load_dotenv

load_dotenv()
client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))

# Try to list voices (minimal permission check)
voices = client.voices.get_all()
print(f'SUCCESS: Found {len(voices)} voices')
print('Your API key has text_to_speech permissions!')
"
```

Expected output:
```
SUCCESS: Found 99 voices
Your API key has text_to_speech permissions!
```

---

## Status After Fix

Once you regenerate the key and update .env:

- ✓ Phase 1: Image generation (DONE - 21 images ready)
- ⏳ Phase 2: Narration generation (WILL WORK after key fix)
- ⏳ Phase 3: Video assembly (needs narration first)
- ⏳ Phase 4: YouTube upload (final step)

Total time to narration working: **5 minutes** (key generation + copy/paste)

---

## Need Help?

If you don't see "Create new API key" button:
1. Check your account tier (free tier may have limitations)
2. Contact ElevenLabs support
3. Check account settings for API key restrictions

---

**Action Required**: Generate new API key with text_to_speech scope
