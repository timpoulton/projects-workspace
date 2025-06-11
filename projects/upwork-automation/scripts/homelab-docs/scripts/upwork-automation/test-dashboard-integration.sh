#!/bin/bash

# Test Dashboard Integration for Upwork Automation System
# Tests the integration between the dashboard and test API
# Created: June 3, 2025

# Color codes for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TEST_API_DOMAIN="https://test-api.projekt-ai.net"
TEST_PAGES_DOMAIN="https://test-pages.projekt-ai.net"
TEST_DASHBOARD="${TEST_PAGES_DOMAIN}/upwork-dashboard-test.html"

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
print_header "UPWORK AUTOMATION DASHBOARD INTEGRATION TESTING"
print_info "Testing dashboard integration with test API"
echo "Date: $(date)"
echo ""

# Test 1: Check if test API is accessible
print_header "Test 1: Check if test API is accessible"
api_response=$(curl -s "${TEST_API_DOMAIN}/api/health")
if [[ $? -eq 0 ]] && [[ "${api_response}" == *"ok"* ]]; then
  print_success "Test API is accessible"
else
  print_error "Test API is not accessible"
  echo "Response: ${api_response}"
  print_info "Please run test-api-endpoints.sh first to ensure the API is working"
  exit 1
fi

# Test 2: Check if test dashboard page is accessible
print_header "Test 2: Check if test dashboard page is accessible"
dashboard_response=$(curl -s -I "${TEST_DASHBOARD}" | head -1)
if [[ "${dashboard_response}" == *"200 OK"* ]]; then
  print_success "Test dashboard is accessible"
else
  print_error "Test dashboard is not accessible"
  echo "Response: ${dashboard_response}"
  exit 1
fi

# Test 3: Check dashboard HTML for correct API endpoint
print_header "Test 3: Check dashboard HTML for correct API endpoint"
dashboard_html=$(curl -s "${TEST_DASHBOARD}")
if [[ "${dashboard_html}" == *"${TEST_API_DOMAIN}/api/proposals"* ]]; then
  print_success "Dashboard HTML contains correct API endpoint"
else
  print_error "Dashboard HTML does not contain correct API endpoint"
  print_info "Extracting API endpoint from dashboard HTML..."
  endpoint=$(echo "${dashboard_html}" | grep -o "https://[^\"]*api/proposals" | head -1)
  if [[ -n "${endpoint}" ]]; then
    print_info "Found endpoint: ${endpoint}"
    print_info "Expected endpoint: ${TEST_API_DOMAIN}/api/proposals"
  else
    print_info "No API endpoint found in dashboard HTML"
  fi
fi

# Test 4: Simulate dashboard loading data from API
print_header "Test 4: Simulate dashboard loading data from API"
print_info "Loading data from API endpoint..."
api_data=$(curl -s "${TEST_API_DOMAIN}/api/proposals")
if [[ $? -eq 0 ]] && [[ "${api_data}" == *"proposals"* ]]; then
  # Parse the proposals count
  proposals_count=$(echo "${api_data}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('total_count', 0))")
  print_success "Successfully loaded ${proposals_count} proposals from API"
  
  # Print some proposal details for verification
  if [[ ${proposals_count} -gt 0 ]]; then
    print_info "Sample proposal details:"
    echo "${api_data}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('proposals') and len(data['proposals']) > 0:
    proposal = data['proposals'][0]
    print(f\"Job Title: {proposal.get('job_title', 'N/A')}\")
    print(f\"Client: {proposal.get('client_name', 'N/A')}\")
    print(f\"Score: {proposal.get('score', 'N/A')}\")
    print(f\"Status: {proposal.get('status', 'N/A')}\")
    print(f\"URL: {proposal.get('proposal_url', 'N/A')}\")
"
  fi
else
  print_error "Failed to load data from API"
  echo "Response: ${api_data}"
fi

# Test 5: Check for essential dashboard elements
print_header "Test 5: Check for essential dashboard elements"
essential_elements=(
  "proposal-list"
  "loading-indicator"
  "filter-controls"
  "approve-button"
  "reject-button"
)

for element in "${essential_elements[@]}"; do
  if [[ "${dashboard_html}" == *"${element}"* ]]; then
    print_success "Dashboard contains ${element}"
  else
    print_error "Dashboard is missing ${element}"
  fi
done

# Test 6: Check for dashboard styling
print_header "Test 6: Check for dashboard styling"
if [[ "${dashboard_html}" == *"<style"* ]]; then
  print_success "Dashboard contains embedded styles"
else
  print_error "Dashboard is missing embedded styles"
fi

# Test 7: Check for external JS libraries
print_header "Test 7: Check for external JS libraries"
libraries=(
  "jquery"
  "bootstrap"
)

for library in "${libraries[@]}"; do
  if [[ "${dashboard_html}" == *"${library}"* ]]; then
    print_success "Dashboard includes ${library}"
  else
    print_info "Dashboard does not include ${library} (may not be required)"
  fi
done

# Summary of testing
print_header "TESTING SUMMARY"

# Count passed tests
passed_tests=0
total_tests=7

# Test 1: API accessible
[[ "${api_response}" == *"ok"* ]] && ((passed_tests++))

# Test 2: Dashboard accessible
[[ "${dashboard_response}" == *"200 OK"* ]] && ((passed_tests++))

# Test 3: Correct API endpoint
[[ "${dashboard_html}" == *"${TEST_API_DOMAIN}/api/proposals"* ]] && ((passed_tests++))

# Test 4: Data loading
[[ "${api_data}" == *"proposals"* ]] && ((passed_tests++))

# Test 5: Essential elements (partial credit)
elements_found=0
for element in "${essential_elements[@]}"; do
  [[ "${dashboard_html}" == *"${element}"* ]] && ((elements_found++))
done
[[ ${elements_found} -ge 3 ]] && ((passed_tests++))

# Test 6: Styling
[[ "${dashboard_html}" == *"<style"* ]] && ((passed_tests++))

# Test 7: External libraries (optional)
libraries_found=0
for library in "${libraries[@]}"; do
  [[ "${dashboard_html}" == *"${library}"* ]] && ((libraries_found++))
done
[[ ${libraries_found} -ge 1 ]] && ((passed_tests++))

# Print summary
if [[ ${passed_tests} -eq ${total_tests} ]]; then
  print_success "All dashboard integration tests passed successfully!"
  echo ""
  echo -e "${BLUE}TEST DASHBOARD:${NC}"
  echo "  • URL: ${TEST_DASHBOARD}"
  echo ""
  echo -e "${BLUE}API ENDPOINT:${NC}"
  echo "  • ${TEST_API_DOMAIN}/api/proposals"
else
  print_error "${passed_tests}/${total_tests} tests passed"
  echo ""
  echo -e "${YELLOW}TROUBLESHOOTING:${NC}"
  echo "1. Ensure the test API is running properly:"
  echo "   ./test-api-endpoints.sh"
  echo ""
  echo "2. Check if the dashboard HTML contains the correct API endpoint:"
  echo "   curl -s ${TEST_DASHBOARD} | grep -o \"https://[^\"]*api/proposals\""
  echo ""
  echo "3. Manually test the dashboard in a browser:"
  echo "   ${TEST_DASHBOARD}"
fi

echo "" 