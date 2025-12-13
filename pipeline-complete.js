#!/usr/bin/env node
/**
 * COMPLETE VIDEO GENERATION PIPELINE
 * One script to rule them all: Research → Script → Images → Narration → Video → YouTube
 *
 * Usage:
 *   node pipeline-complete.js "https://example.com/article"
 *   node pipeline-complete.js              (uses default URL)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
require('dotenv').config();

const Logger = require('./lib/logger');
const CostTracker = require('./lib/cost-tracker');
const ErrorHandler = require('./lib/error-handler');
const ResearchEngine = require('./lib/research-engine');
const ImagePromptGenerator = require('./lib/image-prompt-generator');
const FFmpegAssembler = require('./lib/ffmpeg-assembler');
const DescriptVideoEditor = require('./descript-video-editor');
const ShotstackAssembler = require('./lib/shotstack-assembler');

const logger = new Logger('./logs');
const costTracker = new CostTracker(10.0, logger);
const errorHandler = new ErrorHandler(logger);
const researchEngine = new ResearchEngine(process.env.BRAVE_SEARCH_API_KEY, logger);
const promptGenerator = new ImagePromptGenerator(logger);
const videoAssembler = new FFmpegAssembler(logger);

const DEFAULT_URL = 'https://www.nathanonn.com/claude-code-vs-codex-why-i-use-both-and-you-should-too/';

/**
 * Phase 1: Scrape & convert to JSONL
 */
async function phase1Scrape(url) {
  logger.stage('PHASE 1: SCRAPE & CONVERT TO JSONL');

  try {
    const cmd = `node scrape-and-convert.js "${url}"`;
    logger.info(`Executing: ${cmd}`);
    execSync(cmd, { stdio: 'inherit' });

    // Verify output
    if (!fs.existsSync('dataset.jsonl')) {
      throw new Error('Scrape failed - dataset.jsonl not created');
    }

    logger.success('Phase 1 complete: JSONL created');
    errorHandler.saveCheckpoint('phase1-jsonl', { url, timestamp: new Date().toISOString() });
    return true;

  } catch (error) {
    logger.error('Phase 1 failed', error);
    throw error;
  }
}

/**
 * Phase 2: Clean JSONL
 */
async function phase2Clean() {
  logger.stage('PHASE 2: CLEAN JSONL');

  try {
    const cmd = 'node clean-jsonl.js dataset.jsonl';
    logger.info(`Executing: ${cmd}`);
    execSync(cmd, { stdio: 'inherit' });

    logger.success('Phase 2 complete: JSONL cleaned');
    errorHandler.saveCheckpoint('phase2-cleaned', { timestamp: new Date().toISOString() });
    return true;

  } catch (error) {
    logger.error('Phase 2 failed', error);
    throw error;
  }
}

/**
 * Phase 3: Generate script with image prompts
 */
async function phase3Script() {
  logger.stage('PHASE 3: GENERATE SCRIPT & IMAGE PROMPTS');

  try {
    const cmd = 'node generate-video-script.js dataset.jsonl';
    logger.info(`Executing: ${cmd}`);
    execSync(cmd, { stdio: 'inherit' });

    // Load generated prompts
    const promptsFile = './output/image-prompts.json';
    if (!fs.existsSync(promptsFile)) {
      throw new Error('Image prompts not generated');
    }

    const prompts = JSON.parse(fs.readFileSync(promptsFile, 'utf8'));
    logger.success(`Phase 3 complete: ${prompts.total} image prompts generated`);

    errorHandler.saveCheckpoint('phase3-script', { prompts });
    return prompts;

  } catch (error) {
    logger.error('Phase 3 failed', error);
    throw error;
  }
}

/**
 * Phase 4: Generate images (Flux + Nano Banana)
 */
