# 🚨 CRITICAL MUZEEK API PROTECTION GUIDE
## Club77 Check-in App - NEVER LOSE THIS CONNECTION

**Date:** 2025-05-27  
**Status:** ✅ **MUZEEK API WORKING - 11 REAL EVENTS SYNCED**  
**Critical Backup:** `/root/homelab-docs/apps/club77-checkin/backups/critical-muzeek-backup-20250527/`

---

## 🔐 **CRITICAL API CONFIGURATION (DO NOT CHANGE)**

### **Environment Variables (NEVER MODIFY)**
```yaml
# In docker-compose.yml - THESE ARE WORKING
environment:
  MUZEEK_API_TOKEN: mzku-MS03MTU2NTIxODUtYjI2ZjBlY2FkMDA2MjcwMDljYmI4OWU2NDA5ZjEyZDQ1ZGU2NzdiOQ
  MAILCHIMP_API_KEY: 2692c472af4f17326f5c1384a61b4c5b-us12
  MAILCHIMP_SERVER: us12
  MAILCHIMP_LIST_ID: 53f56e2c77
```

### **Critical Files (BACKUP BEFORE ANY CHANGES)**
- `services/muzeek.js` - API integration logic
- `routes/sync.js` - Sync endpoints
- `models/Event.js` - Database schema
- `docker-compose.yml` - Environment variables
- Database: `events` table with 11 real Muzeek events

---

## 🛡️ **PROTECTION PROTOCOL**

### **BEFORE ANY CHANGES:**
1. **Always backup first:**
   ```bash
   cd /root/homelab-docs/apps/club77-checkin
   docker exec club77_db mysqldump -u root -plkj654 club77 events > backups/pre-change-backup-$(date +%Y%m%d-%H%M%S).sql
   ```

2. **Test API connection:**
   ```bash
   curl -s http://192.168.1.107:3001/api/sync/muzeek/test
   # Should return: {"success":true,"eventCount":20}
   ```

3. **Verify events count:**
   ```bash
   docker exec club77_db mysql -u root -plkj654 club77 -e "SELECT COUNT(*) FROM events WHERE muzeek_id IS NOT NULL;"
   # Should return: 11 (or more)
   ```

### **SAFE CHANGE AREAS (Frontend Only):**
- ✅ `views/*.ejs` files (templates)
- ✅ `public/css/*` (styles)
- ✅ `public/js/*` (frontend JavaScript)
- ✅ Frontend styling and layout

### **DANGER ZONES (NEVER TOUCH WITHOUT BACKUP):**
- ❌ `services/muzeek.js`
- ❌ `routes/sync.js`
- ❌ `models/Event.js`
- ❌ `docker-compose.yml` environment section
- ❌ Database schema changes
- ❌ API endpoints

---

## 🚨 **EMERGENCY RECOVERY**

### **If Events Disappear:**
```bash
cd /root/homelab-docs/apps/club77-checkin

# 1. Restore from backup
docker exec -i club77_db mysql -u root -plkj654 club77 < backups/critical-muzeek-backup-20250527/muzeek-events-backup.sql

# 2. Test API connection
curl -s http://192.168.1.107:3001/api/sync/muzeek/test

# 3. Trigger fresh sync if needed
curl -X POST http://192.168.1.107:3001/api/sync/muzeek/events

# 4. Verify events are back
docker exec club77_db mysql -u root -plkj654 club77 -e "SELECT COUNT(*) FROM events WHERE muzeek_id IS NOT NULL;"
```

### **If API Connection Breaks:**
```bash
# Check container logs
docker logs club77_app

# Check sync logs
tail -20 /root/homelab-docs/apps/club77-checkin/sync.log

# Test connection manually
curl -s http://192.168.1.107:3001/api/sync/muzeek/test
```

---

## 📊 **CURRENT WORKING STATE**

### **Verified Working (2025-05-27):**
- ✅ **API Connection:** 20 events available from Muzeek
- ✅ **Database:** 11 real events synced (test events removed)
- ✅ **Sync System:** Hourly cron job working
- ✅ **Backup System:** Critical backup created
- ✅ **App Status:** Running on port 3001

### **API Test Results:**
```json
{
  "success": true,
  "message": "Muzeek API connection successful",
  "status": 200,
  "eventCount": 20
}
```

---

## 🎯 **SAFE DEPLOYMENT GUIDELINES**

### **For Frontend Changes (SAFE):**
1. Backup database first
2. Test API connection
3. Make frontend changes only
4. Restart app container
5. Verify events still show
6. Test API connection again

### **For Backend Changes (DANGEROUS):**
1. **STOP** - Create full backup
2. Document exactly what you're changing
3. Test on a copy first if possible
4. Have rollback plan ready
5. Monitor API connection throughout
6. Test immediately after changes

---

## 🔄 **MONITORING COMMANDS**

### **Daily Health Check:**
```bash
# Check event count
docker exec club77_db mysql -u root -plkj654 club77 -e "SELECT COUNT(*) as events FROM events WHERE muzeek_id IS NOT NULL;"

# Test API
curl -s http://192.168.1.107:3001/api/sync/muzeek/test | grep success

# Check sync logs
tail -5 /root/homelab-docs/apps/club77-checkin/sync.log
```

---

## 💾 **BACKUP LOCATIONS**

### **Critical Backups:**
- **Primary:** `/root/homelab-docs/apps/club77-checkin/backups/critical-muzeek-backup-20250527/`
- **Automated:** `/root/homelab-docs/backups/club77-events/` (daily)
- **Sync Logs:** `/root/homelab-docs/apps/club77-checkin/sync.log`

### **Recovery Files:**
- `muzeek-events-backup.sql` - Complete events table
- `docker-compose.yml` - Working environment variables
- `services/muzeek.js` - Working API integration

---

## ⚠️ **FINAL WARNING**

**THE MUZEEK API CONNECTION IS CRITICAL FOR CLUB77 OPERATIONS**

- **11 real events** are currently synced and working
- **Test events have been removed** to prevent confusion
- **API token is working** and must not be changed
- **Database schema is correct** and must not be modified
- **Sync system is automated** and working perfectly

**ALWAYS BACKUP BEFORE ANY CHANGES - NO EXCEPTIONS** 