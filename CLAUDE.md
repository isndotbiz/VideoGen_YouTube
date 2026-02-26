# VideoGen_YouTube - Claude Code Instructions

## What This Repo Is

An automated AI-powered YouTube video generation pipeline. Converts a web article URL into a production-ready video through 11 stages: scraping, scripting, image/animation generation, narration, audio mixing, subtitles, composition, and upload.

## Quick Start

```bash
# Full pipeline from a URL
node orchestrate.js "https://example.com/article"

# Python orchestrator (ComfyUI → ElevenLabs → Shotstack → YouTube)
python video_pipeline.py
```

## Pipeline Stages at a Glance

```
URL → Firecrawl → Script → Colors → Images → Animations → Narration → Music → Subtitles → Compose → Upload
      (JSONL)    (Claude) (Manual) (FAL.ai) (FAL WAN2.5) (ElevenLabs)(Pexels) (AssemblyAI)(Shotstack)(YouTube OAuth)
```

Full stage reference: `MASTER_WORKFLOW_DOCUMENTATION.md`
Quick cheat sheet: `WORKFLOW_QUICK_REFERENCE.md`

## Critical Rules

1. **ElevenLabs is literal** - Use `[PAUSE:2000ms]` in scripts, NEVER "pause for 2 seconds". ElevenLabs will read instructions aloud.
2. **BGM volume is exactly 15%** - narration stays at 100%.
3. **Color palette consistency** - all images, infographics, and overlays must use the 5-color palette chosen for that video.
4. **Subtitle timing** - must sync to actual audio (not script timing). Use AssemblyAI output directly.
5. **Output standard** - 1920x1080, 24fps, H.264 codec, AAC audio.
6. **WCAG AA required** - all text overlays must pass color contrast.

## Key Files

| File | Purpose |
|------|---------|
| `orchestrate.js` | Node.js pipeline entry point |
| `video_pipeline.py` | Python pipeline orchestrator |
| `video_pipeline/` | Modular pipeline package (generators, assemblers, uploaders) |
| `elevenlabs_narration_WORKING.py` | Narration with correct ElevenLabs v2+ API |
| `generate_animations_with_fal.py` | FAL.ai WAN 2.5 image-to-video |
| `upload_to_youtube.py` | YouTube OAuth upload |
| `config.json` | Video resolution, bitrate, rendering settings |
| `workflow_config.json` | Pipeline step configuration |
| `.env` | All API keys (never commit this) |
| `requirements.txt` | Python dependencies |

## API Keys (in `.env`)

| Key | Service | Purpose |
|-----|---------|---------|
| `ELEVENLABS_API_KEY` | ElevenLabs | Narration (voice: Rachel) |
| `FAL_API_KEY` / `FAL_KEY` | fal.ai | Images (Flux) + animations (WAN 2.5) |
| `ASSEMBLYAI_API_KEY` | AssemblyAI | Speech-to-text subtitles |
| `PEXELS_API_KEY` | Pexels | Background music |
| `SHORTSTACK_API_KEY` | Shotstack | Video composition |
| `FIRECRAWL_API_KEY` | Firecrawl | Web scraping |
| `REPLICATE_API_KEY` | Replicate | Backup image/video gen |
| `OPENAI_API_KEY` | OpenAI | Backup TTS/script |
| `RUNWAY_API_KEY` | Runway | Backup video animation |
| YouTube OAuth | Google | Upload via `youtube_credentials.json` |
| AWS S3 | AWS | Asset storage |

## Failure Fallbacks

| Primary | Fallback |
|---------|---------|
| Firecrawl | Manual research + save URLs to text file |
| FAL.ai | Replicate API or local ComfyUI (localhost:8188) |
| ElevenLabs | `generate_narration_fallback.py` using OpenAI TTS |
| AssemblyAI | Basic SRT template with manual timing |
| Pexels music | Placeholder in /output folder |
| Shotstack | `final_video_ffmpeg_direct.py` |

## Serena Memories

See `.serena/memories/` for structured context:
- `project_overview.md` - Full tech stack, pipeline stages, output formats
- `suggested_commands.md` - All generation, upload, and utility commands
- `task_checklist.md` - Open issues, missing APIs, fragile components

## Context Template for New Sessions

> "Generate a video about [TOPIC] using MASTER_WORKFLOW_DOCUMENTATION.md stages.
> APIs are in .env. Follow WORKFLOW_QUICK_REFERENCE.md for [PAUSE] format and 15% BGM rule.
> Goal: [SPECIFIC_OUTPUT]. Stop before [NEXT_STAGE]."
