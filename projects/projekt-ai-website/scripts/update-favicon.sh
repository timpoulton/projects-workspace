#!/bin/bash

# PROJEKT AI - Favicon Update Script
# Updates the website favicon from a source image file

echo "🎨 Updating Projekt AI Favicon..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if source file is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide the path to your favicon image"
    echo ""
    echo "📖 Usage:"
    echo "  ./scripts/update-favicon.sh /path/to/your/icon.png"
    echo "  ./scripts/update-favicon.sh \"C:\\Users\\Your Name\\Downloads\\icon48.png\""
    echo ""
    echo "💡 Supported formats: PNG, JPG, ICO, SVG"
    echo "📏 Recommended size: 48x48px or larger"
    exit 1
fi

SOURCE_FILE="$1"

# Check if source file exists (try different path formats for Windows)
if [ ! -f "$SOURCE_FILE" ]; then
    # Try Windows path conversion
    WIN_PATH=$(echo "$SOURCE_FILE" | sed 's|\\|/|g' | sed 's|C:|/mnt/c|g')
    if [ -f "$WIN_PATH" ]; then
        SOURCE_FILE="$WIN_PATH"
        echo "✅ Found file using Windows path conversion: $WIN_PATH"
    else
        echo "❌ Error: Source file not found: $SOURCE_FILE"
        echo "💡 Make sure the file path is correct and the file exists"
        exit 1
    fi
fi

# Ensure we're in the project directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Must be run from the project root directory"
    exit 1
fi

# Create logos directory if it doesn't exist
mkdir -p assets/img/logos

# Copy and rename the favicon
echo "📋 Copying favicon from: $SOURCE_FILE"
cp "$SOURCE_FILE" assets/img/logos/favicon.png

if [ $? -eq 0 ]; then
    echo "✅ Favicon copied successfully!"
    
    # Check if it's a reasonable size
    if command -v identify >/dev/null 2>&1; then
        SIZE=$(identify -format "%wx%h" assets/img/logos/favicon.png 2>/dev/null)
        if [ ! -z "$SIZE" ]; then
            echo "📏 Image size: $SIZE"
        fi
    fi
    
    # Commit the change
    echo "📝 Committing favicon update..."
    git add assets/img/logos/favicon.png
    git add index.html
    git commit -m "feat: Update favicon with new icon"
    
    if [ $? -eq 0 ]; then
        echo "✅ Favicon committed to git"
        
        # Ask about deployment
        echo ""
        echo "🚀 Ready to deploy?"
        echo "   Run: git push"
        echo "   Or: npm run build:prod && git push"
        echo ""
        echo "🌐 The new favicon will appear on projekt-ai.net after deployment"
    else
        echo "⚠️  Git commit failed, but favicon was updated"
    fi
    
else
    echo "❌ Error: Failed to copy favicon"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Favicon update complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" 