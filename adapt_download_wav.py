"""
Playwright automation for downloading adapted music tracks as WAV files.

This script handles the complete download workflow after music adaptation:
1. Find the download button in History panel or top-right area
2. Select WAV format from the format selection modal
3. Download the file with proper naming and verification
4. Return file path and metadata

Usage:
    python adapt_download_wav.py --prompt-set "energy_consistency" --track-num 1 --duration 3

Author: Claude Code
Date: 2025-12-23
"""

import asyncio
import os
import time
from pathlib import Path
from playwright.async_api import async_playwright, Page, Download, TimeoutError as PlaywrightTimeout
import argparse
import json
from datetime import datetime


class AdaptDownloadWAV:
    """Handle downloading adapted music tracks as WAV files."""

    def __init__(self, prompt_set_name: str, track_number: int, duration: int,
                 download_dir: str = "background_music"):
        """
        Initialize the download handler.

        Args:
            prompt_set_name: Name of the prompt set (e.g., "energy_consistency")
            track_number: Track number (1-based)
            duration: Duration in minutes
            download_dir: Directory to save downloaded files
        """
        self.prompt_set_name = prompt_set_name
        self.track_number = track_number
        self.duration = duration
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)

        # Screenshots directory for debugging
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)

        self.page = None
        self.browser = None
        self.context = None

    async def take_screenshot(self, name: str):
        """Take a screenshot for debugging."""
        if self.page:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.screenshots_dir / f"{name}_{timestamp}.png"
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"📸 Screenshot saved: {screenshot_path}")
            return screenshot_path
        return None

    async def find_download_button(self) -> bool:
        """
        Find and click the download button using multiple strategies.

        Returns:
            bool: True if download button found and clicked
        """
        print("\n🔍 Searching for download button...")

        # Strategy 1: Look for download button in History panel
        try:
            print("  Strategy 1: Checking History panel...")
            history_panel = await self.page.wait_for_selector(
                'div[class*="history"], div[id*="history"], aside[class*="history"]',
                timeout=5000
            )

            if history_panel:
                # Look for the most recent adaptation (usually at the top)
                download_buttons = await history_panel.query_selector_all(
                    'button:has-text("Download"), button[aria-label*="download" i], '
                    'a:has-text("Download"), button:has(svg[class*="download"])'
                )

                if download_buttons:
                    print(f"  ✓ Found {len(download_buttons)} download button(s) in History")
                    # Click the first one (most recent)
                    await download_buttons[0].click()
                    await asyncio.sleep(1)
                    return True
        except Exception as e:
            print(f"  ✗ Strategy 1 failed: {e}")

        # Strategy 2: Look for download button in top-right area
        try:
            print("  Strategy 2: Checking top-right area...")
            download_btn = await self.page.wait_for_selector(
                'button:has-text("Download"), button[aria-label*="download" i]',
                timeout=5000
            )

            if download_btn:
                print("  ✓ Found download button in top-right area")
                await download_btn.click()
                await asyncio.sleep(1)
                return True
        except Exception as e:
            print(f"  ✗ Strategy 2 failed: {e}")

        # Strategy 3: Look for download icon (SVG)
        try:
            print("  Strategy 3: Checking for download icon...")
            download_icons = await self.page.query_selector_all(
                'button:has(svg), a:has(svg)'
            )

            for icon_btn in download_icons:
                # Check if the button has download-related SVG
                svg = await icon_btn.query_selector('svg')
                if svg:
                    svg_html = await svg.evaluate('el => el.outerHTML')
                    if 'download' in svg_html.lower() or 'arrow-down' in svg_html.lower():
                        print("  ✓ Found download icon button")
                        await icon_btn.click()
                        await asyncio.sleep(1)
                        return True
        except Exception as e:
            print(f"  ✗ Strategy 3 failed: {e}")

        # Strategy 4: Look for three-dot menu then download option
        try:
            print("  Strategy 4: Checking three-dot menu...")
            menu_buttons = await self.page.query_selector_all(
                'button[aria-label*="menu" i], button[aria-label*="more" i], '
                'button:has-text("⋮"), button:has-text("...")'
            )

            for menu_btn in menu_buttons:
                await menu_btn.click()
                await asyncio.sleep(0.5)

                # Look for download option in the opened menu
                download_option = await self.page.query_selector(
                    'div[role="menu"] button:has-text("Download"), '
                    'div[role="menuitem"]:has-text("Download"), '
                    'li:has-text("Download")'
                )

                if download_option:
                    print("  ✓ Found download in menu")
                    await download_option.click()
                    await asyncio.sleep(1)
                    return True
        except Exception as e:
            print(f"  ✗ Strategy 4 failed: {e}")

        # Strategy 5: Look for any button/link with "download" text
        try:
            print("  Strategy 5: Generic download text search...")
            download_elements = await self.page.query_selector_all(
                '[class*="download" i], [id*="download" i]'
            )

            for elem in download_elements:
                tag_name = await elem.evaluate('el => el.tagName.toLowerCase()')
                if tag_name in ['button', 'a']:
                    print(f"  ✓ Found download element: {tag_name}")
                    await elem.click()
                    await asyncio.sleep(1)
                    return True
        except Exception as e:
            print(f"  ✗ Strategy 5 failed: {e}")

        print("  ✗ No download button found with any strategy")
        await self.take_screenshot("download_button_not_found")
        return False

    async def select_wav_format(self) -> bool:
        """
        Select WAV format from the format selection modal.

        Returns:
            bool: True if WAV format selected successfully
        """
        print("\n🎵 Selecting WAV format...")

        # Wait for modal/menu to appear
        await asyncio.sleep(1)

        # Strategy 1: Look for WAV radio button
        try:
            print("  Strategy 1: Checking for WAV radio button...")
            wav_radio = await self.page.wait_for_selector(
                'input[type="radio"][value*="wav" i], '
                'input[type="radio"][id*="wav" i]',
                timeout=5000
            )

            if wav_radio:
                print("  ✓ Found WAV radio button")
                await wav_radio.click()
                await asyncio.sleep(0.5)
                return True
        except Exception as e:
            print(f"  ✗ Strategy 1 failed: {e}")

        # Strategy 2: Look for WAV button
        try:
            print("  Strategy 2: Checking for WAV button...")
            wav_button = await self.page.wait_for_selector(
                'button:has-text("WAV"), button[value="wav" i], '
                'button[data-format="wav" i]',
                timeout=5000
            )

            if wav_button:
                print("  ✓ Found WAV button")
                await wav_button.click()
                await asyncio.sleep(0.5)
                return True
        except Exception as e:
            print(f"  ✗ Strategy 2 failed: {e}")

        # Strategy 3: Look for WAV label (clicking label clicks radio)
        try:
            print("  Strategy 3: Checking for WAV label...")
            wav_label = await self.page.wait_for_selector(
                'label:has-text("WAV"), span:has-text("WAV")',
                timeout=5000
            )

            if wav_label:
                print("  ✓ Found WAV label")
                await wav_label.click()
                await asyncio.sleep(0.5)
                return True
        except Exception as e:
            print(f"  ✗ Strategy 3 failed: {e}")

        # Strategy 4: Look for dropdown and select WAV
        try:
            print("  Strategy 4: Checking for format dropdown...")
            dropdown = await self.page.wait_for_selector(
                'select[name*="format" i], select[id*="format" i]',
                timeout=5000
            )

            if dropdown:
                print("  ✓ Found format dropdown")
                await dropdown.select_option(label='WAV')
                await asyncio.sleep(0.5)
                return True
        except Exception as e:
            print(f"  ✗ Strategy 4 failed: {e}")

        # Strategy 5: Look for any element with "WAV" text and click it
        try:
            print("  Strategy 5: Generic WAV element search...")
            wav_elements = await self.page.query_selector_all(
                'div:has-text("WAV"), li:has-text("WAV"), '
                '[class*="wav" i]'
            )

            for elem in wav_elements:
                # Check if it's clickable
                is_visible = await elem.is_visible()
                if is_visible:
                    print("  ✓ Found clickable WAV element")
                    await elem.click()
                    await asyncio.sleep(0.5)
                    return True
        except Exception as e:
            print(f"  ✗ Strategy 5 failed: {e}")

        print("  ⚠️  Could not find WAV format selector, continuing anyway...")
        await self.take_screenshot("wav_format_not_found")
        return False

    async def click_download_confirm(self) -> bool:
        """
        Click the final download/confirm button.

        Returns:
            bool: True if confirm button clicked successfully
        """
        print("\n✅ Clicking download confirm button...")

        # Strategy 1: Look for confirm/download button in modal
        try:
            print("  Strategy 1: Checking for confirm button in modal...")
            confirm_btn = await self.page.wait_for_selector(
                'button:has-text("Download"), button:has-text("Confirm"), '
                'button:has-text("OK"), button[type="submit"]',
                timeout=5000
            )

            if confirm_btn:
                # Make sure it's visible and not the same button we clicked before
                is_visible = await confirm_btn.is_visible()
                if is_visible:
                    print("  ✓ Found confirm button")
                    await confirm_btn.click()
                    await asyncio.sleep(1)
                    return True
        except Exception as e:
            print(f"  ✗ Strategy 1 failed: {e}")

        # Strategy 2: Look for primary button in modal dialog
        try:
            print("  Strategy 2: Checking for primary button...")
            primary_btn = await self.page.wait_for_selector(
                'div[role="dialog"] button[class*="primary"], '
                'div[class*="modal"] button[class*="primary"]',
                timeout=5000
            )

            if primary_btn:
                print("  ✓ Found primary button in dialog")
                await primary_btn.click()
                await asyncio.sleep(1)
                return True
        except Exception as e:
            print(f"  ✗ Strategy 2 failed: {e}")

        # Strategy 3: Look for any button in modal that triggers download
        try:
            print("  Strategy 3: Checking all modal buttons...")
            modal_buttons = await self.page.query_selector_all(
                'div[role="dialog"] button, div[class*="modal"] button'
            )

            for btn in modal_buttons:
                text = await btn.inner_text()
                text_lower = text.lower().strip()

                # Look for download-related text (not cancel/close)
                if any(word in text_lower for word in ['download', 'confirm', 'ok', 'yes']):
                    if not any(word in text_lower for word in ['cancel', 'close', 'no']):
                        print(f"  ✓ Found button with text: {text}")
                        await btn.click()
                        await asyncio.sleep(1)
                        return True
        except Exception as e:
            print(f"  ✗ Strategy 3 failed: {e}")

        print("  ⚠️  Could not find confirm button, continuing anyway...")
        await self.take_screenshot("confirm_button_not_found")
        return False

    async def wait_for_download(self) -> tuple[str, int]:
        """
        Wait for download to complete and return file info.

        Returns:
            tuple: (file_path, file_size) or (None, 0) if failed
        """
        print("\n⏳ Waiting for download to complete...")

        try:
            # Wait for download event
            async with self.page.expect_download(timeout=60000) as download_info:
                # The download should already be triggered
                download = await download_info.value

                # Get the suggested filename
                suggested_filename = download.suggested_filename
                print(f"  Original filename: {suggested_filename}")

                # Extract original track name (remove extension)
                original_name = Path(suggested_filename).stem

                # Create new filename with our naming convention
                new_filename = (
                    f"{self.prompt_set_name}_{self.track_number:02d}_"
                    f"{self.duration}min_{original_name}.wav"
                )

                # Save to download directory
                download_path = self.download_dir / new_filename
                await download.save_as(str(download_path))

                # Verify file exists and get size
                if download_path.exists():
                    file_size = download_path.stat().st_size
                    file_size_mb = file_size / (1024 * 1024)

                    print(f"  ✓ Download complete: {download_path}")
                    print(f"  ✓ File size: {file_size_mb:.2f} MB")

                    # Verify it's actually a WAV file
                    if file_size < 1000:
                        print(f"  ⚠️  Warning: File size is suspiciously small ({file_size} bytes)")
                        return None, 0

                    # Check WAV header (RIFF)
                    with open(download_path, 'rb') as f:
                        header = f.read(4)
                        if header != b'RIFF':
                            print(f"  ⚠️  Warning: File does not appear to be a WAV file (header: {header})")
                            return None, 0

                    return str(download_path), file_size
                else:
                    print(f"  ✗ File not found after download: {download_path}")
                    return None, 0

        except PlaywrightTimeout:
            print("  ✗ Download timeout (60 seconds)")
            await self.take_screenshot("download_timeout")
            return None, 0
        except Exception as e:
            print(f"  ✗ Download error: {e}")
            await self.take_screenshot("download_error")
            return None, 0

    async def download_adapted_track(self, page: Page) -> dict:
        """
        Main workflow to download adapted track as WAV.

        Args:
            page: Playwright page object (already navigated to the adaptation page)

        Returns:
            dict: Download result with file_path, file_size, success status
        """
        self.page = page

        result = {
            'success': False,
            'file_path': None,
            'file_size': 0,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }

        try:
            # Step 1: Find and click download button
            print("\n" + "="*60)
            print("STEP 1: Finding download button")
            print("="*60)

            if not await self.find_download_button():
                result['error'] = "Download button not found"
                return result

            await asyncio.sleep(1)

            # Step 2: Select WAV format
            print("\n" + "="*60)
            print("STEP 2: Selecting WAV format")
            print("="*60)

            await self.select_wav_format()
            await asyncio.sleep(1)

            # Step 3: Click confirm/download
            print("\n" + "="*60)
            print("STEP 3: Confirming download")
            print("="*60)

            await self.click_download_confirm()
            await asyncio.sleep(1)

            # Step 4: Wait for download to complete
            print("\n" + "="*60)
            print("STEP 4: Waiting for download")
            print("="*60)

            file_path, file_size = await self.wait_for_download()

            if file_path and file_size > 0:
                result['success'] = True
                result['file_path'] = file_path
                result['file_size'] = file_size

                print("\n" + "="*60)
                print("✅ DOWNLOAD SUCCESSFUL")
                print("="*60)
                print(f"File: {file_path}")
                print(f"Size: {file_size / (1024*1024):.2f} MB")
            else:
                result['error'] = "Download failed or file not saved"
                print("\n" + "="*60)
                print("✗ DOWNLOAD FAILED")
                print("="*60)

            return result

        except Exception as e:
            result['error'] = str(e)
            print(f"\n✗ Error during download: {e}")
            await self.take_screenshot("download_exception")
            return result

    def save_download_log(self, result: dict):
        """Save download result to log file."""
        log_file = self.download_dir / "download_log.jsonl"

        with open(log_file, 'a') as f:
            json.dump(result, f)
            f.write('\n')

        print(f"\n📝 Download log saved: {log_file}")


