#!/bin/bash

# Check proposals.json and create a fresh copy with unique timestamp
echo "🔍 Checking web data file directly..."

WEB_DATA_FILE="/var/www/projekt-ai.net/data/proposals.json"

if [ -f "$WEB_DATA_FILE" ]; then
  # Check counts
  TOTAL_COUNT=$(cat "$WEB_DATA_FILE" | jq '.total_count')
  ACTUAL_COUNT=$(cat "$WEB_DATA_FILE" | jq '.proposals | length')
  
  echo "📊 Web file total_count: $TOTAL_COUNT"
  echo "📊 Web file actual proposals count: $ACTUAL_COUNT"
  
  # Get fresh data directly from server
  echo "🔄 Getting fresh data from server..."
  TIMESTAMP=$(date +%s)
  FRESH_FILE="/var/www/projekt-ai.net/data/proposals-$TIMESTAMP.json"
  
  # Get data directly from API and format it correctly
  echo "curl -s http://localhost:5001/api/proposals > /tmp/raw-proposals-$TIMESTAMP.json"
  curl -s http://localhost:5001/api/proposals > /tmp/raw-proposals-$TIMESTAMP.json
  
  # Count proposals in raw data
  RAW_COUNT=$(cat /tmp/raw-proposals-$TIMESTAMP.json | jq length)
  echo "📊 Raw API data contains $RAW_COUNT proposals"
  
  # Create properly formatted data
  echo "{\"proposals\": $(cat /tmp/raw-proposals-$TIMESTAMP.json), \"generated_at\": \"$(date -Iseconds)\", \"total_count\": $RAW_COUNT}" > "$FRESH_FILE"
  
  # Check the new file
  NEW_TOTAL=$(cat "$FRESH_FILE" | jq '.total_count')
  NEW_ACTUAL=$(cat "$FRESH_FILE" | jq '.proposals | length')
  
  echo "📊 New file total_count: $NEW_TOTAL"
  echo "📊 New file actual proposals count: $NEW_ACTUAL"
  
  # Create latest pointer file with cache busting
  echo "{\"redirect\": \"proposals-$TIMESTAMP.json?v=$TIMESTAMP\", \"timestamp\": $TIMESTAMP}" > "/var/www/projekt-ai.net/data/latest-proposals-$TIMESTAMP.json"
  
  # Update the main file
  cp "$FRESH_FILE" "$WEB_DATA_FILE"
  chmod 644 "$WEB_DATA_FILE"
  
  echo "✅ Created fresh proposals file at: $FRESH_FILE"
  echo "✅ Updated main proposals.json file"
  echo "✅ Created latest pointer at: /var/www/projekt-ai.net/data/latest-proposals-$TIMESTAMP.json"
  
  # Clean up
  rm -f /tmp/raw-proposals-$TIMESTAMP.json
  
  echo "🔄 Please try accessing: https://projekt-ai.net/data/proposals-$TIMESTAMP.json?v=$TIMESTAMP"
  echo "🔄 Please refresh the dashboard with Ctrl+F5"
else
  echo "❌ Web data file not found at $WEB_DATA_FILE"
fi 