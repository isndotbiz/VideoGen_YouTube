#!/usr/bin/env python3
"""
Real-time pipeline execution monitor
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

def get_status():
    """Get current pipeline status"""
    status = {
        "timestamp": datetime.now().isoformat(),
        "phase_1_images": 0,
        "phase_2_audio": False,
        "phase_3_video": False,
        "phase_4_upload": False,
    }

    # Check images
    images = list(Path("output/generated_images").glob("*.png"))
    status["phase_1_images"] = len(images)

    # Check audio
    status["phase_2_audio"] = Path("output/narration.mp3").exists()

    # Check video
    status["phase_3_video"] = Path("output/video_final.mp4").exists()

    return status

def print_progress():
    """Print progress bar"""
    status = get_status()

    print("\n" + "="*70)
    print("VIDEO GENERATION PIPELINE - LIVE STATUS")
    print("="*70)
    print(f"Time: {status['timestamp']}")
    print()

    # Phase 1
    img_count = status['phase_1_images']
    progress = (img_count / 21) * 100
    bar = "#" * int(progress / 5) + "-" * (20 - int(progress / 5))
    print(f"[PHASE 1] Image Generation - FAL.ai")
    print(f"  Progress: [{bar}] {img_count}/21 ({progress:.0f}%)")
    print(f"  Cost: ${img_count * 0.001:.3f} / $0.02")
    print(f"  Time: ~{img_count} minutes elapsed")
    print()

    # Phase 2
    audio_status = "GENERATED" if status['phase_2_audio'] else "WAITING FOR PHASE 1"
    print(f"[PHASE 2] Narration - ElevenLabs")
    print(f"  Status: {audio_status}")
    print()

    # Phase 3
    video_status = "GENERATED" if status['phase_3_video'] else "WAITING FOR PHASES 1 & 2"
    print(f"[PHASE 3] Video Assembly - Shotstack")
    print(f"  Status: {video_status}")
    print()

    # Phase 4
    print(f"[PHASE 4] YouTube Upload")
    print(f"  Status: READY AFTER PHASE 3")
    print()

    print("="*70)
    print("Overall Progress:")
    total_complete = sum([
        1 if img_count == 21 else 0,
        1 if status['phase_2_audio'] else 0,
        1 if status['phase_3_video'] else 0,
    ])
    print(f"  Phases complete: {total_complete}/4")
    print(f"  Overall: {(total_complete/4)*100:.0f}%")
    print("="*70)

if __name__ == "__main__":
    print_progress()
