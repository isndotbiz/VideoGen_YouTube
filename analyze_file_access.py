import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Target directory
target_dir = r"D:\workspace\VideoGen_YouTube"

# Calculate cutoff dates
now = datetime.now()
ten_days_ago = now - timedelta(days=10)
thirty_days_ago = now - timedelta(days=30)

# Results structure
results = {
    "analysis_date": now.isoformat(),
    "10_days": {"count": 0, "files": []},
    "30_days": {"count": 0, "files": []},
    "by_extension": {}
}

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

            # Get file extension
            ext = Path(file).suffix.lower() or 'no_extension'

            # Prepare file info
            file_info = {
                "path": filepath,
                "name": file,
                "last_access": access_time.isoformat(),
                "days_since_access": (now - access_time).days,
                "extension": ext,
                "size_bytes": stat_info.st_size
            }

            # Categorize by access time
            if access_time < thirty_days_ago:
                results["30_days"]["files"].append(file_info)
                results["30_days"]["count"] += 1
            elif access_time < ten_days_ago:
                results["10_days"]["files"].append(file_info)
                results["10_days"]["count"] += 1

            # Group by extension
            if ext not in results["by_extension"]:
                results["by_extension"][ext] = {
                    "total": 0,
                    "not_accessed_10d": 0,
                    "not_accessed_30d": 0,
                    "files": []
                }

            results["by_extension"][ext]["total"] += 1
            if access_time < thirty_days_ago:
                results["by_extension"][ext]["not_accessed_30d"] += 1
                results["by_extension"][ext]["files"].append(file_info)
            elif access_time < ten_days_ago:
                results["by_extension"][ext]["not_accessed_10d"] += 1
                results["by_extension"][ext]["files"].append(file_info)

        except (OSError, PermissionError) as e:
            print(f"Error accessing {filepath}: {e}")
            continue

# Sort files by access time (oldest first)
results["10_days"]["files"].sort(key=lambda x: x["last_access"])
results["30_days"]["files"].sort(key=lambda x: x["last_access"])

# Save results to JSON
output_file = os.path.join(target_dir, "file_access_analysis.json")
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

# Print summary
print(f"\n{'='*80}")
print(f"FILE ACCESS ANALYSIS - {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*80}\n")

print(f"Total files not accessed in 10+ days: {results['10_days']['count']}")
print(f"Total files not accessed in 30+ days: {results['30_days']['count']}")
print(f"\n{'='*80}")
print("BREAKDOWN BY FILE TYPE")
print(f"{'='*80}\n")

# Sort extensions by number of old files
ext_summary = []
for ext, data in results["by_extension"].items():
    old_count = data["not_accessed_10d"] + data["not_accessed_30d"]
    if old_count > 0:
        ext_summary.append({
            "ext": ext,
            "total": data["total"],
            "10d": data["not_accessed_10d"],
            "30d": data["not_accessed_30d"],
            "old_count": old_count
        })

ext_summary.sort(key=lambda x: x["old_count"], reverse=True)

for item in ext_summary:
    print(f"{item['ext']:20} | Total: {item['total']:4} | 10+ days: {item['10d']:4} | 30+ days: {item['30d']:4}")

print(f"\n{'='*80}")
print(f"Detailed results saved to: {output_file}")
print(f"{'='*80}\n")
