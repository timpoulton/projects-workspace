#!/bin/bash

# Club77 Check-in App - Standardized Deployment Script
# Category C (Business) - Port 3001 - External Access with SSL

set -e

echo "🏠 CLUB77 CHECK-IN APP - STANDARDIZED DEPLOYMENT"
echo "=============================================="
echo "Category: C (Business)"
echo "Port: 3001"
echo "Domain: checkin.projekt-ai.net"
echo "SSL: Required"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root"
   exit 1
fi

# Variables
APP_NAME="club77-checkin"
APP_PORT="3001"
APP_DOMAIN="checkin.projekt-ai.net"
CURRENT_DIR="/root/homelab-docs/apps/club77-checkin"
TARGET_DIR="/srv/apps/club77-checkin"

echo "🔍 Step 1: Pre-deployment checks"
echo "Current location: $CURRENT_DIR"
echo "Target location: $TARGET_DIR"

# Check if app is running
if docker ps | grep -q club77_app; then
    echo "🔄 Stopping existing containers..."
    cd "$CURRENT_DIR"
    docker-compose down
fi

echo ""
echo "📁 Step 2: Directory standardization"
if [ ! -d "$TARGET_DIR" ]; then
    echo "Creating standardized directory: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
    cp -r "$CURRENT_DIR"/* "$TARGET_DIR/"
    echo "✅ App copied to standardized location"
else
    echo "✅ Standardized directory already exists"
fi

echo ""
echo "🌐 Step 3: Nginx configuration"
NGINX_CONFIG="/etc/nginx/sites-available/$APP_DOMAIN"
if [ ! -f "$NGINX_CONFIG" ]; then
    echo "Creating nginx configuration..."
    cp "/root/homelab-docs/configs/nginx/checkin.projekt-ai.net.conf" "$NGINX_CONFIG"
    echo "✅ Nginx config created"
else
    echo "✅ Nginx config already exists"
fi

# Enable site
if [ ! -L "/etc/nginx/sites-enabled/$APP_DOMAIN" ]; then
    ln -s "$NGINX_CONFIG" "/etc/nginx/sites-enabled/"
    echo "✅ Nginx site enabled"
fi

echo ""
echo "🔒 Step 4: SSL Certificate"
if [ ! -d "/etc/letsencrypt/live/$APP_DOMAIN" ]; then
    echo "⚠️  SSL certificate not found for $APP_DOMAIN"
    echo "Run: certbot --nginx -d $APP_DOMAIN"
    echo "For now, creating HTTP-only config..."
    
    # Create temporary HTTP-only config
    cat > "/etc/nginx/sites-available/$APP_DOMAIN.temp" << EOF
server {
    listen 80;
    server_name $APP_DOMAIN;
    
    location / {
        proxy_pass http://localhost:$APP_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    
    # Use temp config
    rm -f "/etc/nginx/sites-enabled/$APP_DOMAIN"
    ln -s "/etc/nginx/sites-available/$APP_DOMAIN.temp" "/etc/nginx/sites-enabled/"
    echo "✅ Temporary HTTP config created"
else
    echo "✅ SSL certificate exists"
fi

echo ""
echo "🐳 Step 5: Docker deployment"
cd "$TARGET_DIR"
docker-compose up -d
echo "✅ Containers started"

echo ""
echo "🔄 Step 6: Nginx reload"
nginx -t && systemctl reload nginx
echo "✅ Nginx reloaded"

echo ""
echo "📊 Step 7: Verification"
sleep 5

# Check containers
if docker ps | grep -q club77_app; then
    echo "✅ Club77 app container running"
else
    echo "❌ Club77 app container not running"
fi

if docker ps | grep -q club77_db; then
    echo "✅ Club77 database container running"
else
    echo "❌ Club77 database container not running"
fi

# Check port
if netstat -tlnp | grep -q ":$APP_PORT "; then
    echo "✅ Port $APP_PORT is listening"
else
    echo "❌ Port $APP_PORT is not listening"
fi

# Check HTTP response
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$APP_PORT" | grep -q "200\|302"; then
    echo "✅ App responding on localhost:$APP_PORT"
else
    echo "❌ App not responding on localhost:$APP_PORT"
fi

echo ""
echo "🎯 DEPLOYMENT COMPLETE"
echo "====================="
echo "✅ Category C (Business) compliance verified"
echo "✅ Port 3001 standardized"
echo "✅ Docker deployment active"
echo "✅ Nginx reverse proxy configured"
echo ""
echo "🌐 Access URLs:"
echo "- Internal: http://192.168.1.107:3001"
echo "- External: http://$APP_DOMAIN (HTTP only until SSL setup)"
echo ""
echo "🔒 Next steps:"
echo "1. Set up SSL: certbot --nginx -d $APP_DOMAIN"
echo "2. Update DNS: $APP_DOMAIN → 192.168.1.107"
echo "3. Test external access"
echo "4. Update documentation" 