async def main():
    """Main entry point for standalone usage."""
    parser = argparse.ArgumentParser(
        description="Download adapted music tracks as WAV files"
    )
    parser.add_argument(
        '--prompt-set',
        required=True,
        help='Prompt set name (e.g., energy_consistency)'
    )
    parser.add_argument(
        '--track-num',
        type=int,
        required=True,
        help='Track number (1-based)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        required=True,
        help='Duration in minutes'
    )
    parser.add_argument(
        '--download-dir',
        default='background_music',
        help='Directory to save downloaded files'
    )
    parser.add_argument(
        '--url',
        required=True,
        help='URL of the adaptation page (must be on the results/history page)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )

    args = parser.parse_args()

    # Create downloader instance
    downloader = AdaptDownloadWAV(
        prompt_set_name=args.prompt_set,
        track_number=args.track_num,
        duration=args.duration,
        download_dir=args.download_dir
    )

    # Launch browser and navigate
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=args.headless)
        context = await browser.new_context(
            accept_downloads=True,
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        print(f"\n🌐 Navigating to: {args.url}")
        await page.goto(args.url)
        await page.wait_for_load_state('networkidle')

        # Wait for page to be fully loaded
        await asyncio.sleep(3)

        # Take initial screenshot
        await downloader.take_screenshot("before_download")

        # Execute download workflow
        result = await downloader.download_adapted_track(page)

        # Save log
        downloader.save_download_log(result)

        # Take final screenshot
        await downloader.take_screenshot("after_download")

        await browser.close()

        # Return exit code based on success
        return 0 if result['success'] else 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    exit(exit_code)
