#!/bin/bash

# Club77 Events Backup Script
# Backs up events and guests data to prevent loss during container rebuilds

BACKUP_DIR="/root/homelab-docs/backups/club77-events"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
BACKUP_FILE="$BACKUP_DIR/club77_events_$TIMESTAMP.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo "Creating Club77 events backup..."

# Backup events and guests tables
docker exec club77_db mysqldump -u root -plkj654 club77 events guests > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "✅ Backup created: $BACKUP_FILE"
    
    # Keep only last 10 backups
    ls -t $BACKUP_DIR/club77_events_*.sql | tail -n +11 | xargs -r rm
    
    echo "📊 Backup summary:"
    echo "   File: $BACKUP_FILE"
    echo "   Size: $(du -h $BACKUP_FILE | cut -f1)"
    echo "   Events: $(grep -c "INSERT INTO \`events\`" $BACKUP_FILE || echo "0")"
    echo "   Guests: $(grep -c "INSERT INTO \`guests\`" $BACKUP_FILE || echo "0")"
else
    echo "❌ Backup failed!"
    exit 1
fi 