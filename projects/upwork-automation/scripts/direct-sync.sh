#!/bin/bash
# Direct Sync Script for Upwork Dashboard
# Copies the proposal queue directly to the dashboard data directory
# This script bypasses the API server to ensure immediate updates

# Configuration
SOURCE_FILE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
DEST_DIR="/var/www/projekt-ai.net/data"
DEST_FILE="${DEST_DIR}/proposals.json"
LOG_FILE="/var/log/direct-sync.log"

# Ensure log file exists
touch "$LOG_FILE"

# Log with timestamp
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Ensure destination directory exists
mkdir -p "$DEST_DIR"

# Start sync process
log "Starting direct sync"

# Check if source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    log "ERROR: Source file $SOURCE_FILE does not exist"
    exit 1
fi

# Validate source file is valid JSON
if ! jq empty "$SOURCE_FILE" 2>/dev/null; then
    log "ERROR: Source file $SOURCE_FILE is not valid JSON"
    exit 1
fi

# Count proposals
PROPOSAL_COUNT=$(jq 'length' "$SOURCE_FILE")

# Copy the file, add metadata, and save
TEMP_FILE=$(mktemp)
jq '. | {proposals: ., generated_at: "'$(date -Iseconds)'", total_count: '"$PROPOSAL_COUNT"', sync_method: "direct-sync"}' "$SOURCE_FILE" > "$TEMP_FILE"

# Copy to destination
cp "$TEMP_FILE" "$DEST_FILE"
chmod 644 "$DEST_FILE"

# Clean up
rm "$TEMP_FILE"

log "Direct sync successful - $PROPOSAL_COUNT proposals synced to $DEST_FILE"

# Notify console
echo "Direct sync successful - $PROPOSAL_COUNT proposals synced to $DEST_FILE" 