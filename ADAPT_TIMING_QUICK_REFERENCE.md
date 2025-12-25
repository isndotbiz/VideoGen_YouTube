# Adapt Page Timing - Quick Reference

**Copy-paste timing strategy for Labs Adapt automation**

---

## Navigation & Loading (3-4 seconds)

```python
# Navigate with short wait_until
await page.goto(
    "https://www.epidemicsound.com/labs/adapt/",
    wait_until='domcontentloaded',  # Don't wait for full load
    timeout=30000
)

# Critical: Let dynamic content load
await asyncio.sleep(2)

# Verify correct page
if '/labs/adapt' not in page.url:
    raise Exception(f"Wrong page: {page.url}")

# Wait for search input (up to 10 seconds)
await page.wait_for_selector(
    'input[type="search"]',
    state='visible',
    timeout=10000
)
```

---

## Load Indicators

### Page is Ready When:
- ✓ URL contains `/labs/adapt`
- ✓ Search input is visible: `input[type="search"]`
- ✓ Text "Adapt length" is present: `text="Adapt length"`
- ✓ Text "Adapt music" is present: `text="Adapt music"`

### Track is Loaded When:
- ✓ Canvas elements exist: `canvas` elements count > 0
- ✓ Canvas has content: `width > 0` and `height > 0`
- ✓ Play controls visible: `button[aria-label*="Play"]`

---

## Search & Selection (8-12 seconds)

```python
# 1. Click search input
await page.click('input[type="search"]')
await asyncio.sleep(0.5)

# 2. Type track name
await page.fill('input[type="search"]', "track name")
await asyncio.sleep(1)

# 3. Press Enter
await page.keyboard.press('Enter')
await asyncio.sleep(2)

# 4. Click first result
result = await page.query_selector('a[href*="/track/"]')
await result.click()
await asyncio.sleep(2)  # Wait for track to load
```

---

## Length Adaptation (35-95 seconds)

```python
# 1. Click "Adapt length" button (2 second wait after)
btn = await page.wait_for_selector('button:has-text("Adapt length")', timeout=5000)
await btn.click()
await asyncio.sleep(2)

# 2. Set duration to 180 seconds
input_field = await page.wait_for_selector('input[type="number"]', timeout=5000)
await input_field.fill("180")
await asyncio.sleep(1)

# 3. Enable ducking (optional)
ducking = await page.query_selector('input[type="checkbox"][name*="duck"]')
if ducking:
    await ducking.click()
    await asyncio.sleep(0.5)

# 4. Click "Adapt" button to start processing
process_btn = await page.wait_for_selector(
    'button:has-text("Adapt"), button:has-text("Create")',
    timeout=5000
)
await process_btn.click()

# 5. Wait for AI processing with polling
success = await wait_for_completion(
    page,
    timeout_seconds=90,
    check_interval_seconds=2,
    processing_indicators=['text="Processing"', '[role="progressbar"]'],
    completion_indicators=['text="Complete"', 'button:has-text("Download")']
)
```

---

## Music Adaptation (35-95 seconds)

```python
# 1. Click "Adapt music" button
btn = await page.wait_for_selector('button:has-text("Adapt music")', timeout=5000)
await btn.click()
await asyncio.sleep(2)

# 2. Enter description
textarea = await page.wait_for_selector('textarea', timeout=5000)
await textarea.fill("Minimal, background-friendly for voiceover narration...")
await asyncio.sleep(1)

# 3. Click "Adapt" to start processing
process_btn = await page.wait_for_selector(
    'button:has-text("Adapt"), button:has-text("Process")',
    timeout=5000
)
await process_btn.click()

# 4. Wait for completion (same as length adaptation)
success = await wait_for_completion(
    page,
    timeout_seconds=120,
    check_interval_seconds=2
)
```

---

## AI Processing Wait Loop (Generic)

```python
async def wait_for_completion(
    page,
    timeout_seconds=90,
    check_interval_seconds=2,
    processing_indicators=None,
    completion_indicators=None
) -> bool:
    """
    Poll for processing completion with progress logging.

    Args:
        page: Playwright page
        timeout_seconds: Max wait time
        check_interval_seconds: Poll interval
        processing_indicators: List of selectors showing processing is happening
        completion_indicators: List of selectors showing processing complete

    Returns:
        True if completed, False if timeout
    """
    import time

    processing_indicators = processing_indicators or [
        '[data-state="processing"]',
        'text="Processing"',
        '[role="progressbar"]'
    ]

    completion_indicators = completion_indicators or [
        'text="Complete"',
        'text="Done"',
        'button:has-text("Download")'
    ]

    start_time = time.time()
    last_log_time = start_time

    while (time.time() - start_time) < timeout_seconds:
        # Check if still processing
        is_processing = False
        for indicator in processing_indicators:
            if await page.locator(indicator).count() > 0:
                is_processing = True
                break

        # Check if complete
        is_complete = False
        for indicator in completion_indicators:
            if await page.locator(indicator).count() > 0:
                is_complete = True
                break

        # Success condition: complete and not processing
        if is_complete and not is_processing:
            return True

        # Log progress every 10 seconds
        if (time.time() - last_log_time) >= 10:
            elapsed = int(time.time() - start_time)
            logger.info(f"Processing... {elapsed}s elapsed")
            last_log_time = time.time()

        # Wait before next check
        await asyncio.sleep(check_interval_seconds)

    logger.error(f"Processing timeout after {timeout_seconds}s")
    return False
```

---

## Download (1-2 minutes)

