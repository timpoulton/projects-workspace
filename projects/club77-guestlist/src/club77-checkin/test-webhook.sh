#!/bin/bash

echo "1. Testing HTTP endpoint (direct to container)..."
curl -X POST \
  -H "Content-Type: application/json" \
  -H "x-webflow-webhook-secret: 7ba02129304569b5b6edbc622b1600371e9cb9e46bd5f760f701450d4aa09899" \
  -d '{
    "event_name": "Test Event HTTP",
    "event_date": "2025-06-15",
    "first_name": "Test",
    "last_name": "User HTTP",
    "email": "test-http@example.com",
    "dob": "1990-01-01"
  }' \
  http://localhost:3001/api/webhooks/guest-list-registration

echo -e "\n2. Testing HTTPS endpoint (with certificate verification skipped)..."
curl -X POST \
  -H "Content-Type: application/json" \
  -H "x-webflow-webhook-secret: 7ba02129304569b5b6edbc622b1600371e9cb9e46bd5f760f701450d4aa09899" \
  -d '{
    "event_name": "Test Event HTTPS",
    "event_date": "2025-06-16",
    "first_name": "Test",
    "last_name": "User HTTPS",
    "email": "test-https@example.com",
    "dob": "1990-01-01"
  }' \
  -k https://guestlist.club77.com.au/api/webhooks/guest-list-registration

echo -e "\n3. Testing endpoint accessibility (GET request)..."
curl -k https://guestlist.club77.com.au/api/webhooks/guest-list-registration

# Output the latest guest entries to confirm it worked
echo -e "\n\nChecking latest guest entries:"
docker exec club77_db mysql -u root -plkj654 club77 -e "SELECT * FROM guests ORDER BY id DESC LIMIT 5;" 