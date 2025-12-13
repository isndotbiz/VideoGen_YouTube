#!/usr/bin/env node
/**
 * Generate Subtitles with AssemblyAI
 * Usage: node generate-subtitles-assemblyai.js [audio-file] [output-file]
 */

const fs = require('fs');
const path = require('path');
require('dotenv').config();

const Logger = require('./lib/logger');
const AssemblyAISubtitler = require('./lib/assemblyai-subtitler');

const logger = new Logger('./logs');

async function main() {
  const args = process.argv.slice(2);
  const audioFile = args[0] || './output/narration.mp3';
  const outputFile = args[1] || './output/subtitles.srt';

  logger.info('\n' + '='.repeat(70));
  logger.info('AssemblyAI Subtitle Generator');
  logger.info('='.repeat(70) + '\n');

  try {
    if (!fs.existsSync(audioFile)) {
      throw new Error(`Audio file not found: ${audioFile}`);
    }

    logger.info(`Input:  ${audioFile}`);
    logger.info(`Output: ${outputFile}\n`);

    // Create subtitler
    const subtitler = new AssemblyAISubtitler(logger);

    // Generate subtitles
    const result = await subtitler.generateSubtitles(audioFile, outputFile);

    logger.stage('SUBTITLE GENERATION COMPLETE');
    logger.info(`\n✓ Generated ${result.lines} subtitle lines`);
    logger.info(`✓ Duration: ${result.duration} minutes`);
    logger.info(`✓ Cost: $${result.cost}`);
    logger.info(`✓ Confidence: ${(result.confidence * 100).toFixed(1)}%`);
    logger.info(`\n✓ Saved to: ${outputFile}\n`);

    // Show first few lines
    const srtContent = fs.readFileSync(outputFile, 'utf8');
    const lines = srtContent.split('\n').slice(0, 10);

    logger.info('First few subtitle lines:');
    logger.info(lines.join('\n'));

    logger.info('\n✅ Ready to embed into video with FFmpeg:\n');
    logger.info(`ffmpeg -i output/final_video.mp4 -i ${outputFile} \\`);
    logger.info(`  -c:v copy -c:a copy -c:s mov_text \\`);
    logger.info(`  output/final_video_with_subs.mp4`);

  } catch (error) {
    logger.error('Failed to generate subtitles', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(err => {
    logger.error('Fatal error', err);
    process.exit(1);
  });
}

module.exports = { main };
