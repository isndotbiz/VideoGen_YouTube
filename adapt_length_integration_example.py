#!/usr/bin/env python3
"""
Integration Example: adapt_length_automation with existing workflows

Demonstrates how to use the adapt_length_automation module with:
1. epidemic_browser_adapt.py
2. epidemic_ai_search_adapt.py
3. Custom workflows

Author: VideoGen YouTube Project
Date: December 2025
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from adapt_length_automation import (
    adapt_length_automation,
    adapt_length_simple,
    adapt_length_with_duration_string
)


# ============================================================================
# EXAMPLE 1: Basic Usage (Standalone)
# ============================================================================

async def example_1_basic_usage():
    """
    Basic usage: Open browser, navigate to Adapt, run automation.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to Adapt (must be logged in)
        await page.goto("https://www.epidemicsound.com/labs/adapt/")
        await asyncio.sleep(5)

        print("Please select a track and press Enter...")
        input()

        # Run automation
        success, error = await adapt_length_automation(
            page=page,
            duration_seconds=180,      # 3 minutes
            enable_ducking=True,
            screenshot_on_error=True
        )

        if success:
            print("\n✓ Automation successful!")
        else:
            print(f"\n✗ Automation failed: {error}")

        await browser.close()


# ============================================================================
# EXAMPLE 2: Simple Wrapper
# ============================================================================

async def example_2_simple_wrapper():
    """
    Using the simple wrapper function.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Simple Wrapper")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.epidemicsound.com/labs/adapt/")
        await asyncio.sleep(5)

        print("Select track and press Enter...")
        input()

        # Simple usage - just specify minutes
        success = await adapt_length_simple(page, minutes=3)

        print(f"\nResult: {'Success' if success else 'Failed'}")

        await browser.close()


# ============================================================================
# EXAMPLE 3: Duration String Formats
# ============================================================================

async def example_3_duration_formats():
    """
    Testing different duration format strings.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Duration Format Strings")
    print("=" * 70 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.epidemicsound.com/labs/adapt/")
        await asyncio.sleep(5)

        print("Select track and press Enter...")
        input()

        # Test different formats
        formats = ["3:00", "180", "3 min"]

        for fmt in formats:
            print(f"\nTrying format: {fmt}")
            success = await adapt_length_with_duration_string(page, fmt)
            print(f"Result: {'Success' if success else 'Failed'}")

            if success:
                break  # Stop after first success

        await browser.close()


# ============================================================================
# EXAMPLE 4: Integration with Existing Session
# ============================================================================

async def example_4_with_session():
    """
    Load existing Epidemic session and use adapt automation.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: With Existing Session")
    print("=" * 70 + "\n")

    session_file = Path("epidemic_session.json")

    if not session_file.exists():
        print("✗ No session file found. Login first using epidemic_browser_adapt.py")
        return

    # Load session
    with open(session_file, 'r') as f:
        session_data = json.load(f)

    print(f"✓ Session loaded: {session_file}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Create context with saved session
        context = await browser.new_context(
            storage_state=session_data['storage_state']
        )

        page = await context.new_page()

        # Navigate to Adapt (should be logged in)
        await page.goto("https://www.epidemicsound.com/labs/adapt/")
        await asyncio.sleep(5)

        print("Select track and press Enter...")
        input()

        # Run automation
        success, error = await adapt_length_automation(
            page=page,
            duration_seconds=180,
            enable_ducking=True,
            screenshot_on_error=True
        )

        print(f"\nResult: {'Success' if success else f'Failed: {error}'}")

        await browser.close()


# ============================================================================
# EXAMPLE 5: Batch Processing Multiple Tracks
# ============================================================================

async def example_5_batch_processing():
    """
    Process multiple tracks in sequence.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Batch Processing Multiple Tracks")
    print("=" * 70 + "\n")

    track_urls = [
        "https://www.epidemicsound.com/track/example1/",
        "https://www.epidemicsound.com/track/example2/",
        "https://www.epidemicsound.com/track/example3/"
    ]

    durations = [180, 180, 180]  # 3 minutes each

    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        for idx, (track_url, duration) in enumerate(zip(track_urls, durations), 1):
            print(f"\n--- Processing Track {idx}/{len(track_urls)} ---")
            print(f"URL: {track_url}")
            print(f"Duration: {duration}s")

            try:
                # Navigate to track
                await page.goto(track_url)
                await asyncio.sleep(3)

                # Click "Adapt" button on track page
                adapt_btn = page.locator('button:has-text("Adapt")').first
                if await adapt_btn.count() > 0:
                    await adapt_btn.click()
                    await asyncio.sleep(3)

                # Run adaptation
                success, error = await adapt_length_automation(
                    page=page,
                    duration_seconds=duration,
                    enable_ducking=True,
                    screenshot_on_error=True
                )

                results.append({
                    'track_url': track_url,
                    'duration': duration,
                    'success': success,
                    'error': error
                })

                if success:
                    print(f"✓ Track {idx} adapted successfully")

                    # Download (optional)
                    download_btn = page.locator('button:has-text("Download")').first
                    if await download_btn.count() > 0:
                        print(f"  Download button available")
                else:
                    print(f"✗ Track {idx} failed: {error}")

            except Exception as e:
                print(f"✗ Track {idx} error: {e}")
                results.append({
                    'track_url': track_url,
                    'duration': duration,
                    'success': False,
                    'error': str(e)
                })

            # Delay between tracks
            await asyncio.sleep(2)

        await browser.close()

    # Summary
    print("\n" + "=" * 70)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 70)
    successful = sum(1 for r in results if r['success'])
    print(f"\nTotal tracks: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")

    if results:
        print("\nDetails:")
        for idx, result in enumerate(results, 1):
            status = "✓" if result['success'] else "✗"
            print(f"  {status} Track {idx}: {result['duration']}s - {'Success' if result['success'] else result['error']}")


