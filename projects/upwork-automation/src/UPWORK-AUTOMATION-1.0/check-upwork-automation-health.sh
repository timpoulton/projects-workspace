#!/bin/bash
# Upwork Automation System Health Check
# Checks all components of the Upwork proposal automation system
# Usage: ./check-upwork-automation-health.sh

echo "===== UPWORK AUTOMATION SYSTEM HEALTH CHECK ====="
echo "Started at $(date)"
echo

# Define components and ports
AI_SERVER_PORT=5001
API_SERVER_PORT=5050
NGINX_CONFIG="/etc/nginx/sites-available/upwork-proposal-api.conf"
CLOUDFLARE_DOMAIN="api.projekt-ai.net"
SERVER_IP="125.253.107.197"

# Check if AI server is running
echo "Checking Multi-Model AI server (Port $AI_SERVER_PORT)..."
if nc -z localhost $AI_SERVER_PORT; then
    echo "✅ Multi-Model AI server is running on port $AI_SERVER_PORT"
else
    echo "❌ Multi-Model AI server is NOT running on port $AI_SERVER_PORT"
fi

# Check if API server is running
echo -e "\nChecking API server (Port $API_SERVER_PORT)..."
if nc -z localhost $API_SERVER_PORT; then
    echo "✅ API server is running on port $API_SERVER_PORT"
else
    echo "❌ API server is NOT running on port $API_SERVER_PORT"
fi

# Check Nginx configuration
echo -e "\nChecking Nginx configuration..."
if [ -f "$NGINX_CONFIG" ]; then
    echo "✅ Nginx configuration file exists: $NGINX_CONFIG"
    
    # Check if SSL is configured
    if grep -q "ssl_certificate" "$NGINX_CONFIG"; then
        echo "✅ SSL is configured in Nginx"
    else
        echo "❌ SSL is NOT configured in Nginx"
    fi
    
    # Check if CORS is configured
    if grep -q "Access-Control-Allow-Origin" "$NGINX_CONFIG"; then
        echo "✅ CORS headers are configured in Nginx"
    else
        echo "❌ CORS headers are NOT configured in Nginx"
    fi
else
    echo "❌ Nginx configuration file does NOT exist: $NGINX_CONFIG"
fi

# Check if Nginx is running
echo -e "\nChecking if Nginx service is active..."
if systemctl is-active --quiet nginx; then
    echo "✅ Nginx service is running"
else
    echo "❌ Nginx service is NOT running"
fi

# Check DNS resolution
echo -e "\nChecking DNS resolution for $CLOUDFLARE_DOMAIN..."
RESOLVED_IP=$(dig +short $CLOUDFLARE_DOMAIN)
if [ -n "$RESOLVED_IP" ]; then
    echo "✅ Domain $CLOUDFLARE_DOMAIN resolves to $RESOLVED_IP"
    if [ "$RESOLVED_IP" = "$SERVER_IP" ]; then
        echo "✅ Domain resolves to the correct server IP"
    else
        echo "❌ Domain resolves to $RESOLVED_IP, but expected $SERVER_IP"
    fi
else
    echo "❌ Failed to resolve domain $CLOUDFLARE_DOMAIN"
fi

# Check API connectivity (local)
echo -e "\nChecking local API connectivity..."
LOCAL_API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$API_SERVER_PORT/api/proposals)
if [ "$LOCAL_API_RESPONSE" = "200" ]; then
    echo "✅ Local API is accessible (HTTP 200)"
else
    echo "❌ Local API returned HTTP $LOCAL_API_RESPONSE"
fi

# Check API connectivity (through Nginx)
echo -e "\nChecking API connectivity through Nginx..."
NGINX_API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/proposals)
if [ "$NGINX_API_RESPONSE" = "200" ]; then
    echo "✅ API through Nginx is accessible (HTTP 200)"
else
    echo "❌ API through Nginx returned HTTP $NGINX_API_RESPONSE"
fi

# Check external API connectivity
echo -e "\nChecking external API connectivity (may fail due to Cloudflare)..."
EXTERNAL_API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" https://$CLOUDFLARE_DOMAIN/api/proposals --insecure)
if [ "$EXTERNAL_API_RESPONSE" = "200" ]; then
    echo "✅ External API is accessible (HTTP 200)"
else
    echo "❌ External API returned HTTP $EXTERNAL_API_RESPONSE"
fi

# Check if proposals directory exists and is writable
PROPOSALS_DIR="/srv/apps/client-proposals/public/"
echo -e "\nChecking proposals directory..."
if [ -d "$PROPOSALS_DIR" ]; then
    echo "✅ Proposals directory exists: $PROPOSALS_DIR"
    if [ -w "$PROPOSALS_DIR" ]; then
        echo "✅ Proposals directory is writable"
    else
        echo "❌ Proposals directory is NOT writable"
    fi
else
    echo "❌ Proposals directory does NOT exist: $PROPOSALS_DIR"
fi

# Check if proposal queue file exists
QUEUE_FILE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
echo -e "\nChecking proposal queue file..."
if [ -f "$QUEUE_FILE" ]; then
    echo "✅ Proposal queue file exists: $QUEUE_FILE"
    # Check if queue file is valid JSON
    if jq empty "$QUEUE_FILE" 2>/dev/null; then
        echo "✅ Proposal queue file contains valid JSON"
    else
        echo "❌ Proposal queue file does NOT contain valid JSON"
    fi
else
    echo "❌ Proposal queue file does NOT exist: $QUEUE_FILE"
fi

# Check if the dashboard HTML file exists
DASHBOARD_FILE="/var/www/projekt-ai.net/upwork-dashboard.html"
echo -e "\nChecking dashboard file..."
if [ -f "$DASHBOARD_FILE" ]; then
    echo "✅ Dashboard file exists: $DASHBOARD_FILE"
else
    echo "❌ Dashboard file does NOT exist: $DASHBOARD_FILE"
fi

echo -e "\n===== HEALTH CHECK COMPLETE ====="
echo "Completed at $(date)"
echo
echo "Next steps if issues are found:"
echo "1. Restart AI server: systemctl restart upwork-proposal-server"
echo "2. Restart API server: systemctl restart upwork-api-server"
echo "3. Restart Nginx: systemctl restart nginx"
echo "4. Check logs: journalctl -u upwork-proposal-server -u upwork-api-server -u nginx"
echo "5. Check Cloudflare configuration in the dashboard" 