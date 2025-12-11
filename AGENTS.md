# Repository Guidelines

## Project Structure & Module Organization
- Root JavaScript pipeline (`orchestrate.js`, `scrape-and-convert.js`, `clean-jsonl.js`, `generate-video-script.js`) handles scraping, JSONL cleanup, and script generation; see `package.json` for entry points.
- Python orchestration lives in `run_video_pipeline.py` plus supporting tools such as `fal_batch_generator.py`, `run_pipeline_parallel.py`, and `video_pipeline/` (assemblers, generators, uploaders, utils).
- Configuration and secrets: `.env` (copy from `.env.example`), `workflow_config.json`, `video_pipeline/config.json`, and prompt/script sources like `prompts.json` and `VIDEO_SCRIPTS_ALL_VARIATIONS.md`.
- Outputs and artifacts land in `output/`, `temp/`, `logs/`, and `generated_images/`; keep large or derived files out of commits.

## Setup, Build, and Development Commands
- Node toolchain: `npm install` then `node orchestrate.js "<url>"` for the full scrape → script pipeline. Run individual stages with `node scrape-and-convert.js "<url>"`, `node clean-jsonl.js dataset.jsonl`, or `node generate-video-script.js`.
- Python environment: `python -m venv .venv && .\\.venv\\Scripts\\activate` (Windows) followed by `pip install -r requirements.txt`.
- Video pipeline run: `python run_video_pipeline.py` (single-threaded) or `python run_pipeline_parallel.py` (parallel phases) assuming required APIs (FAL, ElevenLabs, Shotstack, ComfyUI) are configured.

## Coding Style & Naming Conventions
- Python: 4-space indent, type hints where practical, snake_case for functions/vars, PascalCase for classes, UPPER_CASE for constants. Format with `black`, lint with `flake8`, and type-check with `mypy` (see `requirements.txt`).
- JavaScript: CommonJS modules, 2-space indent preferred, camelCase for functions/vars, PascalCase for constructors. Keep scripts idempotent and avoid writing outside the documented output directories.
- Logging: favor the existing `logging` setup in Python and concise `console.log` statements in Node scripts.

## Testing Guidelines
- Framework: `pytest` (with `pytest-asyncio` available). Run locally with `python -m pytest` or `python -m pytest --cov` for coverage.
- Place tests alongside sources or in root `test_*.py` files; mirror module names and keep fixtures small. For API-heavy code, mock external calls to avoid hitting paid services.

## Commit & Pull Request Guidelines
- Commit messages: short, imperative subject lines (e.g., `Add batch retry for Shotstack`); initial history is minimal, so favor descriptive commits over large bundles.
- Before opening a PR: include a brief summary, affected commands (example invocations), validation steps (tests run), and screenshots or log excerpts when outputs change. Reference related issues or docs where applicable.

## Security & Configuration Tips
- Never commit `.env`, API keys, or service tokens. Use the provided `.env.example` as a template and document required keys in your PR description if you add new ones.
- Review generated artifacts before sharing; strip PII and remove heavy media from version control. Keep service timeouts and cost estimates aligned with existing pipeline defaults unless justified.