# ============================================================================
# EXAMPLE 6: With Custom Retry Logic
# ============================================================================

async def example_6_with_retry():
    """
    Retry adaptation with different durations if first attempt fails.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Retry with Different Durations")
    print("=" * 70 + "\n")

    durations_to_try = [180, 240, 300]  # 3, 4, 5 minutes

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.epidemicsound.com/labs/adapt/")
        await asyncio.sleep(5)

        print("Select track and press Enter...")
        input()

        for attempt, duration in enumerate(durations_to_try, 1):
            print(f"\n--- Attempt {attempt}/{len(durations_to_try)}: {duration}s ({duration // 60} min) ---")

            success, error = await adapt_length_automation(
                page=page,
                duration_seconds=duration,
                enable_ducking=True,
                screenshot_on_error=(attempt == len(durations_to_try))  # Screenshot only on last attempt
            )

            if success:
                print(f"\n✓ Success with {duration}s!")
                break
            else:
                print(f"\n✗ Failed with {duration}s: {error}")

                if attempt < len(durations_to_try):
                    print("Retrying with different duration...")
                    await asyncio.sleep(2)
                else:
                    print("All attempts failed")

        await browser.close()


# ============================================================================
# EXAMPLE 7: Integration with epidemic_browser_adapt.py Pattern
# ============================================================================

async def example_7_browser_adapt_pattern():
    """
    Using the pattern from epidemic_browser_adapt.py but with custom length automation.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Browser Adapt Pattern")
    print("=" * 70 + "\n")

    # This example shows how to integrate with the existing
    # epidemic_browser_adapt.py structure

    class AdaptWorkflow:
        def __init__(self, page):
            self.page = page

        async def navigate_to_adapt(self):
            """Navigate to Adapt page."""
            await self.page.goto("https://www.epidemicsound.com/labs/adapt/")
            await asyncio.sleep(3)

        async def select_track(self, track_url: str):
            """Select track by URL."""
            await self.page.goto(track_url)
            await asyncio.sleep(3)

            # Click Adapt button on track page
            adapt_btn = self.page.locator('button:has-text("Adapt")').first
            if await adapt_btn.count() > 0:
                await adapt_btn.click()
                await asyncio.sleep(3)
                return True
            return False

        async def adapt_length_custom(self, duration_seconds: int):
            """Use custom length automation."""
            success, error = await adapt_length_automation(
                page=self.page,
                duration_seconds=duration_seconds,
                enable_ducking=True,
                screenshot_on_error=True
            )
            return success, error

        async def adapt_music(self, description: str):
            """Adapt music (placeholder - would use similar pattern)."""
            print(f"Would adapt music with: {description}")
            # Could create adapt_music_automation.py following same pattern
            return True, None

        async def download(self, output_dir: Path):
            """Download adapted track."""
            download_btn = self.page.locator('button:has-text("Download")').first

            if await download_btn.count() == 0:
                return None, "Download button not found"

            # Click download and wait
            await download_btn.click()
            await asyncio.sleep(2)

            print(f"Download initiated to {output_dir}")
            return True, None

    # Use the workflow
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        workflow = AdaptWorkflow(page)

        # Complete workflow
        await workflow.navigate_to_adapt()

        track_url = "https://www.epidemicsound.com/track/example/"
        print(f"Selecting track: {track_url}")

        if await workflow.select_track(track_url):
            print("✓ Track selected")

            # Adapt length
            success, error = await workflow.adapt_length_custom(duration_seconds=180)
            if success:
                print("✓ Length adapted")

                # Adapt music (optional)
                # success, error = await workflow.adapt_music("Minimal background")

                # Download
                output_dir = Path("background_music_epidemic")
                success, error = await workflow.download(output_dir)
                if success:
                    print("✓ Download complete")
            else:
                print(f"✗ Length adaptation failed: {error}")
        else:
            print("✗ Track selection failed")

        await browser.close()


# ============================================================================
# MAIN MENU
# ============================================================================

async def main():
    """Main menu for examples."""
    examples = {
        "1": ("Basic Usage", example_1_basic_usage),
        "2": ("Simple Wrapper", example_2_simple_wrapper),
        "3": ("Duration Formats", example_3_duration_formats),
        "4": ("With Existing Session", example_4_with_session),
        "5": ("Batch Processing", example_5_batch_processing),
        "6": ("Retry Logic", example_6_with_retry),
        "7": ("Browser Adapt Pattern", example_7_browser_adapt_pattern)
    }

    print("\n" + "=" * 70)
    print("ADAPT LENGTH AUTOMATION - INTEGRATION EXAMPLES")
    print("=" * 70)
    print("\nAvailable examples:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    print("  q. Quit")
    print()

    choice = input("Select example (1-7, q): ").strip().lower()

    if choice == 'q':
        print("Exiting...")
        return

    if choice in examples:
        _, example_func = examples[choice]
        await example_func()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())
