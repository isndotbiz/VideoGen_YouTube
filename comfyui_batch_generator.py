#!/usr/bin/env python3
"""
ComfyUI Batch Image Generator for Flux Turbo
Generates multiple images from prompts using ComfyUI local server
"""

import json
import time
import requests
import logging
import sys
from pathlib import Path
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComfyUIBatchGenerator:
    def __init__(self, server_url: str = "http://localhost:8188"):
        self.server_url = server_url
        self.output_dir = Path("./generated_images")
        self.output_dir.mkdir(exist_ok=True)

    def check_server(self) -> bool:
        """Check if ComfyUI server is running"""
        try:
            response = requests.get(f"{self.server_url}/api/auth", timeout=5)
            logger.info(f"✓ ComfyUI server running at {self.server_url}")
            return True
        except Exception as e:
            logger.error(f"✗ Cannot connect to ComfyUI: {e}")
            logger.info(f"  Make sure ComfyUI is running: python main.py")
            return False

    def load_prompts(self, filepath: str) -> List[Dict]:
        """Load prompts from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data.get('prompts', [])

    def build_workflow(self, prompt: str, seed: int) -> Dict:
        """Build ComfyUI workflow for image generation"""
        return {
            "prompt": {
                "1": {"class_type": "CheckpointLoaderSimple", 
                      "inputs": {"ckpt_name": "flux-turbo.safetensors"}},
                "2": {"class_type": "LoraLoader",
                      "inputs": {"lora_name": "flux_turbo_lora.safetensors",
                                 "strength_model": 1.0, "strength_clip": 1.0,
                                 "model": ["1", 0], "clip": ["1", 1]}},
                "3": {"class_type": "CLIPTextEncode",
                      "inputs": {"text": prompt, "clip": ["2", 1]}},
                "4": {"class_type": "CLIPTextEncode",
                      "inputs": {"text": "low quality, blurry", "clip": ["2", 1]}},
                "5": {"class_type": "EmptyLatentImage",
                      "inputs": {"width": 1920, "height": 1080, "batch_size": 1}},
                "6": {"class_type": "KSampler",
                      "inputs": {"seed": seed, "steps": 20, "cfg": 3.5,
                                 "sampler_name": "DPM++ 2M Karras", "scheduler": "karras",
                                 "denoise": 1.0, "model": ["2", 0],
                                 "positive": ["3", 0], "negative": ["4", 0],
                                 "latent_image": ["5", 0]}},
                "7": {"class_type": "VAEDecode",
                      "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
                "8": {"class_type": "SaveImage",
                      "inputs": {"filename_prefix": f"flux_{seed:03d}", "images": ["7", 0]}}
            }
        }

    def submit_job(self, workflow: Dict) -> Optional[str]:
        """Submit workflow to ComfyUI"""
        try:
            response = requests.post(f"{self.server_url}/prompt", json=workflow, timeout=30)
            if response.status_code == 200:
                return response.json().get("prompt_id")
            else:
                logger.error(f"Failed to submit: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error submitting job: {e}")
            return None

    def wait_for_completion(self, prompt_id: str, timeout: int = 600) -> bool:
        """Wait for ComfyUI job to complete"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.server_url}/history/{prompt_id}", timeout=10)
                if response.status_code == 200:
                    if prompt_id in response.json():
                        logger.info(f"✓ Job {prompt_id} completed")
                        return True
            except Exception as e:
                logger.warning(f"Check status error: {e}")
            
            time.sleep(2)
        
        logger.error(f"Job {prompt_id} timed out")
        return False

    def generate_batch(self, prompts: List[Dict]) -> int:
        """Generate all images from prompts"""
        if not self.check_server():
            return 0

        successful = 0
        for i, prompt_data in enumerate(prompts, 1):
            logger.info(f"\n[{i}/{len(prompts)}] {prompt_data.get('name', 'Untitled')}")
            logger.info(f"  Prompt: {prompt_data['prompt'][:80]}...")

            workflow = self.build_workflow(
                prompt=prompt_data['prompt'],
                seed=prompt_data.get('seed', 42 + i)
            )

            job_id = self.submit_job(workflow)
            if not job_id:
                logger.error("  Failed to submit job")
                continue

            if self.wait_for_completion(job_id):
                successful += 1
            else:
                logger.error("  Job failed or timed out")

        return successful

    def print_stats(self, total: int, successful: int):
        """Print generation statistics"""
        logger.info("\n" + "="*60)
        logger.info(f"BATCH GENERATION COMPLETE")
        logger.info("="*60)
        logger.info(f"Total images requested: {total}")
        logger.info(f"Successfully generated: {successful}")
        logger.info(f"Failed: {total - successful}")
        logger.info(f"Success rate: {(successful/total*100):.1f}%")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info("="*60)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="ComfyUI Flux Turbo Batch Generator")
    parser.add_argument("--prompts", default="prompts.json", help="Prompts JSON file")
    parser.add_argument("--server", default="http://localhost:8188", help="ComfyUI server URL")
    parser.add_argument("--output", default="./generated_images", help="Output directory")

    args = parser.parse_args()

    generator = ComfyUIBatchGenerator(server_url=args.server)
    generator.output_dir = Path(args.output)
    generator.output_dir.mkdir(parents=True, exist_ok=True)

    # Load prompts
    if not Path(args.prompts).exists():
        logger.error(f"Prompts file not found: {args.prompts}")
        sys.exit(1)

    prompts = generator.load_prompts(args.prompts)
    logger.info(f"Loaded {len(prompts)} prompts from {args.prompts}")

    # Generate all images
    successful = generator.generate_batch(prompts)
    generator.print_stats(len(prompts), successful)

    sys.exit(0 if successful == len(prompts) else 1)


if __name__ == "__main__":
    main()
