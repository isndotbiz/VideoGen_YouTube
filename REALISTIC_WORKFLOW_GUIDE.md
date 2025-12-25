# REALISTIC 2-Shot Workflow (What Actually Works)

**IMPORTANT DISCOVERY:** Epidemic Sound's AI search **CANNOT** filter by:
- Volume consistency / dynamic range
- Bass drops / buildups
- Waveform characteristics
- Audio engineering specs

It **CAN ONLY** filter by:
- Genre
- BPM
- Mood
- Vocals (yes/no)
- Instrument type

---

## ✅ WHAT ACTUALLY WORKS

### Step 1: Use PROMPT 1 Only (Genre/BPM/Mood Search)

**Example:**
```
High-energy tech videos with voiceover. Electronic instrumental (chillstep,
minimal techno). 110-130 BPM. Energetic but background-friendly. Modern,
futuristic. No vocals.
```

This gives you 10-50 tracks matching the basic criteria.

### Step 2: Download ALL Candidates (or Sample 10-15)

Download the top 10-15 tracks that look promising.

### Step 3: Analyze with Automated Tools

**Run the volume consistency analyzer:**
```bash
python volume_consistency_analyzer.py --directory background_music_epidemic/
```

**Or use the optimal clip finder:**
```bash
python optimal_clip_finder.py track1.wav
```

This will give you:
- RMS standard deviation (< 2.0 dB = excellent)
- Dynamic range
- Best sections for extraction
- Volume consistency scores

### Step 4: Filter Based on Analysis Results

Keep only tracks with:
- RMS std dev < 2.5 dB (good) or < 1.5 dB (excellent)
- Low speech frequency conflict (< 30%)
- Minimal silence gaps
- Consistent energy scores

---

## 🎯 REVISED PROMPT STRATEGY

Instead of "2-shot prompts", use **"Search + Analyze" workflow**:

### The 10 Prompts (PROMPT 1 Only)

