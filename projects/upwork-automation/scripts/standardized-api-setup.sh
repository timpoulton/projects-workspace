#!/bin/bash

# Standardized API Service Setup for Upwork Proposal System
# Following Project Standardization Guidelines
# Created: June 3, 2025

# Load common utilities and settings
source /root/homelab-docs/scripts/utility/common.sh 2>/dev/null || echo "Warning: Common utilities not found, continuing without them"

# Set standard logging format
log_info() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1"
}

log_error() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1" >&2
}

log_success() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [SUCCESS] $1"
}

# Configuration with standard paths
APP_NAME="upwork-proposal-api"
SERVICE_NAME="${APP_NAME}"
BASE_DIR="/root/homelab-docs"
SCRIPTS_DIR="${BASE_DIR}/scripts/upwork-automation"
WEB_DIR="/var/www/projekt-ai.net"
QUEUE_FILE="${SCRIPTS_DIR}/proposal-queue.json"
API_SERVER_FILE="${SCRIPTS_DIR}/api-server.py"
LOG_DIR="${SCRIPTS_DIR}/logs"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
NGINX_CONF="/etc/nginx/sites-available/${APP_NAME}.conf"
API_PORT=5050  # Category E (External APIs) per PORT-TRACKER.md
API_SUBDOMAIN="api.projekt-ai.net"
API_TEST_PAGE="${WEB_DIR}/api-test.html"
DASHBOARD_HTML="${WEB_DIR}/upwork-dashboard.html"

# Create log directory if it doesn't exist
mkdir -p "${LOG_DIR}"

# Main execution starts
log_info "Starting standardized API service setup"
log_info "Using standard paths and configurations"

# 1. Install dependencies
log_info "Installing required packages"
pip install flask gunicorn

# 2. Create systemd service file with standard format
log_info "Creating systemd service file at ${SERVICE_FILE}"
cat > "${SERVICE_FILE}" << EOL
[Unit]
Description=Upwork Proposal API Service
After=network.target

[Service]
User=root
WorkingDirectory=${SCRIPTS_DIR}
ExecStart=/usr/bin/python3 ${API_SERVER_FILE}
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=${SERVICE_NAME}
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

# 3. Configure nginx with standard best practices
log_info "Configuring nginx for API service"
cat > "${NGINX_CONF}" << EOL
server {
    listen 80;
    server_name ${API_SUBDOMAIN};

    # Standard logging configuration
    access_log /var/log/nginx/${APP_NAME}-access.log;
    error_log /var/log/nginx/${APP_NAME}-error.log;

    location / {
        # Standard proxy configuration
        proxy_pass http://localhost:${API_PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Standard CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        
        # Standard cache control
        add_header Cache-Control "no-cache, no-store, must-revalidate" always;
        add_header Pragma "no-cache" always;
        add_header Expires "0" always;
    }
}
EOL

# Create symbolic link to enable the site
ln -sf "${NGINX_CONF}" /etc/nginx/sites-enabled/

