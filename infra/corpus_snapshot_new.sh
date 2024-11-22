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

# List to keep track of backup directories
BACKUP_DIRS=()

while true; do
    # Check if there are any files (not directories) in CORPUS_DIR that don't contain a '.' in the filename
    if [ -z "$(find "$CORPUS_DIR" -maxdepth 1 -type f ! -name "*.*" -print -quit)" ]; then
        continue
    fi
    break
done

# Take the first snapshot after 1 minute
sleep 60

TIMESTAMP=$(date +"%Y%m%d%H%M%S")

CURRENT_BACKUP="$BACKUP_BASE/backup_$TIMESTAMP"
rsync -a --exclude='*/' --exclude='*.*' "$CORPUS_DIR/" "$CURRENT_BACKUP"

while true; do
    sleep 600   # Take a snapshot every 10 minutes

    TIMESTAMP=$(date +"%Y%m%d%H%M%S")

    # Define the current and previous backup directories
    CURRENT_BACKUP="$BACKUP_BASE/backup_$TIMESTAMP"
    LATEST_BACKUP=$(ls -1dt "$BACKUP_BASE"/backup_* 2>/dev/null | head -1)

    # Use rsync with --link-dest to create a new snapshot with hard links, excluding directories and files with '.'
    rsync -a --link-dest="$LATEST_BACKUP" --exclude='*/' --exclude='*.*' "$CORPUS_DIR/" "$CURRENT_BACKUP"

done
