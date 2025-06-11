# Upwork Proposal Generator Access Guide

This guide provides multiple ways to access the Upwork Proposal Generator, solving any potential connection issues.

## Access Options

The Upwork Proposal Generator can be accessed through several methods:

| Method | URL | Notes |
|--------|-----|-------|
| Direct IP with Port | http://192.168.1.107:5055 | Original URL, requires port number |
| Direct IP (Nginx Proxy) | http://192.168.1.107 | Easier to remember, uses standard port 80 |
| Domain Name | http://upwork-generator.local | Requires hosts file entry |
| Local HTML Dashboard | file:///root/homelab-docs/scripts/upwork-automation/dashboard.html | Open locally on server |
| Localhost | http://localhost:5055 | Only when on the server itself |

## Quick Setup Instructions

1. **Start the server**:
   ```bash
   cd /root/homelab-docs/scripts/upwork-automation && ./run-simple-generator.sh
   ```

2. **Check server accessibility**:
   ```bash
   cd /root/homelab-docs/scripts/upwork-automation && ./check-server-access.sh
   ```

3. **Set up Nginx proxy** (if needed for easier access):
   ```bash
   cd /root/homelab-docs/scripts/upwork-automation && ./setup-server-proxy.sh
   ```

4. **Open the dashboard** (on the server):
   ```bash
   cd /root/homelab-docs/scripts/upwork-automation && ./open-dashboard.sh
   ```

## Troubleshooting Connection Issues

If you're experiencing connection issues, try these solutions:

### 1. Use the Test Pages

Several test HTML files have been created to help diagnose issues:

- `/root/homelab-docs/scripts/upwork-automation/dashboard.html` - Full dashboard
- `/root/homelab-docs/scripts/upwork-automation/test-dashboard.html` - Simple test page
- `/root/homelab-docs/scripts/upwork-automation/server-test.html` - Server connectivity test
- `/var/www/html/upwork-generator-test.html` - Nginx test page

### 2. Network Connectivity

- Ensure you're on the same network as the server
- Try pinging the server: `ping 192.168.1.107`
- Check if there are any VPNs or network isolation preventing access

### 3. Client-side Solutions

- Add an entry to your hosts file:
  - Linux/Mac: `/etc/hosts`
  - Windows: `C:\Windows\System32\drivers\etc\hosts`
  
  Add this line: `192.168.1.107 upwork-generator.local`

- Use SSH tunneling:
  ```bash
  ssh -L 5055:localhost:5055 root@192.168.1.107
  ```
  Then access `http://localhost:5055` on your local machine

### 4. Server-side Checks

- Verify the server is running:
  ```bash
  ps aux | grep simple-upwork-generator.py
  ```

- Check if the port is open:
  ```bash
  ss -tuln | grep 5055
  ```

- Check server logs:
  ```bash
  tail -f /root/homelab-docs/scripts/upwork-automation/simple-generator.log
  ```

## Using the Nginx Proxy

If you're still having trouble, the Nginx proxy (set up with `setup-server-proxy.sh`) provides:

1. Access on standard HTTP port 80 instead of 5055
2. Better handling of connections
3. Multiple server names support (IP and domain name)

## SSH Tunneling Detailed Instructions

SSH tunneling creates a secure connection to the server and forwards ports to your local machine:

1. **From Linux/Mac**:
   ```bash
   ssh -L 5055:localhost:5055 root@192.168.1.107
   ```

2. **From Windows using PuTTY**:
   - Host: `192.168.1.107`
   - Port: `22`
   - Connection > SSH > Tunnels:
     - Source port: `5055`
     - Destination: `localhost:5055`
     - Click "Add"
   - Save and connect

3. **After connecting**, access the generator at:
   ```
   http://localhost:5055
   ```

## Technical Details

The Upwork Proposal Generator system consists of:

1. **Simple Generator Server**: Flask application running on port 5055
2. **Multi-Model AI Server**: Running on port 5001 (used by the generator)
3. **Nginx Reverse Proxy**: Redirects traffic from port 80 to 5055 for easier access

## Maintenance

- **Restart the server**:
  ```bash
  cd /root/homelab-docs/scripts/upwork-automation && pkill -f "simple-upwork-generator.py" && ./run-simple-generator.sh
  ```

- **Check server health**:
  ```bash
  cd /root/homelab-docs/scripts/upwork-automation && ./check-server-access.sh
  ```

- **Reconfigure Nginx proxy**:
  ```bash
  cd /root/homelab-docs/scripts/upwork-automation && ./setup-server-proxy.sh
  ``` 