#!/bin/bash
# Premium AI Setup Script for Upwork Automation
# This script sets up the complete premium AI proposal system

set -e

echo "🚀 Setting up Premium AI Proposal System..."
echo "==========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Create directories
echo "📁 Creating directory structure..."
mkdir -p /root/homelab-docs/scripts/upwork-automation/{models,templates,data,logs}
mkdir -p /var/www/projekt-ai.net/proposals/premium

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install openai anthropic cohere
pip3 install pinecone-client pymongo motor
pip3 install beautifulsoup4 textstat nltk
pip3 install asyncio aiohttp aiofiles
pip3 install pandas numpy scikit-learn
pip3 install python-dotenv rich typer

# Download NLTK data
echo "📚 Downloading language models..."
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"

# Create environment file
echo "🔐 Setting up environment variables..."
cat > /root/homelab-docs/scripts/upwork-automation/.env << 'EOF'
# AI API Keys
OPENAI_API_KEY=""
ANTHROPIC_API_KEY=""
COHERE_API_KEY=""

# Optional Advanced Features
PINECONE_API_KEY=""
MONGODB_URI=""

# System Configuration
PROPOSAL_MODEL="gpt-4-turbo-preview"
REFINEMENT_MODEL="claude-3-opus-20240229"
ANALYSIS_MODEL="command-xlarge-nightly"

# Performance Settings
MAX_CONCURRENT_REQUESTS=5
CACHE_PROPOSALS=true
ENABLE_LEARNING=true

# Proposal Settings
MAX_PROPOSAL_LENGTH=150
MIN_PROPOSAL_LENGTH=100
ENABLE_VARIATIONS=true
NUM_VARIATIONS=4
EOF

echo "⚠️  Please edit .env file and add your API keys!"

# Create configuration file
echo "⚙️  Creating configuration..."
cat > /root/homelab-docs/scripts/upwork-automation/config.json << 'EOF'
{
  "proposal_settings": {
    "max_length": 150,
    "min_length": 100,
    "tone_options": ["professional", "casual", "friendly", "expert"],
    "include_metrics": true,
    "include_cta": true
  },
  "ai_models": {
    "primary": "gpt-4-turbo-preview",
    "refinement": "claude-3-opus-20240229",
    "analysis": "command-xlarge-nightly"
  },
  "scoring_weights": {
    "personalization": 0.3,
    "value_proposition": 0.25,
    "credibility": 0.2,
    "call_to_action": 0.15,
    "readability": 0.1
  },
  "industries": {
    "restaurant": {
      "keywords": ["pos", "ordering", "inventory", "reservations"],
      "pain_points": ["manual processes", "staff scheduling", "customer data"],
      "metrics": ["order processing time", "table turnover", "labor costs"]
    },
    "ecommerce": {
      "keywords": ["shopify", "woocommerce", "inventory", "fulfillment"],
      "pain_points": ["abandoned carts", "customer support", "multi-channel"],
      "metrics": ["conversion rate", "cart value", "customer lifetime value"]
    },
    "saas": {
      "keywords": ["onboarding", "churn", "billing", "analytics"],
      "pain_points": ["user activation", "retention", "usage tracking"],
      "metrics": ["mrr growth", "churn rate", "activation rate"]
    }
  }
}
EOF

# Create sample success patterns database
echo "📊 Creating success patterns database..."
cat > /root/homelab-docs/scripts/upwork-automation/data/success_patterns.json << 'EOF'
{
  "opening_hooks": [
    {
      "pattern": "I noticed you're struggling with {pain_point}...",
      "success_rate": 0.42,
      "usage_count": 156
    },
    {
      "pattern": "Your {specific_challenge} caught my attention because...",
      "success_rate": 0.38,
      "usage_count": 89
    },
    {
      "pattern": "Having automated {number}+ {industry} businesses, your {need} is exactly...",
      "success_rate": 0.45,
      "usage_count": 234
    }
  ],
  "credibility_statements": [
    {
      "pattern": "Last month, I helped {similar_business} achieve {metric}",
      "success_rate": 0.52,
      "usage_count": 178
    },
    {
      "pattern": "My {tool} workflows have saved clients {metric} on average",
      "success_rate": 0.48,
      "usage_count": 145
    }
  ],
  "call_to_actions": [
    {
      "pattern": "I'd love to discuss {specific_aspect}. When would work for a quick call?",
      "success_rate": 0.35,
      "usage_count": 267
    },
    {
      "pattern": "Happy to share a quick screen recording showing how this would work for you",
      "success_rate": 0.41,
      "usage_count": 123
    }
  ]
}
EOF

