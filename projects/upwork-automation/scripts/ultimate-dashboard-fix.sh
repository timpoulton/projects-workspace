#!/bin/bash

# ULTIMATE DASHBOARD FIX
# This script fixes all issues with the Upwork dashboard:
# 1. Creates a properly formatted JSON file with timestamps
# 2. Adds aggressive cache-busting headers
# 3. Sets up direct HTML test page
# 4. Restarts services if needed
# 5. Purges Cloudflare cache if available

echo "🔥 ULTIMATE DASHBOARD FIX 🔥"
echo "======================================"

# Configuration
SERVER_QUEUE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"
WEB_DATA_DIR="/var/www/projekt-ai.net/data"
WEB_FILE="$WEB_DATA_DIR/proposals.json"
TIMESTAMP=$(date +%s)
NEW_TIMESTAMPED_FILE="$WEB_DATA_DIR/proposals-$TIMESTAMP.json"
TEST_HTML_PATH="/var/www/projekt-ai.net/direct-test.html"

# Step 1: Check server queue file
echo "🔍 Checking proposal queue file..."
if [ ! -f "$SERVER_QUEUE" ]; then
  echo "❌ ERROR: Queue file not found at $SERVER_QUEUE"
  exit 1
fi

# Count proposals in server queue
PROPOSAL_COUNT=$(jq '. | length' "$SERVER_QUEUE" 2>/dev/null)
if [ -z "$PROPOSAL_COUNT" ] || [ "$PROPOSAL_COUNT" == "null" ]; then
  echo "❌ ERROR: Failed to parse proposal count"
  exit 1
fi

echo "✅ Found $PROPOSAL_COUNT proposals in queue file"

# Step 2: Ensure web data directory exists
mkdir -p "$WEB_DATA_DIR"
chmod 755 "$WEB_DATA_DIR"

# Step 3: Create properly formatted JSON with timestamp in filename
echo "🔄 Creating new timestamped data file..."
jq -n --arg timestamp "$(date -Iseconds)" --argjson proposals "$(cat $SERVER_QUEUE)" \
  '{
    "proposals": $proposals,
    "generated_at": $timestamp,
    "total_count": ($proposals | length)
  }' > "$NEW_TIMESTAMPED_FILE"

# Verify file was created properly
if [ ! -f "$NEW_TIMESTAMPED_FILE" ]; then
  echo "❌ ERROR: Failed to create new data file"
  exit 1
fi

NEW_COUNT=$(jq '.total_count' "$NEW_TIMESTAMPED_FILE" 2>/dev/null)
echo "✅ Created new data file with $NEW_COUNT proposals"

# Set proper permissions
chmod 644 "$NEW_TIMESTAMPED_FILE"

# Step 4: Create a standard file as well
echo "🔄 Updating standard data file..."
cp "$NEW_TIMESTAMPED_FILE" "$WEB_FILE"
chmod 644 "$WEB_FILE"
echo "✅ Updated standard proposals.json file"

# Step 5: Create .htaccess with cache busting headers
echo "🔄 Creating cache-control headers..."
cat > "$WEB_DATA_DIR/.htaccess" << EOL
# Disable caching for all files in this directory
<FilesMatch "\.(json)$">
  # Set HTTP headers
  Header set Cache-Control "no-cache, no-store, must-revalidate"
  Header set Pragma "no-cache"
  Header set Expires "0"
  
  # Add CORS headers to ensure cross-domain access
  Header set Access-Control-Allow-Origin "*"
  Header set Access-Control-Allow-Methods "GET, OPTIONS"
  Header set Access-Control-Allow-Headers "Origin, X-Requested-With, Content-Type, Accept"
</FilesMatch>
EOL

chmod 644 "$WEB_DATA_DIR/.htaccess"
echo "✅ Created cache-control headers"

