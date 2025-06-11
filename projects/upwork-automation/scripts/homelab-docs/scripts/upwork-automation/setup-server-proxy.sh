#!/bin/bash

# Script to set up a simple Nginx reverse proxy for the Upwork Proposal Generator
# This will make the generator accessible on port 80 for easier access

echo "🔧 Setting up Nginx reverse proxy for Upwork Proposal Generator"
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
PROXY_PORT="80"
DOMAIN="upwork-generator.local"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root${NC}"
  exit 1
fi

# Check if nginx is installed
echo -e "${BLUE}Checking if Nginx is installed...${NC}"
if ! command -v nginx &> /dev/null; then
    echo -e "${YELLOW}Nginx not found. Installing...${NC}"
    apt-get update
    apt-get install -y nginx
    echo -e "${GREEN}✅ Nginx installed${NC}"
else
    echo -e "${GREEN}✅ Nginx is already installed${NC}"
fi

# Check if server is running
echo -e "\n${BLUE}Checking if Upwork Generator server is running...${NC}"
if ! pgrep -f "simple-upwork-generator.py" > /dev/null; then
    echo -e "${RED}❌ Server is not running${NC}"
    echo -e "${YELLOW}ℹ️ Please start the server first:${NC}"
    echo "   cd /root/homelab-docs/scripts/upwork-automation && ./run-simple-generator.sh"
    exit 1
else
    echo -e "${GREEN}✅ Server is running${NC}"
fi

# Create Nginx configuration
echo -e "\n${BLUE}Creating Nginx configuration...${NC}"
NGINX_CONF="/etc/nginx/sites-available/upwork-generator"

cat > "$NGINX_CONF" << EOF
server {
    listen ${PROXY_PORT};
    server_name ${DOMAIN} ${SERVER_IP};

    access_log /var/log/nginx/upwork-generator-access.log;
    error_log /var/log/nginx/upwork-generator-error.log;

    location / {
        proxy_pass http://localhost:${SERVER_PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Don't buffer responses
        proxy_buffering off;
        
        # Set timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

echo -e "${GREEN}✅ Created Nginx configuration${NC}"

# Enable the site
echo -e "\n${BLUE}Enabling the site...${NC}"
if [ ! -f /etc/nginx/sites-enabled/upwork-generator ]; then
    ln -s "$NGINX_CONF" /etc/nginx/sites-enabled/
    echo -e "${GREEN}✅ Site enabled${NC}"
else
    echo -e "${YELLOW}⚠️ Site already enabled${NC}"
fi

# Test Nginx configuration
echo -e "\n${BLUE}Testing Nginx configuration...${NC}"
nginx -t
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Nginx configuration test failed${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Nginx configuration test passed${NC}"
fi

# Reload Nginx
echo -e "\n${BLUE}Reloading Nginx...${NC}"
systemctl reload nginx
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to reload Nginx${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Nginx reloaded successfully${NC}"
fi

# Add entry to /etc/hosts
echo -e "\n${BLUE}Adding entry to /etc/hosts...${NC}"
if ! grep -q "$DOMAIN" /etc/hosts; then
    echo "127.0.0.1 $DOMAIN" >> /etc/hosts
    echo -e "${GREEN}✅ Added $DOMAIN to /etc/hosts${NC}"
else
    echo -e "${YELLOW}⚠️ $DOMAIN already in /etc/hosts${NC}"
fi

# Create a test HTML file
echo -e "\n${BLUE}Creating test HTML file...${NC}"
TEST_HTML="/var/www/html/upwork-generator-test.html"

cat > "${TEST_HTML}" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Upwork Generator Access</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        .test-link { display: block; margin: 10px 0; padding: 10px; background: #f0f0f0; border-radius: 5px; }
        .test-link a { color: #0066cc; text-decoration: none; font-weight: bold; }
        .test-link a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Upwork Generator Access Options</h1>
    
    <div class="test-link">
        <a href="http://${SERVER_IP}" target="_blank">Via IP: http://${SERVER_IP}</a>
    </div>
    
    <div class="test-link">
        <a href="http://${DOMAIN}" target="_blank">Via Domain: http://${DOMAIN}</a>
    </div>
    
    <div class="test-link">
        <a href="http://${SERVER_IP}:${SERVER_PORT}" target="_blank">Direct (original port): http://${SERVER_IP}:${SERVER_PORT}</a>
    </div>
    
    <p>If you can't access the server, please try the troubleshooting steps:</p>
    <ol>
        <li>Ensure you're on the same network as the server</li>
        <li>Try pinging the server: <code>ping ${SERVER_IP}</code></li>
        <li>Add an entry to your hosts file: <code>${SERVER_IP} ${DOMAIN}</code></li>
        <li>Try using SSH tunneling: <code>ssh -L ${SERVER_PORT}:localhost:${SERVER_PORT} root@${SERVER_IP}</code></li>
    </ol>
</body>
</html>
EOF

echo -e "${GREEN}✅ Created test HTML file at ${TEST_HTML}${NC}"

echo -e "\n${GREEN}===== Setup Complete =====${NC}"
echo -e "You can now access the Upwork Proposal Generator at:"
echo -e "  🌐 http://${SERVER_IP}"
echo -e "  🌐 http://${DOMAIN} (if you add to your hosts file)"
echo -e "  🌐 http://${SERVER_IP}:${SERVER_PORT} (original)"
echo -e "\nTest page: http://${SERVER_IP}/upwork-generator-test.html" 