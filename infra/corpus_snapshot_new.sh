#!/bin/bash
# Check for required arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 CORPUS_DIR BACKUP_BASE"
    exit 1
fi

# Set the base directories from arguments
CORPUS_DIR="$1"
BACKUP_BASE="$2"

# Ensure the backup base directory exists
mkdir -p "$BACKUP_BASE"

while true; do
    # Wait for 60 seconds before the next backup check
    sleep 60

    # Check if there are any files (not directories) in CORPUS_DIR that don't contain a '.' in the filename
    if [ -z "$(find "$CORPUS_DIR" -maxdepth 1 -type f ! -name "*.*" -print -quit)" ]; then
        continue
    fi

    CURRENT_TIME=$(date +%s)

    # Function to perform backup if the time difference exceeds the interval
    backup_if_needed() {
        TIMESTAMP=$(date +"%Y%m%d%H%M%S")
        local BACKUP_NAME=$1
        local INTERVAL_SECONDS=$2

        local BACKUP_DIR="$BACKUP_BASE/${BACKUP_NAME}_${TIMESTAMP}"

        if [ -d "$BACKUP_DIR" ]; then
            LAST_BACKUP_TIME=$(stat -c %Y "$BACKUP_DIR")
            TIME_DIFF=$((CURRENT_TIME - LAST_BACKUP_TIME))
            if [ "$TIME_DIFF" -ge "$INTERVAL_SECONDS" ]; then
                rsync -a --delete --exclude='*/' --exclude='*.*' "$CORPUS_DIR/" "$BACKUP_DIR"
                touch "$BACKUP_DIR"  # Update the modification time
            fi
        else
            # Backup directory doesn't exist, perform initial backup
            rsync -a --delete --exclude='*/' --exclude='*.*' "$CORPUS_DIR/" "$BACKUP_DIR"
            touch "$BACKUP_DIR"  # Set the modification time
        fi
    }

    # Perform backups as needed
    backup_if_needed "backup_minute" 60              # 60 seconds = 1 minute
    backup_if_needed "backup_hour" $((60 * 60))      # 3600 seconds = 1 hour
    backup_if_needed "backup_day" $((60 * 60 * 24))  # 86400 seconds = 1 day
    backup_if_needed "backup_week" $((60 * 60 * 24 * 7))  # 604800 seconds = 7 days

done
