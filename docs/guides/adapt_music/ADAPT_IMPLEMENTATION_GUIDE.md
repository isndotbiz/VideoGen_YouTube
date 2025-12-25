# Adapt Page Loading - Implementation Guide

**Step-by-step guide to implement reliable Adapt page automation**

---

## Phase 1: Initial Navigation Setup

### Code Template

```python
import asyncio
from playwright.async_api import async_playwright

async def navigate_to_adapt_page(page, headless=False):
    """
    Navigate to Labs Adapt with proper timing and verification.

    Returns:
        bool: True if successfully navigated and verified
    """

    ADAPT_URL = "https://www.epidemicsound.com/labs/adapt/"
    TIMEOUT_NAVIGATION = 30000  # 30 seconds

    try:
        # Step 1: Navigate with domcontentloaded
        print("Navigating to Labs Adapt...")
        response = await page.goto(
            ADAPT_URL,
            wait_until='domcontentloaded',  # Key: Don't wait for full load
            timeout=TIMEOUT_NAVIGATION
        )

        # Step 2: Verify HTTP status
        if not response or response.status >= 400:
            print(f"Navigation failed with status {response.status if response else 'No response'}")
            return False

        print(f"HTTP {response.status} - Page loaded")

        # Step 3: Allow dynamic content to load (CRITICAL)
        print("Waiting for dynamic content...")
        await asyncio.sleep(2)

        # Step 4: Verify correct page
        current_url = page.url
        print(f"Current URL: {current_url}")

        if '/labs/adapt' not in current_url:
            print(f"ERROR: Wrong page - {current_url}")
            return False

        print("✓ On correct page")
        return True

    except Exception as e:
        print(f"Navigation error: {e}")
        return False
```

---

## Phase 2: Page Readiness Verification

### Code Template

```python
async def verify_adapt_page_loaded(page, timeout_seconds=30):
    """
    Verify that the Adapt page is fully loaded and interactive.

    Uses multiple indicators to detect when page is ready for interaction.

    Returns:
        bool: True if page is ready
    """
    import time

    start_time = time.time()

    # Indicators that page is ready
    required_elements = [
        {
            'name': 'Search input',
            'selector': 'input[type="search"]',
            'timeout': 10000
        },
        {
            'name': 'Adapt length text',
            'locator': 'text="Adapt length"',
            'count_check': True
        },
        {
            'name': 'Adapt music text',
            'locator': 'text="Adapt music"',
            'count_check': True
        }
    ]

    print("\nVerifying Adapt page readiness...")
    print("-" * 60)

    for element in required_elements:
        try:
            if 'selector' in element:
                # Use wait_for_selector for critical elements
                print(f"Checking: {element['name']}...", end=' ')
                result = await page.wait_for_selector(
                    element['selector'],
                    state='visible',
                    timeout=element['timeout']
                )
                print("✓ Found")

            elif 'locator' in element and element.get('count_check'):
                # Use locator count for non-critical elements
                print(f"Checking: {element['name']}...", end=' ')
                count = await page.locator(element['locator']).count()
                if count > 0:
                    print(f"✓ Found ({count})")
                else:
                    print("✗ Not found")

        except Exception as e:
            print(f"✗ Not found ({e})")
            elapsed = int(time.time() - start_time)
            if elapsed > timeout_seconds:
                print(f"\nTimeout after {timeout_seconds}s")
                return False

    print("-" * 60)
    print("✓ Page is ready for automation\n")
    return True
```

### Usage

```python
# After navigation
if await verify_adapt_page_loaded(page):
    print("Ready to proceed with search/automation")
else:
    print("Page failed to load - check screenshots")
    await page.screenshot(path="adapt_load_failure.png")
```

---

## Phase 3: Search and Track Selection

### Code Template

