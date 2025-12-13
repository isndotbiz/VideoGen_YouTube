#!/usr/bin/env node
/**
 * Test Shotstack Assembly
 * Compare with FFmpeg and Descript
 */

const fs = require('fs');
const path = require('path');
require('dotenv').config();

const Logger = require('./lib/logger');
const ShotstackAssembler = require('./lib/shotstack-assembler');

const logger = new Logger('./logs');

async function testShotstack() {
  logger.stage('TESTING SHOTSTACK ASSEMBLY');

  try {
    // Check for images
    const imageDir = './output/generated_images';
    if (!fs.existsSync(imageDir)) {
      logger.error('Image directory not found');
      return false;
    }

    const images = fs.readdirSync(imageDir)
      .filter(f => f.endsWith('.png'))
      .slice(0, 5) // Use first 5 images
      .map(f => ({
        path: path.join(imageDir, f),
        duration: 5,
      }));

    if (images.length === 0) {
      logger.error('No PNG images found');
      return false;
    }

    logger.info(`Found ${images.length} images`);

    // Check for narration
    const narrationFile = './output/narration.mp3';
    if (!fs.existsSync(narrationFile)) {
      logger.error('Narration file not found');
      return false;
    }

    logger.info(`Using narration: ${narrationFile}`);

    // Create assembler
    const assembler = new ShotstackAssembler(logger, true); // Use sandbox

    // Test assembly
    const startTime = Date.now();

    logger.info('Submitting to Shotstack...');
    const result = await assembler.assembleVideo(
      images,
      narrationFile,
      './output/test_shotstack_output.mp4'
    );

    const duration = Date.now() - startTime;

    logger.success(`✓ Shotstack assembly complete!`);
    logger.info(`Output: ${result.outputPath}`);
    logger.info(`Size: ${result.sizeMB} MB`);
    logger.info(`Duration: ${(duration / 1000 / 60).toFixed(1)} min`);
    logger.info(`Cost: ${result.cost} (sandbox = free testing)`);
    logger.info(`Task ID: ${result.taskId}`);

    return true;
  } catch (error) {
    logger.error('Shotstack test failed', error);
    return false;
  }
}

logger.info('\n' + '='.repeat(70));
logger.info('SHOTSTACK VIDEO ASSEMBLY TEST');
logger.info('Testing cloud-based video rendering');
logger.info('='.repeat(70) + '\n');

testShotstack()
  .then(success => {
    if (success) {
      logger.info(
        `
✓ Shotstack is working!

ASSEMBLY METHOD COMPARISON:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method          Speed     Cost          Captions  Quality   Notes
─────────────────────────────────────────────────────────────────
FFmpeg          Fast      Free          No        Good      Requires install
Descript        Medium    ~$15/video    Yes       Excellent Auto-captions
Shotstack       Fast      ~$0.12/min    No        Excellent Cloud-based
(Sandbox)       Testing   FREE          -         Professional Testing

RECOMMENDATION FOR YOUR USE CASE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use Shotstack if you want:
✅ Cloud-based rendering (no local FFmpeg needed)
✅ Professional quality video output
✅ Fast processing (parallel)
✅ Cost-effective (~$0.12/minute in production)
✅ Sandbox for free testing during development

Cost for 5-minute video:
  - Shotstack Sandbox: FREE (for testing)
  - Shotstack Production: ~$0.60 (5 min × $0.12/min)
  - Descript: ~$15
  - FFmpeg: Free (but requires installation)

NEXT STEPS:
1. Use Shotstack Sandbox while testing (FREE)
   node pipeline-complete.js "url" --use-shotstack

2. Switch to Production when ready (add to .env)
   Change ShotstackAssembler(logger, false) for production API

3. Full pipeline with Shotstack:
   node batch-video-generator.js topics.json --use-shotstack
`
      );
    }
    process.exit(success ? 0 : 1);
  })
  .catch(err => {
    logger.error('Fatal error', err);
    process.exit(1);
  });
