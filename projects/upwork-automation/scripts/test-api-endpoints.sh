#!/bin/bash

# Test API Endpoints for Upwork Automation System
# Tests the API endpoints in the test environment
# Created: June 3, 2025

# Color codes for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEST_API_PORT=5052
TEST_API_URL="http://localhost:${TEST_API_PORT}"
TEST_API_DOMAIN="https://test-api.projekt-ai.net"
TEST_PAGES_DOMAIN="https://test-pages.projekt-ai.net"

print_header() {
  echo ""
  echo -e "${BLUE}===============================================${NC}"
  echo -e "${BLUE}  $1${NC}"
  echo -e "${BLUE}===============================================${NC}"
  echo ""
}

print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
  echo -e "${RED}❌ $1${NC}"
}

print_info() {
  echo -e "${YELLOW}ℹ️ $1${NC}"
}

# Start testing
print_header "UPWORK AUTOMATION TEST API TESTING"
print_info "Testing API endpoints in test environment"
echo "Date: $(date)"
echo ""

# Test 1: Check if test port is listening
print_header "Test 1: Check if port ${TEST_API_PORT} is listening"
if netstat -tuln | grep -q ":${TEST_API_PORT} "; then
  print_success "Port ${TEST_API_PORT} is listening"
else
  print_error "Port ${TEST_API_PORT} is not listening"
  print_info "Attempting to check if the service is running..."
  systemctl status upwork-proposal-api-test
fi

# Test 2: Test local API health endpoint
print_header "Test 2: Test local API health endpoint"
health_response=$(curl -s "${TEST_API_URL}/api/health")
if [[ $? -eq 0 ]] && [[ "${health_response}" == *"ok"* ]]; then
  print_success "Local API health endpoint is responding correctly"
  echo "Response:"
  echo "${health_response}" | python3 -m json.tool
else
  print_error "Local API health endpoint is not responding correctly"
  echo "Response: ${health_response}"
fi

# Test 3: Test local API proposals endpoint
print_header "Test 3: Test local API proposals endpoint"
proposals_response=$(curl -s "${TEST_API_URL}/api/proposals")
if [[ $? -eq 0 ]] && [[ "${proposals_response}" == *"proposals"* ]]; then
  # Extract and display the count of proposals
  proposals_count=$(echo "${proposals_response}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_count', 0))")
  print_success "Local API proposals endpoint is responding correctly with ${proposals_count} proposals"
else
  print_error "Local API proposals endpoint is not responding correctly"
  echo "Response: ${proposals_response}"
fi

# Test 4: Test domain API health endpoint
print_header "Test 4: Test domain API health endpoint"
domain_health_response=$(curl -s "${TEST_API_DOMAIN}/api/health")
if [[ $? -eq 0 ]] && [[ "${domain_health_response}" == *"ok"* ]]; then
  print_success "Domain API health endpoint is responding correctly"
  echo "Response:"
  echo "${domain_health_response}" | python3 -m json.tool
else
  print_error "Domain API health endpoint is not responding correctly"
  echo "Response: ${domain_health_response}"
fi

# Test 5: Test domain API proposals endpoint
print_header "Test 5: Test domain API proposals endpoint"
domain_proposals_response=$(curl -s "${TEST_API_DOMAIN}/api/proposals")
if [[ $? -eq 0 ]] && [[ "${domain_proposals_response}" == *"proposals"* ]]; then
  # Extract and display the count of proposals
  domain_proposals_count=$(echo "${domain_proposals_response}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_count', 0))")
  print_success "Domain API proposals endpoint is responding correctly with ${domain_proposals_count} proposals"
else
  print_error "Domain API proposals endpoint is not responding correctly"
  echo "Response: ${domain_proposals_response}"
fi

# Test 6: Verify CORS headers
print_header "Test 6: Verify CORS headers"
cors_headers=$(curl -s -I "${TEST_API_DOMAIN}/api/proposals" | grep -i "Access-Control-Allow")
if [[ -n "${cors_headers}" ]]; then
  print_success "CORS headers are set correctly"
  echo "${cors_headers}"
else
  print_error "CORS headers are missing"
fi

# Test 7: Verify cache control headers
print_header "Test 7: Verify cache control headers"
cache_headers=$(curl -s -I "${TEST_API_DOMAIN}/api/proposals" | grep -i "Cache\|Pragma\|Expires")
if [[ -n "${cache_headers}" ]]; then
  print_success "Cache control headers are set correctly"
  echo "${cache_headers}"
else
  print_error "Cache control headers are missing"
fi

# Test 8: Check test pages domain
print_header "Test 8: Check test pages domain"
test_page_response=$(curl -s -I "${TEST_PAGES_DOMAIN}/api-test-safe.html" | head -1)
if [[ "${test_page_response}" == *"200 OK"* ]]; then
  print_success "Test pages domain is accessible"
  print_info "API test page: ${TEST_PAGES_DOMAIN}/api-test-safe.html"
  print_info "Test dashboard: ${TEST_PAGES_DOMAIN}/upwork-dashboard-test.html"
else
  print_error "Test pages domain is not accessible"
  echo "Response: ${test_page_response}"
fi

# Summary of testing
print_header "TESTING SUMMARY"

if netstat -tuln | grep -q ":${TEST_API_PORT} " && 
   [[ "${health_response}" == *"ok"* ]] &&
   [[ "${proposals_response}" == *"proposals"* ]] &&
   [[ "${domain_health_response}" == *"ok"* ]] &&
   [[ "${domain_proposals_response}" == *"proposals"* ]]; then
  print_success "All API tests passed successfully!"
  echo ""
  echo -e "${BLUE}TEST API ENDPOINTS:${NC}"
  echo "  • Health: ${TEST_API_DOMAIN}/api/health"
  echo "  • Proposals: ${TEST_API_DOMAIN}/api/proposals"
  echo ""
  echo -e "${BLUE}TEST PAGES:${NC}"
  echo "  • API Test Page: ${TEST_PAGES_DOMAIN}/api-test-safe.html"
  echo "  • Test Dashboard: ${TEST_PAGES_DOMAIN}/upwork-dashboard-test.html"
else
  print_error "Some API tests failed"
  echo ""
  echo -e "${YELLOW}TROUBLESHOOTING:${NC}"
  echo "1. Check if the test API service is running:"
  echo "   systemctl status upwork-proposal-api-test"
  echo ""
  echo "2. Check the logs:"
  echo "   journalctl -u upwork-proposal-api-test -f"
  echo "   cat /root/homelab-docs/scripts/upwork-automation/api-server.log"
  echo ""
  echo "3. Check Nginx configuration:"
  echo "   nginx -t"
  echo "   cat /etc/nginx/sites-available/test-api.projekt-ai.net"
  echo "   cat /etc/nginx/sites-available/test-pages.projekt-ai.net"
fi

echo "" 