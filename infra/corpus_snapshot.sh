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
    # Wait for 10 seconds before the next backup
    sleep 10

    # Check if there are any files (not directories) in CORPUS_DIR that don't contain a '.' in the filename
    if [ -z "$(find "$CORPUS_DIR" -maxdepth 1 -type f ! -name "*.*" -print -quit)" ]; then
        continue
    fi

    # Get the current timestamp
    TIMESTAMP=$(date +"%Y%m%d%H%M%S")

    # Define the current and previous backup directories
    CURRENT_BACKUP="$BACKUP_BASE/backup_$TIMESTAMP"
    LATEST_BACKUP=$(ls -1dt "$BACKUP_BASE"/backup_* 2>/dev/null | head -1)

    # Use rsync with --link-dest to create a new snapshot with hard links, excluding directories and files with '.'
    if [ -d "$LATEST_BACKUP" ]; then
        rsync -a --link-dest="$LATEST_BACKUP" --exclude='*/' --exclude='*.*' "$CORPUS_DIR/" "$CURRENT_BACKUP"
    else
        rsync -a --exclude='*/' --exclude='*.*' "$CORPUS_DIR/" "$CURRENT_BACKUP"
    fi
done
