# MUZEEK API MAINTENANCE GUIDE
## Club77 Check-in App Integration

**Last Updated:** 2025-05-26  
**Status:** ✅ WORKING - API Successfully Integrated

---

## 🎯 OVERVIEW

The Club77 Check-in App successfully integrates with the Muzeek API to automatically sync event data. This document provides comprehensive guidance for maintaining this critical API connection.

### Current Status
- ✅ **API Connection**: Working with proper headers
- ✅ **Authentication**: Token-based authentication functional
- ✅ **Data Sync**: 10+ events successfully syncing
- ✅ **Database Schema**: All required columns present

---

## 🔧 API CONFIGURATION

### Authentication
- **API Token**: `mzku-MS03MTU2NTIxODUtYjI2ZjBlY2FkMDA2MjcwMDljYmI4OWU2NDA5ZjEyZDQ1ZGU2NzdiOQ`
- **Base URL**: `https://muzeek.com/i/api`
- **Token Location**: Environment variable `MUZEEK_API_TOKEN` in docker-compose.yml

### Critical Headers (Required for localhost/container requests)
```javascript
{
  'token': this.apiToken,
  'accept': 'application/json',
  'User-Agent': 'Club77-CheckinApp/1.0 (https://checkin.projekt-ai.net)',
  'Origin': 'https://checkin.projekt-ai.net',
  'Referer': 'https://checkin.projekt-ai.net/',
  'Host': 'muzeek.com',
  'Accept-Language': 'en-US,en;q=0.9',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'cross-site'
}
```

**⚠️ CRITICAL**: The headers above are essential for API requests from Docker containers. Without them, you'll get "Error retrieving API token in request".

---

## 📊 DATABASE SCHEMA

### Required Columns in `events` Table
```sql
-- Core fields
id INT PRIMARY KEY AUTO_INCREMENT
name VARCHAR(255) NOT NULL
event_date DATE NOT NULL
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

-- Muzeek integration fields
muzeek_id VARCHAR(255) UNIQUE NULL
muzeek_published BOOLEAN NOT NULL DEFAULT FALSE
description TEXT NULL
artwork_url VARCHAR(500) NULL
start_time VARCHAR(50) NULL DEFAULT '10:00 PM'
end_time VARCHAR(50) NULL DEFAULT '5:00 AM'
venue VARCHAR(255) NULL DEFAULT '77 William St, Darlinghurst'
is_live BOOLEAN NOT NULL DEFAULT TRUE
last_synced DATETIME NULL
```

### Schema Migration Commands
```bash
# Add missing columns if needed
docker-compose exec -T db mysql -u root -plkj654 club77 -e "
ALTER TABLE events 
ADD COLUMN muzeek_id VARCHAR(255) NULL UNIQUE,
ADD COLUMN muzeek_published BOOLEAN NOT NULL DEFAULT FALSE,
ADD COLUMN description TEXT NULL,
ADD COLUMN artwork_url VARCHAR(500) NULL,
ADD COLUMN start_time VARCHAR(50) NULL DEFAULT '10:00 PM',
ADD COLUMN end_time VARCHAR(50) NULL DEFAULT '5:00 AM',
ADD COLUMN venue VARCHAR(255) NULL DEFAULT '77 William St, Darlinghurst',
ADD COLUMN is_live BOOLEAN NOT NULL DEFAULT TRUE,
ADD COLUMN last_synced DATETIME NULL;
"
```

---

## 🚀 API ENDPOINTS

### Test Connection
```bash
curl "http://localhost:3001/api/sync/muzeek/test"
```
**Expected Response:**
```json
{
  "success": true,
  "message": "Muzeek API connection successful",
  "status": 200,
  "eventCount": 20
}
```

### Sync Events
```bash
curl -X POST "http://localhost:3001/api/sync/muzeek/events" -H "Content-Type: application/json"
```
**Expected Response:**
```json
{
  "success": true,
  "message": "Muzeek sync completed",
  "stats": {
    "total": 10,
    "created": 10,
    "updated": 0,
    "errors": 0
  }
}
```

### Check Sync Status
```bash
curl "http://localhost:3001/api/sync/muzeek/status"
```

---

## 🔍 TROUBLESHOOTING

### Common Issues & Solutions

#### 1. "Error retrieving API token in request"
**Cause**: Missing or incorrect headers for localhost/container requests  
**Solution**: Ensure all headers are present in the axios configuration (see Configuration section)

