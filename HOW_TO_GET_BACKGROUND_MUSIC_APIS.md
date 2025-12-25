# How to Get Background Music APIs - Step-by-Step Guide

## OPTION 1: EASIEST & FREE - YouTube Audio Library
**No API needed - Direct download from YouTube**

### Steps:
1. Go to: https://www.youtube.com/audiolibrary
2. Sign in with your Google account
3. Search for "uplifting" or "motivational"
4. Download MP3 file directly
5. Save to: `background_music/uplifting_motivational.mp3`

**Pros:**
- 100% FREE
- No API key required
- YouTube-approved (safe for monetization)
- Perfect for your video
- Takes 2 minutes

**Cons:**
- Manual download (not automated)
- Limited to YouTube Music only

**BEST FOR:** Immediate use, no coding needed

---

## OPTION 2: FAST & FREE - FreePD.com
**Direct downloads, no API**

### Steps:
1. Go to: https://freepd.com/?s=motivational
2. Filter by mood: "Motivational" or "Uplifting"
3. Click any track
4. Click "Free Download" button (green)
5. Save MP3 file to: `background_music/`

**Example Tracks:**
- "Inspiring" - 7:30 duration
- "Success" - Perfect for wealth video
- "Opportunity" - High energy

**Pros:**
- 100% FREE
- Commercial use OK
- High quality tracks
- Lots of categories
- No signup needed

**Cons:**
- Manual download
- Limited automation

**BEST FOR:** Quick start, high-quality free music

---

## OPTION 3: FREE WITH API - Pexels Videos
**Free API, commercial use OK, 200 requests/hour**

### How to Get API Key:
1. Go to: https://www.pexels.com/api/
2. Scroll down to "Get Started"
3. Click "Register API Key"
4. Sign up (free account)
5. Create API key
6. Copy your API key

### Setup in Your Code:
```python
# Option A: Set as environment variable
import os
os.environ['PEXELS_API_KEY'] = 'your_api_key_here'

# Option B: Use in script directly
api_key = 'your_api_key_here'
headers = {'Authorization': api_key}
```

### Usage Example:
```python
import requests

api_key = 'your_pexels_api_key'
response = requests.get(
    'https://api.pexels.com/videos/',
    params={
        'query': 'uplifting motivational',
        'per_page': 10
    },
    headers={'Authorization': api_key}
)

videos = response.json()['videos']
for video in videos:
    print(f"Music: {video['user']['name']}")
    print(f"Duration: {video['duration']} seconds")
```

**Pros:**
- Completely FREE
- Commercial use OK
- Automatic API access
- Programmable
- 200 requests/hour (plenty)

**Cons:**
- Requires free signup
- Need API key in code

**BEST FOR:** Automated background music selection

---

## OPTION 4: GOOD QUALITY FREE - Pixabay
**Free tier with API, commercial use OK**

### How to Get API Key:
1. Go to: https://pixabay.com/api/docs/
2. Click "Get Started"
3. Create free account
4. Go to Dashboard
5. Copy your API key

### Usage:
```python
import requests

api_key = 'your_pixabay_key'
response = requests.get(
    'https://pixabay.com/api/',
    params={
        'key': api_key,
        'q': 'uplifting motivational',
        'type': 'music',
        'per_page': 10
    }
)

music = response.json()['hits']
for track in music:
    print(f"Track: {track['previewURL']}")
```

**Pros:**
- Free tier available
- Good quality music
- Commercial use OK
- 50 requests/hour (free tier)
- Easy to use

**Cons:**
- Lower rate limit than Pexels
- Need signup

**BEST FOR:** Alternative to Pexels

---

## OPTION 5: PREMIUM BUT AFFORDABLE - Epidemic Sound
**$9.99/month, API access, unlimited tracks**

### How to Get:
1. Go to: https://www.epidemicsound.com/
2. Click "Subscribe"
3. Choose "Free Trial" or "$9.99/month"
4. Create account
5. Go to API Docs: https://www.epidemicsound.com/api/
6. Generate API token

### Setup:
```python
import requests

api_key = 'your_epidemic_sound_token'
headers = {'Authorization': f'Bearer {api_key}'}

response = requests.get(
    'https://www.epidemicsound.com/api/search/tracks/',
    params={
        'query': 'uplifting motivational',
        'length': 450  # 7.5 minutes in seconds
    },
    headers=headers
)

tracks = response.json()['results']
```

**Pros:**
- Huge music library (50,000+ tracks)
- Professional quality
- Full API support
- Monthly subscription ($9.99)
- Easy to filter by mood/duration

**Cons:**
- $9.99/month cost
- Overkill if just starting

**BEST FOR:** Serious production, scaling

---

## OPTION 6: PREMIUM - Artlist.io
**$14.99/month, AI-powered, unlimited**

### How to Get:
1. Go to: https://www.artlist.io/
2. Click "Free Trial" (7 days)
3. Create account
4. Go to "Settings" → "API"
5. Generate API key

### Benefits:
- 100,000+ music tracks
- AI-powered search
- Excellent quality
- Easy API integration
- 10GB downloads/month

**Cost:** $14.99/month (with free 7-day trial)

