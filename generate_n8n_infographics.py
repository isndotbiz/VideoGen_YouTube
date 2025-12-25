#!/usr/bin/env python3
"""
Generate new N8N infographics with Nano Banana (FAL AI)
Creates professional, clean infographics for the N8N video
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import APIConfig

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = "output/n8n_infographics"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

PROMPTS = [
    {
        "name": "n8n_workflow_overview",
        "prompt": "Professional infographic for N8N showing workflow automation platform with 400+ integrations, nodes connecting different apps like Gmail, Slack, CRM, databases. Modern design, clean lines, tech aesthetic. High quality."
    },
    {
        "name": "n8n_automation_benefits",
        "prompt": "Infographic showing benefits of workflow automation: save time, reduce errors, increase productivity. Visual elements showing before/after automation. Professional business design."
    },
    {
        "name": "n8n_integrations",
        "prompt": "Visual showcase of N8N's 400+ app integrations: Gmail, Slack, HubSpot, Salesforce, AWS, Google Sheets, etc. App icons arranged in a professional grid. Modern tech design."
    },
    {
        "name": "n8n_use_cases",
        "prompt": "Infographic showing real-world N8N use cases: CRM automation, lead generation, email workflows, data processing, social media automation. Professional business presentation."
    },
]

log("N8N Infographics Generator")
log("=" * 70)
log("Generating new N8N infographics with Nano Banana (FAL AI)...\n")

# Check FAL API key
fal_key = APIConfig.FAL_API_KEY
if not fal_key or fal_key.startswith("your_"):
    log("ERROR: FAL_API_KEY not configured in .env")
    log("Please set FAL_API_KEY in your .env file")
    sys.exit(1)

# ============================================================================
# Generate each infographic
# ============================================================================

generated_files = []

for i, prompt_info in enumerate(PROMPTS, 1):
    name = prompt_info["name"]
    prompt = prompt_info["prompt"]

    log(f"[{i}/{len(PROMPTS)}] Generating: {name}")
    log(f"  Prompt: {prompt[:60]}...")

    try:
        # Use FAL AI Flux model for high-quality infographics
        import fal_client

        result = fal_client.run(
            "fal-ai/flux-pro/v1.1",
            arguments={
                "prompt": prompt,
                "image_size": "landscape_16_9",
                "num_images": 1,
                "enable_safety_checker": True,
            },
        )

        if result and result.get("images"):
            image_url = result["images"][0]["url"]

            # Download image
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                output_path = f"{OUTPUT_DIR}/{name}.jpg"
                with open(output_path, "wb") as f:
                    f.write(response.content)

                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                log(f"  Created: {output_path} ({file_size_mb:.1f} MB)")
                generated_files.append(output_path)
            else:
                log(f"  Error downloading image")
        else:
            log(f"  No image in result")

    except Exception as e:
        log(f"  Error: {str(e)[:100]}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

log("\n" + "=" * 70)
log(f"Generated {len(generated_files)}/{len(PROMPTS)} infographics")
log("=" * 70)

if generated_files:
    log("\nGenerated files:")
    for file in generated_files:
        log(f"  {file}")

    log(f"\nLocation: {OUTPUT_DIR}/")
    log("\nReady to use in videos!")
else:
    log("\nNo infographics generated. Check FAL_API_KEY configuration.")

log("\nDone!")
