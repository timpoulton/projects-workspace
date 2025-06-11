#!/bin/bash

echo "1. Testing GET on test endpoint..."
curl -v http://localhost:3001/api/webhooks/test

echo -e "\n\n2. Testing POST to test endpoint..."
curl -v -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}' \
  http://localhost:3001/api/webhooks/test

echo -e "\n\n3. Testing HTTPS endpoint..."
curl -v -k https://guestlist.club77.com.au/api/webhooks/test 