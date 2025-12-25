"""
Auto-login with credentials and download tracks
"""

import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

OUTPUT_DIR = Path("background_music_epidemic")
OUTPUT_DIR.mkdir(exist_ok=True)

# Credentials
EMAIL = "jdmallin25x40@gmail.com"
PASSWORD = "Time10104040##"

PROMPT = "instrumental electronic chillstep"
MINIMAL_DESC = "Minimal background for voiceover. Reduce mid-range. Subtle consistent."

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

async def login(page):
    """Auto-login to Epidemic Sound"""
    log("Navigating to login page...")
    await page.goto("https://www.epidemicsound.com/login/")
    await asyncio.sleep(3)

    # Accept cookies
    try:
        await page.click('button:has-text("Accept")', timeout=2000)
        log("Cookies accepted")
    except:
        pass

    await asyncio.sleep(2)

    # Enter email
    log("Entering email...")
    email_input = await page.wait_for_selector('input[name="username"], input[type="email"]')
    await email_input.fill(EMAIL)
    await asyncio.sleep(1)

    # Enter password
    log("Entering password...")
    password_input = await page.wait_for_selector('input[name="password"], input[type="password"]')
    await password_input.fill(PASSWORD)
    await asyncio.sleep(1)

    # Click submit
    log("Submitting login...")
    await page.click('button[type="submit"], button:has-text("Log in")')
    await asyncio.sleep(5)

    # Wait for redirect back to main site
    log("Waiting for login to complete...")
    log("(If you see a captcha or 2FA, please complete it in the browser)")
    for i in range(60):  # Wait up to 1 minute
        current_url = page.url

        # Check if we're on the main site (not login/auth pages)
        if 'epidemicsound.com/music' in current_url or 'epidemicsound.com/labs' in current_url:
            log(f"Login successful! On: {current_url}")
            return True

        # Also accept if we're not on login pages
        if '/login' not in current_url and '/auth/realms' not in current_url:
            if 'epidemicsound.com' in current_url:
                log(f"Login successful! On: {current_url}")
                return True

        # Take screenshot to see what's happening
        if i == 10:
            await page.screenshot(path=OUTPUT_DIR / "login_check.png")
            log("Screenshot saved - check login_check.png")

        await asyncio.sleep(1)

    log("Login timeout - check browser")
    await page.screenshot(path=OUTPUT_DIR / "login_timeout.png")
    return False