```python
async def search_and_select_track(page, track_name):
    """
    Search for a track by name and select the first result.

    Args:
        page: Playwright page object
        track_name: Name of track to search for

    Returns:
        bool: True if track selected successfully
    """

    print(f"\nSearching for track: {track_name}")
    print("-" * 60)

    try:
        # Step 1: Find and click search input
        print("Step 1: Locating search input...")
        search_input = await page.wait_for_selector(
            'input[type="search"]',
            timeout=5000
        )
        print("✓ Search input found")

        # Step 2: Clear and type track name
        print(f"Step 2: Typing track name...")
        await search_input.click()
        await asyncio.sleep(0.5)  # Buffer for focus
        await search_input.fill("")
        await asyncio.sleep(0.2)
        await search_input.fill(track_name)
        await asyncio.sleep(1)  # Wait for input processing
        print(f"✓ Typed: {track_name}")

        # Step 3: Press Enter to search
        print("Step 3: Submitting search...")
        await page.keyboard.press('Enter')
        await asyncio.sleep(2)  # Wait for results
        print("✓ Search submitted")

        # Step 4: Wait for results to appear
        print("Step 4: Waiting for results...")
        await asyncio.sleep(1)  # Extra wait for results rendering

        # Step 5: Select first result
        print("Step 5: Selecting first result...")

        result_selectors = [
            'a[href*="/track/"]',
            '[data-testid="track-card"]',
            'article a',
            'button:has-text("Adapt")'
        ]

        result_element = None
        for selector in result_selectors:
            elements = await page.query_selector_all(selector)
            if elements:
                result_element = elements[0]
                print(f"✓ Found result with selector: {selector}")
                break

        if not result_element:
            print("✗ No results found")
            await page.screenshot(path="no_search_results.png")
            return False

        # Step 6: Click the result
        print("Step 6: Clicking track...")
        await result_element.click()
        await asyncio.sleep(2)  # Wait for track to load
        print("✓ Track selected")

        print("-" * 60)
        return True

    except Exception as e:
        print(f"✗ Search/selection failed: {e}")
        await page.screenshot(path="search_error.png")
        return False
```

### Usage

```python
if await search_and_select_track(page, "Neon Dreams"):
    print("Track loaded successfully")
else:
    print("Failed to load track")
```

---

## Phase 4: Length Adaptation

### Code Template

```python
async def adapt_track_length(
    page,
    duration_seconds=180,
    enable_ducking=True,
    max_processing_time=90
):
    """
    Adapt track length with optional ducking mix.

    Args:
        page: Playwright page object
        duration_seconds: Target duration in seconds (default 180 = 3 min)
        enable_ducking: Enable ducking mix if available
        max_processing_time: Max wait for AI processing in seconds

    Returns:
        bool: True if adaptation successful
    """

    print(f"\nAdapting track length to {duration_seconds}s ({duration_seconds//60}min)...")
    print("-" * 60)

    try:
        # Step 1: Open length adaptation panel
        print("Step 1: Opening length adaptation panel...")
        length_btn = await page.wait_for_selector(
            'button:has-text("Adapt length")',
            timeout=5000
        )
        await length_btn.click()
        await asyncio.sleep(2)  # Wait for panel animation
        print("✓ Panel opened")

        # Step 2: Set duration
        print(f"Step 2: Setting duration to {duration_seconds}s...")
        duration_input = await page.wait_for_selector(
            'input[type="number"]',
            timeout=5000
        )
        await duration_input.click()
        await asyncio.sleep(0.2)
        await duration_input.fill("")
        await asyncio.sleep(0.2)
        await duration_input.fill(str(duration_seconds))
        await asyncio.sleep(1)
        print(f"✓ Duration set to {duration_seconds}s")

        # Step 3: Enable ducking mix (optional)
        if enable_ducking:
            print("Step 3: Enabling ducking mix...")
            try:
                ducking_checkbox = await page.query_selector(
                    'input[type="checkbox"][name*="duck"]'
                )
                if ducking_checkbox:
                    is_checked = await ducking_checkbox.evaluate(
                        "el => el.checked"
                    )
                    if not is_checked:
                        await ducking_checkbox.click()
                        await asyncio.sleep(0.5)
                    print("✓ Ducking mix enabled")
                else:
                    print("⚠ Ducking option not found (may be default)")
            except Exception as e:
                print(f"⚠ Could not enable ducking: {e}")

        # Step 4: Click Adapt button
        print("Step 4: Starting AI processing...")
        adapt_btn = await page.wait_for_selector(
            'button:has-text("Adapt"), button:has-text("Create")',
            timeout=5000
        )
        await adapt_btn.click()
        await asyncio.sleep(1)
        print("✓ Processing started")

        # Step 5: Wait for processing with polling
        print(f"Step 5: Waiting for processing (max {max_processing_time}s)...")
        success = await wait_for_ai_processing(
            page,
            timeout_seconds=max_processing_time,
            check_interval=2,
            log_interval=10
        )

        if success:
            print("✓ Length adaptation complete")
        else:
            print("✗ Processing timeout")

        print("-" * 60)
        return success

    except Exception as e:
        print(f"✗ Length adaptation failed: {e}")
        await page.screenshot(path="adapt_length_error.png")
        return False
```

