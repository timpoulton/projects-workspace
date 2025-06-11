#!/bin/bash

# Start All Services for Upwork Proposal Generator
# This script starts both the multi-model AI server and the simple generator

echo "🚀 Starting Upwork Proposal Generator Services..."
echo "=============================================="

# Change to the correct directory
cd /root/homelab-docs/scripts/upwork-automation

# Function to check if a process is running
check_process() {
    if pgrep -f "$1" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# Start Multi-Model AI Server
echo ""
echo "1️⃣  Checking Multi-Model AI Server..."
if check_process "upwork-proposal-server-multimodel.py"; then
    echo "   ✅ Multi-Model AI Server is already running"
else
    echo "   🔄 Starting Multi-Model AI Server..."
    nohup python3 upwork-proposal-server-multimodel.py > multimodel.log 2>&1 &
    sleep 3
    if check_process "upwork-proposal-server-multimodel.py"; then
        echo "   ✅ Multi-Model AI Server started successfully"
    else
        echo "   ❌ Failed to start Multi-Model AI Server"
        echo "   Check multimodel.log for errors"
        exit 1
    fi
fi

# Start Simple Generator
echo ""
echo "2️⃣  Checking Simple Generator..."
if check_process "simple-upwork-generator.py"; then
    echo "   ⚠️  Simple Generator is already running"
    echo "   Do you want to restart it? (y/n)"
    read -r response
    if [[ "$response" == "y" ]]; then
        echo "   🔄 Stopping existing Simple Generator..."
        pkill -f "simple-upwork-generator.py"
        sleep 2
    else
        echo "   ✅ Keeping existing Simple Generator running"
    fi
fi

if ! check_process "simple-upwork-generator.py"; then
    echo "   🔄 Starting Simple Generator..."
    python3 simple-upwork-generator.py &
    GENERATOR_PID=$!
    sleep 3
    if check_process "simple-upwork-generator.py"; then
        echo "   ✅ Simple Generator started successfully"
    else
        echo "   ❌ Failed to start Simple Generator"
        exit 1
    fi
fi

# Display access information
echo ""
echo "=============================================="
echo "✅ All services are running!"
echo ""
echo "📊 Dashboard Access:"
echo "   http://192.168.1.107:5056"
echo ""
echo "🔗 Chrome Extension Webhook:"
echo "   http://192.168.1.107:5056/webhook/rss-jobs"
echo ""
echo "📝 Logs:"
echo "   Simple Generator: tail -f simple-generator.log"
echo "   Multi-Model AI:   tail -f multimodel.log"
echo ""
echo "🧪 Test the system:"
echo "   python3 test-proposal-generation.py"
echo ""
echo "🛑 To stop all services:"
echo "   pkill -f 'upwork-proposal-server-multimodel.py'"
echo "   pkill -f 'simple-upwork-generator.py'"
echo ""
echo "Press Ctrl+C to stop the Simple Generator"
echo "=============================================="

# Keep the script running if Simple Generator was started
if [ ! -z "$GENERATOR_PID" ]; then
    wait $GENERATOR_PID
fi 