#!/bin/bash

# Port forwarding script for Club77 Check-in App
echo "Setting up port forwarding for Club77 Check-in App..."

# Check if socat is installed
if ! command -v socat &> /dev/null; then
    echo "socat is not installed. Installing..."
    apt-get update && apt-get install -y socat
fi

# Kill any existing socat processes for this port
echo "Stopping any existing port forwarding..."
pkill -f "socat TCP-LISTEN:8081" || true
sleep 1

# Start new port forwarding in the background
echo "Starting port forwarding from 8081 to 3001..."
socat TCP-LISTEN:8081,fork TCP:localhost:3001 &
SOCAT_PID=$!
echo "Started socat with PID: $SOCAT_PID"

# Give it a moment to start
sleep 2

# Check if it's running
if netstat -tuln | grep 8081 > /dev/null; then
    echo "✅ Port forwarding is active! App is accessible at:"
    echo "   - Internal: http://localhost:8081"
    echo "   - External: http://guestlist.club77.com.au:8081"
    
    # Try a local test
    echo "Attempting local test..."
    curl -I localhost:8081
else
    echo "❌ Failed to set up port forwarding"
    echo "Checking if port 8081 is already in use by another process:"
    lsof -i :8081
    exit 1
fi

# Update documentation
cat > /root/homelab-docs/club77-checkin/PORT-ACCESS.md << 'EOL'
# Club77 Check-in App Access

The Club77 check-in application is accessible at the following URLs:

## Internal Access
- http://localhost:3001 - Direct access to the Node.js application (container port)
- http://localhost:8081 - Access via port forwarding

## External Access
- http://guestlist.club77.com.au:8081 - Access from outside the network

## Port Forwarding Requirements
To make the application accessible from outside your network:

1. Forward port 8081 on your EdgeRouter to 192.168.1.107:8081 (already set up)
2. Ensure the port forwarding on the server is active

## Restarting Port Forwarding
If the port forwarding stops working, run:
```
bash /root/homelab-docs/club77-checkin/port-forward.sh
```

This script sets up a port forwarding from 8081 to the internal application port 3001.
EOL

echo "Created PORT-ACCESS.md documentation"
echo "Done! Your app should be accessible at http://guestlist.club77.com.au:8081" 