#!/usr/bin/env python3
"""Get detailed error information from failed render"""

import requests
import json

SHOTSTACK_API_KEY = "zZzUDIrXAe2WW3ddq0lS8j73hbrevSYAiT8NjpM8"
render_id = "5c91823b-7a80-47c5-9223-2a2385ce50cf"

headers = {"x-api-key": SHOTSTACK_API_KEY}
url = f"https://api.shotstack.io/v1/render/{render_id}"

response = requests.get(url, headers=headers)
data = response.json()

print("=" * 60)
print("FULL RENDER ERROR DETAILS")
print("=" * 60)
print(json.dumps(data, indent=2))
