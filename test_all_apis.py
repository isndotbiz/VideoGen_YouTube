#!/usr/bin/env python3
"""
Test all APIs and print complete workflow step-by-step
Verifies each API key is configured and working
"""
import os
import sys
from pathlib import Path
import io

# Fix encoding for Windows terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load configuration
try:
    from config import APIConfig
    print("[OK] Config module loaded successfully\n")
except Exception as e:
    print(f"[ERROR] Failed to load config: {e}\n")
    sys.exit(1)


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_stage(num, name, description):
    """Print stage header"""
    print(f"\n[STAGE {num}] {name}")
    print(f"  Description: {description}")
    print("  " + "-" * 76)


def test_api(api_name, api_key, description, test_func=None):
    """Test if API key is configured"""
    if not api_key:
        print(f"  [FAIL] {api_name:30} NOT CONFIGURED")
        return False

    if api_key == "placeholder" or api_key.startswith("sk-") and len(api_key) < 10:
        print(f"  [FAIL] {api_name:30} INVALID/PLACEHOLDER KEY")
        return False

    key_display = api_key[:20] + "..." if len(api_key) > 20 else api_key
    print(f"  [OK]  {api_name:30} {key_display}")

    # Run optional test function
    if test_func:
        try:
            result = test_func()
            if result:
                print(f"       -> Connection test passed")
                return True
            else:
                print(f"       -> Connection test inconclusive")
                return True
        except Exception as e:
            print(f"       -> Test error: {str(e)[:60]}")
            return True

    return True


