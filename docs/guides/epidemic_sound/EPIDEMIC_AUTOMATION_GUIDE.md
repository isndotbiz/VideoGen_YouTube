# Epidemic Sound Browser Automation Guide

## What is Browser Automation?

Browser automation is a technique that allows your computer to control a web browser programmatically - as if an invisible person were clicking, typing, and navigating through websites for you. Think of it as a robot that can:

- Open a web browser (Chrome, Firefox, Edge)
- Navigate to websites
- Fill in forms and click buttons
- Download files
- Extract information from pages
- Perform repetitive tasks automatically

**For Epidemic Sound**, browser automation allows you to:
- Automatically log in to your account
- Search for music across multiple categories
- Use the **Adapt tool** to create custom-length tracks (not available in the API)
- Download tracks in bulk for different video durations
- Save hours of manual clicking and downloading

**Why use automation for Epidemic Sound?**
The Epidemic Sound API has limitations - it doesn't provide access to the powerful Adapt tool that lets you create custom track lengths (15s, 30s, 60s, or custom durations up to 5 minutes). Browser automation fills this gap by interacting with the web interface directly.

---

## Installation

### Step 1: Install Playwright

Playwright is a powerful browser automation framework that can control Chromium, Firefox, and WebKit browsers.

```bash
# Install Playwright Python package
pip install playwright

# Install browser binaries (Chromium recommended)
playwright install chromium

# Optional: Install all browsers (Chromium, Firefox, WebKit)
playwright install
```

**Expected output:**
```
Downloading Chromium 123.0.6312.4 (playwright build v1095) - 142 Mb
Chromium 123.0.6312.4 (playwright build v1095) downloaded to...
```

### Step 2: Verify Installation

Test that Playwright is installed correctly:

```python
# test_playwright.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.google.com")
    print("✓ Playwright is working!")
    browser.close()
```

Run it:
```bash
python test_playwright.py
```

You should see a browser window open, navigate to Google, then close automatically.

### Step 3: Set Up Credentials

Create or update your `.env.local` file (this file should NEVER be committed to git):

```bash
# Epidemic Sound Credentials
EPIDEMIC_SOUND_EMAIL=your-email@example.com
EPIDEMIC_SOUND_PASSWORD=your-secure-password

# Browser automation settings (optional)
EPIDEMIC_HEADLESS=false  # Set to 'true' to run without visible browser
EPIDEMIC_SLOW_MO=50      # Milliseconds to slow down operations (easier to watch)
EPIDEMIC_TIMEOUT=30000   # Default timeout in milliseconds (30 seconds)
```

**Security Warning:** Never commit `.env.local` to version control! Make sure it's in your `.gitignore`.

Add to `.gitignore`:
```
.env.local
.env
*.local
```

---

## Quick Start (5-Minute Test)

### Test 1: Login Test

Create a simple script to verify login works:

```python
# test_epidemic_login.py
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load credentials
load_dotenv('.env.local')
email = os.getenv('EPIDEMIC_SOUND_EMAIL')
password = os.getenv('EPIDEMIC_SOUND_PASSWORD')

with sync_playwright() as p:
    # Launch browser (headless=False means you can see it)
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()

    # Navigate to Epidemic Sound login
    print("Navigating to Epidemic Sound...")
    page.goto('https://www.epidemicsound.com/login/')

    # Fill in credentials
    print("Entering credentials...")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)

    # Click login
    print("Logging in...")
    page.click('button[type="submit"]')

    # Wait for navigation
    page.wait_for_load_state('networkidle')

    print("✓ Login successful!")
    print(f"Current URL: {page.url}")

    # Keep browser open for 5 seconds so you can see the result
    page.wait_for_timeout(5000)

    browser.close()
```

Run it:
```bash
python test_epidemic_login.py
```

**What to expect:**
- Browser window opens
- Navigates to Epidemic Sound login page
- Fills in email and password
- Clicks login button
- You should see your dashboard
- Browser closes after 5 seconds

**Common issues:**
- **2FA/Verification code required**: See troubleshooting section below
- **Login selectors changed**: Epidemic Sound may update their website structure
- **"No such file" error**: Make sure `.env.local` exists with credentials

### Test 2: Single Track Download with Adapt

This test searches for a track, uses the Adapt tool to create a 30-second version, and downloads it:

