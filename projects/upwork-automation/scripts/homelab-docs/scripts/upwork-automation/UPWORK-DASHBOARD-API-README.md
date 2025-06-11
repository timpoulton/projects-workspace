# Upwork Dashboard API System

**Version:** 1.0  
**Last Updated:** June 3, 2025  
**Status:** Production  
**Owner:** Timothy Poulton

## Overview

The Upwork Dashboard API System provides a modern, reliable API for delivering proposal data to the dashboard. This system solves persistent caching issues by implementing proper cache control headers, CORS support, and versioned responses.

## Architecture

```
Client (Dashboard) → Cloudflare → Nginx → API Server → Proposal Queue
```

### Components

1. **Flask API Server** (`api-server.py`)
   - Delivers proposal data with proper headers
   - Provides health check endpoint
   - Implements cache control
   - Runs on port 5050

2. **Nginx Proxy**
   - Handles SSL termination
   - Routes traffic to API server
   - Adds additional headers
   - Configured with api.projekt-ai.net subdomain

3. **Systemd Service**
   - Ensures API server runs continuously
   - Auto-restarts if crashed
   - Provides logging via journald

4. **Cloudflare Configuration**
   - Custom cache rules for API endpoint
   - DNS configuration for api subdomain

## Endpoints

### Proposals API

```
GET https://api.projekt-ai.net/api/proposals
```

**Response:**
```json
{
  "proposals": [...array of proposal objects...],
  "generated_at": "2025-06-03T04:30:45.123456",
  "total_count": 56,
  "version": "20250603043045"
}
```

### Health Check

```
GET https://api.projekt-ai.net/api/health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-06-03T04:30:45.123456",
  "service": "proposal-api"
}
```

## Installation

Run the standardized setup script:

```bash
cd /root/homelab-docs/scripts/upwork-automation
bash standardized-api-setup.sh
```

## Port Configuration

The API uses standardized port allocation:
- **API Server:** 5050 (Category E - External APIs)
- **Proposal Server:** 5001 (Already allocated)

To check for port conflicts:
```bash
bash check-port-conflicts.sh
```

## Troubleshooting

### Common Issues

1. **Cloudflare Caching**
   - Problem: Cloudflare aggressively caches API responses
   - Solution: Ensure cache rules are properly configured in Cloudflare dashboard

2. **Port Conflicts**
   - Problem: "Address already in use" errors when starting servers
   - Solution: Use the `check-port-conflicts.sh` script to identify and resolve conflicts

3. **Missing Proposals**
   - Problem: Dashboard shows fewer proposals than expected
   - Solution: Check the API response directly using the test page

### Diagnostic Commands

Check API service status:
```bash
systemctl status upwork-proposal-api
```

View logs:
```bash
journalctl -u upwork-proposal-api -f
```

Test API directly:
```bash
curl -I https://api.projekt-ai.net/api/proposals
curl https://api.projekt-ai.net/api/proposals | jq '.total_count'
```

Visit test page:
```
https://projekt-ai.net/api-test.html
```

## Security Considerations

- API does not require authentication (internal use only)
- Cloudflare provides DDoS protection
- HTTPS enforced for all connections
- No sensitive data exposed in API responses

## Maintenance

### Regular Maintenance Tasks

1. **Log Rotation**
   - API logs are handled by systemd/journald
   - Nginx logs should be rotated via logrotate

2. **Service Monitoring**
   - Check service status daily
   - Verify API health endpoint responds correctly

3. **Performance Optimization**
   - Monitor response times
   - Consider adding caching for read-heavy loads if needed

### Updating

To update the API server:

1. Stop the service: `systemctl stop upwork-proposal-api`
2. Edit the code in `api-server.py`
3. Start the service: `systemctl start upwork-proposal-api`
4. Check logs for any errors: `journalctl -u upwork-proposal-api -n 50`

## Future Improvements

- Add metrics collection (response time, error rate)
- Implement rate limiting for additional protection
- Add authentication for more sensitive operations
- Create a dashboard for API monitoring
- Implement database storage instead of file-based queue 