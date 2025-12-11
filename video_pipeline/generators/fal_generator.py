"""
FAL.ai Image Generator
Fallback image generation using FAL.ai API
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiohttp

logger = logging.getLogger(__name__)


class FALGenerator:
    """Generate images using FAL.ai API as fallback"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize FAL generator

        Args:
            config: Configuration dictionary with FAL settings
        """
        self.api_key = config.get("api_key")
        if not self.api_key:
            raise ValueError("FAL API key is required")

        self.model = config.get("model", "fal-ai/flux/schnell")
        self.image_size = config.get("image_size", {"width": 1024, "height": 1024})
        self.num_inference_steps = config.get("num_inference_steps", 4)
        self.output_dir = Path(config.get("output_dir", "outputs/images/fal_fallback"))
        self.base_url = "https://fal.run"

        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_image(self, prompt: str, seed: Optional[int] = None) -> Path:
        """
        Generate a single image using FAL.ai

        Args:
            prompt: Text prompt for image generation
            seed: Random seed (None for random)

        Returns:
            Path to generated image

        Raises:
            RuntimeError: If generation fails
        """
        logger.info(f"Generating image with FAL.ai: '{prompt[:100]}...'")

        # Prepare request payload
        payload = {
            "prompt": prompt,
            "image_size": self.image_size,
            "num_inference_steps": self.num_inference_steps,
            "num_images": 1
        }

        if seed is not None:
            payload["seed"] = seed

        headers = {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                # Submit generation request
                async with session.post(
                    f"{self.base_url}/{self.model}",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise RuntimeError(
                            f"FAL.ai API error: {response.status} - {error_text}"
                        )

                    result = await response.json()

                    # Extract image URL
                    images = result.get("images", [])
                    if not images:
                        raise RuntimeError("No images returned from FAL.ai")

                    image_url = images[0].get("url")
                    if not image_url:
                        raise RuntimeError("No image URL in FAL.ai response")

                    logger.debug(f"Image generated, downloading from {image_url}")

                    # Download image
                    async with session.get(image_url) as img_response:
                        if img_response.status != 200:
                            raise RuntimeError(
                                f"Failed to download image: {img_response.status}"
                            )

                        image_data = await img_response.read()

                        # Save image
                        import time
                        filename = f"fal_{int(time.time())}_{hash(prompt) % 10000}.png"
                        output_path = self.output_dir / filename

                        with open(output_path, 'wb') as f:
                            f.write(image_data)

                        logger.info(f"Image saved to {output_path}")
                        return output_path

        except aiohttp.ClientError as e:
            raise RuntimeError(f"FAL.ai API request failed: {e}")

    async def generate_images_batch(self, prompts: List[str],
                                   seeds: Optional[List[int]] = None,
                                   max_concurrent: int = 5) -> List[Path]:
        """
        Generate multiple images in parallel

        Args:
            prompts: List of text prompts
            seeds: Optional list of seeds (same length as prompts)
            max_concurrent: Maximum concurrent API requests

        Returns:
            List of paths to generated images
        """
        if seeds and len(seeds) != len(prompts):
            raise ValueError("Seeds list must match prompts list length")

        seeds = seeds or [None] * len(prompts)

        # Create semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)

        async def generate_with_semaphore(prompt: str, seed: Optional[int],
                                         index: int) -> tuple[int, Path]:
            async with semaphore:
                logger.info(f"Starting FAL.ai generation {index + 1}/{len(prompts)}")
                try:
                    path = await self.generate_image(prompt, seed)
                    return (index, path)
                except Exception as e:
                    logger.error(f"Failed to generate image {index + 1}: {e}")
                    raise

        # Generate all images
        tasks = [
            generate_with_semaphore(prompt, seed, i)
            for i, (prompt, seed) in enumerate(zip(prompts, seeds))
        ]

        results = await asyncio.gather(*tasks)

        # Sort by index and extract paths
        results.sort(key=lambda x: x[0])
        paths = [path for _, path in results]

        logger.info(f"Generated {len(paths)} images successfully with FAL.ai")
        return paths


if __name__ == "__main__":
    # Test FAL generator
    import sys
    import os

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    async def test():
        api_key = os.getenv("FAL_API_KEY")
        if not api_key:
            print("ERROR: FAL_API_KEY environment variable not set!")
            print("Set it with: export FAL_API_KEY='your_key_here'")
            sys.exit(1)

        config = {
            "api_key": api_key,
            "model": "fal-ai/flux/schnell",
            "image_size": {"width": 1024, "height": 1024},
            "num_inference_steps": 4,
            "output_dir": "outputs/images/fal_test"
        }

        generator = FALGenerator(config)

        # Generate test image
        try:
            image_path = await generator.generate_image(
                prompt="A futuristic city at night with neon lights, cyberpunk style",
                seed=12345
            )
            print(f"\nSuccess! Image saved to: {image_path}")

        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)

    asyncio.run(test())
