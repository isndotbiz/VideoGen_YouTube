#!/usr/bin/env python3
"""
Enhanced FAL.ai Batch Image Generator
Production-ready batch image generation with:
- Parallel processing (3-4 concurrent requests)
- Comprehensive error handling and retry logic
- Progress tracking and performance metrics
- Metadata storage for each generated image
- 1920x1080 resolution with high quality settings
"""

import json
import time
import logging
import sys
import os
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import requests
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('batch_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ImageMetadata:
    """Metadata for generated image"""
    section: str
    image_number: int
    image_prompt: str
    description: str
    output_filename: str
    generation_time: float
    timestamp: str
    model: str = "fal-ai/flux/dev"
    resolution: str = "1920x1080"
    success: bool = True
    error_message: Optional[str] = None
    retry_count: int = 0


@dataclass
class GenerationStats:
    """Track generation statistics"""
    total: int = 0
    successful: int = 0
    failed: int = 0
    total_time: float = 0.0
    avg_time: float = 0.0
    total_retries: int = 0

    def update_avg_time(self):
        if self.successful > 0:
            self.avg_time = self.total_time / self.successful


class EnhancedFALBatchGenerator:
    """Production-ready FAL.ai batch image generator"""

    def __init__(
        self,
        output_dir: str = "./output/generated_images",
        max_workers: int = 4,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        timeout: int = 120
    ):
        """
        Initialize the batch generator

        Args:
            output_dir: Directory to save generated images
            max_workers: Number of concurrent generation tasks (3-4 recommended)
            max_retries: Maximum retry attempts per image
            retry_delay: Delay between retries in seconds
            timeout: Request timeout in seconds
        """
        # API setup
        self.api_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
        if not self.api_key:
            raise ValueError("FAL_API_KEY not found in environment variables")

        # Configuration
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_dir = self.output_dir / "metadata"
        self.metadata_dir.mkdir(exist_ok=True)

        self.max_workers = max_workers
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout

        # Statistics
        self.stats = GenerationStats()
        self.metadata_list: List[ImageMetadata] = []

        # Initialize FAL client
        os.environ["FAL_KEY"] = self.api_key
        try:
            import fal_client
            self.client = fal_client
            logger.info(f"FAL.ai client initialized successfully")
        except ImportError:
            logger.error("fal_client not installed. Run: pip install fal-client")
            sys.exit(1)

        logger.info(f"Enhanced FAL Batch Generator initialized:")
        logger.info(f"  Output directory: {self.output_dir}")
        logger.info(f"  Max workers: {self.max_workers}")
        logger.info(f"  Max retries: {self.max_retries}")
        logger.info(f"  Timeout: {self.timeout}s")

    def load_prompts(self, filepath: str) -> List[Dict]:
        """
        Load prompts from JSON file

        Expected structure:
        {
            "prompts": [
                {
                    "section": "Section Name",
                    "image_number": 1,
                    "image_prompt": "The actual prompt text",
                    "description": "Brief description"
                },
                ...
            ]
        }

        Args:
            filepath: Path to JSON file

        Returns:
            List of prompt dictionaries
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Support multiple JSON structures
            if 'prompts' in data:
                prompts = data['prompts']
            elif isinstance(data, list):
                prompts = data
            else:
                raise ValueError("Invalid JSON structure. Expected 'prompts' array or direct array")

            logger.info(f"Loaded {len(prompts)} prompts from {filepath}")
            return prompts

        except Exception as e:
            logger.error(f"Error loading prompts from {filepath}: {e}")
            raise

    def sanitize_filename(self, text: str, max_length: int = 50) -> str:
        """
        Sanitize text for use in filename

        Args:
            text: Text to sanitize
            max_length: Maximum length of output

        Returns:
            Sanitized filename component
        """
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '')

        # Replace spaces with underscores
        text = text.replace(' ', '_')

        # Truncate to max length
        if len(text) > max_length:
            text = text[:max_length]

        # Remove trailing underscores/dots
        text = text.rstrip('_.')

        return text or "image"

    def generate_filename(self, prompt_data: Dict) -> str:
        """
        Generate output filename from prompt data

        Format: {section_number}_{image_number}_{description}.png

        Args:
            prompt_data: Prompt dictionary

        Returns:
            Filename string
        """
        section = prompt_data.get('section', 'unknown')
        image_num = prompt_data.get('image_number') or prompt_data.get('id', 0)
        description = prompt_data.get('description') or prompt_data.get('name', 'image')

        # Sanitize components
        section_clean = self.sanitize_filename(section, 30)
        desc_clean = self.sanitize_filename(description, 40)

        # Create filename
        filename = f"{section_clean}_{image_num:03d}_{desc_clean}.png"

        return filename

    def generate_image_with_retry(
        self,
        prompt_data: Dict,
        attempt: int = 0
    ) -> Optional[ImageMetadata]:
        """
        Generate single image with retry logic

        Args:
            prompt_data: Dictionary containing prompt information
            attempt: Current retry attempt number

        Returns:
            ImageMetadata object or None if failed
        """
        # Extract prompt data
        prompt = (
            prompt_data.get('image_prompt') or
            prompt_data.get('prompt') or
            prompt_data.get('text', '')
        )

        if not prompt:
            logger.error(f"No prompt found in data: {prompt_data}")
            return None

        section = prompt_data.get('section', 'unknown')
        image_num = prompt_data.get('image_number') or prompt_data.get('id', 0)
        description = prompt_data.get('description') or prompt_data.get('name', 'Generated image')

        # Generate filename
        output_filename = self.generate_filename(prompt_data)
        output_path = self.output_dir / output_filename

        # Skip if already exists
        if output_path.exists() and output_path.stat().st_size > 0:
            logger.info(f"Skipping {output_filename} (already exists)")
            return ImageMetadata(
                section=section,
                image_number=image_num,
                image_prompt=prompt,
                description=description,
                output_filename=output_filename,
                generation_time=0.0,
                timestamp=datetime.now().isoformat(),
                success=True
            )

        start_time = time.time()

        try:
            logger.info(f"Generating: {output_filename} (attempt {attempt + 1}/{self.max_retries + 1})")

            # Call FAL.ai API with high quality settings
            result = self.client.run(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": prompt,
                    "image_size": {
                        "width": 1920,
                        "height": 1080
                    },
                    "num_inference_steps": 50,  # Higher for better quality
                    "guidance_scale": 7.5,       # Higher for prompt adherence
                    "num_images": 1,
                    "enable_safety_checker": False,
                    "output_format": "png"
                }
            )

            # Download and save image
            if "images" in result and result["images"]:
                img_url = result["images"][0]["url"]

                response = requests.get(img_url, timeout=self.timeout)
                response.raise_for_status()

                # Save image
                output_path.write_bytes(response.content)

                generation_time = time.time() - start_time

                logger.info(
                    f"[OK] Generated {output_filename} "
                    f"({len(response.content) / 1024:.1f} KB, {generation_time:.1f}s)"
                )

                # Create metadata
                metadata = ImageMetadata(
                    section=section,
                    image_number=image_num,
                    image_prompt=prompt,
                    description=description,
                    output_filename=output_filename,
                    generation_time=generation_time,
                    timestamp=datetime.now().isoformat(),
                    success=True,
                    retry_count=attempt
                )

                # Save metadata JSON
                metadata_path = self.metadata_dir / f"{output_filename}.json"
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(asdict(metadata), f, indent=2)

                return metadata
            else:
                raise Exception("No images in API response")

        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"✗ Error generating {output_filename}: {e}")

            # Retry logic
            if attempt < self.max_retries:
                wait_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                logger.info(f"Retrying in {wait_time:.1f}s...")
                time.sleep(wait_time)
                return self.generate_image_with_retry(prompt_data, attempt + 1)
            else:
                logger.error(f"Failed after {self.max_retries + 1} attempts: {output_filename}")

                # Create failed metadata
                metadata = ImageMetadata(
                    section=section,
                    image_number=image_num,
                    image_prompt=prompt,
                    description=description,
                    output_filename=output_filename,
                    generation_time=generation_time,
                    timestamp=datetime.now().isoformat(),
                    success=False,
                    error_message=str(e),
                    retry_count=attempt
                )

                return metadata

    def generate_batch_parallel(self, prompts: List[Dict]) -> GenerationStats:
        """
        Generate images in parallel using ThreadPoolExecutor

        Args:
            prompts: List of prompt dictionaries

        Returns:
            GenerationStats object
        """
        self.stats.total = len(prompts)
        start_time = time.time()

        logger.info(f"\n{'='*70}")
        logger.info(f"Starting parallel batch generation ({self.max_workers} workers)")
        logger.info(f"Total images: {len(prompts)}")
        logger.info(f"{'='*70}\n")

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_prompt = {
                executor.submit(self.generate_image_with_retry, prompt): prompt
                for prompt in prompts
            }

            # Process completed tasks with progress bar
            with tqdm(total=len(prompts), desc="Generating images") as pbar:
                for future in as_completed(future_to_prompt):
                    metadata = future.result()

                    if metadata:
                        self.metadata_list.append(metadata)

                        if metadata.success:
                            self.stats.successful += 1
                            self.stats.total_time += metadata.generation_time
                        else:
                            self.stats.failed += 1

                        self.stats.total_retries += metadata.retry_count
                    else:
                        self.stats.failed += 1

                    pbar.update(1)

        # Calculate final statistics
        total_elapsed = time.time() - start_time
        self.stats.update_avg_time()

        logger.info(f"\n{'='*70}")
        logger.info("Batch generation complete!")
        logger.info(f"{'='*70}")

        return self.stats

    def save_batch_metadata(self, output_file: str = "batch_metadata.json"):
        """
        Save metadata for all generated images

        Args:
            output_file: Output filename
        """
        output_path = self.output_dir / output_file

        batch_metadata = {
            "generated_at": datetime.now().isoformat(),
            "total_images": self.stats.total,
            "successful": self.stats.successful,
            "failed": self.stats.failed,
            "total_generation_time": self.stats.total_time,
            "avg_generation_time": self.stats.avg_time,
            "total_retries": self.stats.total_retries,
            "images": [asdict(m) for m in self.metadata_list]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(batch_metadata, f, indent=2)

        logger.info(f"Batch metadata saved to: {output_path}")

    def print_statistics(self):
        """Print detailed generation statistics"""
        logger.info(f"\n{'='*70}")
        logger.info("GENERATION STATISTICS")
        logger.info(f"{'='*70}")
        logger.info(f"Total images:           {self.stats.total}")
        logger.info(f"Successfully generated: {self.stats.successful} ({self.stats.successful/self.stats.total*100:.1f}%)")
        logger.info(f"Failed:                 {self.stats.failed} ({self.stats.failed/self.stats.total*100:.1f}%)")
        logger.info(f"Total retries:          {self.stats.total_retries}")
        logger.info(f"")
        logger.info(f"PERFORMANCE METRICS")
        logger.info(f"{'='*70}")
        logger.info(f"Total generation time:  {self.stats.total_time:.1f}s")
        logger.info(f"Average time per image: {self.stats.avg_time:.1f}s")

        if self.stats.successful > 0:
            logger.info(f"Throughput:             {self.stats.successful / self.stats.total_time:.2f} images/second")

        logger.info(f"")
        logger.info(f"OUTPUT")
        logger.info(f"{'='*70}")
        logger.info(f"Images directory:       {self.output_dir}")
        logger.info(f"Metadata directory:     {self.metadata_dir}")
        logger.info(f"")

        # Cost estimation (FAL.ai Flux Dev pricing)
        estimated_cost = self.stats.successful * 0.03  # $0.03 per image
        logger.info(f"Estimated cost:         ${estimated_cost:.2f} USD")
        logger.info(f"{'='*70}\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Enhanced FAL.ai Batch Image Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with default settings
  python enhanced_fal_batch_generator.py --prompts prompts.json

  # Generate with 6 parallel workers
  python enhanced_fal_batch_generator.py --prompts prompts.json --workers 6

  # Generate with custom output directory
  python enhanced_fal_batch_generator.py --prompts prompts.json --output ./my_images
        """
    )

    parser.add_argument(
        "--prompts",
        default="prompts.json",
        help="Path to JSON file containing image prompts (default: prompts.json)"
    )
    parser.add_argument(
        "--output",
        default="./output/generated_images",
        help="Output directory for generated images (default: ./output/generated_images)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4, recommended: 3-4)"
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum retry attempts per image (default: 3)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Request timeout in seconds (default: 120)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load prompts and show what would be generated without actually generating"
    )

    args = parser.parse_args()

    try:
        # Load prompts
        if not Path(args.prompts).exists():
            logger.error(f"Prompts file not found: {args.prompts}")
            sys.exit(1)

        # Initialize generator
        generator = EnhancedFALBatchGenerator(
            output_dir=args.output,
            max_workers=args.workers,
            max_retries=args.max_retries,
            timeout=args.timeout
        )

        # Load prompts
        prompts = generator.load_prompts(args.prompts)

        if args.dry_run:
            logger.info("\n=== DRY RUN MODE ===")
            logger.info(f"Would generate {len(prompts)} images:")
            for i, prompt in enumerate(prompts, 1):
                filename = generator.generate_filename(prompt)
                logger.info(f"  {i}. {filename}")
            logger.info(f"\nEstimated cost: ${len(prompts) * 0.03:.2f} USD")
            logger.info("Run without --dry-run to generate images")
            return

        # Show summary and confirm
        logger.info(f"\nReady to generate {len(prompts)} images")
        logger.info(f"Estimated cost: ${len(prompts) * 0.03:.2f} USD")
        logger.info(f"Parallel workers: {args.workers}")
        logger.info(f"Output directory: {args.output}\n")

        # Generate batch
        stats = generator.generate_batch_parallel(prompts)

        # Save metadata
        generator.save_batch_metadata()

        # Print statistics
        generator.print_statistics()

        # Exit with appropriate code
        sys.exit(0 if stats.failed == 0 else 1)

    except KeyboardInterrupt:
        logger.warning("\nGeneration interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
