#!/usr/bin/env python3
"""
Authentication Manager for Video Generation Pipeline
Handles credential management, validation, and API testing
"""

import os
import json
import sys
from typing import Dict, Optional, Tuple
from pathlib import Path
import requests
from dotenv import load_dotenv, set_key, find_dotenv

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AuthManager:
    """Manages API credentials and authentication"""

    def __init__(self, env_file: str = '.env'):
        self.env_file = env_file
        self.env_path = Path(env_file)
        load_dotenv(self.env_file)

    def get_credential(self, key: str) -> Optional[str]:
        """Retrieve a credential from environment"""
        return os.getenv(key)

    def set_credential(self, key: str, value: str) -> bool:
        """Save a credential to .env file"""
        try:
            # Create .env if it doesn't exist
            if not self.env_path.exists():
                self.env_path.touch()

            set_key(self.env_file, key, value)
            # Reload environment
            load_dotenv(self.env_file, override=True)
            return True
        except Exception as e:
            print(f"{Colors.FAIL}Failed to save {key}: {e}{Colors.ENDC}")
            return False

    def test_fal_ai(self) -> Tuple[bool, str]:
        """Test FAL.ai API connection"""
        api_key = self.get_credential('FAL_API_KEY')
        if not api_key:
            return False, "API key not found"

        try:
            # Test with a simple API call
            headers = {
                'Authorization': f'Key {api_key}',
                'Content-Type': 'application/json'
            }

            # List available models (lightweight endpoint)
            response = requests.get(
                'https://fal.run/fal-ai/fast-sdxl',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200 or response.status_code == 404:
                # 404 is ok - means auth worked but endpoint might be different
                return True, "Authentication successful"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"Unexpected response: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"

    def test_elevenlabs(self) -> Tuple[bool, str]:
        """Test ElevenLabs API connection"""
        api_key = self.get_credential('ELEVENLABS_API_KEY')
        if not api_key:
            return False, "API key not found"

        try:
            headers = {
                'xi-api-key': api_key
            }

            # Get user info
            response = requests.get(
                'https://api.elevenlabs.io/v1/user',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                subscription = data.get('subscription', {}).get('tier', 'free')
                chars_left = data.get('subscription', {}).get('character_count', 0)
                return True, f"Connected (Tier: {subscription}, Chars: {chars_left})"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"Error: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"

    def test_youtube(self) -> Tuple[bool, str]:
        """Test YouTube API connection"""
        api_key = self.get_credential('YOUTUBE_API_KEY')
        client_id = self.get_credential('YOUTUBE_CLIENT_ID')

        # Check if we have either API key or OAuth credentials
        if not api_key and not client_id:
            return False, "No credentials found (need API key or OAuth)"

        try:
            if api_key:
                # Test with a simple search query
                response = requests.get(
                    'https://www.googleapis.com/youtube/v3/search',
                    params={
                        'part': 'snippet',
                        'q': 'test',
                        'maxResults': 1,
                        'key': api_key
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    return True, "API key valid (read-only access)"
                elif response.status_code == 400:
                    error = response.json().get('error', {})
                    return False, f"Invalid request: {error.get('message', 'Unknown error')}"
                elif response.status_code == 403:
                    return False, "Invalid API key or quota exceeded"
                else:
                    return False, f"Error: {response.status_code}"
            else:
                # OAuth credentials present
                return True, "OAuth credentials configured (needs full setup)"

        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"

    def test_shotstack(self) -> Tuple[bool, str]:
        """Test Shotstack API connection"""
        api_key = self.get_credential('SHOTSTACK_API_KEY')
        env = self.get_credential('SHOTSTACK_ENV') or 'sandbox'

        if not api_key:
            return False, "API key not found"

        try:
            # Determine base URL based on environment
            if env == 'sandbox':
                base_url = 'https://api.shotstack.io/stage'
            else:
                base_url = 'https://api.shotstack.io/v1'

            headers = {
                'x-api-key': api_key,
                'Content-Type': 'application/json'
            }

            # Test with sources endpoint (lightweight)
            response = requests.get(
                f'{base_url}/sources',
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                return True, f"Connected ({env} environment)"
            elif response.status_code == 401:
                return False, "Invalid API key"
            elif response.status_code == 403:
                return False, "API key valid but insufficient permissions"
            else:
                return False, f"Error: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"

    def test_all_credentials(self) -> Dict[str, Tuple[bool, str]]:
        """Test all configured API credentials"""
        results = {}

        print(f"\n{Colors.HEADER}Testing API Connections...{Colors.ENDC}\n")

        # Test FAL.ai
        print(f"{Colors.OKCYAN}Testing FAL.ai...{Colors.ENDC}", end=' ')
        success, message = self.test_fal_ai()
        results['FAL.ai'] = (success, message)
        if success:
            print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

        # Test ElevenLabs
        print(f"{Colors.OKCYAN}Testing ElevenLabs...{Colors.ENDC}", end=' ')
        success, message = self.test_elevenlabs()
        results['ElevenLabs'] = (success, message)
        if success:
            print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

        # Test YouTube
        print(f"{Colors.OKCYAN}Testing YouTube...{Colors.ENDC}", end=' ')
        success, message = self.test_youtube()
        results['YouTube'] = (success, message)
        if success:
            print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

        # Test Shotstack
        print(f"{Colors.OKCYAN}Testing Shotstack...{Colors.ENDC}", end=' ')
        success, message = self.test_shotstack()
        results['Shotstack'] = (success, message)
        if success:
            print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

        return results

    def create_config_file(self) -> bool:
        """Create config.json for the pipeline"""
        config = {
            "apis": {
                "fal": {
                    "enabled": bool(self.get_credential('FAL_API_KEY')),
                    "api_key_env": "FAL_API_KEY",
                    "base_url": "https://fal.run"
                },
                "elevenlabs": {
                    "enabled": bool(self.get_credential('ELEVENLABS_API_KEY')),
                    "api_key_env": "ELEVENLABS_API_KEY",
                    "voice_id": self.get_credential('ELEVENLABS_VOICE_ID') or "21m00Tcm4TlvDq8ikWAM",
                    "base_url": "https://api.elevenlabs.io/v1"
                },
                "youtube": {
                    "enabled": bool(self.get_credential('YOUTUBE_API_KEY') or self.get_credential('YOUTUBE_CLIENT_ID')),
                    "api_key_env": "YOUTUBE_API_KEY",
                    "client_id_env": "YOUTUBE_CLIENT_ID",
                    "client_secret_env": "YOUTUBE_CLIENT_SECRET",
                    "base_url": "https://www.googleapis.com/youtube/v3"
                },
                "shotstack": {
                    "enabled": bool(self.get_credential('SHOTSTACK_API_KEY')),
                    "api_key_env": "SHOTSTACK_API_KEY",
                    "environment": self.get_credential('SHOTSTACK_ENV') or "sandbox",
                    "base_url": "https://api.shotstack.io"
                }
            },
            "settings": {
                "output_dir": self.get_credential('OUTPUT_DIR') or "./output",
                "video_width": int(self.get_credential('VIDEO_WIDTH') or 1920),
                "video_height": int(self.get_credential('VIDEO_HEIGHT') or 1080),
                "video_fps": int(self.get_credential('VIDEO_FPS') or 30),
                "debug": self.get_credential('DEBUG') == 'true',
                "api_timeout": int(self.get_credential('API_TIMEOUT') or 30),
                "max_retries": int(self.get_credential('MAX_RETRIES') or 3)
            }
        }

        try:
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"{Colors.FAIL}Failed to create config.json: {e}{Colors.ENDC}")
            return False

    def get_status_report(self) -> str:
        """Generate a status report of all credentials"""
        report = f"\n{Colors.HEADER}{'='*60}\n"
        report += "  API CREDENTIALS STATUS REPORT\n"
        report += f"{'='*60}{Colors.ENDC}\n\n"

        services = [
            ('FAL.ai', 'FAL_API_KEY'),
            ('ElevenLabs', 'ELEVENLABS_API_KEY'),
            ('YouTube API', 'YOUTUBE_API_KEY'),
            ('YouTube OAuth', 'YOUTUBE_CLIENT_ID'),
            ('Shotstack', 'SHOTSTACK_API_KEY')
        ]

        for service, env_var in services:
            value = self.get_credential(env_var)
            if value:
                masked = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
                report += f"{Colors.OKGREEN}✓{Colors.ENDC} {service:20s} {masked}\n"
            else:
                report += f"{Colors.FAIL}✗{Colors.ENDC} {service:20s} Not configured\n"

        return report


if __name__ == "__main__":
    """Test the auth manager directly"""
    manager = AuthManager()

    print(manager.get_status_report())
    results = manager.test_all_credentials()

    # Summary
    print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
    total = len(results)
    passed = sum(1 for success, _ in results.values() if success)

    if passed == total:
        print(f"{Colors.OKGREEN}All {total} API connections successful!{Colors.ENDC}")
    elif passed > 0:
        print(f"{Colors.WARNING}{passed}/{total} API connections successful{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}No API connections successful{Colors.ENDC}")

    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}\n")