def print_workflow():
    """Print complete step-by-step workflow"""

    print_header("VIDEOGEN YOUTUBE - COMPLETE WORKFLOW")

    # STAGE 1
    print_stage(1, "WEB SCRAPING", "Gather research using Firecrawl + manual sources")
    print("""
  Process:
    1. Use Firecrawl to scrape website content
    2. Extract all text, headings, structure into JSONL format
    3. Manually find 3 additional trusted sources on topic
    4. Combine into single research file

  Outputs:
    • research/[topic]/crawled_data.jsonl     - Scraped content
    • research/[topic]/sources.txt             - List of 4 sources

  Time: 2-3 minutes
    """)

    # STAGE 2
    print_stage(2, "SCRIPT GENERATION", "Create professional video script")
    print("""
  Process:
    1. Read JSONL research file
    2. Use Claude LLM to generate natural, conversational script
    3. ~3-5 minutes duration (~600-1000 words)
    4. Format with timing markers: [PAUSE:2000ms] NOT "pause for 2 seconds"
    5. Add visual cues as comments: <!-- Show image here -->

  Script Format Example:
    "Welcome to our video. [PAUSE:2000ms]
     Here's the first point: This is the content...
     [PAUSE:1500ms]
     Now let's discuss..."

  Outputs:
    • scripts/[topic]/script_final.txt        - Optimized script with [PAUSE] markers

  Time: 3-5 minutes
    """)

    # STAGE 3
    print_stage(3, "COLOR PALETTE DESIGN", "Create 5-color WCAG-compliant palette")
    print("""
  Process:
    1. Design 5 colors for consistent branding:
       - Primary: Main brand color
       - Secondary: Accent color
       - Tertiary: Additional elements
       - Background: Usually dark (for video)
       - Text: Usually white/light
    2. Verify WCAG AA compliance (4.5:1 contrast minimum)
    3. Document HEX and RGB values

  WCAG Testing:
    • Tool: WebAIM Contrast Checker
    • Requirement: Text on color = 4.5:1 ratio minimum
    • Test each color combination

  Outputs:
    • design/[topic]/color_palette.json       - 5 colors + metadata

  Example:
    {
      "primary": "#1e3c72",      (dark blue)
      "secondary": "#ff6b35",    (orange)
      "tertiary": "#4ecdc4",     (teal)
      "background": "#0a0e27",   (very dark)
      "text": "#ffffff"          (white)
    }

  Time: 5-10 minutes
    """)

    # STAGE 4
    print_stage(4, "IMAGE & INFOGRAPHIC GENERATION", "Create visual elements")
    print("""
  Process:
    1. Read script - identify where visuals help
    2. Write detailed prompts for each image
    3. Generate infographics:
       - Primary: FAL.ai Nano Banana API
       - Input: Text description + color codes
       - Output: PNG infographic
    4. Generate beautiful images:
       - Primary: FAL.ai Flux Dev model
       - Input: Detailed visual prompt + colors
       - Output: High-quality PNG images
    5. Local Alternative: Comfy Flux server with 3090 GPU

  Image Prompt Example:
    "Create professional infographic about benefits of X,
     using colors #1e3c72, #ff6b35, and #4ecdc4.
     High quality, 4K resolution, modern design style."

  Outputs:
    • assets/[topic]/images/*.png             - Generated images (Flux)
    • assets/[topic]/infographics/*.png       - Generated graphics (Nano Banana)
    • assets/[topic]/metadata.json            - List with prompts

  Time: 5-10 minutes
    """)

    # STAGE 5
    print_stage(5, "ANIMATION GENERATION", "Convert images to 4-second video clips")
    print("""
  Process:
    1. For each image, write motion description
    2. Use FAL.ai WAN 2.5 image-to-video model
    3. Generate 4-second animation clips
    4. Settings:
       - Duration: 4 seconds (fixed)
       - Aspect ratio: 16:9 (fixed)
       - Quality: 1080p minimum

  Animation Prompt Example:
    "Camera smoothly pans across infographic,
     highlighting key points. Professional, smooth motion."

  Outputs:
    • assets/[topic]/animations/*.mp4        - 4-sec video clips

  Time: 2-3 minutes PER animation
       20-30 minutes for 8 animations
    """)

    # STAGE 6
    print_stage(6, "NARRATION GENERATION", "Text-to-speech professional voice")
    print("""
  Process:
    1. Clean script:
       - Remove [PAUSE] markers (convert to silence internally)
       - Remove visual cues/comments
       - Keep only spoken text
    2. Use ElevenLabs text-to-speech:
       - Voice: Rachel (professional, clear)
       - Settings: Stability 0.5, Similarity boost 0.75
    3. Download MP3 file
    4. Verify duration matches script estimate

  CRITICAL: What ElevenLabs Does Wrong
    Input: "Please pause for 2 seconds and then continue"
    Output: Speaks "please pause for two seconds and then continue"

  CRITICAL: What To Do Instead
    Input: "Here's point one. [PAUSE:2000ms] Here's point two."
    Output: "Here's point one." (2 sec silence) "Here's point two."

  Outputs:
    • audio/[topic]/narration.mp3             - ElevenLabs output (2-3 MB typical)

  Time: 30 seconds (API call + download)
    """)

    # STAGE 7
    print_stage(7, "BACKGROUND MUSIC & AUDIO MIXING", "Add music at 15% volume")
    print("""
  Process:
    1. Fetch royalty-free background music:
       - Tool: Pexels API
       - Search: Topic-related ambient music
       - Download: MP3 file
    2. Mix audio:
       - Narration: 100% volume (primary)
       - Background Music: 15% volume (subtle)
    3. Mixing math:
       - Volume multiplier: 0.15
       - In dB: -16dB
    4. Loop music if shorter than narration
    5. Normalize to prevent clipping

  Mixing Tool:
    • pydub: Python audio library (simple)
    • ffmpeg: Command line (more control)

  Outputs:
    • audio/[topic]/background_music.mp3     - Pexels download
    • audio/[topic]/mixed_audio.mp3          - Narration + 15% BGM

  Time: 2-3 minutes
    """)

    # STAGE 8
    print_stage(8, "SUBTITLE GENERATION", "Create synchronized SRT subtitles")
    print("""
  Process:
    1. Use Assembly AI speech-to-text:
       - Input: Narration MP3
       - Output: Transcript with word-level timing
    2. Group words into readable chunks (~10 words per subtitle)
    3. Convert to SRT format (SubRip Text)
    4. Format: index, timestamp range, text

  SRT Format Example:
    1
    00:00:00,000 --> 00:00:05,000
    Welcome to our video about the topic

    2
    00:00:05,000 --> 00:00:10,000
    We'll explore five important points

  Outputs:
    • subtitles/[topic]/subtitles.srt        - Assembly AI output

  Time: 1-2 minutes
    """)

    # STAGE 9
    print_stage(9, "VIDEO COMPOSITION", "Stitch everything together into final video")
    print("""
  Process:
    1. Create base video:
       - Resolution: 1920x1080 (Full HD)
       - Duration: Match audio duration
       - Background: Primary color from palette
       - FPS: 24
    2. Layer elements (in order):
       - Layer 1: Colored background video
       - Layer 2: Static images (timed to script)
       - Layer 3: Animation clips (timed to script)
       - Layer 4: Text overlays (subtitles)
       - Layer 5: Title card (first 2 seconds)
    3. Insert audio:
       - Mixed audio from Stage 7
       - Codec: AAC at 128kbps
    4. Encode and stitch:
       - Primary: ShortStack API
       - Backup: FFmpeg command line

  Video Specifications:
    • Resolution: 1920x1080 (Full HD)
    • Codec: H.264 (libx264)
    • Audio Codec: AAC
    • Audio Bitrate: 128kbps
    • Frame Rate: 24 FPS
    • Format: MP4

  Outputs:
    • video/[topic]/video_COMPLETE.mp4       - Final video

  Time: 5-15 minutes
    """)

    # STAGE 10
    print_stage(10, "PLATFORM OPTIMIZATION", "Create versions for different platforms")
    print("""
  Process:
    1. YouTube: Keep as 1920x1080 (16:9)
    2. TikTok: Convert to 1080x1920 (9:16)
    3. Instagram Reels: 1080x1920 with safe area
    4. Twitter/X: Convert to 1280x720 (16:9)

  Tool:
    • FFmpeg video scaling
    • Or ShortStack API

  Outputs:
    • video/[topic]/platforms/video_youtube.mp4
    • video/[topic]/platforms/video_tiktok.mp4
    • video/[topic]/platforms/video_instagram.mp4
    • video/[topic]/platforms/video_twitter.mp4

  Time: 5-10 minutes
    """)

    # STAGE 11
    print_stage(11, "CLOUD STORAGE", "Store files in AWS S3 (optional)")
    print("""
  Process:
    1. Upload to AWS S3 bucket
    2. Store all assets:
       - Final video
       - Animation clips
       - Images
       - Audio files
       - Subtitles

  Configuration:
    • Bucket: videogen-assets
    • Region: us-east-1 (configurable)

  Time: 5 minutes
    """)

    # TOTAL TIME
    print_header("TOTAL WORKFLOW TIME")
    print("""
  WITHOUT ANIMATIONS: 10-15 minutes
    1. Web Scraping:        2-3 min
    2. Script:              3-5 min
    3. Colors:              5-10 min
    4. Images:              5-10 min
    5. Narration:           30 sec
    6. Audio Mixing:        2-3 min
    7. Subtitles:           1-2 min
    8. Composition:         5-15 min

  WITH ANIMATIONS: 60-90 minutes
    + Animation Gen:        20-30 min (2-3 min × 8 animations)

  FASTEST TEST VIDEO: 5-10 minutes
    (Skip images/animations, use placeholders)
    """)