Use these for initial search. IGNORE PROMPT 2 (it doesn't work):

1. **Energy/Consistency:** "High-energy tech videos with voiceover. Electronic instrumental (chillstep, minimal techno). 110-130 BPM. Energetic but background-friendly."

2. **Genre/Technical:** "Electronic instrumental for tech tutorials. Chillstep, minimal techno, synthwave. 110-130 BPM. Clean production."

3. **Use Case/Audio:** "Background for AI tech tutorials with narration. Energetic electronic instrumental. Chillstep, minimal techno. 110-130 BPM."

4. **Simple:** "Instrumental electronic for tech background. Chillstep or minimal techno. 110-130 BPM. Energetic but background-friendly."

5. **Cinematic:** "Cinematic instrumental for documentaries. Modern orchestral, epic ambient, atmospheric. 60-90 BPM. No vocals."

6. **Upbeat:** "Upbeat motivational for business videos. Corporate pop, indie folk, uplifting electronic. 120-140 BPM. Instrumental."

7. **Calm:** "Extremely calm meditation music. Ambient, soft piano, acoustic guitar. 40-70 BPM. Instrumental. Tranquil."

8. **Corporate:** "Professional corporate for presentations. Soft tech, light corporate pop, minimal piano. 90-110 BPM. Instrumental."

9. **Vlog:** "Casual vlog music. Acoustic, indie, lo-fi hip hop. 80-120 BPM. Instrumental. Warm, authentic."

10. **Gaming:** "High-energy gaming music. Synthwave, trap, dubstep, electronic rock. 130-160 BPM. Mostly instrumental."

---

## 📊 PRACTICAL WORKFLOW

### Method 1: Download First, Analyze Later

```bash
# 1. Use PROMPT 1 to search
# 2. Download 10-15 promising tracks manually
# 3. Run analysis
python volume_consistency_analyzer.py --input background_music_epidemic/

# 4. Check results - keep tracks with RMS std dev < 2.5 dB
```

### Method 2: Use Epidemic's Built-in Filters

After searching with PROMPT 1, use Epidemic's UI filters:

**Available Filters:**
- ✅ BPM (exact range)
- ✅ Mood (Calm, Energetic, Happy, etc.)
- ✅ Genre (Electronic, Corporate, Ambient, etc.)
- ✅ Instruments (Piano, Guitar, Synth, etc.)
- ✅ Vocals (Instrumental only)
- ✅ Duration (30s, 1min, 2min, etc.)

**NOT Available:**
- ❌ Volume consistency
- ❌ Dynamic range
- ❌ Bass drops
- ❌ Waveform characteristics

### Method 3: Use "Similar Tracks" Feature

1. Find ONE perfect track manually
2. Click "Similar Tracks" on Epidemic
3. Download the similar tracks
4. They'll have similar characteristics

---

## 🔧 AUTOMATED ANALYSIS TOOLS

### Tool 1: Volume Consistency Analyzer
```bash
python volume_consistency_analyzer.py --input track.wav
```

**Output:**
- RMS std deviation (target: < 2.0 dB)
- LUFS range (target: < 3 LU)
- Best sections for extraction
- Consistency score

### Tool 2: Optimal Clip Finder
```bash
python optimal_clip_finder.py track.wav --duration 180
```

**Output:**
- Best 3-minute section
- Energy consistency score
- Speech frequency conflict
- Overall suitability score

### Tool 3: Music Curation Analyzer
```bash
python music_curation_analyzer.py --directory background_music_epidemic/
```

**Output:**
- Scores all tracks in directory
- Ranks by consistency
- Identifies best tracks for voiceover

---

## ✅ REALISTIC EXPECTATIONS

### What Epidemic's AI CAN Do:
- Find tracks by genre, BPM, mood
- Filter by instruments, vocals
- Suggest similar tracks
- Provide good starting candidates

### What Epidemic's AI CANNOT Do:
- Filter by volume consistency
- Identify bass drops or buildups
- Analyze waveform characteristics
- Measure dynamic range

### What YOU Must Do:
- Listen to tracks and manually judge
- Use automated analysis tools
- Test tracks in your videos
- Build a library of proven winners

---

## 🎯 RECOMMENDED WORKFLOW

### Step 1: Search with Smart Prompt (2 minutes)
Use PROMPT 1 from your chosen style:
```
Professional corporate for presentations. Soft tech, light corporate pop,
minimal piano. 90-110 BPM. Instrumental. Clean, modern.
```

### Step 2: Apply Epidemic Filters (1 minute)
- BPM: 90-110
- Vocals: Instrumental
- Mood: Calm, Professional, Peaceful
- Genre: Corporate, Ambient

### Step 3: Download Top 10 Tracks (20 minutes)
Download 10 candidates that sound promising.

### Step 4: Batch Analyze (5 minutes)
```bash
python volume_consistency_analyzer.py --directory background_music_epidemic/
```

### Step 5: Keep Best 3-5 Tracks (1 minute)
Filter results:
- Keep: RMS std dev < 2.5 dB
- Keep: No obvious buildups/drops when listening
- Discard: Everything else

### Step 6: Test in Video (10 minutes)
Use your top 3 tracks in actual videos to confirm they work.

**Total Time:** ~40 minutes to find 3-5 perfect tracks

---

## 📝 SIMPLIFIED PROMPTS (What Actually Matters)

Since PROMPT 2 doesn't work, here are optimized single prompts:

### For Tech/Tutorial Videos:
```
Electronic instrumental background music for tech tutorials with voiceover.
Chillstep, minimal techno, or ambient electronic. 110-130 BPM. Clean, modern,
consistent energy. No vocals. Background-friendly production.
```

### For Corporate/Business:
```
Professional corporate background music for business presentations with narration.
Minimal piano, soft tech, light ambient. 90-110 BPM. Clean, unobtrusive,
trustworthy. Instrumental only.
```

### For Calm/Meditation:
```
Ambient meditation music for wellness videos with gentle voice guidance. Soft
piano, ambient pads, acoustic. 50-70 BPM. Extremely minimal, tranquil. Pure
instrumental background.
```

### For Upbeat/Motivational:
```
Upbeat motivational music for business content with voiceover. Indie folk
acoustic, corporate pop, light electronic. 120-130 BPM. Positive, clean,
professional. Instrumental only.
```

---

## 🚀 QUICK START (Realistic Version)

### Fastest Path to Good Background Music:

```bash
# Option 1: Use emergency downloader (no Epidemic needed)
python emergency_music_downloader.py
# → 20 tracks in 5 minutes, analyze later

# Option 2: Search Epidemic + Analyze
1. Search with PROMPT 1 on Epidemic Sound
2. Download 10 promising tracks
3. python volume_consistency_analyzer.py --directory background_music_epidemic/
4. Keep top 3-5 based on RMS std dev scores
```

---

## 💡 KEY INSIGHT

**The "2-shot prompt" is a myth for Epidemic Sound.**

What ACTUALLY works:
1. **Smart Genre/BPM/Mood Search** (PROMPT 1)
2. **Manual listening** OR **Automated analysis tools**
3. **Test in real videos**
4. **Build curated library of winners**

**The analysis tools in this codebase ARE the "PROMPT 2"** - they do the technical filtering that Epidemic's AI cannot.

---

## 📊 TOOL COMPARISON

| Method | Time | Accuracy | Best For |
|--------|------|----------|----------|
| Epidemic AI Search | 2 min | Medium | Initial discovery |
| Manual Listening | 30 min | High | Final selection |
| Automated Analysis | 5 min | High | Batch filtering |
| Test in Video | 10 min | Highest | Validation |

**Recommended:** Use ALL methods in sequence for best results.

---

## ✅ UPDATED DOCUMENTATION

I've updated the following files:
- This file explains what actually works
- MASTER guide will note the limitation
- Use PROMPT 1 only for searches
- Use analysis tools for "PROMPT 2" filtering

**Bottom Line:**
- Epidemic Search = Genre/BPM/Mood filtering
- Your Analysis Tools = Volume/Consistency filtering
- Your Ears = Final judgment

---

**Last Updated:** December 24, 2025
**Status:** Realistic and Actually Works ✅
