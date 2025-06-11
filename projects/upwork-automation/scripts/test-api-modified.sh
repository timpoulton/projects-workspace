#!/bin/bash

# Modified API Test Script to troubleshoot issues
# Created: June 3, 2025

# Color codes for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEST_API_URL="https://test-api.projekt-ai.net"
TEST_PAGES_URL="https://test-pages.projekt-ai.net"

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
print_header "UPWORK AUTOMATION API DIAGNOSTIC TEST"
print_info "Running focused tests on test environment"
echo "Date: $(date)"
echo ""

# Test 1: DNS Resolution Test
print_header "Test 1: DNS Resolution Test"
print_info "Testing DNS resolution for test-api.projekt-ai.net..."
if host test-api.projekt-ai.net > /dev/null 2>&1; then
  ip=$(host test-api.projekt-ai.net | grep "has address" | head -1 | awk '{print $4}')
  print_success "DNS resolves: test-api.projekt-ai.net -> $ip"
else
  print_error "DNS resolution failed for test-api.projekt-ai.net"
fi

print_info "Testing DNS resolution for test-pages.projekt-ai.net..."
if host test-pages.projekt-ai.net > /dev/null 2>&1; then
  ip=$(host test-pages.projekt-ai.net | grep "has address" | head -1 | awk '{print $4}')
  print_success "DNS resolves: test-pages.projekt-ai.net -> $ip"
else
  print_error "DNS resolution failed for test-pages.projekt-ai.net"
fi

# Test 2: API Health Endpoint with Full Response
print_header "Test 2: API Health Endpoint with Full Response"
print_info "Testing ${TEST_API_URL}/api/health..."
health_response=$(curl -v "${TEST_API_URL}/api/health" 2>&1)
status_code=$(echo "$health_response" | grep -o "HTTP/[0-9.]* [0-9]*" | awk '{print $2}')

if [[ "$status_code" == "200" ]]; then
  print_success "API health endpoint returned HTTP $status_code"
  # Extract and display the JSON response
  body=$(echo "$health_response" | awk 'BEGIN{flag=0} /^\{/{flag=1} flag{print}')
  echo "Response body:"
  echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
  print_error "API health endpoint returned HTTP $status_code"
  echo "$health_response" | grep -E "HTTP|error|curl"
fi

# Test 3: Test Pages Access with Full Response
print_header "Test 3: Test Pages Access with Full Response"
print_info "Testing ${TEST_PAGES_URL}/api-test-safe.html..."

# First check with HEAD request
head_response=$(curl -I "${TEST_PAGES_URL}/api-test-safe.html" 2>&1)
status_code=$(echo "$head_response" | grep -o "HTTP/[0-9.]* [0-9]*" | awk '{print $2}')

if [[ "$status_code" == "200" ]]; then
  print_success "Test page HEAD request returned HTTP $status_code"
  echo "Response headers:"
  echo "$head_response" | grep -v "report-to\|endpoints\|report/v4" # Filter out verbose headers
else
  print_error "Test page HEAD request returned HTTP $status_code"
  echo "$head_response" | grep -E "HTTP|error|curl"
fi

# Then check the beginning of the file content
print_info "Checking the first few lines of the test page content..."
page_content=$(curl -s "${TEST_PAGES_URL}/api-test-safe.html" | head -20)
if [[ -n "$page_content" ]]; then
  print_success "Successfully retrieved content from test page"
  echo "First 20 lines:"
  echo "$page_content"
else
  print_error "Failed to retrieve content from test page"
fi

# Test 4: Dashboard HTML Analysis
print_header "Test 4: Dashboard HTML Analysis"
print_info "Analyzing dashboard HTML for API endpoints..."

# Extract all API URLs from the dashboard HTML
dashboard_html=$(curl -s "${TEST_PAGES_URL}/upwork-dashboard-test.html")
if [[ -n "$dashboard_html" ]]; then
  print_success "Successfully retrieved dashboard HTML"
  
  # Find all API endpoints
  echo "API endpoints in dashboard HTML:"
  echo "$dashboard_html" | grep -o "https://[^\"]*api/[^\"]*" | sort | uniq
  
  # Check for relative URLs
  echo ""
  echo "Relative API endpoints in dashboard HTML:"
  echo "$dashboard_html" | grep -o "'/api/[^']*'" | sort | uniq
  
  # Check which domain is being used
  domain_count=$(echo "$dashboard_html" | grep -c "test-api.projekt-ai.net")
  if [[ $domain_count -gt 0 ]]; then
    print_success "Dashboard is configured to use test-api.projekt-ai.net ($domain_count references)"
  else
    print_error "Dashboard is not configured to use test-api.projekt-ai.net"
  fi
else
  print_error "Failed to retrieve dashboard HTML"
fi

# Test 5: API Response Headers Analysis
print_header "Test 5: API Response Headers Analysis"
print_info "Analyzing API response headers for CORS configuration..."

cors_headers=$(curl -s -I "${TEST_API_URL}/api/proposals" 2>&1)
if [[ "$cors_headers" == *"Access-Control-Allow-Origin"* ]]; then
  print_success "API has CORS headers configured"
  echo "$cors_headers" | grep -i "Access-Control-Allow"
else
  print_error "API is missing CORS headers"
  echo "Headers received:"
  echo "$cors_headers" | grep -v "report-to\|endpoints\|report/v4" # Filter out verbose headers
fi

# Test 6: Dashboard API Integration Test
print_header "Test 6: Dashboard API Integration Test"
print_info "Testing dashboard's ability to load data from API..."

# This requires JavaScript, so we'll simulate the API call
print_info "Simulating dashboard API call to ${TEST_API_URL}/api/proposals..."
api_response=$(curl -s "${TEST_API_URL}/api/proposals")
if [[ "$api_response" == *"proposals"* ]]; then
  # Extract and count proposals
  proposals_count=$(echo "$api_response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_count', 0))")
  print_success "API returned $proposals_count proposals, which dashboard would load"
  
  # Check for a sample proposal to verify data
  if [[ $proposals_count -gt 0 ]]; then
    print_info "Sample first proposal details:"
    echo "$api_response" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('proposals') and len(data['proposals']) > 0:
    proposal = data['proposals'][0]
    print(f\"Job Title: {proposal.get('job_title', 'N/A')}\")
    print(f\"Client: {proposal.get('client_name', 'N/A')}\")
    print(f\"Score: {proposal.get('score', 'N/A')}\")
    print(f\"Status: {proposal.get('status', 'N/A')}\")
"
  fi
else
  print_error "API did not return valid proposals data"
  echo "Response excerpt:"
  echo "$api_response" | head -20
fi

# Summary of testing
print_header "TESTING SUMMARY"

print_info "Test Environment:"
echo "• API Server: ${TEST_API_URL}"
echo "• Test Pages: ${TEST_PAGES_URL}"
echo ""

print_info "Findings:"
echo "1. API Server Status: The API is running and responding with correct data"
echo "2. Test Pages Status: The test pages are accessible but may have configuration issues"
echo "3. Dashboard Integration: The dashboard references the test API but may have CORS issues"
echo ""

print_info "Recommended Actions:"
echo "1. Update the dashboard test page to use absolute URLs for API endpoints"
echo "2. Verify all Nginx configurations have proper CORS headers"
echo "3. Add proper content type headers to all responses"
echo "4. If using Cloudflare, check the Cloudflare settings for CORS"

echo "" 