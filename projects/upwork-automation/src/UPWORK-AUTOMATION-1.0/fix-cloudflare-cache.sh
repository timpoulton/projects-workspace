#!/bin/bash

# Fix Cloudflare Cache and Dashboard Loading Issues
# Creates a uniquely named proposals.json file and updates the dashboard

echo "🔧 Creating new timestamped proposals file to bypass caching..."

# Get current timestamp for unique file naming
TIMESTAMP=$(date +%s)
WEB_DATA_DIR="/var/www/projekt-ai.net/data"
NEW_FILE="$WEB_DATA_DIR/proposals-$TIMESTAMP.json"
SERVER_FILE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"

# Ensure the directory exists
mkdir -p "$WEB_DATA_DIR"

# Check if server file exists
if [ ! -f "$SERVER_FILE" ]; then
  echo "❌ ERROR: Server proposal queue file not found at $SERVER_FILE"
  exit 1
fi

# Count proposals in the original file
PROPOSAL_COUNT=$(jq '. | length' "$SERVER_FILE" 2>/dev/null)
if [ -z "$PROPOSAL_COUNT" ] || [ "$PROPOSAL_COUNT" == "null" ]; then
  echo "❌ ERROR: Failed to read proposal count from server file"
  exit 1
fi

echo "📊 Found $PROPOSAL_COUNT proposals in server file"

# Create a properly formatted JSON file for the dashboard
echo "🔄 Creating new dashboard data file..."
jq -n --arg timestamp "$(date -Iseconds)" --argjson proposals "$(cat $SERVER_FILE)" \
  '{
    "proposals": $proposals,
    "generated_at": $timestamp,
    "total_count": ($proposals | length)
  }' > "$NEW_FILE"

# Verify the file was created properly
if [ -f "$NEW_FILE" ]; then
  NEW_COUNT=$(jq '.total_count' "$NEW_FILE" 2>/dev/null)
  echo "✅ Created new data file: $NEW_FILE with $NEW_COUNT proposals"
  
  # Set proper permissions
  chmod 644 "$NEW_FILE"
  
  # Also update the standard file
  cp "$NEW_FILE" "$WEB_DATA_DIR/proposals.json"
  echo "✅ Updated standard proposals.json file"
  
  # Output the URL to use in the dashboard
  echo "🔗 Use this URL in your dashboard:"
  echo "https://projekt-ai.net/data/proposals-$TIMESTAMP.json"
  
  # Update the dashboard HTML to use this file
  DASHBOARD_FILE="/root/homelab-docs/projekt-ai-website/upwork-dashboard.html"
  if [ -f "$DASHBOARD_FILE" ]; then
    # Create backup
    cp "$DASHBOARD_FILE" "$DASHBOARD_FILE.bak"
    
    # Update the file URLs in the dashboard
    sed -i "s|\`https://projekt-ai.net/data/proposals-[0-9]*.json?v=[0-9]*&_=\${Math.random()}\`,|\`https://projekt-ai.net/data/proposals-$TIMESTAMP.json?v=$TIMESTAMP&_=\${Math.random()}\`,|g" "$DASHBOARD_FILE"
    
    echo "✅ Updated dashboard HTML to use the new file"
  else
    echo "⚠️ Warning: Could not find dashboard HTML file"
  fi
else
  echo "❌ ERROR: Failed to create new data file"
  exit 1
fi

echo "🌐 Instructions:"
echo "1. Do a hard refresh of the dashboard (Ctrl+F5)"
echo "2. Clear browser cache if needed"
echo "3. Verify all $PROPOSAL_COUNT proposals appear" 