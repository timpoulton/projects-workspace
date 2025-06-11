#!/bin/bash
# Update Upwork dashboard data and push to git
# This runs via cron to keep the dashboard updated

cd /root/homelab-docs

# Generate static data
echo "📊 Generating static proposals data..."
python3 scripts/upwork-automation/generate-static-proposals.py

# Check if data file was created
if [ ! -f "projekt-ai-website/data/proposals.json" ]; then
    echo "❌ Failed to generate proposals data"
    exit 1
fi

# Commit and push changes
cd projekt-ai-website
git add data/proposals.json
git commit -m "Update Upwork dashboard data - $(date '+%Y-%m-%d %H:%M')" || echo "No changes to commit"
git push || echo "Failed to push changes"

echo "✅ Dashboard data updated and pushed to git"

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
        
        # Purge Cloudflare cache if needed (optional)
        # curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/purge_cache" \
        #      -H "Authorization: Bearer YOUR_API_TOKEN" \
        #      -H "Content-Type: application/json" \
        #      --data '{"files":["https://projekt-ai.net/data/proposals.json"]}'
        
    else
        log "ERROR: Invalid JSON received from server"
        rm -f "$STATIC_FILE.tmp"
        exit 1
    fi
else
    log "ERROR: Failed to fetch data from server"
    exit 1
fi 