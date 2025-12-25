# Volume Consistency Analysis - Quick Start Guide

## What This Tool Does

Analyzes music tracks to identify sections with **consistent volume** (perfect for background music) vs. sections with **dynamic volume changes** (intros, outros, build-ups, drops).

## Installation

```bash
# Install required Python libraries
pip install librosa pydub numpy matplotlib

# Verify installation
python -c "import librosa, pydub, numpy, matplotlib; print('All libraries installed!')"
```

## Basic Usage

### 1. Quick Analysis (Default Settings)

```bash
python volume_consistency_analyzer.py background_music.mp3
```

**What it does**:
- Analyzes volume in 10-second windows
- Identifies sections with < 3 dB variation (consistent)
- Generates visualization PNG
- Extracts best consistent section to MP3
- Saves JSON report with all details

**Output**:
- `output/background_music_consistency_analysis.json` - Full analysis data
- `output/background_music_consistency_visualization.png` - Visual plot
- `output/background_music_best_82s.mp3` - Best consistent section extracted

### 2. Stricter Consistency (For Very Stable Background Music)

```bash
python volume_consistency_analyzer.py music.mp3 --threshold 2.0
```

- Only identifies sections with < 2 dB variation
- Best for narration-heavy videos where music must stay very quiet and consistent

### 3. Lenient Consistency (For Dynamic Tracks)

```bash
python volume_consistency_analyzer.py music.mp3 --threshold 5.0
```

- Allows up to 5 dB variation
- Good for finding usable sections in more dynamic tracks

### 4. Custom Window Size

```bash
python volume_consistency_analyzer.py music.mp3 --window 15
```

- Analyzes in 15-second windows (instead of default 10s)
- Larger windows = detect overall consistency
- Smaller windows = detect quick changes

### 5. Analysis Only (No Extraction)

```bash
python volume_consistency_analyzer.py music.mp3 --no-extract --no-visualize
```

- Just analyze and save JSON report
- Useful for batch processing

## Understanding the Results

### Quality Classifications

| Std Dev | Quality | Suitable For |
|---------|---------|--------------|
| < 1.0 dB | **EXCELLENT** | Ideal background music |
| 1.0-1.5 dB | **VERY GOOD** | Great background music |
| 1.5-2.5 dB | **GOOD** | Good background music |
| 2.5-3.0 dB | **ACCEPTABLE** | Usable with caution |
| > 3.0 dB | **DYNAMIC** | Avoid for background (intro/outro/build-up) |

### Visualization Explained

**Top Panel**: Volume consistency over time
- Blue line = Volume variation (std dev) at each point
- Red dashed line = Your threshold (3 dB default)
- Green shaded area = Consistent regions
- Dark green dotted line = Excellent threshold

**Bottom Panel**: Identified consistent sections
- Each bar = One consistent section
- Green bars = Best quality
- Yellow-green = Acceptable quality
- Position on timeline shows when section occurs

## Real-World Examples

### Example 1: Find 82-Second Background Music Clip

```bash
# Analyze full track
python volume_consistency_analyzer.py epic_music_full.mp3

# Results show best section: 45s - 127s (82s duration)
# Already extracted to: output/epic_music_full_best_82s.mp3

# Use this file directly in your video!
```

### Example 2: Analyze Entire Music Library

```bash
# Create batch script
for file in background_music/*.mp3; do
    python volume_consistency_analyzer.py "$file" --no-visualize --quiet
done

# Check output/*.json files for best sections
```

### Example 3: Find Multiple Good Sections

```python
# Python integration
from volume_consistency_analyzer import VolumeConsistencyAnalyzer

analyzer = VolumeConsistencyAnalyzer(window_duration=10.0, consistency_threshold_db=3.0)
results = analyzer.analyze("music.mp3")

# Get top 5 sections
top_sections = results['consistent_sections'][:5]

for i, section in enumerate(top_sections, 1):
    print(f"{i}. {section['start']:.1f}s - {section['end']:.1f}s ({section['duration']:.1f}s)")
    print(f"   Quality: {section['avg_std']:.2f} dB std dev")
    print(f"   Score: {section['score']:.0f}/100")
```

## Parameter Tuning Guide

### When to Adjust Window Size

**Use smaller windows (5-8s)** when:
- Track has quick changes
- Need to detect short consistent sections
- Working with shorter tracks (< 2 minutes)

**Use larger windows (15-30s)** when:
- Track is very long (> 5 minutes)
- Want to find large consistent sections
- Track has slow, gradual changes

### When to Adjust Threshold

**Use stricter threshold (1.0-2.0 dB)** when:
- Creating narration-heavy videos
- Need very stable background music
- Track has excellent production quality

**Use lenient threshold (4.0-6.0 dB)** when:
- Working with dynamic tracks
- Can't find any sections with default threshold
- Background music will be very quiet anyway (< 10% volume)

## Interpreting JSON Output

```json
{
  "file_path": "background_music.mp3",
  "duration": 180.5,
  "consistent_sections": [
    {
      "start": 45.0,
      "end": 127.0,
      "duration": 82.0,
      "avg_std": 2.3,
      "avg_mean": -18.5,
      "score": 77.0,
      "num_segments": 15
    }
  ],
  "best_section_path": "output/background_music_best_82s.mp3"
}
```

