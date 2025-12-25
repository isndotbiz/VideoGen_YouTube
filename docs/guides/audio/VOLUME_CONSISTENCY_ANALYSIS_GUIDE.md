# Comprehensive Guide: Music Track Volume Consistency Analysis

## Executive Summary

This guide provides a complete technical solution for analyzing music track volume consistency to identify sections suitable for background music vs. dynamic sections (intros, outros, build-ups, drops). It focuses on practical, implementable solutions using ffmpeg, Python libraries (librosa, pydub), and established audio metrics.

---

## Table of Contents

1. [Understanding Volume Consistency Metrics](#understanding-volume-consistency-metrics)
2. [Tools & Libraries Overview](#tools--libraries-overview)
3. [Volume Analysis Methods](#volume-analysis-methods)
4. [Practical Implementation](#practical-implementation)
5. [Threshold Definitions](#threshold-definitions)
6. [Auto-Extracting Consistent Sections](#auto-extracting-consistent-sections)
7. [Visualization Techniques](#visualization-techniques)
8. [Complete Production Solution](#complete-production-solution)

---

## Understanding Volume Consistency Metrics

### 1. RMS (Root Mean Square)

**What it measures**: Average power of the audio signal over time

**Pros**:
- Fast to calculate
- Works well for detecting volume changes
- Good for relative comparisons within the same track

**Cons**:
- Doesn't reflect perceived loudness accurately
- Electrical measurement, not perceptual

**Use case**: Real-time volume change detection, quick consistency checks

### 2. LUFS (Loudness Units relative to Full Scale)

**What it measures**: Perceived loudness based on human hearing

**Pros**:
- Industry standard for loudness measurement
- Reflects how humans actually perceive loudness
- Used by all streaming platforms (Spotify: -14 LUFS, YouTube: -13 LUFS)
- Better for comparing different tracks

**Cons**:
- Slower to calculate than RMS
- More complex implementation

**Use case**: Professional loudness analysis, streaming platform compliance, cross-track comparison

### 3. dBFS (Decibels relative to Full Scale)

**What it measures**: Amplitude relative to digital maximum

**Pros**:
- Standard digital audio measurement
- Easy to understand and implement
- Good for detecting peaks and clipping

**Cons**:
- Peak-based, not average loudness
- Doesn't reflect sustained volume

**Use case**: Peak detection, clipping prevention, dynamic range analysis

### Recommendation for Background Music Analysis

**Best approach**: Combine RMS for consistency detection + LUFS for final quality check

- Use **RMS** to detect volume variations within sections (fast)
- Use **LUFS** to validate overall loudness consistency (accurate)
- Use **dBFS** to ensure no clipping or silent sections

---

## Tools & Libraries Overview

### Option 1: ffmpeg (Fastest, Command-Line)

**Pros**: Pre-installed, very fast, no Python dependencies
**Cons**: Limited customization, requires parsing output

```bash
# Volume detection
ffmpeg -i audio.mp3 -af "volumedetect" -f null - 2>&1 | grep -E "(mean_volume|max_volume)"

# EBUR128 loudness analysis (LUFS)
ffmpeg -i audio.mp3 -af "ebur128" -f null - 2>&1
```

### Option 2: librosa (Best for Music Analysis)

**Pros**: Excellent for music features, well-documented
**Cons**: Slower, requires Python setup

```python
import librosa
import numpy as np

y, sr = librosa.load("audio.mp3")
rms = librosa.feature.rms(y=y)
```

### Option 3: pydub (Easiest Python Integration)

**Pros**: Simple API, works with any audio format
**Cons**: Less sophisticated analysis

```python
from pydub import AudioSegment

audio = AudioSegment.from_file("audio.mp3")
loudness = audio.dBFS  # Average loudness
```

### Option 4: pyloudnorm (Best for LUFS)

**Pros**: Dedicated LUFS library, accurate ITU-R BS.1770 implementation
**Cons**: Additional dependency

```python
import pyloudnorm as pyln

meter = pyln.Meter(sr)
loudness = meter.integrated_loudness(audio)
```

---

## Volume Analysis Methods

### Method 1: Sliding Window RMS Analysis

**Purpose**: Detect volume consistency over time windows

```python
import librosa
import numpy as np

def analyze_volume_consistency(file_path, window_duration=10.0, hop_duration=1.0):
    """
    Analyze volume consistency using sliding window RMS

    Args:
        file_path: Path to audio file
        window_duration: Window size in seconds (default: 10s)
        hop_duration: Hop size in seconds (default: 1s)

    Returns:
        segments: List of dicts with start, end, rms_db, variance
    """
    # Load audio
    y, sr = librosa.load(file_path, sr=None)

    window_samples = int(window_duration * sr)
    hop_samples = int(hop_duration * sr)

    segments = []

    for i in range(0, len(y) - window_samples, hop_samples):
        window = y[i:i+window_samples]

        # Calculate RMS for window
        rms = np.sqrt(np.mean(window**2))
        rms_db = librosa.amplitude_to_db([rms])[0]

        # Calculate variance within window
        # Subdivide window into 1-second chunks
        chunk_size = sr  # 1 second
        chunk_rms = []

        for j in range(0, len(window), chunk_size):
            chunk = window[j:j+chunk_size]
            if len(chunk) >= chunk_size // 2:
                chunk_rms.append(np.sqrt(np.mean(chunk**2)))

        chunk_rms_db = librosa.amplitude_to_db(chunk_rms)
        variance = np.var(chunk_rms_db)
        std_dev = np.std(chunk_rms_db)

        segments.append({
            'start': i / sr,
            'end': (i + window_samples) / sr,
            'duration': window_duration,
            'rms_db': float(rms_db),
            'variance_db': float(variance),
            'std_dev_db': float(std_dev),
            'rms_range': float(np.max(chunk_rms_db) - np.min(chunk_rms_db))
        })

    return segments

# Example usage
segments = analyze_volume_consistency("background_music.mp3", window_duration=10.0)

# Find consistent sections (low variance)
consistent_sections = [s for s in segments if s['std_dev_db'] < 3.0]
print(f"Found {len(consistent_sections)} consistent sections")
```

### Method 2: LUFS-based Consistency Analysis

**Purpose**: Industry-standard loudness consistency measurement

```python
import librosa
import numpy as np
import pyloudnorm as pyln

def analyze_lufs_consistency(file_path, window_duration=10.0, hop_duration=1.0):
    """
    Analyze loudness consistency using LUFS (ITU-R BS.1770)

    Args:
        file_path: Path to audio file
        window_duration: Window size in seconds
        hop_duration: Hop size in seconds

    Returns:
        segments: List of dicts with LUFS measurements
    """
    # Load audio
    y, sr = librosa.load(file_path, sr=None)

    # Create loudness meter
    meter = pyln.Meter(sr)

    window_samples = int(window_duration * sr)
    hop_samples = int(hop_duration * sr)

    segments = []

    for i in range(0, len(y) - window_samples, hop_samples):
        window = y[i:i+window_samples]

        # Measure integrated loudness for this window
        try:
            loudness = meter.integrated_loudness(window)
        except:
            loudness = -100.0  # Silent section

        # Calculate loudness range within window
        chunk_size = sr  # 1 second chunks
        chunk_loudness = []

        for j in range(0, len(window), chunk_size):
            chunk = window[j:j+chunk_size]
            if len(chunk) >= chunk_size // 2:
                try:
                    chunk_lufs = meter.integrated_loudness(chunk)
                    chunk_loudness.append(chunk_lufs)
                except:
                    pass

        if chunk_loudness:
            lufs_range = max(chunk_loudness) - min(chunk_loudness)
            lufs_std = np.std(chunk_loudness)
        else:
            lufs_range = 0
            lufs_std = 0

        segments.append({
            'start': i / sr,
            'end': (i + window_samples) / sr,
            'duration': window_duration,
            'lufs': float(loudness),
            'lufs_range': float(lufs_range),
            'lufs_std': float(lufs_std)
        })

    return segments

# Example usage
segments = analyze_lufs_consistency("background_music.mp3", window_duration=10.0)

# Find consistent sections (LUFS variation < 3 LU)
consistent = [s for s in segments if s['lufs_range'] < 3.0 and s['lufs'] > -30]
print(f"Found {len(consistent)} LUFS-consistent sections")
```

### Method 3: FFmpeg-based Real-time Analysis

**Purpose**: Fast analysis without loading entire file into memory

```python
import subprocess
import json
import numpy as np

def analyze_volume_ffmpeg(file_path, segment_duration=10.0):
    """
    Analyze volume using ffmpeg's astats filter

    Args:
        file_path: Path to audio file
        segment_duration: Segment duration in seconds

    Returns:
        segments: List of volume statistics per segment
    """
    # Get total duration first
    duration_cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]

    result = subprocess.run(duration_cmd, capture_output=True, text=True)
    total_duration = float(result.stdout.strip())

    segments = []

    # Analyze each segment
    for start in np.arange(0, total_duration, segment_duration):
        end = min(start + segment_duration, total_duration)

        # Extract segment statistics
        stats_cmd = [
            'ffmpeg', '-ss', str(start), '-t', str(segment_duration),
            '-i', file_path,
            '-af', 'astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-',
            '-f', 'null', '-'
        ]

        result = subprocess.run(stats_cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)

        # Parse output for RMS levels
        lines = result.stdout.split('\n')
        rms_values = []

        for line in lines:
            if 'RMS_level' in line:
                try:
                    # Extract RMS value
                    value = float(line.split('=')[-1].strip())
                    rms_values.append(value)
                except:
                    pass

        if rms_values:
            segments.append({
                'start': start,
                'end': end,
                'duration': end - start,
                'mean_rms_db': float(np.mean(rms_values)),
                'std_rms_db': float(np.std(rms_values)),
                'rms_range_db': float(np.max(rms_values) - np.min(rms_values))
            })

    return segments
```

---

## Threshold Definitions

### Consistency Thresholds (Based on Research & Industry Standards)

#### RMS-based Thresholds

```python
CONSISTENCY_THRESHOLDS = {
    'rms_variance': {
        'very_consistent': 1.5,   # Variance < 1.5 dB (excellent for background)
        'consistent': 3.0,        # Variance < 3.0 dB (good for background)
        'moderate': 5.0,          # Variance < 5.0 dB (acceptable)
        'dynamic': float('inf')   # Variance >= 5.0 dB (intro/outro/build-up)
    },
    'rms_std_dev': {
        'very_consistent': 1.0,   # Std dev < 1.0 dB
        'consistent': 2.0,        # Std dev < 2.0 dB
        'moderate': 3.0,          # Std dev < 3.0 dB
        'dynamic': float('inf')   # Std dev >= 3.0 dB
    },
    'rms_range': {
        'very_consistent': 3.0,   # Range < 3 dB (10-sec window)
        'consistent': 6.0,        # Range < 6 dB
        'moderate': 10.0,         # Range < 10 dB
        'dynamic': float('inf')   # Range >= 10 dB
    }
}
```

#### LUFS-based Thresholds

```python
LUFS_THRESHOLDS = {
    'lufs_range': {
        'very_consistent': 2.0,   # Range < 2 LU (loudness units)
        'consistent': 3.0,        # Range < 3 LU (recommended)
        'moderate': 5.0,          # Range < 5 LU
        'dynamic': float('inf')   # Range >= 5 LU
    },
    'optimal_background_lufs': {
        'min': -35.0,             # Minimum acceptable loudness
        'ideal_min': -25.0,       # Ideal minimum for background music
        'ideal_max': -15.0,       # Ideal maximum for background music
        'max': -10.0              # Maximum (might overpower narration)
    }
}
```

#### Section Classification Rules

```python
def classify_section(segment, metric='rms'):
    """
    Classify audio section based on volume consistency

    Args:
        segment: Dict with volume statistics
        metric: 'rms' or 'lufs'

    Returns:
        classification: str ('very_consistent', 'consistent', 'moderate', 'dynamic')
        suitability: str ('excellent', 'good', 'acceptable', 'avoid')
    """
    if metric == 'rms':
        variance = segment.get('variance_db', 0)
        std_dev = segment.get('std_dev_db', 0)

        if variance < 1.5 and std_dev < 1.0:
            return 'very_consistent', 'excellent_for_background'
        elif variance < 3.0 and std_dev < 2.0:
            return 'consistent', 'good_for_background'
        elif variance < 5.0 and std_dev < 3.0:
            return 'moderate', 'acceptable_with_caution'
        else:
            return 'dynamic', 'avoid_for_background'

    elif metric == 'lufs':
        lufs_range = segment.get('lufs_range', 0)
        lufs = segment.get('lufs', -100)

        # Check if within acceptable loudness range
        too_quiet = lufs < -35
        too_loud = lufs > -10

        if too_quiet:
            return 'too_quiet', 'avoid_too_quiet'
        if too_loud:
            return 'too_loud', 'avoid_too_loud'

        if lufs_range < 2.0:
            return 'very_consistent', 'excellent_for_background'
        elif lufs_range < 3.0:
            return 'consistent', 'good_for_background'
        elif lufs_range < 5.0:
            return 'moderate', 'acceptable_with_caution'
        else:
            return 'dynamic', 'avoid_for_background'
```

### Practical Threshold Recommendations

**For 10-second windows** (recommended for background music analysis):
- **Excellent**: RMS variance < 1.5 dB, LUFS range < 2 LU
- **Good**: RMS variance < 3 dB, LUFS range < 3 LU
- **Acceptable**: RMS variance < 5 dB, LUFS range < 5 LU
- **Dynamic (Avoid)**: RMS variance >= 5 dB, LUFS range >= 5 LU

**Why these thresholds work**:
- 3 dB change = 2x perceived loudness change (noticeable but acceptable)
- 6 dB change = 4x perceived loudness change (very noticeable)
- 10 dB change = 10x perceived loudness change (dramatic)

---

## Auto-Extracting Consistent Sections

### Complete Extraction System

```python
#!/usr/bin/env python3
"""
Automatic Consistent Section Extractor
Finds and extracts the "meat" of songs, avoiding intros/outros
"""

import librosa
import numpy as np
from pydub import AudioSegment
import json
from pathlib import Path

class ConsistentSectionExtractor:
    """
    Extract consistent volume sections from music tracks
    """

    def __init__(self,
                 window_duration=10.0,
                 hop_duration=5.0,
                 consistency_threshold=3.0,
                 min_section_duration=30.0):
        """
        Initialize extractor

        Args:
            window_duration: Analysis window size (seconds)
            hop_duration: Hop between windows (seconds)
            consistency_threshold: Max std dev for consistent section (dB)
            min_section_duration: Minimum duration for extracted section (seconds)
        """
        self.window_duration = window_duration
        self.hop_duration = hop_duration
        self.consistency_threshold = consistency_threshold
        self.min_section_duration = min_section_duration

    def analyze_track(self, file_path):
        """
        Analyze entire track for volume consistency

        Returns:
            analysis: Dict with segments and recommendations
        """
        print(f"\nAnalyzing: {Path(file_path).name}")

        # Load audio
        y, sr = librosa.load(file_path, sr=None)
        duration = len(y) / sr

        print(f"Duration: {duration:.1f}s")

        # Analyze in windows
        window_samples = int(self.window_duration * sr)
        hop_samples = int(self.hop_duration * sr)

        segments = []

        for i in range(0, len(y) - window_samples, hop_samples):
            window = y[i:i+window_samples]

            # Calculate RMS statistics
            chunk_size = sr  # 1-second chunks
            chunk_rms = []

            for j in range(0, len(window), chunk_size):
                chunk = window[j:j+chunk_size]
                if len(chunk) >= chunk_size // 2:
                    rms = np.sqrt(np.mean(chunk**2))
                    chunk_rms.append(rms)

            chunk_rms_db = librosa.amplitude_to_db(chunk_rms)

            mean_rms_db = np.mean(chunk_rms_db)
            std_dev_db = np.std(chunk_rms_db)
            variance_db = np.var(chunk_rms_db)
            rms_range = np.max(chunk_rms_db) - np.min(chunk_rms_db)

            # Classify consistency
            if std_dev_db < 1.0:
                consistency = 'very_consistent'
                score = 100
            elif std_dev_db < 2.0:
                consistency = 'consistent'
                score = 85
            elif std_dev_db < 3.0:
                consistency = 'moderate'
                score = 70
            else:
                consistency = 'dynamic'
                score = max(0, 50 - (std_dev_db - 3.0) * 10)

            segments.append({
                'start': i / sr,
                'end': (i + window_samples) / sr,
                'mean_rms_db': float(mean_rms_db),
                'std_dev_db': float(std_dev_db),
                'variance_db': float(variance_db),
                'rms_range_db': float(rms_range),
                'consistency': consistency,
                'score': score
            })

        return {
            'file_path': file_path,
            'duration': duration,
            'segments': segments
        }

    def find_consistent_sections(self, analysis):
        """
        Find contiguous consistent sections

        Returns:
            sections: List of consistent section ranges
        """
        segments = analysis['segments']

        # Find consistent segments
        consistent_segments = [
            s for s in segments
            if s['std_dev_db'] < self.consistency_threshold
        ]

        if not consistent_segments:
            return []

        # Merge contiguous segments into sections
        sections = []
        current_section = {
            'start': consistent_segments[0]['start'],
            'end': consistent_segments[0]['end'],
            'segments': [consistent_segments[0]]
        }

        for segment in consistent_segments[1:]:
            # Check if contiguous with current section
            if segment['start'] <= current_section['end'] + self.hop_duration:
                # Extend current section
                current_section['end'] = segment['end']
                current_section['segments'].append(segment)
            else:
                # Start new section
                sections.append(current_section)
                current_section = {
                    'start': segment['start'],
                    'end': segment['end'],
                    'segments': [segment]
                }

        # Add final section
        sections.append(current_section)

        # Filter by minimum duration
        valid_sections = [
            s for s in sections
            if (s['end'] - s['start']) >= self.min_section_duration
        ]

        # Calculate section statistics
        for section in valid_sections:
            section['duration'] = section['end'] - section['start']
            section['num_segments'] = len(section['segments'])
            section['avg_std_dev'] = np.mean([seg['std_dev_db'] for seg in section['segments']])
            section['avg_score'] = np.mean([seg['score'] for seg in section['segments']])

        # Sort by score
        valid_sections.sort(key=lambda x: x['avg_score'], reverse=True)

        return valid_sections

    def extract_section(self, file_path, start_time, end_time, output_path):
        """
        Extract specific section from audio file

        Args:
            file_path: Source audio file
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Output file path
        """
        print(f"\nExtracting section:")
        print(f"  {start_time:.1f}s -> {end_time:.1f}s ({end_time-start_time:.1f}s)")

        # Load with pydub
        audio = AudioSegment.from_file(file_path)

        # Extract section
        start_ms = int(start_time * 1000)
        end_ms = int(end_time * 1000)

        section = audio[start_ms:end_ms]

        # Export
        section.export(output_path, format="mp3", bitrate="192k")

        print(f"  Saved: {output_path}")

        return output_path

    def auto_extract_best_section(self, file_path, target_duration=None, output_dir="output"):
        """
        Automatically find and extract the best consistent section

        Args:
            file_path: Source audio file
            target_duration: Desired duration (None = longest section)
            output_dir: Output directory

        Returns:
            extracted_path: Path to extracted section
        """
        # Analyze track
        analysis = self.analyze_track(file_path)

        # Find consistent sections
        sections = self.find_consistent_sections(analysis)

        if not sections:
            print("No consistent sections found!")
            return None

        print(f"\nFound {len(sections)} consistent sections:")
        for i, section in enumerate(sections, 1):
            print(f"  {i}. {section['start']:.1f}s - {section['end']:.1f}s "
                  f"({section['duration']:.1f}s, score: {section['avg_score']:.0f})")

        # Select best section
        if target_duration:
            # Find section closest to target duration
            best_section = min(sections, key=lambda s: abs(s['duration'] - target_duration))
        else:
            # Use highest scoring section
            best_section = sections[0]

        # Extract section
        Path(output_dir).mkdir(exist_ok=True)

        filename = Path(file_path).stem
        output_path = Path(output_dir) / f"{filename}_consistent_{int(best_section['duration'])}s.mp3"

        self.extract_section(
            file_path,
            best_section['start'],
            best_section['end'],
            str(output_path)
        )

        return str(output_path)


# Example usage
if __name__ == "__main__":
    extractor = ConsistentSectionExtractor(
        window_duration=10.0,
        hop_duration=5.0,
        consistency_threshold=3.0,
        min_section_duration=30.0
    )

    # Auto-extract best section
    output = extractor.auto_extract_best_section(
        "background_music/long_track.mp3",
        target_duration=82.0
    )

    print(f"\nExtracted section: {output}")
```

---

## Visualization Techniques

### Method 1: Volume Over Time Plot

```python
import matplotlib.pyplot as plt
import librosa
import numpy as np

def visualize_volume_over_time(file_path, output_image="volume_analysis.png"):
    """
    Create comprehensive volume visualization

    Args:
        file_path: Path to audio file
        output_image: Output image path
    """
    # Load audio
    y, sr = librosa.load(file_path, sr=None)

    # Calculate RMS in 0.1s windows
    hop_length = int(0.1 * sr)
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)

    # Calculate time axis
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)

    # Calculate moving statistics (10s windows)
    window_size = 100  # 10 seconds / 0.1s
    moving_mean = np.convolve(rms_db, np.ones(window_size)/window_size, mode='valid')
    moving_std = []

    for i in range(len(rms_db) - window_size):
        window = rms_db[i:i+window_size]
        moving_std.append(np.std(window))

    moving_std = np.array(moving_std)

    # Create figure
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    # Plot 1: RMS over time
    axes[0].plot(times, rms_db, linewidth=0.5, alpha=0.7, label='RMS (dB)')
    axes[0].set_ylabel('RMS (dB)')
    axes[0].set_title(f'Volume Analysis: {Path(file_path).name}')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Plot 2: Moving average
    times_moving = times[:len(moving_mean)]
    axes[1].plot(times_moving, moving_mean, linewidth=2, label='10s Moving Average', color='blue')
    axes[1].fill_between(times_moving,
                          moving_mean - 3,
                          moving_mean + 3,
                          alpha=0.2,
                          color='green',
                          label='±3dB Consistency Zone')
    axes[1].set_ylabel('RMS (dB)')
    axes[1].set_title('Volume Consistency (10s windows)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # Plot 3: Consistency indicator (standard deviation)
    times_std = times[:len(moving_std)]
    axes[2].plot(times_std, moving_std, linewidth=2, color='red', label='Std Dev')
    axes[2].axhline(y=3.0, color='orange', linestyle='--', label='3dB Threshold (Consistent)')
    axes[2].axhline(y=5.0, color='red', linestyle='--', label='5dB Threshold (Dynamic)')
    axes[2].fill_between(times_std, 0, 3.0, alpha=0.2, color='green', label='Consistent Region')
    axes[2].set_xlabel('Time (seconds)')
    axes[2].set_ylabel('Std Dev (dB)')
    axes[2].set_title('Volume Consistency Score (lower = more consistent)')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    plt.savefig(output_image, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved: {output_image}")

    return output_image


# Example usage
visualize_volume_over_time("background_music.mp3", "output/volume_analysis.png")
```

### Method 2: Heatmap Visualization

```python
import matplotlib.pyplot as plt
import librosa
import numpy as np

def visualize_consistency_heatmap(file_path, output_image="consistency_heatmap.png"):
    """
    Create heatmap showing consistent vs. dynamic regions

    Args:
        file_path: Path to audio file
        output_image: Output image path
    """
    # Load audio
    y, sr = librosa.load(file_path, sr=None)

    # Calculate RMS in 1s windows
    hop_length = sr  # 1 second
    window_length = sr * 10  # 10 second analysis windows

    rms_values = []
    time_points = []

    for i in range(0, len(y) - window_length, hop_length):
        window = y[i:i+window_length]

        # Calculate RMS for 1s chunks within window
        chunks = []
        for j in range(0, len(window), sr):
            chunk = window[j:j+sr]
            if len(chunk) >= sr // 2:
                rms = np.sqrt(np.mean(chunk**2))
                chunks.append(librosa.amplitude_to_db([rms])[0])

        rms_values.append(chunks)
        time_points.append(i / sr)

    # Convert to array
    rms_array = np.array(rms_values).T

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

    # Heatmap
    im = ax1.imshow(rms_array, aspect='auto', origin='lower',
                    cmap='RdYlGn_r', interpolation='nearest',
                    extent=[0, time_points[-1], 0, 10])
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Position in 10s window (seconds)')
    ax1.set_title(f'Volume Consistency Heatmap: {Path(file_path).name}')
    plt.colorbar(im, ax=ax1, label='RMS (dB)')

    # Consistency score over time
    consistency_scores = np.std(rms_array, axis=0)
    ax2.plot(time_points, consistency_scores, linewidth=2, color='purple')
    ax2.axhline(y=3.0, color='orange', linestyle='--', label='Good (<3dB)')
    ax2.axhline(y=5.0, color='red', linestyle='--', label='Moderate (<5dB)')
    ax2.fill_between(time_points, 0, 3.0, alpha=0.3, color='green')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Consistency Score (Std Dev dB)')
    ax2.set_title('Volume Consistency Over Time')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(output_image, dpi=150, bbox_inches='tight')
    print(f"\nHeatmap saved: {output_image}")

    return output_image
```

### Method 3: Interactive Report

```python
def generate_analysis_report(file_path, output_html="analysis_report.html"):
    """
    Generate interactive HTML report with visualizations

    Args:
        file_path: Path to audio file
        output_html: Output HTML file path
    """
    # Analyze track
    extractor = ConsistentSectionExtractor()
    analysis = extractor.analyze_track(file_path)
    sections = extractor.find_consistent_sections(analysis)

    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Volume Consistency Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
            .section {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .excellent {{ border-left: 5px solid #4CAF50; }}
            .good {{ border-left: 5px solid #8BC34A; }}
            .moderate {{ border-left: 5px solid #FFC107; }}
            .dynamic {{ border-left: 5px solid #F44336; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
        </style>
    </head>
    <body>
        <h1>Volume Consistency Analysis Report</h1>
        <h2>{Path(file_path).name}</h2>
        <p><strong>Duration:</strong> {analysis['duration']:.1f}s</p>

        <h2>Consistent Sections Found: {len(sections)}</h2>

        <table>
            <tr>
                <th>Rank</th>
                <th>Start</th>
                <th>End</th>
                <th>Duration</th>
                <th>Avg Std Dev</th>
                <th>Score</th>
                <th>Classification</th>
            </tr>
    """

    for i, section in enumerate(sections, 1):
        classification = 'excellent' if section['avg_std_dev'] < 1.5 else \
                        'good' if section['avg_std_dev'] < 2.5 else \
                        'moderate' if section['avg_std_dev'] < 3.5 else 'dynamic'

        html += f"""
            <tr class="{classification}">
                <td>{i}</td>
                <td>{section['start']:.1f}s</td>
                <td>{section['end']:.1f}s</td>
                <td>{section['duration']:.1f}s</td>
                <td>{section['avg_std_dev']:.2f} dB</td>
                <td>{section['avg_score']:.0f}</td>
                <td>{classification.upper()}</td>
            </tr>
        """

    html += """
        </table>

        <h2>Recommendations</h2>
        <div class="section excellent">
            <h3>Use These Sections for Background Music:</h3>
            <ul>
    """

    for i, section in enumerate(sections[:3], 1):
        html += f"<li>Section {i}: {section['start']:.1f}s - {section['end']:.1f}s ({section['duration']:.1f}s)</li>"

    html += """
            </ul>
        </div>
    </body>
    </html>
    """

    with open(output_html, 'w') as f:
        f.write(html)

    print(f"\nReport saved: {output_html}")
    return output_html
```

---

## Complete Production Solution

### All-in-One Volume Consistency Analyzer

```python
#!/usr/bin/env python3
"""
Complete Volume Consistency Analyzer
Production-ready solution for analyzing music tracks
"""

import librosa
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from pathlib import Path
import json
import argparse

class VolumeConsistencyAnalyzer:
    """
    Complete solution for volume consistency analysis
    """

    def __init__(self,
                 window_duration=10.0,
                 consistency_threshold_db=3.0):
        """
        Initialize analyzer

        Args:
            window_duration: Analysis window in seconds
            consistency_threshold_db: Threshold for consistent classification
        """
        self.window_duration = window_duration
        self.threshold = consistency_threshold_db

    def analyze(self, file_path, visualize=True, extract_best=True):
        """
        Complete analysis pipeline

        Args:
            file_path: Path to audio file
            visualize: Generate visualizations
            extract_best: Extract best consistent section

        Returns:
            results: Dict with complete analysis
        """
        print(f"\n{'='*80}")
        print(f"VOLUME CONSISTENCY ANALYSIS")
        print(f"{'='*80}\n")
        print(f"File: {file_path}")

        # 1. Load and analyze
        print("\n[1/4] Loading and analyzing audio...")
        y, sr = librosa.load(file_path, sr=None)
        duration = len(y) / sr
        print(f"  Duration: {duration:.1f}s")
        print(f"  Sample rate: {sr} Hz")

        # 2. Segment analysis
        print(f"\n[2/4] Analyzing {self.window_duration}s windows...")
        segments = self._analyze_segments(y, sr)

        # 3. Find consistent sections
        print("\n[3/4] Identifying consistent sections...")
        consistent_sections = self._find_consistent_sections(segments)

        print(f"  Found {len(consistent_sections)} consistent sections")
        for i, section in enumerate(consistent_sections[:5], 1):
            print(f"    {i}. {section['start']:.1f}s - {section['end']:.1f}s "
                  f"({section['duration']:.1f}s, std: {section['avg_std']:.2f}dB)")

        # 4. Visualization
        if visualize:
            print("\n[4/4] Generating visualizations...")
            self._visualize(file_path, segments, consistent_sections)

        # 5. Extract best section
        best_section_path = None
        if extract_best and consistent_sections:
            best = consistent_sections[0]
            output_path = f"output/{Path(file_path).stem}_best_{int(best['duration'])}s.mp3"
            best_section_path = self._extract_section(file_path, best['start'], best['end'], output_path)

        # Summary
        results = {
            'file_path': file_path,
            'duration': duration,
            'total_segments': len(segments),
            'consistent_sections': consistent_sections,
            'best_section_path': best_section_path,
            'analysis_params': {
                'window_duration': self.window_duration,
                'consistency_threshold': self.threshold
            }
        }

        # Save JSON report
        report_path = f"output/{Path(file_path).stem}_analysis.json"
        Path("output").mkdir(exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n{'='*80}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"\nReport: {report_path}")
        if best_section_path:
            print(f"Best section: {best_section_path}")

        return results

    def _analyze_segments(self, y, sr):
        """Analyze audio in segments"""
        window_samples = int(self.window_duration * sr)
        hop_samples = window_samples // 2  # 50% overlap

        segments = []

        for i in range(0, len(y) - window_samples, hop_samples):
            window = y[i:i+window_samples]

            # Calculate RMS in 1s chunks
            chunk_size = sr
            chunk_rms = []

            for j in range(0, len(window), chunk_size):
                chunk = window[j:j+chunk_size]
                if len(chunk) >= chunk_size // 2:
                    rms = np.sqrt(np.mean(chunk**2))
                    chunk_rms.append(rms)

            chunk_rms_db = librosa.amplitude_to_db(chunk_rms)

            segments.append({
                'start': i / sr,
                'end': (i + window_samples) / sr,
                'mean_db': float(np.mean(chunk_rms_db)),
                'std_db': float(np.std(chunk_rms_db)),
                'range_db': float(np.max(chunk_rms_db) - np.min(chunk_rms_db)),
                'is_consistent': np.std(chunk_rms_db) < self.threshold
            })

        return segments

    def _find_consistent_sections(self, segments):
        """Find contiguous consistent sections"""
        consistent = [s for s in segments if s['is_consistent']]

        if not consistent:
            return []

        sections = []
        current = {
            'start': consistent[0]['start'],
            'end': consistent[0]['end'],
            'segments': [consistent[0]]
        }

        for seg in consistent[1:]:
            if seg['start'] <= current['end'] + 1.0:  # Within 1 second
                current['end'] = seg['end']
                current['segments'].append(seg)
            else:
                sections.append(current)
                current = {
                    'start': seg['start'],
                    'end': seg['end'],
                    'segments': [seg]
                }

        sections.append(current)

        # Add statistics
        for section in sections:
            section['duration'] = section['end'] - section['start']
            section['avg_std'] = np.mean([s['std_db'] for s in section['segments']])
            section['score'] = 100 - (section['avg_std'] * 10)

        # Sort by score
        sections.sort(key=lambda x: x['score'], reverse=True)

        return sections

    def _extract_section(self, file_path, start, end, output_path):
        """Extract audio section"""
        audio = AudioSegment.from_file(file_path)
        section = audio[int(start*1000):int(end*1000)]
        section.export(output_path, format="mp3", bitrate="192k")
        return output_path

    def _visualize(self, file_path, segments, sections):
        """Generate visualizations"""
        fig, axes = plt.subplots(2, 1, figsize=(14, 8))

        # Plot 1: Consistency over time
        times = [s['start'] for s in segments]
        std_devs = [s['std_db'] for s in segments]

        axes[0].plot(times, std_devs, linewidth=2, label='Std Dev')
        axes[0].axhline(y=self.threshold, color='red', linestyle='--',
                        label=f'Threshold ({self.threshold}dB)')
        axes[0].fill_between(times, 0, self.threshold, alpha=0.2, color='green',
                             label='Consistent Region')
        axes[0].set_ylabel('Std Dev (dB)')
        axes[0].set_title(f'Volume Consistency: {Path(file_path).name}')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()

        # Plot 2: Identified sections
        for i, section in enumerate(sections[:10], 1):
            axes[1].barh(i, section['duration'], left=section['start'],
                         height=0.8, alpha=0.7,
                         label=f"Section {i} ({section['duration']:.0f}s)")

        axes[1].set_xlabel('Time (seconds)')
        axes[1].set_ylabel('Section #')
        axes[1].set_title('Consistent Sections Identified')
        axes[1].grid(True, alpha=0.3, axis='x')
        if len(sections) <= 10:
            axes[1].legend(loc='right')

        plt.tight_layout()
        output_image = f"output/{Path(file_path).stem}_visualization.png"
        plt.savefig(output_image, dpi=150, bbox_inches='tight')
        print(f"  Saved: {output_image}")


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Analyze music tracks for volume consistency',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python volume_consistency_analyzer.py music.mp3

  # Custom window and threshold
  python volume_consistency_analyzer.py music.mp3 --window 15 --threshold 2.5

  # Analysis only (no extraction)
  python volume_consistency_analyzer.py music.mp3 --no-extract
        """
    )

    parser.add_argument('audio_file', help='Path to audio file')
    parser.add_argument('--window', type=float, default=10.0,
                       help='Analysis window duration in seconds (default: 10)')
    parser.add_argument('--threshold', type=float, default=3.0,
                       help='Consistency threshold in dB (default: 3.0)')
    parser.add_argument('--no-visualize', action='store_true',
                       help='Skip visualization generation')
    parser.add_argument('--no-extract', action='store_true',
                       help='Skip extracting best section')

    args = parser.parse_args()

    # Validate file
    if not Path(args.audio_file).exists():
        print(f"Error: File not found: {args.audio_file}")
        return 1

    # Run analysis
    analyzer = VolumeConsistencyAnalyzer(
        window_duration=args.window,
        consistency_threshold_db=args.threshold
    )

    results = analyzer.analyze(
        args.audio_file,
        visualize=not args.no_visualize,
        extract_best=not args.no_extract
    )

    return 0


if __name__ == '__main__':
    exit(main())
```

---

## Quick Start Guide

### Installation

```bash
# Install required libraries
pip install librosa pydub numpy matplotlib pyloudnorm

# Ensure ffmpeg is installed
ffmpeg -version
```

### Basic Usage

```bash
# Analyze a music track
python volume_consistency_analyzer.py background_music.mp3

# Custom parameters
python volume_consistency_analyzer.py music.mp3 --window 15 --threshold 2.5

# Analysis only (no extraction/visualization)
python volume_consistency_analyzer.py music.mp3 --no-extract --no-visualize
```

### Python Integration

```python
from volume_consistency_analyzer import VolumeConsistencyAnalyzer

# Create analyzer
analyzer = VolumeConsistencyAnalyzer(
    window_duration=10.0,
    consistency_threshold_db=3.0
)

# Run analysis
results = analyzer.analyze("background_music.mp3")

# Access results
best_section = results['consistent_sections'][0]
print(f"Best section: {best_section['start']:.1f}s - {best_section['end']:.1f}s")
```

---

## Summary

### Key Takeaways

1. **Use RMS for fast consistency detection** (variance < 3 dB over 10s windows)
2. **Use LUFS for accurate loudness measurement** (range < 3 LU for consistency)
3. **Combine metrics for best results** (RMS for speed + LUFS for accuracy)
4. **Avoid intro/outro sections** (typically 10-20% of track duration)
5. **Target middle sections** (highest consistency, best for looping)

### Recommended Thresholds

| Metric | Excellent | Good | Acceptable | Dynamic |
|--------|-----------|------|------------|---------|
| RMS Variance | < 1.5 dB | < 3.0 dB | < 5.0 dB | >= 5.0 dB |
| RMS Std Dev | < 1.0 dB | < 2.0 dB | < 3.0 dB | >= 3.0 dB |
| LUFS Range | < 2.0 LU | < 3.0 LU | < 5.0 LU | >= 5.0 LU |

### Best Practices

1. **Analyze in 10-second windows** (good balance between accuracy and granularity)
2. **Use 50% overlap** (better detection of section boundaries)
3. **Require minimum 30-second sections** (long enough for meaningful use)
4. **Prefer sections scoring 85+** (very consistent, excellent for background)
5. **Visualize results** (helps verify automated decisions)

---

## Sources

- [Understanding LUFS | The Key To Consistent Audio Loudness 2025](https://mixingmonster.com/understanding-lufs/)
- [LUFS: The Key to Getting Loud Tracks in 2025 - EDMProd](https://www.edmprod.com/lufs/)
- [LUFS vs RMS: A Simple Guide for Music Producers](https://mixelite.com/blog/lufs-vs-rms/)
- [LUFS Vs RMS - What's the Difference - Music Guy Mixing](https://www.musicguymixing.com/lufs-vs-rms/)
- [LUFS vs RMS: Which One to Use and Why?](https://emastered.com/blog/lufs-vs-rms)
- [Everything You Need To Know About Loudness LUFS vs. RMS vs. dBFS](https://mrmixandmaster.com/loudness-lufs-vs-rms-vs-dbfs/)
