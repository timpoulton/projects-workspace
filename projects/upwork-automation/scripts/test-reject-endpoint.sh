#!/bin/bash

# Get the first proposal ID to test with
echo "🔍 Getting a proposal ID to test rejection..."
PROPOSAL_ID=$(curl -s http://localhost:5001/api/proposals | jq -r '.[0].job_id')

if [ -z "$PROPOSAL_ID" ] || [ "$PROPOSAL_ID" == "null" ]; then
  echo "❌ Failed to get a valid proposal ID"
  exit 1
fi

echo "📋 Testing rejection for proposal ID: $PROPOSAL_ID"

# Try the reject endpoint
echo "🔄 Calling reject endpoint..."
curl -i -X POST -H "Content-Type: application/json" -d "{\"id\":\"$PROPOSAL_ID\"}" http://localhost:5001/api/proposals/reject

# Check if the proposal was actually removed
echo -e "\n\n🔍 Checking if proposal was removed..."
sleep 1
REMAINING_COUNT=$(curl -s http://localhost:5001/api/proposals | jq ". | map(select(.job_id == \"$PROPOSAL_ID\")) | length")

if [ "$REMAINING_COUNT" -eq "0" ]; then
  echo "✅ SUCCESS: Proposal was successfully removed!"
else
  echo "❌ FAILED: Proposal still exists in the queue ($REMAINING_COUNT found)"
fi

# Check the total count
TOTAL_COUNT=$(curl -s http://localhost:5001/api/proposals | jq ". | length")
echo "📊 Total proposals remaining: $TOTAL_COUNT"

# Get the proposals.json file to see if it was updated
echo "🔍 Checking web data file..."
WEB_COUNT=$(cat /var/www/projekt-ai.net/data/proposals.json | jq '.proposals | length')
echo "📊 Web data file contains $WEB_COUNT proposals"

echo "🔄 Running sync script to update web data..."
bash /root/homelab-docs/scripts/upwork-automation/sync-dashboard-data.sh --force

# Final counts
echo "📊 Final API count: $(curl -s http://localhost:5001/api/proposals | jq ". | length")"
echo "📊 Final web data count: $(cat /var/www/projekt-ai.net/data/proposals.json | jq '.proposals | length')" 