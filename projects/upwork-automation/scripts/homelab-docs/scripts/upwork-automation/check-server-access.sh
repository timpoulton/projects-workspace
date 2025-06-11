#!/bin/bash

# Script to check if the Upwork Proposal Generator server is accessible
# and provide troubleshooting steps if it's not

echo "🔍 Checking Upwork Proposal Generator server accessibility..."
echo ""

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Server details
SERVER_IP="192.168.1.107"
SERVER_PORT="5055"
SERVER_URL="http://${SERVER_IP}:${SERVER_PORT}"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if server process is running
echo -e "${BLUE}Checking if server process is running...${NC}"
if pgrep -f "simple-upwork-generator.py" > /dev/null; then
    echo -e "${GREEN}✅ Server process is running${NC}"
else
    echo -e "${RED}❌ Server process is not running${NC}"
    echo -e "${YELLOW}ℹ️ Try starting the server with:${NC}"
    echo "   cd /root/homelab-docs/scripts/upwork-automation && ./run-simple-generator.sh"
    exit 1
fi

# Check localhost connectivity
echo -e "\n${BLUE}Checking localhost connectivity...${NC}"
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:${SERVER_PORT}" | grep -q "200"; then
    echo -e "${GREEN}✅ Server is accessible via localhost${NC}"
else
    echo -e "${RED}❌ Server is not accessible via localhost${NC}"
    echo -e "${YELLOW}ℹ️ This indicates the server may not be binding to all interfaces or is not running properly${NC}"
    echo "   Check server logs for errors"
fi

# Check IP address connectivity from server
echo -e "\n${BLUE}Checking IP connectivity from server...${NC}"
if curl -s -o /dev/null -w "%{http_code}" "http://${SERVER_IP}:${SERVER_PORT}" | grep -q "200"; then
    echo -e "${GREEN}✅ Server is accessible via IP address from the server itself${NC}"
else
    echo -e "${RED}❌ Server is not accessible via IP address from the server${NC}"
    echo -e "${YELLOW}ℹ️ This indicates a possible network configuration issue${NC}"
    echo "   Check that the server is binding to all interfaces (0.0.0.0)"
fi

# Check if port is open
echo -e "\n${BLUE}Checking if port ${SERVER_PORT} is open...${NC}"
if command_exists "ss"; then
    if ss -tuln | grep -q ":${SERVER_PORT}"; then
        echo -e "${GREEN}✅ Port ${SERVER_PORT} is open and listening${NC}"
    else
        echo -e "${RED}❌ Port ${SERVER_PORT} is not open${NC}"
        echo -e "${YELLOW}ℹ️ The server is not listening on port ${SERVER_PORT}${NC}"
        echo "   Check if the server started with the correct port"
    fi
elif command_exists "netstat"; then
    if netstat -tuln | grep -q ":${SERVER_PORT}"; then
        echo -e "${GREEN}✅ Port ${SERVER_PORT} is open and listening${NC}"
    else
        echo -e "${RED}❌ Port ${SERVER_PORT} is not open${NC}"
        echo -e "${YELLOW}ℹ️ The server is not listening on port ${SERVER_PORT}${NC}"
        echo "   Check if the server started with the correct port"
    fi
else
    echo -e "${YELLOW}⚠️ Cannot check if port is open (ss or netstat not available)${NC}"
fi

# Check for firewall blocking
echo -e "\n${BLUE}Checking for firewall rules...${NC}"
if command_exists "iptables"; then
    if iptables -L | grep -q "DROP"; then
        echo -e "${YELLOW}⚠️ Firewall rules found that might block connections${NC}"
        echo "   Check iptables rules to ensure port ${SERVER_PORT} is allowed"
    else
        echo -e "${GREEN}✅ No obvious firewall blocks detected${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Cannot check firewall (iptables not available)${NC}"
fi

# Generate an HTML file for testing
echo -e "\n${BLUE}Creating test HTML file...${NC}"
TEST_HTML="/root/homelab-docs/scripts/upwork-automation/server-test.html"
cat > "${TEST_HTML}" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Server Test</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Server Access Test</h1>
    <p>Click the links below to test server access:</p>
    <ul>
        <li><a href="http://${SERVER_IP}:${SERVER_PORT}" target="_blank">Access via IP: http://${SERVER_IP}:${SERVER_PORT}</a></li>
        <li><a href="http://localhost:${SERVER_PORT}" target="_blank">Access via localhost: http://localhost:${SERVER_PORT}</a></li>
        <li><a href="http://tpserver:${SERVER_PORT}" target="_blank">Access via hostname: http://tpserver:${SERVER_PORT}</a></li>
    </ul>
</body>
</html>
EOF
echo -e "${GREEN}✅ Created test HTML file at ${TEST_HTML}${NC}"

# Print summary and recommendations
echo -e "\n${BLUE}=== Summary and Recommendations ===${NC}"
echo -e "1. Server process is running: $(pgrep -f "simple-upwork-generator.py" > /dev/null && echo -e "${GREEN}Yes${NC}" || echo -e "${RED}No${NC}")"
echo -e "2. Server accessible via localhost: $(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${SERVER_PORT}" | grep -q "200" && echo -e "${GREEN}Yes${NC}" || echo -e "${RED}No${NC}")"
echo -e "3. Server accessible via IP from server: $(curl -s -o /dev/null -w "%{http_code}" "http://${SERVER_IP}:${SERVER_PORT}" | grep -q "200" && echo -e "${GREEN}Yes${NC}" || echo -e "${RED}No${NC}")"

echo -e "\n${YELLOW}Try these troubleshooting steps:${NC}"
echo "1. Ensure you're on the same network as the server"
echo "2. Try using the test HTML file generated at ${TEST_HTML}"
echo "3. Ping the server to verify network connectivity: ping ${SERVER_IP}"
echo "4. Check for any VPN or network isolation that might be preventing access"
echo "5. Try using SSH tunneling: ssh -L ${SERVER_PORT}:localhost:${SERVER_PORT} root@${SERVER_IP}"
echo "6. Check the server logs: tail -f /root/homelab-docs/scripts/upwork-automation/simple-generator.log"

echo -e "\n${GREEN}For direct access, use:${NC}"
echo "http://${SERVER_IP}:${SERVER_PORT}" 