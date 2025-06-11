#!/bin/bash

# Cleanup Old Proposals Script
# Keep only the most recent 100 proposals and remove the rest

SERVER_DIR="/var/www/projekt-ai.net/proposals/"
NETLIFY_DIR="/root/homelab-docs/projekt-ai-website/proposals/"
KEEP_COUNT=100

echo "🧹 Cleaning up old proposals - keeping only the most recent $KEEP_COUNT"
echo "📂 Server directory: $SERVER_DIR"
echo "🌐 Netlify directory: $NETLIFY_DIR"

# Count current proposals
SERVER_CURRENT=$(find "$SERVER_DIR" -name "*.html" | wc -l)
NETLIFY_CURRENT=$(find "$NETLIFY_DIR" -name "*.html" | wc -l)

echo "📊 Current counts:"
echo "   Server: $SERVER_CURRENT proposals"
echo "   Netlify: $NETLIFY_CURRENT proposals"

if [ $SERVER_CURRENT -le $KEEP_COUNT ]; then
    echo "✅ Server already has $KEEP_COUNT or fewer proposals. No cleanup needed."
else
    echo "🔄 Cleaning up server directory..."
    
    # Find the most recent files and create a temporary list
    find "$SERVER_DIR" -name "*.html" -printf '%T@ %p\n' | sort -rn | head -n $KEEP_COUNT | cut -d' ' -f2- > /tmp/keep_files.txt
    
    # Remove old files (keep only the most recent 100)
    REMOVED_COUNT=0
    while IFS= read -r file; do
        if ! grep -q "$file" /tmp/keep_files.txt; then
            rm -f "$file"
            ((REMOVED_COUNT++))
        fi
    done < <(find "$SERVER_DIR" -name "*.html")
    
    echo "   🗑️  Removed $REMOVED_COUNT old proposals from server"
fi

if [ $NETLIFY_CURRENT -le $KEEP_COUNT ]; then
    echo "✅ Netlify already has $KEEP_COUNT or fewer proposals. No cleanup needed."
else
    echo "🔄 Cleaning up Netlify directory..."
    
    # Find the most recent files and create a temporary list
    find "$NETLIFY_DIR" -name "*.html" -printf '%T@ %p\n' | sort -rn | head -n $KEEP_COUNT | cut -d' ' -f2- > /tmp/keep_netlify_files.txt
    
    # Remove old files (keep only the most recent 100)
    NETLIFY_REMOVED_COUNT=0
    while IFS= read -r file; do
        if ! grep -q "$file" /tmp/keep_netlify_files.txt; then
            rm -f "$file"
            ((NETLIFY_REMOVED_COUNT++))
        fi
    done < <(find "$NETLIFY_DIR" -name "*.html")
    
    echo "   🗑️  Removed $NETLIFY_REMOVED_COUNT old proposals from Netlify"
fi

# Clean up temporary files
rm -f /tmp/keep_files.txt /tmp/keep_netlify_files.txt

# Count final proposals
SERVER_FINAL=$(find "$SERVER_DIR" -name "*.html" | wc -l)
NETLIFY_FINAL=$(find "$NETLIFY_DIR" -name "*.html" | wc -l)

echo "📊 Final counts:"
echo "   Server: $SERVER_FINAL proposals"
echo "   Netlify: $NETLIFY_FINAL proposals"

# Update proposal queue to match (keep only recent 100)
echo "🔄 Updating proposal queue..."
QUEUE_FILE="/root/homelab-docs/scripts/upwork-automation/proposal-queue.json"

if [ -f "$QUEUE_FILE" ]; then
    # Keep only the most recent 100 entries in the queue
    python3 -c "
import json
with open('$QUEUE_FILE', 'r') as f:
    queue = json.load(f)
# Sort by timestamp and keep only the most recent 100
queue = sorted(queue, key=lambda x: x.get('created_at', ''), reverse=True)[:$KEEP_COUNT]
with open('$QUEUE_FILE', 'w') as f:
    json.dump(queue, f, indent=2)
print(f'✅ Updated queue to {len(queue)} entries')
"
fi

# Deploy changes to Netlify
echo "🚀 Deploying cleanup to Netlify..."
cd /root/homelab-docs/projekt-ai-website

# Check git status
CHANGED_FILES=$(git status --porcelain | wc -l)

if [ $CHANGED_FILES -gt 0 ]; then
    echo "🔧 Changes detected, committing and deploying..."
    
    # Add all changes (including deletions)
    git add -A proposals/
    
    # Commit with informative message
    git commit -m "Cleanup: Keep only most recent $KEEP_COUNT proposals (removed old ones)"
    
    # Push to deploy
    git push
    
    echo "🚀 Deployment triggered! Changes will be live in 2-3 minutes."
else
    echo "✅ No changes detected - cleanup already synced"
fi

echo ""
echo "🎯 CLEANUP COMPLETE!"
echo "   📈 Kept $KEEP_COUNT most recent proposals"
echo "   🗑️  Removed old proposals to improve performance"
echo "   🌐 Changes deployed to https://projekt-ai.net/proposals/" 