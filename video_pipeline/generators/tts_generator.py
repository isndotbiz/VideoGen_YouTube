"""
TTS Generator using ElevenLabs API
Generates narration audio from text scripts
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiohttp
import hashlib

logger = logging.getLogger(__name__)


class TTSGenerator:
    """Generate narration audio using ElevenLabs TTS"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize TTS generator

        Args:
            config: Configuration dictionary with ElevenLabs settings
        """
        self.api_key = config.get("api_key")
        if not self.api_key:
            raise ValueError("ElevenLabs API key is required")

        self.voice_id = config.get("voice_id", "21m00Tcm4TlvDq8ikWAM")
        self.model = config.get("model", "eleven_turbo_v2")
        self.output_dir = Path(config.get("output_dir", "outputs/audio"))

        # Voice settings
        self.stability = config.get("stability", 0.5)
        self.similarity_boost = config.get("similarity_boost", 0.75)
        self.style = config.get("style", 0.0)
        self.use_speaker_boost = config.get("use_speaker_boost", True)

        self.base_url = "https://api.elevenlabs.io/v1"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def list_voices(self) -> List[Dict[str, Any]]:
        """
        List available voices

        Returns:
            List of voice information dictionaries

        Raises:
            RuntimeError: If API request fails
        """
        headers = {
            "xi-api-key": self.api_key
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/voices",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(
                            f"Failed to list voices: {response.status} - {error_text}"
                        )

                    data = await response.json()
                    voices = data.get("voices", [])

                    logger.info(f"Retrieved {len(voices)} available voices")
                    return voices

        except aiohttp.ClientError as e:
            raise RuntimeError(f"ElevenLabs API request failed: {e}")

    async def generate_audio(self, text: str, voice_id: Optional[str] = None,
                           output_filename: Optional[str] = None) -> Path:
        """
        Generate audio from text

        Args:
            text: Text to convert to speech
            voice_id: Optional voice ID (uses default if not provided)
            output_filename: Optional output filename

        Returns:
            Path to generated audio file

        Raises:
            RuntimeError: If generation fails
        """
        voice_id = voice_id or self.voice_id

        logger.info(f"Generating audio with voice {voice_id}: '{text[:100]}...'")

        # Prepare request payload
        payload = {
            "text": text,
            "model_id": self.model,
            "voice_settings": {
                "stability": self.stability,
                "similarity_boost": self.similarity_boost,
                "style": self.style,
                "use_speaker_boost": self.use_speaker_boost
            }
        }

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/text-to-speech/{voice_id}",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(
                            f"ElevenLabs API error: {response.status} - {error_text}"
                        )

                    audio_data = await response.read()

                    # Generate filename if not provided
                    if not output_filename:
                        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                        output_filename = f"narration_{text_hash}.mp3"

                    output_path = self.output_dir / output_filename
                    with open(output_path, 'wb') as f:
                        f.write(audio_data)

                    logger.info(f"Audio saved to {output_path} ({len(audio_data)} bytes)")
                    return output_path

        except aiohttp.ClientError as e:
            raise RuntimeError(f"ElevenLabs API request failed: {e}")

    async def generate_audio_batch(self, texts: List[str],
                                  voice_id: Optional[str] = None,
                                  max_concurrent: int = 3) -> List[Path]:
        """
        Generate multiple audio files in parallel

        Args:
            texts: List of texts to convert to speech
            voice_id: Optional voice ID (uses default if not provided)
            max_concurrent: Maximum concurrent API requests

        Returns:
            List of paths to generated audio files
        """
        voice_id = voice_id or self.voice_id

        # Create semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)

        async def generate_with_semaphore(text: str, index: int) -> tuple[int, Path]:
            async with semaphore:
                logger.info(f"Starting audio generation {index + 1}/{len(texts)}")
                try:
                    filename = f"narration_{index:03d}.mp3"
                    path = await self.generate_audio(text, voice_id, filename)
                    return (index, path)
                except Exception as e:
                    logger.error(f"Failed to generate audio {index + 1}: {e}")
                    raise

        # Generate all audio files
        tasks = [
            generate_with_semaphore(text, i)
            for i, text in enumerate(texts)
        ]

        results = await asyncio.gather(*tasks)

        # Sort by index and extract paths
        results.sort(key=lambda x: x[0])
        paths = [path for _, path in results]

        logger.info(f"Generated {len(paths)} audio files successfully")
        return paths

    async def get_audio_duration(self, audio_path: Path) -> float:
        """
        Get duration of audio file in seconds

        Args:
            audio_path: Path to audio file

        Returns:
            Duration in seconds

        Note:
            This requires ffprobe or similar tool to be installed
        """
        try:
            import subprocess
            import json

            result = subprocess.run(
                [
                    "ffprobe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    str(audio_path)
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)
                duration = float(data["format"]["duration"])
                logger.debug(f"Audio duration: {duration}s for {audio_path.name}")
                return duration
            else:
                logger.warning(f"Failed to get audio duration for {audio_path}")
                return 0.0

        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Cannot determine audio duration: {e}")
            return 0.0

    async def estimate_duration(self, text: str, words_per_minute: int = 150) -> float:
        """
        Estimate audio duration based on text length

        Args:
            text: Text to estimate duration for
            words_per_minute: Average speaking rate

        Returns:
            Estimated duration in seconds
        """
        word_count = len(text.split())
        duration = (word_count / words_per_minute) * 60
        return duration


if __name__ == "__main__":
    # Test TTS generator
    import sys
    import os

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    async def test():
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            print("ERROR: ELEVENLABS_API_KEY environment variable not set!")
            print("Set it with: export ELEVENLABS_API_KEY='your_key_here'")
            sys.exit(1)

        config = {
            "api_key": api_key,
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel voice
            "model": "eleven_turbo_v2",
            "output_dir": "outputs/audio/test",
            "stability": 0.5,
            "similarity_boost": 0.75
        }

        generator = TTSGenerator(config)

        # List available voices
        print("\nListing available voices...")
        try:
            voices = await generator.list_voices()
            print(f"\nFound {len(voices)} voices:")
            for voice in voices[:5]:  # Show first 5
                print(f"  - {voice['name']} (ID: {voice['voice_id']})")
        except Exception as e:
            print(f"Failed to list voices: {e}")

        # Generate test audio
        print("\nGenerating test narration...")
        test_text = (
            "Welcome to this AI-generated video. "
            "In this demonstration, we showcase the power of text-to-speech "
            "technology combined with advanced video generation capabilities."
        )

        try:
            audio_path = await generator.generate_audio(test_text)
            print(f"\nSuccess! Audio saved to: {audio_path}")

            duration = await generator.get_audio_duration(audio_path)
            if duration > 0:
                print(f"Audio duration: {duration:.2f} seconds")

        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)

    asyncio.run(test())
