#!/bin/bash

# Club77 Events Restore Script
# Restores events and guests data from backup

BACKUP_DIR="/root/homelab-docs/backups/club77-events"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file>"
    echo ""
    echo "Available backups:"
    ls -la $BACKUP_DIR/club77_events_*.sql 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring Club77 events from: $BACKUP_FILE"

# Restore the backup
docker exec -i club77_db mysql -u root -plkj654 club77 < $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "✅ Restore completed successfully!"
    
    # Show summary
    echo "📊 Restore summary:"
    EVENTS=$(docker exec club77_db mysql -u root -plkj654 club77 -e "SELECT COUNT(*) FROM events;" -s -N)
    GUESTS=$(docker exec club77_db mysql -u root -plkj654 club77 -e "SELECT COUNT(*) FROM guests;" -s -N)
    echo "   Events restored: $EVENTS"
    echo "   Guests restored: $GUESTS"
else
    echo "❌ Restore failed!"
    exit 1
fi 