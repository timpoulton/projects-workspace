#!/bin/bash

echo "Updating nginx configuration for Club77 guest list app..."

# Create backup of existing nginx configurations
TIMESTAMP=$(date +%Y%m%d%H%M%S)
mkdir -p /etc/nginx/sites-enabled/backups
find /etc/nginx/sites-enabled/ -name "*guestlist*" -exec cp {} /etc/nginx/sites-enabled/backups/{}.$TIMESTAMP \;
echo "Created backup of existing configurations in /etc/nginx/sites-enabled/backups/"

# Create directory if it doesn't exist
mkdir -p /etc/nginx/sites-enabled/

# Create new configuration file for port 8080 (the port you expect users to access)
cat > /etc/nginx/sites-enabled/guestlist-port8080.club77.com.au << 'EOL'
server {
    listen 8080;
    server_name guestlist.club77.com.au;

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
    }

    access_log /var/log/nginx/guestlist-8080.club77.com.au.access.log;
    error_log /var/log/nginx/guestlist-8080.club77.com.au.error.log;
}
EOL

echo "Created new configuration for port 8080"

# Ensure the directory exists for logs
mkdir -p /var/log/nginx

# Test nginx configuration
echo "Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Configuration test successful! Reloading nginx..."
    systemctl reload nginx
    echo "Nginx reloaded successfully."
    echo "Your app should now be accessible at: http://guestlist.club77.com.au:8080"
else
    echo "Configuration test failed. Nginx was not reloaded."
    echo "Please check the error messages above and fix the configuration."
fi

# Make sure the Docker container is running
if ! docker ps | grep club77_app >/dev/null; then
    echo "Warning: The club77_app container doesn't appear to be running!"
    echo "Starting the container now..."
    cd /root/homelab-docs/club77-checkin && docker-compose up -d
else
    echo "The club77_app container is running properly."
    echo "The application should be accessible through nginx now."
fi

# Test the application is accessible
echo "Testing if the application is accessible..."
if curl -s localhost:3001 >/dev/null; then
    echo "✅ Application is accessible on port 3001!"
else
    echo "❌ Application is NOT accessible on port 3001."
    echo "Checking container logs for issues:"
    docker logs club77_app --tail 20
fi 