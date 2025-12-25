#!/usr/bin/env python3
"""
Configuration loader for API keys and settings from .env file
Uses python-dotenv to load environment variables
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    print("[WARNING] python-dotenv not installed. Install with: pip install python-dotenv")
    load_dotenv = None

# Load .env file
ENV_FILE = Path(__file__).parent / ".env"

if ENV_FILE.exists():
    if load_dotenv:
        load_dotenv(ENV_FILE)
    else:
        # Manual fallback if dotenv not installed
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()
else:
    print(f"[WARNING] .env file not found at {ENV_FILE}")
    print("[INFO] Create it from .env.example and fill in your API keys")

# ============================================
# API Configuration
# ============================================

class APIConfig:
    """API Configuration loaded from .env - ALL AVAILABLE APIS"""

    # ============================================
    # VIDEO GENERATION APIS
    # ============================================

    # FAL.ai - Text-to-video, Image generation
    FAL_API_KEY = os.getenv("FAL_API_KEY", "")

    # Runway ML - Video generation and editing
    RUNWAYML_API_KEY = os.getenv("RUNWAYML_API_KEY", "")

    # Replicate AI - Image/video/audio generation
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

    # Descript - Video assembly and editing
    DESCRIPT_API_KEY = os.getenv("DESCRIPT_API_KEY", "")

    # Shotstack - Professional video assembly
    SHOTSTACK_API_KEY = os.getenv("SHOTSTACK_API_KEY", "")
    SHOTSTACK_OWNER_ID = os.getenv("SHOTSTACK_OWNER_ID", "")
    SHOTSTACK_SANDBOX_API_KEY = os.getenv("SHOTSTACK_SANDBOX_API_KEY", "")

    # ============================================
    # AUDIO & SPEECH APIS
    # ============================================

    # ElevenLabs - Text-to-Speech
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

    # AssemblyAI - Speech-to-text and subtitles
    ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")

    # ============================================
    # LLM & AI MODELS
    # ============================================

    # OpenAI - GPT-4, ChatGPT
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Anthropic - Claude
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # Google Gemini - Advanced AI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Groq - Fast inference
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # Perplexity - AI search and synthesis
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

    # OpenRouter - Multi-model LLM access
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

    # ============================================
    # MEDIA & ASSET APIS
    # ============================================

    # Pexels - Stock images and videos
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

    # HuggingFace - Model and dataset hub
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

    # CivitAI - AI model sharing
    CIVITAI_API_KEY = os.getenv("CIVITAI_API_KEY", "")

    # ============================================
    # SEARCH & RESEARCH APIS
    # ============================================

    # Brave Search - Privacy-focused search
    BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY", "")

    # ============================================
    # PLATFORM APIS
    # ============================================

    # YouTube - Video publishing
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    YOUTUBE_REDIRECT_URI = os.getenv("YOUTUBE_REDIRECT_URI", "")

    # GitHub - Version control and automation
    GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN", "")

    # AWS - Cloud services
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION = os.getenv("AWS_REGION", "")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")

    # ============================================
    # LOCAL SERVICES
    # ============================================

    # ComfyUI - Local image generation
    COMFYUI_SERVER_URL = os.getenv("COMFYUI_SERVER_URL", "")
    COMFYUI_OUTPUT_DIR = os.getenv("COMFYUI_OUTPUT_DIR", "")

    # Salad Cloud - GPU computing
    SALAD_API_KEY = os.getenv("SALAD_API_KEY", "")

    @classmethod
    def check_required_apis(cls):
        """Check which required APIs are configured"""
        required = {
            "Pexels": cls.PEXELS_API_KEY,
            "ElevenLabs": cls.ELEVENLABS_API_KEY,
            "FAL.ai": cls.FAL_API_KEY,
            "AssemblyAI": cls.ASSEMBLYAI_API_KEY,
        }

        missing = [api for api, key in required.items() if not key or key.startswith("your_")]

        return {
            "total": len(required),
            "configured": len(required) - len(missing),
            "missing": missing,
            "all_ready": len(missing) == 0,
        }

    @classmethod
    def list_all_apis(cls):
        """List all available APIs and their status"""
        apis = {
            "Video Generation": {
                "FAL.ai": cls.FAL_API_KEY,
                "Runway ML": cls.RUNWAYML_API_KEY,
                "Replicate AI": cls.REPLICATE_API_TOKEN,
                "Descript": cls.DESCRIPT_API_KEY,
                "Shotstack": cls.SHOTSTACK_API_KEY,
            },
            "Audio & Speech": {
                "ElevenLabs": cls.ELEVENLABS_API_KEY,
                "AssemblyAI": cls.ASSEMBLYAI_API_KEY,
            },
            "LLM & AI Models": {
                "OpenAI": cls.OPENAI_API_KEY,
                "Anthropic (Claude)": cls.ANTHROPIC_API_KEY,
                "Google Gemini": cls.GEMINI_API_KEY,
                "Groq": cls.GROQ_API_KEY,
                "Perplexity": cls.PERPLEXITY_API_KEY,
                "OpenRouter": cls.OPENROUTER_API_KEY,
            },
            "Media & Assets": {
                "Pexels": cls.PEXELS_API_KEY,
                "HuggingFace": cls.HUGGINGFACE_TOKEN,
                "CivitAI": cls.CIVITAI_API_KEY,
            },
            "Search & Research": {
                "Brave Search": cls.BRAVE_SEARCH_API_KEY,
            },
            "Platforms": {
                "YouTube": cls.YOUTUBE_CLIENT_ID,
                "GitHub": cls.GITHUB_API_TOKEN,
                "AWS": cls.AWS_ACCESS_KEY_ID,
            },
            "Local Services": {
                "ComfyUI": cls.COMFYUI_SERVER_URL,
                "Salad Cloud": cls.SALAD_API_KEY,
            },
        }

        return apis

    @classmethod
    def print_status(cls):
        """Print comprehensive API configuration status"""
        apis = cls.list_all_apis()

        print("\n" + "="*80)
        print("API INVENTORY - COMPLETE CONFIGURATION")
        print("="*80)

        total_apis = 0
        configured_apis = 0

        for category, services in apis.items():
            print(f"\n[{category.upper()}]")
            print("-" * 80)

            for service_name, api_key in services.items():
                total_apis += 1
                status = "[READY]" if api_key and not api_key.startswith("your_") else "[MISSING]"

                if api_key and not api_key.startswith("your_"):
                    configured_apis += 1
                    display_key = api_key[:20] + "..." if len(api_key) > 20 else api_key
                    print(f"  {status} {service_name:25s} | {display_key}")
                else:
                    print(f"  {status} {service_name:25s} | Not configured")

        print("\n" + "="*80)
        print(f"SUMMARY: {configured_apis}/{total_apis} APIs configured")
        print("="*80)

        return {
            "total": total_apis,
            "configured": configured_apis,
            "missing": total_apis - configured_apis,
        }

# ============================================
# Video Configuration
# ============================================

class VideoConfig:
    """Video output configuration"""

    WIDTH = int(os.getenv("VIDEO_RESOLUTION_WIDTH", "1920"))
    HEIGHT = int(os.getenv("VIDEO_RESOLUTION_HEIGHT", "1080"))
    FPS = int(os.getenv("VIDEO_FPS", "24"))
    CODEC = os.getenv("VIDEO_CODEC", "libx264")
    AUDIO_CODEC = os.getenv("AUDIO_CODEC", "aac")
    AUDIO_BITRATE = os.getenv("AUDIO_BITRATE", "128k")

    NARRATION_VOLUME = float(os.getenv("NARRATION_VOLUME", "1.0"))
    BACKGROUND_MUSIC_VOLUME = float(os.getenv("BACKGROUND_MUSIC_VOLUME", "0.15"))

# ============================================
# Project Configuration
# ============================================

class ProjectConfig:
    """Project settings"""

    PROJECT_NAME = os.getenv("PROJECT_NAME", "free-ai-tools-course")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
    TEMP_DIR = os.getenv("TEMP_DIR", "temp")
    LOGS_DIR = os.getenv("LOGS_DIR", "logs")

    # Create directories if they don't exist
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    Path(TEMP_DIR).mkdir(exist_ok=True)
    Path(LOGS_DIR).mkdir(exist_ok=True)

    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================
# Setup Instructions
# ============================================

SETUP_INSTRUCTIONS = """
QUICK SETUP - 5 MINUTES

1. Edit the .env file in the project root:
   D:\\workspace\\VideoGen_YouTube\\.env

2. Replace placeholder values with your actual API keys:

   PEXELS_API_KEY=your_key_here
   ELEVENLABS_API_KEY=your_key_here
   FAL_API_KEY=your_key_here
   ASSEMBLYAI_API_KEY=your_key_here

3. Save the .env file

4. Run any video generation script:
   python test_pipeline_video_1.py

The configuration will be loaded automatically from .env!

API KEY LINKS:
- Pexels: https://www.pexels.com/api/
- ElevenLabs: https://elevenlabs.io
- FAL.ai: https://fal.ai/dashboard
- AssemblyAI: https://www.assemblyai.com

All keys are FREE with free accounts!
"""

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
    APIConfig.print_status()
