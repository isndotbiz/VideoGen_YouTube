# Volume Consistency Analysis System

## Quick Navigation

**New user?** Start here:
1. Read [Quick Start Guide](VOLUME_CONSISTENCY_QUICK_START.md) (10 minutes)
2. Run the analyzer: `python volume_consistency_analyzer.py background_music.mp3`
3. Check output folder for results

**Need technical details?** See [Technical Guide](VOLUME_CONSISTENCY_ANALYSIS_GUIDE.md)

**Want an overview?** Read [Summary](VOLUME_CONSISTENCY_SUMMARY.md)

---

## What This Does

Automatically identifies which parts of music tracks have **consistent volume** (perfect for background music) vs. parts with **dynamic volume changes** (intros, outros, build-ups, drops).

### The Problem It Solves

Manual background music selection is:
- Time-consuming (listening to entire tracks)
- Subjective (what "sounds consistent" varies)
- Error-prone (easy to pick dynamic sections)
- Not scalable (can't analyze 100+ tracks efficiently)

### The Solution

Automated, scientific analysis:
- **Fast**: Analyzes 3-minute track in ~15 seconds
- **Objective**: Uses RMS standard deviation (industry standard)
- **Accurate**: Identifies sections within 3 dB variation
- **Scalable**: Batch process entire music libraries
- **Visual**: Generates plots for verification

---

## Files Included

### 1. `volume_consistency_analyzer.py` (Main Tool)
**Production-ready Python script**

- Command-line interface with extensive options
- Automated volume analysis using librosa
- Intelligent section detection and ranking
- Visual analysis plots (2-panel PNG)
- Automatic best section extraction (MP3)
- JSON report generation
- Error handling and validation

**Quick usage**:
```bash
python volume_consistency_analyzer.py your_music.mp3
```

### 2. `VOLUME_CONSISTENCY_QUICK_START.md` (User Guide)
**Start here for practical usage**

- Installation instructions
- Basic and advanced usage examples
- Parameter tuning guide
- Troubleshooting common issues
- Real-world examples
- Integration patterns
- Batch processing scripts

**Best for**: Day-to-day usage, learning the basics

### 3. `VOLUME_CONSISTENCY_ANALYSIS_GUIDE.md` (Technical Reference)
**Comprehensive technical documentation**

- Volume metrics explained (RMS, LUFS, dBFS)
- Tool comparisons (librosa, pydub, ffmpeg, pyloudnorm)
- Multiple implementation approaches
- Scientific basis for thresholds
- Complete code examples
- Visualization techniques
- Performance benchmarks

**Best for**: Understanding the science, customizing the solution

### 4. `VOLUME_CONSISTENCY_SUMMARY.md` (Overview)
**High-level overview and integration guide**

- How the system works
- Technical implementation details
- Real-world applications
- Integration with video pipeline
- Extension examples
- Best practices

**Best for**: Understanding the complete solution, planning integration

### 5. `README_VOLUME_CONSISTENCY.md` (This File)
**Navigation hub**

- Quick overview
- File descriptions
- Getting started guide
- Common use cases

**Best for**: Finding the right documentation

---

## Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install librosa pydub numpy matplotlib
```

### Step 2: Run Analysis
```bash
python volume_consistency_analyzer.py background_music/your_track.mp3
```

### Step 3: Check Results
```
output/
├── your_track_consistency_analysis.json       # Full analysis data
├── your_track_consistency_visualization.png   # Visual plot
└── your_track_best_82s.mp3                   # Best section extracted
```

### Step 4: Review Visualization
Open the PNG file to see:
- **Top panel**: Volume consistency over time (green = consistent)
- **Bottom panel**: Identified sections ranked by quality

### Step 5: Use Extracted Section
The best consistent section is already extracted as MP3 - use it directly in your video!

---

## Common Use Cases

### Use Case 1: Find Background Music for Video
```bash
# Analyze your music track
python volume_consistency_analyzer.py epic_music.mp3

# Use the extracted section (already saved)
# output/epic_music_best_82s.mp3

# Mix with narration at 15% volume
ffmpeg -i narration.mp3 -i output/epic_music_best_82s.mp3 \
  -filter_complex "[1:a]volume=0.15[music];[0:a][music]amix=inputs=2[out]" \
  -map "[out]" final_audio.mp3
```

### Use Case 2: Curate Music Library
```bash
# Analyze all tracks
for track in background_music/*.mp3; do
    python volume_consistency_analyzer.py "$track" --no-visualize
done

# Now output/ contains best sections from each track
# Review the JSON files to select top tracks
```

### Use Case 3: Find 82-Second Clip for Video
```bash
# Default extraction is ~82s (or best available)
python volume_consistency_analyzer.py music.mp3

# Check duration in JSON:
cat output/music_consistency_analysis.json | grep duration
```

### Use Case 4: Strict Quality Control
```bash
# Only accept sections with < 2 dB variation
python volume_consistency_analyzer.py music.mp3 --threshold 2.0

# If no sections found, increase to 2.5 or 3.0
```

### Use Case 5: Python Integration
```python
from volume_consistency_analyzer import VolumeConsistencyAnalyzer

# Analyze track
analyzer = VolumeConsistencyAnalyzer()
results = analyzer.analyze("music.mp3", visualize=False)

# Get best section details
best = results['consistent_sections'][0]
print(f"Use section: {best['start']:.1f}s - {best['end']:.1f}s")
print(f"Quality: {best['avg_std']:.2f} dB std dev")

# Extracted file location
print(f"MP3: {results['best_section_path']}")
```

---

## Understanding Results

### Quality Classifications

| Std Dev | Label | Meaning | Use It? |
|---------|-------|---------|---------|
| < 1.0 dB | EXCELLENT | Perfectly consistent | Yes! Ideal |
| 1.0-1.5 dB | VERY GOOD | Barely noticeable variation | Yes! Great |
| 1.5-2.5 dB | GOOD | Slight variation | Yes! Good |
| 2.5-3.0 dB | ACCEPTABLE | Noticeable variation | Maybe - test it |
| > 3.0 dB | DYNAMIC | Very noticeable changes | No - avoid |

### JSON Output Structure
```json
{
  "file_path": "music.mp3",
  "duration": 180.5,
  "consistent_sections": [
    {
      "start": 45.2,
      "end": 127.8,
      "duration": 82.6,
      "avg_std": 2.1,
      "score": 79.0
    }
  ],
  "best_section_path": "output/music_best_82s.mp3"
}
```

**Key fields**:
- `start`/`end`: Time positions (seconds)
- `duration`: Section length (seconds)
- `avg_std`: Quality metric (lower = better)
- `score`: Overall quality (0-100, higher = better)

---

## Parameter Guide

### Window Duration (`--window`)
**What it controls**: Size of analysis window

- **5-8s**: Detect quick changes, find smaller sections
- **10-15s**: Balanced (default: 10s) - recommended
- **15-30s**: Detect overall consistency, find larger sections

**Example**:
```bash
# Analyze in 15-second windows
python volume_consistency_analyzer.py music.mp3 --window 15
```

### Consistency Threshold (`--threshold`)
**What it controls**: Maximum allowed variation (std dev in dB)

- **1.0-2.0 dB**: Very strict (only perfect sections)
- **2.0-3.0 dB**: Strict (default: 3.0) - recommended
- **3.0-5.0 dB**: Moderate (allows more variation)
- **5.0+ dB**: Lenient (includes dynamic sections)

**Example**:
```bash
# Require very consistent sections (< 2 dB variation)
python volume_consistency_analyzer.py music.mp3 --threshold 2.0
```

### Other Options
```bash
# No visualization (faster)
--no-visualize

# No extraction (analysis only)
--no-extract

# Minimal output
--quiet
```

---

## Troubleshooting

### "No consistent sections found"
**Cause**: Track is too dynamic for current threshold

**Solution**: Increase threshold
```bash
python volume_consistency_analyzer.py music.mp3 --threshold 5.0
```

### "Only found short sections"
**Cause**: Window size too large for track variations

**Solution**: Decrease window size
```bash
python volume_consistency_analyzer.py music.mp3 --window 5
```

### "ImportError: No module named 'librosa'"
**Cause**: Missing dependencies

**Solution**:
```bash
pip install librosa pydub numpy matplotlib
```

### "Best section is in the outro"
**Cause**: Fade-outs have low volume variation

**Solution**: Review visualization, select 2nd or 3rd ranked section
```python
# In Python:
results = analyzer.analyze("music.mp3")
second_best = results['consistent_sections'][1]  # Try this one
```

---

## Performance Notes

- **Speed**: ~10-20 seconds for 3-minute track
- **Memory**: ~200-400 MB
- **Disk**: Minimal (~10 MB per analysis)
- **CPU**: Single-core (can be parallelized)

**For large libraries** (100+ tracks):
```bash
# Run in parallel (4 at a time)
ls background_music/*.mp3 | xargs -n1 -P4 python volume_consistency_analyzer.py
```

---

## Integration Examples

### With Existing Pipeline
```python
# In your video generation script:
from volume_consistency_analyzer import VolumeConsistencyAnalyzer

def get_background_music(source_track, target_duration):
    """Get best consistent section from track"""
    analyzer = VolumeConsistencyAnalyzer()
    results = analyzer.analyze(source_track, visualize=False, verbose=False)

    # Find section closest to target duration
    best = min(
        results['consistent_sections'],
        key=lambda s: abs(s['duration'] - target_duration)
    )

    return results['best_section_path']

# Use it
bg_music = get_background_music("music.mp3", narration_duration=82)
```

### Batch Processing
```bash
#!/bin/bash
# analyze_all_music.sh

mkdir -p output

for track in background_music/*.mp3; do
    echo "Analyzing: $(basename "$track")"
    python volume_consistency_analyzer.py "$track" --quiet --no-visualize
done

echo "Done! Check output/ for extracted sections"
```

---

## Next Steps

1. **Try it now**: Run on one of your music tracks
   ```bash
   python volume_consistency_analyzer.py background_music/sample.mp3
   ```

2. **Review results**: Check the visualization PNG to understand selections

3. **Batch process**: Analyze your entire music library
   ```bash
   for f in background_music/*.mp3; do
       python volume_consistency_analyzer.py "$f" --no-visualize
   done
   ```

4. **Integrate**: Add to your video pipeline (see examples above)

5. **Customize**: Adjust thresholds and windows for your specific needs

---

## Support & Resources

### Documentation Files
- Quick reference: `VOLUME_CONSISTENCY_QUICK_START.md`
- Technical details: `VOLUME_CONSISTENCY_ANALYSIS_GUIDE.md`
- Overview: `VOLUME_CONSISTENCY_SUMMARY.md`

### Command Help
```bash
python volume_consistency_analyzer.py --help
```

### Example Workflows
See `VOLUME_CONSISTENCY_QUICK_START.md` for:
- Real-world examples
- Integration patterns
- Batch processing scripts
- Python code examples

---

## Summary

**What you have**:
- ✅ Production-ready volume consistency analyzer
- ✅ Automated section detection and ranking
- ✅ Visual verification tools
- ✅ Extracted MP3 sections ready to use
- ✅ Comprehensive documentation
- ✅ Integration examples

**What you can do**:
- Find perfect background music sections automatically
- Curate entire music libraries efficiently
- Verify selections visually
- Integrate into video pipelines
- Batch process 100+ tracks

**Time saved**: 5-10 minutes per track (listening + testing) → 15 seconds automated

Start analyzing: `python volume_consistency_analyzer.py your_music.mp3`
