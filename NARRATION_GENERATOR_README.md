# Claude Code vs Codex - Professional Narration Generator

## Overview

`claude_codex_narration_generator.py` generates high-quality professional narration audio from the expanded video script using ElevenLabs v2.0 API.

## Features

- Reads expanded narration script from `VIDEO_SCRIPTS_ALL_VARIATIONS.md`
- Intelligently cleans text by removing:
  - Markdown formatting (headers, bold, italic, code blocks)
  - Visual cues and annotations (VISUAL, PAUSE, EMPHASIS, B-ROLL)
  - Timestamp markers
  - URLs and metadata
  - Multiple formatting symbols (***)
- Generates professional audio using ElevenLabs v2.0:
  - Model: `eleven_multilingual_v2` (latest multilingual model)
  - Voice: Rachel (Professional Female) - clear, engaging
  - Speed: Natural (1.0x)
  - Stability: 0.65 for natural variation
  - Similarity Boost: 0.75 for clarity
  - Speaker Boost: Enabled for enhanced audio quality
- Comprehensive logging and metadata tracking

## Output Files

### Generated Files

1. **`output/narration_enhanced.mp3`** (6.35 MB)
   - Professional-quality audio narration
   - MP3 format, 128 kbps, 44.1 kHz, Mono
   - Approximately 6.8 minutes duration
   - Clean speech with no artifacts

2. **`output/narration_script_cleaned.txt`** (6.5 KB)
   - Plain text version of the narration script
   - All markdown and formatting removed
   - Ready for TTS processing
   - 1,017 words

3. **`output/narration_metadata.txt`** (529 bytes)
   - Complete audio metadata
   - File size and duration estimates
   - Voice settings and model info
   - Generation timestamp

4. **`narration_generation.log`** (3.4 KB)
   - Detailed execution log
   - Step-by-step processing info
   - Error tracking and debugging

## Usage

### Prerequisites

```bash
# Install required packages
pip install elevenlabs python-dotenv

# Set environment variable in .env
ELEVENLABS_API_KEY=your_api_key_here
```

### Run Script

```bash
python claude_codex_narration_generator.py
```

### Expected Output

```
============================================================
CLAUDE CODE VS CODEX - NARRATION GENERATOR
============================================================

Step 1: Extracting narration script...
Reading script from: VIDEO_SCRIPTS_ALL_VARIATIONS.md
Extracted script: 9264 characters

Step 2: Cleaning text for narration...
Cleaning text for narration...
Text cleaned: 6454 characters remaining
Cleaned script saved to: output\narration_script_cleaned.txt

Step 3: Generating professional narration...
ElevenLabs client initialized
Generating narration...
Voice: Rachel (Professional Female)
Model: eleven_multilingual_v2
Text length: 6454 characters
Estimated words: 1017

============================================================
NARRATION GENERATION COMPLETE!
============================================================
Output file: output/narration_enhanced.mp3
File size: 6.35 MB
Text length: 6454 characters
Word count: 1017 words
Estimated duration: 6.8 minutes
Voice: Rachel (Professional Female)
Model: eleven_multilingual_v2
============================================================
```

## Technical Details

### Text Cleaning Process

The script uses comprehensive regex patterns to remove:

1. **Markdown Headers**: `# Header`, `## Subheader`
2. **Visual Cues**: `[VISUAL: ...]`, `[PAUSE: ...]`, `[EMPHASIS: ...]`
3. **Timestamps**: `(0:00-1:30)`, `(1:00-3:00)`
4. **Formatting**: `***text***`, `**text**`, `*text*`, `__text__`, `_text_`
5. **Section Dividers**: `---`, `===`
6. **Code Blocks**: ` ```code``` `, `` `inline` ``
7. **URLs**: `https://...`, `http://...`
8. **Metadata**: `**Key:** Value` format
9. **Multiple Spaces/Newlines**: Normalized to single spaces and paragraph breaks

### Voice Settings

- **Stability (0.65)**: Provides natural voice variation while maintaining consistency
- **Similarity Boost (0.75)**: Enhances voice clarity and recognition
- **Style (0.0)**: Neutral, professional delivery
- **Speaker Boost (True)**: Enhanced audio quality and clarity

### Cost Estimate

- Approximately $0.30 per generation (1,017 words)
- Based on ElevenLabs pricing: ~$0.30 per 1,000 characters

## Integration with Video Pipeline

This script integrates with the broader video generation pipeline:

1. **Input**: `VIDEO_SCRIPTS_ALL_VARIATIONS.md` (expanded script)
2. **Output**: `output/narration_enhanced.mp3` (professional audio)
3. **Next Step**: Use audio in video assembly with Shotstack or FFmpeg

## Troubleshooting

### Common Issues

**Issue**: `ELEVENLABS_API_KEY not set in environment`
- **Solution**: Add your API key to `.env` file

**Issue**: `ElevenLabs library not installed`
- **Solution**: Run `pip install elevenlabs`

**Issue**: `Script file not found`
- **Solution**: Ensure `VIDEO_SCRIPTS_ALL_VARIATIONS.md` exists in project root

**Issue**: `Cleaned text too short`
- **Solution**: Check script extraction logic - may need to adjust regex patterns

### Debug Mode

Check these files for debugging:

1. `narration_generation.log` - Full execution log
2. `output/narration_script_cleaned.txt` - Verify text cleaning
3. `output/narration_metadata.txt` - Audio generation details

## Script Architecture

```
claude_codex_narration_generator.py
├── extract_narration_script()     # Extract Script 1 from markdown
├── clean_text_for_narration()     # Remove formatting/annotations
├── generate_narration_with_elevenlabs()  # Generate audio via API
└── main()                          # Orchestrate full pipeline
```

## Performance Metrics

- **Script Extraction**: < 1 second
- **Text Cleaning**: < 1 second
- **Audio Generation**: ~73 seconds (1.2 minutes)
- **Total Runtime**: ~75 seconds
- **Output Quality**: Professional broadcast quality

## Audio Quality

- **Format**: MP3, 128 kbps
- **Sample Rate**: 44.1 kHz
- **Channels**: Mono
- **Voice**: Professional female (Rachel)
- **Clarity**: High - with speaker boost enabled
- **Artifacts**: None - clean professional audio
- **Pacing**: Natural conversational pace (~150 WPM)

## Next Steps

After generating narration:

1. Review `output/narration_script_cleaned.txt` to verify text accuracy
2. Listen to `output/narration_enhanced.mp3` for quality check
3. Use audio file in video assembly pipeline
4. Sync with generated images and b-roll footage

## Related Files

- `elevenlabs_narration_WORKING.py` - Reference implementation
- `VIDEO_SCRIPTS_ALL_VARIATIONS.md` - Source script with full narration
- `AI_VIDEO_NARRATION_WITH_MARKERS.md` - Narration guidelines
- `.env` - Environment variables and API keys

## Version Info

- **Script Version**: 1.0
- **ElevenLabs API**: v2.0
- **Model**: eleven_multilingual_v2
- **Created**: 2025-12-10
- **Last Updated**: 2025-12-10
