#!/usr/bin/env node
/**
 * Complete Workflow: Generate Video with AssemblyAI Subtitles
 *
 * Steps:
 * 1. Scrape article
 * 2. Clean JSONL
 * 3. Generate script
 * 4. Generate images
 * 5. Generate narration
 * 6. Assemble video (FFmpeg or Shotstack)
 * 7. Generate subtitles (AssemblyAI)
 * 8. Embed subtitles into video
 * 9. Upload to YouTube
 *
 * Usage: node generate-video-with-subtitles.js "https://example.com"
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
require('dotenv').config();

const Logger = require('./lib/logger');
const CostTracker = require('./lib/cost-tracker');
const ErrorHandler = require('./lib/error-handler');
const AssemblyAISubtitler = require('./lib/assemblyai-subtitler');

const logger = new Logger('./logs');
const costTracker = new CostTracker(10.0, logger);
const errorHandler = new ErrorHandler(logger);

const DEFAULT_URL = 'https://zapier.com/blog/claude-vs-chatgpt/';

/**
 * Run existing pipeline
 */
async function runPipeline(url) {
  logger.stage('Running complete video pipeline');

  try {
    // Phases 1-6: Use existing pipeline
    const cmd = `node pipeline-complete.js "${url}"`;
    logger.info(`Executing: ${cmd}`);
    execSync(cmd, { stdio: 'inherit' });

    return true;
  } catch (error) {
    logger.error('Pipeline failed', error);
    throw error;
  }
}

/**
 * Generate subtitles with AssemblyAI
 */
async function generateSubtitles() {
  logger.stage('PHASE 7: GENERATE SUBTITLES (AssemblyAI)');

  try {
    const audioFile = './output/narration.mp3';
    if (!fs.existsSync(audioFile)) {
      throw new Error('Narration file not found');
    }

    const subtitler = new AssemblyAISubtitler(logger);
    const result = await subtitler.generateSubtitles(audioFile, './output/subtitles.srt');

    const cost = parseFloat(result.cost);
    costTracker.addCall('assemblyai', 'transcription', cost, {
      duration: result.duration,
      lines: result.lines,
    });

    logger.success(`Phase 7 complete: Subtitles generated ($${result.cost})`);
    errorHandler.saveCheckpoint('phase7-subtitles', { result });

    return result;
  } catch (error) {
    logger.error('Subtitle generation failed', error);
    throw error;
  }
}

/**
 * Embed subtitles into video
 */
async function embedSubtitles() {
  logger.stage('PHASE 8: EMBED SUBTITLES INTO VIDEO');

  try {
    const videoFile = './output/final_video.mp4';
    const subtitleFile = './output/subtitles.srt';
    const outputFile = './output/final_video_with_subs.mp4';

    if (!fs.existsSync(videoFile)) {
      throw new Error('Video file not found');
    }

    if (!fs.existsSync(subtitleFile)) {
      throw new Error('Subtitle file not found');
    }

    logger.info('Checking for FFmpeg...');
    try {
      execSync('ffmpeg -version', { stdio: 'pipe' });
    } catch {
      logger.warn('FFmpeg not found - subtitles generated but not embedded');
      logger.info('To embed subtitles, install FFmpeg and run:');
      logger.info(`  node embed-subtitles.js "${videoFile}" "${subtitleFile}" "${outputFile}"`);
      return false;
    }

    logger.info('Embedding subtitles with FFmpeg...');
    const cmd = `ffmpeg -i "${videoFile}" -i "${subtitleFile}" -c:v copy -c:a copy -c:s mov_text "${outputFile}"`;

    execSync(cmd, { stdio: 'inherit' });

    if (!fs.existsSync(outputFile)) {
      throw new Error('Failed to create output video');
    }

    logger.success('Phase 8 complete: Subtitles embedded');
    logger.info(`Output: ${outputFile}`);

    errorHandler.saveCheckpoint('phase8-embedded', { outputFile });
    return true;
  } catch (error) {
    logger.error('Subtitle embedding failed', error);
    throw error;
  }
}

/**
 * Main workflow
 */
async function main() {
  const startTime = Date.now();

  try {
    const url = process.argv[2] || DEFAULT_URL;

    logger.info('\n' + '='.repeat(70));
    logger.info('Complete Video Generation with AssemblyAI Subtitles');
    logger.info(`URL: ${url}`);
    logger.info('='.repeat(70) + '\n');

    // Run main pipeline (phases 1-6)
    logger.stage('PHASES 1-6: Running Main Pipeline');
    await runPipeline(url);

    // Generate subtitles
    const subtitleResult = await generateSubtitles();

    // Embed subtitles
    const embedResult = await embedSubtitles();

    // Final report
    const duration = Date.now() - startTime;
    const durationMin = (duration / 1000 / 60).toFixed(1);

    logger.stage('COMPLETE VIDEO GENERATION FINISHED');
    logger.summary({
      total_duration: `${durationMin} minutes`,
      total_cost: costTracker.getTotal().toFixed(2),
      cost_breakdown: costTracker.getByService(),
      video_file: embedResult
        ? './output/final_video_with_subs.mp4'
        : './output/final_video.mp4',
      subtitle_file: './output/subtitles.srt',
      next_step: 'Upload to YouTube',
    });

    logger.info(`\n✅ Video ready for YouTube!`);
    logger.info(
      `   File: ${embedResult ? './output/final_video_with_subs.mp4' : './output/final_video.mp4'}`
    );
    logger.info(`   Subtitles: ./output/subtitles.srt`);
    logger.info(`   Total cost: ~$${costTracker.getTotal().toFixed(2)}\n`);
  } catch (error) {
    logger.error('COMPLETE WORKFLOW FAILED', error);
    logger.info(`\nLog file: ${logger.getLogFile()}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(err => {
    logger.error('Fatal error', err);
    process.exit(1);
  });
}

module.exports = { main, runPipeline, generateSubtitles, embedSubtitles };
