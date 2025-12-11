#!/usr/bin/env python3
"""Generate animated video loops using Runway ML with budget tracking"""

import os
import json
import logging
import requests
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

RUNWAY_API_KEY = "key_583c257d0f479da77756e05bb1a9585ef2b4a17a69cc3d7a5ba1302897ecd362e6660a4f720defc16cb0cfd09eb087d9141e705e8d330d49162b246dc723055f"
RUNWAY_BASE_URL = "https://api.dev.runwayml.com/v1"

# Budget tracking
BUDGET = 5.00  # $5.00
COST_PER_VIDEO = 0.80  # Estimated cost per ~5 second video generation
MAX_VIDEOS = int(BUDGET / COST_PER_VIDEO)  # Should get ~6 videos

# Select best images for animation (high visual impact)
TARGET_ANIMATIONS = [
    {
        'image_name': 'Introduction_Title_Claude_Code_Showcase_001_image.png',
        'image_number': 1,
        'section': 'Introduction/Title',
        'prompt': 'Camera slowly dollies forward through the center of the split screen while both neural networks pulse with energy, particles flowing between them, subtle rotation of the network structures, seamless loop returning to starting position'
    },
    {
        'image_name': 'Claude_Code_Showcase_007_image.png',
        'image_number': 7,
        'section': 'Claude Code Showcase',
        'prompt': 'Golden thread continuously weaves through the code structure, starting from bottom left and traveling to top right, code blocks light up in sequence as thread passes through them, gentle rotation of entire structure, thread leaves brief light trail that fades'
    },
    {
        'image_name': 'Codex_Showcase_012_image.png',
        'image_number': 12,
        'section': 'Codex Showcase',
        'prompt': 'Six threads flow continuously from left to right at different speeds, files move along conveyor-like paths, completion checkmarks appear on finished files, new files queue up on the left, threads occasionally split and merge, industrial mechanical rhythm'
    },
    {
        'image_name': 'Comparison_Visuals_018_image.png',
        'image_number': 18,
        'section': 'Comparison Visuals',
        'prompt': 'Features illuminate one by one from top to bottom, icons animate to demonstrate their function, highlighting sweeps down each column, checkmarks appear next to applicable use cases, subtle gradient background shifts between amber and blue zones'
    },
    {
        'image_name': 'Use_Cases_024_image.png',
        'image_number': 24,
        'section': 'Use Cases',
        'prompt': 'Developer types questions, Claude appears on screen with explanations, cursor highlights relevant code sections, developer nods and makes notes, rubber duck appears to listen, screen content updates showing progress'
    },
    {
        'image_name': 'Use_Cases_025_image.png',
        'image_number': 25,
        'section': 'Use Cases',
        'prompt': 'Files change from gray (pending) to blue (processing) to green (complete) in waves, multiple worker bots move between files, progress counter rapidly increments, dashboard charts update showing completion percentage'
    }
]

def get_image_path(image_name: str) -> Path:
    """Get full path to image"""
    # Try different naming patterns
    images_dir = Path("output/generated_images")

    # Direct match
    direct = images_dir / image_name
    if direct.exists():
        return direct

    # Fuzzy match - try to find close match
    for img in images_dir.glob("*.png"):
        if image_name.lower() in img.name.lower() or img.name.lower() in image_name.lower():
            return img

    return None

