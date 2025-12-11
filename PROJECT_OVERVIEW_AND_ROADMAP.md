# VideoGen_YouTube - AI-Powered Video Generation Platform

## Project Overview

An automated YouTube video generation system that creates educational/informational videos from web content using cutting-edge AI APIs.

### Current Tech Stack

- **Image Generation**: fal.ai (Flux Pro, Nano Banana Pro for text-heavy images)
- **Video Animation**: Runway API
- **Text-to-Speech**: ElevenLabs API
- **Video Assembly**: Custom Python pipeline
- **YouTube Upload**: OAuth integration with SEO optimization
- **Cloud Storage**: AWS S3 (for asset management)

## Current Capabilities

✅ Web scraping and content extraction (Firecrawl)
✅ JSONL dataset creation from Markdown
✅ AI-powered image generation (fal.ai Flux models)
✅ Text-heavy image generation (Nano Banana)
✅ Video animation (Runway)
✅ Text-to-speech narration (ElevenLabs)
✅ Automated YouTube upload with SEO
✅ Batch processing and parallel execution
✅ AWS S3 asset storage

## Known Issues & Improvements Needed

### 🔴 Critical Issues

1. **ElevenLabs Narration Control**
   - **Problem**: Cannot add pauses, pacing, or emphasis in narration
   - **Impact**: Narration sounds robotic, no dramatic pauses
   - **Solution Needed**: Implement SSML-like markup or ElevenLabs API features for timing control

2. **Image Quality Issues**
   - **Problem**: Auto-selected images are low quality
   - **Impact**: Final videos look unprofessional
   - **Solution Needed**: Better prompt engineering, quality validation, manual review step

3. **Script Humanization**
   - **Problem**: Generated scripts sound AI-written
   - **Impact**: Videos lack natural flow and engagement
   - **Solution Needed**: Integrate AI humanizer API before narration generation

### 🟡 High Priority Features

4. **Subtitle/Caption Integration**
   - **Status**: Not implemented
   - **Goal**: Add professional subtitles to videos
   - **Tools**: Canva API integration or alternative subtitle generation
   - **Benefits**: Accessibility, engagement, professionalism

5. **Background Audio**
   - **Status**: Missing
   - **Goal**: Add subtle background music to videos
   - **Needs**: Music library integration, audio mixing enhancement
   - **Benefits**: Professional polish, emotional engagement

6. **Video Stitching Improvement**
   - **Status**: Using basic API stitching
   - **Goal**: Implement Canva API for better composition
   - **Benefits**: Better transitions, text overlays, visual effects

### 🟢 Enhancements

7. **AWS S3 Integration Expansion**
   - **Status**: Partial implementation
   - **Goal**: Full asset lifecycle management
   - **Features Needed**:
     - Automatic bucket creation per project
     - Asset versioning
     - Cleanup of old assets
     - CDN integration for faster delivery

8. **Better Prompt Engineering**
   - **Goal**: Improve image generation quality
   - **Needs**: Prompt templates, style consistency, quality checks

9. **YouTube SEO Optimization**
   - **Status**: Basic implementation
   - **Goal**: Enhanced metadata, thumbnail generation, tag optimization

## Roadmap & Implementation Plan

### Phase 1: Critical Fixes (Week 1-2)

#### Task 1.1: ElevenLabs Timing Control
- Research ElevenLabs API capabilities for pauses
- Implement script preprocessing with timing markers
- Add `<break>` or similar syntax support
- Test various timing patterns

#### Task 1.2: Script Humanization Pipeline
- Research AI humanizer APIs (e.g., Undetectable AI, QuillBot, etc.)
- Integrate humanizer API into pipeline
- Add before/after comparison
- Implement quality checks

#### Task 1.3: Image Quality Enhancement
- Review current prompt templates
- Implement image quality scoring
- Add manual review checkpoints
- Create prompt improvement guidelines

### Phase 2: Feature Additions (Week 3-4)

#### Task 2.1: Subtitle Generation
- Research Canva API for subtitle support
- Alternatively: Implement Whisper API for auto-transcription
- Add subtitle burning to video pipeline
- Style customization options

#### Task 2.2: Background Audio Integration
- Source royalty-free music library
- Implement audio mixing with narration
- Add volume balancing
- Create music selection logic based on content

#### Task 2.3: AWS S3 Enhancement
- Create S3 bucket management module
- Implement automatic asset upload
- Add asset cleanup cron job
- Set up CloudFront CDN (optional)

### Phase 3: Polish & Optimization (Week 5-6)

#### Task 3.1: Canva API Integration
- Evaluate Canva API capabilities
- Implement video composition via Canva
- Add professional templates
- A/B test vs current stitching method

#### Task 3.2: Enhanced YouTube Upload
- Improve SEO metadata generation
- Add thumbnail auto-generation
- Implement analytics tracking
- Add upload scheduling

#### Task 3.3: Quality Assurance Pipeline
- Automated quality checks
- Content moderation
- Brand consistency validation
- Performance metrics

## API Keys & Services Needed

### Currently Configured
- ✅ fal.ai API (Flux Pro, Nano Banana)
- ✅ Runway API
- ✅ ElevenLabs API
- ✅ AWS S3 credentials
- ✅ YouTube OAuth

### Need to Add
- ⬜ AI Humanizer API (e.g., Undetectable AI, QuillBot)
- ⬜ Canva API (for subtitles/video composition)
- ⬜ Music/Audio library API (e.g., Epidemic Sound, AudioJungle)
- ⬜ (Optional) Whisper API for transcription
- ⬜ (Optional) CloudFront for CDN

## Configuration Files to Update

1. `config.json` - Add new API keys and service endpoints
2. `workflow_config.json` - Add new pipeline steps
3. `.env` - Store sensitive credentials
4. `requirements.txt` - Add new Python dependencies

## Success Metrics

- **Image Quality**: 90%+ manual approval rate
- **Narration Quality**: Natural-sounding with proper pacing
- **Video Polish**: Professional subtitles, smooth transitions, background audio
- **Upload Success**: Optimized SEO, good initial engagement
- **Production Speed**: Maintain or improve current batch processing times

## Next Steps

1. ✅ Separate from True_Nas project (DONE)
2. ⬜ Set up dedicated Git repo and push
3. ⬜ Audit current API usage and costs
4. ⬜ Research and select AI humanizer API
5. ⬜ Research Canva API capabilities and pricing
6. ⬜ Source background music library
7. ⬜ Begin Phase 1 implementation

## Related Projects

- **True_Nas**: Main TrueNAS server management (separate repo)
- **Baby_Nas**: Local VM TrueNAS for backups (separate repo)

---

**Project Status**: Active Development
**Last Updated**: December 11, 2025
**Priority**: High - Content Creation Platform
