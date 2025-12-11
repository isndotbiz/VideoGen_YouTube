#!/usr/bin/env python3
"""Test script to verify video assembly configuration"""

import json
from pathlib import Path
from enhanced_video_assembly_longform import (
    calculate_total_duration,
    calculate_image_duration,
    SECTION_TIMINGS,
    SECTION_BOUNDARIES
)

def main():
    print("=" * 70)
    print("VIDEO ASSEMBLY CONFIGURATION TEST")
    print("=" * 70)
    print()

    # Check files exist
    print("1. FILE VERIFICATION")
    print("-" * 70)
    
    files_to_check = [
        ("Main Script", "enhanced_video_assembly_longform.py"),
        ("Quick Start", "QUICK_START_LONGFORM_VIDEO.md"),
        ("README", "README_LONGFORM_VIDEO.md"),
        ("Workflow", "LONGFORM_VIDEO_WORKFLOW.md"),
        ("Examples", "EXAMPLE_USAGE.md"),
        ("Index", "VIDEO_ASSEMBLY_INDEX.md"),
    ]
    
    for name, file_path in files_to_check:
        exists = Path(file_path).exists()
        size = Path(file_path).stat().st_size if exists else 0
        status = "✓" if exists else "✗"
        print(f"  {status} {name:20s} {file_path:40s} {size/1024:6.1f}KB")
    
    print()
    
    # Check images
    print("2. IMAGE ASSETS")
    print("-" * 70)
    images_dir = Path("output/generated_images")
    if images_dir.exists():
        images = sorted(list(images_dir.glob("*.png")))
        print(f"  Images found: {len(images)}")
        print(f"  First image: {images[0].name if images else 'None'}")
        print(f"  Last image:  {images[-1].name if images else 'None'}")
    else:
        print(f"  ✗ Directory not found: {images_dir}")
    
    print()
    
    # Check narration
    print("3. AUDIO ASSETS")
    print("-" * 70)
    narration_path = Path("output/narration.mp3")
    if narration_path.exists():
        size = narration_path.stat().st_size
        print(f"  ✓ Narration: {narration_path} ({size/1024/1024:.1f}MB)")
    else:
        print(f"  ✗ Narration not found: {narration_path}")
    
    print()
    
    # Show timing configuration
    print("4. TIMING CONFIGURATION")
    print("-" * 70)
    print("  Section Timings:")
    for key, value in SECTION_TIMINGS.items():
        print(f"    {key:20s}: {value:5.1f}s")
    
    print()
    
    # Calculate durations for different image counts
    print("5. DURATION CALCULATIONS")
    print("-" * 70)
    print(f"  {'Images':<10} {'Duration':<15} {'Minutes':<12} {'Cost'}")
    print(f"  {'-'*9} {'-'*14} {'-'*11} {'-'*8}")
    
    for count in [15, 21, 30, 35, 40, 50]:
        duration = calculate_total_duration(count)
        minutes = duration / 60
        cost = minutes * 0.20
        print(f"  {count:<10} {duration:>6.1f} seconds  {minutes:>5.2f} min    ${cost:>5.2f}")
    
    print()
    
    # Current setup analysis
    if images_dir.exists():
        print("6. CURRENT SETUP ANALYSIS")
        print("-" * 70)
        current_count = len(list(images_dir.glob("*.png")))
        current_duration = calculate_total_duration(current_count)
        current_minutes = current_duration / 60
        current_cost = current_minutes * 0.20
        
        print(f"  Current image count: {current_count}")
        print(f"  Video duration: {current_duration:.1f}s ({current_minutes:.2f} minutes)")
        print(f"  Estimated cost: ${current_cost:.2f}")
        print(f"  Estimated render time: {int(current_minutes * 1.5)} minutes")
        print()
        
        print("  Timing breakdown:")
        for i in range(min(current_count, 10)):
            dur = calculate_image_duration(i, current_count)
            section = ""
            if i == 0:
                section = "Title"
            elif 1 <= i <= 3:
                section = "Intro-Fast"
            elif 4 <= i <= 5:
                section = "Intro-Slow"
            elif i >= current_count - 5:
                section = "Conclusion"
            else:
                section = "Main"
            print(f"    Image {i:2d}: {dur:4.1f}s  ({section})")
        
        if current_count > 10:
            print(f"    ... ({current_count - 10} more images)")
    
    print()
    print("=" * 70)
    print("CONFIGURATION TEST COMPLETE")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Review QUICK_START_LONGFORM_VIDEO.md for setup")
    print("  2. Ensure .env file has AWS and Shotstack credentials")
    print("  3. Run: python enhanced_video_assembly_longform.py")

if __name__ == "__main__":
    main()
