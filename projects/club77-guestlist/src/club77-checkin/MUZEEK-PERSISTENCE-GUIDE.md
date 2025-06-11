# Club77 Muzeek API Persistence Guide

## 🔄 **Automated Sync System**

### **Hourly Sync (Cron Job)**
```bash
# Runs every hour to keep events updated
0 * * * * /root/homelab-docs/apps/club77-checkin/sync-events-cron.sh
```

**Log Location:** `/root/homelab-docs/apps/club77-checkin/sync.log`

### **Startup Sync**
- App automatically syncs on startup if no events found
- Prevents empty event list after container rebuilds
- 2-second delay to ensure database is ready

## 🔐 **API Configuration Persistence**

### **Environment Variables (docker-compose.yml)**
```yaml
environment:
  MUZEEK_API_TOKEN: mzku-MS03MTU2NTIxODUtYjI2ZjBlY2FkMDA2MjcwMDljYmI4OWU2NDA5ZjEyZDQ1ZGU2NzdiOQ
  MAILCHIMP_API_KEY: 2692c472af4f17326f5c1384a61b4c5b-us12
  MAILCHIMP_SERVER: us12
  MAILCHIMP_LIST_ID: 53f56e2c77
```

**✅ These persist across container rebuilds**

## 💾 **Data Backup & Restore**

### **Manual Backup**
```bash
# Create backup
/root/homelab-docs/apps/club77-checkin/backup-events.sh

# Restore from backup
/root/homelab-docs/apps/club77-checkin/restore-events.sh /path/to/backup.sql
```

### **Automatic Backup**
- Events backed up daily at 2 AM via existing cron job
- Keeps last 10 backups automatically
- Location: `/root/homelab-docs/backups/club77-events/`

## 🚨 **Recovery Procedures**

### **If Events Disappear After Rebuild**
1. **Check if sync is working:**
   ```bash
   curl -X POST http://192.168.1.107:3001/api/sync/muzeek/events
   ```

2. **Check sync logs:**
   ```bash
   tail -f /root/homelab-docs/apps/club77-checkin/sync.log
   ```

3. **Manual sync trigger:**
   ```bash
   /root/homelab-docs/apps/club77-checkin/sync-events-cron.sh
   ```

4. **Restore from backup if needed:**
   ```bash
   /root/homelab-docs/apps/club77-checkin/restore-events.sh /root/homelab-docs/backups/club77-events/club77_events_YYYYMMDD_HHMMSS.sql
   ```

### **If API Token Expires**
1. Update token in `docker-compose.yml`
2. Rebuild container: `docker-compose up -d --build`
3. Test connection: `curl -X GET http://192.168.1.107:3001/api/sync/muzeek/test`

## 📊 **Monitoring**

### **Check Sync Status**
```bash
# API endpoint
curl http://192.168.1.107:3001/api/sync/muzeek/status

# Log file
tail /root/homelab-docs/apps/club77-checkin/sync.log

# Database count
docker exec club77_db mysql -u root -plkj654 club77 -e "SELECT COUNT(*) as event_count FROM events WHERE muzeek_id IS NOT NULL;"
```

### **Verify Events Are Showing**
```bash
# Check homepage
curl -s http://192.168.1.107:3001 | grep -c "club77-event-card"

# Check database directly
docker exec club77_db mysql -u root -plkj654 club77 -e "SELECT name, event_date, is_live FROM events ORDER BY event_date DESC LIMIT 5;"
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Events Not Syncing**
- Check API token validity
- Verify network connectivity to muzeek.com
- Check sync log for errors

#### **Events Not Displaying**
- Verify `is_live = true` in database
- Check for JavaScript errors in browser console
- Restart app container

#### **Database Connection Issues**
- Ensure club77_db container is running
- Check database credentials in docker-compose.yml
- Verify database schema is correct

## 🎯 **Best Practices**

1. **Always backup before major changes**
2. **Test sync after any container rebuild**
3. **Monitor sync logs regularly**
4. **Keep API tokens secure and updated**
5. **Use the automated systems rather than manual intervention**

## 📝 **Quick Commands Reference**

```bash
# Sync events now
curl -X POST http://192.168.1.107:3001/api/sync/muzeek/events

# Check sync status
curl http://192.168.1.107:3001/api/sync/muzeek/status

# Test API connection
curl http://192.168.1.107:3001/api/sync/muzeek/test

# View recent sync logs
tail -20 /root/homelab-docs/apps/club77-checkin/sync.log

# Backup events
/root/homelab-docs/apps/club77-checkin/backup-events.sh

# Check cron jobs
crontab -l | grep club77
``` 