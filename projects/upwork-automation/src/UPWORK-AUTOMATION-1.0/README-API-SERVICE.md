# Upwork Proposal API Service

## Overview

This is a modern, reliable API service for delivering Upwork proposal data to the dashboard. It addresses the caching issues and provides a more standard and compliant approach than using static JSON files.

## Key Features

- **Proper API Endpoints**: RESTful API design with proper JSON responses
- **Cache Control Headers**: Prevents aggressive caching by browsers and CDNs
- **CORS Support**: Allows secure cross-origin requests
- **Versioned Responses**: Each response includes timestamp and version info
- **Health Checks**: Easily monitor API health
- **Proper Logging**: Tracks API usage and errors
- **Systemd Service**: Runs as a system service with auto-restart

## Benefits over Static JSON Files

1. **Bypass Cloudflare Caching**: The API is designed to prevent caching issues that affect static files
2. **Real-time Data**: Always serves the latest data without relying on cache busting techniques
3. **Universal Compatibility**: Follows web standards for maximum compatibility
4. **Better Error Handling**: Provides meaningful error responses
5. **Monitoring Capabilities**: Logs access and tracks performance
6. **Scalability**: Can be easily extended with additional endpoints

## Technical Details

The API service consists of:

- **Flask API Server**: Lightweight Python-based API server
- **Nginx Proxy**: Handles SSL termination and additional headers
- **Systemd Service**: Ensures the API runs continuously
- **DNS Configuration**: Custom api.projekt-ai.net subdomain

## Installation

Run the setup script to install and configure everything:

```bash
bash /root/homelab-docs/scripts/upwork-automation/api-service-setup.sh
```

## API Endpoints

### Get Proposals

```
GET https://api.projekt-ai.net/api/proposals
```

**Response Format:**
```json
{
  "proposals": [...],
  "generated_at": "2025-06-03T04:30:45.123456",
  "total_count": 56,
  "version": "20250603043045"
}
```

### Health Check

```
GET https://api.projekt-ai.net/api/health
```

**Response Format:**
```json
{
  "status": "ok",
  "timestamp": "2025-06-03T04:30:45.123456",
  "service": "proposal-api"
}
```

## Maintenance

### View Service Status
```bash
systemctl status upwork-proposal-api
```

### View Logs
```bash
journalctl -u upwork-proposal-api -f
```

### Restart Service
```bash
systemctl restart upwork-proposal-api
```

## Integration with Dashboard

The dashboard HTML has been updated to use the API endpoint instead of static JSON files. This provides a more reliable experience and eliminates caching issues.

## Test Page

A test page is available at:
```
https://projekt-ai.net/api-test.html
```

This page allows you to test the API and verify that it's working correctly.

## Troubleshooting

If you encounter issues:

1. Check if the API service is running with `systemctl status upwork-proposal-api`
2. Check the logs with `journalctl -u upwork-proposal-api -f`
3. Verify that the DNS record for api.projekt-ai.net is correctly pointing to your server
4. Check that Nginx is properly configured with `nginx -t`
5. Try accessing the test page at https://projekt-ai.net/api-test.html 