# 4. Create test page with standardized layout
log_info "Creating API test page at ${API_TEST_PAGE}"
cat > "${API_TEST_PAGE}" << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>API Test Page | Projekt AI</title>
    <link rel="icon" type="image/svg+xml" href="/assets/img/logos/favicon.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Standard Projekt AI styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            min-height: 100vh;
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        h1 { 
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 20px;
            color: #fff;
            letter-spacing: -0.02em;
        }
        h2 {
            font-size: 24px;
            font-weight: 600;
            margin: 30px 0 15px;
            color: #fff;
        }
        h3 {
            font-size: 18px;
            font-weight: 600;
            margin: 20px 0 10px;
            color: rgba(255, 255, 255, 0.9);
        }
        .card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .info-card {
            background: rgba(25, 118, 210, 0.05);
            border: 1px solid rgba(25, 118, 210, 0.2);
        }
        .success { 
            background: rgba(76, 175, 80, 0.1);
            border: 1px solid rgba(76, 175, 80, 0.3);
            color: #4CAF50;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        .error { 
            background: rgba(244, 67, 54, 0.1);
            border: 1px solid rgba(244, 67, 54, 0.3);
            color: #F44336;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        pre { 
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 8px;
            overflow: auto;
            font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.8);
            margin: 10px 0;
        }
        button {
            background: rgba(255, 255, 255, 0.05);
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        button:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
        }
        .primary-btn {
            background: rgba(25, 118, 210, 0.1);
            color: #1976D2;
            border-color: rgba(25, 118, 210, 0.3);
        }
        .primary-btn:hover {
            background: rgba(25, 118, 210, 0.2);
            border-color: rgba(25, 118, 210, 0.4);
        }
        .controls {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>API Test Page</h1>
        
        <div class="card info-card">
            <h3>API Information</h3>
            <ul>
                <li>This page tests the new proposals API endpoint</li>
                <li>The API includes proper cache headers</li>
                <li>Responses include version and timestamp</li>
            </ul>
        </div>
        
        <div class="controls">
            <button class="primary-btn" onclick="loadProposals()">Load Proposals from API</button>
            <button onclick="checkHealth()">Check API Health</button>
            <button onclick="clearOutput()">Clear Results</button>
        </div>
        
        <div id="status"></div>
        <div id="output"></div>
    </div>
    
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
                const url = \`https://${API_SUBDOMAIN}/api/proposals?_=\${timestamp}\`;
                
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
                    <div class="card">
                        <h2>API Response</h2>
                        <p><strong>Total count:</strong> \${data.total_count}</p>
                        <p><strong>Actual proposals:</strong> \${data.proposals ? data.proposals.length : 0}</p>
                        <p><strong>Generated at:</strong> \${data.generated_at}</p>
                        <p><strong>Version:</strong> \${data.version}</p>
                        
                        <h3>Response Headers</h3>
                        <pre>\${formatHeaders(response.headers)}</pre>
                        
                        <h3>First 3 Proposals</h3>
                        <pre>\${JSON.stringify(data.proposals.slice(0, 3), null, 2)}</pre>
                    </div>
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
                const response = await fetch(\`https://${API_SUBDOMAIN}/api/health\`, {
                    cache: 'no-store'
                });
                
                if (!response.ok) {
                    throw new Error(\`HTTP error \${response.status}\`);
                }
                
                const data = await response.json();
                
                status.innerHTML = \`✅ API is healthy\`;
                status.className = 'success';
                
                output.innerHTML = \`
                    <div class="card">
                        <h2>Health Check Result</h2>
                        <pre>\${JSON.stringify(data, null, 2)}</pre>
                        
                        <h3>Response Headers</h3>
                        <pre>\${formatHeaders(response.headers)}</pre>
                    </div>
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

chmod 644 "${API_TEST_PAGE}"

# 5. Update dashboard to use API endpoint
log_info "Updating dashboard to use API endpoint"
TIMESTAMP=$(date +%s)

# Backup dashboard file using standardized naming convention
BACKUP_FILE="${DASHBOARD_HTML}.bak-${TIMESTAMP}"
cp "${DASHBOARD_HTML}" "${BACKUP_FILE}"
log_info "Created backup of dashboard at ${BACKUP_FILE}"

# Update API endpoints in dashboard
sed -i "s|https://projekt-ai.net/data/proposals.json|https://${API_SUBDOMAIN}/api/proposals|g" "${DASHBOARD_HTML}"
sed -i "s|https://projekt-ai.net/data/proposals-[0-9]*.json|https://${API_SUBDOMAIN}/api/proposals|g" "${DASHBOARD_HTML}"

# 6. Start and enable the service
log_info "Testing nginx configuration"
if nginx -t; then
    log_info "Reloading nginx configuration"
    systemctl reload nginx
else
    log_error "Nginx configuration test failed"
    exit 1
fi

log_info "Enabling and starting API service"
systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

# Check if service started successfully
if systemctl is-active --quiet "${SERVICE_NAME}"; then
    log_success "API service started successfully"
else
    log_error "Failed to start API service"
    exit 1
fi

# Create a reference file for DNS setup
DNS_REFERENCE="${SCRIPTS_DIR}/dns-setup-${APP_NAME}.txt"
log_info "Creating DNS reference file at ${DNS_REFERENCE}"

cat > "${DNS_REFERENCE}" << EOL
# DNS Configuration for ${APP_NAME}
# Created: $(date '+%Y-%m-%d %H:%M:%S')

To complete the setup, add this DNS record in Cloudflare:

Type: A
Name: api
Content: $(curl -s ifconfig.me)
Proxy status: Proxied

# Additional Configuration
- Disable Rocket Loader for this subdomain
- Create a Cache Rule to bypass cache for the API subdomain
EOL

# Final output with standardized formatting
echo ""
echo "====================== SETUP COMPLETED ======================"
echo ""
log_success "API Service setup completed successfully"
echo ""
echo "API ENDPOINTS:"
echo "  • API: https://${API_SUBDOMAIN}/api/proposals"
echo "  • Health: https://${API_SUBDOMAIN}/api/health"
echo "  • Test Page: https://projekt-ai.net/api-test.html"
echo ""
echo "SERVICE MANAGEMENT:"
echo "  • Status: systemctl status ${SERVICE_NAME}"
echo "  • Logs: journalctl -u ${SERVICE_NAME} -f"
echo "  • Restart: systemctl restart ${SERVICE_NAME}"
echo ""
echo "DNS SETUP:"
echo "  • Instructions saved to: ${DNS_REFERENCE}"
echo ""
echo "=============================================================" 