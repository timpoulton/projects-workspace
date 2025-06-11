# Club77 Check-in App Access

The Club77 check-in application is accessible at the following URLs:

## Internal Access
- http://localhost:3001 - Direct access to the Node.js application (container port)
- http://localhost:8081 - Access via port forwarding

## External Access
- http://guestlist.club77.com.au:8081 - Access from outside the network

## Port Forwarding Requirements
To make the application accessible from outside your network:

1. Forward port 8081 on your EdgeRouter to 192.168.1.107:8081 (already set up)
2. Ensure the port forwarding on the server is active

## Restarting Port Forwarding
If the port forwarding stops working, run:
```
bash /root/homelab-docs/club77-checkin/port-forward.sh
```

This script sets up a port forwarding from 8081 to the internal application port 3001.