```python
# 1. Click download button
download_btn = await page.wait_for_selector(
    'button:has-text("Download")',
    timeout=10000
)
await download_btn.click()
await asyncio.sleep(2)

# 2. Select WAV format (if dialog appears)
wav_btn = await page.query_selector('button:has-text("WAV")')
if wav_btn:
    await wav_btn.click()
    await asyncio.sleep(1)

# 3. Handle download
async with page.expect_download() as download_info:
    final_btn = await page.wait_for_selector(
        'button:has-text("Download")',
        timeout=5000
    )
    await final_btn.click()

download = await download_info.value
await download.save_as("output.wav")
```

---

## Timing Summary

| Phase | Duration | Wait After |
|-------|----------|-----------|
| Navigate | 1-2s | 2s (critical) |
| Search input ready | 0-5s | N/A (wait_for_selector) |
| Type & search | 1.5s | 2s after Enter |
| Track click | 0.1s | 2-3s after |
| Open adapt length | 0.1s | 2s after |
| Set duration & duck | 2-3s | N/A |
| Process | 30-90s | Poll every 2s |
| **Total per track** | **5-8 minutes** | |

---

## Common Patterns

### Try Multiple Selectors

```python
selectors = [
    'button:has-text("Adapt")',
    'button:has-text("Create")',
    'button:has-text("Process")',
    'button[type="submit"]'
]

element = None
for selector in selectors:
    try:
        element = await page.wait_for_selector(selector, timeout=3000)
        if element:
            break
    except:
        continue

if not element:
    raise Exception("Could not find adapt button")
```

### Safe Click Pattern

```python
async def safe_click(page, selector, timeout=5000, sleep_after=1):
    """Click with error handling and stabilization"""
    try:
        element = await page.wait_for_selector(selector, timeout=timeout)
        await element.click()
        await asyncio.sleep(sleep_after)
        return True
    except Exception as e:
        logger.error(f"Failed to click {selector}: {e}")
        return False
```

### Wait for Multiple Indicators

```python
async def verify_page_ready(page):
    """Check all indicators of page readiness"""
    checks = {
        'url': '/labs/adapt' in page.url,
        'search': await page.locator('input[type="search"]').count() > 0,
        'adapt_length': await page.locator('text="Adapt length"').count() > 0,
        'adapt_music': await page.locator('text="Adapt music"').count() > 0,
    }

    if not all(checks.values()):
        logger.warning(f"Page not fully ready: {checks}")
        return False
    return True
```

---

## Troubleshooting Timing Issues

### Problem: "Search input not found"
**Solution:** Increase initial sleep
```python
await page.goto(..., wait_until='domcontentloaded')
await asyncio.sleep(3)  # Was 2, increase to 3
```

### Problem: "Processing timeout"
**Solution:** Increase timeout or polling frequency
```python
# Increase timeout
success = await wait_for_completion(page, timeout_seconds=180)  # Was 90

# OR check more frequently
success = await wait_for_completion(page, check_interval_seconds=1)  # Was 2
```

### Problem: "Results not appearing after search"
**Solution:** Increase post-Enter sleep
```python
await page.keyboard.press('Enter')
await asyncio.sleep(3)  # Was 2, increase to 3
```

### Problem: "Track not loading after click"
**Solution:** Add extra sleep before proceeding
```python
await result.click()
await asyncio.sleep(4)  # Was 2, increase to 4
```

---

## Best Practices

1. **Always use wait_until='domcontentloaded'** - Faster than 'load'
2. **Always add 2-second sleep after navigation** - Critical for dynamic content
3. **Always verify with wait_for_selector** - Don't just sleep blindly
4. **Use 2-second check intervals** - Fast enough for responsiveness
5. **Log every 10 seconds during processing** - Track progress
6. **Set 90+ second timeout for AI** - Processing can be slow
7. **Take screenshots on errors** - Helps debugging

---

## Complete Example

```python
async def process_track_complete(page, track_name="Neon Dreams"):
    """Complete track processing workflow"""

    # NAVIGATION (3-4s)
    await page.goto(
        "https://www.epidemicsound.com/labs/adapt/",
        wait_until='domcontentloaded',
        timeout=30000
    )
    await asyncio.sleep(2)

    # SEARCH & SELECT (8-12s)
    await page.fill('input[type="search"]', track_name)
    await asyncio.sleep(1)
    await page.keyboard.press('Enter')
    await asyncio.sleep(2)
    result = await page.query_selector('a[href*="/track/"]')
    await result.click()
    await asyncio.sleep(2)

    # LENGTH ADAPTATION (35-95s)
    await (await page.wait_for_selector('button:has-text("Adapt length")')).click()
    await asyncio.sleep(2)
    await page.fill('input[type="number"]', "180")
    await asyncio.sleep(1)
    await (await page.wait_for_selector('button:has-text("Adapt")')).click()
    await wait_for_completion(page, timeout_seconds=90)

    # MUSIC ADAPTATION (35-95s)
    await (await page.wait_for_selector('button:has-text("Adapt music")')).click()
    await asyncio.sleep(2)
    await page.fill('textarea', "Minimal background music...")
    await asyncio.sleep(1)
    await (await page.wait_for_selector('button:has-text("Adapt")')).click()
    await wait_for_completion(page, timeout_seconds=120)

    # DOWNLOAD (1-2 min)
    async with page.expect_download() as dl:
        await (await page.wait_for_selector('button:has-text("Download")')).click()
    return await dl.value
```

---

## See Also

- Full timing analysis: `ADAPT_TIMING_AND_LOADING_ANALYSIS.md`
- Navigation implementation: `adapt_navigation.py`
- Complete orchestration: `labs_adapt_complete.py`
- Length automation: `adapt_length_automation.py`
