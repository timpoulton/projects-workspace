#!/bin/bash
# Test the enhanced scoring system with a high-value job

echo "🧪 Testing Enhanced Scoring System..."
echo "Sending a high-scoring job that should be 'MUST APPLY' priority"

curl -X POST http://localhost:8090/webhook/rss-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [{
      "title": "Automate Restaurant Inventory Management with Make.com",
      "description": "We are a high-end restaurant chain looking for an experienced automation expert to build a complex inventory management system using Make.com (formerly Integromat). This is a long-term project that requires advanced API integration skills to connect our POS system, supplier databases, and analytics platform. The ideal candidate will have experience with nightlife/hospitality industry and understand the unique challenges of restaurant operations.",
      "budget": "$5,000 - $8,000",
      "postedTime": "'$(date -u +%Y-%m-%dT%H:%M:%S)'.000Z",
      "proposalsCount": 3,
      "duration": "3 to 6 months",
      "client": {
        "paymentVerified": true,
        "totalSpent": 125000,
        "totalJobsPosted": 15,
        "totalHires": 12,
        "avgHourlyRate": 4.9,
        "location": {
          "country": "United States"
        }
      }
    }]
  }' | jq .

echo -e "\n✅ Test complete! Check the scoring breakdown above."
echo "View the generated proposal at: https://projekt-ai.net/proposals/" 