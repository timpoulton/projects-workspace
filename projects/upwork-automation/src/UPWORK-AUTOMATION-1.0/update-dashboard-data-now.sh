#!/bin/bash
# Sync dashboard data to website directory
# Runs every 5 minutes via cron job

# Sync proposal data
curl -s "http://192.168.1.107:5001/data/proposals.json" > /var/www/projekt-ai.net/data/proposals.json

# Set permissions
chmod 644 /var/www/projekt-ai.net/data/proposals.json

# Log update
echo "[$(date)] Updated dashboard data" >> /root/homelab-docs/scripts/upwork-automation/update-dashboard.log

# Success message
echo "✅ Dashboard data updated at $(date)"
echo "📊 Total proposals: $(curl -s "http://192.168.1.107:5001/data/proposals.json" | jq '.total_count')" 