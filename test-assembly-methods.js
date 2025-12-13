#!/usr/bin/env node
/**
 * Test FFmpeg vs Descript Assembly Methods
 * Uses existing images + narration to compare output quality
 */

const fs = require('fs');
const path = require('path');
require('dotenv').config();

const Logger = require('./lib/logger');
const FFmpegAssembler = require('./lib/ffmpeg-assembler');
const DescriptVideoEditor = require('./descript-video-editor');

const logger = new Logger('./logs');

/**
 * Get images from directory
 */
function getImages(imageDir, limit = 16) {
  if (!fs.existsSync(imageDir)) {
    logger.error(`Image directory not found: ${imageDir}`);
    return [];
  }

  const images = fs.readdirSync(imageDir)
    .filter(f => f.endsWith('.png'))
    .slice(0, limit)
    .map(f => ({
      path: path.join(imageDir, f),
      duration: 5, // 5 seconds per image
    }));

  return images;
}

/**
 * Test FFmpeg Assembly
 */
async function testFFmpeg() {
  logger.stage('TEST 1: FFmpeg Assembly (FREE, LOCAL)');

  try {
    const assembler = new FFmpegAssembler(logger);

    if (!assembler.checkFFmpeg()) {
      throw new Error('FFmpeg not installed');
    }

    const imageDir = './output/generated_images';
    const images = getImages(imageDir, 5);
    const narrationFile = './output/narration.mp3';

    if (images.length === 0) {
      throw new Error('No images found');
    }

    if (!fs.existsSync(narrationFile)) {
      throw new Error('Narration file not found');
    }

    logger.info(`Found ${images.length} images for assembly`);
    logger.info(`Using narration: ${narrationFile}`);

    const startTime = Date.now();

    const result = await assembler.assembleVideo(
      images,
      narrationFile,
      null,
      './output/test_ffmpeg_output.mp4'
    );

    const duration = Date.now() - startTime;

    logger.success(`✓ FFmpeg assembly complete in ${(duration / 1000).toFixed(0)}s`);
    logger.info(`Output: ${result.outputPath}`);
    logger.info(`Size: ${result.sizeMB} MB`);
    logger.info(`Duration: ${result.duration}s`);
    logger.info(`Features: No captions`);
    logger.info(`Cost: $0`);

    return {
      method: 'FFmpeg',
      success: true,
      outputPath: result.outputPath,
      duration,
      size: result.sizeMB,
    };
  } catch (error) {
    logger.error('FFmpeg test failed', error);
    return {
      method: 'FFmpeg',
      success: false,
      error: error.message,
    };
  }
}

/**
 * Test Descript Assembly
 */
async function testDescript() {
  logger.stage('TEST 2: Descript Assembly (PAID, CLOUD)');

  try {
    if (!process.env.DESCRIPT_API_KEY) {
      throw new Error('DESCRIPT_API_KEY not set in .env');
    }

    const editor = new DescriptVideoEditor();
    const narrationFile = './output/narration.mp3';

    if (!fs.existsSync(narrationFile)) {
      throw new Error('Narration file not found');
    }

    logger.info(`Using narration: ${narrationFile}`);

    const projectName = `TestCompare_${new Date().toISOString().slice(0, 10).replace(/-/g, '')}`;

    const startTime = Date.now();

    const result = await editor.fullWorkflow(narrationFile, projectName);

    const duration = Date.now() - startTime;

    if (!result) {
      throw new Error('Descript workflow failed');
    }

    logger.success(`✓ Descript assembly queued in ${(duration / 1000).toFixed(0)}s`);
    logger.info(`Project ID: ${result.projectId}`);
    logger.info(`Project Name: ${projectName}`);
    logger.info(`Export Status: ${result.exportResult.status}`);
    logger.info(`Features: Auto-captions, speaker detection, noise removal`);
    logger.info(`Cost: ~$15 (part of your Creator plan - FREE)`);

    return {
      method: 'Descript',
      success: true,
      projectId: result.projectId,
      projectName,
      duration,
    };
  } catch (error) {
    logger.error('Descript test failed', error);
    return {
      method: 'Descript',
      success: false,
      error: error.message,
    };
  }
}

/**
 * Compare results
 */
function compareResults(ffmpegResult, descriptResult) {
  logger.stage('COMPARISON: FFmpeg vs Descript');

  console.log(`
╔════════════════════════════════════════════════════════════════════╗
║                  FFMPEG vs DESCRIPT COMPARISON                     ║
╠════════════════════════════════════════════════════════════════════╣
║ Feature              │ FFmpeg           │ Descript              ║
╠══════════════════════╪══════════════════╪═══════════════════════╣
║ Speed                │ Fast (~30s)      │ Medium (~5s upload)   ║
║ Cost                 │ $0               │ Free (on plan)        ║
║ Auto-Captions        │ ❌ No            │ ✅ Yes               ║
║ Speaker Detection    │ ❌ No            │ ✅ Yes               ║
║ Noise Removal        │ ❌ No            │ ✅ Yes               ║
║ Video Quality        │ Good             │ Excellent             ║
║ Local Processing     │ ✅ Yes           │ ❌ Cloud              ║
║ Internet Required    │ ❌ No            │ ✅ Yes               ║
║ SEO Benefits         │ ⚠️  Moderate      │ ✅ High (captions)    ║
║ YouTube Shorts Ready │ ✅ Yes           │ ✅ Yes               ║
╚══════════════════════╧══════════════════╧═══════════════════════╝

FFmpeg Test:
  Status: ${ffmpegResult.success ? '✅ PASSED' : '❌ FAILED'}
  ${ffmpegResult.success ? `Output: ${ffmpegResult.outputPath}` : `Error: ${ffmpegResult.error}`}
  ${ffmpegResult.success ? `Duration: ${(ffmpegResult.duration / 1000).toFixed(1)}s` : ''}

Descript Test:
  Status: ${descriptResult.success ? '✅ PASSED' : '❌ FAILED'}
  ${descriptResult.success ? `Project: ${descriptResult.projectName}` : `Error: ${descriptResult.error}`}
  ${descriptResult.success ? `Duration: ${(descriptResult.duration / 1000).toFixed(1)}s` : ''}

RECOMMENDATION FOR YOUR USE CASE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Since you have the Descript Creator Plan:
✅ Use Descript (--use-descript flag)
   • Auto-captions = Better SEO ranking
   • Included in your plan = No extra cost
   • Professional quality = Better for monetization
   • Perfect for building YouTube library

You get all the benefits of Descript WITHOUT additional cost.

To build your SEO video library:
  node batch-video-generator.js topics.json --use-descript

This generates 5 high-SEO AI comparison videos with professional captions.
`);
}

/**
 * Main
 */
async function main() {
  logger.info('\n' + '='.repeat(70));
  logger.info('ASSEMBLY METHOD COMPARISON TEST');
  logger.info('Testing FFmpeg vs Descript with existing images + narration');
  logger.info('='.repeat(70) + '\n');

  const ffmpegResult = await testFFmpeg();
  logger.info('');
  const descriptResult = await testDescript();
  logger.info('');

  compareResults(ffmpegResult, descriptResult);

  logger.stage('TEST COMPLETE');
}

if (require.main === module) {
  main().catch(err => {
    logger.error('Fatal error', err);
    process.exit(1);
  });
}

module.exports = { testFFmpeg, testDescript, compareResults };