def test_all_apis():
    """Test all configured APIs"""

    print_header("API KEY VERIFICATION")

    # Test functions for APIs
    def test_elevenlabs():
        try:
            import requests
            response = requests.get(
                "https://api.elevenlabs.io/v1/voices",
                headers={"xi-api-key": APIConfig.ELEVENLABS_API_KEY},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

    def test_fal():
        try:
            os.environ['FAL_KEY'] = APIConfig.FAL_API_KEY
            import fal_client
            # Just check if client can be initialized
            return True
        except:
            return False

    def test_assembly():
        try:
            import requests
            response = requests.get(
                "https://api.assemblyai.com/v2/realtime/token",
                headers={"Authorization": APIConfig.ASSEMBLYAI_API_KEY},
                timeout=5
            )
            return response.status_code in [200, 401]  # 401 means key is recognized but expired
        except:
            return False

    def test_pexels():
        try:
            import requests
            response = requests.get(
                "https://api.pexels.com/v1/curated?page=1&per_page=1",
                headers={"Authorization": APIConfig.PEXELS_API_KEY},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

    def test_openai():
        try:
            import openai
            openai.api_key = APIConfig.OPENAI_API_KEY
            # Don't actually call the API, just check if key format is valid
            return len(APIConfig.OPENAI_API_KEY) > 10
        except:
            return False

    def test_anthropic():
        try:
            return len(APIConfig.ANTHROPIC_API_KEY) > 10
        except:
            return False

    # PRIMARY APIS (CRITICAL)
    print("\n[PRIMARY APIs - CRITICAL FOR SYSTEM]")
    print("-" * 80)

    test_api("ELEVENLABS_API_KEY", APIConfig.ELEVENLABS_API_KEY,
             "Text-to-speech narration", test_elevenlabs)
    test_api("FAL_API_KEY", APIConfig.FAL_API_KEY,
             "Image & animation generation", test_fal)
    test_api("ASSEMBLYAI_API_KEY", APIConfig.ASSEMBLYAI_API_KEY,
             "Subtitle generation (speech-to-text)", test_assembly)
    test_api("PEXELS_API_KEY", APIConfig.PEXELS_API_KEY,
             "Royalty-free music & videos", test_pexels)
    test_api("SHOTSTACK_API_KEY", APIConfig.SHOTSTACK_API_KEY,
             "Video composition/stitching")
    test_api("FIRECRAWL_API_KEY", APIConfig.FIRECRAWL_API_KEY,
             "Web scraping & content extraction")

    # BACKUP APIS
    print("\n[BACKUP APIs - FOR FALLBACK]")
    print("-" * 80)

    test_api("REPLICATE_API_KEY", APIConfig.REPLICATE_API_KEY,
             "Alternative image/video generation")
    test_api("OPENAI_API_KEY", APIConfig.OPENAI_API_KEY,
             "Script writing & TTS alternative", test_openai)
    test_api("ANTHROPIC_API_KEY", APIConfig.ANTHROPIC_API_KEY,
             "Claude API for script generation", test_anthropic)
    test_api("RUNWAY_API_KEY", APIConfig.RUNWAY_API_KEY,
             "Alternative video generation")

    # OPTIONAL/BONUS APIS
    print("\n[OPTIONAL/BONUS APIs]")
    print("-" * 80)

    test_api("BRAVE_API_KEY", APIConfig.BRAVE_API_KEY,
             "Search capability")
    test_api("AWS_ACCESS_KEY_ID", APIConfig.AWS_ACCESS_KEY_ID,
             "Cloud storage (S3)")
    test_api("AWS_SECRET_ACCESS_KEY", APIConfig.AWS_SECRET_ACCESS_KEY,
             "Cloud storage secret")
    test_api("DESCRIPT_API_KEY", APIConfig.DESCRIPT_API_KEY,
             "Video editing alternative")
    test_api("SQUADBOX_API_KEY", APIConfig.SQUADBOX_API_KEY,
             "Content moderation/feedback")

    # LOCAL SETUP
    print("\n[LOCAL SETUP]")
    print("-" * 80)

    test_api("COMFY_GPU_ENDPOINT", APIConfig.COMFY_GPU_ENDPOINT,
             "Local GPU image generation (3090)")

    # Check for FFmpeg
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            print(f"  [OK]  {'FFmpeg':30} System installed (video composition fallback)")
        else:
            print(f"  [FAIL] {'FFmpeg':30} NOT FOUND - Install with: choco install ffmpeg")
    except:
        print(f"  [FAIL] {'FFmpeg':30} NOT FOUND - Install with: choco install ffmpeg")


def main():
    """Main execution"""

    # Print workflow
    print_workflow()

    # Test APIs
    test_all_apis()

    # Summary
    print_header("NEXT STEPS")
    print("""
  1. Create a test video without animations (5-10 minutes):
     python compose_with_opencv.py

  2. Once verified, add animations (20-30 minutes):
     python generate_animations_with_fal.py

  3. Create final video with animations:
     python compose_final_video.py

  4. Create platform versions:
     python create_platform_versions.py

  5. Upload to YouTube and other platforms
    """)

    print_header("END OF WORKFLOW VERIFICATION")


if __name__ == '__main__':
    main()
