#!/bin/bash
# Install Playwright and required browsers for Epidemic Sound automation

set -e

echo "========================================"
echo "Playwright Installation Script"
echo "========================================"
echo

echo "[1/3] Installing Playwright Python package..."
pip install playwright
echo

echo "[2/3] Installing Chromium browser..."
playwright install chromium
echo

echo "[3/3] Verifying installation..."
python -c "import playwright; print(f'Playwright version: {playwright.__version__}')"
echo

echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Add credentials to .env file:"
echo "   EPIDEMIC_EMAIL=your_email@example.com"
echo "   EPIDEMIC_PASSWORD=your_password"
echo
echo "2. Test the login:"
echo "   python epidemic_browser_login.py --test"
echo
echo "For help, see: EPIDEMIC_SOUND_SETUP.md"
echo