async def download_track(page, track_name, index):
    """Download one track"""
    log(f"\n{'='*60}")
    log(f"TRACK {index}: {track_name[:40]}")
    log(f"{'='*60}")

    try:
        # Go to Labs Adapt
        log("Navigate to Labs Adapt")
        await page.goto("https://www.epidemicsound.com/labs/adapt/", wait_until='load')
        await asyncio.sleep(4)

        # Check if we got redirected to login
        if 'login' in page.url or 'auth' in page.url:
            log("Redirected to login - session expired")
            return {'success': False, 'error': 'Session expired'}

        # Click "New" button to open search
        log("Click 'New' button")
        try:
            await page.click('button:has-text("New")', timeout=5000)
            await asyncio.sleep(2)
            log("New button clicked")
        except:
            log("New button not found - search may already be open")

        # Find search
        log("Find search input")
        search_input = await page.wait_for_selector('input[type="search"]', state='visible', timeout=10000)

        # Search
        log(f"Search: {track_name[:30]}")
        await search_input.fill(track_name)
        await asyncio.sleep(1)
        await page.keyboard.press('Enter')
        await asyncio.sleep(6)  # Increased wait for results

        # Try multiple selectors for results
        log("Looking for results...")
        results = None
        result_selectors = [
            'a[href*="/track/"]',
            '[data-testid*="track"]',
            'article a',
            'button:has-text("Adapt")',
        ]

        for selector in result_selectors:
            elements = await page.locator(selector).all()
            if elements and len(elements) > 0:
                results = elements
                log(f"Found {len(elements)} results with: {selector}")
                break

        if not results:
            # Take screenshot for debugging
            await page.screenshot(path=OUTPUT_DIR / f"no_results_{index}.png")
            raise Exception("No results found")

        # Click first result
        log("Select track")
        await results[0].click()
        await asyncio.sleep(4)

        # Adapt Length
        log("Adapt Length (3 min)")
        await page.click('button:has-text("Adapt length")')
        await asyncio.sleep(2)

        dur = await page.wait_for_selector('input[type="number"]')
        await dur.fill("180")

        try:
            duck = await page.wait_for_selector('input[type="checkbox"]', timeout=2000)
            if not await duck.is_checked():
                await duck.click()
        except:
            pass

        await page.click('button:has-text("Adapt")')
        log("Processing length...")

        for i in range(15):
            if await page.locator('button:has-text("Download"), button:has-text("Adapt music")').count() > 0:
                break
            await asyncio.sleep(2)

        # Adapt Music
        log("Adapt Music")
        await page.click('button:has-text("Adapt music")')
        await asyncio.sleep(2)

        try:
            desc = await page.wait_for_selector('textarea', timeout=3000)
            await desc.fill(MINIMAL_DESC)
        except:
            pass

        await page.click('button:has-text("Adapt")')
        log("Processing music...")

        for i in range(15):
            if await page.locator('button:has-text("Download")').count() > 0:
                break
            await asyncio.sleep(2)

        # Download
        log("Download WAV")
        await page.click('button:has-text("Download")')
        await asyncio.sleep(1)
        await page.click('text="WAV"')
        await asyncio.sleep(1)

        filename = f"track_{index}.wav"
        save_path = OUTPUT_DIR / filename

        async with page.expect_download(timeout=30000) as dl_info:
            await page.click('button:has-text("Download")')

        dl = await dl_info.value
        await dl.save_as(save_path)

        size_mb = save_path.stat().st_size / (1024 * 1024)
        log(f"SUCCESS: {save_path.name} - {size_mb:.1f} MB")
        return {'success': True, 'path': str(save_path)}

    except Exception as e:
        log(f"FAILED: {e}")
        await page.screenshot(path=OUTPUT_DIR / f"error_track_{index}.png")
        return {'success': False, 'error': str(e)}

async def main():
    log("="*60)
    log("AUTO-LOGIN AND DOWNLOAD WORKFLOW")
    log("="*60)

    async with async_playwright() as p:
        log("Opening browser...")
        browser = await p.chromium.launch(headless=False, args=['--start-maximized'])
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Login
            if not await login(page):
                log("Login failed - stopping")
                await asyncio.sleep(10)
                return

            await asyncio.sleep(2)

            # Search for tracks
            log("\nSearch for tracks")
            await page.goto("https://www.epidemicsound.com/music/search/")
            await asyncio.sleep(3)

            search = await page.wait_for_selector("input[type='search']", state='visible')
            await search.fill(PROMPT)
            await search.press("Enter")
            await asyncio.sleep(4)

            try:
                await page.click("text=Instrumental", timeout=2000)
                await asyncio.sleep(2)
            except:
                pass

            tracks = await page.query_selector_all("a[href*='/music/tracks/']")
            track_names = []
            for t in tracks[:3]:
                name = (await t.text_content()).strip()
                track_names.append(name)
                log(f"  Found: {name}")

            # Download each track
            results = []
            for idx, name in enumerate(track_names, 1):
                result = await download_track(page, name, idx)
                results.append(result)
                await asyncio.sleep(2)

            # Summary
            log("\n" + "="*60)
            log("SUMMARY")
            log("="*60)
            ok = [r for r in results if r['success']]
            log(f"Success: {len(ok)}/{len(results)}")

            if ok:
                log("\nFiles:")
                for r in ok:
                    log(f"  {Path(r['path']).name}")

            log("\nClosing in 10 seconds...")
            await asyncio.sleep(10)

        except Exception as e:
            log(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            await asyncio.sleep(10)

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
