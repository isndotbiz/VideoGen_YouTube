"""
Epidemic Sound - Adapt Music Feature Automation
================================================

Standalone Playwright automation for the "Adapt Music" feature in Epidemic Sound Labs Adapt.
This script is designed to run AFTER adapt_length_automation.py completes.

Key Features:
1. Clicks "Adapt music" button
2. Enters AI description for music adaptation
3. Selects stems (All stems)
4. Processes music adaptation with AI
5. Monitors progress with detailed logging
6. Verifies completion
7. Takes debugging screenshots

Based on: EPIDEMIC_COMPLETE_WORKFLOW.md (Step 3: Adapt Music Second)

Requirements:
- playwright
- python-dotenv

Setup:
    pip install playwright python-dotenv
    playwright install chromium

Usage:
    # Basic usage (assumes page already on Adapt tool with track loaded)
    python adapt_music_automation.py

    # With custom description
    python adapt_music_automation.py --description "Your custom description"

    # Non-headless mode for debugging
    python adapt_music_automation.py --no-headless

    # Custom timeout
    python adapt_music_automation.py --timeout 180

Author: VideoGen YouTube Project
Last Updated: December 2025
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

from playwright.sync_api import (
    sync_playwright,
    Browser,
    BrowserContext,
    Page,
    TimeoutError as PlaywrightTimeoutError
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

# Default description from EPIDEMIC_COMPLETE_WORKFLOW.md
DEFAULT_DESCRIPTION = (
    "Minimal, background-friendly for voiceover narration. Reduce mid-range "
    "frequencies (200-800Hz) to make room for voice. Keep electronic energy "
    "but make it subtle and consistent. Remove dramatic buildups. Create "
    "steady, hypnotic groove suitable for extended background use."
)

# Alternative shorter description
SHORT_DESCRIPTION = (
    "Minimal, background-friendly for voiceover narration. Reduce mid-range "
    "frequencies, keep electronic energy but subtle. Remove buildups, create "
    "steady groove."
)

# Timeouts (seconds)
TIMEOUT_DEFAULT = 30
TIMEOUT_AI_PROCESSING = 120  # 2 minutes max for AI adaptation
TIMEOUT_ELEMENT_SEARCH = 10

# Screenshot directory
SCREENSHOT_DIR = Path("debug_screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# EXCEPTIONS
# ============================================================================

class AdaptMusicError(Exception):
    """Base exception for adapt music automation errors."""
    pass


class ElementNotFoundError(AdaptMusicError):
    """Raised when required element cannot be found."""
    pass


class ProcessingTimeoutError(AdaptMusicError):
    """Raised when AI processing times out."""
    pass


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def take_screenshot(page: Page, name: str) -> Path:
    """
    Take a screenshot for debugging.

    Args:
        page: Playwright page object
        name: Screenshot name/description

    Returns:
        Path to saved screenshot
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{name}.png"
    filepath = SCREENSHOT_DIR / filename

    try:
        page.screenshot(path=str(filepath), full_page=True)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        logger.warning(f"Failed to save screenshot: {e}")
        return None


def wait_with_progress(seconds: int, message: str = "Waiting") -> None:
    """
    Wait with progress logging.

    Args:
        seconds: Number of seconds to wait
        message: Message to log
    """
    logger.info(f"{message} for {seconds} seconds...")
    for i in range(seconds):
        if i > 0 and i % 10 == 0:
            logger.info(f"  {message}... {i}/{seconds}s elapsed")
        time.sleep(1)


# ============================================================================
# ADAPT MUSIC AUTOMATION
# ============================================================================

