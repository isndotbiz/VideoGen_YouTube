#!/usr/bin/env python3
"""Real-time image generation progress monitor"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

start_time = time.time()

print("\n" + "="*70)
print("REAL-TIME IMAGE GENERATION MONITOR")
print("="*70)

while True:
    elapsed = time.time() - start_time
    images = list(Path("output/generated_images").glob("*.png"))
    count = len(images)

    if count > 0:
        rate = count / (elapsed / 60) if elapsed > 0 else 0
        remaining = (21 - count) / rate if rate > 0 else 0
    else:
        rate = 0
        remaining = 0

    percent = (count / 21) * 100

    # Progress bar
    filled = int(percent / 5)
    bar = "#" * filled + "-" * (20 - filled)

    print(f"\rProgress: [{bar}] {count}/21 ({percent:.0f}%) | "
          f"Rate: {rate:.1f} img/min | ETA: {remaining:.0f}m | "
          f"Elapsed: {elapsed/60:.1f}m", end="", flush=True)

    if count >= 21:
        print("\n" + "="*70)
        print("IMAGE GENERATION COMPLETE!")
        print("="*70)
        print(f"Total images: {count}/21")
        print(f"Total time: {elapsed/60:.1f} minutes")
        print(f"Average per image: {elapsed/count:.1f} seconds")
        print(f"Cost: ${count * 0.001:.3f}")
        print("="*70)
        break

    time.sleep(5)
