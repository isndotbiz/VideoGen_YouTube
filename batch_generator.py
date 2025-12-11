#!/usr/bin/env python3
"""
Flux Turbo Batch Generator

Automates batch image generation using ComfyUI API with Flux Turbo model.
Reads prompts from prompts.json and submits them to a local ComfyUI server.

Requirements:
    pip install requests websocket-client pillow

Usage:
    python batch_generator.py
    python batch_generator.py --host localhost --port 8188
    python batch_generator.py --prompts custom_prompts.json
    python batch_generator.py --mode fast
"""

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

try:
    import requests
    import websocket
    from PIL import Image
    from io import BytesIO
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Install with: pip install requests websocket-client pillow")
    sys.exit(1)


class ComfyUIClient:
    """Client for interacting with ComfyUI API"""

    def __init__(self, host: str = "localhost", port: int = 8188):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{port}/ws"
        self.client_id = str(uuid.uuid4())

    def check_connection(self) -> bool:
        """Check if ComfyUI server is running"""
        try:
            response = requests.get(f"{self.base_url}/system_stats", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def load_workflow(self, workflow_path: str) -> Dict:
        """Load workflow JSON from file"""
        with open(workflow_path, 'r') as f:
            return json.load(f)

    def update_prompt(self, workflow: Dict, positive_prompt: str, negative_prompt: str = None) -> Dict:
        """Update the prompt in the workflow"""
        workflow_copy = json.loads(json.dumps(workflow))

        # Find and update positive prompt node (usually node 3)
        for node in workflow_copy['nodes']:
            if node['type'] == 'CLIPTextEncode' and node['id'] == 3:
                node['widgets_values'] = [positive_prompt]
            elif node['type'] == 'CLIPTextEncode' and node['id'] == 4 and negative_prompt:
                node['widgets_values'] = [negative_prompt]

        return workflow_copy

    def update_output_prefix(self, workflow: Dict, prefix: str) -> Dict:
        """Update the output filename prefix"""
        workflow_copy = json.loads(json.dumps(workflow))

        # Find SaveImage node (usually node 8)
        for node in workflow_copy['nodes']:
            if node['type'] == 'SaveImage':
                node['widgets_values'] = [prefix]
                break

        return workflow_copy

    def update_seed(self, workflow: Dict, seed: int = -1) -> Dict:
        """Update the seed for generation"""
        workflow_copy = json.loads(json.dumps(workflow))

        # Find KSampler node (usually node 6)
        for node in workflow_copy['nodes']:
            if node['type'] == 'KSampler':
                # Keep other settings, only update seed
                node['widgets_values'][0] = seed
                break

        return workflow_copy

    def update_generation_params(self, workflow: Dict, steps: int = None,
                                 cfg: float = None, width: int = None,
                                 height: int = None) -> Dict:
        """Update generation parameters"""
        workflow_copy = json.loads(json.dumps(workflow))

        for node in workflow_copy['nodes']:
            if node['type'] == 'KSampler' and (steps or cfg):
                if steps:
                    node['widgets_values'][2] = steps  # steps
                if cfg:
                    node['widgets_values'][3] = cfg    # cfg_scale
            elif node['type'] == 'EmptyLatentImage' and (width or height):
                if width:
                    node['widgets_values'][0] = width
                if height:
                    node['widgets_values'][1] = height

        return workflow_copy

    def queue_prompt(self, workflow: Dict) -> str:
        """Queue a prompt for generation"""
        prompt_data = {
            "prompt": workflow,
            "client_id": self.client_id
        }

        response = requests.post(f"{self.base_url}/prompt", json=prompt_data)
        if response.status_code != 200:
            raise Exception(f"Failed to queue prompt: {response.text}")

        return response.json()['prompt_id']

    def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
        """Download generated image"""
        params = {
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type
        }

        response = requests.get(f"{self.base_url}/view", params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to download image: {response.text}")

        return response.content

    def get_history(self, prompt_id: str) -> Dict:
        """Get generation history for a prompt"""
        response = requests.get(f"{self.base_url}/history/{prompt_id}")
        if response.status_code != 200:
            raise Exception(f"Failed to get history: {response.text}")

        return response.json()

    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> Dict:
        """Wait for a prompt to complete generation"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)

            if prompt_id in history:
                return history[prompt_id]

            time.sleep(1)

        raise TimeoutError(f"Generation timed out after {timeout} seconds")

    def get_output_images(self, prompt_id: str) -> List[Dict]:
        """Get output images from completed generation"""
        history = self.wait_for_completion(prompt_id)

        images = []
        if 'outputs' in history:
            for node_id, node_output in history['outputs'].items():
                if 'images' in node_output:
                    for image_data in node_output['images']:
                        images.append(image_data)

        return images


class BatchGenerator:
    """Manages batch image generation"""

    def __init__(self, client: ComfyUIClient, workflow_path: str, output_dir: str = "outputs"):
        self.client = client
        self.workflow_path = workflow_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Load base workflow
        self.base_workflow = client.load_workflow(workflow_path)

    def generate_single(self, prompt_data: Dict, output_name: str,
                       settings: Dict = None) -> Optional[str]:
        """Generate a single image from prompt data"""
        try:
            # Extract prompt text
            positive_prompt = prompt_data.get('text', '')
            negative_prompt = prompt_data.get('negative',
                'blurry, low quality, distorted, ugly, bad composition, watermark, text, signature')

            # Update workflow
            workflow = self.client.update_prompt(
                self.base_workflow,
                positive_prompt,
                negative_prompt
            )

            # Update output prefix
            workflow = self.client.update_output_prefix(workflow, output_name)

            # Apply custom settings if provided
            if settings:
                workflow = self.client.update_generation_params(
                    workflow,
                    steps=settings.get('steps'),
                    cfg=settings.get('cfg_scale'),
                    width=settings.get('width'),
                    height=settings.get('height')
                )

            # Queue the prompt
            print(f"Generating: {prompt_data.get('title', output_name)}")
            print(f"  Prompt: {positive_prompt[:80]}...")

            prompt_id = self.client.queue_prompt(workflow)
            print(f"  Queued with ID: {prompt_id}")

            # Wait for completion
            images = self.client.get_output_images(prompt_id)

            if not images:
                print("  WARNING: No images generated")
                return None

            # Download the first image
            image_data = images[0]
            image_bytes = self.client.get_image(
                image_data['filename'],
                image_data.get('subfolder', ''),
                image_data.get('type', 'output')
            )

            # Save to output directory
            output_path = self.output_dir / f"{output_name}.png"
            with open(output_path, 'wb') as f:
                f.write(image_bytes)

            print(f"  Saved to: {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"  ERROR: {e}")
            return None

    def generate_batch(self, prompts: List[Dict], settings: Dict = None,
                      start_index: int = 1) -> List[str]:
        """Generate multiple images from prompt list"""
        results = []
        total = len(prompts)

        print(f"\nStarting batch generation of {total} images...")
        print(f"Output directory: {self.output_dir.absolute()}\n")

        for i, prompt_data in enumerate(prompts, start=start_index):
            print(f"[{i}/{total}] ", end="")

            # Create output name with zero-padded index
            output_name = f"flux_turbo_{str(i).zfill(3)}"

            # Generate image
            output_path = self.generate_single(prompt_data, output_name, settings)
            results.append(output_path)

            # Brief pause between generations
            if i < total:
                time.sleep(0.5)

        print(f"\nBatch generation complete!")
        print(f"Successfully generated: {sum(1 for r in results if r)} / {total}")

        return results


def load_prompts(prompts_file: str) -> tuple[List[Dict], Dict]:
    """Load prompts from JSON file"""
    with open(prompts_file, 'r') as f:
        data = json.load(f)

    prompts = data.get('prompts', [])
    settings = data.get('generation_settings', {})

    return prompts, settings


def main():
    parser = argparse.ArgumentParser(description='Flux Turbo Batch Image Generator')
    parser.add_argument('--host', default='localhost', help='ComfyUI server host')
    parser.add_argument('--port', type=int, default=8188, help='ComfyUI server port')
    parser.add_argument('--workflow', default='flux_turbo_batch.json',
                       help='Workflow JSON file')
    parser.add_argument('--prompts', default='prompts.json',
                       help='Prompts JSON file')
    parser.add_argument('--output', default='outputs',
                       help='Output directory')
    parser.add_argument('--mode', choices=['fast', 'balanced', 'quality'],
                       default='balanced', help='Generation mode preset')
    parser.add_argument('--start', type=int, default=1,
                       help='Start index for output numbering')
    parser.add_argument('--limit', type=int, help='Limit number of images to generate')

    args = parser.parse_args()

    # Check if files exist
    if not os.path.exists(args.workflow):
        print(f"ERROR: Workflow file not found: {args.workflow}")
        sys.exit(1)

    if not os.path.exists(args.prompts):
        print(f"ERROR: Prompts file not found: {args.prompts}")
        sys.exit(1)

    # Initialize client
    print("Connecting to ComfyUI server...")
    client = ComfyUIClient(args.host, args.port)

    if not client.check_connection():
        print(f"ERROR: Cannot connect to ComfyUI server at {args.host}:{args.port}")
        print("Make sure ComfyUI is running with: python main.py")
        sys.exit(1)

    print("Connected successfully!\n")

    # Load prompts
    prompts, default_settings = load_prompts(args.prompts)

    # Apply mode preset
    mode_presets = {
        'fast': {'steps': 15, 'cfg_scale': 3.0},
        'balanced': {'steps': 20, 'cfg_scale': 3.5},
        'quality': {'steps': 30, 'cfg_scale': 4.0}
    }

    settings = {**default_settings, **mode_presets[args.mode]}

    print(f"Generation mode: {args.mode}")
    print(f"Settings: {settings}\n")

    # Limit prompts if requested
    if args.limit:
        prompts = prompts[:args.limit]

    # Create batch generator
    generator = BatchGenerator(client, args.workflow, args.output)

    # Generate batch
    results = generator.generate_batch(prompts, settings, args.start)

    # Print summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    print(f"Total requested: {len(prompts)}")
    print(f"Successfully generated: {sum(1 for r in results if r)}")
    print(f"Failed: {sum(1 for r in results if not r)}")
    print(f"Output directory: {Path(args.output).absolute()}")
    print("="*60)


if __name__ == '__main__':
    main()
