#!/bin/bash
# Installation script for Epidemic Sound Browser Automation
# Run with: bash install_epidemic_browser.sh

echo "=============================================="
echo "Epidemic Sound Browser Automation - Install"
echo "=============================================="

# Check Python installation
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "L Python not found. Please install Python 3.8+"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD=$(command -v python3 || command -v python)
echo " Using Python: $PYTHON_CMD"

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2)
echo " Python version: $PYTHON_VERSION"

# Install Playwright
echo ""
echo "[1/3] Installing Playwright..."
$PYTHON_CMD -m pip install playwright pandas

if [ $? -ne 0 ]; then
    echo "L Failed to install Playwright"
    exit 1
fi
echo " Playwright installed"

# Install Playwright browsers
echo ""
echo "[2/3] Installing Chromium browser..."
$PYTHON_CMD -m playwright install chromium

if [ $? -ne 0 ]; then
    echo "L Failed to install Chromium"
    exit 1
fi
echo " Chromium installed"

# Verify installation
echo ""
echo "[3/3] Verifying installation..."
$PYTHON_CMD -c "from playwright.async_api import async_playwright; print(' Playwright import successful')"

if [ $? -ne 0 ]; then
    echo "L Playwright verification failed"
    exit 1
fi

# Create example .env file
echo ""
echo "Creating example .env file..."
cat > .env.example.epidemic << EOF
# Epidemic Sound Credentials
EPIDEMIC_SOUND_EMAIL=your.email@example.com
EPIDEMIC_SOUND_PASSWORD=your_password_here

# Epidemic Sound API (optional, for downloading)
EPIDEMIC_SOUND_ACCESS_KEY_ID=your_access_key_id
EPIDEMIC_SOUND_ACCESS_KEY_SECRET=your_access_key_secret
EOF

echo " Created .env.example.epidemic"

# Success
echo ""
echo "=============================================="
echo " Installation Complete!"
echo "=============================================="
echo ""
echo "Next Steps:"
echo "  1. Copy .env.example.epidemic to .env"
echo "  2. Edit .env and add your credentials"
echo "  3. Run: python epidemic_browser_search.py --help"
echo "  4. Or run examples: python example_epidemic_browser.py"
echo ""
echo "Quick Test:"
echo "  python epidemic_browser_search.py --query \"ambient\" --limit 5"
echo ""