def upload_image_to_runway(image_path: Path) -> Optional[str]:
    """Upload image to Runway and get asset ID - two-step process"""
    logger.info(f"Uploading image to Runway: {image_path.name}")

    try:
        headers = {
            "Authorization": f"Bearer {RUNWAY_API_KEY}",
            "Content-Type": "application/json",
            "X-Runway-Version": "2024-11-15"
        }

        # Step 1: Create upload metadata
        payload = {
            "title": image_path.name,
            "type": "image"
        }

        response = requests.post(
            f"{RUNWAY_BASE_URL}/uploads",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code not in [200, 201]:
            logger.error(f"Upload metadata failed: {response.status_code} - {response.text}")
            return None

        data = response.json()
        asset_id = data.get('id')
        upload_url = data.get('upload_url')

        if not upload_url:
            logger.error(f"No upload URL received: {data}")
            return None

        logger.info(f"Got upload URL, uploading file...")

        # Step 2: Upload file to signed URL
        with open(image_path, 'rb') as f:
            file_data = f.read()

        response = requests.put(
            upload_url,
            data=file_data,
            headers={'Content-Type': 'image/png'},
            timeout=60
        )

        if response.status_code not in [200, 201, 204]:
            logger.error(f"File upload failed: {response.status_code} - {response.text}")
            return None

        logger.info(f"Upload successful. Asset ID: {asset_id}")
        return asset_id

    except Exception as e:
        logger.error(f"Upload error: {e}")
        return None

def generate_runway_video(image_path: Path, motion_prompt: str, title: str) -> Optional[str]:
    """Generate video using Runway Gen-3 Motion"""
    logger.info(f"\nGenerating animation for: {title}")
    logger.info(f"Prompt: {motion_prompt[:100]}...")

    try:
        # Upload image first
        asset_id = upload_image_to_runway(image_path)
        if not asset_id:
            logger.error("Failed to upload image")
            return None

        # Create generation task
        headers = {
            "Authorization": f"Bearer {RUNWAY_API_KEY}",
            "Content-Type": "application/json",
            "X-Runway-Version": "2024-11-15"
        }

        payload = {
            "promptImage": asset_id,
            "motionPrompt": motion_prompt,
            "duration": 5,  # 5 seconds
            "model": "gen3",
            "quality": "high"
        }

        logger.info("Submitting generation request to Runway...")
        response = requests.post(
            f"{RUNWAY_BASE_URL}/image_to_video",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code in [200, 201]:
            data = response.json()
            task_id = data.get('id')
            logger.info(f"Generation task created. ID: {task_id}")
            return task_id
        else:
            logger.error(f"Generation failed: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        logger.error(f"Generation error: {e}")
        return None

def check_generation_status(task_id: str) -> Tuple[str, Optional[str]]:
    """Check status of generation task and get video URL if complete"""
    try:
        headers = {
            "Authorization": f"Bearer {RUNWAY_API_KEY}",
            "X-Runway-Version": "2024-11-15"
        }

        response = requests.get(
            f"{RUNWAY_BASE_URL}/tasks/{task_id}",
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            status = data.get('status')

            if status == 'SUCCEEDED':
                video_url = data.get('output', [{}])[0].get('url')
                return status, video_url
            elif status in ['QUEUED', 'IN_PROGRESS']:
                progress = data.get('progress', 0)
                return status, f"{progress}% complete"
            elif status == 'FAILED':
                error = data.get('error', 'Unknown error')
                return status, error
            else:
                return status, None
        else:
            return 'ERROR', f"HTTP {response.status_code}"

    except Exception as e:
        return 'ERROR', str(e)

def download_video(url: str, output_path: Path) -> bool:
    """Download generated video"""
    try:
        logger.info(f"Downloading video to: {output_path}")
        response = requests.get(url, timeout=120)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)

            size_mb = output_path.stat().st_size / (1024*1024)
            logger.info(f"Downloaded successfully: {size_mb:.1f}MB")
            return True
        else:
            logger.error(f"Download failed: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"Download error: {e}")
        return False

def main():
    logger.info("=" * 70)
    logger.info("RUNWAY ML ANIMATION GENERATOR - $5 BUDGET")
    logger.info("=" * 70)
    logger.info(f"Budget: ${BUDGET:.2f}")
    logger.info(f"Estimated cost per video: ${COST_PER_VIDEO:.2f}")
    logger.info(f"Target animations: {MAX_VIDEOS}")
    logger.info("=" * 70 + "\n")

    output_dir = Path("output/animated_loops")
    output_dir.mkdir(exist_ok=True)

    results = []
    task_ids = {}

    # Submit generation tasks
    logger.info("PHASE 1: Submitting animation tasks to Runway...\n")

    for i, target in enumerate(TARGET_ANIMATIONS[:MAX_VIDEOS], 1):
        image_path = get_image_path(target['image_name'])

        if not image_path or not image_path.exists():
            logger.warning(f"[{i}] Image not found: {target['image_name']}")
            continue

        task_id = generate_runway_video(
            image_path,
            target['prompt'],
            f"{target['section']} - Image {target['image_number']}"
        )

        if task_id:
            task_ids[task_id] = {
                'title': target['section'],
                'image_number': target['image_number'],
                'output_file': output_dir / f"animation_{i:02d}_{target['image_number']:02d}.mp4"
            }
            logger.info(f"[{i}] Task submitted successfully\n")
        else:
            logger.error(f"[{i}] Task submission failed\n")

        time.sleep(2)  # Rate limiting

    if not task_ids:
        logger.error("No tasks were submitted successfully")
        return False

    logger.info(f"\n{'='*70}")
    logger.info(f"Submitted {len(task_ids)} animation tasks")
    logger.info(f"Waiting for completions (this may take 2-5 minutes)...")
    logger.info(f"{'='*70}\n")

    # Poll for completions
    logger.info("PHASE 2: Monitoring task progress...\n")

    completed = {}
    check_count = 0
    max_checks = 60  # 10 minutes max

    while len(completed) < len(task_ids) and check_count < max_checks:
        check_count += 1

        for task_id in task_ids:
            if task_id in completed:
                continue

            status, result = check_generation_status(task_id)

            if status == 'SUCCEEDED':
                logger.info(f"[COMPLETE] {task_ids[task_id]['title']} - Image {task_ids[task_id]['image_number']}")
                completed[task_id] = result

                # Download video
                if result and result.startswith('http'):
                    if download_video(result, task_ids[task_id]['output_file']):
                        results.append({
                            'status': 'success',
                            'file': str(task_ids[task_id]['output_file']),
                            'title': task_ids[task_id]['title']
                        })

            elif status == 'IN_PROGRESS':
                logger.info(f"[PROGRESS] {task_ids[task_id]['title']}: {result}")
            elif status == 'FAILED':
                logger.error(f"[FAILED] {task_ids[task_id]['title']}: {result}")
                completed[task_id] = None

        if len(completed) < len(task_ids):
            time.sleep(5)  # Check every 5 seconds

    # Summary
    logger.info(f"\n{'='*70}")
    logger.info("ANIMATION GENERATION COMPLETE")
    logger.info(f"{'='*70}")
    logger.info(f"Generated: {len([r for r in results if r['status'] == 'success'])} animations")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"\nGenerated files:")

    for result in results:
        if result['status'] == 'success':
            file_size = Path(result['file']).stat().st_size / (1024*1024)
            logger.info(f"  - {Path(result['file']).name} ({file_size:.1f}MB)")
            logger.info(f"    Section: {result['title']}")

    logger.info(f"\n{len(results)} videos ready for integration into main video!")

    return len(results) > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