async function phase4Images(prompts) {
  logger.stage('PHASE 4: GENERATE IMAGES');

  try {
    const cmd = 'python image-generation-nano-banana.py';
    logger.info(`Executing: ${cmd}`);
    execSync(cmd, { stdio: 'inherit' });

    // Cost estimation
    const fluxCost = prompts.photorealistic.length * 0.06;
    const nanoCost = prompts.textbased.length * 0.015;
    const totalImageCost = fluxCost + nanoCost;

    costTracker.addCall('fal', 'flux-pro', fluxCost, { count: prompts.photorealistic.length });
    costTracker.addCall('fal', 'nano-banana', nanoCost, { count: prompts.textbased.length });

    logger.success(`Phase 4 complete: Images generated ($${totalImageCost.toFixed(2)})`);
    errorHandler.saveCheckpoint('phase4-images', { prompts, cost: totalImageCost });
    return true;

  } catch (error) {
    logger.error('Phase 4 failed', error);
    throw error;
  }
}

/**
 * Phase 5: Generate narration
 */
async function phase5Narration() {
  logger.stage('PHASE 5: GENERATE NARRATION');

  try {
    const cmd = 'python elevenlabs_narration_WORKING.py';
    logger.info(`Executing: ${cmd}`);
    execSync(cmd, { stdio: 'inherit' });

    // Cost estimation (roughly $0.45 for 1500 words)
    const narrationCost = 0.45;
    costTracker.addCall('elevenlabs', 'text-to-speech', narrationCost, { words: 1500 });

    logger.success(`Phase 5 complete: Narration generated ($${narrationCost.toFixed(2)})`);
    errorHandler.saveCheckpoint('phase5-narration', { cost: narrationCost });
    return true;

  } catch (error) {
    logger.error('Phase 5 failed', error);
    throw error;
  }
}

/**
 * Phase 6: Generate Runway videos
 */
async function phase6Videos() {
  logger.stage('PHASE 6: GENERATE RUNWAY VIDEOS');

  try {
    // Queue videos
    const cmd = 'node runway-video-generator.js --batch';
    logger.info(`Executing: ${cmd}`);
    const output = execSync(cmd, { encoding: 'utf8', stdio: 'pipe' });
    logger.info(`Runway output: ${output}`);

    // Cost estimation (5 videos * $0.08)
    const videoCost = 5 * 0.08;
    costTracker.addCall('runway', 'gen3', videoCost, { count: 5 });

    logger.success(`Phase 6 complete: Videos queued ($${videoCost.toFixed(2)})`);
    logger.warn('NOTE: Runway videos require monitoring at https://app.runwayml.com/queue');
    errorHandler.saveCheckpoint('phase6-runway', { cost: videoCost });
    return true;

  } catch (error) {
    logger.warn('Phase 6 warning (optional)', error);
    // Don't fail pipeline if Runway optional
    return false;
  }
}

/**
 * Phase 7A: Assemble video with FFmpeg (FREE, LOCAL)
 */
async function phase7AssembleFFmpeg() {
  logger.stage('PHASE 7A: ASSEMBLE VIDEO (FFmpeg - FREE)');

  try {
    // Check FFmpeg
    if (!videoAssembler.checkFFmpeg()) {
      throw new Error('FFmpeg not installed - install with: apt-get install ffmpeg');
    }

    // Create simple image sequence
    const imageDir = './output/generated_images';
    if (!fs.existsSync(imageDir)) {
      logger.warn('No images found - skipping assembly');
      return false;
    }

    // Get images
    const images = fs.readdirSync(imageDir)
      .filter(f => f.endsWith('.png'))
      .sort()
      .map(f => ({
        path: path.join(imageDir, f),
        duration: 5, // 5 seconds per image
      }));

    logger.info(`Found ${images.length} images for assembly`);

    // Assemble
    const narrationFile = './output/narration.mp3';
    if (!fs.existsSync(narrationFile)) {
      throw new Error('Narration MP3 not found');
    }

    const result = await videoAssembler.assembleVideo(
      images,
      narrationFile,
      null,
      './output/final_video.mp4'
    );

    logger.success(`Phase 7A complete: Video assembled with FFmpeg (${result.sizeMB} MB)`);
    errorHandler.saveCheckpoint('phase7a-assembled-ffmpeg', { result });
    return true;

  } catch (error) {
    logger.error('Phase 7A failed', error);
    throw error;
  }
}