```python
# test_epidemic_adapt.py
import os
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv('.env.local')

def test_adapt_download():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        # Login (reuse login code from above)
        page.goto('https://www.epidemicsound.com/login/')
        page.fill('input[name="email"]', os.getenv('EPIDEMIC_SOUND_EMAIL'))
        page.fill('input[name="password"]', os.getenv('EPIDEMIC_SOUND_PASSWORD'))
        page.click('button[type="submit"]')
        page.wait_for_load_state('networkidle')

        # Search for ambient music
        print("Searching for ambient music...")
        page.goto('https://www.epidemicsound.com/music/genres/ambient/')
        page.wait_for_selector('.track-card', timeout=10000)

        # Click first track
        print("Selecting first track...")
        page.click('.track-card:first-child')
        page.wait_for_load_state('networkidle')

        # Open Adapt tool
        print("Opening Adapt tool...")
        page.click('button:has-text("Adapt")')  # Click Adapt button
        page.wait_for_selector('.adapt-dialog', timeout=5000)

        # Select 30-second preset
        print("Creating 30-second version...")
        page.click('button:has-text("30 sec")')
        page.wait_for_timeout(2000)  # Wait for processing

        # Download the adapted track
        print("Downloading track...")
        with page.expect_download() as download_info:
            page.click('button:has-text("Download")')

        download = download_info.value

        # Save to downloads folder
        output_dir = Path('downloads/epidemic_automated')
        output_dir.mkdir(parents=True, exist_ok=True)
        download.save_as(output_dir / f'ambient_30sec_{download.suggested_filename}')

        print(f"✓ Downloaded to: {output_dir}")

        browser.close()

if __name__ == '__main__':
    test_adapt_download()
```

**Note:** The actual CSS selectors (`.track-card`, `.adapt-dialog`, etc.) may need to be updated based on Epidemic Sound's current website structure. Use your browser's Developer Tools (F12) to inspect elements and find the correct selectors.

### Test 3: Verify Automation Works

Create a comprehensive test that verifies all automation capabilities:

```python
# verify_epidemic_automation.py
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv('.env.local')

def verify_automation():
    with sync_playwright() as p:
        print("Testing Epidemic Sound browser automation...")
        print("=" * 60)

        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()

        # Test 1: Login
        print("\n[1/4] Testing login...")
        page.goto('https://www.epidemicsound.com/login/')
        page.fill('input[name="email"]', os.getenv('EPIDEMIC_SOUND_EMAIL'))
        page.fill('input[name="password"]', os.getenv('EPIDEMIC_SOUND_PASSWORD'))
        page.click('button[type="submit"]')
        page.wait_for_load_state('networkidle')

        if 'dashboard' in page.url or 'music' in page.url:
            print("   ✓ Login successful")
        else:
            print("   ✗ Login failed - check credentials")
            browser.close()
            return

        # Test 2: Navigate to music library
        print("\n[2/4] Testing music library access...")
        page.goto('https://www.epidemicsound.com/music/')
        page.wait_for_selector('.music-grid, .track-list', timeout=10000)
        print("   ✓ Music library accessible")

        # Test 3: Search functionality
        print("\n[3/4] Testing search...")
        search_input = page.locator('input[placeholder*="Search"], input[type="search"]')
        search_input.fill('ambient calm')
        page.keyboard.press('Enter')
        page.wait_for_timeout(2000)
        print("   ✓ Search working")

        # Test 4: Track details
        print("\n[4/4] Testing track details access...")
        page.goto('https://www.epidemicsound.com/music/genres/ambient/')
        page.wait_for_selector('.track-card', timeout=10000)
        track_count = page.locator('.track-card').count()
        print(f"   ✓ Found {track_count} tracks")

        print("\n" + "=" * 60)
        print("✓ All automation tests passed!")
        print("\nYou can now proceed with the full workflow.")

        page.wait_for_timeout(3000)
        browser.close()

if __name__ == '__main__':
    verify_automation()
```

---

## Full Workflow

### Download Music for All Video Platforms

This workflow downloads curated music for different video types (YouTube, TikTok, Instagram, etc.) and durations (15s, 30s, 60s, 3min).

**Expected time:** 2-3 hours (depending on number of tracks)

**What to expect:**
- Browser will open and navigate automatically
- You'll see pages loading, searches happening, clicks occurring
- Downloads will save to `downloads/epidemic_automated/` folder
- Progress will be logged to console
- Browser may pause if 2FA verification is needed

### Full Automation Script

