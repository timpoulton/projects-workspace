#!/bin/bash

# SAFE API Service Setup for Upwork Proposal System
# Modified version that doesn't affect existing services
# Created: June 3, 2025

# Load common utilities and settings
source /root/homelab-docs/scripts/utility/common.sh 2>/dev/null || {
  # Define minimal logging if common.sh is not available
  log_info() { echo "[INFO] $1"; }
  log_error() { echo "[ERROR] $1" >&2; }
  log_success() { echo "[SUCCESS] $1"; }
}

# Configuration with modified settings for safe deployment
APP_NAME="upwork-proposal-api-test"  # Modified name to distinguish from production
SERVICE_NAME="${APP_NAME}"
BASE_DIR="/root/homelab-docs"
SCRIPTS_DIR="${BASE_DIR}/scripts/upwork-automation"
WEB_DIR="/var/www/projekt-ai.net"
QUEUE_FILE="${SCRIPTS_DIR}/proposal-queue.json"
API_SERVER_FILE="${SCRIPTS_DIR}/api-server-test.py"  # Using a different filename
LOG_DIR="${SCRIPTS_DIR}/logs"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
API_PORT=5052  # Using a different port for safety
API_TEST_PAGE="${WEB_DIR}/api-test-safe.html"  # Different test page

# Create backup directory
BACKUP_DIR="${SCRIPTS_DIR}/backups-$(date +%Y%m%d-%H%M%S)"
mkdir -p "${BACKUP_DIR}"
mkdir -p "${LOG_DIR}"

# Log the start of the safe setup
log_info "Starting SAFE API service setup (test mode)"
log_info "Using non-standard port ${API_PORT} to avoid conflicts"
log_info "Creating backups in ${BACKUP_DIR}"

# Backup critical files
cp "${SCRIPTS_DIR}/proposal-queue.json" "${BACKUP_DIR}/" 2>/dev/null || log_info "No proposal queue to backup"
cp "${WEB_DIR}/upwork-dashboard.html" "${BACKUP_DIR}/" 2>/dev/null || log_info "No dashboard to backup"

# Create a copy of the API server with modified port
log_info "Creating test version of API server"
cp "${SCRIPTS_DIR}/api-server.py" "${API_SERVER_FILE}"
sed -i "s/PORT = 5050/PORT = ${API_PORT}/" "${API_SERVER_FILE}"

# 1. Create systemd service file with unique name
log_info "Creating systemd service file at ${SERVICE_FILE}"
cat > "${SERVICE_FILE}" << EOL
[Unit]
Description=Upwork Proposal API Service (TEST MODE)
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

# 2. Create test page with modified endpoints
log_info "Creating API test page at ${API_TEST_PAGE}"
cat > "${API_TEST_PAGE}" << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAFE API Test Page | Projekt AI</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .notice {
            background-color: #fffacd;
            border: 1px solid #e6db55;
            padding: 10px 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            background: #f9f9f9;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }
        pre {
            background: #f1f1f1;
            padding: 10px;
            border-radius: 4px;
            overflow: auto;
            font-family: monospace;
        }
        .success { color: #4CAF50; }
        .error { color: #F44336; }
    </style>
</head>
<body>
    <h1>SAFE API Test Page (TEST MODE)</h1>
    
    <div class="notice">
        <strong>This is a TEST version of the API.</strong> 
        <p>This test API runs on port ${API_PORT} and will not affect your production system.</p>
    </div>
    
    <div class="card">
        <h2>API Information</h2>
        <ul>
            <li>Test API running on port ${API_PORT}</li>
            <li>Using the same proposal-queue.json data</li>
            <li>No changes to your dashboard or production system</li>
        </ul>
    </div>
    
    <div>
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
                const timestamp = Date.now();
                const url = \`http://localhost:${API_PORT}/api/proposals?_=\${timestamp}\`;
                
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
                        <p><strong>Version:</strong> \${data.version || 'N/A'}</p>
                        
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
                const response = await fetch(\`http://localhost:${API_PORT}/api/health\`, {
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

# 3. Create a test dashboard (copy of production)
TEST_DASHBOARD="${WEB_DIR}/upwork-dashboard-test.html"
if [ -f "${WEB_DIR}/upwork-dashboard.html" ]; then
    log_info "Creating test dashboard at ${TEST_DASHBOARD}"
    cp "${WEB_DIR}/upwork-dashboard.html" "${TEST_DASHBOARD}"
    
    # Update API endpoints in test dashboard
    sed -i "s|https://projekt-ai.net/data/proposals.json|http://localhost:${API_PORT}/api/proposals|g" "${TEST_DASHBOARD}"
    sed -i "s|https://projekt-ai.net/data/proposals-[0-9]*.json|http://localhost:${API_PORT}/api/proposals|g" "${TEST_DASHBOARD}"
else
    log_info "No dashboard found to create test version"
fi

# 4. Start the test service
log_info "Starting test API service"
systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

# Check if service started successfully
if systemctl is-active --quiet "${SERVICE_NAME}"; then
    log_success "Test API service started successfully"
else
    log_error "Failed to start test API service"
    exit 1
fi

# Create a rollback script
ROLLBACK_SCRIPT="${SCRIPTS_DIR}/rollback-test-api.sh"
log_info "Creating rollback script at ${ROLLBACK_SCRIPT}"

cat > "${ROLLBACK_SCRIPT}" << EOL
#!/bin/bash

echo "Rolling back test API changes..."

# Stop and disable the test service
systemctl stop ${SERVICE_NAME}
systemctl disable ${SERVICE_NAME}

# Remove test files
rm -f ${API_SERVER_FILE}
rm -f ${SERVICE_FILE}
rm -f ${API_TEST_PAGE}
rm -f ${TEST_DASHBOARD}

# Reload systemd
systemctl daemon-reload

echo "Rollback complete. Test API removed."
EOL

chmod +x "${ROLLBACK_SCRIPT}"

# Final output
echo ""
echo "====================== TEST SETUP COMPLETED ======================"
echo ""
log_success "SAFE Test API Service setup completed successfully"
echo ""
echo "TEST API ENDPOINTS:"
echo "  • API: http://localhost:${API_PORT}/api/proposals"
echo "  • Health: http://localhost:${API_PORT}/api/health"
echo ""
echo "TEST PAGES:"
echo "  • API Test Page: http://projekt-ai.net/api-test-safe.html"
echo "  • Test Dashboard: http://projekt-ai.net/upwork-dashboard-test.html"
echo ""
echo "ROLLBACK:"
echo "  • To remove test API: ${ROLLBACK_SCRIPT}"
echo ""
echo "NOTE: This test API will not affect your production system"
echo "      Once verified, you can proceed with the production deployment"
echo "=============================================================" 