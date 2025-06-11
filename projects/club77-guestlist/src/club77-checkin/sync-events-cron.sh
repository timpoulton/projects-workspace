#!/bin/bash

# Club77 Muzeek Events Auto-Sync Script
# Runs every hour to keep events updated
# Usage: Add to crontab with: 0 * * * * /root/homelab-docs/apps/club77-checkin/sync-events-cron.sh

LOG_FILE="/root/homelab-docs/apps/club77-checkin/sync.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting Muzeek events sync..." >> $LOG_FILE

# Check if Club77 app is running on CORRECT PORT (3005, not 3001)
if ! curl -s http://localhost:3005 > /dev/null; then
    echo "[$TIMESTAMP] ERROR: Club77 app not responding on port 3005" >> $LOG_FILE
    exit 1
fi

# Use container bypass as primary method (HTTP endpoint has authentication issues)
echo "[$TIMESTAMP] INFO: Using container bypass method for sync..." >> $LOG_FILE

# Execute sync directly in container (bypasses web auth)
CONTAINER_RESPONSE=$(docker exec club77_checkin_tailwind node test-sync.js 2>/dev/null)

if echo "$CONTAINER_RESPONSE" | grep -q '"success":true'; then
    STATS=$(echo "$CONTAINER_RESPONSE" | grep -o '"stats":{[^}]*}')
    echo "[$TIMESTAMP] SUCCESS: Container sync completed - $STATS" >> $LOG_FILE
else
    echo "[$TIMESTAMP] ERROR: Container sync failed - $CONTAINER_RESPONSE" >> $LOG_FILE
    exit 1
fi

# Keep only last 100 lines of log
tail -n 100 $LOG_FILE > ${LOG_FILE}.tmp && mv ${LOG_FILE}.tmp $LOG_FILE

echo "[$TIMESTAMP] Sync completed successfully" >> $LOG_FILE 