/**
 * Phase 7B: Assemble video with Descript API (HIGHER QUALITY, PAID)
 */
async function phase7AssembleDescript() {
  logger.stage('PHASE 7B: ASSEMBLE VIDEO (Descript API - PAID)');

  try {
    if (!process.env.DESCRIPT_API_KEY) {
      throw new Error('DESCRIPT_API_KEY not found in .env');
    }

    const descriptEditor = new DescriptVideoEditor();

    // Get narration file
    const narrationFile = './output/narration.mp3';
    if (!fs.existsSync(narrationFile)) {
      throw new Error('Narration MP3 not found');
    }

    // Create project name from timestamp
    const projectName = `VideoGen_${new Date().toISOString().slice(0, 10).replace(/-/g, '')}`;

    logger.info(`Creating Descript project: ${projectName}`);

    // Run full Descript workflow
    const result = await descriptEditor.fullWorkflow(narrationFile, projectName);

    if (!result) {
      throw new Error('Descript workflow failed');
    }

    // Cost estimation (Descript pay-as-you-go: ~$10-20 per video depending on length)
    const descriptCost = 15.0;
    costTracker.addCall('descript', 'video-export', descriptCost, { projectId: result.projectId });

    logger.success(`Phase 7B complete: Video queued in Descript ($${descriptCost.toFixed(2)})`);
    logger.info(`Project ID: ${result.projectId}`);
    logger.info(`Download URL will be available in Descript dashboard`);
    logger.info(`Expected output: ${result.exportResult.outputPath}`);

    errorHandler.saveCheckpoint('phase7b-assembled-descript', { result });
    return result;

  } catch (error) {
    logger.error('Phase 7B failed', error);
    throw error;
  }
}

/**
 * Phase 7C: Assemble video with Shotstack (CLOUD, FAST, CHEAP)
 */
async function phase7AssembleShotstack() {
  logger.stage('PHASE 7C: ASSEMBLE VIDEO (Shotstack - CLOUD)');

  try {
    if (!process.env.SHOTSTACK_SANDBOX_API_KEY && !process.env.SHOTSTACK_API_KEY) {
      throw new Error('SHOTSTACK_API_KEY not found in .env');
    }

    const assembler = new ShotstackAssembler(logger, true); // Use sandbox for free testing

    // Get images
    const imageDir = './output/generated_images';
    if (!fs.existsSync(imageDir)) {
      throw new Error('No images found');
    }

    const images = fs.readdirSync(imageDir)
      .filter(f => f.endsWith('.png'))
      .sort()
      .map(f => ({
        path: path.join(imageDir, f),
        duration: 5, // 5 seconds per image
      }));

    if (images.length === 0) {
      throw new Error('No PNG images found');
    }

    logger.info(`Found ${images.length} images for assembly`);

    // Get narration
    const narrationFile = './output/narration.mp3';
    if (!fs.existsSync(narrationFile)) {
      throw new Error('Narration MP3 not found');
    }

    // Assemble with Shotstack
    const result = await assembler.assembleVideo(
      images,
      narrationFile,
      './output/final_video.mp4'
    );

    const shotCost = parseFloat(result.cost);
    costTracker.addCall('shotstack', 'render', shotCost, { images: images.length });

    logger.success(`Phase 7C complete: Video rendered (${result.sizeMB} MB, $${result.cost})`);
    logger.info(`Task ID: ${result.taskId}`);

    errorHandler.saveCheckpoint('phase7c-assembled-shotstack', { result });
    return result;

  } catch (error) {
    logger.error('Phase 7C failed', error);
    throw error;
  }
}

/**
 * Phase 7: Assemble video (choose FFmpeg, Descript, or Shotstack)
 */
