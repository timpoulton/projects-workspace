#!/bin/bash

# Script to access the Upwork Proposal Generator
# Checks for server status and opens the browser to the appropriate URL

echo "🚀 Accessing Upwork Proposal Generator..."

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Server details
SERVER_IP="192.168.1.107"
SERVER_PORT="5055"
PROXY_PORT="80"
DOMAIN="upwork-generator.local"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to open URL in browser
open_in_browser() {
    local url="$1"
    echo -e "${BLUE}Opening ${url} in browser...${NC}"
    
    if command_exists "xdg-open"; then
        # Linux with desktop environment
        xdg-open "$url" &
    elif command_exists "open"; then
        # macOS
        open "$url" &
    elif command_exists "start"; then
        # Windows
        start "$url" &
    else
        # No GUI browser available
        echo -e "${YELLOW}⚠️ Could not detect a browser to open the URL${NC}"
        echo -e "${GREEN}Please manually open: ${url}${NC}"
    fi
}

# Check if server is running
echo -e "${BLUE}Checking if server is running...${NC}"
if ! pgrep -f "simple-upwork-generator.py" > /dev/null; then
    echo -e "${RED}❌ Server is not running${NC}"
    echo -e "${YELLOW}ℹ️ Starting the server...${NC}"
    
    # Try to start the server
    cd "$(dirname "$0")" && ./run-simple-generator.sh &
    
    # Wait for server to start
    echo -e "${YELLOW}⏳ Waiting for server to start...${NC}"
    sleep 5
    
    # Check again
    if ! pgrep -f "simple-upwork-generator.py" > /dev/null; then
        echo -e "${RED}❌ Failed to start server${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ Server started successfully${NC}"
    fi
else
    echo -e "${GREEN}✅ Server is already running${NC}"
fi

# Check which access methods are available
echo -e "\n${BLUE}Checking available access methods...${NC}"

# Check nginx proxy
if curl -s -o /dev/null -w "%{http_code}" "http://${SERVER_IP}" | grep -q "200"; then
    echo -e "${GREEN}✅ Nginx proxy is working (http://${SERVER_IP})${NC}"
    BEST_URL="http://${SERVER_IP}"
# Check direct access
elif curl -s -o /dev/null -w "%{http_code}" "http://${SERVER_IP}:${SERVER_PORT}" | grep -q "200"; then
    echo -e "${GREEN}✅ Direct access is working (http://${SERVER_IP}:${SERVER_PORT})${NC}"
    BEST_URL="http://${SERVER_IP}:${SERVER_PORT}"
# Check localhost
elif curl -s -o /dev/null -w "%{http_code}" "http://localhost:${SERVER_PORT}" | grep -q "200"; then
    echo -e "${GREEN}✅ Localhost access is working (http://localhost:${SERVER_PORT})${NC}"
    BEST_URL="http://localhost:${SERVER_PORT}"
else
    echo -e "${RED}❌ Server is running but not accessible via any method${NC}"
    
    # Fall back to local HTML dashboard
    echo -e "${YELLOW}ℹ️ Falling back to local HTML dashboard${NC}"
    DASHBOARD_FILE="$(dirname "$0")/dashboard.html"
    
    if [ -f "$DASHBOARD_FILE" ]; then
        echo -e "${GREEN}✅ Using local dashboard file${NC}"
        BEST_URL="file://${DASHBOARD_FILE}"
    else
        echo -e "${RED}❌ Could not find local dashboard file${NC}"
        echo -e "${YELLOW}ℹ️ Creating a simple dashboard file...${NC}"
        
        # Create a simple dashboard file
        DASHBOARD_FILE="$(dirname "$0")/quick-access.html"
        cat > "$DASHBOARD_FILE" << EOF
<!DOCTYPE html>
<html>
<head><title>Quick Access</title></head>
<body>
    <h1>Upwork Generator Quick Access</h1>
    <p>Try these URLs:</p>
    <ul>
        <li><a href="http://${SERVER_IP}" target="_blank">http://${SERVER_IP}</a></li>
        <li><a href="http://${SERVER_IP}:${SERVER_PORT}" target="_blank">http://${SERVER_IP}:${SERVER_PORT}</a></li>
        <li><a href="http://localhost:${SERVER_PORT}" target="_blank">http://localhost:${SERVER_PORT}</a></li>
    </ul>
</body>
</html>
EOF
        BEST_URL="file://${DASHBOARD_FILE}"
    fi
fi

# Open the best URL in browser
open_in_browser "$BEST_URL"

echo -e "\n${GREEN}✅ Done!${NC}"
echo -e "If the browser doesn't open automatically, please manually navigate to:"
echo -e "${BLUE}${BEST_URL}${NC}"
echo ""
echo -e "${YELLOW}Additional access options:${NC}"
echo -e "1. Via IP: ${BLUE}http://${SERVER_IP}${NC}"
echo -e "2. Direct access: ${BLUE}http://${SERVER_IP}:${SERVER_PORT}${NC}"
echo -e "3. Via domain (requires hosts file entry): ${BLUE}http://${DOMAIN}${NC}"
echo -e "4. Localhost (on server only): ${BLUE}http://localhost:${SERVER_PORT}${NC}" 