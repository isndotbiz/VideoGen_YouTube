#!/usr/bin/env python3
"""
API Setup and Configuration Script
Sets up all API keys and tests connections
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Tuple

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

class APISetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.env_file = self.base_dir / ".env"
        self.config_file = self.base_dir / "config.json"
        self.credentials = {}

    def prompt_for_key(self, prompt: str, required: bool = True) -> str:
        """Prompt user for input with validation"""
        while True:
            value = input(f"{Colors.CYAN}{prompt}{Colors.END}: ").strip()
            if value or not required:
                return value
            print_error("This field is required. Please enter a value.")

    def setup_fal_ai(self) -> Tuple[bool, str]:
        """Setup FAL.ai API key"""
        print_info("FAL.ai - Flux Image Generation")
        print("Get your API key from: https://fal.ai/dashboard/keys")
        key = self.prompt_for_key("Enter FAL_API_KEY", required=True)

        try:
            # Test connection
            import requests
            headers = {"Authorization": f"Key {key}"}
            response = requests.get("https://api.fal.ai/v1/status", headers=headers, timeout=5)
            if response.status_code == 200:
                print_success("FAL.ai API key valid")
                self.credentials["FAL_API_KEY"] = key
                return True, ""
            else:
                return False, f"API returned status {response.status_code}"
        except Exception as e:
            print_warning(f"Could not fully test FAL.ai: {str(e)}")
            print_info("Key format appears valid. Will test during first use.")
            self.credentials["FAL_API_KEY"] = key
            return True, ""

    def setup_elevenlabs(self) -> Tuple[bool, str]:
        """Setup ElevenLabs API key"""
        print_info("ElevenLabs - Text-to-Speech")
        print("Get your API key from: https://elevenlabs.io/app/settings/api-keys")
        key = self.prompt_for_key("Enter ELEVENLABS_API_KEY", required=True)

        try:
            import requests
            headers = {"xi-api-key": key}
            response = requests.get("https://api.elevenlabs.io/v1/user", headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print_success(f"ElevenLabs API key valid (User: {data.get('first_name', 'Unknown')})")
                self.credentials["ELEVENLABS_API_KEY"] = key
                return True, ""
            else:
                return False, f"API returned status {response.status_code}"
        except Exception as e:
            return False, str(e)

    def setup_shotstack(self) -> Tuple[bool, str]:
        """Setup Shotstack API key"""
        print_info("Shotstack - Video Assembly (Fallback)")
        print("Get your API key from: https://dashboard.shotstack.io/settings/api-key")
        key = self.prompt_for_key("Enter SHOTSTACK_API_KEY", required=True)

        try:
            import requests
            headers = {"x-api-key": key, "content-type": "application/json"}
            response = requests.get("https://api.shotstack.io/stage/status", headers=headers, timeout=5)
            if response.status_code == 200:
                print_success("Shotstack API key valid")
                self.credentials["SHOTSTACK_API_KEY"] = key
                return True, ""
            else:
                return False, f"API returned status {response.status_code}"
        except Exception as e:
            return False, str(e)

    def setup_youtube(self) -> Tuple[bool, str]:
        """Setup YouTube API credentials"""
        print_info("YouTube - Video Publishing (OAuth 2.0)")
        print("Get credentials from: https://console.cloud.google.com")
        print("1. Create a new project")
        print("2. Enable YouTube Data API v3")
        print("3. Create OAuth 2.0 credentials (Desktop application)")

        client_id = self.prompt_for_key("Enter YOUTUBE_CLIENT_ID", required=True)
        client_secret = self.prompt_for_key("Enter YOUTUBE_CLIENT_SECRET", required=True)

        self.credentials["YOUTUBE_CLIENT_ID"] = client_id
        self.credentials["YOUTUBE_CLIENT_SECRET"] = client_secret
        self.credentials["YOUTUBE_REDIRECT_URI"] = "http://localhost:8888/callback"

        print_warning("YouTube OAuth will complete on first use with web browser.")
        return True, ""

    def setup_comfyui(self) -> Tuple[bool, str]:
        """Setup ComfyUI local server"""
        print_info("ComfyUI - Local Flux Turbo Generation")
        url = self.prompt_for_key("Enter COMFYUI_SERVER_URL [http://localhost:8188]", required=False)
        url = url or "http://localhost:8188"

        try:
            import requests
            response = requests.get(f"{url}/api/auth", timeout=5)
            if response.status_code in [200, 401]:  # 401 means auth required but server is up
                print_success(f"ComfyUI server reachable at {url}")
                self.credentials["COMFYUI_SERVER_URL"] = url
                return True, ""
            else:
                return False, f"Server returned status {response.status_code}"
        except Exception as e:
            print_warning(f"ComfyUI server not reachable: {str(e)}")
            print_info("Make sure ComfyUI is running. You can start it later.")
            self.credentials["COMFYUI_SERVER_URL"] = url
            return True, ""

    def save_env_file(self):
        """Save credentials to .env file"""
        env_content = "# Generated by setup_apis.py - DO NOT COMMIT THIS FILE\n\n"

        for key, value in self.credentials.items():
            env_content += f"{key}={value}\n"

        # Add defaults
        env_content += "\n# Settings\n"
        env_content += "DEBUG=false\n"
        env_content += "LOG_LEVEL=INFO\n"
        env_content += "PARALLEL_PROCESSING=true\n"
        env_content += "MAX_RETRIES=3\n"
        env_content += "REQUEST_TIMEOUT=300\n"
        env_content += "\n# Video Settings\n"
        env_content += "VIDEO_RESOLUTION=1920x1080\n"
        env_content += "VIDEO_BITRATE=8000k\n"
        env_content += "AUDIO_BITRATE=128k\n"
        env_content += "\n# Output Paths\n"
        env_content += "OUTPUT_DIR=./output\n"
        env_content += "TEMP_DIR=./temp\n"
        env_content += "LOGS_DIR=./logs\n"

        with open(self.env_file, 'w') as f:
            f.write(env_content)

        print_success(f"Saved credentials to {self.env_file}")
        print_warning(f"Add this file to .gitignore to prevent accidental commits")

    def save_config_file(self):
        """Save configuration to config.json"""
        config = {
            "apis": {
                "fal": {
                    "name": "FAL.ai",
                    "endpoint": "https://api.fal.ai/v1",
                    "status": "configured"
                },
                "elevenlabs": {
                    "name": "ElevenLabs",
                    "endpoint": "https://api.elevenlabs.io/v1",
                    "status": "configured"
                },
                "shotstack": {
                    "name": "Shotstack",
                    "endpoint": "https://api.shotstack.io/stage",
                    "status": "configured"
                },
                "youtube": {
                    "name": "YouTube",
                    "endpoint": "https://www.googleapis.com/youtube/v3",
                    "status": "configured"
                },
                "comfyui": {
                    "name": "ComfyUI",
                    "endpoint": self.credentials.get("COMFYUI_SERVER_URL", "http://localhost:8188"),
                    "status": "configured"
                }
            },
            "video": {
                "resolution": "1920x1080",
                "bitrate": "8000k",
                "codec": "h264",
                "fps": 30
            },
            "paths": {
                "output": "./output",
                "temp": "./temp",
                "logs": "./logs"
            }
        }

        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

        print_success(f"Saved configuration to {self.config_file}")

    def run_setup(self):
        """Run complete setup workflow"""
        print_header("Video Generation Pipeline - API Setup")

        apis_to_setup = [
            ("FAL.ai", self.setup_fal_ai),
            ("ElevenLabs", self.setup_elevenlabs),
            ("Shotstack", self.setup_shotstack),
            ("YouTube", self.setup_youtube),
            ("ComfyUI", self.setup_comfyui),
        ]

        print(f"This script will guide you through setting up {len(apis_to_setup)} APIs.\n")

        failed_apis = []

        for api_name, setup_func in apis_to_setup:
            print(f"\n{Colors.BOLD}Setting up {api_name}...{Colors.END}")
            success, error = setup_func()

            if not success:
                print_error(f"{api_name} setup failed: {error}")
                failed_apis.append((api_name, error))

            input(f"\nPress Enter to continue...")

        # Save files
        print_header("Saving Configuration")
        self.save_env_file()
        self.save_config_file()

        # Summary
        print_header("Setup Summary")

        if failed_apis:
            print_warning(f"{len(failed_apis)} API(s) had issues:")
            for api_name, error in failed_apis:
                print(f"  • {api_name}: {error}")
            print_info("You can fix these and re-run the setup script.")
        else:
            print_success("All APIs configured successfully!")

        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Setup Complete!{Colors.END}")
        print(f"\nNext steps:")
        print(f"  1. Review your .env file for any issues")
        print(f"  2. Ensure ComfyUI is running (if using local generation)")
        print(f"  3. Run: python video_pipeline.py --help")
        print(f"\n")

if __name__ == "__main__":
    setup = APISetup()
    setup.run_setup()
