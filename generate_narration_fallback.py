#!/usr/bin/env python3
"""Fallback narration generator using gTTS (Google Text-to-Speech)"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_with_gtts():
    """Generate narration using Google Text-to-Speech fallback"""
    try:
        from gtts import gTTS

        # Read script
        with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
            content = f.read()

        # Extract script
        script = content[200:2500]
        logger.info(f"Script extracted: {len(script)} characters")

        # Generate with Google TTS
        logger.info("Generating narration with Google TTS (free fallback)...")
        tts = gTTS(text=script, lang='en', slow=False)

        # Save
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "narration.mp3"

        tts.save(str(output_file))

        file_size = output_file.stat().st_size
        logger.info(f"SUCCESS: Narration saved to {output_file}")
        logger.info(f"File size: {file_size} bytes")
        logger.info(f"Cost: FREE (Google TTS)")

        return True

    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == "__main__":
    try:
        from gtts import gTTS
        logger.info("Using gTTS for narration generation...")
        success = generate_with_gtts()
        exit(0 if success else 1)
    except ImportError:
        logger.info("Installing gTTS...")
        import subprocess
        subprocess.run(['pip', 'install', '-q', 'gtts'], check=True)
        success = generate_with_gtts()
        exit(0 if success else 1)
