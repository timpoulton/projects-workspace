#!/bin/bash

# Sync Proposals to Netlify Script
# Copies generated proposals from server to Netlify site for public access

SOURCE_DIR="/var/www/projekt-ai.net/proposals/"
NETLIFY_DIR="/root/homelab-docs/projekt-ai-website/proposals/"

echo "🔄 Syncing proposals from server to Netlify site..."
echo "📂 Source: $SOURCE_DIR"
echo "🌐 Destination: $NETLIFY_DIR"

# Create destination directory if it doesn't exist
mkdir -p "$NETLIFY_DIR"

# Count files before sync
SOURCE_COUNT=$(find "$SOURCE_DIR" -name "*.html" | wc -l)
NETLIFY_COUNT_BEFORE=$(find "$NETLIFY_DIR" -name "*.html" | wc -l)

echo "📊 Files before sync:"
echo "   Server: $SOURCE_COUNT proposals"
echo "   Netlify: $NETLIFY_COUNT_BEFORE proposals"

# Sync all HTML files (rsync preserves permissions and only copies newer files)
rsync -av --include="*.html" --exclude="*" "$SOURCE_DIR" "$NETLIFY_DIR"

# Count files after sync
NETLIFY_COUNT_AFTER=$(find "$NETLIFY_DIR" -name "*.html" | wc -l)

echo "📊 Files after sync:"
echo "   Netlify: $NETLIFY_COUNT_AFTER proposals"

# Navigate to Netlify site and deploy
cd /root/homelab-docs/projekt-ai-website

# Check git status
echo "📋 Checking git status..."
CHANGED_FILES=$(git status --porcelain | wc -l)

if [ $CHANGED_FILES -gt 0 ]; then
    echo "🔧 Changes detected, committing and deploying..."
    
    # Add all proposal files
    git add proposals/
    
    # Commit with informative message
    git commit -m "Sync proposals: $NETLIFY_COUNT_AFTER total proposals available"
    
    # Push to deploy
    git push
    
    echo "🚀 Deployment triggered! Proposals will be live in 2-3 minutes."
    echo "✅ URLs now accessible: https://projekt-ai.net/proposals/[filename]"
else
    echo "✅ No changes detected - all proposals already synced"
fi

echo ""
echo "🎯 SYNC COMPLETE!"
echo "   📈 Synced $SOURCE_COUNT server proposals to Netlify"
echo "   🌐 Live URLs: https://projekt-ai.net/proposals/"
echo "   ⏱️  Deployment time: 2-3 minutes" 