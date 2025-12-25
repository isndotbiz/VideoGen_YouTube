#!/usr/bin/env python3
"""
Epidemic Sound Labs Adapt - Complete Automation Pipeline
=========================================================

Master orchestration script that combines all Adapt automation modules into
a complete workflow for downloading background music optimized for voiceover.

This script automates:
1. Navigation to Labs Adapt
2. Track search and selection
3. Length adaptation (3 minutes, ducking enabled, steady section)
4. Music adaptation (minimal, background-friendly)
5. WAV download
6. Progress tracking and error handling

Usage:
    # Download specific tracks
    python labs_adapt_complete.py --tracks "Track Name 1" "Track Name 2" "Track Name 3"

    # Download first N tracks from Electronic genre
    python labs_adapt_complete.py --count 5

    # Resume from checkpoint
    python labs_adapt_complete.py --resume

    # Run in headless mode (faster, no GUI)
    python labs_adapt_complete.py --headless --count 5

Requirements:
    pip install playwright
    playwright install chromium

Session:
    Must have valid epidemic_session.json file (run epidemic_browser_login.py first)

Expected Runtime:
    5-8 minutes per track:
    - Navigation: 1-2 min
    - Adapt Length: 1 min
    - Adapt Music: 1-2 min
    - Download: 1 min
    - Buffer: 1-2 min

Author: VideoGen YouTube Project
Last Updated: December 2025
"""

import asyncio
import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any

from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    TimeoutError as PlaywrightTimeoutError,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("labs_adapt_complete.log", encoding='utf-8'),
    ],
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class TrackTask:
    """Individual track download task"""
    track_name: str
    track_index: int
    status: str = "pending"  # pending, navigating, adapting_length, adapting_music, downloading, completed, failed
    download_path: Optional[str] = None
    error: Optional[str] = None
    attempts: int = 0
    start_time: Optional[float] = None
    end_time: Optional[float] = None


@dataclass
class ProgressStats:
    """Overall progress statistics"""
    total_tracks: int
    completed: int = 0
    failed: int = 0
    current_track: str = ""
    current_status: str = ""
    start_time: float = 0.0
    estimated_completion_time: float = 0.0


class AdaptConfig:
    """Configuration for Adapt processing"""

    # Length adaptation
    LENGTH_DURATION_SECONDS = 180  # 3 minutes
    LENGTH_ENABLE_DUCKING = True
    LENGTH_SECTION_TYPE = "steady"  # steady, energetic, calm

    # Music adaptation
    MUSIC_DESCRIPTION = (
        "Minimal, background-friendly for voiceover narration. "
        "Reduce mid-range frequencies 200-800Hz where voice sits. "
        "Keep electronic energy but subtle. Remove buildups and drops. "
        "Create steady, consistent groove with narrow dynamic range. "
        "Optimize for ducking mix technology."
    )
    MUSIC_STEMS = "all"

    # Download
    DOWNLOAD_FORMAT = "wav"
    OUTPUT_DIR = Path("background_music_epidemic/labs_adapt_complete")

    # Timeouts
    TIMEOUT_NAVIGATION = 30000  # 30 seconds
    TIMEOUT_ADAPT_PROCESSING = 120000  # 2 minutes
    TIMEOUT_DOWNLOAD = 120000  # 2 minutes

    # Retry
    MAX_RETRY_ATTEMPTS = 2
    RETRY_DELAY_SECONDS = 5


# ============================================================================
# SESSION MANAGER
# ============================================================================

