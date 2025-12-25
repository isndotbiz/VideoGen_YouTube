"""
Epidemic Sound Labs Adapt Navigation Automation

Handles navigation to Labs Adapt page, track search, and track loading.
Uses saved session from epidemic_session.json for authentication.

Key Features:
- Session restoration from saved cookies
- Navigation to Labs Adapt interface
- Track search with intelligent waiting
- Result selection and verification
- Waveform loading confirmation
- Extensive error handling and screenshots
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AdaptNavigator:
    """Handles navigation and interaction with Epidemic Sound Labs Adapt"""

    ADAPT_URL = "https://www.epidemicsound.com/labs/adapt/"
    SESSION_FILE = "epidemic_session.json"
    SCREENSHOT_DIR = Path("screenshots/adapt")

    # Timeouts (in milliseconds)
    TIMEOUT_NAVIGATION = 30000
    TIMEOUT_SEARCH = 15000
    TIMEOUT_TRACK_LOAD = 20000
    TIMEOUT_WAVEFORM = 25000

    def __init__(self, headless: bool = False, slow_mo: int = 100):
        """
        Initialize the Adapt Navigator

        Args:
            headless: Run browser in headless mode
            slow_mo: Slow down operations by specified milliseconds
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        # Ensure screenshot directory exists
        self.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    async def _save_screenshot(self, name: str) -> Path:
        """
        Save a screenshot with timestamp

        Args:
            name: Base name for the screenshot

        Returns:
            Path to saved screenshot
        """
        if not self.page:
            logger.warning("Cannot save screenshot - no page available")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = self.SCREENSHOT_DIR / filename

        try:
            await self.page.screenshot(path=str(filepath), full_page=True)
            logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            return None

    async def _load_session(self) -> Dict[str, Any]:
        """
        Load saved session from JSON file

        Returns:
            Session data dictionary

        Raises:
            FileNotFoundError: If session file doesn't exist
            json.JSONDecodeError: If session file is invalid
        """
        session_path = Path(self.SESSION_FILE)

        if not session_path.exists():
            raise FileNotFoundError(
                f"Session file not found: {self.SESSION_FILE}\n"
                "Please run the login script first to save your session."
            )

        try:
            with open(session_path, 'r') as f:
                session_data = json.load(f)

            logger.info(f"Loaded session with {len(session_data.get('cookies', []))} cookies")
            return session_data

        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid session file format: {e}",
                e.doc,
                e.pos
            )

    async def initialize_browser(self) -> Page:
        """
        Initialize browser with saved session

        Returns:
            Page object ready for navigation

        Raises:
            Exception: If browser initialization fails
        """
        logger.info("Initializing browser...")

        try:
            # Load session data
            session_data = await self._load_session()

            # Launch Playwright
            playwright = await async_playwright().start()

            # Launch browser
            self.browser = await playwright.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo
            )

            # Create context with session
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=session_data.get('user_agent',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
            )

            # Add cookies
            if 'cookies' in session_data:
                await self.context.add_cookies(session_data['cookies'])
                logger.info("Session cookies restored")

            # Add local storage if available
            self.page = await self.context.new_page()

            if 'local_storage' in session_data:
                await self.page.goto('https://www.epidemicsound.com')
                for key, value in session_data['local_storage'].items():
                    await self.page.evaluate(
                        f'localStorage.setItem("{key}", {json.dumps(value)})'
                    )
                logger.info("Local storage restored")

            logger.info("Browser initialized successfully")
            return self.page

        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            await self.cleanup()
            raise

    async def navigate_to_adapt(self) -> bool:
        """
        Navigate to Labs Adapt page

        Returns:
            True if navigation successful

        Raises:
            Exception: If navigation fails
        """
        if not self.page:
            raise RuntimeError("Browser not initialized. Call initialize_browser() first.")

        logger.info(f"Navigating to Labs Adapt: {self.ADAPT_URL}")

        try:
            # Navigate to Adapt page
            response = await self.page.goto(
                self.ADAPT_URL,
                wait_until='domcontentloaded',
                timeout=self.TIMEOUT_NAVIGATION
            )

            if not response or response.status >= 400:
                await self._save_screenshot("adapt_navigation_error")
                raise Exception(f"Navigation failed with status: {response.status if response else 'No response'}")

            logger.info("Successfully navigated to Adapt page")

            # Wait for page to stabilize
            await asyncio.sleep(2)

            # Check if we're actually on the Adapt page
            current_url = self.page.url
            if '/labs/adapt' not in current_url:
                await self._save_screenshot("adapt_wrong_page")
                raise Exception(f"Ended up on wrong page: {current_url}")

            logger.info("Confirmed on Labs Adapt page")
            await self._save_screenshot("adapt_page_loaded")

            return True

        except PlaywrightTimeoutError:
            logger.error("Timeout while navigating to Adapt")
            await self._save_screenshot("adapt_navigation_timeout")
            raise
        except Exception as e:
            logger.error(f"Failed to navigate to Adapt: {e}")
            await self._save_screenshot("adapt_navigation_failed")
            raise

    async def _wait_for_search_input(self) -> bool:
        """
        Wait for search input to be available

        Returns:
            True if search input found
        """
        logger.info("Waiting for search input to load...")

        # Possible selectors for the search input
        search_selectors = [
            'input[placeholder*="Search"]',
            'input[placeholder*="search"]',
            'input[type="search"]',
            'input[aria-label*="Search"]',
            'input[aria-label*="search"]',
            '[data-testid*="search"] input',
            '.search-input',
            '#search-input',
            'input.input',  # Common class name
        ]

        for selector in search_selectors:
            try:
                await self.page.wait_for_selector(
                    selector,
                    state='visible',
                    timeout=5000
                )
                logger.info(f"Found search input with selector: {selector}")
                return selector
            except PlaywrightTimeoutError:
                continue

        # If no selector worked, try to find any input that looks like search
        logger.warning("Standard selectors didn't work, scanning all inputs...")
        await self._save_screenshot("searching_for_input")

        inputs = await self.page.query_selector_all('input')
        logger.info(f"Found {len(inputs)} total input elements")

        for i, input_elem in enumerate(inputs):
            try:
                placeholder = await input_elem.get_attribute('placeholder')
                aria_label = await input_elem.get_attribute('aria-label')
                input_type = await input_elem.get_attribute('type')
                class_name = await input_elem.get_attribute('class')

                logger.info(f"Input {i}: type={input_type}, placeholder={placeholder}, aria-label={aria_label}, class={class_name}")

                # Check if this looks like a search input
                if any([
                    placeholder and 'search' in placeholder.lower(),
                    aria_label and 'search' in aria_label.lower(),
                    input_type == 'search',
                    class_name and 'search' in class_name.lower()
                ]):
                    logger.info(f"Found search-like input at index {i}")
                    return f'input:nth-of-type({i+1})'

            except Exception as e:
                logger.debug(f"Error checking input {i}: {e}")
                continue

        return None

    async def search_track(self, track_name: str) -> bool:
        """
        Search for a track in the Adapt search bar

        Args:
            track_name: Name of track to search for

        Returns:
            True if search executed successfully

        Raises:
            Exception: If search fails
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")

        logger.info(f"Searching for track: {track_name}")

        try:
            # Wait for and find search input
            search_selector = await self._wait_for_search_input()

            if not search_selector:
                await self._save_screenshot("search_input_not_found")
                raise Exception("Could not find search input on Adapt page")

            # Clear any existing text
            await self.page.click(search_selector, click_count=3)
            await self.page.keyboard.press('Backspace')
            await asyncio.sleep(0.5)

            # Type the track name
            logger.info(f"Typing track name into search: {track_name}")
            await self.page.fill(search_selector, track_name)
            await asyncio.sleep(1)

            # Take screenshot after typing
            await self._save_screenshot("search_typed")

            # Press Enter to search
            await self.page.keyboard.press('Enter')
            await asyncio.sleep(2)

            logger.info("Search query submitted")
            await self._save_screenshot("search_submitted")

            return True

        except Exception as e:
            logger.error(f"Failed to search for track: {e}")
            await self._save_screenshot("search_failed")
            raise

    async def _wait_for_search_results(self) -> bool:
        """
        Wait for search results to appear

        Returns:
            True if results found
        """
        logger.info("Waiting for search results...")

        # Possible selectors for search results
        result_selectors = [
            '[role="listbox"]',
            '[role="list"]',
            '.search-results',
            '.results-list',
            '[data-testid*="results"]',
            '[data-testid*="search-result"]',
            '.track-item',
            '[class*="result"]',
        ]

        for selector in result_selectors:
            try:
                await self.page.wait_for_selector(
                    selector,
                    state='visible',
                    timeout=5000
                )
                logger.info(f"Found search results with selector: {selector}")
                return selector
            except PlaywrightTimeoutError:
                continue

        # Check if there are any visible lists or items that appeared
        await asyncio.sleep(2)
        await self._save_screenshot("checking_for_results")

        logger.warning("Could not find results with standard selectors")
        return None

    async def select_first_track(self) -> bool:
        """
        Select the first track from search results

        Returns:
            True if track selected successfully

        Raises:
            Exception: If track selection fails
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")

        logger.info("Selecting first track from search results...")

        try:
            # Wait for results to appear
            results_selector = await self._wait_for_search_results()

            if not results_selector:
                logger.warning("Results selector not found, will try alternative approach")

            # Possible selectors for individual track items
            track_selectors = [
                f'{results_selector} > *:first-child' if results_selector else None,
                '[role="option"]:first-of-type',
                '.track-item:first-of-type',
                '[data-testid*="track"]:first-of-type',
                '[class*="track"]:first-of-type',
                'button:has-text("Play")',
                'li:first-of-type',
            ]

            # Remove None values
            track_selectors = [s for s in track_selectors if s]

            track_element = None
            selected_selector = None

            for selector in track_selectors:
                try:
                    track_element = await self.page.wait_for_selector(
                        selector,
                        state='visible',
                        timeout=3000
                    )
                    if track_element:
                        selected_selector = selector
                        logger.info(f"Found track element with selector: {selector}")
                        break
                except PlaywrightTimeoutError:
                    continue

            if not track_element:
                # Try clicking on any clickable element that appeared
                logger.warning("Standard selectors failed, looking for clickable elements...")
                await self._save_screenshot("no_track_element_found")

                # Try to find buttons or links
                clickables = await self.page.query_selector_all('button, a, [role="button"], [role="option"]')

                if clickables:
                    logger.info(f"Found {len(clickables)} clickable elements, trying first one")
                    track_element = clickables[0]
                else:
                    raise Exception("No clickable track elements found in search results")

            # Get track info before clicking
            try:
                track_text = await track_element.text_content()
                logger.info(f"Selecting track: {track_text[:100]}")
            except:
                logger.info("Selecting track (couldn't get text)")

            await self._save_screenshot("before_track_click")

            # Click the track
            await track_element.click()
            await asyncio.sleep(2)

            logger.info("Track clicked successfully")
            await self._save_screenshot("after_track_click")

            return True

        except Exception as e:
            logger.error(f"Failed to select track: {e}")
            await self._save_screenshot("track_selection_failed")
            raise

    async def verify_track_loaded(self) -> bool:
        """
        Verify that the track has loaded in the Adapt interface
        Checks for waveform display and other UI elements

        Returns:
            True if track loaded successfully

        Raises:
            Exception: If track loading verification fails
        """
        if not self.page:
            raise RuntimeError("Browser not initialized")

        logger.info("Verifying track loaded in Adapt interface...")

        try:
            # Wait a moment for loading
            await asyncio.sleep(3)
            await self._save_screenshot("verifying_track_load")

            # Possible selectors for waveform or track loaded state
            waveform_selectors = [
                'canvas',  # Waveforms are often drawn on canvas
                '[class*="waveform"]',
                '[class*="audio-visual"]',
                '[data-testid*="waveform"]',
                'svg',  # Sometimes waveforms are SVG
                '[class*="player"]',
                '[class*="timeline"]',
            ]

            found_elements = []

            for selector in waveform_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    if elements:
                        found_elements.append({
                            'selector': selector,
                            'count': len(elements)
                        })
                        logger.info(f"Found {len(elements)} elements matching: {selector}")
                except Exception as e:
                    logger.debug(f"Error checking selector {selector}: {e}")

            if not found_elements:
                logger.warning("No waveform elements found with standard selectors")
                await self._save_screenshot("no_waveform_found")
                raise Exception("Could not verify track waveform loaded")

            # Check for canvas elements specifically (most common for waveforms)
            canvas_elements = await self.page.query_selector_all('canvas')

            if canvas_elements:
                logger.info(f"Found {len(canvas_elements)} canvas elements (likely waveforms)")

                # Check if any canvas has content (width/height > 0)
                for i, canvas in enumerate(canvas_elements):
                    try:
                        width = await canvas.evaluate('el => el.width')
                        height = await canvas.evaluate('el => el.height')
                        logger.info(f"Canvas {i}: {width}x{height}")

                        if width > 0 and height > 0:
                            logger.info(f"Canvas {i} appears to have content (waveform)")
                    except Exception as e:
                        logger.debug(f"Error checking canvas {i}: {e}")

            # Look for playback controls as additional verification
            control_selectors = [
                'button[aria-label*="Play"]',
                'button[aria-label*="play"]',
                '[class*="play-button"]',
                '[data-testid*="play"]',
            ]

            for selector in control_selectors:
                try:
                    control = await self.page.query_selector(selector)
                    if control:
                        logger.info(f"Found playback control: {selector}")
                        break
                except:
                    pass

            await self._save_screenshot("track_loaded_verified")
            logger.info("Track appears to be loaded successfully")

            return True

        except PlaywrightTimeoutError:
            logger.error("Timeout waiting for track to load")
            await self._save_screenshot("track_load_timeout")
            raise
        except Exception as e:
            logger.error(f"Failed to verify track loaded: {e}")
            await self._save_screenshot("track_verification_failed")
            raise

    async def navigate_and_search(self, track_name: str) -> Page:
        """
        Complete workflow: navigate to Adapt and search for track

        Args:
            track_name: Name of track to search for

        Returns:
            Page object ready for Adapt operations

        Raises:
            Exception: If any step fails
        """
        try:
            # Initialize browser with session
            await self.initialize_browser()

            # Navigate to Adapt page
            await self.navigate_to_adapt()

            # Search for track
            await self.search_track(track_name)

            # Select first result
            await self.select_first_track()

            # Verify track loaded
            await self.verify_track_loaded()

            logger.info("✓ Navigation and search completed successfully!")
            logger.info("Page is ready for Adapt operations (length adjustment, etc.)")

            return self.page

        except Exception as e:
            logger.error(f"Failed during navigate_and_search: {e}")
            await self._save_screenshot("workflow_failed")
            raise

    async def cleanup(self):
        """Clean up browser resources"""
        logger.info("Cleaning up browser resources...")

        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            logger.info("Cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


async def main():
    """
    Main function for testing the Adapt navigation
    """
    # Test track name - adjust this to match your needs
    TEST_TRACK_NAME = "upbeat"  # Change this to your test track

    logger.info("=" * 60)
    logger.info("Epidemic Sound Labs Adapt Navigation Test")
    logger.info("=" * 60)

    navigator = AdaptNavigator(headless=False, slow_mo=100)

    try:
        # Run the complete workflow
        page = await navigator.navigate_and_search(TEST_TRACK_NAME)

        logger.info("\n" + "=" * 60)
        logger.info("SUCCESS! Track loaded in Adapt interface")
        logger.info("=" * 60)
        logger.info("\nPage is ready for further operations:")
        logger.info("  - Adjust track length")
        logger.info("  - Download adapted version")
        logger.info("  - Apply other Adapt features")
        logger.info("\nBrowser will remain open for inspection...")

        # Keep browser open for inspection
        await asyncio.sleep(30)

    except FileNotFoundError as e:
        logger.error("\n" + "!" * 60)
        logger.error("SESSION FILE NOT FOUND")
        logger.error("!" * 60)
        logger.error(f"\n{e}")
        logger.error("\nPlease run the login script first to save your session:")
        logger.error("  python epidemic_login.py")

    except Exception as e:
        logger.error("\n" + "!" * 60)
        logger.error("NAVIGATION FAILED")
        logger.error("!" * 60)
        logger.error(f"\n{e}")
        logger.error(f"\nCheck screenshots in: {navigator.SCREENSHOT_DIR}")

    finally:
        await navigator.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
