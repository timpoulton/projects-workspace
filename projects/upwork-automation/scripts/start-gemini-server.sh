#!/bin/bash
# Start Gemini-enhanced Upwork Proposal Server

echo "🚀 Starting Gemini-enhanced Upwork Proposal Server..."

# Check if old server is running
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5001 is already in use. Stopping existing server..."
    # Try to kill the process
    kill $(lsof -t -i:5001) 2>/dev/null || true
    sleep 2
fi

# Start the new server
cd /root/homelab-docs/scripts/upwork-automation
echo "✨ Starting server with Gemini AI integration..."
python3 upwork-proposal-server-gemini.py 