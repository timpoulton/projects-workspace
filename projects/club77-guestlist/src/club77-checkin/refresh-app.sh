#!/bin/bash

echo "====== Club77 Guest Check-In App Data Refresh ======"
echo "This script will verify and refresh data in the application"

# Check if the containers are running
echo "Checking if containers are running..."
if docker ps | grep club77_app > /dev/null; then
    echo "✅ App container is running"
else 
    echo "❌ App container is not running!"
    echo "Attempting to start containers..."
    cd /root/homelab-docs/club77-checkin && docker-compose up -d
    sleep 5
fi

# Check database for events
echo -e "\n=== Events in Database ==="
docker exec club77_db mysql -u root -p'lkj654' club77 -e "SELECT id, name, event_date, created_at FROM events ORDER BY event_date DESC LIMIT 10;"

# Check database for recent guests
echo -e "\n=== Recent Guests in Database ==="
docker exec club77_db mysql -u root -p'lkj654' club77 -e "SELECT id, event_id, first_name, last_name, email, checked_in, created_at FROM guests ORDER BY created_at DESC LIMIT 10;"

# Restart the app container to refresh connections
echo -e "\n=== Restarting App Container ==="
docker restart club77_app
sleep 5

# Display connection information
echo -e "\n=== App Information ==="
echo "App should be running at: http://guestlist.club77.com.au:8080"
echo "Internal URL: http://localhost:3001"

# Check if app is responding on port 3001
echo -e "\nTesting direct app access..."
if curl -s localhost:3001 > /dev/null; then
    echo "✅ App is responding on port 3001!"
else
    echo "❌ App is not responding on port 3001"
    echo "Recent logs from app container:"
    docker logs club77_app --tail 20
fi 