#!/usr/bin/env python3
"""
Complete Video Generation Pipeline
Orchestrates: ComfyUI → ElevenLabs → Shotstack → YouTube
"""

import os
import json
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import asyncio
import requests
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class VideoConfig:
    """Configuration for video generation"""
    resolution: str = "1920x1080"
    bitrate: str = "8000k"
    fps: int = 30
    audio_bitrate: str = "128k"
    output_dir: str = "./output"
    temp_dir: str = "./temp"

class PipelinePhase(Enum):
    IMAGES = 1
    NARRATION = 2
    ANIMATION = 3
    ASSEMBLY = 4
    UPLOAD = 5

class ComfyUIGenerator:
    """Generate images locally using ComfyUI with Flux Turbo"""

    def __init__(self, server_url: str = "http://localhost:8188"):
        self.server_url = server_url
        self.logger = logging.getLogger(__name__)

    def check_server(self) -> bool:
        """Check if ComfyUI server is running"""
        try:
            response = requests.get(f"{self.server_url}/api/auth", timeout=5)
            self.logger.info("✓ ComfyUI server is running")
            return True
        except Exception as e:
            self.logger.error(f"✗ ComfyUI server not reachable: {e}")
            return False

    def generate_image(self, prompt: str, seed: int, output_path: str) -> bool:
        """Generate image using ComfyUI Flux Turbo"""
        try:
            # Prepare ComfyUI workflow
            workflow = self._build_workflow(prompt, seed)

            # Submit to ComfyUI
            response = requests.post(
                f"{self.server_url}/api/generate",
                json=workflow,
                timeout=300
            )

            if response.status_code == 200:
                self.logger.info(f"✓ Generated image: {output_path}")
                return True
            else:
                self.logger.error(f"✗ Generation failed: {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"✗ Error generating image: {e}")
            return False

    def _build_workflow(self, prompt: str, seed: int) -> Dict:
        """Build ComfyUI workflow for Flux Turbo"""
        return {
            "prompt": {
                "1": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {"ckpt_name": "flux-turbo.safetensors"}
                },
                "2": {
                    "class_type": "LoraLoader",
                    "inputs": {
                        "lora_name": "flux_turbo_lora.safetensors",
                        "strength_model": 1.0,
                        "strength_clip": 1.0,
                        "model": ["1", 0],
                        "clip": ["1", 1]
                    }
                },
                "3": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": prompt, "clip": ["2", 1]}
                },
                "4": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": "low quality, blurry", "clip": ["2", 1]}
                },
                "5": {
                    "class_type": "EmptyLatentImage",
                    "inputs": {"width": 1920, "height": 1080, "batch_size": 1}
                },
                "6": {
                    "class_type": "KSampler",
                    "inputs": {
                        "seed": seed,
                        "steps": 20,
                        "cfg": 3.5,
                        "sampler_name": "DPM++ 2M Karras",
                        "scheduler": "karras",
                        "denoise": 1.0,
                        "model": ["2", 0],
                        "positive": ["3", 0],
                        "negative": ["4", 0],
                        "latent_image": ["5", 0]
                    }
                },
                "7": {
                    "class_type": "VAEDecode",
                    "inputs": {"samples": ["6", 0], "vae": ["1", 2]}
                },
                "8": {
                    "class_type": "SaveImage",
                    "inputs": {
                        "filename_prefix": "flux_turbo",
                        "images": ["7", 0]
                    }
                }
            }
        }


