"""
ComfyUI Image Generator
Handles local image generation using ComfyUI with Flux Turbo
"""

import asyncio
import json
import logging
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiohttp
import websockets
from PIL import Image
import io

logger = logging.getLogger(__name__)


class ComfyUIGenerator:
    """Generate images using local ComfyUI instance"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ComfyUI generator

        Args:
            config: Configuration dictionary with ComfyUI settings
        """
        self.host = config.get("host", "127.0.0.1")
        self.port = config.get("port", 8188)
        self.base_url = f"http://{self.host}:{self.port}"
        self.ws_url = f"ws://{self.host}:{self.port}/ws"
        self.timeout = config.get("timeout", 300)
        self.max_retries = config.get("max_retries", 3)
        self.output_dir = Path(config.get("output_dir", "outputs/images"))
        self.workflow_path = Path(config.get("workflow_path", "workflows/flux_turbo.json"))

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client_id = str(uuid.uuid4())

    async def check_connection(self) -> bool:
        """
        Check if ComfyUI server is accessible

        Returns:
            True if server is accessible, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/system_stats", timeout=5) as response:
                    if response.status == 200:
                        logger.info(f"ComfyUI server is accessible at {self.base_url}")
                        return True
                    else:
                        logger.warning(f"ComfyUI server returned status {response.status}")
                        return False
        except Exception as e:
            logger.error(f"Cannot connect to ComfyUI server: {e}")
            return False

    def load_workflow(self, workflow_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load ComfyUI workflow from JSON file

        Args:
            workflow_path: Path to workflow JSON file

        Returns:
            Workflow dictionary

        Raises:
            FileNotFoundError: If workflow file doesn't exist
            json.JSONDecodeError: If workflow file is invalid
        """
        path = workflow_path or self.workflow_path

        if not path.exists():
            raise FileNotFoundError(f"Workflow file not found: {path}")

        with open(path, 'r') as f:
            workflow = json.load(f)

        logger.debug(f"Loaded workflow from {path}")
        return workflow

    def update_workflow_prompt(self, workflow: Dict[str, Any], prompt: str,
                               seed: Optional[int] = None) -> Dict[str, Any]:
        """
        Update workflow with new prompt and seed

        Args:
            workflow: Base workflow dictionary
            prompt: Text prompt for image generation
            seed: Random seed (None for random)

        Returns:
            Updated workflow dictionary
        """
        # Deep copy to avoid modifying original
        import copy
        updated = copy.deepcopy(workflow)

        # Find text prompt nodes (typically CLIPTextEncode nodes)
        for node_id, node in updated.items():
            if node.get("class_type") == "CLIPTextEncode":
                if "inputs" in node and "text" in node["inputs"]:
                    node["inputs"]["text"] = prompt
                    logger.debug(f"Updated prompt in node {node_id}")

            # Find KSampler or similar nodes for seed
            if seed is not None and node.get("class_type") in ["KSampler", "KSamplerAdvanced"]:
                if "inputs" in node and "seed" in node["inputs"]:
                    node["inputs"]["seed"] = seed
                    logger.debug(f"Updated seed to {seed} in node {node_id}")

        return updated

    async def queue_prompt(self, workflow: Dict[str, Any]) -> str:
        """
        Queue a prompt for generation

        Args:
            workflow: Workflow dictionary to queue

        Returns:
            Prompt ID

        Raises:
            aiohttp.ClientError: If request fails
        """
        payload = {
            "prompt": workflow,
            "client_id": self.client_id
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/prompt",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise aiohttp.ClientError(
                        f"Failed to queue prompt: {response.status} - {error_text}"
                    )

                result = await response.json()
                prompt_id = result.get("prompt_id")

                if not prompt_id:
                    raise ValueError("No prompt_id returned from ComfyUI")

                logger.info(f"Queued prompt with ID: {prompt_id}")
                return prompt_id

    async def wait_for_completion(self, prompt_id: str) -> Dict[str, Any]:
        """
        Wait for prompt completion via WebSocket

        Args:
            prompt_id: ID of the queued prompt

        Returns:
            Generation result data

        Raises:
            TimeoutError: If generation exceeds timeout
            RuntimeError: If generation fails
        """
        start_time = time.time()

        try:
            async with websockets.connect(f"{self.ws_url}?clientId={self.client_id}") as ws:
                logger.info(f"Connected to ComfyUI WebSocket for prompt {prompt_id}")

                while True:
                    # Check timeout
                    if time.time() - start_time > self.timeout:
                        raise TimeoutError(
                            f"Image generation exceeded timeout of {self.timeout}s"
                        )

                    # Receive message
                    try:
                        message = await asyncio.wait_for(ws.recv(), timeout=10)
                        data = json.loads(message)
                    except asyncio.TimeoutError:
                        # No message in 10s, continue waiting
                        continue

                    msg_type = data.get("type")

                    # Progress update
                    if msg_type == "progress":
                        progress = data.get("data", {})
                        value = progress.get("value", 0)
                        max_value = progress.get("max", 100)
                        percentage = (value / max_value * 100) if max_value > 0 else 0
                        logger.info(f"Generation progress: {percentage:.1f}%")

                    # Execution started
                    elif msg_type == "execution_start":
                        exec_prompt_id = data.get("data", {}).get("prompt_id")
                        if exec_prompt_id == prompt_id:
                            logger.info(f"Execution started for prompt {prompt_id}")

                    # Execution complete
                    elif msg_type == "executing":
                        exec_data = data.get("data", {})
                        exec_prompt_id = exec_data.get("prompt_id")
                        node = exec_data.get("node")

                        if exec_prompt_id == prompt_id and node is None:
                            logger.info(f"Execution completed for prompt {prompt_id}")
                            return await self.get_history(prompt_id)

                    # Execution error
                    elif msg_type == "execution_error":
                        error_data = data.get("data", {})
                        exec_prompt_id = error_data.get("prompt_id")
                        if exec_prompt_id == prompt_id:
                            error_msg = error_data.get("exception_message", "Unknown error")
                            raise RuntimeError(f"Generation failed: {error_msg}")

        except websockets.exceptions.WebSocketException as e:
            raise RuntimeError(f"WebSocket error: {e}")

    async def get_history(self, prompt_id: str) -> Dict[str, Any]:
        """
        Get generation history for a prompt

        Args:
            prompt_id: Prompt ID

        Returns:
            History data
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/history/{prompt_id}") as response:
                if response.status != 200:
                    raise RuntimeError(f"Failed to get history: {response.status}")

                data = await response.json()
                return data.get(prompt_id, {})

    async def download_image(self, filename: str, subfolder: str = "",
                           folder_type: str = "output") -> Path:
        """
        Download generated image from ComfyUI

        Args:
            filename: Image filename
            subfolder: Subfolder in output directory
            folder_type: Folder type (output, input, temp)

        Returns:
            Path to downloaded image

        Raises:
            RuntimeError: If download fails
        """
        params = {
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/view", params=params) as response:
                if response.status != 200:
                    raise RuntimeError(
                        f"Failed to download image: {response.status}"
                    )

                image_data = await response.read()

                # Save image
                output_path = self.output_dir / filename
                with open(output_path, 'wb') as f:
                    f.write(image_data)

                logger.info(f"Downloaded image to {output_path}")
                return output_path

    async def generate_image(self, prompt: str, seed: Optional[int] = None,
                           workflow_path: Optional[Path] = None) -> Path:
        """
        Generate a single image

        Args:
            prompt: Text prompt for image generation
            seed: Random seed (None for random)
            workflow_path: Optional custom workflow path

        Returns:
            Path to generated image

        Raises:
            RuntimeError: If generation fails
        """
        logger.info(f"Generating image with prompt: '{prompt[:100]}...'")

        # Check connection
        if not await self.check_connection():
            raise RuntimeError("ComfyUI server is not accessible")

        # Load and update workflow
        workflow = self.load_workflow(workflow_path)
        workflow = self.update_workflow_prompt(workflow, prompt, seed)

        # Queue prompt
        prompt_id = await self.queue_prompt(workflow)

        # Wait for completion
        history = await self.wait_for_completion(prompt_id)

        # Extract output images
        outputs = history.get("outputs", {})
        image_info = None

        for node_output in outputs.values():
            if "images" in node_output and node_output["images"]:
                image_info = node_output["images"][0]
                break

        if not image_info:
            raise RuntimeError("No output images found in generation result")

        # Download image
        filename = image_info["filename"]
        subfolder = image_info.get("subfolder", "")
        image_path = await self.download_image(filename, subfolder)

        logger.info(f"Image generated successfully: {image_path}")
        return image_path

    async def generate_images_batch(self, prompts: List[str],
                                   seeds: Optional[List[int]] = None,
                                   max_concurrent: int = 3) -> List[Path]:
        """
        Generate multiple images in parallel

        Args:
            prompts: List of text prompts
            seeds: Optional list of seeds (same length as prompts)
            max_concurrent: Maximum concurrent generations

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
                logger.info(f"Starting generation {index + 1}/{len(prompts)}")
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

        logger.info(f"Generated {len(paths)} images successfully")
        return paths


if __name__ == "__main__":
    # Test ComfyUI generator
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    async def test():
        config = {
            "host": "127.0.0.1",
            "port": 8188,
            "output_dir": "outputs/images/test",
            "workflow_path": "workflows/flux_turbo.json",
            "timeout": 300
        }

        generator = ComfyUIGenerator(config)

        # Check connection
        connected = await generator.check_connection()
        if not connected:
            print("ERROR: ComfyUI server is not running!")
            print(f"Please start ComfyUI server at {generator.base_url}")
            sys.exit(1)

        # Generate test image
        try:
            image_path = await generator.generate_image(
                prompt="A beautiful sunset over mountains, highly detailed, 4k",
                seed=42
            )
            print(f"\nSuccess! Image saved to: {image_path}")

        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)

    asyncio.run(test())
