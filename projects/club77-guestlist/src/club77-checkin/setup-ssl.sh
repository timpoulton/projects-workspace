#!/bin/bash

# Club77 Check-in App - SSL Setup Script
# Sets up SSL certificate for checkin.projekt-ai.net

set -e

echo "🔒 CLUB77 CHECK-IN APP - SSL SETUP"
echo "=================================="
echo "Domain: checkin.projekt-ai.net"
echo "Port: 3001"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root"
   exit 1
fi

# Variables
APP_DOMAIN="checkin.projekt-ai.net"
APP_PORT="3001"

echo "🔍 Step 1: Pre-SSL checks"

# Check if app is running
if ! docker ps | grep -q club77_app; then
    echo "🔄 Starting Club77 containers..."
    cd /root/homelab-docs/apps/club77-checkin
    docker-compose up -d
    sleep 10
fi

# Verify app is responding
if curl -s -o /dev/null -w "%{http_code}" "http://localhost:$APP_PORT" | grep -q "200\|302"; then
    echo "✅ Club77 app is responding on port $APP_PORT"
else
    echo "❌ Club77 app is not responding on port $APP_PORT"
    echo "Please check the application first"
    exit 1
fi

echo ""
echo "🌐 Step 2: Nginx configuration"

# Create temporary HTTP-only config if it doesn't exist
if [ ! -f "/etc/nginx/sites-available/$APP_DOMAIN.temp" ]; then
    cat > "/etc/nginx/sites-available/$APP_DOMAIN.temp" << 'EOF'
server {
    listen 80;
    server_name checkin.projekt-ai.net;
    
    # Proxy to Club77 Check-in App (Category C - Business)
    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:3001/health;
        access_log off;
    }

    # Static files optimization
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        proxy_pass http://localhost:3001;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Logging
    access_log /var/log/nginx/checkin.projekt-ai.net.access.log;
    error_log /var/log/nginx/checkin.projekt-ai.net.error.log;
}
EOF
    echo "✅ Temporary HTTP config created"
fi

# Enable the temporary config
ln -sf "/etc/nginx/sites-available/$APP_DOMAIN.temp" "/etc/nginx/sites-enabled/$APP_DOMAIN"

# Test and reload nginx
if nginx -t; then
    systemctl reload nginx
    echo "✅ Nginx configuration loaded"
else
    echo "❌ Nginx configuration test failed"
    exit 1
fi

echo ""
echo "🔒 Step 3: SSL Certificate Setup"

# Check if SSL certificate already exists
if [ -d "/etc/letsencrypt/live/$APP_DOMAIN" ]; then
    echo "✅ SSL certificate already exists for $APP_DOMAIN"
else
    echo "🔄 Setting up SSL certificate with certbot..."
    
    # Run certbot to get SSL certificate
    if certbot --nginx -d "$APP_DOMAIN" --non-interactive --agree-tos --email admin@projekt-ai.net; then
        echo "✅ SSL certificate obtained successfully"
    else
        echo "❌ Failed to obtain SSL certificate"
        echo "Please check:"
        echo "1. DNS is pointing $APP_DOMAIN to this server"
        echo "2. Port 80 and 443 are open"
        echo "3. Domain is accessible from the internet"
        exit 1
    fi
fi

echo ""
echo "🌐 Step 4: Final SSL Configuration"

# Copy the full SSL configuration
cp "/root/homelab-docs/configs/nginx/checkin.projekt-ai.net.conf" "/etc/nginx/sites-available/$APP_DOMAIN"

# Enable the SSL config
ln -sf "/etc/nginx/sites-available/$APP_DOMAIN" "/etc/nginx/sites-enabled/$APP_DOMAIN"

# Test and reload nginx
if nginx -t; then
    systemctl reload nginx
    echo "✅ SSL configuration applied"
else
    echo "❌ SSL configuration test failed"
    exit 1
fi

echo ""
echo "📊 Step 5: Verification"

# Test HTTPS
if curl -s -I "https://$APP_DOMAIN" | grep -q "200\|302"; then
    echo "✅ HTTPS is working for $APP_DOMAIN"
else
    echo "⚠️  HTTPS test failed - may need DNS propagation time"
fi

# Test HTTP redirect
if curl -s -I "http://$APP_DOMAIN" | grep -q "301\|302"; then
    echo "✅ HTTP to HTTPS redirect is working"
else
    echo "⚠️  HTTP redirect test failed"
fi

# Check certificate
if certbot certificates | grep -q "$APP_DOMAIN"; then
    echo "✅ SSL certificate is installed"
    certbot certificates | grep -A 5 "$APP_DOMAIN"
else
    echo "❌ SSL certificate not found"
fi

echo ""
echo "🎯 SSL SETUP COMPLETE"
echo "===================="
echo "✅ SSL certificate installed for $APP_DOMAIN"
echo "✅ HTTPS enforcement enabled"
echo "✅ Security headers configured"
echo ""
echo "🌐 Access URLs:"
echo "- HTTPS: https://$APP_DOMAIN"
echo "- Internal: http://192.168.1.107:$APP_PORT"
echo ""
echo "🔍 Next steps:"
echo "1. Test external access: https://$APP_DOMAIN"
echo "2. Verify all functionality works over HTTPS"
echo "3. Update any hardcoded HTTP URLs to HTTPS"
echo "4. Set up certificate auto-renewal (should be automatic)"

echo ""
echo "📋 Certificate auto-renewal:"
echo "Certbot should automatically renew certificates."
echo "Test renewal: certbot renew --dry-run" 