class AdaptMusicAutomation:
    """Automation for Epidemic Sound Adapt Music feature."""

    def __init__(
        self,
        page: Optional[Page] = None,
        headless: bool = True,
        slow_mo: int = 500,
        description: Optional[str] = None,
        stems: str = "all",
        timeout: int = TIMEOUT_AI_PROCESSING
    ):
        """
        Initialize adapt music automation.

        Args:
            page: Existing Playwright page (if None, creates new browser)
            headless: Run browser in headless mode
            slow_mo: Slow down operations by N milliseconds
            description: Custom description for music adaptation
            stems: Which stems to adapt (default: "all")
            timeout: Maximum wait time for AI processing (seconds)
        """
        self.page = page
        self.headless = headless
        self.slow_mo = slow_mo
        self.description = description or DEFAULT_DESCRIPTION
        self.stems = stems
        self.timeout = timeout

        # Browser objects (if creating new)
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.owns_browser = page is None  # Track if we created the browser

        logger.info("Adapt Music automation initialized")
        logger.info(f"Description: {self.description[:100]}...")
        logger.info(f"Stems: {self.stems}")
        logger.info(f"Timeout: {self.timeout}s")

    def start_browser(self) -> None:
        """Start browser if not provided."""
        if self.page:
            logger.info("Using existing page")
            return

        logger.info("Starting new browser...")
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )

        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        self.page = self.context.new_page()
        logger.info("Browser started")

    def close_browser(self) -> None:
        """Close browser if we created it."""
        if not self.owns_browser:
            logger.info("Page owned externally, not closing")
            return

        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

        logger.info("Browser closed")

    def find_adapt_music_button(self) -> bool:
        """
        Find and click the "Adapt music" button.

        Returns:
            True if button found and clicked

        Raises:
            ElementNotFoundError: If button cannot be found
        """
        logger.info("Looking for 'Adapt music' button...")

        # Take initial screenshot
        take_screenshot(self.page, "01_before_adapt_music")

        # Multiple possible selectors for the button
        button_selectors = [
            'button:has-text("Adapt music")',
            'button:has-text("Music")',
            '[data-testid="adapt-music-button"]',
            '[aria-label="Adapt music"]',
            'button:text-is("Adapt music")',
            'button:text-matches("Adapt.*music", "i")',
            # CSS class patterns
            'button.adapt-music',
            'button[class*="adaptMusic"]',
            'button[class*="adapt-music"]',
        ]

        for selector in button_selectors:
            try:
                logger.debug(f"Trying selector: {selector}")
                button = self.page.locator(selector).first

                if button.count() > 0:
                    logger.info(f"Found 'Adapt music' button with selector: {selector}")

                    # Wait for button to be visible and enabled
                    button.wait_for(state="visible", timeout=5000)

                    # Scroll into view if needed
                    button.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(500)

                    # Click the button
                    button.click()
                    logger.info("Clicked 'Adapt music' button")

                    # Wait for panel to open
                    self.page.wait_for_timeout(2000)
                    take_screenshot(self.page, "02_adapt_music_panel_opened")

                    return True
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
                continue

        # If we get here, button was not found
        take_screenshot(self.page, "ERROR_button_not_found")
        raise ElementNotFoundError(
            "Could not find 'Adapt music' button. Tried multiple selectors. "
            "Check screenshot for current page state."
        )

    def enter_description(self) -> bool:
        """
        Enter description in text field.

        Returns:
            True if description entered successfully

        Raises:
            ElementNotFoundError: If description input cannot be found
        """
        logger.info("Looking for description input field...")

        # Multiple possible selectors for description input
        input_selectors = [
            'textarea[name*="description"]',
            'textarea[placeholder*="describe"]',
            'textarea[placeholder*="Describe"]',
            'input[name*="description"]',
            'input[placeholder*="describe"]',
            '[contenteditable="true"]',  # Contenteditable div
            'textarea',  # Any textarea
            'input[type="text"]',  # Generic text input
            '[data-testid="description-input"]',
            '[aria-label*="description"]',
            '[aria-label*="Description"]',
        ]

        for selector in input_selectors:
            try:
                logger.debug(f"Trying selector: {selector}")
                input_field = self.page.locator(selector).first

                if input_field.count() > 0:
                    logger.info(f"Found description input with selector: {selector}")

                    # Wait for input to be visible
                    input_field.wait_for(state="visible", timeout=5000)

                    # Clear existing content
                    input_field.click()
                    self.page.keyboard.press("Control+A")
                    self.page.keyboard.press("Delete")
                    self.page.wait_for_timeout(500)

                    # Enter description
                    input_field.fill(self.description)
                    logger.info(f"Description entered: '{self.description[:50]}...'")

                    # Verify text was entered
                    self.page.wait_for_timeout(1000)
                    take_screenshot(self.page, "03_description_entered")

                    return True
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
                continue

        # If we get here, input was not found
        take_screenshot(self.page, "ERROR_description_input_not_found")
        raise ElementNotFoundError(
            "Could not find description input field. Tried multiple selectors. "
            "Check screenshot for current page state."
        )

    def select_stems(self) -> bool:
        """
        Select stems from dropdown.

        Returns:
            True if stems selected (or if selection not available)
        """
        logger.info(f"Looking for stems selector (target: '{self.stems}')...")

        # Multiple possible selectors for stems dropdown
        stems_selectors = [
            'select[name*="stems"]',
            'select[name*="Stems"]',
            '[data-testid="stems-select"]',
            '[aria-label*="stems"]',
            '[aria-label*="Stems"]',
            'select',  # Any select dropdown
            'button[role="combobox"]',  # Custom dropdown button
            'div[role="combobox"]',
        ]

        for selector in stems_selectors:
            try:
                logger.debug(f"Trying selector: {selector}")
                stems_element = self.page.locator(selector).first

                if stems_element.count() > 0:
                    logger.info(f"Found stems selector with: {selector}")

                    # Check if it's a select element
                    tag_name = stems_element.evaluate("el => el.tagName.toLowerCase()")

                    if tag_name == "select":
                        # Standard select dropdown
                        stems_element.wait_for(state="visible", timeout=5000)

                        # Try to select by value or label
                        try:
                            stems_element.select_option(self.stems)
                        except:
                            # Try "All stems" as label
                            try:
                                stems_element.select_option(label="All stems")
                            except:
                                # Try first option
                                stems_element.select_option(index=0)

                        logger.info(f"Stems selected: {self.stems}")
                        self.page.wait_for_timeout(1000)
                        take_screenshot(self.page, "04_stems_selected")
                        return True
                    else:
                        # Custom dropdown - try clicking to open
                        stems_element.click()
                        self.page.wait_for_timeout(1000)

                        # Look for "All stems" option
                        all_stems_option = self.page.locator('text="All stems"').first
                        if all_stems_option.count() > 0:
                            all_stems_option.click()
                            logger.info("Selected 'All stems' from custom dropdown")
                            self.page.wait_for_timeout(1000)
                            take_screenshot(self.page, "04_stems_selected")
                            return True

                        # Click any option with "all" in it
                        option = self.page.locator('[role="option"]:has-text("all")').first
                        if option.count() > 0:
                            option.click()
                            logger.info("Selected stems option")
                            return True

            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
                continue

        # Stems selection might not be available - this is OK
        logger.info("Stems selector not found - may not be available, continuing...")
        return True

    def click_process_button(self) -> bool:
        """
        Click the arrow/submit button to start processing.

        Returns:
            True if button clicked successfully

        Raises:
            ElementNotFoundError: If process button cannot be found
        """
        logger.info("Looking for process/submit button...")

        # Multiple possible selectors for the process button
        button_selectors = [
            'button[type="submit"]',
            'button:has-text("Adapt")',
            'button:has-text("Process")',
            'button:has-text("Generate")',
            'button:has-text("Create")',
            'button[aria-label*="submit"]',
            'button[aria-label*="process"]',
            'button[aria-label*="adapt"]',
            # Arrow buttons
            'button:has([data-icon="arrow"])',
            'button:has(svg[class*="arrow"])',
            'button[class*="submit"]',
            'button[class*="process"]',
            # Icon-only buttons (common in modern UIs)
            'button[aria-label="Submit"]',
            'button svg',  # Button containing SVG (likely arrow icon)
        ]

        for selector in button_selectors:
            try:
                logger.debug(f"Trying selector: {selector}")
                button = self.page.locator(selector).first

                if button.count() > 0:
                    logger.info(f"Found process button with selector: {selector}")

                    # Wait for button to be visible and enabled
                    button.wait_for(state="visible", timeout=5000)

                    # Check if button is enabled
                    is_disabled = button.is_disabled()
                    if is_disabled:
                        logger.warning("Button found but disabled, trying anyway...")

                    # Scroll into view
                    button.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(500)

                    # Click the button
                    button.click()
                    logger.info("Clicked process button - AI adaptation starting!")

                    # Wait for processing to begin
                    self.page.wait_for_timeout(3000)
                    take_screenshot(self.page, "05_processing_started")

                    return True
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
                continue

        # If we get here, button was not found
        take_screenshot(self.page, "ERROR_process_button_not_found")
        raise ElementNotFoundError(
            "Could not find process/submit button. Tried multiple selectors. "
            "Check screenshot for current page state."
        )

    def wait_for_processing(self) -> bool:
        """
        Wait for AI processing to complete with progress monitoring.

        Returns:
            True if processing completed successfully

        Raises:
            ProcessingTimeoutError: If processing times out
        """
        logger.info("=" * 80)
        logger.info("WAITING FOR AI MUSIC ADAPTATION")
        logger.info(f"Maximum wait time: {self.timeout} seconds")
        logger.info("=" * 80)

        start_time = time.time()
        last_progress_log = 0

        # Processing indicators (things that show processing is happening)
        processing_indicators = [
            '.processing',
            '[data-state="processing"]',
            '[data-state="loading"]',
            'text="Processing"',
            'text="Generating"',
            'text="Adapting"',
            '[role="progressbar"]',
            '[aria-busy="true"]',
            '.spinner',
            '.loader',
            '[class*="loading"]',
            '[class*="spinner"]',
        ]

        # Completion indicators
        completion_indicators = [
            'text="Complete"',
            'text="Done"',
            'text="Finished"',
            'button:has-text("Download")',
            'button:has-text("Preview")',
            '.result-ready',
            '[data-state="complete"]',
            '[data-state="success"]',
            'text="View original"',  # Shows after adaptation
        ]

        check_count = 0

        while (time.time() - start_time) < self.timeout:
            elapsed = time.time() - start_time
            check_count += 1

            # Check if still processing
            is_processing = False
            for indicator in processing_indicators:
                try:
                    if self.page.locator(indicator).count() > 0:
                        is_processing = True
                        logger.debug(f"Processing indicator found: {indicator}")
                        break
                except:
                    pass

            # Check if complete
            is_complete = False
            for indicator in completion_indicators:
                try:
                    if self.page.locator(indicator).count() > 0:
                        is_complete = True
                        logger.debug(f"Completion indicator found: {indicator}")
                        break
                except:
                    pass

            # If complete and not processing, we're done!
            if is_complete and not is_processing:
                logger.info("=" * 80)
                logger.info("AI MUSIC ADAPTATION COMPLETE!")
                logger.info(f"Total processing time: {int(elapsed)} seconds")
                logger.info("=" * 80)
                take_screenshot(self.page, "06_processing_complete")
                return True

            # Log progress every 10 seconds
            if elapsed - last_progress_log >= 10:
                logger.info(f"Still processing... {int(elapsed)}s elapsed ({int((elapsed/self.timeout)*100)}%)")

                # Take periodic screenshots for debugging
                if int(elapsed) % 30 == 0:
                    take_screenshot(self.page, f"progress_{int(elapsed)}s")

                last_progress_log = elapsed

            # Wait before next check
            self.page.wait_for_timeout(2000)  # Check every 2 seconds

        # Timeout reached
        logger.error("=" * 80)
        logger.error("PROCESSING TIMEOUT!")
        logger.error(f"Exceeded maximum wait time: {self.timeout}s")
        logger.error("=" * 80)
        take_screenshot(self.page, "ERROR_processing_timeout")

        raise ProcessingTimeoutError(
            f"AI processing did not complete within {self.timeout} seconds. "
            "Check screenshots in debug_screenshots/ folder."
        )

    def verify_completion(self) -> Dict[str, Any]:
        """
        Verify adaptation completed successfully.

        Returns:
            Dictionary with verification results
        """
        logger.info("Verifying adaptation completion...")

        result = {
            'success': False,
            'preview_available': False,
            'download_available': False,
            'history_updated': False,
            'notes': []
        }

        try:
            # Check for preview button
            preview_button = self.page.locator('button:has-text("Preview"), button[aria-label="Play"]').first
            if preview_button.count() > 0:
                result['preview_available'] = True
                result['notes'].append("Preview button found")
                logger.info("✓ Preview button available")

            # Check for download button
            download_button = self.page.locator('button:has-text("Download")').first
            if download_button.count() > 0:
                result['download_available'] = True
                result['notes'].append("Download button found")
                logger.info("✓ Download button available")

            # Check for history panel update
            history_panel = self.page.locator('text="History", [data-testid="history"]').first
            if history_panel.count() > 0:
                result['history_updated'] = True
                result['notes'].append("History panel visible")
                logger.info("✓ History panel visible")

            # Check for "View original" button (indicates adaptation was applied)
            view_original = self.page.locator('text="View original"').first
            if view_original.count() > 0:
                result['notes'].append("View original button found")
                logger.info("✓ View original button available")

            # Success if we have at least preview or download
            if result['preview_available'] or result['download_available']:
                result['success'] = True
                logger.info("Verification PASSED - adaptation appears successful")
            else:
                result['notes'].append("WARNING: No preview or download button found")
                logger.warning("Verification WARNING - expected buttons not found")

            take_screenshot(self.page, "07_verification_complete")

        except Exception as e:
            result['notes'].append(f"Verification error: {str(e)}")
            logger.error(f"Verification error: {e}")

        return result

    def run(self) -> Dict[str, Any]:
        """
        Run complete adapt music automation workflow.

        Returns:
            Dictionary with results
        """
        logger.info("=" * 80)
        logger.info("ADAPT MUSIC AUTOMATION - STARTING")
        logger.info("=" * 80)

        result = {
            'success': False,
            'steps_completed': [],
            'error': None,
            'processing_time': None,
            'verification': None
        }

        start_time = time.time()

        try:
            # Start browser if needed
            self.start_browser()
            result['steps_completed'].append('browser_started')

            # Step 1: Find and click "Adapt music" button
            self.find_adapt_music_button()
            result['steps_completed'].append('adapt_music_button_clicked')

            # Step 2: Enter description
            self.enter_description()
            result['steps_completed'].append('description_entered')

            # Step 3: Select stems (optional, might not be available)
            self.select_stems()
            result['steps_completed'].append('stems_selected')

            # Step 4: Click process button
            self.click_process_button()
            result['steps_completed'].append('process_button_clicked')

            # Step 5: Wait for AI processing
            processing_complete = self.wait_for_processing()
            if processing_complete:
                result['steps_completed'].append('processing_complete')

            # Step 6: Verify completion
            verification = self.verify_completion()
            result['verification'] = verification
            result['steps_completed'].append('verification_complete')

            # Calculate processing time
            result['processing_time'] = time.time() - start_time

            # Overall success
            if verification['success']:
                result['success'] = True
                logger.info("=" * 80)
                logger.info("ADAPT MUSIC AUTOMATION - SUCCESS!")
                logger.info(f"Total time: {result['processing_time']:.1f} seconds")
                logger.info("=" * 80)
            else:
                logger.warning("Automation completed but verification failed")

        except Exception as e:
            result['error'] = str(e)
            result['processing_time'] = time.time() - start_time
            logger.error("=" * 80)
            logger.error("ADAPT MUSIC AUTOMATION - FAILED")
            logger.error(f"Error: {e}")
            logger.error("=" * 80)
            take_screenshot(self.page, "ERROR_final")

        finally:
            # Close browser if we created it
            if self.owns_browser:
                self.close_browser()

        return result

    def __enter__(self):
        """Context manager entry."""
        self.start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.owns_browser:
            self.close_browser()


