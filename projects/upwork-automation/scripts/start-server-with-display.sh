#!/bin/bash
# Start the Upwork Proposal Generator with virtual display support

cd /root/homelab-docs/scripts/upwork-automation

# Kill any existing instances
pkill -f "simple-upwork-generator.py"

# Check if xvfb is installed
if ! command -v xvfb-run &> /dev/null; then
    echo "Installing xvfb..."
    apt-get update && apt-get install -y xvfb
fi

echo "Starting Upwork Proposal Generator with virtual display..."

# Start with xvfb-run for virtual display
xvfb-run -a --server-args="-screen 0 1920x1080x24" \
    venv/bin/python simple-upwork-generator.py 