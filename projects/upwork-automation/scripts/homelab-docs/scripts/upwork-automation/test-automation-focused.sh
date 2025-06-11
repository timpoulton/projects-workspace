#!/bin/bash
# Test the automation-focused scoring system

echo "🧪 Testing Automation-Focused Scoring..."
echo "Sending a Make.com automation job that should score high"

curl -X POST http://localhost:8090/webhook/rss-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [{
      "title": "Need Make.com Expert to Automate Our Sales Process",
      "description": "We need an experienced Make.com (Integromat) expert to build a complex automation workflow. We want to integrate our CRM with email automation, connect multiple systems including Slack, Google Sheets, and our database. This is a long-term project requiring advanced API integration skills. Looking for someone who can create scalable solutions using no-code platforms.",
      "budget": "$3,000 - $5,000",
      "postedTime": "'$(date -u +%Y-%m-%dT%H:%M:%S)'.000Z",
      "proposalsCount": 4,
      "duration": "3 to 6 months",
      "client": {
        "paymentVerified": true,
        "totalSpent": 75000,
        "totalJobsPosted": 12,
        "totalHires": 10,
        "avgHourlyRate": 4.9,
        "location": {
          "country": "United States"
        }
      }
    }]
  }' | jq .

echo -e "\n\n🧪 Testing a job that should score lower (WordPress)"

curl -X POST http://localhost:8090/webhook/rss-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [{
      "title": "WordPress Developer Needed",
      "description": "Need a WordPress developer to create a simple website with basic features. Should know PHP and be able to work with themes and plugins.",
      "budget": "$500 - $1,000",
      "postedTime": "'$(date -u +%Y-%m-%dT%H:%M:%S)'.000Z",
      "proposalsCount": 25,
      "duration": "less than 1 month",
      "client": {
        "paymentVerified": false,
        "totalSpent": 500,
        "totalJobsPosted": 3,
        "totalHires": 1,
        "location": {
          "country": "India"
        }
      }
    }]
  }' | jq .

echo -e "\n✅ Tests complete! Check the scoring breakdowns above." 