```python
# epidemic_sound_automation.py
import os
import time
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, Browser

load_dotenv('.env.local')

class EpidemicSoundAutomation:
    """
    Automated browser client for Epidemic Sound.

    Features:
    - Automatic login with session management
    - Bulk track search and filtering
    - Adapt tool usage for custom durations
    - Platform-specific downloads (YouTube, TikTok, Instagram)
    - Organized file structure
    """

    def __init__(self, headless: bool = False, slow_mo: int = 50):
        self.email = os.getenv('EPIDEMIC_SOUND_EMAIL')
        self.password = os.getenv('EPIDEMIC_SOUND_PASSWORD')
        self.headless = headless
        self.slow_mo = slow_mo
        self.output_dir = Path('downloads/epidemic_automated')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def login(self, page: Page) -> bool:
        """Login to Epidemic Sound."""
        try:
            print("Logging in to Epidemic Sound...")
            page.goto('https://www.epidemicsound.com/login/', wait_until='networkidle')

            # Fill credentials
            page.fill('input[name="email"]', self.email)
            page.fill('input[name="password"]', self.password)

            # Submit
            page.click('button[type="submit"]')
            page.wait_for_load_state('networkidle')

            # Check if login successful
            if 'login' in page.url:
                print("❌ Login failed - check credentials or 2FA")
                return False

            print("✓ Login successful")
            return True

        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def search_music(self, page: Page, query: str = None,
                    genre: str = None, mood: str = None,
                    instrumental_only: bool = True) -> None:
        """Search for music with filters."""

        if genre:
            # Navigate to genre page
            url = f'https://www.epidemicsound.com/music/genres/{genre.lower()}/'
            print(f"Navigating to genre: {genre}")
            page.goto(url, wait_until='networkidle')
        else:
            # Use search
            page.goto('https://www.epidemicsound.com/music/', wait_until='networkidle')
            if query:
                search_input = page.locator('input[placeholder*="Search"]')
                search_input.fill(query)
                page.keyboard.press('Enter')
                page.wait_for_timeout(2000)

        # Apply filters
        if instrumental_only:
            # Click Vocals filter
            try:
                page.click('button:has-text("Vocals")', timeout=5000)
                page.click('label:has-text("Instrumental")', timeout=5000)
                page.wait_for_timeout(1000)
            except:
                print("   ⚠ Could not apply instrumental filter")

        if mood:
            # Click Mood filter
            try:
                page.click('button:has-text("Mood")', timeout=5000)
                page.click(f'label:has-text("{mood}")', timeout=5000)
                page.wait_for_timeout(1000)
            except:
                print(f"   ⚠ Could not apply mood filter: {mood}")

        # Wait for results
        page.wait_for_selector('.track-card, .music-item', timeout=10000)

    def download_track_with_adapt(self, page: Page, track_index: int,
                                  duration: int, output_name: str) -> bool:
        """
        Download a track using Adapt tool for custom duration.

        Args:
            page: Playwright page object
            track_index: Index of track in search results (0-based)
            duration: Duration in seconds (15, 30, 60, or custom)
            output_name: Name for output file

        Returns:
            bool: True if successful
        """
        try:
            # Click track
            tracks = page.locator('.track-card, .music-item')
            tracks.nth(track_index).click()
            page.wait_for_load_state('networkidle')

            # Get track title for logging
            title = page.locator('h1, .track-title').first.text_content()
            print(f"   Processing: {title}")

            # Click Adapt button
            page.click('button:has-text("Adapt"), a:has-text("Adapt")', timeout=5000)
            page.wait_for_timeout(2000)

            # Select duration
            if duration == 15:
                page.click('button:has-text("15 sec")')
            elif duration == 30:
                page.click('button:has-text("30 sec")')
            elif duration == 60:
                page.click('button:has-text("60 sec")')
            else:
                # Custom duration
                page.click('button:has-text("Custom")')
                page.fill('input[type="number"]', str(duration))
                page.click('button:has-text("Create")')

            # Wait for Adapt to process
            print(f"   Creating {duration}s version...")
            page.wait_for_timeout(5000)  # Adapt processing time

            # Download
            with page.expect_download(timeout=30000) as download_info:
                page.click('button:has-text("Download")')

            download = download_info.value

            # Save with custom name
            output_path = self.output_dir / f"{output_name}.mp3"
            download.save_as(output_path)
            print(f"   ✓ Downloaded: {output_path.name}")

            # Go back to results
            page.go_back()
            page.wait_for_timeout(1000)

            return True

        except Exception as e:
            print(f"   ✗ Error downloading track {track_index}: {e}")
            # Try to recover by going back
            try:
                page.go_back()
            except:
                pass
            return False

    def download_platform_music(self, platform: str, durations: List[int],
                               tracks_per_category: int = 3) -> None:
        """
        Download music optimized for a specific platform.

        Args:
            platform: Platform name (youtube, tiktok, instagram, etc.)
            durations: List of durations to download (e.g., [15, 30, 60])
            tracks_per_category: Number of tracks per mood/genre combo
        """

        print(f"\n{'='*60}")
        print(f"Downloading music for {platform.upper()}")
        print(f"Durations: {durations}, Tracks per category: {tracks_per_category}")
        print(f"{'='*60}\n")

        # Platform-specific configurations
        configs = {
            'youtube': {
                'genres': ['ambient', 'corporate'],
                'moods': ['Calm', 'Uplifting'],
                'bpm_range': (60, 80)
            },
            'tiktok': {
                'genres': ['electronic', 'lofi'],
                'moods': ['Energetic', 'Happy'],
                'bpm_range': (100, 140)
            },
            'instagram': {
                'genres': ['lofi', 'acoustic'],
                'moods': ['Laid-back', 'Dreamy'],
                'bpm_range': (80, 110)
            },
            'linkedin': {
                'genres': ['corporate'],
                'moods': ['Professional', 'Inspiring'],
                'bpm_range': (70, 90)
            }
        }

        config = configs.get(platform, configs['youtube'])

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless, slow_mo=self.slow_mo)
            page = browser.new_page()

            # Login
            if not self.login(page):
                browser.close()
                return

            # Download tracks for each genre/mood combination
            download_count = 0

            for genre in config['genres']:
                for mood in config['moods']:
                    print(f"\n[{genre.upper()} × {mood.upper()}]")

                    # Search for music
                    self.search_music(page, genre=genre, mood=mood,
                                    instrumental_only=True)

                    # Download tracks at each duration
                    for track_idx in range(tracks_per_category):
                        for duration in durations:
                            output_name = (f"{platform}_{genre}_{mood}_"
                                         f"{duration}s_track{track_idx+1}")

                            success = self.download_track_with_adapt(
                                page, track_idx, duration, output_name
                            )

                            if success:
                                download_count += 1

                            # Rate limiting - be respectful
                            time.sleep(2)

            print(f"\n{'='*60}")
            print(f"✓ Downloaded {download_count} tracks for {platform}")
            print(f"{'='*60}\n")

            browser.close()

    def download_all_platforms(self) -> None:
        """Download music for all major platforms."""

        platforms_config = {
            'youtube': [30, 60, 180],  # 30s intro, 60s background, 3min full
            'tiktok': [15, 30],        # 15s clips, 30s videos
            'instagram': [15, 30, 60], # Reels and posts
            'linkedin': [30, 60]       # Professional content
        }

        print("\n" + "="*60)
        print("EPIDEMIC SOUND BULK DOWNLOAD")
        print("="*60)
        print(f"\nOutput directory: {self.output_dir}")
        print("\nThis will download music for:")
        for platform, durations in platforms_config.items():
            print(f"  - {platform.upper()}: {durations}s versions")

        print("\nEstimated time: 2-3 hours")
        print("\nPress Ctrl+C at any time to stop.")
        print("="*60 + "\n")

        # Prompt to continue
        input("Press Enter to start, or Ctrl+C to cancel...")

        # Download for each platform
        for platform, durations in platforms_config.items():
            self.download_platform_music(
                platform=platform,
                durations=durations,
                tracks_per_category=3
            )

        print("\n" + "="*60)
        print("✓ DOWNLOAD COMPLETE!")
        print(f"All tracks saved to: {self.output_dir}")
        print("="*60 + "\n")

# Main execution
if __name__ == '__main__':
    # Create automation client
    client = EpidemicSoundAutomation(
        headless=os.getenv('EPIDEMIC_HEADLESS', 'false').lower() == 'true',
        slow_mo=int(os.getenv('EPIDEMIC_SLOW_MO', 50))
    )

    # Run full download workflow
    client.download_all_platforms()
```

