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

# Record the start time
START_TIME=$(date +%s)

# Define backup times in seconds from the start
BACKUP_TIMES=(60 3600 86400 604800)  # 1 min, 1 hr, 1 day, 1 week

# Keep track of backups done
BACKUPS_DONE=0

# List to keep track of backup directories
BACKUP_DIRS=()

while [ $BACKUPS_DONE -lt 4 ]; do
    # Calculate how much time to sleep until the next backup time
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME))
    NEXT_BACKUP_TIME=${BACKUP_TIMES[$BACKUPS_DONE]}
    SLEEP_TIME=$((NEXT_BACKUP_TIME - ELAPSED_TIME))

    if [ $SLEEP_TIME -gt 0 ]; then
        sleep $SLEEP_TIME
    fi

    # Proceed with backup

    # Get the current timestamp
    TIMESTAMP=$(date +"%Y%m%d%H%M%S")

    # Define the current backup directory
    CURRENT_BACKUP="$BACKUP_BASE/backup_$TIMESTAMP"

    # Determine the latest backup directory for --link-dest
    if [ ${#BACKUP_DIRS[@]} -gt 0 ]; then
        LATEST_BACKUP="${BACKUP_DIRS[-1]}"
        rsync -a --link-dest="$LATEST_BACKUP" --exclude='*/' --exclude='*.*' "$CORPUS_DIR/" "$CURRENT_BACKUP"
    else
        rsync -a --exclude='*/' --exclude='*.*' "$CORPUS_DIR/" "$CURRENT_BACKUP"
    fi

    # Add current backup to the list
    BACKUP_DIRS+=("$CURRENT_BACKUP")

    # Increment backups done
    BACKUPS_DONE=$((BACKUPS_DONE + 1))
done