---

## MY RECOMMENDATION FOR YOUR PROJECT

### SHORT TERM (Start Now - FREE):
**Use YouTube Audio Library:**
1. Go to https://www.youtube.com/audiolibrary
2. Search "uplifting" or "motivational"
3. Download one track (2 minutes)
4. Save as: `background_music/uplifting_motivational.mp3`
5. Done! Ready to use in video pipeline

**This works immediately with your fix_video_complete.py:**
```python
music_path = "background_music/uplifting_motivational.mp3"
add_background_music(narration_path, output_path, music_volume=0.15)
```

### MEDIUM TERM (Scale Up - Still Free):
**Get Pexels API key (5 minutes):**
1. Go to https://www.pexels.com/api/
2. Sign up (free)
3. Create API key
4. Use in your Python script for automatic music selection
5. Still $0 cost

### LONG TERM (Professional - $10/month):
**Get Epidemic Sound subscription ($9.99/month):**
- Only if you're making 10+ videos/month
- Professional quality
- Easiest API to use
- Best for YouTube channel growth

---

## QUICK START (NEXT 5 MINUTES)

### For Your Free AI Tools Video:

```bash
# Step 1: Download one track manually from YouTube Audio Library
# (Go to https://www.youtube.com/audiolibrary, download "Inspiring" track)

# Step 2: Save it here:
mkdir background_music
# Copy downloaded file to: background_music/uplifting_motivational.mp3

# Step 3: Update your video pipeline
# Edit fix_video_complete.py, add this after narration:

def add_background_music_to_pipeline(narration_path, bg_music_path, output_path):
    from moviepy.editor import AudioFileClip, CompositeAudioClip

    # Load files
    narration = AudioFileClip(narration_path)
    music = AudioFileClip(bg_music_path)

    # Trim music to match narration duration
    if music.duration < narration.duration:
        # Loop if needed
        pass
    else:
        music = music.subclip(0, narration.duration)

    # Mix: Music at 15% + Narration at 100%
    music = music.volume_proc(lambda t: 0.15)
    final_audio = CompositeAudioClip([music, narration])

    # Export
    final_audio.write_audiofile(output_path, verbose=False, logger=None)
    return output_path

# Step 4: Run it
add_background_music_to_pipeline(
    "output/narration_free_ai_tools.mp3",
    "background_music/uplifting_motivational.mp3",
    "output/narration_with_bgm.mp3"
)
```

---

## SETTING UP PEXELS API (Slightly More Advanced)

If you want automatic background music selection:

### 1. Get API Key:
```
1. Visit: https://www.pexels.com/api/
2. Click "Register API Key"
3. Create free account
4. Your API key appears in dashboard
5. Copy it
```

### 2. Set Environment Variable (Windows):
```bash
# In Command Prompt:
setx PEXELS_API_KEY "your_api_key_here"

# Verify it works:
echo %PEXELS_API_KEY%
```

### 3. Use in Python:
```python
import os
import requests

# Get API key from environment
api_key = os.getenv('PEXELS_API_KEY')

# Search for music
response = requests.get(
    'https://api.pexels.com/videos/',
    params={
        'query': 'uplifting motivational',
        'per_page': 5,
        'page': 1
    },
    headers={'Authorization': api_key}
)

videos = response.json()['videos']

# Download first video
for video in videos:
    for file in video['video_files']:
        if file['type'] == 'video/mp4':
            # Download the video/audio
            url = file['link']
            r = requests.get(url)
            with open('background_music/pexels_track.mp4', 'wb') as f:
                f.write(r.content)
            print("Downloaded!")
            break
    break
```

---

## COMPARISON TABLE

| Service | Cost | Signup | API | Quality | Best For |
|---------|------|--------|-----|---------|----------|
| **YouTube Audio Library** | FREE | YouTube account | No | Good | Quick start |
| **FreePD** | FREE | No signup | No | Excellent | Manual downloads |
| **Pexels** | FREE | Free account | Yes | Good | Automated selection |
| **Pixabay** | FREE | Free account | Yes | Good | Alternative API |
| **Epidemic Sound** | $9.99/mo | Yes | Yes | Excellent | Serious production |
| **Artlist** | $14.99/mo | Yes | Yes | Excellent | Premium quality |

---

## NEXT STEPS FOR YOUR VIDEO

1. **Right Now:** Download 1 track from YouTube Audio Library (2 min)
2. **Save it:** `background_music/uplifting_motivational.mp3`
3. **Add to video:** Update `fix_video_complete.py` with 10 lines of code
4. **Done:** Background music will mix automatically

**No API key needed for step 1.**

If you want to automate it, get Pexels API key (free, 5 minutes).

---

## DO THIS RIGHT NOW (FREE START)

```bash
# 1. Create music folder
mkdir background_music

# 2. Go here and download:
# https://www.youtube.com/audiolibrary
# Search: "motivational" or "uplifting"
# Download one MP3

# 3. Save to:
# background_music/uplifting_motivational.mp3

# 4. Update your Python code with the mixing function above

# 5. Run your pipeline:
# python fix_video_complete.py
```

That's it! **No API keys, no cost, works in 5 minutes.**

