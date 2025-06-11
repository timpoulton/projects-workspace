#!/bin/bash

# Script to update the Upwork Generator setup with the new port number
# This script updates Nginx configuration and documentation to point to port 5056

echo "🔄 Updating Upwork Generator Setup (Port 5055 → 5056)"

# Directory where the scripts are located
SCRIPT_DIR="/root/homelab-docs/scripts/upwork-automation"
OLD_PORT=5055
NEW_PORT=5056

# Update Nginx configuration
echo "📝 Updating Nginx configuration..."
if [ -f "/etc/nginx/sites-available/upwork-generator" ]; then
    sudo sed -i "s/proxy_pass http:\/\/localhost:$OLD_PORT;/proxy_pass http:\/\/localhost:$NEW_PORT;/g" /etc/nginx/sites-available/upwork-generator
    sudo systemctl reload nginx
    echo "✅ Nginx configuration updated"
else
    echo "⚠️ Nginx configuration file not found. Will create it now."
    # Create Nginx configuration
    sudo bash -c "cat > /etc/nginx/sites-available/upwork-generator << 'EOL'
server {
    listen 80;
    server_name 192.168.1.107 upwork-generator.local;

    location / {
        proxy_pass http://localhost:$NEW_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL"

    # Enable the site
    if [ ! -f "/etc/nginx/sites-enabled/upwork-generator" ]; then
        sudo ln -s /etc/nginx/sites-available/upwork-generator /etc/nginx/sites-enabled/
    fi
    
    sudo systemctl reload nginx
    echo "✅ New Nginx configuration created and enabled"
fi

# Update access scripts
echo "📝 Updating access scripts..."
for script in "$SCRIPT_DIR/access-generator.sh" "$SCRIPT_DIR/check-server-access.sh" "$SCRIPT_DIR/setup-server-proxy.sh"; do
    if [ -f "$script" ]; then
        sed -i "s/SERVER_PORT=$OLD_PORT/SERVER_PORT=$NEW_PORT/g" "$script"
        echo "✅ Updated $script"
    fi
done

# Update HTML files
echo "📝 Updating HTML files..."
for html in "$SCRIPT_DIR/dashboard.html" "$SCRIPT_DIR/test-dashboard.html"; do
    if [ -f "$html" ]; then
        sed -i "s/:$OLD_PORT/:$NEW_PORT/g" "$html"
        echo "✅ Updated $html"
    fi
done

# Update documentation files
echo "📝 Updating documentation files..."
for doc in "$SCRIPT_DIR/README-ACCESS-SOLUTION.md" "$SCRIPT_DIR/UPWORK-GENERATOR-ACCESS-GUIDE.md"; do
    if [ -f "$doc" ]; then
        sed -i "s/:$OLD_PORT/:$NEW_PORT/g" "$doc"
        echo "✅ Updated $doc"
    fi
done

# Create a symbolic link to the complete documentation
if [ -f "$SCRIPT_DIR/UPWORK-GENERATOR-COMPLETE-DOCUMENTATION.md" ]; then
    echo "📝 Creating symbolic link to documentation in /var/www/html..."
    sudo ln -sf "$SCRIPT_DIR/UPWORK-GENERATOR-COMPLETE-DOCUMENTATION.md" "/var/www/html/upwork-generator-docs.md"
    echo "✅ Documentation link created"
fi

# Restart the generator with the new port
echo "🔄 Restarting the Upwork Generator..."
pkill -f "simple-upwork-generator.py"
cd "$SCRIPT_DIR" && ./run-simple-generator.sh > /dev/null 2>&1 &
echo "✅ Upwork Generator restarted on port $NEW_PORT"

echo "📋 Summary of changes:"
echo "  - Updated Nginx to proxy from port 80 to port $NEW_PORT"
echo "  - Updated all access scripts to use port $NEW_PORT"
echo "  - Updated HTML dashboards to link to port $NEW_PORT"
echo "  - Updated documentation to reference port $NEW_PORT"
echo "  - Restarted the Upwork Generator on port $NEW_PORT"
echo ""
echo "🌐 The Upwork Generator is now accessible at:"
echo "  - http://192.168.1.107 (via Nginx proxy)"
echo "  - http://192.168.1.107:$NEW_PORT (direct port access)"
echo "  - http://localhost:$NEW_PORT (from the server)"
echo ""
echo "✅ Setup update complete!"

# Make the script executable
chmod +x "$0" 