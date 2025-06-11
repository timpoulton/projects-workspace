#!/bin/bash

echo "🤖 OpenAI API Setup for Upwork Proposal Server"
echo "============================================"
echo ""
echo "To enable AI-powered proposal generation, you need an OpenAI API key."
echo ""
echo "1. Get your API key from: https://platform.openai.com/api-keys"
echo "2. Set it as an environment variable:"
echo ""
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "Or add it to your ~/.bashrc file:"
echo "   echo \"export OPENAI_API_KEY='your-api-key-here'\" >> ~/.bashrc"
echo "   source ~/.bashrc"
echo ""
echo "3. Test the AI-powered server:"
echo "   python3 scripts/upwork-automation/upwork-proposal-server.py"
echo ""
echo "Note: Without the API key, the server will fall back to basic pattern matching."
echo ""

# Check if API key is already set
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ OpenAI API key is already configured!"
else
    echo "❌ OpenAI API key is not set."
    echo ""
    read -p "Would you like to set it now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your OpenAI API key: " api_key
        echo ""
        echo "export OPENAI_API_KEY='$api_key'" >> ~/.bashrc
        export OPENAI_API_KEY="$api_key"
        echo "✅ API key saved to ~/.bashrc"
        echo "✅ API key exported for current session"
    fi
fi 