---

## Phase 5: AI Processing Wait Loop

### Code Template

```python
async def wait_for_ai_processing(
    page,
    timeout_seconds=90,
    check_interval=2,
    log_interval=10
):
    """
    Poll for AI processing completion.

    Uses indicators to detect when processing is complete.

    Args:
        page: Playwright page object
        timeout_seconds: Maximum wait time
        check_interval: How often to check (seconds)
        log_interval: How often to log progress (seconds)

    Returns:
        bool: True if processing completed, False if timeout
    """
    import time

    print(f"  Polling every {check_interval}s, max wait {timeout_seconds}s...")

    start_time = time.time()
    last_log = start_time

    # Indicators that processing is happening
    processing_indicators = [
        '[data-state="processing"]',
        '[aria-busy="true"]',
        'text="Processing"',
        'text="Generating"',
        '[role="progressbar"]',
        '.spinner',
        '.processing'
    ]

    # Indicators that processing is complete
    completion_indicators = [
        'text="Complete"',
        'text="Done"',
        'button:has-text("Download")',
        'button:has-text("Adapt music")',
        '[data-state="complete"]',
        '[aria-busy="false"]'
    ]

    while True:
        elapsed = int(time.time() - start_time)

        # Check processing state
        is_processing = False
        for indicator in processing_indicators:
            try:
                count = await page.locator(indicator).count()
                if count > 0:
                    is_processing = True
                    break
            except:
                continue

        # Check completion state
        is_complete = False
        for indicator in completion_indicators:
            try:
                count = await page.locator(indicator).count()
                if count > 0:
                    is_complete = True
                    break
            except:
                continue

        # Log progress every N seconds
        if (time.time() - last_log) >= log_interval:
            status = "Processing" if is_processing else "Not processing"
            pct = int((elapsed / timeout_seconds) * 100)
            print(f"  {elapsed}s elapsed ({pct}%) - {status}")
            last_log = time.time()

        # Success condition
        if is_complete and not is_processing:
            return True

        # Timeout condition
        if elapsed > timeout_seconds:
            print(f"  TIMEOUT after {timeout_seconds}s")
            return False

        # Wait before next check
        await asyncio.sleep(check_interval)
```

---

## Phase 6: Music Adaptation

### Code Template

