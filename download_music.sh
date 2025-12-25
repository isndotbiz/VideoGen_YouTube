#!/bin/bash
# Master Music Downloader - Linux/Mac Shell Script
# Quick launcher for download_all_platform_music.py

echo "================================================================================"
echo "                    MASTER MUSIC DOWNLOADER"
echo "================================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found!"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

# Check environment variables
if [ -z "$EPIDEMIC_ACCESS_KEY_ID" ]; then
    echo "ERROR: EPIDEMIC_ACCESS_KEY_ID not set!"
    echo ""
    echo "Set environment variables:"
    echo "  export EPIDEMIC_ACCESS_KEY_ID=\"your_access_key_id\""
    echo "  export EPIDEMIC_ACCESS_KEY_SECRET=\"your_access_key_secret\""
    echo ""
    exit 1
fi

if [ -z "$EPIDEMIC_ACCESS_KEY_SECRET" ]; then
    echo "ERROR: EPIDEMIC_ACCESS_KEY_SECRET not set!"
    echo ""
    echo "Set environment variables:"
    echo "  export EPIDEMIC_ACCESS_KEY_ID=\"your_access_key_id\""
    echo "  export EPIDEMIC_ACCESS_KEY_SECRET=\"your_access_key_secret\""
    echo ""
    exit 1
fi

echo "Credentials verified!"
echo ""

# Parse command line arguments
case "$1" in
    quick)
        echo "Running in QUICK MODE - 20 tracks"
        echo ""
        python3 download_all_platform_music.py --quick
        ;;
    youtube)
        echo "Downloading YOUTUBE only"
        echo ""
        python3 download_all_platform_music.py --platforms youtube
        ;;
    tiktok)
        echo "Downloading TIKTOK only"
        echo ""
        python3 download_all_platform_music.py --platforms tiktok
        ;;
    instagram)
        echo "Downloading INSTAGRAM only"
        echo ""
        python3 download_all_platform_music.py --platforms instagram
        ;;
    twitter)
        echo "Downloading TWITTER only"
        echo ""
        python3 download_all_platform_music.py --platforms twitter
        ;;
    resume)
        echo "Resuming previous download"
        echo ""
        python3 download_all_platform_music.py --resume
        ;;
    help|--help|-h)
        echo "Usage:"
        echo "  ./download_music.sh           - Download all 60 tracks"
        echo "  ./download_music.sh quick     - Quick test (20 tracks)"
        echo "  ./download_music.sh youtube   - YouTube only"
        echo "  ./download_music.sh tiktok    - TikTok only"
        echo "  ./download_music.sh instagram - Instagram only"
        echo "  ./download_music.sh twitter   - Twitter only"
        echo "  ./download_music.sh resume    - Resume interrupted download"
        echo "  ./download_music.sh help      - Show this help"
        echo ""
        exit 0
        ;;
    *)
        echo "Downloading ALL 60 tracks"
        echo ""
        python3 download_all_platform_music.py
        ;;
esac

echo ""
echo "================================================================================"
echo "                          DOWNLOAD COMPLETE"
echo "================================================================================"
echo ""
echo "View your library: python3 show_music_library.py"
echo ""
