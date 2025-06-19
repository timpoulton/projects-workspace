#!/bin/bash

# PROJEKT AI - Style Enforcement Setup Script
# Sets up all the tools and rules to enforce Extra Medium design principles

echo "🎨 Setting up Extra Medium Style Enforcement..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Ensure we're in the project directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Must be run from the project root directory"
    exit 1
fi

# Check if .cursorrules exists
if [ ! -f ".cursorrules" ]; then
    echo "❌ Error: .cursorrules file not found!"
    echo "💡 The .cursorrules file contains the core style enforcement rules."
    exit 1
fi

# Check if style validator exists
if [ ! -f "scripts/style-validator.js" ]; then
    echo "❌ Error: Style validator not found!"
    echo "💡 The style validator automatically checks for design violations."
    exit 1
fi

# Make style validator executable
chmod +x scripts/style-validator.js
echo "✅ Style validator permissions set"

# Setup Git hooks
if [ -d ".git/hooks" ]; then
    # Make pre-commit hook executable
    if [ -f ".git/hooks/pre-commit" ]; then
        chmod +x .git/hooks/pre-commit
        echo "✅ Pre-commit hook activated"
    else
        echo "⚠️  Pre-commit hook not found - style validation won't run automatically"
    fi
else
    echo "⚠️  Not a Git repository - pre-commit hooks unavailable"
fi

# Test the style validator
echo ""
echo "🔍 Testing style validation..."
if node scripts/style-validator.js . > /dev/null 2>&1; then
    echo "✅ Style validator working correctly"
else
    echo "⚠️  Style validator found violations (this is normal for initial setup)"
fi

# Display usage instructions
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 STYLE ENFORCEMENT SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Available Commands:"
echo "  npm run style:validate          # Check current files for violations"
echo "  npm run style:validate-strict   # Strict validation with full report"
echo "  npm run pre-commit              # Run pre-commit validation manually"
echo ""
echo "🔧 How It Works:"
echo "  • .cursorrules defines the Extra Medium design principles"
echo "  • style-validator.js automatically scans for violations"
echo "  • Pre-commit hook prevents bad code from being committed"
echo "  • All changes must pass validation before deployment"
echo ""
echo "🚫 What's Forbidden:"
echo "  • Blue colors and gradients"
echo "  • Rounded corners (except circles)"
echo "  • Heavy shadows and effects"
echo "  • Non-Inter fonts"
echo "  • Legacy CSS files"
echo "  • Agency language"
echo ""
echo "✅ What's Required:"
echo "  • Clean, minimalist design"
echo "  • Extra Medium aesthetic"
echo "  • Personal branding focus"
echo "  • Approved color palette only"
echo "  • Performance optimization"
echo ""
echo "📖 For complete guidelines, see .cursorrules file"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" 