**Key fields**:
- `start`/`end`: Time positions in seconds
- `duration`: Length of consistent section
- `avg_std`: Average std dev (lower = more consistent)
- `score`: Quality score (higher = better)
- `best_section_path`: Where extracted MP3 was saved

## Troubleshooting

### Problem: "No consistent sections found"

**Solution**: Track is too dynamic. Try:
```bash
# Increase threshold
python volume_consistency_analyzer.py music.mp3 --threshold 5.0

# Or use larger windows
python volume_consistency_analyzer.py music.mp3 --window 20
```

### Problem: "Only found very short sections"

**Solution**: Decrease window size to detect smaller consistent parts:
```bash
python volume_consistency_analyzer.py music.mp3 --window 5
```

### Problem: "Best section is at the very end"

**Cause**: Track ends with long fade-out (low volume = low variance)

**Solution**: Review multiple sections, not just the best:
```python
results = analyzer.analyze("music.mp3")
for section in results['consistent_sections'][:5]:
    # Review start/end times
    # Avoid sections in first/last 10% of track
```

### Problem: "ImportError: No module named 'librosa'"

**Solution**:
```bash
pip install librosa pydub numpy matplotlib
```

## Advanced Usage

### Batch Process All Music Files

```bash
#!/bin/bash
# batch_analyze.sh

mkdir -p output

for file in background_music/*.mp3; do
    echo "Analyzing: $file"
    python volume_consistency_analyzer.py "$file" --no-visualize --quiet
done

echo "Done! Check output/ for results"
```

### Python Integration

```python
from volume_consistency_analyzer import VolumeConsistencyAnalyzer
from pathlib import Path

# Create analyzer
analyzer = VolumeConsistencyAnalyzer(
    window_duration=10.0,
    consistency_threshold_db=3.0
)

# Analyze all MP3 files
music_files = Path("background_music").glob("*.mp3")

best_tracks = []

for music_file in music_files:
    results = analyzer.analyze(str(music_file), visualize=False, verbose=False)

    if results['consistent_sections']:
        best_section = results['consistent_sections'][0]
        best_tracks.append({
            'file': music_file.name,
            'duration': best_section['duration'],
            'quality': best_section['avg_std'],
            'score': best_section['score']
        })

# Sort by quality
best_tracks.sort(key=lambda x: x['score'], reverse=True)

print("Top 10 Best Background Music Tracks:")
for i, track in enumerate(best_tracks[:10], 1):
    print(f"{i}. {track['file']} - Score: {track['score']:.0f}, Duration: {track['duration']:.0f}s")
```

## Integration with Video Pipeline

### Example: Auto-Select Background Music

```python
from volume_consistency_analyzer import VolumeConsistencyAnalyzer

def get_best_background_music(music_file, target_duration=82):
    """
    Get best consistent section from music file

    Returns:
        Path to extracted MP3 section
    """
    analyzer = VolumeConsistencyAnalyzer()
    results = analyzer.analyze(music_file, visualize=False, verbose=False)

    if not results['consistent_sections']:
        raise ValueError(f"No consistent sections found in {music_file}")

    # Find section closest to target duration
    best = min(
        results['consistent_sections'],
        key=lambda s: abs(s['duration'] - target_duration)
    )

    # Extract it
    output = f"output/bg_music_{target_duration}s.mp3"
    analyzer._extract_section(music_file, best['start'], best['end'], output, False)

    return output

# Use in video pipeline
bg_music = get_best_background_music("background_music/epic_track.mp3", target_duration=82)
print(f"Using background music: {bg_music}")
```

## Tips for Best Results

1. **Analyze before using**: Don't assume the middle of a track is consistent - build-ups often occur mid-track

2. **Use visualizations**: The PNG plots help you understand WHY certain sections were chosen

3. **Check multiple tracks**: Different tracks work better for different video styles

4. **Save extracted sections**: Build a library of pre-extracted consistent sections for quick access

5. **Consider context**: A section that's "ACCEPTABLE" (2.5-3 dB) might work fine if background music volume is very low (< 10%)

6. **Avoid intro/outro bias**: Sometimes the analyzer picks very quiet sections at the end. Review the visualization to ensure you're not getting a fade-out.

## Performance Notes

- **Analysis speed**: ~10-20 seconds for a 3-minute track
- **Memory usage**: ~200-400 MB (loads entire track)
- **Disk usage**: Minimal (extracted MP3 + JSON + PNG)

## Summary

**Default command** (covers 90% of use cases):
```bash
python volume_consistency_analyzer.py your_music.mp3
```

**For narration-heavy videos** (stricter):
```bash
python volume_consistency_analyzer.py your_music.mp3 --threshold 2.0
```

**For dynamic tracks** (lenient):
```bash
python volume_consistency_analyzer.py your_music.mp3 --threshold 5.0
```

That's it! The tool does the hard work of analyzing volume consistency so you can quickly find the perfect background music sections.