class SessionManager:
    """Manage browser session with saved cookies"""

    SESSION_FILE = "epidemic_session.json"
    BASE_URL = "https://www.epidemicsound.com"

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.session_file = Path(self.SESSION_FILE)
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self) -> None:
        """Start browser with saved session"""
        logger.info("Starting browser session...")

        if not self.session_file.exists():
            raise RuntimeError(
                f"Session file not found: {self.session_file}\n"
                "Please run epidemic_browser_login.py first to create a session."
            )

        # Load session
        with open(self.session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)

        storage_state = session_data.get('storage_state')
        if not storage_state:
            raise RuntimeError("Invalid session file - no storage state found")

        # Start browser
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ],
        )

        # Create context with saved session
        self.context = await self.browser.new_context(
            storage_state=storage_state,
            viewport={'width': 1920, 'height': 1080},
            user_agent=(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
        )

        self.page = await self.context.new_page()
        logger.info("Browser session started with saved cookies")

    async def close(self) -> None:
        """Close browser"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info("Browser session closed")

    async def get_page(self) -> Page:
        """Get active page"""
        if not self.page:
            raise RuntimeError("Session not started")
        return self.page


# ============================================================================
# NAVIGATION MODULE
# ============================================================================

class AdaptNavigation:
    """Navigate to Labs Adapt and search for tracks"""

    LABS_URL = "https://www.epidemicsound.com/labs/"
    ADAPT_URL = "https://www.epidemicsound.com/labs/adapt/"

    def __init__(self, page: Page):
        self.page = page

    async def navigate_to_adapt(self) -> bool:
        """Navigate to Labs > Adapt"""
        try:
            logger.info("Navigating to Labs Adapt...")

            await self.page.goto(self.ADAPT_URL, wait_until='load', timeout=30000)
            await asyncio.sleep(3)

            # Verify we're on Adapt page
            adapt_indicators = [
                'text="Adapt length"',
                'text="Adapt music"',
                'text="Select a track"',
                'input[type="search"]',
            ]

            for indicator in adapt_indicators:
                if await self.page.locator(indicator).count() > 0:
                    logger.info("Successfully navigated to Adapt")
                    return True

            logger.warning("Adapt page loaded but indicators not found")
            return True

        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False

    async def search_track(self, track_name: str) -> bool:
        """Search for track by name"""
        try:
            logger.info(f"Searching for: {track_name[:50]}...")

            # Find search input
            search_input = await self.page.wait_for_selector(
                'input[type="search"], input[placeholder*="Search"]',
                timeout=10000
            )

            # Clear and enter track name
            await search_input.fill("")
            await asyncio.sleep(0.5)
            await search_input.fill(track_name)
            await asyncio.sleep(1)
            await search_input.press("Enter")
            await asyncio.sleep(4)

            logger.info("Search executed, waiting for results...")
            return True

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return False

    async def select_first_result(self) -> bool:
        """Select first track from search results"""
        try:
            logger.info("Selecting first result...")

            # Wait for results
            await asyncio.sleep(2)

            # Try various selectors for track results
            result_selectors = [
                'a[href*="/track/"]',
                'button:has-text("Adapt")',
                '[data-testid="track-card"]',
                'article a',
            ]

            for selector in result_selectors:
                elements = await self.page.locator(selector).all()
                if elements and len(elements) > 0:
                    await elements[0].click()
                    await asyncio.sleep(3)
                    logger.info("Track selected")
                    return True

            logger.error("No search results found")
            return False

        except Exception as e:
            logger.error(f"Result selection failed: {e}")
            return False


# ============================================================================
# LENGTH ADAPTATION MODULE
# ============================================================================

class AdaptLength:
    """Adapt track length to 3 minutes with ducking"""

    def __init__(self, page: Page, config: AdaptConfig):
        self.page = page
        self.config = config

    async def adapt_length(self) -> bool:
        """Execute length adaptation"""
        try:
            logger.info("Starting length adaptation...")

            # Click "Adapt length" button
            adapt_length_btn = await self.page.wait_for_selector(
                'button:has-text("Adapt length"), button:has-text("Length")',
                timeout=10000
            )
            await adapt_length_btn.click()
            await asyncio.sleep(2)
            logger.info("Adapt length panel opened")

            # Set duration (3 minutes = 180 seconds)
            duration_input = await self.page.wait_for_selector(
                'input[type="number"], input[placeholder*="duration"]',
                timeout=5000
            )
            await duration_input.fill("")
            await asyncio.sleep(0.5)
            await duration_input.fill(str(self.config.LENGTH_DURATION_SECONDS))
            await asyncio.sleep(1)
            logger.info(f"Duration set to {self.config.LENGTH_DURATION_SECONDS}s (3 minutes)")

            # Enable ducking mix
            if self.config.LENGTH_ENABLE_DUCKING:
                try:
                    ducking_checkbox = await self.page.wait_for_selector(
                        'input[type="checkbox"][name*="duck"], label:has-text("Ducking")',
                        timeout=3000
                    )
                    await ducking_checkbox.click()
                    await asyncio.sleep(0.5)
                    logger.info("Ducking mix enabled")
                except Exception as e:
                    logger.warning(f"Ducking toggle not found (may be enabled by default): {e}")

            # Select steady section
            try:
                steady_option = await self.page.wait_for_selector(
                    'button:has-text("Steady"), label:has-text("Steady")',
                    timeout=3000
                )
                await steady_option.click()
                await asyncio.sleep(0.5)
                logger.info("Steady section selected")
            except Exception as e:
                logger.warning(f"Section type selection not found: {e}")

            # Click Adapt/Process button
            process_btn = await self.page.wait_for_selector(
                'button:has-text("Adapt"), button:has-text("Create"), button:has-text("Generate")',
                timeout=5000
            )
            await process_btn.click()
            logger.info("Length adaptation processing started...")

            # Wait for processing to complete
            success = await self._wait_for_processing()

            if success:
                logger.info("Length adaptation complete!")
                return True
            else:
                logger.error("Length adaptation timeout")
                return False

        except Exception as e:
            logger.error(f"Length adaptation failed: {e}")
            await self.page.screenshot(path="error_adapt_length.png")
            return False

    async def _wait_for_processing(self, timeout_seconds: int = 120) -> bool:
        """Wait for AI processing to complete"""
        logger.info("Waiting for AI processing...")

        start_time = time.time()
        last_log = start_time

        processing_indicators = [
            '[data-state="processing"]',
            '.processing',
            'text="Processing"',
            'text="Generating"',
            '[role="progressbar"]',
        ]

        complete_indicators = [
            'text="Complete"',
            'text="Done"',
            'button:has-text("Download")',
            'button:has-text("Adapt music")',
        ]

        while (time.time() - start_time) < timeout_seconds:
            # Check if still processing
            is_processing = False
            for indicator in processing_indicators:
                if await self.page.locator(indicator).count() > 0:
                    is_processing = True
                    break

            # Check if complete
            is_complete = False
            for indicator in complete_indicators:
                if await self.page.locator(indicator).count() > 0:
                    is_complete = True
                    break

            if is_complete and not is_processing:
                return True

            # Log progress every 10 seconds
            if time.time() - last_log >= 10:
                elapsed = int(time.time() - start_time)
                logger.info(f"  Still processing... ({elapsed}s elapsed)")
                last_log = time.time()

            await asyncio.sleep(2)

        logger.warning(f"Processing timeout after {timeout_seconds}s")
        return False


# ============================================================================
# MUSIC ADAPTATION MODULE
# ============================================================================

class AdaptMusic:
    """Adapt music to be minimal and background-friendly"""

    def __init__(self, page: Page, config: AdaptConfig):
        self.page = page
        self.config = config

    async def adapt_music(self) -> bool:
        """Execute music adaptation"""
        try:
            logger.info("Starting music adaptation...")

            # Click "Adapt music" button
            adapt_music_btn = await self.page.wait_for_selector(
                'button:has-text("Adapt music"), button:has-text("Music")',
                timeout=10000
            )
            await adapt_music_btn.click()
            await asyncio.sleep(2)
            logger.info("Adapt music panel opened")

            # Enter description
            description_input = await self.page.wait_for_selector(
                'textarea, input[type="text"][placeholder*="descri"]',
                timeout=5000
            )
            await description_input.fill(self.config.MUSIC_DESCRIPTION)
            await asyncio.sleep(1)
            logger.info("Description entered")

            # Select "All stems"
            try:
                stems_dropdown = await self.page.wait_for_selector(
                    'select[name*="stem"], button:has-text("stem")',
                    timeout=3000
                )
                await stems_dropdown.click()
                await asyncio.sleep(0.5)

                all_stems_option = await self.page.wait_for_selector(
                    'option:has-text("All"), text="All stems"',
                    timeout=2000
                )
                await all_stems_option.click()
                await asyncio.sleep(0.5)
                logger.info("All stems selected")
            except Exception as e:
                logger.warning(f"Stems selection not found (using default): {e}")

            # Click Adapt/Process button
            process_btn = await self.page.wait_for_selector(
                'button:has-text("Adapt"), button:has-text("Process"), button[type="submit"]',
                timeout=5000
            )
            await process_btn.click()
            logger.info("Music adaptation processing started...")

            # Wait for processing to complete
            success = await self._wait_for_processing()

            if success:
                logger.info("Music adaptation complete!")
                return True
            else:
                logger.error("Music adaptation timeout")
                return False

        except Exception as e:
            logger.error(f"Music adaptation failed: {e}")
            await self.page.screenshot(path="error_adapt_music.png")
            return False

    async def _wait_for_processing(self, timeout_seconds: int = 120) -> bool:
        """Wait for AI processing to complete"""
        logger.info("Waiting for music AI processing...")

        start_time = time.time()
        last_log = start_time

        processing_indicators = [
            '[data-state="processing"]',
            '.processing',
            'text="Processing"',
            'text="Generating"',
            '[role="progressbar"]',
        ]

        complete_indicators = [
            'text="Complete"',
            'text="Done"',
            'button:has-text("Download")',
        ]

        while (time.time() - start_time) < timeout_seconds:
            # Check if still processing
            is_processing = False
            for indicator in processing_indicators:
                if await self.page.locator(indicator).count() > 0:
                    is_processing = True
                    break

            # Check if complete
            is_complete = False
            for indicator in complete_indicators:
                if await self.page.locator(indicator).count() > 0:
                    is_complete = True
                    break

            if is_complete and not is_processing:
                return True

            # Log progress every 10 seconds
            if time.time() - last_log >= 10:
                elapsed = int(time.time() - start_time)
                logger.info(f"  Still processing... ({elapsed}s elapsed)")
                last_log = time.time()

            await asyncio.sleep(2)

        logger.warning(f"Music processing timeout after {timeout_seconds}s")
        return False


# ============================================================================
# DOWNLOAD MODULE
# ============================================================================

class AdaptDownload:
    """Download adapted track as WAV"""

    def __init__(self, page: Page, config: AdaptConfig):
        self.page = page
        self.config = config

    async def download_wav(self, track_name: str, track_index: int) -> Optional[Path]:
        """Download adapted track as WAV"""
        try:
            logger.info("Starting WAV download...")

            # Ensure output directory exists
            self.config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            # Find download button
            download_btn_selectors = [
                'button:has-text("Download")',
                'a:has-text("Download")',
                '[aria-label*="Download"]',
                '[data-action="download"]',
            ]

            download_btn = None
            for selector in download_btn_selectors:
                elements = await self.page.locator(selector).all()
                if elements and len(elements) > 0:
                    download_btn = elements[0]
                    break

            if not download_btn:
                raise Exception("Download button not found")

            await download_btn.click()
            await asyncio.sleep(2)
            logger.info("Download dialog opened")

            # Select WAV format
            try:
                wav_option = await self.page.wait_for_selector(
                    'button:has-text("WAV"), text="WAV", option[value*="wav"]',
                    timeout=3000
                )
                await wav_option.click()
                await asyncio.sleep(1)
                logger.info("WAV format selected")
            except Exception as e:
                logger.warning(f"WAV format selection not found (may be default): {e}")

            # Setup download handler
            async with self.page.expect_download(timeout=120000) as download_info:
                # Click final download button
                final_download_btn = await self.page.wait_for_selector(
                    'button:has-text("Download")',
                    timeout=5000
                )
                await final_download_btn.click()
                logger.info("Download initiated...")

            download = await download_info.value

            # Generate filename
            safe_name = "".join(c for c in track_name if c.isalnum() or c in (' ', '-', '_'))[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"adapt_{track_index:03d}_{safe_name}_{timestamp}.wav"
            save_path = self.config.OUTPUT_DIR / filename

            # Save file
            await download.save_as(save_path)

            file_size = save_path.stat().st_size / (1024 * 1024)
            logger.info(f"Download complete: {filename} ({file_size:.1f} MB)")

            return save_path

        except Exception as e:
            logger.error(f"Download failed: {e}")
            await self.page.screenshot(path="error_download.png")
            return None


# ============================================================================
# ORCHESTRATOR
# ============================================================================

class LabsAdaptOrchestrator:
    """Master orchestrator that combines all modules"""

    def __init__(
        self,
        track_names: List[str],
        headless: bool = False,
        resume: bool = False,
    ):
        self.track_names = track_names
        self.headless = headless
        self.resume = resume

        self.config = AdaptConfig()
        self.checkpoint_file = Path("labs_adapt_checkpoint.json")

        # State
        self.tasks: List[TrackTask] = []
        self.progress: Optional[ProgressStats] = None

        # Initialize tasks
        self._initialize_tasks()

        # Load checkpoint if resuming
        if self.resume:
            self._load_checkpoint()

    def _initialize_tasks(self):
        """Initialize task list"""
        if self.tasks:
            return  # Already initialized (from checkpoint)

        for idx, track_name in enumerate(self.track_names):
            task = TrackTask(
                track_name=track_name,
                track_index=idx,
            )
            self.tasks.append(task)

        logger.info(f"Initialized {len(self.tasks)} tasks")

    def _save_checkpoint(self):
        """Save progress to checkpoint file"""
        try:
            checkpoint = {
                'timestamp': datetime.now().isoformat(),
                'tasks': [asdict(task) for task in self.tasks],
                'progress': asdict(self.progress) if self.progress else None,
            }

            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint, f, indent=2)

            logger.debug("Checkpoint saved")
        except Exception as e:
            logger.warning(f"Failed to save checkpoint: {e}")

    def _load_checkpoint(self):
        """Load progress from checkpoint file"""
        if not self.checkpoint_file.exists():
            logger.info("No checkpoint file found")
            return

        try:
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)

            self.tasks = [TrackTask(**task) for task in checkpoint.get('tasks', [])]

            completed = sum(1 for t in self.tasks if t.status == 'completed')
            failed = sum(1 for t in self.tasks if t.status == 'failed')

            logger.info(f"Loaded checkpoint: {completed} completed, {failed} failed")
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}")

    def _print_progress(self):
        """Print progress bar and stats"""
        if not self.progress:
            return

        pct = (self.progress.completed / self.progress.total_tracks) * 100
        elapsed = time.time() - self.progress.start_time

        # Calculate ETA
        if self.progress.completed > 0:
            avg_time = elapsed / self.progress.completed
            remaining = self.progress.total_tracks - self.progress.completed
            eta_seconds = avg_time * remaining
            eta = str(timedelta(seconds=int(eta_seconds)))
        else:
            eta = "calculating..."

        print()
        print("=" * 80)
        print(f"PROGRESS: {self.progress.completed}/{self.progress.total_tracks} ({pct:.1f}%) | Failed: {self.progress.failed}")
        print(f"Current: {self.progress.current_track}")
        print(f"Status: {self.progress.current_status}")
        print(f"Elapsed: {str(timedelta(seconds=int(elapsed)))} | ETA: {eta}")
        print("=" * 80)

    async def run(self):
        """Main orchestration loop"""
        try:
            print()
            print("=" * 80)
            print("EPIDEMIC SOUND LABS ADAPT - COMPLETE AUTOMATION")
            print("=" * 80)
            print(f"Total tracks: {len(self.track_names)}")
            print(f"Duration: 3 minutes per track")
            print(f"Format: WAV")
            print(f"Output: {self.config.OUTPUT_DIR}")
            print()
            print("Workflow per track:")
            print("  1. Navigate to Labs Adapt")
            print("  2. Search and select track")
            print("  3. Adapt Length (3 min, ducking, steady)")
            print("  4. Adapt Music (minimal, background-friendly)")
            print("  5. Download WAV")
            print()
            print(f"Expected time: {len(self.track_names) * 6} minutes")
            print("=" * 80)
            print()

            # Initialize progress
            self.progress = ProgressStats(
                total_tracks=len(self.tasks),
                completed=sum(1 for t in self.tasks if t.status == 'completed'),
                failed=sum(1 for t in self.tasks if t.status == 'failed'),
                start_time=time.time(),
            )

            # Start browser session
            async with SessionManager(headless=self.headless) as session:
                page = await session.get_page()

                # Initialize modules
                navigation = AdaptNavigation(page)
                adapt_length = AdaptLength(page, self.config)
                adapt_music = AdaptMusic(page, self.config)
                adapt_download = AdaptDownload(page, self.config)

                # Process each track
                for task in self.tasks:
                    # Skip if already completed
                    if task.status == 'completed':
                        logger.info(f"Skipping {task.track_name} (already completed)")
                        continue

                    # Update progress
                    self.progress.current_track = task.track_name
                    self.progress.current_status = "Starting..."
                    self._print_progress()

                    # Process track
                    success = await self._process_track(
                        task, navigation, adapt_length, adapt_music, adapt_download
                    )

                    if success:
                        task.status = 'completed'
                        self.progress.completed += 1
                        logger.info(f"SUCCESS: {task.track_name}")
                    else:
                        task.status = 'failed'
                        self.progress.failed += 1
                        logger.error(f"FAILED: {task.track_name}")

                    # Save checkpoint after each track
                    self._save_checkpoint()

                    # Small delay before next track
                    if task != self.tasks[-1]:
                        await asyncio.sleep(3)

                # Final summary
                self._print_final_summary()

        except KeyboardInterrupt:
            logger.info("\nInterrupted by user")
            self._save_checkpoint()
            logger.info("Progress saved to checkpoint")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            self._save_checkpoint()

    async def _process_track(
        self,
        task: TrackTask,
        navigation: AdaptNavigation,
        adapt_length: AdaptLength,
        adapt_music: AdaptMusic,
        adapt_download: AdaptDownload,
    ) -> bool:
        """Process a single track with retry logic"""

        max_attempts = self.config.MAX_RETRY_ATTEMPTS + 1

        while task.attempts < max_attempts:
            task.attempts += 1
            task.start_time = time.time()

            try:
                logger.info(f"\nProcessing ({task.attempts}/{max_attempts}): {task.track_name}")

                # STEP 1: Navigate to Adapt
                self.progress.current_status = "Navigating to Labs Adapt..."
                self._print_progress()

                if not await navigation.navigate_to_adapt():
                    raise Exception("Failed to navigate to Adapt")

                # STEP 2: Search for track
                self.progress.current_status = "Searching for track..."
                self._print_progress()

                if not await navigation.search_track(task.track_name):
                    raise Exception("Failed to search for track")

                if not await navigation.select_first_result():
                    raise Exception("Failed to select track from results")

                # STEP 3: Adapt Length
                self.progress.current_status = "Adapting length (3 min)..."
                self._print_progress()

                if not await adapt_length.adapt_length():
                    raise Exception("Length adaptation failed")

                # STEP 4: Adapt Music
                self.progress.current_status = "Adapting music (minimal)..."
                self._print_progress()

                if not await adapt_music.adapt_music():
                    raise Exception("Music adaptation failed")

                # STEP 5: Download WAV
                self.progress.current_status = "Downloading WAV..."
                self._print_progress()

                download_path = await adapt_download.download_wav(
                    task.track_name, task.track_index
                )

                if not download_path:
                    raise Exception("Download failed")

                task.download_path = str(download_path)
                task.end_time = time.time()

                duration = task.end_time - task.start_time
                logger.info(f"Track completed in {int(duration)}s")

                return True

            except Exception as e:
                task.error = str(e)
                logger.warning(f"Attempt {task.attempts} failed: {e}")

                if task.attempts < max_attempts:
                    logger.info(f"Retrying in {self.config.RETRY_DELAY_SECONDS}s...")
                    await asyncio.sleep(self.config.RETRY_DELAY_SECONDS)

        logger.error(f"Track failed after {max_attempts} attempts")
        return False

    def _print_final_summary(self):
        """Print final summary"""
        if not self.progress:
            return

        total_time = time.time() - self.progress.start_time

        print()
        print("=" * 80)
        print("DOWNLOAD COMPLETE!")
        print("=" * 80)
        print(f"Total tracks: {self.progress.total_tracks}")
        print(f"Completed: {self.progress.completed}")
        print(f"Failed: {self.progress.failed}")
        print(f"Total time: {str(timedelta(seconds=int(total_time)))}")
        print(f"Output directory: {self.config.OUTPUT_DIR.absolute()}")
        print()

        if self.progress.completed > 0:
            print("Downloaded files:")
            for task in self.tasks:
                if task.status == 'completed' and task.download_path:
                    print(f"  {Path(task.download_path).name}")

        print("=" * 80)


# ============================================================================
# CLI
# ============================================================================

async def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Epidemic Sound Labs Adapt - Complete Automation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download specific tracks
  python labs_adapt_complete.py --tracks "Neon Dreams" "Electric Pulse" "Digital Wave"

  # Download first 5 from Electronic genre (requires additional implementation)
  python labs_adapt_complete.py --count 5

  # Resume from checkpoint
  python labs_adapt_complete.py --resume

  # Run in headless mode
  python labs_adapt_complete.py --headless --tracks "Track 1" "Track 2"

Requirements:
  - Valid epidemic_session.json file (run epidemic_browser_login.py first)
  - Playwright installed (pip install playwright && playwright install chromium)

Expected Runtime:
  5-8 minutes per track
        """
    )

    # Track selection
    track_group = parser.add_mutually_exclusive_group(required=True)
    track_group.add_argument(
        '--tracks',
        nargs='+',
        help='List of track names to download'
    )
    track_group.add_argument(
        '--count',
        type=int,
        help='Download first N tracks from Electronic genre'
    )
    track_group.add_argument(
        '--resume',
        action='store_true',
        help='Resume from last checkpoint'
    )

    # Options
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run in headless mode (no GUI)'
    )

    args = parser.parse_args()

    # Get track names
    track_names = []

    if args.tracks:
        track_names = args.tracks
    elif args.count:
        # TODO: Implement genre browsing to get first N tracks
        logger.error("--count not yet implemented. Use --tracks instead.")
        sys.exit(1)
    elif args.resume:
        # Track names will be loaded from checkpoint
        pass

    # Create orchestrator
    orchestrator = LabsAdaptOrchestrator(
        track_names=track_names,
        headless=args.headless,
        resume=args.resume,
    )

    # Run
    await orchestrator.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
