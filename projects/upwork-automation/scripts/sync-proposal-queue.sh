#!/bin/bash
# Sync proposal queue to web-accessible location

SOURCE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
DEST="/var/www/projekt-ai.net/proposals/proposal-queue.json"

# Copy the file if it exists
if [ -f "$SOURCE" ]; then
    cp "$SOURCE" "$DEST"
    echo "✅ Proposal queue synced to web directory"
else
    echo "❌ Source file not found: $SOURCE"
fi 