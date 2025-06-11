# Upwork Proposal API Service Documentation
**Version:** 1.0.0  
**Date:** June 3, 2025  
**Author:** System Admin  
**Status:** Production

## Overview

The Upwork Proposal API Service provides a standardized, reliable interface for accessing proposal data for the Upwork Dashboard. This service replaces the previous static file-based approach with a proper API that handles caching, CORS, and provides consistent data structure.

## Architecture

The service consists of:

1. **Flask API Server** - Serves proposal data with proper headers
2. **Nginx Reverse Proxy** - Handles SSL and domain routing
3. **Systemd Service** - Ensures the API server runs continuously
4. **DNS Configuration** - Makes the API accessible via api.projekt-ai.net

```
Client Request → api.projekt-ai.net → Nginx → API Server (port 5050) → proposal-queue.json
```

## Endpoints

### Proposals Endpoint

- **URL:** https://api.projekt-ai.net/api/proposals
- **Method:** GET
- **Description:** Returns all proposals with metadata
- **Response Format:**
  ```json
  {
    "proposals": [ /* array of proposal objects */ ],
    "generated_at": "2025-06-03T04:33:48.123456",
    "total_count": 42,
    "version": "20250603043348"
  }
  ```

### Health Endpoint

- **URL:** https://api.projekt-ai.net/api/health
- **Method:** GET
- **Description:** Simple health check to verify service status
- **Response Format:**
  ```json
  {
    "status": "ok",
    "timestamp": "2025-06-03T04:33:48.123456",
    "service": "proposal-api"
  }
  ```

## Key Features

1. **Proper Cache Control**
   - Headers prevent browser caching
   - Enables real-time dashboard updates

2. **CORS Support**
   - Cross-origin resource sharing enabled
   - Works with any client regardless of domain

3. **Consistent Data Format**
   - Standardized proposal structure
   - Metadata for tracking freshness

4. **Error Handling**
   - Graceful handling of missing files
   - Proper logging of issues

5. **Performance**
   - Lightweight Flask implementation
   - Efficient JSON processing

## Management

### Service Control

```bash
# Check service status
systemctl status upwork-proposal-api

# Restart service
systemctl restart upwork-proposal-api

# View logs
journalctl -u upwork-proposal-api -f
```

### File Locations

- **API Server:** `/root/homelab-docs/scripts/upwork-automation/api-server.py`
- **Service Definition:** `/etc/systemd/system/upwork-proposal-api.service`
- **Nginx Config:** `/etc/nginx/sites-available/upwork-proposal-api.conf`
- **Data Source:** `/root/homelab-docs/scripts/upwork-automation/proposal-queue.json`
- **Logs:** `/root/homelab-docs/scripts/upwork-automation/api-server.log`

### API Testing

A test page is available at https://projekt-ai.net/api-test.html that provides:

- Interactive API testing
- Response inspection
- Headers verification

## DNS Configuration

This service requires a DNS A record:

```
Type: A
Name: api
Content: [Server IP]
Proxy status: Proxied (via Cloudflare)
```

Additionally:
- Disable Rocket Loader for this subdomain
- Create a Cache Rule to bypass cache for the API subdomain

## Troubleshooting

### Common Issues

1. **API returns empty proposals array**
   - Check if proposal-queue.json exists and is valid JSON
   - Verify file permissions allow reading

2. **Service fails to start**
   - Check logs: `journalctl -u upwork-proposal-api -f`
   - Verify port 5050 isn't used by another service

3. **Dashboard not updating**
   - Verify dashboard is using the new API endpoint
   - Check browser console for CORS or mixed content errors
   - Clear browser cache

### Solutions

- **Reset API:** `systemctl restart upwork-proposal-api`
- **Repair permissions:** `chmod 644 /root/homelab-docs/scripts/upwork-automation/proposal-queue.json`
- **Rebuild data:** Run the data sync script if data is corrupted

## Integration with Dashboard

The Upwork Dashboard now uses this API instead of static JSON files. The dashboard has been updated to:

1. Use the proper API endpoint
2. Handle the new response format
3. Include cache-busting query parameters

This integration ensures real-time updates without caching issues.

## Security Considerations

- The API is publicly accessible but read-only
- No authentication is required as data is non-sensitive
- Cloudflare provides additional DDoS protection
- Rate limiting can be added if needed

## Future Improvements

1. Add authentication for write operations
2. Implement proposal filtering endpoints
3. Add performance metrics collection
4. Create a status dashboard for monitoring

## Related Documentation

- [Upwork Dashboard API README](./UPWORK-DASHBOARD-API-README.md)
- [README-API-SERVICE](./README-API-SERVICE.md)
- [Upwork Automation Strategy](../../UPWORK-AUTOMATION-STRATEGY.md) 