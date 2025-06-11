#!/bin/bash

# Upwork Automation System Health Check
# Run this regularly to ensure all components are functioning properly
# Created: June 3, 2025

# Configuration
LOG_FILE="/root/homelab-docs/scripts/upwork-automation/logs/system-health-$(date +%Y%m%d).log"
QUEUE_FILE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
API_URL="https://api.projekt-ai.net/api/health"
API_PROPOSALS_URL="https://api.projekt-ai.net/api/proposals"
LOCAL_JSON="/var/www/projekt-ai.net/data/proposals.json"

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Start log entry
echo "=======================================" >> "$LOG_FILE"
echo "SYSTEM HEALTH CHECK - $(date)" >> "$LOG_FILE"
echo "=======================================" >> "$LOG_FILE"

# Function to log results
log_result() {
  echo "[$1] $2: $3" >> "$LOG_FILE"
  if [ "$1" == "PASS" ]; then
    echo -e "\e[32m✅ $2: $3\e[0m"
  elif [ "$1" == "WARN" ]; then
    echo -e "\e[33m⚠️ $2: $3\e[0m"
  else
    echo -e "\e[31m❌ $2: $3\e[0m"
  fi
}

echo "🔍 Running system health check..."

# Check services
echo -e "\n📊 Checking services:"

# Check multi-model service
MM_STATUS=$(systemctl is-active upwork-proposal-multimodel)
if [ "$MM_STATUS" == "active" ]; then
  log_result "PASS" "Multi-Model AI Service" "Running"
else
  log_result "FAIL" "Multi-Model AI Service" "Not running ($MM_STATUS)"
fi

# Check API service
API_STATUS=$(systemctl is-active upwork-proposal-api)
if [ "$API_STATUS" == "active" ]; then
  log_result "PASS" "API Service" "Running"
else
  log_result "FAIL" "API Service" "Not running ($API_STATUS)"
fi

# Check Nginx
NGINX_STATUS=$(systemctl is-active nginx)
if [ "$NGINX_STATUS" == "active" ]; then
  log_result "PASS" "Nginx" "Running"
else
  log_result "FAIL" "Nginx" "Not running ($NGINX_STATUS)"
fi

# Check ports
echo -e "\n📊 Checking ports:"

# Check port 5001 (Multi-Model AI)
if netstat -tuln | grep -q ":5001 "; then
  log_result "PASS" "Port 5001 (Multi-Model AI)" "Open and listening"
else
  log_result "FAIL" "Port 5001 (Multi-Model AI)" "Not listening"
fi

# Check port 5050 (API)
if netstat -tuln | grep -q ":5050 "; then
  log_result "PASS" "Port 5050 (API)" "Open and listening"
else
  log_result "FAIL" "Port 5050 (API)" "Not listening"
fi

# Check API health endpoint
echo -e "\n📊 Checking API endpoints:"

# Check API health
API_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")
if [ "$API_HEALTH" == "200" ]; then
  log_result "PASS" "API Health Endpoint" "Responding (200 OK)"
else
  log_result "FAIL" "API Health Endpoint" "Not responding (HTTP $API_HEALTH)"
fi

# Check API proposals endpoint
API_PROPOSALS=$(curl -s -o /dev/null -w "%{http_code}" "$API_PROPOSALS_URL")
if [ "$API_PROPOSALS" == "200" ]; then
  # Get the count of proposals
  PROPOSAL_COUNT=$(curl -s "$API_PROPOSALS_URL" | jq '.total_count')
  log_result "PASS" "API Proposals Endpoint" "Responding with $PROPOSAL_COUNT proposals"
else
  log_result "FAIL" "API Proposals Endpoint" "Not responding (HTTP $API_PROPOSALS)"
fi

# Check data files
echo -e "\n📊 Checking data files:"

# Check queue file
if [ -f "$QUEUE_FILE" ]; then
  QUEUE_COUNT=$(jq '. | length' "$QUEUE_FILE" 2>/dev/null)
  if [ -z "$QUEUE_COUNT" ] || [ "$QUEUE_COUNT" == "null" ]; then
    log_result "FAIL" "Queue File" "Invalid JSON format"
  else
    log_result "PASS" "Queue File" "Valid with $QUEUE_COUNT proposals"
  fi
else
  log_result "FAIL" "Queue File" "Not found"
fi

# Check local JSON file
if [ -f "$LOCAL_JSON" ]; then
  LOCAL_COUNT=$(jq '.total_count' "$LOCAL_JSON" 2>/dev/null)
  if [ -z "$LOCAL_COUNT" ] || [ "$LOCAL_COUNT" == "null" ]; then
    log_result "FAIL" "Local JSON File" "Invalid JSON format"
  else
    log_result "PASS" "Local JSON File" "Valid with $LOCAL_COUNT proposals"
  fi
else
  log_result "FAIL" "Local JSON File" "Not found"
fi

# Compare counts
if [ -n "$QUEUE_COUNT" ] && [ -n "$LOCAL_COUNT" ] && [ -n "$PROPOSAL_COUNT" ]; then
  if [ "$QUEUE_COUNT" == "$LOCAL_COUNT" ] && [ "$QUEUE_COUNT" == "$PROPOSAL_COUNT" ]; then
    log_result "PASS" "Data Consistency" "All sources have $QUEUE_COUNT proposals"
  else
    log_result "WARN" "Data Consistency" "Inconsistent counts: Queue=$QUEUE_COUNT, Local=$LOCAL_COUNT, API=$PROPOSAL_COUNT"
  fi
fi

# Check disk space
echo -e "\n📊 Checking disk space:"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}')
DISK_USAGE_NUM=${DISK_USAGE%\%}
if [ "$DISK_USAGE_NUM" -lt 80 ]; then
  log_result "PASS" "Disk Space" "Sufficient ($DISK_USAGE used)"
elif [ "$DISK_USAGE_NUM" -lt 90 ]; then
  log_result "WARN" "Disk Space" "Getting low ($DISK_USAGE used)"
else
  log_result "FAIL" "Disk Space" "Critical ($DISK_USAGE used)"
fi

# End log entry
echo -e "\nSystem health check completed at $(date)"
echo "=======================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo -e "\n✅ Health check complete. Log saved to $LOG_FILE" 