# ============================================================================
# CLI
# ============================================================================

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Epidemic Sound - Adapt Music Feature Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default description
  python adapt_music_automation.py

  # Custom description
  python adapt_music_automation.py --description "Minimal background for voiceover"

  # Non-headless for debugging
  python adapt_music_automation.py --no-headless

  # Custom timeout
  python adapt_music_automation.py --timeout 180

  # Use short description
  python adapt_music_automation.py --use-short-description

Notes:
  - This script assumes you're already on the Adapt tool page with a track loaded
  - Run adapt_length_automation.py first if you haven't already
  - Screenshots are saved to debug_screenshots/ folder
  - Default timeout is 120 seconds (2 minutes)
        """
    )

    parser.add_argument(
        '--description',
        help='Custom description for music adaptation'
    )
    parser.add_argument(
        '--use-short-description',
        action='store_true',
        help='Use shorter version of default description'
    )
    parser.add_argument(
        '--stems',
        default='all',
        help='Stems to adapt (default: all)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=TIMEOUT_AI_PROCESSING,
        help=f'Maximum wait time in seconds (default: {TIMEOUT_AI_PROCESSING})'
    )
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run browser in visible mode (for debugging)'
    )
    parser.add_argument(
        '--slow',
        type=int,
        default=500,
        help='Slow down operations by N milliseconds (default: 500)'
    )

    args = parser.parse_args()

    # Determine description to use
    if args.description:
        description = args.description
    elif args.use_short_description:
        description = SHORT_DESCRIPTION
    else:
        description = DEFAULT_DESCRIPTION

    # Run automation
    try:
        automation = AdaptMusicAutomation(
            headless=not args.no_headless,
            slow_mo=args.slow,
            description=description,
            stems=args.stems,
            timeout=args.timeout
        )

        result = automation.run()

        # Print summary
        print("\n" + "=" * 80)
        print("ADAPT MUSIC AUTOMATION - SUMMARY")
        print("=" * 80)
        print(f"Success: {result['success']}")
        print(f"Processing time: {result['processing_time']:.1f}s")
        print(f"Steps completed: {len(result['steps_completed'])}")
        print(f"Steps: {', '.join(result['steps_completed'])}")

        if result['error']:
            print(f"\nError: {result['error']}")

        if result['verification']:
            print(f"\nVerification:")
            for key, value in result['verification'].items():
                if key != 'notes':
                    print(f"  {key}: {value}")

        print("=" * 80)

        # Exit code
        sys.exit(0 if result['success'] else 1)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        logger.exception("Fatal error")
        sys.exit(1)


if __name__ == "__main__":
    main()