```python
async def adapt_track_music(
    page,
    description="Minimal, background-friendly for voiceover narration. Reduce mid-range 200-800Hz. Remove buildups and drops.",
    max_processing_time=120
):
    """
    Adapt track music to be minimal and background-friendly.

    Args:
        page: Playwright page object
        description: AI description of desired music changes
        max_processing_time: Max wait for AI processing

    Returns:
        bool: True if adaptation successful
    """

    print(f"\nAdapting music...")
    print("-" * 60)

    try:
        # Step 1: Open music adaptation panel
        print("Step 1: Opening music adaptation panel...")
        music_btn = await page.wait_for_selector(
            'button:has-text("Adapt music")',
            timeout=5000
        )
        await music_btn.click()
        await asyncio.sleep(2)  # Wait for panel animation
        print("✓ Panel opened")

        # Step 2: Enter description
        print("Step 2: Entering music description...")
        description_field = await page.wait_for_selector(
            'textarea, input[type="text"][placeholder*="descri"]',
            timeout=5000
        )
        await description_field.click()
        await asyncio.sleep(0.2)
        await description_field.fill("")
        await asyncio.sleep(0.2)
        await description_field.fill(description)
        await asyncio.sleep(1)
        print("✓ Description entered")

        # Step 3: Click Adapt button
        print("Step 3: Starting AI processing...")
        adapt_btn = await page.wait_for_selector(
            'button:has-text("Adapt"), button:has-text("Process")',
            timeout=5000
        )
        await adapt_btn.click()
        await asyncio.sleep(1)
        print("✓ Processing started")

        # Step 4: Wait for processing
        print(f"Step 4: Waiting for processing (max {max_processing_time}s)...")
        success = await wait_for_ai_processing(
            page,
            timeout_seconds=max_processing_time,
            check_interval=2,
            log_interval=10
        )

        if success:
            print("✓ Music adaptation complete")
        else:
            print("✗ Processing timeout")

        print("-" * 60)
        return success

    except Exception as e:
        print(f"✗ Music adaptation failed: {e}")
        await page.screenshot(path="adapt_music_error.png")
        return False
```

---

## Phase 7: Download

### Code Template

```python
async def download_adapted_track(page, output_path="output.wav"):
    """
    Download the adapted track as WAV.

    Args:
        page: Playwright page object
        output_path: Where to save the file

    Returns:
        bool: True if download successful
    """

    print(f"\nDownloading track...")
    print("-" * 60)

    try:
        # Step 1: Find and click download button
        print("Step 1: Locating download button...")
        download_btn = await page.wait_for_selector(
            'button:has-text("Download")',
            timeout=5000
        )
        await download_btn.click()
        await asyncio.sleep(2)
        print("✓ Download dialog opened")

        # Step 2: Select WAV format (if dialog)
        print("Step 2: Selecting WAV format...")
        try:
            wav_btn = await page.query_selector('button:has-text("WAV")')
            if wav_btn:
                await wav_btn.click()
                await asyncio.sleep(1)
                print("✓ WAV format selected")
        except:
            print("⚠ WAV format not in dialog (may be default)")

        # Step 3: Handle the download
        print("Step 3: Downloading file...")
        async with page.expect_download(timeout=120000) as download_info:
            # Click final download button
            final_btn = await page.wait_for_selector(
                'button:has-text("Download")',
                timeout=5000
            )
            await final_btn.click()

        # Step 4: Save downloaded file
        download = await download_info.value
        await download.save_as(output_path)

        file_size = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"✓ Downloaded ({file_size:.1f} MB)")

        print("-" * 60)
        return True

    except Exception as e:
        print(f"✗ Download failed: {e}")
        await page.screenshot(path="download_error.png")
        return False
```

---

## Phase 8: Complete Workflow

### Code Template

