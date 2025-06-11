#!/bin/bash
# Upwork Proposal Automation Setup Script
# Installs dependencies and prepares the automation system

set -e

echo "🚀 Setting up Upwork Proposal Automation System"
echo "================================================"

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p jobs logs config

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install feedparser requests || {
    echo "ℹ️  feedparser and requests may already be installed"
}

# Make scripts executable
echo "🔧 Setting up permissions..."
chmod +x upwork-rss-monitor.py

# Create systemd service for automation
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/upwork-automation.service << 'EOL'
[Unit]
Description=Upwork Proposal Automation Monitor
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/homelab-docs/scripts/upwork-automation
ExecStart=/usr/bin/python3 /root/homelab-docs/scripts/upwork-automation/upwork-rss-monitor.py
Restart=always
RestartSec=1800

[Install]
WantedBy=multi-user.target
EOL

# Create cron job for regular monitoring
echo "⏰ Setting up cron job..."
(crontab -l 2>/dev/null; echo "*/30 * * * * cd /root/homelab-docs/scripts/upwork-automation && python3 upwork-rss-monitor.py >> logs/monitor.log 2>&1") | crontab -

# Test RSS feed access
echo "🌐 Testing RSS feed access..."
python3 -c "
import feedparser
test_url = 'https://www.upwork.com/ab/feed/jobs/rss?q=automation&sort=recency'
print(f'Testing feed: {test_url}')
feed = feedparser.parse(test_url)
print(f'✅ RSS feed accessible: {len(feed.entries)} entries found')
" || {
    echo "⚠️  RSS feed test failed - may need network connectivity"
}

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Test the system:     python3 upwork-rss-monitor.py"
echo "2. Start the service:   systemctl start upwork-automation"
echo "3. Enable auto-start:   systemctl enable upwork-automation"
echo "4. Check logs:          tail -f logs/monitor.log"
echo ""
echo "📋 CONFIGURATION:"
echo "- Edit config.json to customize RSS feeds and keywords"
echo "- Check jobs/ directory for generated proposals"
echo "- Monitor logs/ directory for automation activity"
echo ""
echo "🚀 READY TO AUTOMATE! 🚀" 