@echo off
REM Installation script for Epidemic Sound Browser Automation (Windows)
REM Run with: install_epidemic_browser.bat

echo ==============================================
echo Epidemic Sound Browser Automation - Install
echo ==============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python found

REM Install Playwright
echo.
echo [1/3] Installing Playwright...
python -m pip install playwright pandas

if %errorlevel% neq 0 (
    echo X Failed to install Playwright
    pause
    exit /b 1
)
echo [OK] Playwright installed

REM Install Playwright browsers
echo.
echo [2/3] Installing Chromium browser...
python -m playwright install chromium

if %errorlevel% neq 0 (
    echo X Failed to install Chromium
    pause
    exit /b 1
)
echo [OK] Chromium installed

REM Verify installation
echo.
echo [3/3] Verifying installation...
python -c "from playwright.async_api import async_playwright; print('[OK] Playwright import successful')"

if %errorlevel% neq 0 (
    echo X Playwright verification failed
    pause
    exit /b 1
)

REM Create example .env file
echo.
echo Creating example .env file...
(
echo # Epidemic Sound Credentials
echo EPIDEMIC_SOUND_EMAIL=your.email@example.com
echo EPIDEMIC_SOUND_PASSWORD=your_password_here
echo.
echo # Epidemic Sound API ^(optional, for downloading^)
echo EPIDEMIC_SOUND_ACCESS_KEY_ID=your_access_key_id
echo EPIDEMIC_SOUND_ACCESS_KEY_SECRET=your_access_key_secret
) > .env.example.epidemic

echo [OK] Created .env.example.epidemic

REM Success
echo.
echo ==============================================
echo [OK] Installation Complete!
echo ==============================================
echo.
echo Next Steps:
echo   1. Copy .env.example.epidemic to .env
echo   2. Edit .env and add your credentials
echo   3. Run: python epidemic_browser_search.py --help
echo   4. Or run examples: python example_epidemic_browser.py
echo.
echo Quick Test:
echo   python epidemic_browser_search.py --query "ambient" --limit 5
echo.

pause
