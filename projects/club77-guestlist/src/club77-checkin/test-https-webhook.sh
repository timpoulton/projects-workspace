#!/bin/bash

# Simple script to test the HTTPS webhook endpoint

echo "Testing HTTPS endpoint for the Club77 guest check-in system..."
curl -v -X POST \
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

echo "Test complete." 