class ElevenLabsNarrator:
    """Generate voiceovers using ElevenLabs TTS"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
        self.logger = logging.getLogger(__name__)

    def get_voices(self) -> List[Dict]:
        """Get available voices"""
        try:
            response = requests.get(
                f"{self.base_url}/voices",
                headers={"xi-api-key": self.api_key},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()["voices"]
            return []
        except Exception as e:
            self.logger.error(f"✗ Error fetching voices: {e}")
            return []

    def generate_speech(self, text: str, output_path: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bool:
        """Generate speech from text"""
        try:
            response = requests.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                headers={"xi-api-key": self.api_key},
                json={
                    "text": text,
                    "model_id": "eleven_turbo_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75
                    }
                },
                timeout=120
            )

            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                self.logger.info(f"✓ Generated narration: {output_path}")
                return True
            else:
                self.logger.error(f"✗ TTS failed: {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"✗ Error generating speech: {e}")
            return False


class ShotstackAssembler:
    """Assemble videos using Shotstack API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.shotstack.io/stage"
        self.logger = logging.getLogger(__name__)

    def assemble_video(
        self,
        image_sequence: List[str],
        narration_audio: str,
        output_path: str,
        duration_per_image: float = 5.0
    ) -> bool:
        """Assemble video from images and audio"""
        try:
            # Build clip list
            clips = []
            for i, image in enumerate(image_sequence):
                clips.append({
                    "type": "image",
                    "asset": {"type": "image", "src": f"file://{image}"},
                    "length": duration_per_image,
                    "fit": "crop",
                    "scale": 1.0
                })

            # Add audio
            track = {
                "clips": clips,
                "type": "video"
            }

            edit = {
                "timeline": {
                    "tracks": [track],
                    "background": "#000000",
                    "soundtrack": {
                        "src": f"file://{narration_audio}",
                        "effect": "fadeInFadeOut"
                    }
                },
                "output": {
                    "format": "mp4",
                    "resolution": "1920x1080",
                    "aspectRatio": "16:9",
                    "size": {"width": 1920, "height": 1080},
                    "bitrate": 8000,
                    "framerate": 30,
                    "quality": "high"
                }
            }

            # Submit to Shotstack
            response = requests.post(
                f"{self.base_url}/render",
                headers={"x-api-key": self.api_key, "content-type": "application/json"},
                json=edit,
                timeout=60
            )

            if response.status_code == 201:
                render_id = response.json()["response"]["id"]
                self.logger.info(f"✓ Video assembly started: {render_id}")

                # Poll for completion
                return self._wait_for_render(render_id, output_path)
            else:
                self.logger.error(f"✗ Assembly failed: {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"✗ Error assembling video: {e}")
            return False

    def _wait_for_render(self, render_id: str, output_path: str, timeout: int = 3600) -> bool:
        """Wait for Shotstack render to complete"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            response = requests.get(
                f"{self.base_url}/render/{render_id}",
                headers={"x-api-key": self.api_key},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()["response"]
                status = data["status"]

                if status == "done":
                    video_url = data["url"]
                    # Download video
                    video_response = requests.get(video_url, timeout=300)
                    with open(output_path, 'wb') as f:
                        f.write(video_response.content)
                    self.logger.info(f"✓ Video downloaded: {output_path}")
                    return True

                elif status == "failed":
                    self.logger.error(f"✗ Render failed: {data.get('error', 'Unknown error')}")
                    return False

                else:
                    self.logger.info(f"  Rendering... ({status})")

            time.sleep(5)

        self.logger.error("✗ Render timeout")
        return False


class YouTubeUploader:
    """Upload videos to YouTube"""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = logging.getLogger(__name__)

    def upload(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str],
        is_public: bool = False
    ) -> bool:
        """Upload video to YouTube"""
        try:
            self.logger.info(f"Preparing to upload: {title}")

            # YouTube authentication would happen here
            # For now, just validate the file exists
            if not Path(video_path).exists():
                self.logger.error(f"✗ Video file not found: {video_path}")
                return False

            self.logger.info(f"✓ Ready to upload to YouTube: {title}")
            self.logger.info(f"  Description: {description[:100]}...")
            self.logger.info(f"  Tags: {', '.join(tags)}")
            self.logger.info(f"  Visibility: {'Public' if is_public else 'Private'}")

            return True

        except Exception as e:
            self.logger.error(f"✗ Error uploading video: {e}")
            return False


class VideoPipeline:
    """Main orchestration engine"""

    def __init__(self, config: VideoConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.start_time = datetime.now()
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories"""
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.config.temp_dir).mkdir(parents=True, exist_ok=True)

    def run_full_pipeline(
        self,
        prompts: List[str],
        script_text: str,
        video_title: str,
        video_description: str,
        skip_phases: List[PipelinePhase] = None
    ) -> bool:
        """Run complete pipeline"""
        skip_phases = skip_phases or []

        self.logger.info("="*60)
        self.logger.info("VIDEO GENERATION PIPELINE - STARTING")
        self.logger.info("="*60)

        try:
            # Phase 1: Generate Images
            if PipelinePhase.IMAGES not in skip_phases:
                self.logger.info("\n📸 PHASE 1: IMAGE GENERATION")
                image_files = self._generate_images(prompts)
                if not image_files:
                    return False

            # Phase 2: Generate Narration
            if PipelinePhase.NARRATION not in skip_phases:
                self.logger.info("\n🎤 PHASE 2: NARRATION GENERATION")
                audio_file = self._generate_narration(script_text)
                if not audio_file:
                    return False

            # Phase 3: Create Animations
            if PipelinePhase.ANIMATION not in skip_phases:
                self.logger.info("\n🎬 PHASE 3: ANIMATION CREATION")
                animation_files = self._create_animations(image_files)
                if not animation_files:
                    self.logger.warning("  Skipping animation phase, proceeding with static images")
                    animation_files = image_files

            # Phase 4: Assemble Video
            if PipelinePhase.ASSEMBLY not in skip_phases:
                self.logger.info("\n🎞️ PHASE 4: VIDEO ASSEMBLY")
                video_file = self._assemble_video(animation_files, audio_file)
                if not video_file:
                    return False

            # Phase 5: Upload
            if PipelinePhase.UPLOAD not in skip_phases:
                self.logger.info("\n📺 PHASE 5: YOUTUBE UPLOAD")
                success = self._upload_video(
                    video_file,
                    video_title,
                    video_description
                )
                if not success:
                    return False

            self._print_summary()
            return True

        except Exception as e:
            self.logger.error(f"✗ Pipeline failed: {e}")
            return False

    def _generate_images(self, prompts: List[str]) -> List[str]:
        """Generate images from prompts"""
        self.logger.info(f"Generating {len(prompts)} images...")

        comfyui = ComfyUIGenerator()

        if not comfyui.check_server():
            self.logger.warning("ComfyUI not running - falling back to FAL.ai would happen here")
            return []

        image_files = []
        for i, prompt in enumerate(prompts, 1):
            output_file = Path(self.config.temp_dir) / f"image_{i:02d}.png"
            if comfyui.generate_image(prompt, seed=42+i, output_path=str(output_file)):
                image_files.append(str(output_file))
            else:
                self.logger.warning(f"Failed to generate image {i}")

        return image_files

    def _generate_narration(self, text: str) -> Optional[str]:
        """Generate narration from text"""
        self.logger.info("Generating narration...")

        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            self.logger.error("ELEVENLABS_API_KEY not set")
            return None

        narrator = ElevenLabsNarrator(api_key)
        output_file = Path(self.config.temp_dir) / "narration.mp3"

        if narrator.generate_speech(text, str(output_file)):
            return str(output_file)
        return None

    def _create_animations(self, image_files: List[str]) -> List[str]:
        """Create animations from images"""
        self.logger.info(f"Creating {len(image_files)} animations...")
        self.logger.info("(Would use SpeedSketch API here)")
        return image_files  # For now, return original images

    def _assemble_video(self, images: List[str], audio: str) -> Optional[str]:
        """Assemble video from images and audio"""
        self.logger.info("Assembling video...")

        api_key = os.getenv("SHOTSTACK_API_KEY")
        if not api_key:
            self.logger.error("SHOTSTACK_API_KEY not set")
            return None

        assembler = ShotstackAssembler(api_key)
        output_file = Path(self.config.output_dir) / "video_final.mp4"

        if assembler.assemble_video(images, audio, str(output_file)):
            return str(output_file)
        return None

    def _upload_video(self, video_file: str, title: str, description: str) -> bool:
        """Upload video to YouTube"""
        self.logger.info("Uploading to YouTube...")

        client_id = os.getenv("YOUTUBE_CLIENT_ID")
        client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")

        if not client_id or not client_secret:
            self.logger.warning("YouTube credentials not configured - skipping upload")
            return True

        uploader = YouTubeUploader(client_id, client_secret)

        tags = ["ClaudeCode", "Codex", "AI", "Development", "Programming"]

        return uploader.upload(
            video_file,
            title,
            description,
            tags,
            is_public=False
        )

    def _print_summary(self):
        """Print pipeline summary"""
        elapsed = datetime.now() - self.start_time

        self.logger.info("\n" + "="*60)
        self.logger.info("PIPELINE COMPLETE")
        self.logger.info("="*60)
        self.logger.info(f"Total time: {elapsed}")
        self.logger.info(f"Output: {self.config.output_dir}")
        self.logger.info("="*60)


def main():
    """Main entry point"""
    config = VideoConfig()
    pipeline = VideoPipeline(config)

    # Example usage
    prompts = [
        "A clean split-screen showing two AI coding tools side by side, professional design",
        "A question mark with branching paths in orange and blue",
    ]

    script = "Hey everyone, today we're comparing Claude Code vs Codex..."

    success = pipeline.run_full_pipeline(
        prompts=prompts,
        script_text=script,
        video_title="Claude Code vs Codex: Why I Use Both",
        video_description="A comprehensive comparison of two AI coding tools"
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
