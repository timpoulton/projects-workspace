#!/bin/bash
# Upwork Dashboard Data Sync Script
# Syncs proposal data from API to static JSON file for dashboard fallback
# Run every 5 minutes via cron for reliable dashboard data

# Configuration
API_URL="http://localhost:5050/api/proposals"
DASHBOARD_DATA_DIR="/var/www/projekt-ai.net/data"
DATA_FILE="${DASHBOARD_DATA_DIR}/proposals.json"
LOG_FILE="/var/log/dashboard-sync.log"

# Ensure log file exists
touch "$LOG_FILE"

# Log with timestamp
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Ensure data directory exists
mkdir -p "$DASHBOARD_DATA_DIR"

# Start sync process
log "Starting dashboard data sync"

# Add cache busting parameter
TIMESTAMP=$(date +%s)
RANDOM_NUM=$((RANDOM % 10000))
FULL_URL="${API_URL}?v=${TIMESTAMP}&_=${RANDOM_NUM}"

# Fetch data from API
log "Fetching data from $FULL_URL"
HTTP_CODE=$(curl -s -w "%{http_code}" -o /tmp/proposals.json "$FULL_URL")

# Check if fetch was successful
if [ "$HTTP_CODE" == "200" ]; then
    # Validate JSON
    if jq empty /tmp/proposals.json 2>/dev/null; then
        # Count proposals
        PROPOSAL_COUNT=$(jq '.proposals | length' /tmp/proposals.json)
        
        # Add metadata
        TEMP_FILE=$(mktemp)
        jq '. + {"sync_timestamp": "'$(date -Iseconds)'", "sync_source": "cron-job"}' /tmp/proposals.json > "$TEMP_FILE"
        
        # Copy to destination
        cp "$TEMP_FILE" "$DATA_FILE"
        chmod 644 "$DATA_FILE"
        
        # Clean up
        rm "$TEMP_FILE"
        
        log "Sync successful - $PROPOSAL_COUNT proposals synced to $DATA_FILE"
    else
        log "ERROR: Invalid JSON received from API"
    fi
else
    log "ERROR: Failed to fetch data from API, HTTP code: $HTTP_CODE"
fi

# Clean up
rm -f /tmp/proposals.json

log "Sync process completed" 