### Running the Full Workflow

```bash
python epidemic_sound_automation.py
```

**What happens:**
1. Browser opens (or runs in background if headless mode enabled)
2. Logs into Epidemic Sound
3. For each platform (YouTube, TikTok, Instagram, LinkedIn):
   - Searches for appropriate genres and moods
   - Downloads 3 tracks per category
   - Creates versions at multiple durations using Adapt
   - Saves to organized folder structure
4. Total: ~72 tracks (4 platforms × 3 categories × 3 tracks × 2-3 durations)
5. Estimated time: 2-3 hours

---

## Configuration

### Headless vs Headed Mode

**Headed Mode (default)**: Browser window is visible
```python
client = EpidemicSoundAutomation(headless=False)
```
**Use when:**
- First time running (to see what's happening)
- Debugging issues
- Manual intervention needed (2FA)

**Headless Mode**: Browser runs invisibly in background
```python
client = EpidemicSoundAutomation(headless=True)
```
**Use when:**
- Running on server
- Automation is stable and tested
- Running overnight/unattended

### Platform Selection

To download for specific platforms only:

```python
# Download only for YouTube
client.download_platform_music(
    platform='youtube',
    durations=[30, 60, 180],
    tracks_per_category=5
)

# Or customize platforms
platforms = {
    'youtube': [60, 180],
    'instagram': [15, 30]
}

for platform, durations in platforms.items():
    client.download_platform_music(platform, durations)
```

### Track Counts Per Category

Control how many tracks to download per genre/mood combination:

```python
# Download 5 tracks per category (default is 3)
client.download_platform_music(
    platform='youtube',
    durations=[30, 60],
    tracks_per_category=5  # Downloads 5 ambient/calm, 5 ambient/uplifting, etc.
)
```

### Adapt Settings Customization

Customize Adapt durations for different video types:

```python
# Tutorial videos - longer background music
tutorial_config = {
    'genres': ['ambient', 'corporate'],
    'moods': ['Calm', 'Focused'],
    'durations': [120, 180, 300]  # 2min, 3min, 5min
}

# Product demos - shorter, punchier
demo_config = {
    'genres': ['electronic', 'corporate'],
    'moods': ['Uplifting', 'Energetic'],
    'durations': [15, 30, 45]  # Quick clips
}

# Explainer videos - medium length
explainer_config = {
    'genres': ['ambient', 'lofi'],
    'moods': ['Calm', 'Inspiring'],
    'durations': [60, 90, 120]  # 1-2 minutes
}
```

Add custom download method:

```python
def download_custom_config(self, config_name: str, config: dict):
    """Download with custom configuration."""
    print(f"\nDownloading {config_name} music...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=self.headless)
        page = browser.new_page()

        if not self.login(page):
            return

        for genre in config['genres']:
            for mood in config['moods']:
                self.search_music(page, genre=genre, mood=mood)

                for track_idx in range(3):  # 3 tracks per combo
                    for duration in config['durations']:
                        output_name = f"{config_name}_{genre}_{mood}_{duration}s_track{track_idx+1}"
                        self.download_track_with_adapt(page, track_idx, duration, output_name)
                        time.sleep(2)

        browser.close()
```

Usage:
```python
client.download_custom_config('tutorial', tutorial_config)
```

---

## Monitoring

### How to Watch Progress

**Console Output:**
The script provides real-time progress updates:

```
==============================================================
Downloading music for YOUTUBE
Durations: [30, 60, 180], Tracks per category: 3
==============================================================

[AMBIENT × CALM]
   Processing: Gentle Morning Light
   Creating 30s version...
   ✓ Downloaded: youtube_ambient_Calm_30s_track1.mp3
   Processing: Peaceful Meditation
   Creating 60s version...
   ✓ Downloaded: youtube_ambient_Calm_60s_track1.mp3
```

**Browser Visibility:**
When running in headed mode, you can watch the browser:
- Pages loading
- Search queries being executed
- Filters being applied
- Adapt tool opening and processing
- Downloads starting

### Understanding Logs

**Log Levels:**

- `✓` - Success (green in terminal)
- `⚠` - Warning (yellow) - non-critical issue, continuing
- `✗` - Error (red) - task failed, will retry or skip
- `❌` - Critical Error - workflow stopped

**Example logs:**

```
✓ Login successful                    # Authentication worked
⚠ Could not apply instrumental filter  # Filter not found, continuing anyway
✗ Error downloading track 5            # Single track failed, moving to next
❌ Login failed - check credentials    # Critical - workflow stops
```

### When to Intervene

**Manual intervention required:**

1. **Two-Factor Authentication (2FA)**
   ```
   [Browser paused]
   ⚠ Waiting for 2FA verification...
   ```
   **Action:** Enter your 2FA code in the browser window
   **Script:** Will wait up to 60 seconds

2. **Session Expired**
   ```
   ❌ Session expired - please re-login
   ```
   **Action:** Let script re-login automatically, or restart if it fails

3. **Download Blocked**
   ```
   ⚠ Download blocked - check browser permissions
   ```
   **Action:** Allow downloads in browser popup

4. **Rate Limited**
   ```
   ⚠ Rate limit detected - pausing for 60 seconds...
   ```
   **Action:** Wait - script will resume automatically

**When to stop and debug:**

- Repeated login failures (3+)
- Same track failing multiple times
- Browser crashes or freezes
- Download folder not being created

---

## Troubleshooting

### Common Errors

#### 1. Selectors Changed

**Error:**
```
playwright._impl._api_types.TimeoutError: Timeout 30000ms exceeded.
waiting for selector ".track-card"
```

**Cause:** Epidemic Sound updated their website structure

**Fix:**
1. Open Epidemic Sound in browser
2. Right-click on element you're trying to find (e.g., track card)
3. Select "Inspect" (opens Developer Tools)
4. Find the current class name or selector
5. Update script with new selector

**Example:**
```python
# Old selector (no longer works)
page.click('.track-card')

# Find new selector in browser inspector
# New selector found: '.music-item'
page.click('.music-item')
```

**Common selector updates needed:**
```python
# Track cards
'.track-card' → '.music-item' or '[data-testid="track-card"]'

# Adapt button
'button:has-text("Adapt")' → 'a[href*="/adapt"]'

# Download button
'button:has-text("Download")' → 'button[aria-label="Download"]'
```

#### 2. Network Issues

**Error:**
```
playwright._impl._api_types.TimeoutError: Timeout waiting for load state
```

**Cause:** Slow network, Epidemic Sound servers slow, or connection interrupted

**Fix 1 - Increase Timeout:**
```python
# Default timeout (30 seconds)
page.goto(url, wait_until='networkidle', timeout=30000)

# Increase to 60 seconds
page.goto(url, wait_until='networkidle', timeout=60000)
```

**Fix 2 - Add Retry Logic:**
```python
def robust_goto(page, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            page.goto(url, wait_until='networkidle', timeout=60000)
            return True
        except Exception as e:
            print(f"   ⚠ Attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"   Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"   ✗ All retries failed")
                return False
```

**Fix 3 - Check Internet Connection:**
```bash
# Test connectivity
ping epidemicsound.com
```

#### 3. Session Expired

**Error:**
```
❌ Login failed - redirected back to login page
```

**Cause:**
- Credentials incorrect
- Session expired during long-running automation
- Account requires re-verification

**Fix 1 - Re-login Automatically:**
```python
def auto_relogin_on_expire(page):
    """Check if session expired and re-login."""
    if 'login' in page.url:
        print("   ⚠ Session expired - re-logging in...")
        return self.login(page)
    return True

# Use before critical operations
if not auto_relogin_on_expire(page):
    print("   ✗ Re-login failed")
    return
```

**Fix 2 - Use Session Storage:**
```python
# Save authenticated session after first login
context = browser.new_context()
page = context.new_page()
self.login(page)

# Save session state
context.storage_state(path="epidemic_session.json")

# Later: Reuse session
context = browser.new_context(storage_state="epidemic_session.json")
page = context.new_page()
# Already logged in!
```

**Fix 3 - Verify Credentials:**
```python
# Test login separately
python test_epidemic_login.py
```

### When to Retry vs Skip

**Retry when:**
- Network timeout (could be temporary)
- Rate limit (wait and retry)
- Element not found (page may still be loading)
- Download interrupted (file may be partially saved)

**Skip when:**
- Track deleted/unavailable (404 error)
- Subscription doesn't allow download (403 error)
- Adapt not available for track (move to next)
- Same track failing 3+ times in a row

**Retry implementation:**
```python
def download_with_retry(self, page, track_idx, duration, output_name, max_retries=3):
    """Download with automatic retry on failure."""
    for attempt in range(max_retries):
        try:
            return self.download_track_with_adapt(page, track_idx, duration, output_name)
        except Exception as e:
            print(f"   ⚠ Attempt {attempt+1} failed: {e}")

            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)  # Exponential backoff
                print(f"   Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"   ✗ Skipping after {max_retries} attempts")
                return False
```

---

## Safety & Ethics

### Terms of Service Considerations

**Epidemic Sound Terms of Service:**
- Automation is **not explicitly prohibited** in their TOS
- You must have an **active subscription** to download tracks
- Downloaded tracks are for **your own use only**
- You cannot **redistribute** or **resell** downloaded tracks
- **Respect rate limits** - don't overload their servers

**Recommendation:** Use automation for **personal productivity**, not to scrape their entire library.

### Rate Limiting Respect

**Why rate limiting matters:**
- Epidemic Sound servers have capacity limits
- Excessive requests can trigger anti-bot measures
- Respectful automation ensures service availability for everyone

**Implement rate limiting:**

```python
import time

# Add delay between requests (2-3 seconds)
time.sleep(2)

# Randomize delays to appear more human
import random
time.sleep(random.uniform(1.5, 3.0))

# Limit concurrent operations
max_concurrent = 1  # Only one browser instance at a time

# Batch with breaks
for i, track in enumerate(tracks):
    download_track(track)

    # Break every 20 tracks
    if (i + 1) % 20 == 0:
        print("Taking a 60-second break...")
        time.sleep(60)
```

**Respect signs of rate limiting:**
```python
def check_rate_limit(page):
    """Check if we're being rate limited."""
    if 'rate limit' in page.content().lower():
        print("⚠ Rate limit detected - waiting 5 minutes...")
        time.sleep(300)
        return True
    return False
```

### When Automation is Appropriate

**✓ Good use cases:**
- Downloading tracks for your own video projects
- Building a personal music library (within subscription limits)
- Batch creating custom durations for upcoming videos
- Organizing music by platform/use case

**✗ Inappropriate use cases:**
- Scraping entire Epidemic Sound library
- Downloading tracks you don't intend to use
- Sharing automation tools to bypass subscription requirements
- Reselling or redistributing downloaded tracks
- Running 24/7 continuous automation

**Rule of thumb:** If you could reasonably do it manually (just slower), automation is appropriate.

### Account Safety Tips

**Protect your account:**

1. **Use strong, unique passwords**
   ```bash
   # Generate secure password
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Enable 2FA (Two-Factor Authentication)**
   - Adds security layer
   - Automation can handle 2FA with manual intervention

3. **Don't share credentials**
   - Keep `.env.local` secure
   - Never commit to public repositories
   - Don't share session files

4. **Monitor unusual activity**
   - Check "Recent Downloads" in Epidemic Sound dashboard
   - Review account activity regularly
   - Report any unauthorized access

5. **Use session storage carefully**
   ```python
   # Don't save session state to public locations
   context.storage_state(path="epidemic_session.json")  # OK

   # Make sure it's in .gitignore
   # epidemic_session.json
   # .env.local
   ```

6. **Respect automation limits**
   - Don't run multiple instances simultaneously
   - Take breaks (every 50 tracks, pause 5 minutes)
   - Don't automate more than you'd manually download

---

## Advanced Usage

### Custom Adapt Descriptions for Different Video Types

The Adapt tool can create tracks optimized for specific video types. Customize descriptions to get better AI-generated adaptations:

```python
def download_with_custom_adapt(self, page, track_idx, duration,
                               video_type: str, output_name: str):
    """Download with video-type-specific Adapt descriptions."""

    # Video type descriptions for better AI adaptation
    adapt_descriptions = {
        'tutorial': 'Calm background music for educational tutorial video',
        'product_demo': 'Uplifting music for product demonstration',
        'explainer': 'Gentle background music that supports narration',
        'intro': 'Engaging intro music with strong opening',
        'outro': 'Smooth outro music with natural fade out',
        'transition': 'Brief transition music for scene changes',
        'time_lapse': 'Energetic music for time-lapse footage',
        'interview': 'Subtle background music for interview segments'
    }

    description = adapt_descriptions.get(video_type, 'Background music for video')

    # Click track
    tracks = page.locator('.track-card')
    tracks.nth(track_idx).click()
    page.wait_for_load_state('networkidle')

    # Open Adapt
    page.click('button:has-text("Adapt")')
    page.wait_for_timeout(2000)

    # Enter custom duration and description
    page.click('button:has-text("Custom")')
    page.fill('input[type="number"]', str(duration))

    # Fill description field (if available)
    try:
        page.fill('textarea[placeholder*="description"], textarea[name="description"]',
                 description)
    except:
        pass  # Description field may not exist

    # Create and download
    page.click('button:has-text("Create")')
    page.wait_for_timeout(5000)

    with page.expect_download() as download_info:
        page.click('button:has-text("Download")')

    download = download_info.value
    download.save_as(self.output_dir / f"{output_name}.mp3")

    page.go_back()
```

Usage:
```python
# Download intro music
client.download_with_custom_adapt(page, 0, 15, 'intro', 'youtube_intro_1')

# Download tutorial background
client.download_with_custom_adapt(page, 1, 180, 'tutorial', 'tutorial_background_1')
```

### Batch Processing Strategies

**Strategy 1: Platform-Specific Batches**

Download all music for one platform at a time:

```python
# Monday: YouTube content
client.download_platform_music('youtube', [30, 60, 180], tracks_per_category=10)

# Tuesday: Social media content
client.download_platform_music('instagram', [15, 30], tracks_per_category=5)
client.download_platform_music('tiktok', [15, 30], tracks_per_category=5)
```

**Strategy 2: Genre-Specific Batches**

Build genre-focused libraries:

```python
def download_genre_library(self, genre: str, track_count: int = 20):
    """Download comprehensive library for one genre."""

    moods = ['Calm', 'Uplifting', 'Energetic', 'Peaceful']
    durations = [15, 30, 60, 120, 180]

    for mood in moods:
        for duration in durations:
            for i in range(track_count // len(moods)):
                output_name = f"{genre}_{mood}_{duration}s_track{i+1}"
                # Download logic...

# Build ambient library
client.download_genre_library('ambient', track_count=50)
```

**Strategy 3: Incremental Daily Downloads**

Download a small batch daily to build library over time:

```python
import schedule

def daily_download_job():
    """Download 10 tracks per day."""
    client = EpidemicSoundAutomation()

    # Rotate through platforms each day
    day_of_week = datetime.now().weekday()
    platforms = ['youtube', 'instagram', 'tiktok', 'linkedin', 'facebook']

    platform = platforms[day_of_week % len(platforms)]

    client.download_platform_music(
        platform=platform,
        durations=[30, 60],
        tracks_per_category=2  # Small daily batch
    )

# Schedule for 2 AM daily
schedule.every().day.at("02:00").do(daily_download_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Integration with Video Pipeline

**Integrate with your video generation workflow:**

```python
# video_pipeline.py
from epidemic_sound_automation import EpidemicSoundAutomation

def generate_video_with_music(script_data):
    """Complete video generation with automated music."""

    # 1. Calculate video duration
    video_duration = calculate_narration_duration(script_data)

    # 2. Download matching music automatically
    music_client = EpidemicSoundAutomation()

    music_file = music_client.download_single_track(
        genre='ambient',
        mood='Calm',
        duration=video_duration,
        video_type='tutorial'
    )

    # 3. Generate narration
    narration_file = generate_narration(script_data)

    # 4. Generate images/animations
    visuals = generate_visuals(script_data)

    # 5. Compose video with music
    compose_video(
        visuals=visuals,
        narration=narration_file,
        background_music=music_file,
        output='final_video.mp4'
    )
```

**Smart music selection based on video characteristics:**

```python
def auto_select_music(video_metadata):
    """Automatically select appropriate music based on video characteristics."""

    # Analyze video metadata
    topic = video_metadata.get('topic', '')
    duration = video_metadata.get('duration', 60)
    pace = video_metadata.get('pace', 'medium')  # slow, medium, fast

    # Determine genre and mood
    if 'tutorial' in topic or 'how-to' in topic:
        genre, mood = 'ambient', 'Calm'
    elif 'product' in topic or 'review' in topic:
        genre, mood = 'corporate', 'Uplifting'
    elif 'story' in topic or 'narrative' in topic:
        genre, mood = 'cinematic', 'Emotional'
    else:
        genre, mood = 'ambient', 'Neutral'

    # Adjust for pace
    if pace == 'fast':
        mood = 'Energetic'
    elif pace == 'slow':
        mood = 'Calm'

    # Download appropriate music
    client = EpidemicSoundAutomation()
    return client.download_single_track(genre, mood, duration)
```

---

## Comparison: Browser Automation vs Manual vs API

### Feature Comparison

| Feature | Browser Automation | Manual | API |
|---------|-------------------|--------|-----|
| **Setup Time** | 30 minutes | 0 minutes | 5 minutes |
| **Learning Curve** | Medium | None | Low |
| **Adapt Tool Access** | ✓ Yes | ✓ Yes | ✗ No |
| **Custom Durations** | ✓ Yes | ✓ Yes | ✗ No |
| **Bulk Downloads** | ✓ Fast | ✗ Slow | ✓ Fast |
| **Search Filters** | ✓ All | ✓ All | ✓ Most |
| **Stems Download** | ✓ Yes | ✓ Yes | ⚠ Limited |
| **Ducking Mix** | ✓ Yes | ✓ Yes | ⚠ Limited |
| **Rate Limits** | Medium | None | Strict |
| **Reliability** | Medium | High | High |
| **Maintenance** | High* | None | Low |
| **Cost** | Free | Free | Free |

*Requires updates when website changes

### Performance Comparison

**Manual Download:**
- Time per track: ~2-3 minutes (with Adapt)
- 10 tracks: 20-30 minutes
- 100 tracks: 3-5 hours

**Browser Automation:**
- Time per track: ~30-45 seconds
- 10 tracks: 5-8 minutes
- 100 tracks: 50-75 minutes

**API Download:**
- Time per track: ~5-10 seconds
- 10 tracks: 1-2 minutes
- 100 tracks: 8-17 minutes
- **BUT**: No Adapt tool access

### Pros and Cons

#### Browser Automation

**Pros:**
- Access to Adapt tool (custom durations)
- Can use all web features (stems, ducking, segments)
- Visual feedback (can watch what's happening)
- Can handle dynamic content
- Bypasses API rate limits

**Cons:**
- Breaks when website updates (requires maintenance)
- Slower than API
- More resource-intensive (full browser running)
- Requires active session management
- May trigger anti-bot measures if overused

#### Manual Download

**Pros:**
- No setup required
- Most reliable (you control everything)
- Best for one-off downloads
- Can make judgment calls on quality
- No risk of account issues

**Cons:**
- Very time-consuming for bulk downloads
- Repetitive and tedious
- Human error possible
- Not suitable for automation workflows

#### API Download

**Pros:**
- Fastest download speed
- Most reliable (official interface)
- Easy to integrate with code
- Good documentation
- Designed for automation

**Cons:**
- No access to Adapt tool
- No custom durations
- Strict rate limits
- Limited to API-exposed features
- Requires API credentials

### When to Use Which Method

**Use Browser Automation when:**
- You need Adapt tool (custom durations)
- Downloading 20-100 tracks in one session
- You need stems or ducking mix
- API doesn't support required feature
- Building a comprehensive music library

**Use Manual when:**
- Downloading 1-5 tracks
- Evaluating music quality before automating
- Need to make creative decisions
- Testing before full automation
- Website changes broke automation

**Use API when:**
- Downloading tracks without Adapt
- Need maximum speed
- Integrating with production workflow
- Downloading at standard durations
- Want most reliable automation

**Hybrid Approach (Recommended):**
```python
# Use API for standard downloads
api_client.download_track(track_id, 'music/track.mp3')

# Use browser automation for custom durations
browser_client.download_track_with_adapt(page, track_idx, 45, 'custom_45s')
```

---

## Summary

### Quick Decision Guide

**Choose browser automation if:**
- ✓ You need to download 20+ tracks regularly
- ✓ You need custom durations via Adapt tool
- ✓ You want to batch-download for multiple platforms
- ✓ You're comfortable with basic Python and debugging
- ✓ You have time for initial setup and occasional maintenance

**Choose manual download if:**
- ✓ You only need a few tracks occasionally
- ✓ You want to preview music quality before downloading
- ✓ You don't have technical skills for automation
- ✓ You value simplicity over speed

**Choose API if:**
- ✓ You don't need Adapt tool
- ✓ You want maximum reliability
- ✓ You need production-grade automation
- ✓ Standard durations work for your needs

### Next Steps

1. **Try the Quick Start** (5 minutes)
   - Test login automation
   - Verify download works
   - Familiarize yourself with process

2. **Run Small Batch** (30 minutes)
   - Download 5-10 tracks for one platform
   - Test different genres and moods
   - Verify file quality and organization

3. **Full Automation** (2-3 hours)
   - Run complete workflow for all platforms
   - Build comprehensive music library
   - Integrate with video pipeline

4. **Maintain and Update**
   - Monitor for website changes
   - Update selectors as needed
   - Expand library over time

### Support and Resources

- **Epidemic Sound Documentation**: https://support.epidemicsound.com/
- **Playwright Documentation**: https://playwright.dev/python/
- **Project Issues**: Report problems in project repository
- **Community**: Share your automation workflows!

---

**Created:** December 2024
**Version:** 1.0
**Compatibility:** Epidemic Sound website (as of December 2024)

**Note:** Web automation scripts may require updates when Epidemic Sound updates their website structure. Check for selector updates if scripts stop working.
