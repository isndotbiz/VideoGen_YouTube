#!/usr/bin/env python3
"""
Production-Ready Setup Script for Video Generation Pipeline
Handles API authentication, credential management, and configuration
"""

import os
import sys
import json
from pathlib import Path
from getpass import getpass
from auth_manager import AuthManager, Colors

BANNER = f"""
{Colors.HEADER}{'='*70}
   VIDEO GENERATION PIPELINE - SETUP WIZARD
{'='*70}{Colors.ENDC}

This wizard will help you configure all required API credentials.
You'll be prompted for each API key. Keys are stored in .env file.

{Colors.WARNING}SECURITY REMINDER:{Colors.ENDC}
  • Never commit .env to version control
  • Keep your API keys secure
  • Use environment-specific keys for dev/prod

{Colors.HEADER}{'='*70}{Colors.ENDC}
"""

API_INFO = {
    'FAL_API_KEY': {
        'name': 'FAL.ai',
        'url': 'https://fal.ai/dashboard/keys',
        'description': 'AI image & video generation',
        'required': True,
        'example': 'fal_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    },
    'ELEVENLABS_API_KEY': {
        'name': 'ElevenLabs',
        'url': 'https://elevenlabs.io/app/settings/api-keys',
        'description': 'Text-to-speech voice synthesis',
        'required': True,
        'example': 'el_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    },
    'YOUTUBE_API_KEY': {
        'name': 'YouTube Data API',
        'url': 'https://console.cloud.google.com/apis/credentials',
        'description': 'YouTube API access (read-only)',
        'required': False,
        'example': 'AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    },
    'SHOTSTACK_API_KEY': {
        'name': 'Shotstack',
        'url': 'https://dashboard.shotstack.io/register',
        'description': 'Video editing API',
        'required': True,
        'example': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
}

OPTIONAL_FIELDS = {
    'ELEVENLABS_VOICE_ID': {
        'name': 'ElevenLabs Voice ID',
        'description': 'Specific voice to use (optional)',
        'default': '21m00Tcm4TlvDq8ikWAM',
        'example': '21m00Tcm4TlvDq8ikWAM'
    },
    'SHOTSTACK_ENV': {
        'name': 'Shotstack Environment',
        'description': 'sandbox or v1 (production)',
        'default': 'sandbox',
        'example': 'sandbox'
    },
    'VIDEO_WIDTH': {
        'name': 'Video Width',
        'description': 'Default video width in pixels',
        'default': '1920',
        'example': '1920'
    },
    'VIDEO_HEIGHT': {
        'name': 'Video Height',
        'description': 'Default video height in pixels',
        'default': '1080',
        'example': '1080'
    }
}


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{Colors.OKBLUE}{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}{Colors.ENDC}\n")


def prompt_api_key(key: str, info: dict) -> str:
    """Prompt user for an API key with helpful information"""
    print(f"{Colors.BOLD}{info['name']}{Colors.ENDC}")
    print(f"  Purpose: {info['description']}")
    print(f"  Get your key: {Colors.OKCYAN}{info['url']}{Colors.ENDC}")
    print(f"  Example: {info['example']}")

    if info['required']:
        print(f"  {Colors.WARNING}(Required){Colors.ENDC}")
    else:
        print(f"  {Colors.OKGREEN}(Optional - press Enter to skip){Colors.ENDC}")

    # Secure input for API keys
    value = getpass(f"\n  Enter {info['name']} API key: ").strip()

    if not value and info['required']:
        print(f"  {Colors.FAIL}This field is required!{Colors.ENDC}")
        return prompt_api_key(key, info)

    return value


def prompt_optional_field(key: str, info: dict) -> str:
    """Prompt for optional configuration fields"""
    print(f"{Colors.BOLD}{info['name']}{Colors.ENDC}")
    print(f"  {info['description']}")
    print(f"  Default: {info['default']}")

    value = input(f"  Enter value (or press Enter for default): ").strip()
    return value if value else info['default']


def check_existing_env() -> bool:
    """Check if .env file already exists"""
    return Path('.env').exists()


def backup_existing_env():
    """Backup existing .env file"""
    if Path('.env').exists():
        import shutil
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'.env.backup.{timestamp}'
        shutil.copy('.env', backup_name)
        print(f"{Colors.OKGREEN}Backed up existing .env to {backup_name}{Colors.ENDC}")


def interactive_setup():
    """Interactive setup wizard"""
    print(BANNER)

    # Check for existing configuration
    if check_existing_env():
        print(f"{Colors.WARNING}Found existing .env file!{Colors.ENDC}")
        response = input("Do you want to (o)verwrite, (u)pdate, or (c)ancel? [o/u/c]: ").lower()

        if response == 'c':
            print("Setup cancelled.")
            return False
        elif response == 'u':
            print(f"{Colors.OKGREEN}Update mode: Existing values will be preserved{Colors.ENDC}")
        elif response == 'o':
            backup_existing_env()
            print(f"{Colors.WARNING}Overwrite mode: All values will be replaced{Colors.ENDC}")
        else:
            print("Invalid option. Setup cancelled.")
            return False
    else:
        # Create .env from .env.example
        if Path('.env.example').exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print(f"{Colors.OKGREEN}Created .env file from template{Colors.ENDC}")

    manager = AuthManager()

    # Collect required API keys
    print_section("STEP 1: Required API Keys")

    for key, info in API_INFO.items():
        if info['required']:
            # Check if already set
            existing = manager.get_credential(key)
            if existing and response == 'u':
                masked = existing[:8] + '...' + existing[-4:] if len(existing) > 12 else '***'
                print(f"{Colors.OKGREEN}✓ {info['name']} already configured: {masked}{Colors.ENDC}")
                use_existing = input(f"  Keep existing value? [Y/n]: ").lower()
                if use_existing != 'n':
                    continue

            value = prompt_api_key(key, info)
            if value:
                manager.set_credential(key, value)
                print(f"{Colors.OKGREEN}✓ Saved {info['name']}{Colors.ENDC}\n")

    # Collect optional API keys
    print_section("STEP 2: Optional API Keys")

    for key, info in API_INFO.items():
        if not info['required']:
            existing = manager.get_credential(key)
            if existing and response == 'u':
                print(f"{Colors.OKGREEN}✓ {info['name']} already configured{Colors.ENDC}")
                continue

            response_opt = input(f"Configure {info['name']}? [y/N]: ").lower()
            if response_opt == 'y':
                value = prompt_api_key(key, info)
                if value:
                    manager.set_credential(key, value)
                    print(f"{Colors.OKGREEN}✓ Saved {info['name']}{Colors.ENDC}\n")

    # Collect optional configuration
    print_section("STEP 3: Optional Configuration")

    for key, info in OPTIONAL_FIELDS.items():
        value = prompt_optional_field(key, info)
        manager.set_credential(key, value)
        print(f"{Colors.OKGREEN}✓ Set {info['name']} = {value}{Colors.ENDC}\n")

    # Test all connections
    print_section("STEP 4: Testing API Connections")

    results = manager.test_all_credentials()

    # Create configuration file
    print_section("STEP 5: Creating Configuration File")

    if manager.create_config_file():
        print(f"{Colors.OKGREEN}✓ Created config.json{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}✗ Failed to create config.json{Colors.ENDC}")

    # Final summary
    print_section("SETUP COMPLETE")

    total = len(results)
    passed = sum(1 for success, _ in results.values() if success)

    print(f"API Connections: {Colors.OKGREEN}{passed}/{total} successful{Colors.ENDC}\n")

    if passed == total:
        print(f"{Colors.OKGREEN}{'='*70}")
        print("  ✓ All API connections successful!")
        print("  ✓ Configuration saved to .env")
        print("  ✓ Pipeline configuration saved to config.json")
        print(f"{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.BOLD}Next steps:{Colors.ENDC}")
        print("  1. Review config.json")
        print("  2. Test individual API calls")
        print("  3. Run your video generation pipeline\n")
        return True
    elif passed > 0:
        print(f"{Colors.WARNING}{'='*70}")
        print(f"  ⚠ {passed}/{total} API connections successful")
        print("  Some APIs failed to connect. Review errors above.")
        print(f"{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.BOLD}Troubleshooting:{Colors.ENDC}")
        print("  1. Verify your API keys are correct")
        print("  2. Check API service status")
        print("  3. Review rate limits and quotas")
        print("  4. Re-run setup: python setup.py\n")
        return False
    else:
        print(f"{Colors.FAIL}{'='*70}")
        print("  ✗ No API connections successful")
        print("  Please verify your API keys and try again.")
        print(f"{'='*70}{Colors.ENDC}\n")
        return False


def quick_test():
    """Quick test of existing configuration"""
    print(BANNER)
    print_section("Testing Existing Configuration")

    if not check_existing_env():
        print(f"{Colors.FAIL}No .env file found. Run setup first:{Colors.ENDC}")
        print(f"  python setup.py\n")
        return

    manager = AuthManager()
    print(manager.get_status_report())
    results = manager.test_all_credentials()

    total = len(results)
    passed = sum(1 for success, _ in results.values() if success)

    print(f"\n{Colors.HEADER}{'='*70}{Colors.ENDC}")
    if passed == total:
        print(f"{Colors.OKGREEN}All {total} API connections successful!{Colors.ENDC}")
    elif passed > 0:
        print(f"{Colors.WARNING}{passed}/{total} API connections successful{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}No API connections successful{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}\n")


def show_help():
    """Show help information"""
    print(BANNER)
    print(f"{Colors.BOLD}USAGE:{Colors.ENDC}")
    print("  python setup.py              Run interactive setup wizard")
    print("  python setup.py test         Test existing configuration")
    print("  python setup.py help         Show this help message\n")

    print(f"{Colors.BOLD}REQUIRED APIS:{Colors.ENDC}")
    for key, info in API_INFO.items():
        if info['required']:
            print(f"  • {info['name']}: {info['description']}")
            print(f"    {Colors.OKCYAN}{info['url']}{Colors.ENDC}\n")

    print(f"{Colors.BOLD}FILES CREATED:{Colors.ENDC}")
    print("  • .env              Environment variables (credentials)")
    print("  • config.json       Pipeline configuration")
    print("  • .env.backup.*     Backup of previous .env (if exists)\n")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'test':
            quick_test()
        elif command == 'help':
            show_help()
        else:
            print(f"{Colors.FAIL}Unknown command: {command}{Colors.ENDC}")
            print("Run 'python setup.py help' for usage information.\n")
            sys.exit(1)
    else:
        # Run interactive setup
        success = interactive_setup()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup interrupted by user{Colors.ENDC}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}\n")
        sys.exit(1)
