"""
Configuration Loader for Video Pipeline
Handles loading settings from config.json and .env files
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Loads and validates configuration from multiple sources"""

    def __init__(self, config_path: Optional[str] = None, env_path: Optional[str] = None):
        """
        Initialize configuration loader

        Args:
            config_path: Path to config.json file
            env_path: Path to .env file
        """
        self.base_dir = Path(__file__).parent
        self.config_path = Path(config_path) if config_path else self.base_dir / "config.json"
        self.env_path = Path(env_path) if env_path else self.base_dir / ".env"

        self.config = {}
        self.env_vars = {}
        self._load_configuration()

    def _load_configuration(self):
        """Load configuration from all sources"""
        # Load environment variables
        if self.env_path.exists():
            load_dotenv(self.env_path)
            logger.info(f"Loaded environment variables from {self.env_path}")
        else:
            logger.warning(f"No .env file found at {self.env_path}")

        # Load JSON configuration
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Loaded configuration from {self.config_path}")
        else:
            logger.warning(f"No config.json found at {self.config_path}, using defaults")
            self.config = self._get_default_config()

        # Override with environment variables
        self._apply_env_overrides()

        # Validate configuration
        self._validate_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "comfyui": {
                "host": "127.0.0.1",
                "port": 8188,
                "timeout": 300,
                "max_retries": 3
            },
            "pipeline": {
                "checkpoint_dir": "checkpoints",
                "enable_checkpoints": True,
                "dry_run": False,
                "verbose": True
            },
            "retry": {
                "max_attempts": 3,
                "initial_delay": 1,
                "max_delay": 60,
                "exponential_base": 2
            },
            "logging": {
                "level": "INFO",
                "console": True
            }
        }

    def _apply_env_overrides(self):
        """Apply environment variable overrides to configuration"""
        # API Keys
        api_keys = {
            "ELEVENLABS_API_KEY": ("elevenlabs", "api_key"),
            "FAL_API_KEY": ("fal", "api_key"),
            "SHOTSTACK_API_KEY": ("shotstack", "api_key"),
            "YOUTUBE_CLIENT_ID": ("youtube", "client_id"),
            "YOUTUBE_CLIENT_SECRET": ("youtube", "client_secret"),
        }

        for env_var, (section, key) in api_keys.items():
            value = os.getenv(env_var)
            if value:
                if section not in self.config:
                    self.config[section] = {}
                self.config[section][key] = value

        # ComfyUI overrides
        if os.getenv("COMFYUI_HOST"):
            self.config.setdefault("comfyui", {})["host"] = os.getenv("COMFYUI_HOST")
        if os.getenv("COMFYUI_PORT"):
            self.config.setdefault("comfyui", {})["port"] = int(os.getenv("COMFYUI_PORT"))

        # ElevenLabs voice ID
        if os.getenv("ELEVENLABS_VOICE_ID"):
            self.config.setdefault("elevenlabs", {})["voice_id"] = os.getenv("ELEVENLABS_VOICE_ID")

        # Pipeline settings
        if os.getenv("DRY_RUN"):
            dry_run = os.getenv("DRY_RUN").lower() in ("true", "1", "yes")
            self.config.setdefault("pipeline", {})["dry_run"] = dry_run

        if os.getenv("VERBOSE"):
            verbose = os.getenv("VERBOSE").lower() in ("true", "1", "yes")
            self.config.setdefault("pipeline", {})["verbose"] = verbose

        if os.getenv("MAX_RETRIES"):
            max_retries = int(os.getenv("MAX_RETRIES"))
            self.config.setdefault("retry", {})["max_attempts"] = max_retries

    def _validate_config(self):
        """Validate required configuration values"""
        errors = []

        # Check for required API keys (only if not in dry run mode)
        if not self.get("pipeline.dry_run", False):
            required_keys = [
                ("elevenlabs.api_key", "ElevenLabs API key"),
                ("shotstack.api_key", "Shotstack API key"),
            ]

            for key_path, description in required_keys:
                if not self.get(key_path):
                    errors.append(f"Missing {description} ({key_path})")

        # Validate ComfyUI configuration
        comfyui_port = self.get("comfyui.port")
        if comfyui_port and not (1 <= comfyui_port <= 65535):
            errors.append(f"Invalid ComfyUI port: {comfyui_port}")

        # Validate retry configuration
        max_attempts = self.get("retry.max_attempts", 3)
        if max_attempts < 1:
            errors.append(f"retry.max_attempts must be >= 1, got {max_attempts}")

        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info("Configuration validation successful")

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation

        Args:
            key_path: Dot-separated path (e.g., 'comfyui.host')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation

        Args:
            key_path: Dot-separated path (e.g., 'comfyui.host')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section

        Args:
            section: Section name (e.g., 'comfyui')

        Returns:
            Configuration section dictionary
        """
        return self.config.get(section, {})

    def ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            self.get("comfyui.output_dir", "outputs/images"),
            self.get("elevenlabs.output_dir", "outputs/audio"),
            self.get("fal.output_dir", "outputs/images/fal_fallback"),
            self.get("shotstack.output_dir", "outputs/videos"),
            self.get("pipeline.checkpoint_dir", "checkpoints"),
            os.path.dirname(self.get("logging.file", "logs/video_pipeline.log")),
            "credentials",
            "workflows",
        ]

        for directory in directories:
            path = self.base_dir / directory
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {path}")

    def save_config(self, output_path: Optional[str] = None):
        """
        Save current configuration to JSON file

        Args:
            output_path: Path to save config (defaults to original config path)
        """
        output_path = Path(output_path) if output_path else self.config_path

        with open(output_path, 'w') as f:
            json.dump(self.config, f, indent=2)

        logger.info(f"Configuration saved to {output_path}")

    def __repr__(self) -> str:
        return f"ConfigLoader(config_path={self.config_path})"


# Convenience function for quick loading
def load_config(config_path: Optional[str] = None, env_path: Optional[str] = None) -> ConfigLoader:
    """
    Load configuration with default paths

    Args:
        config_path: Optional path to config.json
        env_path: Optional path to .env file

    Returns:
        ConfigLoader instance
    """
    return ConfigLoader(config_path, env_path)


if __name__ == "__main__":
    # Test configuration loading
    logging.basicConfig(level=logging.DEBUG)

    config = load_config()
    config.ensure_directories()

    print("\nConfiguration loaded successfully!")
    print(f"ComfyUI host: {config.get('comfyui.host')}")
    print(f"ComfyUI port: {config.get('comfyui.port')}")
    print(f"Dry run mode: {config.get('pipeline.dry_run')}")
    print(f"Verbose mode: {config.get('pipeline.verbose')}")
    print(f"\nFull ComfyUI config: {config.get_section('comfyui')}")
