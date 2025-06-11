#!/bin/bash

# Verification Script for Upwork API Service
# Checks all components of the API setup to ensure proper operation
# Created: June 3, 2025

# Load common utilities
source /root/homelab-docs/scripts/utility/common.sh 2>/dev/null || {
  # Define minimal logging if common.sh is not available
  log_info() { echo "[INFO] $1"; }
  log_error() { echo "[ERROR] $1" >&2; }
  log_success() { echo "[SUCCESS] $1"; }
}

print_section() {
  echo ""
  echo "===================================================="
  echo "  $1"
  echo "===================================================="
  echo ""
}

# Configuration
API_SERVICE="upwork-proposal-api"
API_PORT=5050
API_URL="http://localhost:${API_PORT}"
NGINX_CONF="/etc/nginx/sites-available/${API_SERVICE}.conf"
SERVICE_FILE="/etc/systemd/system/${API_SERVICE}.service"
QUEUE_FILE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
API_SERVER_FILE="/root/homelab-docs/scripts/upwork-automation/api-server.py"
TEST_PAGE="/var/www/projekt-ai.net/api-test.html"

# Start verification
print_section "Upwork API Service Verification"
log_info "Starting verification of all API service components"

# Check if all required files exist
log_info "Checking required files..."
missing_files=0

check_file() {
  if [[ -f "$1" ]]; then
    echo "✅ $1 exists"
  else
    echo "❌ $1 is missing"
    missing_files=$((missing_files + 1))
  fi
}

check_file "${NGINX_CONF}"
check_file "${SERVICE_FILE}"
check_file "${QUEUE_FILE}"
check_file "${API_SERVER_FILE}"
check_file "${TEST_PAGE}"

if [[ ${missing_files} -gt 0 ]]; then
  log_error "${missing_files} required files are missing"
else
  log_success "All required files exist"
fi

# Check if service is running
log_info "Checking service status..."
if systemctl is-active --quiet "${API_SERVICE}"; then
  log_success "Service ${API_SERVICE} is running"
else
  log_error "Service ${API_SERVICE} is not running"
  systemctl status "${API_SERVICE}"
fi

# Check if port is listening
log_info "Checking if port ${API_PORT} is listening..."
if netstat -tuln | grep -q ":${API_PORT} "; then
  log_success "Port ${API_PORT} is listening"
else
  log_error "Port ${API_PORT} is not listening"
fi

# Check API health endpoint
log_info "Testing API health endpoint..."
health_response=$(curl -s "${API_URL}/api/health")
if [[ $? -eq 0 ]] && [[ "${health_response}" == *"ok"* ]]; then
  log_success "API health endpoint is responding correctly"
  echo "${health_response}" | python3 -m json.tool
else
  log_error "API health endpoint is not responding correctly"
  echo "Response: ${health_response}"
fi

# Check proposals endpoint
log_info "Testing API proposals endpoint..."
proposals_response=$(curl -s "${API_URL}/api/proposals")
if [[ $? -eq 0 ]] && [[ "${proposals_response}" == *"proposals"* ]]; then
  # Extract and display the count of proposals
  proposals_count=$(echo "${proposals_response}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_count', 0))")
  log_success "API proposals endpoint is responding correctly with ${proposals_count} proposals"
else
  log_error "API proposals endpoint is not responding correctly"
  echo "Response: ${proposals_response}"
fi

# Check nginx configuration
log_info "Verifying nginx configuration..."
if nginx -t 2>/dev/null; then
  log_success "Nginx configuration is valid"
else
  log_error "Nginx configuration has errors"
  nginx -t
fi

# Verify CORS headers
log_info "Testing CORS headers..."
cors_headers=$(curl -s -I "${API_URL}/api/proposals" | grep -i "Access-Control-Allow")
if [[ -n "${cors_headers}" ]]; then
  log_success "CORS headers are set correctly"
  echo "${cors_headers}"
else
  log_error "CORS headers are missing"
fi

# Verify cache control headers
log_info "Testing cache control headers..."
cache_headers=$(curl -s -I "${API_URL}/api/proposals" | grep -i "Cache\|Pragma\|Expires")
if [[ -n "${cache_headers}" ]]; then
  log_success "Cache control headers are set correctly"
  echo "${cache_headers}"
else
  log_error "Cache control headers are missing"
fi

# Summary of verification
print_section "Verification Summary"

if [[ ${missing_files} -eq 0 ]] && 
   systemctl is-active --quiet "${API_SERVICE}" &&
   netstat -tuln | grep -q ":${API_PORT} " &&
   [[ "${health_response}" == *"ok"* ]] &&
   [[ "${proposals_response}" == *"proposals"* ]]; then
  log_success "✅ API service is fully operational"
  echo ""
  echo "API ENDPOINTS:"
  echo "  • Health: ${API_URL}/api/health"
  echo "  • Proposals: ${API_URL}/api/proposals"
  echo ""
  echo "To access the API externally, use:"
  echo "  • https://api.projekt-ai.net/api/proposals"
  echo "  • https://api.projekt-ai.net/api/health"
  echo ""
  echo "Test page: https://projekt-ai.net/api-test.html"
else
  log_error "❌ API service has issues that need to be resolved"
  echo ""
  echo "NEXT STEPS:"
  echo "1. Review the errors above"
  echo "2. Fix any identified issues"
  echo "3. Run this verification script again"
  echo ""
  echo "For troubleshooting, check the logs:"
  echo "  • journalctl -u ${API_SERVICE} -f"
  echo "  • /root/homelab-docs/scripts/upwork-automation/api-server.log"
fi

echo "" 