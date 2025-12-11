#!/usr/bin/env python3
"""WORKING ElevenLabs narration generator with correct API v2+"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_narration_working():
    """Generate narration using CORRECT ElevenLabs API v2+"""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        logger.error("ELEVENLABS_API_KEY not set in environment")
        return False

    try:
        from elevenlabs import ElevenLabs

        # Initialize client
        client = ElevenLabs(api_key=api_key)
        logger.info("ElevenLabs client initialized")

        # Read script
        with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
            content = f.read()

        # Extract script (first 2500 chars after header)
        script = content[200:2500]
        logger.info(f"Script extracted: {len(script)} characters")

        # Generate audio using CORRECT method: text_to_speech.convert()
        logger.info("Generating narration...")
        logger.info("Voice: Rachel | Model: eleven_monolingual_v1")

        audio = client.text_to_speech.convert(
            text=script,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice ID
            model_id="eleven_monolingual_v1"
        )

        # Save audio
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "narration.mp3"

        # Write binary data
        bytes_written = 0
        with open(output_file, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
                    bytes_written += len(chunk)

        logger.info(f"SUCCESS: Narration saved to {output_file}")
        logger.info(f"File size: {bytes_written} bytes")
        logger.info(f"Estimated cost: $0.02")

        return True

    except Exception as e:
        logger.error(f"ERROR generating narration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_narration_working()
    if success:
        logger.info("Narration generation COMPLETE!")
        exit(0)
    else:
        logger.error("Narration generation FAILED!")
        exit(1)
