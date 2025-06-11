#!/bin/bash

# Fix Dashboard URLs Script
# Updates the test dashboard to use absolute URLs for all API endpoints
# Created: June 3, 2025

# Color codes for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DASHBOARD_PATH="/var/www/projekt-ai.net/upwork-dashboard-test.html"
BACKUP_PATH="/root/homelab-docs/scripts/upwork-automation/backups-$(date +%Y%m%d-%H%M%S)"
TEST_API_URL="https://test-api.projekt-ai.net"

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

# Start script
print_header "DASHBOARD URL FIX SCRIPT"
print_info "This script will update the test dashboard to use absolute URLs"
echo "Date: $(date)"
echo ""

# Create backup directory
print_info "Creating backup directory..."
mkdir -p "${BACKUP_PATH}"
if [[ $? -eq 0 ]]; then
  print_success "Created backup directory: ${BACKUP_PATH}"
else
  print_error "Failed to create backup directory"
  exit 1
fi

# Create backup of dashboard
print_info "Creating backup of dashboard file..."
cp "${DASHBOARD_PATH}" "${BACKUP_PATH}/upwork-dashboard-test.html.bak"
if [[ $? -eq 0 ]]; then
  print_success "Backup created: ${BACKUP_PATH}/upwork-dashboard-test.html.bak"
else
  print_error "Failed to create backup"
  exit 1
fi

# Check if the dashboard file exists
if [[ ! -f "${DASHBOARD_PATH}" ]]; then
  print_error "Dashboard file not found: ${DASHBOARD_PATH}"
  exit 1
fi

print_header "UPDATING DASHBOARD URLs"

# Count current relative URLs
relative_count=$(grep -c "'/api/proposals/" "${DASHBOARD_PATH}")
print_info "Found ${relative_count} relative API endpoints to update"

# First, update the approve endpoint
print_info "Updating approve endpoint URL..."
sed -i "s|'/api/proposals/approve'|'${TEST_API_URL}/api/proposals/approve'|g" "${DASHBOARD_PATH}"
if [[ $? -eq 0 ]]; then
  print_success "Updated approve endpoint URL"
else
  print_error "Failed to update approve endpoint URL"
fi

# Update the reject endpoint
print_info "Updating reject endpoint URL..."
sed -i "s|'/api/proposals/reject'|'${TEST_API_URL}/api/proposals/reject'|g" "${DASHBOARD_PATH}"
if [[ $? -eq 0 ]]; then
  print_success "Updated reject endpoint URL"
else
  print_error "Failed to update reject endpoint URL"
fi

# Update the edit endpoint
print_info "Updating edit endpoint URL..."
sed -i "s|'/api/proposals/edit'|'${TEST_API_URL}/api/proposals/edit'|g" "${DASHBOARD_PATH}"
if [[ $? -eq 0 ]]; then
  print_success "Updated edit endpoint URL"
else
  print_error "Failed to update edit endpoint URL"
fi

# Count updated relative URLs
updated_relative_count=$(grep -c "'/api/proposals/" "${DASHBOARD_PATH}")
absolute_count=$(grep -c "${TEST_API_URL}/api/proposals/" "${DASHBOARD_PATH}")

print_header "VERIFICATION"
print_info "Verifying URL updates..."
echo "• Original relative URLs: ${relative_count}"
echo "• Remaining relative URLs: ${updated_relative_count}"
echo "• Absolute URLs: ${absolute_count}"

if [[ ${updated_relative_count} -eq 0 ]]; then
  print_success "All relative URLs have been updated to absolute URLs"
else
  print_error "${updated_relative_count} relative URLs remain, manual inspection required"
  grep -n "'/api/proposals/" "${DASHBOARD_PATH}"
fi

# Add cache-busting version timestamp
timestamp=$(date +%s)
print_info "Adding cache-busting timestamp: ${timestamp}..."

# Add version comment at the top of the file
sed -i "1s/^/<!-- Dashboard with absolute URLs - Version: ${timestamp} -->\n/" "${DASHBOARD_PATH}"

# Add note about changes
cat >> "${DASHBOARD_PATH}" << EOL

<!-- 
Dashboard updated by fix-dashboard-urls.sh on $(date)
Changes made:
1. Converted relative API URLs to absolute URLs
2. Added cache-busting timestamp
3. Updated all endpoints to use ${TEST_API_URL}
-->
EOL

print_success "Added version information to dashboard"

print_header "COMPLETION"
print_info "Dashboard URL updates complete!"
echo ""
echo "Next steps:"
echo "1. Test the dashboard in a browser: ${TEST_API_URL}/upwork-dashboard-test.html"
echo "2. Verify all API endpoints work correctly"
echo "3. If needed, restore the backup from: ${BACKUP_PATH}/upwork-dashboard-test.html.bak"
echo ""
echo "To restore the backup:"
echo "cp ${BACKUP_PATH}/upwork-dashboard-test.html.bak ${DASHBOARD_PATH}"
echo ""

print_info "Running test to verify the dashboard can be accessed..."
curl -s -I "https://test-pages.projekt-ai.net/upwork-dashboard-test.html" | head -1
echo "" 