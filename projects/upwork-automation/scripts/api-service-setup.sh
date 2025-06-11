#!/bin/bash

# Setup script for the Upwork Proposal API Service
# This installs Flask, sets up a systemd service, and updates the dashboard

echo "🚀 Setting up Upwork Proposal API Service"
echo "========================================"

# 1. Install dependencies
echo "📦 Installing required packages..."
pip install flask gunicorn

# 2. Create a systemd service file
echo "🔧 Creating systemd service..."
SERVICE_FILE="/etc/systemd/system/upwork-proposal-api.service"

cat > $SERVICE_FILE << EOL
[Unit]
Description=Upwork Proposal API Service
After=network.target

[Service]
User=root
WorkingDirectory=/root/homelab-docs/scripts/upwork-automation
ExecStart=/usr/bin/python3 /root/homelab-docs/scripts/upwork-automation/api-server.py
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=upwork-proposal-api
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

# 3. Reload systemd, enable and start the service
echo "🔄 Starting the service..."
systemctl daemon-reload
systemctl enable upwork-proposal-api
systemctl start upwork-proposal-api

# 4. Configure nginx to proxy the API
echo "🌐 Configuring nginx..."
NGINX_CONF="/etc/nginx/sites-available/proposal-api.conf"

cat > $NGINX_CONF << EOL
server {
    listen 80;
    server_name api.projekt-ai.net;

    location / {
        proxy_pass http://localhost:5050;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Add proper CORS headers
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
        
        # Cache control
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }
}
EOL

# Create symbolic link to enable the site
ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 5. Update the dashboard HTML to use the API
echo "🔄 Updating the dashboard..."
DASHBOARD_HTML="/var/www/projekt-ai.net/upwork-dashboard.html"
TIMESTAMP=$(date +%s)

# Backup the original file
cp $DASHBOARD_HTML "${DASHBOARD_HTML}.bak-${TIMESTAMP}"

# Update the API endpoint in the dashboard
sed -i "s|https://projekt-ai.net/data/proposals.json|https://api.projekt-ai.net/api/proposals|g" $DASHBOARD_HTML
sed -i "s|https://projekt-ai.net/data/proposals-[0-9]*.json|https://api.projekt-ai.net/api/proposals|g" $DASHBOARD_HTML

# 6. Create a test HTML file to verify the API
echo "🔍 Creating test page..."
TEST_HTML="/var/www/projekt-ai.net/api-test.html"

cat > $TEST_HTML << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>API Test Page</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 1200px; margin: 0 auto; }
        .proposal { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .controls { margin: 20px 0; }
        button { padding: 10px 15px; margin-right: 10px; cursor: pointer; }
        #status { padding: 10px; margin: 10px 0; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        h1 { color: #333; }
        .proposal-count { font-size: 18px; font-weight: bold; margin: 20px 0; }
        .cache-info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        pre { background: #f5f5f5; padding: 10px; border-radius: 5px; overflow: auto; }
    </style>
</head>
<body>
    <h1>API Test Page</h1>
    <div class="cache-info">
        <p><strong>API Information:</strong></p>
        <ul>
            <li>This page tests the new proposals API endpoint</li>
            <li>The API includes proper cache headers</li>
            <li>Responses include version and timestamp</li>
        </ul>
    </div>
    
    <div class="controls">
        <button onclick="loadProposals()">Load Proposals from API</button>
        <button onclick="checkHealth()">Check API Health</button>
        <button onclick="clearOutput()">Clear Results</button>
    </div>
    
    <div id="status"></div>
    <div id="output"></div>
    
    <script>
        // Load proposals from API
        async function loadProposals() {
            const status = document.getElementById('status');
            const output = document.getElementById('output');
            
            status.innerHTML = 'Loading...';
            status.className = '';
            
            try {
                // Add cache-busting query parameter
                const timestamp = Date.now();
                const url = \`https://api.projekt-ai.net/api/proposals?_=\${timestamp}\`;
                
                console.log('Loading from:', url);
                
                const response = await fetch(url, {
                    cache: 'no-store',
                    headers: {
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0'
                    }
                });
                
                if (!response.ok) {
                    throw new Error(\`HTTP error \${response.status}\`);
                }
                
                const data = await response.json();
                
                status.innerHTML = \`✅ Successfully loaded data\`;
                status.className = 'success';
                
                // Display JSON data
                output.innerHTML = \`
                    <div class="proposal-count">
                        <p><strong>Total count in API response:</strong> \${data.total_count}</p>
                        <p><strong>Actual proposals count:</strong> \${data.proposals ? data.proposals.length : 0}</p>
                        <p><strong>Generated at:</strong> \${data.generated_at}</p>
                        <p><strong>Version:</strong> \${data.version}</p>
                    </div>
                    <h3>Response Headers:</h3>
                    <pre>\${formatHeaders(response.headers)}</pre>
                    <h3>First 3 Proposals:</h3>
                    <pre>\${JSON.stringify(data.proposals.slice(0, 3), null, 2)}</pre>
                \`;
                
            } catch (error) {
                status.innerHTML = \`❌ Error: \${error.message}\`;
                status.className = 'error';
                console.error('Failed to load proposals:', error);
            }
        }
        
        // Check API health
        async function checkHealth() {
            const status = document.getElementById('status');
            const output = document.getElementById('output');
            
            status.innerHTML = 'Checking API health...';
            status.className = '';
            
            try {
                const response = await fetch('https://api.projekt-ai.net/api/health', {
                    cache: 'no-store'
                });
                
                if (!response.ok) {
                    throw new Error(\`HTTP error \${response.status}\`);
                }
                
                const data = await response.json();
                
                status.innerHTML = \`✅ API is healthy\`;
                status.className = 'success';
                
                output.innerHTML = \`
                    <h3>Health Check Result:</h3>
                    <pre>\${JSON.stringify(data, null, 2)}</pre>
                    <h3>Response Headers:</h3>
                    <pre>\${formatHeaders(response.headers)}</pre>
                \`;
                
            } catch (error) {
                status.innerHTML = \`❌ Error: \${error.message}\`;
                status.className = 'error';
                console.error('Failed to check API health:', error);
            }
        }
        
        // Format response headers
        function formatHeaders(headers) {
            let result = '';
            for (const [key, value] of headers.entries()) {
                result += \`\${key}: \${value}\n\`;
            }
            return result;
        }
        
        // Clear output
        function clearOutput() {
            document.getElementById('status').innerHTML = '';
            document.getElementById('status').className = '';
            document.getElementById('output').innerHTML = '';
        }
    </script>
</body>
</html>
EOL

chmod 644 $TEST_HTML

# 7. Add DNS record instructions
echo ""
echo "========================================"
echo "🎉 API Service setup completed!"
echo "========================================"
echo ""
echo "🔸 To complete the setup, add this DNS record in Cloudflare:"
echo "  Type: A"
echo "  Name: api"
echo "  Content: $(curl -s ifconfig.me)"
echo "  Proxy status: Proxied"
echo ""
echo "🔸 Then you can access:"
echo "  • API Endpoint: https://api.projekt-ai.net/api/proposals"
echo "  • Health Check: https://api.projekt-ai.net/api/health"
echo "  • Test Page: https://projekt-ai.net/api-test.html"
echo ""
echo "🔸 Service Status:"
echo "  systemctl status upwork-proposal-api"
echo ""
echo "🔸 To view logs:"
echo "  journalctl -u upwork-proposal-api -f"
echo ""
echo "✅ Setup completed successfully!" 