#!/bin/bash

echo "🧪 Testing Simple Upwork Proposal System..."
echo ""

# Test job data
TEST_JOB='{
  "title": "CRM Integration Automation for Marketing Agency",
  "description": "We need help connecting our CRM (HubSpot) to our email marketing platform (Mailchimp) and project management tool (Asana). Currently doing everything manually which is taking hours each week. Need someone who can create automated workflows to sync contacts, trigger campaigns based on CRM data, and create tasks automatically when deals move stages.",
  "budget": 2500,
  "url": "https://www.upwork.com/jobs/~021234567890abcdef",
  "client": {
    "name": "Marketing Solutions Inc",
    "paymentVerified": true,
    "jobsPosted": 15,
    "totalSpent": 25000
  },
  "skills": ["automation", "zapier", "api integration", "crm"],
  "posted": "2025-06-01T20:00:00Z"
}'

# Send to our simple server
echo "📨 Sending job to simple server..."
RESPONSE=$(curl -s -X POST "http://localhost:8090/webhook/rss-jobs" \
  -H "Content-Type: application/json" \
  -d "{\"jobs\": [$TEST_JOB]}")

echo "Response: $RESPONSE"
echo ""

# Check the queue
echo "📋 Checking proposal queue..."
python3 scripts/upwork-automation/view-proposals.py

echo ""
echo "✅ Test complete!"
echo ""
echo "To view a specific message, use:"
echo "  python3 scripts/upwork-automation/view-proposals.py show 1"
echo ""
echo "To clear the queue:"
echo "  python3 scripts/upwork-automation/view-proposals.py clear" 