```python
async def process_track_complete(page, track_name, output_path):
    """
    Complete workflow: Search → Load → Adapt Length → Adapt Music → Download

    Args:
        page: Playwright page object
        track_name: Name of track to process
        output_path: Where to save downloaded WAV

    Returns:
        bool: True if entire workflow succeeded
    """

    print("\n" + "=" * 70)
    print(f"PROCESSING TRACK: {track_name}")
    print("=" * 70)

    # Phase 1: Navigation
    if not await navigate_to_adapt_page(page):
        print("\n✗ Navigation failed")
        return False

    # Phase 2: Verification
    if not await verify_adapt_page_loaded(page):
        print("\n✗ Page verification failed")
        return False

    # Phase 3: Search & Select
    if not await search_and_select_track(page, track_name):
        print("\n✗ Track search/selection failed")
        return False

    # Phase 4: Length Adaptation
    if not await adapt_track_length(
        page,
        duration_seconds=180,
        enable_ducking=True,
        max_processing_time=90
    ):
        print("\n✗ Length adaptation failed")
        return False

    # Phase 5: Music Adaptation
    if not await adapt_track_music(
        page,
        description="Minimal, background-friendly for voiceover narration. "
                   "Reduce mid-range 200-800Hz. Remove buildups and drops.",
        max_processing_time=120
    ):
        print("\n✗ Music adaptation failed")
        return False

    # Phase 6: Download
    if not await download_adapted_track(page, output_path):
        print("\n✗ Download failed")
        return False

    print("\n" + "=" * 70)
    print(f"✓ TRACK PROCESSING COMPLETE")
    print("=" * 70)
    print(f"Output: {output_path}\n")

    return True
```

---

## Usage Example

```python
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import json

async def main():
    # Load session
    with open("epidemic_session.json", "r") as f:
        session = json.load(f)

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=session['storage_state'])
        page = await context.new_page()

        try:
            # Process track
            success = await process_track_complete(
                page,
                track_name="Neon Dreams",
                output_path="neon_dreams_adapted.wav"
            )

            if success:
                print("\nSUCCESS! Track downloaded and saved.")
            else:
                print("\nFAILED! Check logs and screenshots.")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Error Handling Patterns

### Pattern 1: Graceful Degradation

```python
async def try_optional_feature(page, selector, action_description):
    """Try an optional feature, continue if not found"""
    try:
        element = await page.query_selector(selector)
        if element:
            await element.click()
            await asyncio.sleep(0.5)
            print(f"✓ {action_description}")
            return True
    except:
        pass

    print(f"⚠ {action_description} not available")
    return False
```

### Pattern 2: Retry with Backoff

```python
async def retry_action(action, max_attempts=3, backoff_delay=2):
    """Retry an action with exponential backoff"""
    for attempt in range(1, max_attempts + 1):
        try:
            return await action()
        except Exception as e:
            if attempt == max_attempts:
                raise
            delay = backoff_delay * attempt
            print(f"Attempt {attempt} failed, retrying in {delay}s...")
            await asyncio.sleep(delay)
```

---

## Debugging Tips

1. **Always take screenshots on errors**
   ```python
   await page.screenshot(path="error_state.png")
   ```

2. **Log page content for debugging**
   ```python
   content = await page.content()
   with open("debug_page.html", "w") as f:
       f.write(content)
   ```

3. **Check browser console for errors**
   ```python
   logs = []
   page.on("console", lambda msg: logs.append(msg.text))
   # After operations
   for log in logs:
       print(f"Browser log: {log}")
   ```

4. **Verify selector existence before wait**
   ```python
   elements = await page.query_selector_all(selector)
   print(f"Found {len(elements)} elements matching {selector}")
   ```

---

## Performance Optimization

1. **Use headless mode for speed**
   ```python
   browser = await p.chromium.launch(headless=True)
   ```

2. **Reduce check intervals during processing**
   ```python
   await wait_for_ai_processing(page, check_interval=1)  # Check every 1s
   ```

3. **Parallelize independent tracks**
   ```python
   tasks = [process_track_complete(page, name, out) for name, out in tracks]
   results = await asyncio.gather(*tasks)
   ```

---

## See Also

- Complete reference: `ADAPT_TIMING_AND_LOADING_ANALYSIS.md`
- Quick reference: `ADAPT_TIMING_QUICK_REFERENCE.md`
- Navigation implementation: `adapt_navigation.py`
- Orchestration: `labs_adapt_complete.py`
