# Club77 Check-In Project Summary

## System Overview
- **Purpose:** Manage guest check-ins at Club77 events
- **Components:**
  - Webflow form for guest registration
  - Webhook endpoint to receive form submissions
  - MySQL database to store events and guests
  - Web interface for staff to manage check-ins
- **Deployment:** Docker containers (app + db)
- **Access URL:** guestlist.club77.com.au:8081

## Current Status
- The webhook is successfully receiving data from Webflow forms
- Guest data is being stored in the MySQL database
- Container setup is functioning correctly
- External access has been configured using port forwarding (8081 → 3001)

## Testing Status
- Webhook tests are successful (via test-webhook.sh)
- App accessibility verified through port 8081
- Port forwarding is working correctly

## Technical Details
- **Port:** 3001 (container), 8081 (external)
- **Database:** MySQL (club77_db container)
- **Technology:** Node.js, Express, EJS templates
- **Port Forwarding:** Using socat to forward 8081 → 3001 (see port-forward.sh)

## Files of Interest
- `app.js` - Main application file
- `routes/webhooks.js` - Webhook endpoint implementation
- `routes/events.js` - Event display logic
- `routes/guests.js` - Guest management logic
- `models/` - Database models
- `views/` - UI templates

## Next Steps
1. Set up port forwarding on the EdgeRouter (port 8081 → 192.168.1.107:8081)
2. Add a firewall rule to the EdgeRouter's WAN_IN ruleset for port 8081
3. Test the application from outside the network
4. Verify mobile usability for event staff
5. If the port forwarding stops working, run `/root/homelab-docs/club77-checkin/port-forward.sh` 