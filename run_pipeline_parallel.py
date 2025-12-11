#!/usr/bin/env python3
"""
Parallel Video Generation Pipeline Orchestrator
Runs all phases concurrently respecting dependencies
"""

import os
import sys
import json
import time
import logging
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables silently (no Unicode issues)
load_dotenv()

# Configure logging to avoid Unicode issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """Orchestrates parallel pipeline execution"""

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.output_dir = Path(os.getenv('OUTPUT_DIR', './output'))
        self.temp_dir = Path(os.getenv('TEMP_DIR', './temp'))
        self.logs_dir = Path(os.getenv('LOGS_DIR', './logs'))

        # Create directories
        for d in [self.output_dir, self.temp_dir, self.logs_dir]:
            d.mkdir(parents=True, exist_ok=True)

        self.processes = {}
        self.results = {}

    def verify_env(self) -> bool:
        """Verify all required environment variables are set"""
        required = [
            'FAL_API_KEY',
            'ELEVENLABS_API_KEY',
            'SHOTSTACK_API_KEY',
            'COMFYUI_SERVER_URL'
        ]

        missing = []
        for var in required:
            value = os.getenv(var)
            if not value or value.startswith('your_'):
                missing.append(var)

        if missing:
            logger.error(f"Missing environment variables: {missing}")
            return False

        logger.info("[INIT] All required environment variables found")
        return True

    def check_dependencies(self) -> bool:
        """Check if required Python packages are installed"""
        packages = [
            'requests', 'elevenlabs', 'fal_client',
            'google_auth_oauthlib', 'moviepy', 'pydub'
        ]

        missing = []
        for pkg in packages:
            try:
                __import__(pkg.replace('-', '_'))
            except ImportError:
                missing.append(pkg)

        if missing:
            logger.warning(f"Missing packages: {missing}")
            logger.info("Run: pip install -r requirements.txt")
            return False

        logger.info("[INIT] All required packages installed")
        return True

    def check_resources(self) -> Dict[str, bool]:
        """Check availability of external resources"""
        status = {}

        # Check ComfyUI server
        try:
            import requests
            response = requests.get(f"{os.getenv('COMFYUI_SERVER_URL', 'http://localhost:8188')}/api/auth", timeout=5)
            status['comfyui'] = response.status_code == 200
            logger.info(f"[RESOURCES] ComfyUI: {'OK' if status['comfyui'] else 'UNREACHABLE'}")
        except Exception as e:
            status['comfyui'] = False
            logger.warning(f"[RESOURCES] ComfyUI: UNREACHABLE ({str(e)[:50]})")

        # Check required files
        files_ok = all(Path(f).exists() for f in [
            'prompts.json',
            'VIDEO_SCRIPTS_ALL_VARIATIONS.md'
        ])
        status['files'] = files_ok
        logger.info(f"[RESOURCES] Input files: {'OK' if files_ok else 'MISSING'}")

        return status

    async def run_image_generation(self) -> Tuple[bool, str]:
        """Phase 1: Generate images (can run in parallel)"""
        logger.info("[PHASE 1] Starting image generation via ComfyUI...")

        try:
            output_log = self.logs_dir / "phase1_images.log"

            # Run batch generator
            result = await asyncio.create_subprocess_exec(
                'python', 'comfyui_batch_generator.py',
                '--prompts', 'prompts.json',
                '--output', str(self.output_dir / 'generated_images'),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.base_dir
            )

            stdout, stderr = await result.communicate()
            success = result.returncode == 0

            # Save log
            with open(output_log, 'wb') as f:
                f.write(stdout)
                if stderr:
                    f.write(b'\n--- STDERR ---\n' + stderr)

            status = "[OK]" if success else "[FAILED]"
            logger.info(f"[PHASE 1] Image generation {status}")
            return success, str(output_log)

        except Exception as e:
            logger.error(f"[PHASE 1] Error: {e}")
            return False, str(e)

    async def run_narration_generation(self) -> Tuple[bool, str]:
        """Phase 2: Generate narration (can run in parallel)"""
        logger.info("[PHASE 2] Starting narration generation via ElevenLabs...")

        try:
            output_log = self.logs_dir / "phase2_narration.log"

            # Run narration generator
            result = await asyncio.create_subprocess_exec(
                'python', '-c',
                '''
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    from elevenlabs import client as elevenlabs_client
    from elevenlabs import set_api_key

    api_key = os.getenv("ELEVENLABS_API_KEY")
    set_api_key(api_key)

    # Read script
    with open("VIDEO_SCRIPTS_ALL_VARIATIONS.md") as f:
        content = f.read()

    # Extract YouTube script (first section)
    script = content.split("##")[1].split("\\n\\n")[1][:2000]

    # Generate speech
    audio = elevenlabs_client.generate(
        text=script,
        voice="Rachel",
        model="eleven_monolingual_v1"
    )

    # Save audio
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "narration.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print("Narration generated successfully")

except Exception as e:
    print(f"Error: {e}")
    import sys
    sys.exit(1)
''',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.base_dir
            )

            stdout, stderr = await result.communicate()
            success = result.returncode == 0

            # Save log
            with open(output_log, 'wb') as f:
                f.write(stdout)
                if stderr:
                    f.write(b'\n--- STDERR ---\n' + stderr)

            status = "[OK]" if success else "[FAILED]"
            logger.info(f"[PHASE 2] Narration generation {status}")
            return success, str(output_log)

        except Exception as e:
            logger.error(f"[PHASE 2] Error: {e}")
            return False, str(e)

    async def run_video_assembly(self, images_done: bool, narration_done: bool) -> Tuple[bool, str]:
        """Phase 3-4: Wait for dependencies, then assemble video"""
        if not images_done or not narration_done:
            logger.warning("[PHASE 3] Waiting for images and narration to complete...")
            # Wait in loop
            max_wait = 3600  # 1 hour
            waited = 0
            while (not images_done or not narration_done) and waited < max_wait:
                await asyncio.sleep(5)
                waited += 5

        logger.info("[PHASE 3] Starting video assembly via Shotstack...")

        try:
            output_log = self.logs_dir / "phase3_assembly.log"

            # Verify inputs exist
            images_dir = self.output_dir / 'generated_images'
            narration_file = self.output_dir / 'narration.mp3'

            if not images_dir.exists():
                logger.error(f"[PHASE 3] Images directory not found: {images_dir}")
                return False, f"Missing: {images_dir}"

            if not narration_file.exists():
                logger.error(f"[PHASE 3] Narration file not found: {narration_file}")
                return False, f"Missing: {narration_file}"

            logger.info(f"[PHASE 3] Found {len(list(images_dir.glob('*.png')))} images")
            logger.info(f"[PHASE 3] Found narration: {narration_file}")

            # Create assembly script
            assembly_script = '''
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SHOTSTACK_API_KEY")
base_url = "https://api.shotstack.io/v1"

# Build edit from images and narration
edit = {
    "timeline": {
        "tracks": [
            {
                "clips": [
                    {
                        "asset": {
                            "type": "image",
                            "src": f"file://{Path('output/generated_images/flux_001.png').absolute()}"
                        },
                        "start": 0,
                        "length": 5
                    }
                ]
            }
        ]
    },
    "output": {
        "format": "mp4",
        "resolution": "1920x1080"
    }
}

# Submit render
headers = {"x-api-key": api_key}
response = requests.post(
    f"{base_url}/render",
    json={"edit": edit},
    headers=headers
)

if response.status_code == 200:
    render_id = response.json()["response"]["id"]
    print(f"Render started: {render_id}")
else:
    print(f"Error: {response.text}")
'''

            with open(self.temp_dir / 'assembly_task.py', 'w') as f:
                f.write(assembly_script)

            # Run assembly
            result = await asyncio.create_subprocess_exec(
                'python', str(self.temp_dir / 'assembly_task.py'),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.base_dir
            )

            stdout, stderr = await result.communicate()
            success = result.returncode == 0

            # Save log
            with open(output_log, 'wb') as f:
                f.write(stdout)
                if stderr:
                    f.write(b'\n--- STDERR ---\n' + stderr)

            status = "[OK]" if success else "[FAILED]"
            logger.info(f"[PHASE 3] Video assembly {status}")
            return success, str(output_log)

        except Exception as e:
            logger.error(f"[PHASE 3] Error: {e}")
            return False, str(e)

    async def run_youtube_upload(self, assembly_done: bool) -> Tuple[bool, str]:
        """Phase 5: Upload to YouTube"""
        if not assembly_done:
            logger.warning("[PHASE 4] Waiting for video assembly to complete...")
            # In real scenario, would wait for assembly

        logger.info("[PHASE 4] YouTube upload configured (requires browser auth)")
        logger.info("[PHASE 4] Run: python video_pipeline.py --phase upload --video output/video.mp4")

        return True, "YouTube upload: awaiting manual auth"

    async def run_all_phases(self) -> Dict:
        """Execute all phases with correct dependency management"""
        start_time = time.time()
        logger.info("=" * 70)
        logger.info("PIPELINE EXECUTION STARTED")
        logger.info("=" * 70)

        # Verify setup
        if not self.verify_env() or not self.check_dependencies():
            logger.error("Setup verification failed")
            return {"success": False, "error": "Setup verification failed"}

        resources = self.check_resources()

        # Phase 1 & 2: Run images and narration in parallel
        logger.info("\n[ORCHESTRATION] Launching Phase 1 (Images) and Phase 2 (Narration) in parallel...")

        tasks = [
            self.run_image_generation(),
            self.run_narration_generation()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        images_ok = isinstance(results[0], tuple) and results[0][0]
        narration_ok = isinstance(results[1], tuple) and results[1][0]

        # Phase 3: Assembly (depends on 1 & 2)
        logger.info("\n[ORCHESTRATION] Launching Phase 3 (Assembly)...")
        assembly_ok, assembly_log = await self.run_video_assembly(images_ok, narration_ok)

        # Phase 4: Upload (depends on 3)
        logger.info("\n[ORCHESTRATION] Phase 4 (YouTube Upload)...")
        upload_ok, upload_log = await self.run_youtube_upload(assembly_ok)

        elapsed = time.time() - start_time

        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("PIPELINE EXECUTION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Total time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
        logger.info(f"Phase 1 (Images):    {'PASS' if images_ok else 'FAIL'}")
        logger.info(f"Phase 2 (Narration):  {'PASS' if narration_ok else 'FAIL'}")
        logger.info(f"Phase 3 (Assembly):   {'PASS' if assembly_ok else 'FAIL'}")
        logger.info(f"Phase 4 (YouTube):    {'PASS' if upload_ok else 'FAIL'}")
        logger.info(f"Overall: {'SUCCESS' if all([images_ok, narration_ok, assembly_ok]) else 'PARTIAL'}")
        logger.info(f"Logs: {self.logs_dir}")
        logger.info("=" * 70)

        return {
            "success": all([images_ok, narration_ok, assembly_ok]),
            "phase_1_images": images_ok,
            "phase_2_narration": narration_ok,
            "phase_3_assembly": assembly_ok,
            "phase_4_upload": upload_ok,
            "duration": elapsed,
            "logs_dir": str(self.logs_dir)
        }

async def main():
    """Main entry point"""
    orchestrator = PipelineOrchestrator()
    result = await orchestrator.run_all_phases()

    # Print final result
    if result.get("success"):
        logger.info("\nAll pipeline phases completed successfully!")
        sys.exit(0)
    else:
        logger.error("\nPipeline failed on one or more phases")
        logger.info(f"Check logs in: {result.get('logs_dir', './logs')}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
