#!/usr/bin/env python3
"""Get full render details from Shotstack"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SHOTSTACK_API_KEY")
render_id = "7df0d42a-ab3b-4549-8ccc-f2c56c29ae22"

headers = {"x-api-key": api_key}
response = requests.get(
    f"https://api.shotstack.io/v1/render/{render_id}",
    headers=headers
)

data = response.json()
print(json.dumps(data, indent=2))
