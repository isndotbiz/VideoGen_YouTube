#!/usr/bin/env python3
"""
Safe cleanup script for deleting empty files in VideoGen_YouTube workspace.
This script will:
1. Delete only files that are 0 bytes in size
2. Skip files accessed within the last 24 hours (safety measure)
3. Create a backup log of all deleted files
4. Provide detailed progress output
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
target_dir = r"D:\workspace\VideoGen_YouTube"
dry_run = True  # Set to False to actually delete files
skip_recent_hours = 24  # Don't delete files accessed in the last 24 hours

# Results
deleted_files = []
skipped_files = []
errors = []

# Calculate cutoff time
now = datetime.now()
recent_cutoff = now - timedelta(hours=skip_recent_hours)

print(f"\n{'='*100}")
print(f"EMPTY FILE CLEANUP - {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*100}\n")
print(f"Mode: {'DRY RUN (no files will be deleted)' if dry_run else 'DELETION ACTIVE'}")
print(f"Safety: Skipping files accessed in the last {skip_recent_hours} hours\n")

# Walk through directory
for root, dirs, files in os.walk(target_dir):
    # Skip certain directories
    skip_dirs = ['.git', '__pycache__', 'node_modules', '.venv', 'venv']
    dirs[:] = [d for d in dirs if d not in skip_dirs]

    for file in files:
        filepath = os.path.join(root, file)

        # Skip the cleanup scripts themselves
        if file in ['cleanup_analysis.py', 'cleanup_delete_empty_files.py',
                    'analyze_file_access.py', 'file_access_analysis.json',
                    'cleanup_analysis.json', 'CLEANUP_REPORT.md']:
            continue

        try:
            # Get file stats
            stat_info = os.stat(filepath)
            size = stat_info.st_size
            access_time = datetime.fromtimestamp(stat_info.st_atime)

            # Only process empty files
            if size == 0:
                # Check if recently accessed
                if access_time > recent_cutoff:
                    skipped_files.append({
                        "path": filepath,
                        "reason": "accessed_recently",
                        "last_access": access_time.isoformat(),
                        "hours_since_access": (now - access_time).total_seconds() / 3600
                    })
                    print(f"SKIPPED (recent): {filepath}")
                    print(f"   Last access: {access_time.strftime('%Y-%m-%d %H:%M:%S')} "
                          f"({(now - access_time).total_seconds() / 3600:.1f} hours ago)\n")
                else:
                    # Delete the file
                    if not dry_run:
                        os.remove(filepath)
                        action = "DELETED"
                    else:
                        action = "WOULD DELETE"

                    deleted_files.append({
                        "path": filepath,
                        "last_access": access_time.isoformat(),
                        "days_since_access": (now - access_time).days,
                        "deleted_at": now.isoformat()
                    })

                    print(f"{action}: {filepath}")
                    print(f"   Last access: {access_time.strftime('%Y-%m-%d %H:%M:%S')} "
                          f"({(now - access_time).days} days ago)\n")

        except (OSError, PermissionError) as e:
            errors.append({
                "path": filepath,
                "error": str(e)
            })
            print(f"ERROR: {filepath}")
            print(f"   {str(e)}\n")
            continue

# Print summary
print(f"\n{'='*100}")
print("CLEANUP SUMMARY")
print(f"{'='*100}\n")

print(f"Files {'that would be' if dry_run else ''} deleted: {len(deleted_files)}")
print(f"Files skipped (recently accessed): {len(skipped_files)}")
print(f"Errors encountered: {len(errors)}\n")

if deleted_files:
    print("Deleted/Would delete:")
    for f in deleted_files:
        print(f"  - {f['path']}")
    print()

if skipped_files:
    print("Skipped (recently accessed):")
    for f in skipped_files:
        print(f"  - {f['path']} (accessed {f['hours_since_access']:.1f} hours ago)")
    print()

if errors:
    print("Errors:")
    for e in errors:
        print(f"  - {e['path']}: {e['error']}")
    print()

# Save log
log = {
    "cleanup_date": now.isoformat(),
    "dry_run": dry_run,
    "skip_recent_hours": skip_recent_hours,
    "summary": {
        "deleted_count": len(deleted_files),
        "skipped_count": len(skipped_files),
        "error_count": len(errors)
    },
    "deleted_files": deleted_files,
    "skipped_files": skipped_files,
    "errors": errors
}

log_file = os.path.join(target_dir, "cleanup_log.json")
with open(log_file, 'w') as f:
    json.dump(log, f, indent=2)

print(f"{'='*100}")
print(f"Cleanup log saved to: {log_file}")

if dry_run:
    print(f"\nWARNING: This was a DRY RUN - no files were actually deleted.")
    print(f"To perform actual deletion, edit this script and set: dry_run = False")
print(f"{'='*100}\n")
