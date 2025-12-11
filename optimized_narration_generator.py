#!/usr/bin/env python3
"""Optimized narration generator with correct ElevenLabs API v2+"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_narration():
    """Generate narration using ElevenLabs"""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        logger.error("ELEVENLABS_API_KEY not set")
        return False

    try:
        from elevenlabs import client as elevenlabs_client

        # Read script
        with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
            content = f.read()

        # Extract script (first 2500 chars after header)
        script = content[200:2500]

        logger.info(f"Generating narration from {len(script)} character script...")
        logger.info("Voice: Rachel | Model: eleven_monolingual_v1")

        # Generate with correct API
        audio_generator = elevenlabs_client.generate(
            api_key=api_key,
            text=script,
            voice="Rachel",
            model="eleven_monolingual_v1"
        )

        # Save audio
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / "narration.mp3"
        bytes_written = 0

        with open(output_file, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
                bytes_written += len(chunk)

        logger.info(f"Narration saved: {output_file} ({bytes_written} bytes)")
        logger.info(f"Cost: ~$0.02")

        return True

    except Exception as e:
        logger.error(f"Narration generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_narration()
    exit(0 if success else 1)