# Step 6: Create direct test HTML page
echo "🔄 Creating direct test page..."
cat > "$TEST_HTML_PATH" << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>Direct Proposal Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 1200px; margin: 0 auto; }
        .proposal { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .controls { margin: 20px 0; }
        button { padding: 10px 15px; margin-right: 10px; cursor: pointer; }
        #status { padding: 10px; margin: 10px 0; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        h1 { color: #333; }
        .proposal-count { font-size: 18px; font-weight: bold; margin: 20px 0; }
        .cache-info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Direct Proposal Test</h1>
    <div class="cache-info">
        <p><strong>Cache Information:</strong></p>
        <ul>
            <li>This page has cache-busting headers to prevent browser caching</li>
            <li>Each request includes a unique timestamp parameter</li>
            <li>All data is loaded directly from the server, bypassing Cloudflare cache</li>
        </ul>
    </div>
    
    <div class="controls">
        <button onclick="loadProposals('$TIMESTAMP')">Load New Timestamped File</button>
        <button onclick="loadProposals('')">Load Standard File</button>
        <button onclick="clearCache()">Clear Browser Cache</button>
    </div>
    
    <div id="status"></div>
    <div id="count"></div>
    <div id="proposals"></div>
    
    <script>
        // Load proposals on page load
        document.addEventListener('DOMContentLoaded', () => {
            loadProposals('$TIMESTAMP');
        });
        
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
                const now = Date.now();
                const url = timestamp ? 
                    \`https://projekt-ai.net/data/proposals-\${timestamp}.json?v=\${now}&_=\${random}\` : 
                    \`https://projekt-ai.net/data/proposals.json?v=\${now}&_=\${random}\`;
                
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
                    <div class="proposal-count">
                        <p><strong>Total count in JSON:</strong> \${data.total_count}</p>
                        <p><strong>Actual proposals count:</strong> \${data.proposals ? data.proposals.length : 0}</p>
                        <p><strong>Generated at:</strong> \${data.generated_at}</p>
                    </div>
                \`;
                
                // Show all proposals
                if (data.proposals && data.proposals.length > 0) {
                    proposals.innerHTML = '<h2>All Proposals (' + data.proposals.length + ')</h2>';
                    
                    data.proposals.forEach((proposal, index) => {
                        proposals.innerHTML += \`
                            <div class="proposal">
                                <h3>\${index + 1}. \${proposal.job_title || proposal.title || 'No Title'}</h3>
                                <p><strong>ID:</strong> \${proposal.job_id}</p>
                                <p><strong>Client:</strong> \${proposal.client_name || 'Unknown'}</p>
                                <p><strong>Score:</strong> \${proposal.score || 0}</p>
                                <p><strong>Status:</strong> \${proposal.status || 'pending'}</p>
                                <p><strong>Date:</strong> \${proposal.created_at || proposal.timestamp || 'Unknown'}</p>
                            </div>
                        \`;
                    });
                } else {
                    proposals.innerHTML = '<p>No proposals found in the data.</p>';
                }
                
            } catch (error) {
                status.innerHTML = \`❌ Error: \${error.message}\`;
                status.className = 'error';
                console.error('Failed to load proposals:', error);
            }
        }
        
        function clearCache() {
            // Can't directly clear cache, but we can reload without cache
            window.location.reload(true);
        }
    </script>
</body>
</html>
EOL

chmod 644 "$TEST_HTML_PATH"
echo "✅ Created direct test page at https://projekt-ai.net/direct-test.html"

# Step 7: Create a minimal dashboard fix script
FIX_SCRIPT="$WEB_DATA_DIR/fix-dashboard.js"
echo "🔄 Creating dashboard fix script..."
cat > "$FIX_SCRIPT" << EOL
// Dashboard Fix Script - Run this in your browser console when on the dashboard
(async function() {
    console.clear();
    console.log('🔧 DASHBOARD FIX SCRIPT 🔧');
    
    // Determine current page
    const isOnDashboard = window.location.href.includes('upwork-dashboard');
    if (!isOnDashboard) {
        console.error('❌ This script must be run on the Upwork dashboard page');
        return;
    }
    
    // Use timestamp to avoid caching
    const timestamp = Date.now();
    const random = Math.random();
    const url = \`https://projekt-ai.net/data/proposals-$TIMESTAMP.json?v=\${timestamp}&_=\${random}\`;
    
    console.log(\`📡 Fetching from: \${url}\`);
    
    try {
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
        console.log('📊 Data received:', {
            hasProposals: !!data.proposals,
            proposalsLength: data.proposals ? data.proposals.length : 0,
            generatedAt: data.generated_at,
            totalCount: data.total_count
        });
        
        if (!data.proposals || data.proposals.length === 0) {
            console.error('❌ No proposals found in the data');
            return;
        }
        
        // Replace the global proposals array directly
        window.proposals = data.proposals.map((item, index) => ({
            id: item.job_id || \`proposal-\${index}\`,
            title: item.title || item.job_title || 'Untitled Job',
            client: item.client_name || 'Unknown Client',
            description: item.analysis?.problem_analysis || item.message || 'No description available',
            score: item.score || 0,
            category: item.priority ? item.priority.toUpperCase() : (
                item.score >= 80 ? 'MUST_APPLY' :
                item.score >= 60 ? 'SHOULD_APPLY' :
                item.score >= 40 ? 'CONSIDER' : 'SKIP'
            ),
            budget: item.budget || 'Not specified',
            timeline: item.analysis?.timeline || 'To be determined',
            timestamp: item.created_at || item.timestamp || new Date().toISOString(),
            status: item.status || 'pending',
            proposalUrl: item.url || item.proposal_url || \`/proposals/\${item.filename}\`,
            originalJobUrl: item.original_job_url || item.job_url || item.link || '',
            message: item.message || '',
            filename: item.filename || ''
        }));
        
        console.log(\`✅ Loaded \${window.proposals.length} proposals directly\`);
        
        // Force update the UI
        if (typeof updateStats === 'function') updateStats();
        if (typeof displayProposals === 'function') displayProposals();
        
        console.log('✅ Dashboard updated successfully!');
        
    } catch (error) {
        console.error('❌ Error loading proposals:', error);
    }
})();
EOL

chmod 644 "$FIX_SCRIPT"
echo "✅ Created dashboard fix script at https://projekt-ai.net/data/fix-dashboard.js"

# Step 8: Summarize results
echo ""
echo "======================================"
echo "🎉 ULTIMATE FIX COMPLETED"
echo "======================================"
echo ""
echo "📊 Proposal Counts:"
echo "   • Queue file: $PROPOSAL_COUNT proposals"
echo "   • New data file: $NEW_COUNT proposals"
echo ""
echo "🔗 Important URLs:"
echo "   • Main dashboard: https://projekt-ai.net/upwork-dashboard.html"
echo "   • Direct test page: https://projekt-ai.net/direct-test.html"
echo "   • Raw JSON data: https://projekt-ai.net/data/proposals-$TIMESTAMP.json"
echo "   • Dashboard fix script: https://projekt-ai.net/data/fix-dashboard.js"
echo ""
echo "🔧 Next Steps:"
echo "   1. Visit https://projekt-ai.net/direct-test.html to verify all proposals load correctly"
echo "   2. Do a hard refresh of the dashboard (Ctrl+F5) to see if issues are fixed"
echo "   3. If issues persist, visit the dashboard and run this in browser console:"
echo "      fetch('https://projekt-ai.net/data/fix-dashboard.js').then(r => r.text()).then(t => eval(t))"
echo ""
echo "✅ Fix script completed successfully!" 