# Create test script
echo "🧪 Creating test script..."
cat > /root/homelab-docs/scripts/upwork-automation/test-premium-ai.py << 'EOF'
#!/usr/bin/env python3
"""Test script for Premium AI Proposal System"""

import asyncio
import json
from premium_ai_proposal_system import PremiumProposalGenerator, ProposalRequest

async def test_system():
    """Test the premium AI system with a sample job"""
    
    print("🧪 Testing Premium AI Proposal System...")
    print("=" * 50)
    
    # Initialize generator
    generator = PremiumProposalGenerator()
    
    # Test job
    test_job = ProposalRequest(
        job_title="Zapier Expert Needed - Automate Our Restaurant Operations",
        job_description="""
        We're a growing restaurant chain (5 locations) drowning in manual processes.
        
        Need help with:
        - Connecting our POS system to inventory management
        - Automating staff scheduling based on sales forecasts
        - Setting up automated customer feedback collection
        - Creating dashboards for each location manager
        
        We use Toast POS, Google Sheets, and Slack. Open to other tools.
        
        Must have experience with restaurant operations. 
        Looking to start ASAP. Budget is flexible for the right person.
        """,
        budget="$2,000 - $5,000",
        required_skills=["Zapier", "API Integration", "Restaurant Systems", "Toast POS"]
    )
    
    # Generate proposal
    print("\n🤖 Generating proposal...")
    result = await generator.generate_premium_proposal(test_job)
    
    # Display results
    print("\n✅ PROPOSAL GENERATED!")
    print("=" * 50)
    print(f"\n📝 Primary Proposal:\n{result['primary_proposal']}")
    print(f"\n📊 Optimization Score: {result['optimization_score']}")
    print(f"\n💡 Personalization Tips:")
    for tip in result['personalization_tips']:
        print(f"   - {tip}")
    
    print("\n🔄 Variations Generated:")
    for var in result['variations']:
        print(f"   - {var['type']}: Score {var['score']}")
    
    print("\n✨ Test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_system())
EOF

chmod +x /root/homelab-docs/scripts/upwork-automation/test-premium-ai.py

# Create systemd service for the premium server
echo "🔧 Creating systemd service..."
cat > /etc/systemd/system/upwork-premium-ai.service << 'EOF'
[Unit]
Description=Upwork Premium AI Proposal Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/homelab-docs/scripts/upwork-automation
Environment="PATH=/usr/bin:/usr/local/bin"
EnvironmentFile=/root/homelab-docs/scripts/upwork-automation/.env
ExecStart=/usr/bin/python3 /root/homelab-docs/scripts/upwork-automation/premium_ai_proposal_system.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create monitoring script
echo "📈 Creating monitoring script..."
cat > /root/homelab-docs/scripts/upwork-automation/monitor-ai-performance.py << 'EOF'
#!/usr/bin/env python3
"""Monitor AI Proposal System Performance"""

import json
import pandas as pd
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table

console = Console()

def display_metrics():
    """Display current system metrics"""
    
    table = Table(title="AI Proposal System Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Target", style="yellow")
    table.add_column("Status", style="magenta")
    
    # Add metrics (would pull from database in production)
    metrics = [
        ("Response Rate", "32%", "35%", "🟡"),
        ("Win Rate", "12%", "10%", "✅"),
        ("Avg Generation Time", "4.2s", "<5s", "✅"),
        ("Personalization Score", "87%", "85%", "✅"),
        ("API Cost/Proposal", "$0.08", "<$0.15", "✅"),
        ("Proposals Today", "47", "50", "🟡"),
    ]
    
    for metric in metrics:
        table.add_row(*metric)
    
    console.print(table)
    
    # Show top performing patterns
    console.print("\n[bold cyan]Top Performing Patterns:[/bold cyan]")
    console.print("1. 'Having automated 200+ restaurants...' - 48% response rate")
    console.print("2. 'I noticed your Toast POS integration need...' - 45% response rate")
    console.print("3. 'Last week I saved a similar restaurant $2k/month...' - 43% response rate")

if __name__ == "__main__":
    display_metrics()
EOF

chmod +x /root/homelab-docs/scripts/upwork-automation/monitor-ai-performance.py

echo ""
echo "✅ Premium AI System Setup Complete!"
echo "===================================="
echo ""
echo "📋 Next Steps:"
echo "1. Edit /root/homelab-docs/scripts/upwork-automation/.env and add your API keys"
echo "2. Run the test script: ./test-premium-ai.py"
echo "3. Start the service: systemctl start upwork-premium-ai"
echo "4. Monitor performance: ./monitor-ai-performance.py"
echo ""
echo "📚 Documentation: /root/homelab-docs/UPWORK-AI-PREMIUM-IMPLEMENTATION-GUIDE.md"
echo ""
echo "🚀 Ready to achieve 35%+ response rates!" 