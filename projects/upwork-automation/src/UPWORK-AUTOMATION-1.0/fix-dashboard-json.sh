#!/bin/bash

# Fix Dashboard JSON Script
# Ensures all proposals are properly included in the dashboard data

echo "🔍 Checking proposals JSON data..."

# Check server data
SERVER_COUNT=$(curl -s "http://localhost:5001/api/proposals" | jq length)
echo "📊 Server API proposals count: $SERVER_COUNT"

# Check web data file
WEB_DATA_FILE="/var/www/projekt-ai.net/data/proposals.json"
if [ -f "$WEB_DATA_FILE" ]; then
    WEB_COUNT=$(cat "$WEB_DATA_FILE" | jq '.total_count')
    ACTUAL_COUNT=$(cat "$WEB_DATA_FILE" | jq '.proposals | length')
    echo "📊 Web data file total_count: $WEB_COUNT"
    echo "📊 Web data file actual proposals: $ACTUAL_COUNT"
    
    # Check if the counts don't match
    if [ "$WEB_COUNT" != "$ACTUAL_COUNT" ] || [ "$WEB_COUNT" != "$SERVER_COUNT" ]; then
        echo "⚠️ Count mismatch detected! Fixing the data..."
        
        # Get fresh data from server
        TEMP_FILE="/tmp/fresh-proposals-$$.json"
        curl -s "http://localhost:5001/data/proposals.json" > "$TEMP_FILE"
        
        # Verify the JSON is valid
        if jq empty "$TEMP_FILE" 2>/dev/null; then
            # Add cache-busting timestamp to filename
            TIMESTAMP=$(date +%s)
            cp "$TEMP_FILE" "$WEB_DATA_FILE"
            chmod 644 "$WEB_DATA_FILE"
            
            # Also create a timestamped version
            cp "$TEMP_FILE" "/var/www/projekt-ai.net/data/proposals-$TIMESTAMP.json"
            chmod 644 "/var/www/projekt-ai.net/data/proposals-$TIMESTAMP.json"
            
            # Create a small file that redirects to the latest version
            echo "{\"redirect\": \"proposals-$TIMESTAMP.json\", \"timestamp\": $TIMESTAMP}" > "/var/www/projekt-ai.net/data/latest-proposals.json"
            
            echo "✅ Fixed! New data file created with $SERVER_COUNT proposals."
        else
            echo "❌ Error: Invalid JSON from server"
        fi
        
        # Clean up
        rm -f "$TEMP_FILE"
    else
        echo "✅ All good! Web data matches server data with $WEB_COUNT proposals."
    fi
else
    echo "❌ Error: Web data file not found"
    
    # Create directory if it doesn't exist
    mkdir -p "/var/www/projekt-ai.net/data/"
    
    # Fetch and save fresh data
    curl -s "http://localhost:5001/data/proposals.json" > "$WEB_DATA_FILE"
    chmod 644 "$WEB_DATA_FILE"
    
    echo "✅ Created new web data file from server."
fi

# Update the dashboard HTML to force refresh
DASHBOARD_HTML="/root/homelab-docs/projekt-ai-website/upwork-dashboard.html"
if [ -f "$DASHBOARD_HTML" ]; then
    # Add current timestamp to force browser cache refresh
    TIMESTAMP=$(date +%s)
    sed -i "s/<meta name=\"cache-version\".*/<meta name=\"cache-version\" content=\"$TIMESTAMP\">/" "$DASHBOARD_HTML"
    
    if ! grep -q "cache-version" "$DASHBOARD_HTML"; then
        # Add the meta tag if it doesn't exist
        sed -i "/<meta name=\"viewport\"/a \    <meta name=\"cache-version\" content=\"$TIMESTAMP\">" "$DASHBOARD_HTML"
    fi
    
    echo "✅ Updated dashboard HTML with cache-busting timestamp."
fi

echo "✅ Dashboard JSON check complete."
echo "🔄 Please refresh the dashboard page with Ctrl+F5 to see all proposals." 