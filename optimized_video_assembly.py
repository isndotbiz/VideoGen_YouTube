#!/usr/bin/env python3
"""Optimized Shotstack video assembly"""

import os
import json
import logging
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def assemble_video():
    """Assemble video from images and narration using Shotstack"""
    api_key = os.getenv("SHOTSTACK_API_KEY")
    if not api_key:
        logger.error("SHOTSTACK_API_KEY not set")
        return False

    try:
        import requests

        images_dir = Path("output/generated_images")
        narration_file = Path("output/narration.mp3")

        if not images_dir.exists() or not narration_file.exists():
            logger.error(f"Missing inputs: images={images_dir.exists()}, audio={narration_file.exists()}")
            return False

        # Get all images sorted
        images = sorted(list(images_dir.glob("*.png")))
        logger.info(f"Found {len(images)} images and narration file")

        if not images:
            logger.error("No images found")
            return False

        # Build clips from images (5 seconds each)
        clips = []
        for img_path in images:
            clips.append({
                "asset": {
                    "type": "image",
                    "src": f"file://{img_path.absolute()}"
                },
                "start": 0,
                "length": 5
            })

        # Build edit JSON
        edit = {
            "timeline": {
                "tracks": [
                    {
                        "clips": clips
                    },
                    {
                        "clips": [
                            {
                                "asset": {
                                    "type": "audio",
                                    "src": f"file://{narration_file.absolute()}"
                                },
                                "start": 0,
                                "length": len(images) * 5
                            }
                        ]
                    }
                ]
            },
            "output": {
                "format": "mp4",
                "resolution": "1920x1080",
                "bitrate": "8000k",
                "frame_rate": 30
            }
        }

        logger.info("Submitting render to Shotstack...")
        logger.info(f"Duration: {len(images) * 5} seconds ({len(images) * 5 / 60:.1f} minutes)")
        logger.info(f"Cost: ${(len(images) * 5 / 60) * 0.20:.2f}")

        # Submit render
        headers = {"x-api-key": api_key}

        # Build complete render request
        render_request = {
            "timeline": edit["timeline"],
            "output": edit["output"],
            "callback": "https://example.com/callback"  # Optional callback URL
        }

        logger.info(f"Sending render request with {len(clips)} clips")

        response = requests.post(
            "https://api.shotstack.io/v1/render",
            json=render_request,
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            logger.error(f"Render submission failed: {response.text}")
            return False

        render_id = response.json().get("response", {}).get("id")
        logger.info(f"Render job submitted: {render_id}")
        logger.info(f"Estimated rendering time: {(len(images) * 5 / 60 * 1.5):.0f} minutes")

        return True

    except Exception as e:
        logger.error(f"Video assembly failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = assemble_video()
    exit(0 if success else 1)
