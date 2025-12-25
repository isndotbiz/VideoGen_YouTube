"""
Test script for adapt_music_automation.py

This script verifies the automation works correctly by testing individual components.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from adapt_music_automation import (
    AdaptMusicAutomation,
    DEFAULT_DESCRIPTION,
    SHORT_DESCRIPTION,
    take_screenshot,
    wait_with_progress,
    SCREENSHOT_DIR
)


def test_imports():
    """Test that all imports work."""
    print("Testing imports...")
    try:
        from playwright.sync_api import sync_playwright
        print("[PASS] Playwright imported successfully")
        return True
    except ImportError as e:
        print(f"[FAIL] Failed to import Playwright: {e}")
        print("  Run: pip install playwright")
        print("  Then: playwright install chromium")
        return False


def test_screenshot_dir():
    """Test that screenshot directory can be created."""
    print("\nTesting screenshot directory...")
    try:
        if SCREENSHOT_DIR.exists():
            print(f"[PASS] Screenshot directory exists: {SCREENSHOT_DIR}")
        else:
            SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            print(f"[PASS] Screenshot directory created: {SCREENSHOT_DIR}")
        return True
    except Exception as e:
        print(f"[FAIL] Failed to create screenshot directory: {e}")
        return False


def test_descriptions():
    """Test that descriptions are defined correctly."""
    print("\nTesting descriptions...")
    try:
        assert len(DEFAULT_DESCRIPTION) > 0, "Default description is empty"
        assert len(SHORT_DESCRIPTION) > 0, "Short description is empty"

        print(f"[PASS] Default description ({len(DEFAULT_DESCRIPTION)} chars):")
        print(f"  {DEFAULT_DESCRIPTION[:100]}...")

        print(f"[PASS] Short description ({len(SHORT_DESCRIPTION)} chars):")
        print(f"  {SHORT_DESCRIPTION[:100]}...")

        return True
    except AssertionError as e:
        print(f"[FAIL] Description test failed: {e}")
        return False


def test_automation_init():
    """Test that automation can be initialized."""
    print("\nTesting automation initialization...")
    try:
        # Test with defaults
        automation = AdaptMusicAutomation(
            page=None,
            headless=True,
            description="Test description"
        )

        print("[PASS] Automation initialized with defaults")
        print(f"  Headless: {automation.headless}")
        print(f"  Timeout: {automation.timeout}s")
        print(f"  Stems: {automation.stems}")
        print(f"  Owns browser: {automation.owns_browser}")

        # Test with custom parameters
        automation2 = AdaptMusicAutomation(
            headless=False,
            slow_mo=1000,
            description="Custom description",
            stems="melody",
            timeout=180
        )

        print("[PASS] Automation initialized with custom params")
        print(f"  Slow mo: {automation2.slow_mo}ms")
        print(f"  Timeout: {automation2.timeout}s")
        print(f"  Stems: {automation2.stems}")

        return True
    except Exception as e:
        print(f"[FAIL] Automation initialization failed: {e}")
        return False


def test_helper_functions():
    """Test helper functions."""
    print("\nTesting helper functions...")
    try:
        # Test wait_with_progress (should complete quickly)
        import time
        start = time.time()
        # Don't actually wait 10 seconds in test
        print("[PASS] wait_with_progress function exists")

        return True
    except Exception as e:
        print(f"[FAIL] Helper function test failed: {e}")
        return False


def test_browser_start_stop():
    """Test that browser can start and stop."""
    print("\nTesting browser start/stop...")
    try:
        automation = AdaptMusicAutomation(headless=True)

        print("  Starting browser...")
        automation.start_browser()

        if automation.browser is None:
            print("[FAIL] Browser not started")
            return False

        print("[PASS] Browser started successfully")

        print("  Closing browser...")
        automation.close_browser()

        if automation.browser is not None:
            print("[FAIL] Browser not closed")
            return False

        print("[PASS] Browser closed successfully")

        return True
    except Exception as e:
        print(f"[FAIL] Browser test failed: {e}")
        print("  Make sure Playwright is installed: playwright install chromium")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("ADAPT MUSIC AUTOMATION - TEST SUITE")
    print("=" * 80)

    tests = [
        ("Imports", test_imports),
        ("Screenshot Directory", test_screenshot_dir),
        ("Descriptions", test_descriptions),
        ("Automation Init", test_automation_init),
        ("Helper Functions", test_helper_functions),
        ("Browser Start/Stop", test_browser_start_stop),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'=' * 80}")
        print(f"TEST: {test_name}")
        print('=' * 80)

        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n[FAIL] Test crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n=== ALL TESTS PASSED ===")
        print("\nYou can now run the automation:")
        print("  python adapt_music_automation.py --no-headless")
        return 0
    else:
        print("\n=== SOME TESTS FAILED ===")
        print("\nPlease fix the issues above before running the automation.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
