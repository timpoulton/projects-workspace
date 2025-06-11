#!/bin/bash

echo "Setting up nginx for Club77 check-in app..."

# Create a simple nginx configuration
cat > /etc/nginx/conf.d/club77-checkin.conf << 'EOL'
server {
    listen 8081;
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

    access_log /var/log/nginx/club77-checkin.access.log;
    error_log /var/log/nginx/club77-checkin.error.log;
}
EOL

echo "Created nginx configuration at /etc/nginx/conf.d/club77-checkin.conf"

# Test nginx configuration
echo "Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Configuration test successful! Reloading nginx..."
    systemctl reload nginx
    echo "Nginx reloaded successfully."
    echo "Your app should now be accessible at: http://guestlist.club77.com.au:8081"
    
    # Check if port 8081 is already in use
    PORT_CHECK=$(netstat -tuln | grep :8081)
    if [ -n "$PORT_CHECK" ]; then
        echo "Warning: Port 8081 is already in use by another service!"
        echo "Port check: $PORT_CHECK"
    else
        echo "Port 8081 is available for nginx to use."
    fi
else
    echo "Configuration test failed. Nginx was not reloaded."
    echo "Please check the error messages above and fix the configuration."
fi

# Update the project documentation
cat > PORT-ACCESS.md << 'EOL'
# Club77 Check-in App Access

The Club77 check-in application is accessible at the following URLs:

## Internal Access
- http://localhost:3001 - Direct access to the Node.js application

## External Access
- http://guestlist.club77.com.au:8081 - Access via nginx reverse proxy

## Port Forwarding Requirements
To make the application accessible from outside your network:

1. Forward port 8081 on your EdgeRouter to 192.168.1.107:8081
2. Add a firewall rule to allow incoming traffic on port 8081

## Testing External Access
From outside your network, use:
```
curl http://guestlist.club77.com.au:8081
```

Or open the URL in a web browser.
EOL

echo "Created PORT-ACCESS.md documentation"
echo "Done! Remember to set up port forwarding on your router for port 8081." 