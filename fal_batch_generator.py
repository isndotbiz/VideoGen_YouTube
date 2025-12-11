#!/usr/bin/env python3
"""
FAL.ai Batch Image Generator for Flux
Generates multiple images using FAL.ai API
"""

import json
import time
import logging
import sys
import os
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FALBatchGenerator:
    def __init__(self):
        self.api_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
        if not self.api_key:
            raise ValueError("FAL_API_KEY not set in environment")

        self.output_dir = Path("./output/generated_images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set FAL_KEY for the client library
        os.environ["FAL_KEY"] = self.api_key

        # Initialize FAL client
        try:
            import fal_client
            self.client = fal_client
            logger.info(f"FAL.ai client initialized with API key")
        except ImportError:
            logger.error("fal_client not installed. Run: pip install fal-client")
            sys.exit(1)

    def generate_image(self, prompt: str, seed: int, output_path: str) -> bool:
        """Generate single image via FAL.ai"""
        try:
            logger.info(f"Generating: {output_path}")

            # Call FAL.ai Flux model with correct API
            result = self.client.run(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": prompt,
                    "seed": seed,
                    "image_size": "landscape_16_9",
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5,
                }
            )

            # Download image
            if "images" in result and result["images"]:
                import requests
                img_url = result["images"][0]["url"]

                response = requests.get(img_url, timeout=30)
                if response.status_code == 200:
                    # Save as PNG
                    output_file = self.output_dir / Path(output_path).name
                    output_file.write_bytes(response.content)
                    logger.info(f"Saved: {output_file} ({len(response.content)} bytes)")
                    return True
            else:
                logger.error(f"No images in response: {result}")
                return False

        except Exception as e:
            logger.error(f"Error generating {output_path}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def load_prompts(self, filepath: str) -> List[Dict]:
        """Load prompts from JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data.get('prompts', [])

    def generate_batch(self, prompts: List[Dict]) -> int:
        """Generate all images"""
        successful = 0

        for i, prompt_data in enumerate(prompts, 1):
            logger.info(f"\n[{i}/{len(prompts)}] {prompt_data.get('name', 'Image ' + str(i))}")

            # Use 'prompt' field, fallback to other common names
            prompt_text = prompt_data.get('prompt') or prompt_data.get('text') or prompt_data.get('description')

            if not prompt_text:
                logger.error(f"  No prompt text found")
                continue

            seed = prompt_data.get('seed', 42 + i)
            output_file = f"flux_{seed:03d}.png"

            if self.generate_image(prompt_text, seed, output_file):
                successful += 1
            else:
                logger.error(f"  Failed to generate")

            # Rate limiting - FAL.ai has generous limits but be respectful
            if i < len(prompts):
                time.sleep(1)

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
        logger.info(f"Total cost: ${successful * 0.001:.2f} (FAL.ai)")
        logger.info("="*60)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="FAL.ai Flux Batch Generator")
    parser.add_argument("--prompts", default="prompts.json", help="Prompts JSON file")
    parser.add_argument("--output", default="./output/generated_images", help="Output directory")

    args = parser.parse_args()

    try:
        generator = FALBatchGenerator()
        generator.output_dir = Path(args.output)
        generator.output_dir.mkdir(parents=True, exist_ok=True)

        # Load prompts
        if not Path(args.prompts).exists():
            logger.error(f"Prompts file not found: {args.prompts}")
            sys.exit(1)

        prompts = generator.load_prompts(args.prompts)
        logger.info(f"Loaded {len(prompts)} prompts from {args.prompts}")
        logger.info(f"Estimated cost: ${len(prompts) * 0.001:.2f}")
        logger.info(f"Estimated time: {len(prompts)} minutes\n")

        # Generate all images
        successful = generator.generate_batch(prompts)
        generator.print_stats(len(prompts), successful)

        sys.exit(0 if successful == len(prompts) else 1)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