#### 2. "Unknown column 'description' in 'field list'"
**Cause**: Database schema missing required columns  
**Solution**: Run schema migration commands above

#### 3. API returns 0 events
**Cause**: Date format or filtering issues  
**Solution**: Check date formatting (DD-MM-YYYY) and API parameters

#### 4. High CPU usage / runaway processes
**Cause**: Background processes interfering with database operations  
**Solution**: Run cleanup script
```bash
cd /root/homelab-docs && ./scripts/cleanup.sh
```

### Diagnostic Commands

#### Check API Connection
```bash
# Test direct API call
curl -X GET "https://muzeek.com/i/api/events?sort=date&start=26-05-2025&end=26-05-2027&orderdirection=asc" \
  -H "accept: application/json" \
  -H "token: mzku-MS03MTU2NTIxODUtYjI2ZjBlY2FkMDA2MjcwMDljYmI4OWU2NDA5ZjEyZDQ1ZGU2NzdiOQ" \
  | jq '. | length'
```

#### Check Database Schema
```bash
# Verify all columns exist
docker-compose exec -T db mysql -u root -plkj654 club77 -e "DESCRIBE events;"

# Check for specific column
docker-compose exec -T db mysql -u root -plkj654 club77 -e "SHOW COLUMNS FROM events WHERE Field='description';"
```

#### Check App Logs
```bash
# View recent logs
docker-compose logs app --tail=50

# Follow logs in real-time
docker-compose logs -f app
```

---

## 🔄 MAINTENANCE PROCEDURES

### Daily Checks
1. **Verify API Connection**: Run test endpoint
2. **Check Event Count**: Ensure events are syncing
3. **Monitor Logs**: Look for any errors

### Weekly Maintenance
1. **Database Cleanup**: Remove old events if needed
2. **Log Rotation**: Clear old application logs
3. **Performance Check**: Monitor response times

### Monthly Tasks
1. **Token Validation**: Verify API token is still valid
2. **Schema Review**: Check for any new Muzeek API fields
3. **Backup Verification**: Ensure database backups are working

### Emergency Recovery
If the API stops working:

1. **Run Cleanup Script**:
   ```bash
   cd /root/homelab-docs && ./scripts/cleanup.sh
   ```

2. **Restart Services**:
   ```bash
   cd /root/homelab-docs/apps/club77-checkin
   docker-compose restart app
   ```

3. **Check Database Schema**:
   ```bash
   docker-compose exec -T db mysql -u root -plkj654 club77 -e "DESCRIBE events;"
   ```

4. **Test API Connection**:
   ```bash
   curl "http://localhost:3001/api/sync/muzeek/test"
   ```

5. **If Still Failing, Rebuild**:
   ```bash
   docker-compose down && docker-compose up -d --build
   ```

---

## 📝 CONFIGURATION FILES

### Key Files to Monitor
- `services/muzeek.js` - API integration logic
- `docker-compose.yml` - Environment variables and token
- `models/Event.js` - Database model definition
- `routes/sync.js` - API endpoints

### Environment Variables
```yaml
# In docker-compose.yml
MUZEEK_API_TOKEN: mzku-MS03MTU2NTIxODUtYjI2ZjBlY2FkMDA2MjcwMDljYmI4OWU2NDA5ZjEyZDQ1ZGU2NzdiOQ
```

---

## 🚨 CRITICAL NOTES

1. **Never hardcode the API token** - Always use environment variables
2. **Headers are essential** - The specific headers listed above are required for container requests
3. **Database schema must be complete** - Missing columns will cause sync failures
4. **Run cleanup script** if experiencing issues - Background processes can interfere
5. **Monitor logs regularly** - Early detection prevents major issues

---

## 📞 SUPPORT

### Quick Reference Commands
```bash
# Test API
curl "http://localhost:3001/api/sync/muzeek/test"

# Sync events
curl -X POST "http://localhost:3001/api/sync/muzeek/events" -H "Content-Type: application/json"

# Check logs
docker-compose logs app --tail=20

# Restart app
docker-compose restart app

# Full rebuild
docker-compose down && docker-compose up -d --build
```

### Success Indicators
- ✅ Test endpoint returns `"success": true`
- ✅ Sync creates/updates events without errors
- ✅ Event count matches expected number from Muzeek
- ✅ No error messages in application logs

**Last Successful Sync**: 2025-05-26 - 10 events synced successfully 