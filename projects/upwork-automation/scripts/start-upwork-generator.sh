#!/bin/bash
# Start Upwork Proposal Generator with proper setup

cd /root/homelab-docs/scripts/upwork-automation

# Kill any existing instances
echo "Stopping any existing instances..."
pkill -f "simple-upwork-generator.py" || true
pkill -f "Xvfb" || true

# Clear Chrome cache
echo "Clearing Chrome cache..."
rm -rf /root/.local/share/undetected_chromedriver/
rm -rf /tmp/.com.google.Chrome*
rm -rf /tmp/.org.chromium.*

# Start virtual display
echo "Starting virtual display..."
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
XVFB_PID=$!
sleep 2

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up..."
    kill $XVFB_PID 2>/dev/null || true
    pkill -f "simple-upwork-generator.py" || true
}
trap cleanup EXIT

# Start the server
echo "Starting Upwork Proposal Generator..."
echo "Access it at: http://192.168.1.107:5056"
echo "Press Ctrl+C to stop"

# Run with the virtual display
DISPLAY=:99 venv/bin/python simple-upwork-generator.py 