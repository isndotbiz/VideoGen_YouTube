#!/usr/bin/env python3
"""
Secrets Manager - Secure Environment Variable and Secrets Management
====================================================================

Features:
- Load and validate .env files
- Encrypt/decrypt sensitive data
- Support multiple environments (dev/staging/prod)
- Key rotation capabilities
- Prevent accidental secrets exposure

Usage:
    from secrets_manager import SecretsManager

    # Initialize
    secrets = SecretsManager()

    # Get API keys
    fal_key = secrets.get('FAL_API_KEY')

    # Validate all required keys present
    if secrets.validate():
        print("All required secrets configured!")

    # Export for specific environment
    secrets.export_for_environment('production')
"""

import os
import sys
import json
import base64
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


class SecretsManager:
    """Manage environment variables and secrets securely."""

    # Required API keys for the video pipeline
    REQUIRED_KEYS = [
        'FAL_API_KEY',
        'ELEVENLABS_API_KEY',
        'SHOTSTACK_API_KEY',
    ]

    # Optional keys
    OPTIONAL_KEYS = [
        'YOUTUBE_CLIENT_ID',
        'YOUTUBE_CLIENT_SECRET',
        'YOUTUBE_API_KEY',
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY',
        'PEXELS_API_KEY',
        'UNSPLASH_ACCESS_KEY',
        'COMFYUI_SERVER_URL',
        'PIKA_API_KEY',
        'REPLICATE_API_KEY',
    ]

    # Keys that should never be logged or displayed
    SENSITIVE_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS

    def __init__(self, env_file: str = '.env', environment: str = None):
        """
        Initialize the secrets manager.

        Args:
            env_file: Path to the .env file (default: .env)
            environment: Environment name (dev/staging/prod), auto-detected if None
        """
        self.env_file = Path(env_file)
        self.environment = environment or os.getenv('ENVIRONMENT', 'development')
        self.secrets: Dict[str, str] = {}
        self.loaded = False

        # Initialize encryption key if SECRET_KEY is set
        self.encryption_key = None

    def load(self, required: bool = True) -> bool:
        """
        Load environment variables from .env file.

        Args:
            required: If True, raise error if .env doesn't exist

        Returns:
            True if loaded successfully, False otherwise
        """
        if not self.env_file.exists():
            if required:
                raise FileNotFoundError(
                    f"Environment file not found: {self.env_file}\n"
                    f"Please copy .env.example to .env and configure your API keys."
                )
            print(f"Warning: {self.env_file} not found, using environment variables only")
            self.loaded = False
            return False

        # Load .env file
        with open(self.env_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Parse key=value
                if '=' not in line:
                    print(f"Warning: Invalid line {line_num} in {self.env_file}: {line}")
                    continue

                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                # Store in secrets dict and set environment variable
                self.secrets[key] = value
                os.environ[key] = value

        # Initialize encryption if SECRET_KEY is present
        secret_key = self.secrets.get('SECRET_KEY')
        if secret_key and secret_key != 'your_secret_encryption_key_here_generate_one':
            self.encryption_key = self._derive_key(secret_key)

        self.loaded = True
        print(f"✓ Loaded {len(self.secrets)} environment variables from {self.env_file}")
        return True

    def get(self, key: str, default: Any = None, required: bool = False) -> Optional[str]:
        """
        Get a secret value.

        Args:
            key: Environment variable name
            default: Default value if not found
            required: Raise error if not found and no default

        Returns:
            Secret value or default
        """
        # Try loaded secrets first
        value = self.secrets.get(key)

        # Fall back to environment variables
        if value is None:
            value = os.getenv(key, default)

        # Check if required
        if required and value is None:
            raise ValueError(f"Required secret '{key}' not found in environment")

        return value

    def set(self, key: str, value: str, persist: bool = False):
        """
        Set a secret value.

        Args:
            key: Environment variable name
            value: Secret value
            persist: If True, save to .env file
        """
        self.secrets[key] = value
        os.environ[key] = value

        if persist:
            self._persist_to_env()

    def validate(self, strict: bool = False) -> bool:
        """
        Validate that all required secrets are present.

        Args:
            strict: If True, also check that values are not defaults

        Returns:
            True if all required secrets are valid
        """
        missing = []
        invalid = []

        for key in self.REQUIRED_KEYS:
            value = self.get(key)

            if not value:
                missing.append(key)
            elif strict and self._is_placeholder(value):
                invalid.append(key)

        if missing:
            print(f"✗ Missing required secrets: {', '.join(missing)}")
            return False

        if invalid:
            print(f"✗ Secrets with placeholder values: {', '.join(invalid)}")
            return False

        print(f"✓ All {len(self.REQUIRED_KEYS)} required secrets are configured")
        return True

    def encrypt(self, data: str) -> str:
        """
        Encrypt sensitive data.

        Args:
            data: Plain text data to encrypt

        Returns:
            Encrypted data as base64 string
        """
        if not self.encryption_key:
            raise ValueError("Encryption key not configured. Set SECRET_KEY in .env")

        f = Fernet(self.encryption_key)
        encrypted = f.encrypt(data.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data.

        Args:
            encrypted_data: Base64 encoded encrypted data

        Returns:
            Decrypted plain text
        """
        if not self.encryption_key:
            raise ValueError("Encryption key not configured. Set SECRET_KEY in .env")

        f = Fernet(self.encryption_key)
        encrypted = base64.b64decode(encrypted_data)
        decrypted = f.decrypt(encrypted)
        return decrypted.decode()

    def rotate_key(self, old_key: str, new_key: str):
        """
        Rotate encryption key and re-encrypt all secrets.

        Args:
            old_key: Current encryption key
            new_key: New encryption key to use
        """
        # This would decrypt with old key and re-encrypt with new key
        # Implementation depends on how encrypted data is stored
        raise NotImplementedError("Key rotation not yet implemented")

    def export_for_environment(self, env: str, output_file: Optional[str] = None) -> Dict[str, str]:
        """
        Export secrets for a specific environment.

        Args:
            env: Environment name (development/staging/production)
            output_file: Optional file to write secrets to

        Returns:
            Dictionary of environment variables
        """
        env_secrets = {}

        # Copy all current secrets
        env_secrets.update(self.secrets)

        # Override ENVIRONMENT
        env_secrets['ENVIRONMENT'] = env

        # Adjust settings based on environment
        if env == 'production':
            env_secrets['DEBUG'] = 'false'
            env_secrets['LOG_LEVEL'] = 'WARNING'
            env_secrets['SHOTSTACK_ENV'] = 'v1'
        elif env == 'staging':
            env_secrets['DEBUG'] = 'false'
            env_secrets['LOG_LEVEL'] = 'INFO'
            env_secrets['SHOTSTACK_ENV'] = 'sandbox'
        else:  # development
            env_secrets['DEBUG'] = 'true'
            env_secrets['LOG_LEVEL'] = 'DEBUG'
            env_secrets['SHOTSTACK_ENV'] = 'sandbox'

        # Write to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(f"# Environment: {env}\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n\n")
                for key, value in sorted(env_secrets.items()):
                    f.write(f"{key}={value}\n")
            print(f"✓ Exported {len(env_secrets)} secrets to {output_file}")

        return env_secrets

    def mask_secret(self, key: str) -> str:
        """
        Get a masked version of a secret for safe display.

        Args:
            key: Secret key name

        Returns:
            Masked secret value
        """
        value = self.get(key)
        if not value or len(value) < 8:
            return '****'

        # Show first 4 and last 4 characters
        return f"{value[:4]}...{value[-4:]}"

    def list_secrets(self, show_values: bool = False):
        """
        List all configured secrets.

        Args:
            show_values: If True, show masked values
        """
        print(f"\n{'Secret Key':<30} {'Status':<15} {'Value' if show_values else ''}")
        print("=" * 80)

        # Required keys
        print("\nRequired:")
        for key in self.REQUIRED_KEYS:
            value = self.get(key)
            status = "✓ Set" if value and not self._is_placeholder(value) else "✗ Missing"
            display_value = self.mask_secret(key) if show_values and value else ""
            print(f"{key:<30} {status:<15} {display_value}")

        # Optional keys
        print("\nOptional:")
        for key in self.OPTIONAL_KEYS:
            value = self.get(key)
            status = "✓ Set" if value and not self._is_placeholder(value) else "- Not set"
            display_value = self.mask_secret(key) if show_values and value else ""
            print(f"{key:<30} {status:<15} {display_value}")

        # Other environment variables
        other_keys = [k for k in self.secrets.keys()
                      if k not in self.REQUIRED_KEYS + self.OPTIONAL_KEYS]
        if other_keys:
            print("\nOther Settings:")
            for key in sorted(other_keys):
                value = self.secrets[key]
                status = "✓ Set"
                display_value = value if show_values and key not in self.SENSITIVE_KEYS else ""
                print(f"{key:<30} {status:<15} {display_value}")

    def _is_placeholder(self, value: str) -> bool:
        """Check if a value is a placeholder."""
        placeholders = [
            'your_key_here',
            'your_api_key_here',
            'your_client_id_here',
            'your_client_secret_here',
            'xxxxx',
            'xxxxxxxx',
        ]
        return any(ph in value.lower() for ph in placeholders)

    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password."""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'firecrawl-video-pipeline',  # Fixed salt for consistency
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def _persist_to_env(self):
        """Persist current secrets to .env file."""
        # Create backup
        if self.env_file.exists():
            backup_file = f"{self.env_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.env_file.rename(backup_file)
            print(f"✓ Created backup: {backup_file}")

        # Write new .env
        with open(self.env_file, 'w') as f:
            f.write(f"# Updated: {datetime.now().isoformat()}\n\n")
            for key, value in sorted(self.secrets.items()):
                f.write(f"{key}={value}\n")

        print(f"✓ Saved {len(self.secrets)} secrets to {self.env_file}")


def main():
    """CLI interface for secrets manager."""
    import argparse

    parser = argparse.ArgumentParser(description='Secrets Manager for Video Pipeline')
    parser.add_argument('command', choices=['validate', 'list', 'export', 'generate-key'],
                       help='Command to execute')
    parser.add_argument('--env', default='.env', help='Path to .env file')
    parser.add_argument('--show-values', action='store_true', help='Show masked secret values')
    parser.add_argument('--environment', choices=['development', 'staging', 'production'],
                       help='Target environment')
    parser.add_argument('--output', help='Output file for export')

    args = parser.parse_args()

    if args.command == 'generate-key':
        import secrets
        key = secrets.token_hex(32)
        print(f"\nGenerated SECRET_KEY:\n{key}\n")
        print("Add this to your .env file:")
        print(f"SECRET_KEY={key}\n")
        return

    # Load secrets manager
    manager = SecretsManager(env_file=args.env)

    try:
        manager.load(required=False)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.command == 'validate':
        if manager.validate(strict=True):
            print("\n✓ All secrets are properly configured!")
            sys.exit(0)
        else:
            print("\n✗ Some secrets are missing or invalid")
            print("\nRun: python secrets_manager.py list --show-values")
            print("To see which secrets need to be configured")
            sys.exit(1)

    elif args.command == 'list':
        manager.list_secrets(show_values=args.show_values)

    elif args.command == 'export':
        if not args.environment:
            print("Error: --environment required for export")
            sys.exit(1)

        output_file = args.output or f".env.{args.environment}"
        manager.export_for_environment(args.environment, output_file)


if __name__ == '__main__':
    main()
