#!/bin/bash

# Script to open the Upwork Proposal Generator Dashboard
# This provides a simple way to access the dashboard

echo "🚀 Opening Upwork Proposal Generator Dashboard..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Dashboard HTML file
DASHBOARD_FILE="$SCRIPT_DIR/dashboard.html"

# Check if the dashboard file exists
if [ ! -f "$DASHBOARD_FILE" ]; then
    echo "❌ Dashboard file not found at $DASHBOARD_FILE"
    exit 1
fi

# Determine which browser opener to use based on the environment
if command -v xdg-open > /dev/null; then
    # Linux with desktop environment
    echo "📊 Opening dashboard in browser..."
    xdg-open "$DASHBOARD_FILE"
elif command -v open > /dev/null; then
    # macOS
    echo "📊 Opening dashboard in browser..."
    open "$DASHBOARD_FILE"
elif command -v start > /dev/null; then
    # Windows
    echo "📊 Opening dashboard in browser..."
    start "$DASHBOARD_FILE"
else
    # No GUI browser available
    echo "⚠️ Could not detect a browser to open the dashboard"
    echo "📝 You can manually open the dashboard at:"
    echo "$DASHBOARD_FILE"
    
    # Try to display the file path
    echo ""
    echo "File URL: file://$DASHBOARD_FILE"
fi

echo ""
echo "ℹ️ If you're accessing this server remotely, please copy the dashboard.html file to your local machine"
echo "  or access the server directly at http://192.168.1.107:5055" 