async function phase7Assemble(assemblyMethod = 'ffmpeg') {
  if (assemblyMethod === 'descript') {
    return await phase7AssembleDescript();
  } else if (assemblyMethod === 'shotstack') {
    return await phase7AssembleShotstack();
  } else {
    return await phase7AssembleFFmpeg();
  }
}

/**
 * Phase 8: Upload to YouTube
 */
async function phase8YouTube() {
  logger.stage('PHASE 8: YOUTUBE UPLOAD');

  try {
    const videoFile = './output/final_video.mp4';
    if (!fs.existsSync(videoFile)) {
      logger.warn('Final video not found - skipping YouTube upload');
      return false;
    }

    const cmd = `python upload_to_youtube.py --video "${videoFile}"`;
    logger.info(`Would execute: ${cmd}`);
    logger.warn('YouTube upload requires OAuth credentials - manual step for now');

    errorHandler.saveCheckpoint('phase8-youtube-ready', { videoFile });
    return true;

  } catch (error) {
    logger.error('Phase 8 warning', error);
    return false;
  }
}

/**
 * Main orchestration
 */
async function main() {
  const startTime = Date.now();

  try {
    // Parse arguments
    const args = process.argv.slice(2);
    const url = args[0] || DEFAULT_URL;

    let assemblyMethod = 'ffmpeg';
    if (args.includes('--use-descript')) {
      assemblyMethod = 'descript';
    } else if (args.includes('--use-shotstack')) {
      assemblyMethod = 'shotstack';
    }

    logger.info(`\n${'='.repeat(70)}`);
    logger.info('VideoGen YouTube - Complete Automated Pipeline');
    logger.info(`URL: ${url}`);
    logger.info(
      `Assembly Method: ${
        assemblyMethod === 'shotstack'
          ? 'Shotstack (cloud, fast, $0.12/min in production, free sandbox)'
          : assemblyMethod === 'descript'
          ? 'Descript API (higher quality, $15/video, auto-captions)'
          : 'FFmpeg (free, local, no captions)'
      }`
    );
    logger.info(`${'='.repeat(70)}\n`);

    // Run phases
    await phase1Scrape(url);
    await phase2Clean();
    const prompts = await phase3Script();
    await phase4Images(prompts);
    await phase5Narration();
    await phase6Videos();

    // Assembly requires manual Runway download for now
    logger.warn('\n⚠️  MANUAL STEP: Download Runway videos from https://app.runwayml.com/queue');
    logger.warn('   Then re-run with appropriate assembly method:\n');
    logger.warn('   FFmpeg (free):        node pipeline-complete.js --assemble');
    logger.warn('   Descript (paid):      node pipeline-complete.js --assemble --use-descript');
    logger.warn('   Shotstack (fast):     node pipeline-complete.js --assemble --use-shotstack\n');

    await phase7Assemble(assemblyMethod);
    await phase8YouTube();

    // Final report
    const duration = Date.now() - startTime;
    const durationMin = (duration / 1000 / 60).toFixed(1);

    logger.stage('PIPELINE COMPLETE');
    logger.summary({
      total_duration: `${durationMin} minutes`,
      total_cost: costTracker.getTotal().toFixed(2),
      cost_breakdown: costTracker.getByService(),
      output: './output/final_video.mp4',
      next_step: 'Upload to YouTube or review in editor',
    });

    logger.info(`\nLog file: ${logger.getLogFile()}`);

  } catch (error) {
    logger.error('PIPELINE FAILED', error);
    logger.info(`\nLog file: ${logger.getLogFile()}`);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main().catch(err => {
    logger.error('Fatal error', err);
    process.exit(1);
  });
}

module.exports = {
  main,
  phase1Scrape,
  phase2Clean,
  phase3Script,
  phase4Images,
  phase5Narration,
  phase6Videos,
  phase7Assemble,
  phase7AssembleFFmpeg,
  phase7AssembleDescript,
  phase7AssembleShotstack,
  phase8YouTube
};
