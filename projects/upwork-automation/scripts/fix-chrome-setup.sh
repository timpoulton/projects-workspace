#!/bin/bash
# Fix Chrome setup for Upwork scraper

echo "Fixing Chrome setup for Upwork scraper..."

# Install required system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    wget \
    gnupg \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libxtst6 \
    xdg-utils \
    fonts-liberation \
    libgbm-dev

# Kill any existing Chrome processes
echo "Killing existing Chrome processes..."
pkill -f chrome || true
pkill -f chromium || true

# Clear Chrome driver cache
echo "Clearing Chrome driver cache..."
rm -rf /root/.local/share/undetected_chromedriver/
rm -rf /tmp/.com.google.Chrome*
rm -rf /tmp/.org.chromium.*

# Set up display
echo "Setting up virtual display..."
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
sleep 2

echo "Chrome setup complete!"
echo "You can now run the scraper with:"
echo "  export DISPLAY=:99"
echo "  cd /root/homelab-docs/scripts/upwork-automation"
echo "  venv/bin/python simple-upwork-generator.py" 