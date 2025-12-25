import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Target directory
target_dir = r"D:\workspace\VideoGen_YouTube"

# Calculate cutoff dates
now = datetime.now()
ten_days_ago = now - timedelta(days=10)
thirty_days_ago = now - timedelta(days=30)

# Results structure
empty_files = []
old_files_10d = []
old_files_30d = []
file_stats = defaultdict(lambda: {
    "count": 0,
    "empty_count": 0,
    "total_size": 0,
    "old_10d": 0,
    "old_30d": 0
})

# Walk through directory
for root, dirs, files in os.walk(target_dir):
    # Skip certain directories
    skip_dirs = ['.git', '__pycache__', 'node_modules', '.venv', 'venv']
    dirs[:] = [d for d in dirs if d not in skip_dirs]

    for file in files:
        filepath = os.path.join(root, file)
        try:
            # Get file stats
            stat_info = os.stat(filepath)
            access_time = datetime.fromtimestamp(stat_info.st_atime)
            size = stat_info.st_size

            # Get file extension
            ext = Path(file).suffix.lower() or 'no_extension'

            # Update stats
            file_stats[ext]["count"] += 1
            file_stats[ext]["total_size"] += size

            # Check if empty
            if size == 0:
                file_stats[ext]["empty_count"] += 1
                empty_files.append({
                    "path": filepath,
                    "name": file,
                    "extension": ext,
                    "last_access": access_time.isoformat(),
                    "days_since_access": (now - access_time).days
                })

            # Check access time
            days_since = (now - access_time).days
            if access_time < thirty_days_ago:
                file_stats[ext]["old_30d"] += 1
                old_files_30d.append({
                    "path": filepath,
                    "name": file,
                    "extension": ext,
                    "last_access": access_time.isoformat(),
                    "days_since_access": days_since,
                    "size_bytes": size
                })
            elif access_time < ten_days_ago:
                file_stats[ext]["old_10d"] += 1
                old_files_10d.append({
                    "path": filepath,
                    "name": file,
                    "extension": ext,
                    "last_access": access_time.isoformat(),
                    "days_since_access": days_since,
                    "size_bytes": size
                })

        except (OSError, PermissionError) as e:
            print(f"Error accessing {filepath}: {e}")
            continue

# Sort lists
empty_files.sort(key=lambda x: x["extension"])
old_files_10d.sort(key=lambda x: x["days_since_access"], reverse=True)
old_files_30d.sort(key=lambda x: x["days_since_access"], reverse=True)

# Print comprehensive report
print(f"\n{'='*100}")
print(f"WORKSPACE CLEANUP ANALYSIS - {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*100}\n")

# Summary
print("SUMMARY")
print(f"  Total empty files (0 bytes): {len(empty_files)}")
print(f"  Files not accessed in 10+ days: {len(old_files_10d)}")
print(f"  Files not accessed in 30+ days: {len(old_files_30d)}")
print()

# Empty files by extension
if empty_files:
    print(f"{'='*100}")
    print("EMPTY FILES (0 BYTES) - CANDIDATES FOR DELETION")
    print(f"{'='*100}\n")

    by_ext = defaultdict(list)
    for f in empty_files:
        by_ext[f["extension"]].append(f)

    for ext in sorted(by_ext.keys()):
        files = by_ext[ext]
        print(f"\n{ext} files ({len(files)} empty):")
        print("-" * 100)
        for f in files:
            print(f"  {f['path']}")
            print(f"    Last accessed: {f['last_access']} ({f['days_since_access']} days ago)")

# Old files 10+ days
if old_files_10d:
    print(f"\n{'='*100}")
    print("FILES NOT ACCESSED IN 10+ DAYS")
    print(f"{'='*100}\n")

    for f in old_files_10d:
        size_mb = f['size_bytes'] / (1024 * 1024)
        print(f"  {f['path']}")
        print(f"    Extension: {f['extension']} | Size: {size_mb:.2f} MB | Last access: {f['days_since_access']} days ago")

# Old files 30+ days
if old_files_30d:
    print(f"\n{'='*100}")
    print("FILES NOT ACCESSED IN 30+ DAYS - HIGH PRIORITY FOR DELETION")
    print(f"{'='*100}\n")

    for f in old_files_30d:
        size_mb = f['size_bytes'] / (1024 * 1024)
        print(f"  {f['path']}")
        print(f"    Extension: {f['extension']} | Size: {size_mb:.2f} MB | Last access: {f['days_since_access']} days ago")

# File type statistics
print(f"\n{'='*100}")
print("FILE TYPE STATISTICS")
print(f"{'='*100}\n")

print(f"{'Extension':<20} | {'Total':>8} | {'Empty':>8} | {'10+ days':>10} | {'30+ days':>10} | {'Total Size (MB)':>15}")
print("-" * 100)

for ext in sorted(file_stats.keys(), key=lambda x: file_stats[x]["count"], reverse=True):
    stats = file_stats[ext]
    size_mb = stats["total_size"] / (1024 * 1024)
    print(f"{ext:<20} | {stats['count']:>8} | {stats['empty_count']:>8} | {stats['old_10d']:>10} | {stats['old_30d']:>10} | {size_mb:>15.2f}")

# Save detailed results
output = {
    "analysis_date": now.isoformat(),
    "summary": {
        "empty_files_count": len(empty_files),
        "old_10d_count": len(old_files_10d),
        "old_30d_count": len(old_files_30d)
    },
    "empty_files": empty_files,
    "old_files_10d": old_files_10d,
    "old_files_30d": old_files_30d,
    "file_stats": dict(file_stats)
}

output_file = os.path.join(target_dir, "cleanup_analysis.json")
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*100}")
print(f"Detailed results saved to: {output_file}")
print(f"{'='*100}\n")
