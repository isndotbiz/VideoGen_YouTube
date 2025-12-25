@echo off
REM Master Music Downloader - Windows Batch Script
REM Quick launcher for download_all_platform_music.py

echo ================================================================================
echo                    MASTER MUSIC DOWNLOADER
echo ================================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check environment variables
if "%EPIDEMIC_ACCESS_KEY_ID%"=="" (
    echo ERROR: EPIDEMIC_ACCESS_KEY_ID not set!
    echo.
    echo Set environment variables:
    echo   $env:EPIDEMIC_ACCESS_KEY_ID="your_access_key_id"
    echo   $env:EPIDEMIC_ACCESS_KEY_SECRET="your_access_key_secret"
    echo.
    pause
    exit /b 1
)

if "%EPIDEMIC_ACCESS_KEY_SECRET%"=="" (
    echo ERROR: EPIDEMIC_ACCESS_KEY_SECRET not set!
    echo.
    echo Set environment variables:
    echo   $env:EPIDEMIC_ACCESS_KEY_ID="your_access_key_id"
    echo   $env:EPIDEMIC_ACCESS_KEY_SECRET="your_access_key_secret"
    echo.
    pause
    exit /b 1
)

echo Credentials verified!
echo.

REM Parse command line arguments
if "%1"=="quick" (
    echo Running in QUICK MODE - 20 tracks
    echo.
    python download_all_platform_music.py --quick
) else if "%1"=="youtube" (
    echo Downloading YOUTUBE only
    echo.
    python download_all_platform_music.py --platforms youtube
) else if "%1"=="tiktok" (
    echo Downloading TIKTOK only
    echo.
    python download_all_platform_music.py --platforms tiktok
) else if "%1"=="instagram" (
    echo Downloading INSTAGRAM only
    echo.
    python download_all_platform_music.py --platforms instagram
) else if "%1"=="twitter" (
    echo Downloading TWITTER only
    echo.
    python download_all_platform_music.py --platforms twitter
) else if "%1"=="resume" (
    echo Resuming previous download
    echo.
    python download_all_platform_music.py --resume
) else if "%1"=="help" (
    echo Usage:
    echo   download_music.bat           - Download all 60 tracks
    echo   download_music.bat quick     - Quick test ^(20 tracks^)
    echo   download_music.bat youtube   - YouTube only
    echo   download_music.bat tiktok    - TikTok only
    echo   download_music.bat instagram - Instagram only
    echo   download_music.bat twitter   - Twitter only
    echo   download_music.bat resume    - Resume interrupted download
    echo   download_music.bat help      - Show this help
    echo.
    pause
    exit /b 0
) else (
    echo Downloading ALL 60 tracks
    echo.
    python download_all_platform_music.py
)

echo.
echo ================================================================================
echo                          DOWNLOAD COMPLETE
echo ================================================================================
echo.
echo View your library: python show_music_library.py
echo.
pause
