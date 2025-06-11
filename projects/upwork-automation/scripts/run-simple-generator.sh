#!/bin/bash

# Simple script to run the simplified Upwork proposal generator
# This script ensures the virtual environment is activated and all dependencies are installed

echo "🚀 Starting Simple Upwork Proposal Generator"

# Directory where the script is located
SCRIPT_DIR="/root/homelab-docs/scripts/upwork-automation"
VENV_DIR="$SCRIPT_DIR/venv"

# Check if virtual environment exists, create if not
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install required packages
echo "Installing dependencies..."
pip install flask requests
pip install selenium undetected-chromedriver 2>/dev/null

# Check if Chrome is installed
if ! command -v google-chrome &> /dev/null; then
  echo "⚠️ Google Chrome is not installed. The Selenium-based scraper will be disabled."
  echo "  To enable the Selenium scraper, install Chrome with:"
  echo "  apt update && apt install -y wget gnupg"
  echo "  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -"
  echo "  echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google.list"
  echo "  apt update && apt install -y google-chrome-stable"
fi

# Check if the multi-model server is running
if pgrep -f "upwork-proposal-server-multimodel.py" > /dev/null; then
  echo "✅ Multi-Model AI server is running"
else
  echo "⚠️ Multi-Model AI server is not running"
  echo "Starting Multi-Model AI server..."
  
  # Try to start the multi-model server
  python "$SCRIPT_DIR/upwork-proposal-server-multimodel.py" > "$SCRIPT_DIR/logs/multimodel-server.log" 2>&1 &
  
  # Wait for it to start
  sleep 5
  
  if pgrep -f "upwork-proposal-server-multimodel.py" > /dev/null; then
    echo "✅ Multi-Model AI server started successfully"
  else
    echo "❌ Failed to start Multi-Model AI server. Please check logs."
    echo "Continuing anyway, fallback generation will be used."
  fi
fi

# Run the simple generator
echo "Starting Simple Upwork Proposal Generator..."
python "$SCRIPT_DIR/simple-upwork-generator.py" 