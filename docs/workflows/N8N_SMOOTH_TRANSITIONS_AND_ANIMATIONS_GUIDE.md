# N8N Video: Smooth Transitions and Animations Guide

## Overview
This guide provides the best, simplest ways to add professional smooth transitions and subtle animations between N8N video scenes without significantly increasing file size.

---

## Table of Contents
1. [FFmpeg Transition Filters](#ffmpeg-transition-filters)
2. [Ken Burns Effect (Recommended)](#ken-burns-effect-recommended)
3. [Advanced Transition Combinations](#advanced-transition-combinations)
4. [File Size Optimization](#file-size-optimization)
5. [Python Implementation Examples](#python-implementation-examples)
6. [Quick Reference Commands](#quick-reference-commands)

---

## FFmpeg Transition Filters

### 1. Fade Transition (Simplest & Fastest)
**Best for:** Scene changes, infographic transitions, start/end

**FFmpeg Filter:**
```bash
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=29.5:d=0.5" output.mp4
```

**Parameters:**
- `fade=t=in:st=0:d=0.5` - Fade in for 0.5 seconds from start
- `fade=t=out:st=29.5:d=0.5` - Fade out for 0.5 seconds at end (at 30-second mark)
- `d=0.5` - Duration in seconds (0.3-0.8 recommended for subtle effect)

**File Size Impact:** Minimal (1-2%)

---

### 2. Dissolve Transition (Smooth Cross-fade)
**Best for:** Between infographics, scene-to-scene transitions

**FFmpeg Filter:**
```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v]trim=end=29.5:d=29.5[a]; \
                   [1:v]trim=start=0:d=0.5[b]; \
                   [a][b]blend=all_mode=overlay:all_opacity=0.5[blend]; \
                   [blend]fade=t=out:d=0.5[out]" \
  -map "[out]" output.mp4
```

**Simplified: Use xfade for video concat**
```bash
ffmpeg -f concat -safe 0 -i clips.txt -vf xfade=transition=dissolve:duration=0.5:offset=29.5 output.mp4
```

**File Size Impact:** Minimal (1-2%)

---

### 3. Zoom/Pan (Ken Burns Effect) - RECOMMENDED
**Best for:** Static infographics, keeping viewer engaged

**FFmpeg Filter - Subtle Zoom:**
```bash
ffmpeg -loop 1 -i infographic.png -c:v libx264 -t 30 \
  -vf "scale=1920:1080,zoompan=z=1.0025:d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1920x1080,fps=24" \
  output.mp4
```

**Parameters Explained:**
- `z=1.0025` - Zoom factor (0.25% zoom per second, very subtle)
  - `z=1.001` - Ultra-subtle (1% total over 30 sec)
  - `z=1.005` - Subtle (5% total over 30 sec)
  - `z=1.01` - Noticeable (10% total over 30 sec)
- `d=1` - Duration per pan step (1 frame at 24fps)
- `x=iw/2-(iw/zoom/2)` - Horizontal centering
- `y=ih/2-(ih/zoom/2)` - Vertical centering
- `s=1920x1080` - Output size

**File Size Impact:** Minimal (0-1%, uses H.264 encoding)

---

### 4. Slide Transition
**Best for:** Infographic transitions, directional movement

**Slide Left:**
```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "xfade=transition=slideright:duration=0.5:offset=29.5" \
  output.mp4
```

**Available slide directions:**
- `slideleft`, `slideright`, `slideup`, `slidedown`
- `duration=0.5` (0.3-1.0 seconds recommended)

**File Size Impact:** Minimal (1-2%)

---

### 5. Wipe Transition
**Best for:** Professional scene transitions, info reveals

**Horizontal Wipe:**
```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "xfade=transition=wipeleft:duration=0.5:offset=29.5" \
  output.mp4
```

**Available wipe directions:**
- `wipeleft`, `wiperight`, `wipeup`, `wipedown`

**File Size Impact:** Minimal (1-2%)

---

## Ken Burns Effect (RECOMMENDED)

### Why Ken Burns for N8N Videos?
- Smooth, subtle, very professional
- Prevents viewer "image fatigue" on static infographics
- Minimal file size increase
- Easy to implement with FFmpeg
- Works on single images (no need for video sequences)

### Simple Ken Burns Implementation

**Subtle version (30-second segment):**
```bash
ffmpeg -loop 1 -i infographic.png \
  -c:v libx264 -t 30 -crf 23 \
  -vf "scale=1920:1080,zoompan=z=1.001:d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1920x1080,fps=24" \
  -c:a aac -b:a 128k \
  output.mp4
```

**Medium version (more noticeable):**
```bash
ffmpeg -loop 1 -i infographic.png \
  -c:v libx264 -t 30 -crf 23 \
  -vf "scale=1920:1080,zoompan=z=1.005:d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1920x1080,fps=24" \
  -c:a aac -b:a 128k \
  output.mp4
```

**Aggressive version (pan + zoom):**
```bash
ffmpeg -loop 1 -i infographic.png \
  -c:v libx264 -t 30 -crf 23 \
  -vf "scale=1920:1080,zoompan=z=1.01:d=1:x=iw/2-(iw/zoom/2)+50*sin(t)*2:y=ih/2-(ih/zoom/2)+30*cos(t),fps=24" \
  -c:a aac -b:a 128k \
  output.mp4
```

---

## Advanced Transition Combinations

### Professional Fade + Ken Burns Sequence

**Single command for complete N8N segment:**
```bash
ffmpeg -loop 1 -i intro.png -i content.png -i outro.png \
  -filter_complex "[0]scale=1920:1080,fade=t=in:d=0.3:alpha=1[intro]; \
                   [1]scale=1920:1080,zoompan=z=1.003:d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1920x1080,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st=27:d=0.3:alpha=1[content]; \
                   [2]scale=1920:1080,fade=t=in:d=0.3:alpha=1[outro]; \
                   [intro][content][outro]concat=n=3" \
  -c:v libx264 -crf 23 -t 90 \
  output.mp4
```

### Dissolve Between Infographics

**Using xfade for seamless transitions:**
```bash
# Create clips list file (clips.txt):
# file 'clip1.mp4'
# file 'clip2.mp4'
# file 'clip3.mp4'

ffmpeg -f concat -safe 0 -i clips.txt \
  -vf "xfade=transition=fade:duration=0.5:offset=29.5,xfade=transition=fade:duration=0.5:offset=59.5" \
  -c:v libx264 -crf 23 output.mp4
```

---

## File Size Optimization

### Video Parameters That Keep File Size Small

**Best Settings for N8N Videos:**
```bash
ffmpeg -i input.mp4 \
  -c:v libx264 \           # H.264 codec (universal, efficient)
  -crf 23 \                # Quality (18-28, 23 = good balance)
  -preset fast \           # Encoding speed (fast, medium, slow)
  -c:a aac \               # Audio codec
  -b:a 192k \              # Audio bitrate (128-192 recommended)
  -movflags +faststart \   # Enable streaming
  output.mp4
```

**File Size Estimates:**
- 1920x1080, 24fps, 30 seconds, Ken Burns: ~8-12 MB
- 1920x1080, 24fps, 30 seconds, fade transition: ~7-10 MB
- 1920x1080, 24fps, 30 seconds, static (no effects): ~7-9 MB

**For 3-minute video (180 seconds):**
- Estimated size: 45-75 MB (without compression)
- With `-crf 23`: 35-50 MB
- With `-crf 28`: 25-35 MB

### Compression Settings Comparison

| Setting | Quality | File Size | Encoding Time |
|---------|---------|-----------|----------------|
| `-crf 18` | Very High | 60-80 MB | Slow (5+ min) |
| `-crf 23` | High | 40-50 MB | Medium (2-3 min) |
| `-crf 28` | Good | 25-35 MB | Fast (1-2 min) |

---

## Python Implementation Examples

### Example 1: Simple Fade Transitions Between Clips

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path

def add_fade_transitions(input_clips: list, output_path: str,
                         fade_duration: float = 0.5):
    """
    Add fade transitions between video clips.

    Args:
        input_clips: List of video file paths
        output_path: Output video file path
        fade_duration: Duration of fade effect in seconds
    """

    # Create clips list file
    clips_file = Path(output_path).parent / "clips.txt"
    with open(clips_file, 'w') as f:
        for clip in input_clips:
            f.write(f"file '{clip}'\n")

    # Calculate offsets for xfade
    # Each clip is 30 seconds (example), so offset is 29.5
    clip_duration = 30
    offset = clip_duration - fade_duration

    # Build filter for multiple fades
    num_clips = len(input_clips)
    xfade_filters = []
    for i in range(num_clips - 1):
        offset_time = offset + (i * clip_duration)
        xfade_filters.append(
            f"xfade=transition=fade:duration={fade_duration}:offset={offset_time}"
        )

    filter_string = ",".join(xfade_filters)

    # FFmpeg command
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(clips_file),
        '-vf', filter_string,
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        output_path
    ]

    subprocess.run(cmd, check=True)
    clips_file.unlink()  # Cleanup
    print(f"Video with fade transitions: {output_path}")


# Usage
clips = [
    "output/clip1.mp4",
    "output/clip2.mp4",
    "output/clip3.mp4"
]
add_fade_transitions(clips, "output/final_with_fades.mp4", fade_duration=0.5)
```

---

### Example 2: Ken Burns Animation on Static Infographics

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path

def apply_ken_burns_to_image(image_path: str, duration: int,
                             output_path: str, zoom_level: float = 1.003):
    """
    Apply Ken Burns effect (subtle zoom + pan) to static image.

    Args:
        image_path: Path to input image
        duration: Duration in seconds
        output_path: Output video file path
        zoom_level: Zoom factor per second
                   1.001 = ultra-subtle
                   1.003 = subtle
                   1.005 = moderate
                   1.01 = aggressive
    """

    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_path,
        '-c:v', 'libx264',
        '-t', str(duration),
        '-crf', '23',
        '-vf', (
            f'scale=1920:1080,'
            f'zoompan=z={zoom_level}:d=1:'
            f'x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):'
            f's=1920x1080,fps=24'
        ),
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"Ken Burns video: {output_path}")


# Usage examples
apply_ken_burns_to_image(
    "images/n8n_intro.png",
    duration=15,
    output_path="output/intro_with_ken_burns.mp4",
    zoom_level=1.001  # Ultra-subtle
)

apply_ken_burns_to_image(
    "images/n8n_features.png",
    duration=30,
    output_path="output/features_with_ken_burns.mp4",
    zoom_level=1.003  # Subtle
)
```

---

### Example 3: Complete N8N Video with Multiple Transitions

```python
#!/usr/bin/env python3
import subprocess
import json
from pathlib import Path
from datetime import datetime

def create_n8n_video_with_smooth_transitions(
    infographics_dir: str,
    narration_audio: str,
    background_music: str,
    output_path: str,
    music_volume: float = 0.15
):
    """
    Create N8N video with smooth transitions between infographics.

    Timeline structure:
    - Fade in intro (0.3s)
    - Intro infographic with Ken Burns (15s)
    - Fade transition (0.5s)
    - Content infographics with Ken Burns (each 20-30s)
    - Fade transition (0.5s)
    - Outro with fade out (0.3s)
    """

    infographics = [
        {"file": f"{infographics_dir}/intro.png", "duration": 15},
        {"file": f"{infographics_dir}/features.png", "duration": 30},
        {"file": f"{infographics_dir}/benefits.png", "duration": 30},
        {"file": f"{infographics_dir}/scalability.png", "duration": 30},
        {"file": f"{infographics_dir}/outro.png", "duration": 10},
    ]

    # Generate temporary video files with Ken Burns
    temp_files = []
    total_duration = 0

    for idx, infographic in enumerate(infographics):
        temp_file = f"temp_kenburns_{idx}.mp4"
        duration = infographic["duration"]

        # Apply Ken Burns effect
        cmd = [
            'ffmpeg', '-y',
            '-loop', '1',
            '-i', infographic["file"],
            '-c:v', 'libx264',
            '-crf', '23',
            '-t', str(duration),
            '-vf', (
                f'scale=1920:1080,'
                f'zoompan=z=1.003:d=1:'
                f'x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):'
                f's=1920x1080,fps=24'
            ),
            temp_file
        ]

        subprocess.run(cmd, check=True, capture_output=True)
        temp_files.append(temp_file)
        total_duration += duration

    # Create concat file with fade transitions
    concat_file = "concat_list.txt"
    with open(concat_file, 'w') as f:
        for temp_file in temp_files:
            f.write(f"file '{temp_file}'\n")

    # Concatenate with fade transitions
    fade_duration = 0.5
    offsets = []
    current_time = 0
    for duration in [inf["duration"] for inf in infographics[:-1]]:
        offsets.append(current_time + duration - fade_duration)
        current_time += duration

    xfade_filters = [
        f"xfade=transition=fade:duration={fade_duration}:offset={offset}"
        for offset in offsets
    ]
    filter_string = ",".join(xfade_filters)

    temp_video = "temp_concatenated.mp4"
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_file,
        '-vf', filter_string,
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        temp_video
    ]

    subprocess.run(cmd, check=True, capture_output=True)

    # Mix audio (narration + background music)
    mixed_audio = "temp_mixed_audio.wav"
    cmd = [
        'ffmpeg', '-y',
        '-i', narration_audio,
        '-i', background_music,
        '-filter_complex',
        f'[0]volume=1.0[narration];[1]volume={music_volume}[music];'
        f'[narration][music]amix=inputs=2:duration=first[out]',
        '-map', '[out]',
        '-c:a', 'pcm_s16le',
        '-t', str(int(total_duration)),
        mixed_audio
    ]

    subprocess.run(cmd, check=True, capture_output=True)

    # Final video with audio
    cmd = [
        'ffmpeg', '-y',
        '-i', temp_video,
        '-i', mixed_audio,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        output_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)

    # Cleanup temp files
    for f in temp_files + [concat_file, temp_video, mixed_audio]:
        Path(f).unlink(missing_ok=True)

    # Get final stats
    import os
    size_mb = os.path.getsize(output_path) / (1024 * 1024)

    print(f"\n{'='*60}")
    print("N8N Video with Smooth Transitions Complete!")
    print(f"{'='*60}")
    print(f"Output: {output_path}")
    print(f"Duration: {total_duration} seconds")
    print(f"Size: {size_mb:.1f} MB")
    print(f"Transitions: Fade (0.5s between each segment)")
    print(f"Animation: Ken Burns (subtle zoom)")
    print(f"Audio: Narration + {music_volume*100:.0f}% background music")


# Usage
create_n8n_video_with_smooth_transitions(
    infographics_dir="output/n8n_infographics",
    narration_audio="output/n8n_narration.wav",
    background_music="background_music/bg_track.mp3",
    output_path="output/n8n_3min_with_transitions.mp4",
    music_volume=0.15
)
```

---

## Quick Reference Commands

### Most Used Commands for N8N Videos

**1. Apply Ken Burns to single image (30 seconds):**
```bash
ffmpeg -loop 1 -i image.png -c:v libx264 -t 30 -crf 23 \
  -vf "scale=1920:1080,zoompan=z=1.003:d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1920x1080,fps=24" \
  output.mp4
```

**2. Concatenate with fade transitions:**
```bash
ffmpeg -f concat -safe 0 -i clips.txt \
  -vf "xfade=transition=fade:duration=0.5:offset=29.5" \
  -c:v libx264 -crf 23 output.mp4
```

**3. Fade in + Ken Burns + Fade out:**
```bash
ffmpeg -loop 1 -i image.png -c:v libx264 -t 30 -crf 23 \
  -vf "scale=1920:1080,fade=t=in:d=0.3,zoompan=z=1.003:d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1920x1080,fps=24,fade=t=out:st=29.7:d=0.3" \
  output.mp4
```

**4. Add background music (15% volume):**
```bash
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a]volume=1.0[narration];[1:a]volume=0.15[music];[narration][music]amix=inputs=2:duration=first[out]" \
  -map 0:v -map "[out]" -c:v copy -c:a aac output.mp4
```

---

## Transition Selection Guide for N8N Content

| Scene Type | Recommended Transition | Duration | Why |
|-----------|----------------------|----------|-----|
| Intro to Features | Fade | 0.3-0.5s | Professional start |
| Feature to Feature | Fade | 0.5s | Smooth, not distracting |
| Feature to Benefit | Slide | 0.5-0.7s | Directional emphasis |
| Section to Section | Dissolve | 0.5s | Seamless flow |
| Infographic on screen | Ken Burns | Full duration | Keeps static images alive |
| Outro fade | Fade out | 0.5-1.0s | Professional ending |

---

## Testing & Validation

### Checklist Before Publishing
- [ ] Transitions smooth (not jarring)
- [ ] Audio syncs with video transitions
- [ ] File size acceptable (< 100 MB for 3-minute video)
- [ ] Video plays on YouTube without glitches
- [ ] Ken Burns effect not too aggressive (viewer distraction check)
- [ ] Fade duration matches audio timing

### Quick Quality Check
```bash
# Check video properties
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of default=noprint_wrappers=1:nokey=1 output.mp4

# Check audio properties
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels -of default=noprint_wrappers=1:nokey=1 output.mp4
```

---

## Summary: Best Approach for N8N Videos

### Recommended Implementation Stack

1. **For Static Infographics:** Ken Burns effect (z=1.003)
2. **Between Scenes:** Fade transitions (0.5 seconds)
3. **Audio:** Narration (100%) + background music (15%)
4. **Encoding:** H.264, CRF 23, 24fps for smooth playback
5. **Final Size Target:** 50-75 MB for 3-minute video

### Why This Works
- **Professional appearance:** Subtle animations and smooth transitions
- **Minimal file size:** H.264 + appropriate CRF keeps videos manageable
- **Easy to implement:** Single FFmpeg commands, Python scripts available
- **YouTube friendly:** Universal codec support, great streaming quality
- **Viewer engagement:** Motion prevents "static image fatigue" on long videos

---

## Additional Resources

### FFmpeg Transition Filter Reference
- `fade` - Simple fade in/out
- `xfade` - Cross-fade between videos
- `zoompan` - Ken Burns effect (zoom + pan)
- `scale` - Resize video
- `fps` - Frame rate adjustment
- `hflip`, `vflip` - Horizontal/vertical flip

### File Size Tips
1. Use `-crf 23` for balance (18-28 range)
2. Reduce audio bitrate to 128k for background music
3. Keep resolution at 1920x1080 (standard for YouTube)
4. Use `-preset fast` for reasonable encoding times

### Performance Notes
- Ken Burns: ~10 MB per 30 seconds
- Fade transition: ~0.5 MB overhead
- Total overhead for smooth transitions: < 5% file size increase

