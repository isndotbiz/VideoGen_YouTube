#!/usr/bin/env node
/**
 * Embed SRT Subtitles into MP4 Video
 * Requires FFmpeg
 * Usage: node embed-subtitles.js [video-file] [subtitle-file] [output-file]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
require('dotenv').config();

const Logger = require('./lib/logger');

const logger = new Logger('./logs');

function checkFFmpeg() {
  try {
    execSync('ffmpeg -version', { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

async function embedSubtitles(videoPath, subtitlePath, outputPath) {
  try {
    if (!fs.existsSync(videoPath)) {
      throw new Error(`Video file not found: ${videoPath}`);
    }

    if (!fs.existsSync(subtitlePath)) {
      throw new Error(`Subtitle file not found: ${subtitlePath}`);
    }

    if (!checkFFmpeg()) {
      throw new Error('FFmpeg not found. Install with: choco install ffmpeg (Windows)');
    }

    logger.stage('EMBEDDING SUBTITLES INTO VIDEO');
    logger.info(`Video:    ${videoPath}`);
    logger.info(`Subtitles: ${subtitlePath}`);
    logger.info(`Output:   ${outputPath}\n`);

    logger.info('Running FFmpeg...');

    // FFmpeg command to embed subtitles
    const cmd = `ffmpeg -i "${videoPath}" -i "${subtitlePath}" -c:v copy -c:a copy -c:s mov_text "${outputPath}"`;

    execSync(cmd, { stdio: 'inherit' });

    // Check output
    if (!fs.existsSync(outputPath)) {
      throw new Error('Output file not created');
    }

    const stats = fs.statSync(outputPath);
    const sizeMB = (stats.size / 1024 / 1024).toFixed(2);

    logger.success(`✓ Subtitles embedded!`);
    logger.info(`Output: ${outputPath}`);
    logger.info(`Size: ${sizeMB} MB\n`);

    logger.info('Video is ready for YouTube upload with hardcoded subtitles!');

    return {
      outputPath,
      sizeMB,
    };
  } catch (error) {
    logger.error('Failed to embed subtitles', error);
    throw error;
  }
}

async function main() {
  const args = process.argv.slice(2);
  const videoFile = args[0] || './output/final_video.mp4';
  const subtitleFile = args[1] || './output/subtitles.srt';
  const outputFile = args[2] || './output/final_video_with_subs.mp4';

  logger.info('\n' + '='.repeat(70));
  logger.info('Embed Subtitles into Video');
  logger.info('='.repeat(70) + '\n');

  try {
    await embedSubtitles(videoFile, subtitleFile, outputFile);
  } catch (error) {
    logger.error('Fatal error', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(err => {
    logger.error('Fatal error', err);
    process.exit(1);
  });
}

module.exports = { embedSubtitles, checkFFmpeg };
