#!/bin/bash
# Upwork Automation Server - Fixed Version Deployment
# Safely deploys the corrected OpenAI API v1.0+ implementation

set -e

echo "🚀 Deploying FIXED Upwork Proposal Server..."
echo "🔧 FIXES: OpenAI API v1.0+, Client Name Extraction, Enhanced Fallbacks"

# Backup current version
echo "📦 Creating backup of current server..."
cp scripts/upwork-automation/upwork-proposal-server.py scripts/upwork-automation/upwork-proposal-server-backup-$(date +%Y%m%d-%H%M%S).py

# Stop current server
echo "⏹️ Stopping current server..."
pkill -f upwork-proposal-server || echo "Server not running"
sleep 2

# Deploy fixed version
echo "🚀 Deploying fixed version..."
cp scripts/upwork-automation/upwork-proposal-server-fixed.py scripts/upwork-automation/upwork-proposal-server.py

# Ensure OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ WARNING: OPENAI_API_KEY environment variable not set"
    echo "   AI features will fall back to enhanced content generation"
fi

# Verify scoring config exists
if [ ! -f "scripts/upwork-automation/scoring-config.json" ]; then
    echo "⚠️ WARNING: scoring-config.json not found"
    echo "   Server will use basic scoring"
fi

# Start fixed server
echo "▶️ Starting fixed server..."
cd /root/homelab-docs
python3 scripts/upwork-automation/upwork-proposal-server.py &
SERVER_PID=$!

# Wait for startup
sleep 3

# Test server health
echo "🔍 Testing server health..."
if curl -s http://localhost:5001/webhook/rss-jobs -X POST -H "Content-Type: application/json" -d '[]' | grep -q "success"; then
    echo "✅ Server is healthy and responding!"
    echo "🎯 Webhook URL: http://192.168.1.107:5001/webhook/rss-jobs"
    echo "📊 Proposals: /var/www/projekt-ai.net/proposals/"
    echo "📋 Queue: scripts/upwork-automation/proposal-queue.json"
    echo ""
    echo "🔧 FIXES DEPLOYED:"
    echo "   ✅ OpenAI API updated to v1.0+ format"
    echo "   ✅ Intelligent client name extraction added"
    echo "   ✅ Enhanced fallback content for better quality"
    echo "   ✅ Improved error handling and recovery"
    echo ""
    echo "🧪 To test with a sample job:"
    echo "   python3 scripts/upwork-automation/test-fixed-server.py"
else
    echo "❌ Server health check failed!"
    echo "🔄 Rolling back to previous version..."
    pkill -f upwork-proposal-server || true
    # Find latest backup
    LATEST_BACKUP=$(ls -1t scripts/upwork-automation/upwork-proposal-server-backup-*.py | head -1)
    if [ -f "$LATEST_BACKUP" ]; then
        cp "$LATEST_BACKUP" scripts/upwork-automation/upwork-proposal-server.py
        echo "📦 Restored from: $LATEST_BACKUP"
    fi
    exit 1
fi

echo "🎉 Fixed server deployment complete!"
echo "   Process ID: $SERVER_PID"
echo "   Log: journalctl -f --grep upwork-proposal-server" 