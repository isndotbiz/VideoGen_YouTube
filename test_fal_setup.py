#!/usr/bin/env python3
"""
Test script to validate FAL.ai setup and generate a single test image
Run this before using the batch generator to ensure everything works
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}{text:^70}{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓{RESET} {text}")


def print_error(text):
    """Print error message"""
    print(f"{RED}✗{RESET} {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠{RESET} {text}")


def print_info(text):
    """Print info message"""
    print(f"  {text}")


def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str} (meets requirement ≥3.8)")
        return True
    else:
        print_error(f"Python {version_str} (requires ≥3.8)")
        return False


def check_dependencies():
    """Check required packages"""
    print_header("Checking Dependencies")

    packages = {
        'fal_client': 'fal-client',
        'dotenv': 'python-dotenv',
        'requests': 'requests',
        'tqdm': 'tqdm'
    }

    all_installed = True

    for module, package in packages.items():
        try:
            __import__(module if module != 'dotenv' else 'dotenv')
            print_success(f"{package} installed")
        except ImportError:
            print_error(f"{package} not installed")
            print_info(f"Install with: pip install {package}")
            all_installed = False

    return all_installed


def check_environment():
    """Check environment variables"""
    print_header("Checking Environment Variables")

    load_dotenv()

    api_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")

    if api_key:
        # Mask the key for security
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print_success(f"FAL_API_KEY found: {masked_key}")
        print_info(f"Key length: {len(api_key)} characters")
        return True
    else:
        print_error("FAL_API_KEY not found")
        print_info("Add to .env file: FAL_API_KEY=your_key_here")
        print_info("Get key from: https://fal.ai/dashboard/keys")
        return False


def check_output_directory():
    """Check output directory"""
    print_header("Checking Output Directory")

    output_dir = Path("./output/generated_images")

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        print_success(f"Output directory ready: {output_dir.absolute()}")

        # Check write permissions
        test_file = output_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        print_success("Directory is writable")

        return True
    except Exception as e:
        print_error(f"Cannot create/write to output directory: {e}")
        return False


def test_fal_client():
    """Test FAL client initialization"""
    print_header("Testing FAL Client")

    try:
        import fal_client

        api_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
        os.environ["FAL_KEY"] = api_key

        print_success("FAL client imported successfully")
        print_info("Client ready for API calls")
        return True

    except Exception as e:
        print_error(f"FAL client error: {e}")
        return False


def generate_test_image():
    """Generate a single test image"""
    print_header("Generating Test Image")

    try:
        import fal_client
        import requests
        from datetime import datetime

        api_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
        os.environ["FAL_KEY"] = api_key

        test_prompt = "A beautiful serene landscape with mountains and a lake at sunset, photorealistic, 8k resolution"

        print_info(f"Prompt: {test_prompt[:60]}...")
        print_info("Generating image (this may take 10-15 seconds)...")

        # Generate image
        result = fal_client.run(
            "fal-ai/flux/dev",
            arguments={
                "prompt": test_prompt,
                "image_size": {
                    "width": 1920,
                    "height": 1080
                },
                "num_inference_steps": 28,  # Faster for testing
                "guidance_scale": 7.5,
                "num_images": 1,
                "enable_safety_checker": False,
                "output_format": "png"
            }
        )

        # Download image
        if "images" in result and result["images"]:
            img_url = result["images"][0]["url"]

            response = requests.get(img_url, timeout=60)
            response.raise_for_status()

            # Save test image
            output_dir = Path("./output/generated_images")
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"test_image_{timestamp}.png"

            output_file.write_bytes(response.content)

            file_size = len(response.content) / 1024  # KB

            print_success(f"Test image generated successfully!")
            print_info(f"Location: {output_file}")
            print_info(f"Size: {file_size:.1f} KB")
            print_info(f"Resolution: 1920x1080")

            return True
        else:
            print_error("No images in API response")
            return False

    except Exception as e:
        print_error(f"Failed to generate test image: {e}")
        import traceback
        print_info("Full error:")
        print(traceback.format_exc())
        return False


def print_summary(results):
    """Print summary of all checks"""
    print_header("Setup Validation Summary")

    all_passed = all(results.values())

    for check, passed in results.items():
        if passed:
            print_success(check)
        else:
            print_error(check)

    print()

    if all_passed:
        print(f"{GREEN}{'='*70}{RESET}")
        print(f"{GREEN}{'ALL CHECKS PASSED!':^70}{RESET}")
        print(f"{GREEN}{'='*70}{RESET}\n")
        print_info("You're ready to use the Enhanced FAL Batch Generator!")
        print_info("Run: python enhanced_fal_batch_generator.py --prompts sample_image_prompts.json --dry-run")
    else:
        print(f"{RED}{'='*70}{RESET}")
        print(f"{RED}{'SOME CHECKS FAILED':^70}{RESET}")
        print(f"{RED}{'='*70}{RESET}\n")
        print_info("Please fix the issues above before running the batch generator")

    return all_passed


def main():
    """Run all validation checks"""
    print_header("FAL.ai Batch Generator Setup Validation")
    print_info("This script will validate your setup and generate a test image\n")

    results = {}

    # Run checks
    results["Python Version ≥3.8"] = check_python_version()
    results["Required Packages"] = check_dependencies()
    results["FAL_API_KEY"] = check_environment()
    results["Output Directory"] = check_output_directory()
    results["FAL Client"] = test_fal_client()

    # Only try to generate test image if all prerequisites pass
    if all(results.values()):
        print()
        user_input = input(f"{YELLOW}Generate a test image? This will cost ~$0.03 (y/n): {RESET}").lower()

        if user_input == 'y':
            results["Test Image Generation"] = generate_test_image()
        else:
            print_warning("Skipping test image generation")
            results["Test Image Generation"] = None
    else:
        print_warning("Skipping test image generation due to failed prerequisites")
        results["Test Image Generation"] = None

    # Print summary
    # Filter out None results
    summary_results = {k: v for k, v in results.items() if v is not None}
    success = print_summary(summary_results)

    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
