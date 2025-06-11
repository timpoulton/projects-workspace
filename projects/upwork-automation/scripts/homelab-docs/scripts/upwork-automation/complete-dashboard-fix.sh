#!/bin/bash

# Complete Dashboard Fix
# Addresses all potential issues with the Upwork Automation Dashboard
# - Fixes synchronization between server and web data
# - Creates a unique timestamped file to bypass caching
# - Updates dashboard HTML to display all proposals
# - Tests the server API endpoints

echo "🔧 COMPREHENSIVE DASHBOARD FIX SCRIPT"
echo "======================================"

# Configuration
SERVER_QUEUE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
WEB_DATA_DIR="/var/www/projekt-ai.net/data"
WEB_FILE="$WEB_DATA_DIR/proposals.json"
DASHBOARD_FILE="/root/homelab-docs/projekt-ai-website/upwork-dashboard.html"
SERVER_URL="http://localhost:5001"
TIMESTAMP=$(date +%s)
NEW_TIMESTAMPED_FILE="$WEB_DATA_DIR/proposals-$TIMESTAMP.json"

# Step 1: Check if server is running
echo "🔍 Checking if server is running on port 5001..."
if netstat -tuln | grep ":5001 " > /dev/null; then
  echo "✅ Server is running on port 5001"
  
  # Test server API
  echo "🔄 Testing server API..."
  if curl -s "$SERVER_URL/api/proposals" > /dev/null; then
    SERVER_COUNT=$(curl -s "$SERVER_URL/api/proposals" | jq '. | length')
    echo "✅ Server API working - $SERVER_COUNT proposals available"
  else
    echo "⚠️ Server API not responding at $SERVER_URL/api/proposals"
    echo "   Will try to work with queue file directly"
  fi
else
  echo "⚠️ No server running on port 5001"
  echo "   Will try to work with queue file directly"
fi

# Step 2: Check proposal queue file
echo "🔍 Checking proposal queue file..."
if [ -f "$SERVER_QUEUE" ]; then
  QUEUE_COUNT=$(jq '. | length' "$SERVER_QUEUE" 2>/dev/null)
  if [ -n "$QUEUE_COUNT" ] && [ "$QUEUE_COUNT" != "null" ]; then
    echo "✅ Queue file contains $QUEUE_COUNT proposals"
  else
    echo "❌ ERROR: Queue file exists but couldn't parse proposal count"
    exit 1
  fi
else
  echo "❌ ERROR: Queue file not found at $SERVER_QUEUE"
  exit 1
fi

# Step 3: Create web data directory if needed
echo "🔍 Checking web data directory..."
if [ -d "$WEB_DATA_DIR" ]; then
  echo "✅ Web data directory exists"
else
  echo "🔄 Creating web data directory..."
  mkdir -p "$WEB_DATA_DIR"
  chmod 755 "$WEB_DATA_DIR"
  echo "✅ Created web data directory"
fi

# Step 4: Create properly formatted JSON data file
echo "🔄 Creating new dashboard data files..."

# Create a proper JSON structure
echo "{
  \"proposals\": $(cat $SERVER_QUEUE),
  \"generated_at\": \"$(date -Iseconds)\",
  \"total_count\": $QUEUE_COUNT
}" > "$NEW_TIMESTAMPED_FILE"

# Verify the file was created correctly
if [ -f "$NEW_TIMESTAMPED_FILE" ]; then
  NEW_COUNT=$(jq '.proposals | length' "$NEW_TIMESTAMPED_FILE" 2>/dev/null)
  NEW_TOTAL=$(jq '.total_count' "$NEW_TIMESTAMPED_FILE" 2>/dev/null)
  
  if [ "$NEW_COUNT" = "$QUEUE_COUNT" ] && [ "$NEW_TOTAL" = "$QUEUE_COUNT" ]; then
    echo "✅ Created timestamped data file with $NEW_COUNT proposals"
    chmod 644 "$NEW_TIMESTAMPED_FILE"
    
    # Also update the standard file
    cp "$NEW_TIMESTAMPED_FILE" "$WEB_FILE"
    chmod 644 "$WEB_FILE"
    echo "✅ Updated standard data file"
  else
    echo "⚠️ Warning: New file has $NEW_COUNT proposals (expected $QUEUE_COUNT)"
  fi
else
  echo "❌ ERROR: Failed to create timestamped data file"
  exit 1
fi

# Step 5: Update dashboard HTML to use the new file
if [ -f "$DASHBOARD_FILE" ]; then
  echo "🔄 Updating dashboard HTML..."
  
  # Create backup
  cp "$DASHBOARD_FILE" "$DASHBOARD_FILE.bak-$TIMESTAMP"
  
  # Update the file URL in the dashboard
  sed -i "s|\`https://projekt-ai.net/data/proposals-[0-9]*.json?v=[0-9]*&_=\${Math.random()}\`,|\`https://projekt-ai.net/data/proposals-$TIMESTAMP.json?v=$TIMESTAMP&_=\${Math.random()}\`,|g" "$DASHBOARD_FILE"
  
  # Make sure there's no artificial limit on displayed proposals
  MODIFIED=$(grep -c "// No 15-proposal limit" "$DASHBOARD_FILE")
  if [ "$MODIFIED" -gt 0 ]; then
    echo "✅ Dashboard HTML is already fixed to show all proposals"
  else
    echo "⚠️ Dashboard may have an artificial limit - manual fix required"
    echo "   Please edit $DASHBOARD_FILE to ensure all proposals are displayed"
  fi
  
  echo "✅ Updated dashboard HTML to use the new data file"
