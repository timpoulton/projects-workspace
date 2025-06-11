#!/bin/bash
# Safe restart script for multi-model server
echo "🔄 SAFE SERVER RESTART"

# Find current server process
SERVER_PID=$(ps aux | grep "upwork-proposal-server-multimodel.py" | grep -v grep | awk '{print $2}')

if [ -n "$SERVER_PID" ]; then
    echo "📍 Found server running on PID: $SERVER_PID"
    
    # Backup current queue
    cp /root/homelab-docs/scripts/upwork-automation/proposal-queue.json \
       /root/homelab-docs/scripts/upwork-automation/proposal-queue-backup-$(date +%Y%m%d-%H%M%S).json
    echo "💾 Queue backed up"
    
    # Stop server gracefully
    echo "🛑 Stopping server..."
    kill $SERVER_PID
    sleep 2
    
    # Check if stopped
    if ps -p $SERVER_PID > /dev/null; then
        echo "⚠️ Graceful stop failed, forcing..."
        kill -9 $SERVER_PID
        sleep 1
    fi
    
    echo "✅ Server stopped"
else
    echo "⚠️ No server process found"
fi

# Start new server
echo "🚀 Starting updated server..."
cd /root/homelab-docs/scripts/upwork-automation
python3 upwork-proposal-server-multimodel.py &

echo "✅ Server restart complete!"
echo "📊 Check status: curl -s http://192.168.1.107:5001/status" 