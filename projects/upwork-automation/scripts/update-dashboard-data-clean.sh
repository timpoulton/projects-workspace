#!/bin/bash

# Update Dashboard Data Script
# Updates the static proposals.json file for the dashboard

PROPOSALS_API="http://127.0.0.1:5001/data/proposals.json"
STATIC_FILE="/var/www/projekt-ai.net/data/proposals.json"
LOG_FILE="/root/homelab-docs/scripts/upwork-automation/update-dashboard.log"

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if proposal server is running
if ! curl -s "$PROPOSALS_API" > /dev/null; then
    log "ERROR: Proposal server not responding at $PROPOSALS_API"
    exit 1
fi

# Fetch latest data
log "Fetching latest proposal data..."
if curl -s "$PROPOSALS_API" > "$STATIC_FILE.tmp"; then
    # Validate JSON
    if jq empty "$STATIC_FILE.tmp" 2>/dev/null; then
        mv "$STATIC_FILE.tmp" "$STATIC_FILE"
        TOTAL_COUNT=$(jq -r '.total_count' "$STATIC_FILE")
        log "SUCCESS: Updated dashboard data with $TOTAL_COUNT proposals"
        
        # Set proper permissions
        chmod 644 "$STATIC_FILE"
        
    else
        log "ERROR: Invalid JSON received from server"
        rm -f "$STATIC_FILE.tmp"
        exit 1
    fi
else
    log "ERROR: Failed to fetch data from server"
    exit 1
fi 