#!/usr/bin/env python3
"""
Professional Claude Code vs Codex Narration Generator
Generates clean, high-quality audio from expanded script using ElevenLabs v2.0
"""

import os
import re
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('narration_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def clean_text_for_narration(text: str) -> str:
    """
    Clean and prepare text for TTS narration.
    Removes markdown formatting, visual cues, and problematic characters.

    Args:
        text: Raw script text with markdown/annotations

    Returns:
        Clean text ready for professional narration
    """
    logger.info("Cleaning text for narration...")

    # Remove markdown headers
    text = re.sub(r'^#+\s+.*$', '', text, flags=re.MULTILINE)

    # Remove visual/editing cues in brackets
    text = re.sub(r'\[VISUAL:.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\[PAUSE:.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\[EMPHASIS:.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\[B-ROLL:.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)

    # Remove timestamp markers
    text = re.sub(r'\(\d{1,2}:\d{2}-\d{1,2}:\d{2}\)', '', text)

    # Remove markdown bold/italic
    text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'\1', text)  # Bold+italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)      # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)          # Italic
    text = re.sub(r'__([^_]+)__', r'\1', text)          # Underline bold
    text = re.sub(r'_([^_]+)_', r'\1', text)            # Underline

    # Remove section dividers
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^===+$', '', text, flags=re.MULTILINE)

    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', '', text)

    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)

    # Remove metadata lines (key: value format)
    text = re.sub(r'^\*\*[^:]+:\*\*.*$', '', text, flags=re.MULTILINE)

    # Clean up quotes - normalize to standard double quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")

    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)

    # Remove multiple newlines (keep paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Remove empty lines at start and end
    text = text.strip()

    logger.info(f"Text cleaned: {len(text)} characters remaining")
    return text