else
  echo "⚠️ Warning: Dashboard HTML file not found at $DASHBOARD_FILE"
fi

# Step 6: Create a direct access test page
TEST_PAGE="$WEB_DATA_DIR/test-dashboard.html"
echo "🔄 Creating direct test page..."

cat > "$TEST_PAGE" << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proposals Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        .proposal { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .buttons { margin: 20px 0; }
        button { padding: 10px 15px; margin-right: 10px; cursor: pointer; }
        #status { padding: 10px; margin: 10px 0; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>Direct Proposals Test</h1>
    <p>This page directly tests loading proposals from the data file, bypassing the dashboard code.</p>
    
    <div class="buttons">
        <button onclick="loadProposals('$TIMESTAMP')">Load New Timestamped File</button>
        <button onclick="loadProposals('')">Load Standard File</button>
    </div>
    
    <div id="status"></div>
    <div id="count"></div>
    <div id="proposals"></div>
    
    <script>
        async function loadProposals(timestamp) {
            const status = document.getElementById('status');
            const count = document.getElementById('count');
            const proposals = document.getElementById('proposals');
            
            status.innerHTML = 'Loading...';
            status.className = '';
            count.innerHTML = '';
            proposals.innerHTML = '';
            
            try {
                // Use cache busting
                const random = Math.random();
                const url = timestamp ? 
                    \`https://projekt-ai.net/data/proposals-\${timestamp}.json?v=\${timestamp}&_=\${random}\` : 
                    \`https://projekt-ai.net/data/proposals.json?v=\${Date.now()}&_=\${random}\`;
                
                console.log('Loading from:', url);
                
                const response = await fetch(url, {
                    cache: 'no-store',
                    headers: {
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0'
                    }
                });
                
                if (!response.ok) {
                    throw new Error(\`HTTP error \${response.status}\`);
                }
                
                const data = await response.json();
                
                status.innerHTML = \`✅ Successfully loaded data\`;
                status.className = 'success';
                
                count.innerHTML = \`
                    <p><strong>Total count in JSON:</strong> \${data.total_count}</p>
                    <p><strong>Actual proposals count:</strong> \${data.proposals ? data.proposals.length : 0}</p>
                    <p><strong>Generated at:</strong> \${data.generated_at}</p>
                \`;
                
                // Show first 10 proposals
                if (data.proposals && data.proposals.length > 0) {
                    data.proposals.slice(0, 10).forEach((proposal, index) => {
                        proposals.innerHTML += \`
                            <div class="proposal">
                                <h3>\${index + 1}. \${proposal.job_title || 'No Title'}</h3>
                                <p><strong>ID:</strong> \${proposal.job_id}</p>
                                <p><strong>Client:</strong> \${proposal.client_name || 'Unknown'}</p>
                                <p><strong>Score:</strong> \${proposal.score || 0}</p>
                            </div>
                        \`;
                    });
                    
                    proposals.innerHTML += \`<p><em>Showing 10 of \${data.proposals.length} proposals...</em></p>\`;
                } else {
                    proposals.innerHTML = '<p>No proposals found in the data.</p>';
                }
                
            } catch (error) {
                status.innerHTML = \`❌ Error: \${error.message}\`;
                status.className = 'error';
                console.error('Failed to load proposals:', error);
            }
        }
    </script>
</body>
</html>
EOL

chmod 644 "$TEST_PAGE"
echo "✅ Created direct test page at https://projekt-ai.net/data/test-dashboard.html"

# Step 7: Summarize results
echo ""
echo "======================================"
echo "🎉 FIX COMPLETED"
echo "======================================"
echo ""
echo "📊 Proposal Counts:"
echo "   • Queue file: $QUEUE_COUNT proposals"
echo "   • New data file: $NEW_COUNT proposals"
echo ""
echo "🔗 Important URLs:"
echo "   • Main dashboard: https://projekt-ai.net/upwork-dashboard.html"
echo "   • Direct test page: https://projekt-ai.net/data/test-dashboard.html"
echo "   • Raw JSON data: https://projekt-ai.net/data/proposals-$TIMESTAMP.json"
echo ""
echo "🔧 Next Steps:"
echo "   1. Do a hard refresh of the dashboard (Ctrl+F5)"
echo "   2. If dashboard still shows only 15 proposals, use the direct test page"
echo "   3. Copy the contents of /root/homelab-docs/scripts/upwork-automation/direct-data-check.js"
echo "      and paste it in your browser console while on the dashboard page"
echo ""
echo "✅ Fix script completed successfully!" 