def extract_narration_script(file_path: str) -> str:
    """
    Extract the full narration script from the VIDEO_SCRIPTS_ALL_VARIATIONS.md file.
    Focuses on Script 1 (Full Version) which contains the complete 17-minute narration.

    Args:
        file_path: Path to the script file

    Returns:
        Extracted narration text
    """
    logger.info(f"Reading script from: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract Script 1: Full Version section (everything until Script 2 or end)
        # Look for the intro section start and continue until we hit Script 2
        intro_match = re.search(r'## INTRO SECTION', content, re.IGNORECASE)
        if not intro_match:
            logger.warning("Could not find INTRO SECTION, using full content")
            return content

        start_pos = intro_match.start()

        # Find where Script 2 starts (if it exists)
        script2_match = re.search(r'# SCRIPT 2:', content, re.IGNORECASE)
        if script2_match:
            end_pos = script2_match.start()
        else:
            # If no Script 2, take a reasonable amount (first ~15000 chars after intro)
            end_pos = min(start_pos + 15000, len(content))

        script_text = content[start_pos:end_pos]
        logger.info(f"Extracted script: {len(script_text)} characters")

        return script_text

    except FileNotFoundError:
        logger.error(f"Script file not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading script: {e}")
        raise


def generate_narration_with_elevenlabs(text: str, output_path: str) -> dict:
    """
    Generate professional narration using ElevenLabs v2.0 API.

    Args:
        text: Clean narration text
        output_path: Where to save the audio file

    Returns:
        Dictionary with audio metadata
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not set in environment")

    try:
        from elevenlabs import ElevenLabs

        # Initialize client with API key
        client = ElevenLabs(api_key=api_key)
        logger.info("ElevenLabs client initialized")

        # Voice configuration
        # Using professional, clear voices for narration
        # Rachel (21m00Tcm4TlvDq8ikWAM) - Professional female voice
        # Or use Adam (pNInz6obpgDQGcFmaJgB) - Professional male voice
        voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel - clear, professional
        model_id = "eleven_multilingual_v2"  # Latest multilingual model

        logger.info(f"Generating narration...")
        logger.info(f"Voice: Rachel (Professional Female)")
        logger.info(f"Model: {model_id}")
        logger.info(f"Text length: {len(text)} characters")
        logger.info(f"Estimated words: {len(text.split())}")

        # Generate audio with optimal settings for clarity
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            voice_settings={
                "stability": 0.65,        # Natural variation (0.6-0.7 range)
                "similarity_boost": 0.75,  # Voice clarity
                "style": 0.0,              # Neutral style
                "use_speaker_boost": True  # Enhanced clarity
            }
        )

        # Create output directory
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save audio stream
        logger.info(f"Saving audio to: {output_path}")
        bytes_written = 0

        with open(output_file, 'wb') as f:
            for chunk in audio_generator:
                if chunk:
                    f.write(chunk)
                    bytes_written += len(chunk)

        # Calculate metadata
        file_size_mb = bytes_written / (1024 * 1024)
        estimated_duration_seconds = len(text.split()) / 2.5  # ~150 WPM = 2.5 words/sec
        estimated_duration_minutes = estimated_duration_seconds / 60

        metadata = {
            "file_path": str(output_file.absolute()),
            "file_size_bytes": bytes_written,
            "file_size_mb": round(file_size_mb, 2),
            "text_length": len(text),
            "word_count": len(text.split()),
            "estimated_duration_seconds": round(estimated_duration_seconds, 1),
            "estimated_duration_minutes": round(estimated_duration_minutes, 1),
            "voice": "Rachel (Professional Female)",
            "model": model_id,
            "voice_settings": {
                "stability": 0.65,
                "similarity_boost": 0.75,
                "style": 0.0,
                "speaker_boost": True
            },
            "generation_time": datetime.now().isoformat()
        }

        logger.info("=" * 60)
        logger.info("NARRATION GENERATION COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"Output file: {output_path}")
        logger.info(f"File size: {metadata['file_size_mb']} MB")
        logger.info(f"Text length: {metadata['text_length']} characters")
        logger.info(f"Word count: {metadata['word_count']} words")
        logger.info(f"Estimated duration: {metadata['estimated_duration_minutes']} minutes")
        logger.info(f"Voice: {metadata['voice']}")
        logger.info(f"Model: {metadata['model']}")
        logger.info("=" * 60)

        return metadata

    except ImportError:
        logger.error("ElevenLabs library not installed. Run: pip install elevenlabs")
        raise
    except Exception as e:
        logger.error(f"Error generating narration: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Main execution function"""
    try:
        logger.info("=" * 60)
        logger.info("CLAUDE CODE VS CODEX - NARRATION GENERATOR")
        logger.info("=" * 60)

        # File paths
        script_file = "VIDEO_SCRIPTS_ALL_VARIATIONS.md"
        output_file = "output/narration_enhanced.mp3"

        # Step 1: Extract script
        logger.info("\nStep 1: Extracting narration script...")
        raw_text = extract_narration_script(script_file)

        # Step 2: Clean text
        logger.info("\nStep 2: Cleaning text for narration...")
        clean_text = clean_text_for_narration(raw_text)

        # Validate we have content
        if len(clean_text) < 100:
            raise ValueError("Cleaned text too short - check extraction logic")

        # Save cleaned script for reference
        debug_output = Path("output/narration_script_cleaned.txt")
        debug_output.parent.mkdir(parents=True, exist_ok=True)
        with open(debug_output, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        logger.info(f"Cleaned script saved to: {debug_output}")

        # Step 3: Generate audio
        logger.info("\nStep 3: Generating professional narration...")
        metadata = generate_narration_with_elevenlabs(clean_text, output_file)

        # Step 4: Save metadata
        metadata_file = Path("output/narration_metadata.txt")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write("NARRATION METADATA\n")
            f.write("=" * 60 + "\n\n")
            for key, value in metadata.items():
                if isinstance(value, dict):
                    f.write(f"{key}:\n")
                    for k, v in value.items():
                        f.write(f"  {k}: {v}\n")
                else:
                    f.write(f"{key}: {value}\n")
        logger.info(f"Metadata saved to: {metadata_file}")

        logger.info("\n" + "=" * 60)
        logger.info("ALL TASKS COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        logger.info(f"\nOutput audio: {output_file}")
        logger.info(f"Cleaned script: {debug_output}")
        logger.info(f"Metadata: {metadata_file}")

        return True

    except Exception as e:
        logger.error(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
