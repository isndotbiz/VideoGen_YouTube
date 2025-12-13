#!/usr/bin/env node
/**
 * Batch Video Generator
 * Generate multiple YouTube videos in parallel from a list of URLs
 * Usage: node batch-video-generator.js topics.json --use-descript
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
require('dotenv').config();

const Logger = require('./lib/logger');
const logger = new Logger('./logs');

/**
 * Default topics with high-SEO AI comparison angles
 */
const DEFAULT_TOPICS = [
  {
    id: 'claude-vs-chatgpt',
    title: 'Claude vs ChatGPT: Which AI Should You Use?',
    url: 'https://zapier.com/blog/claude-vs-chatgpt/',
    tags: ['AI', 'Claude', 'ChatGPT', 'Comparison'],
    duration: '4-5 min',
  },
  {
    id: 'claude-vs-gemini',
    title: 'Claude vs Google Gemini: The AI Showdown',
    url: 'https://www.analyticsvidhya.com/blog/2024/claude-vs-gemini/',
    tags: ['AI', 'Claude', 'Gemini', 'Google'],
    duration: '4-5 min',
  },
  {
    id: 'claude-coding-guide',
    title: 'Claude for Coding: The Developer\'s AI Sidekick',
    url: 'https://www.descope.com/blog/post/claude-vs-chatgpt',
    tags: ['AI', 'Claude', 'Coding', 'Developers'],
    duration: '5-6 min',
  },
  {
    id: 'free-ai-tools',
    title: 'Free AI Tools That Beat Paid Plans in 2024',
    url: 'https://www.appypieautomate.ai/blog/free-ai-tools-that-work-better-than-paid',
    tags: ['AI', 'Free', 'Tools', 'Budget'],
    duration: '5-6 min',
  },
  {
    id: 'chatgpt-beginners',
    title: 'ChatGPT for Beginners: A Complete Guide',
    url: 'https://zapier.com/blog/how-to-use-chatgpt/',
    tags: ['ChatGPT', 'Tutorial', 'Beginners', 'Guide'],
    duration: '6-7 min',
  },
];

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const config = {
    topicsFile: args[0] || null,
    useDescript: args.includes('--use-descript'),
    parallel: !args.includes('--sequential'),
    parallelCount: parseInt(args.find(a => a.startsWith('--parallel='))?.split('=')[1]) || 2,
    skipImages: args.includes('--skip-images'),
    dryRun: args.includes('--dry-run'),
  };
  return config;
}

/**
 * Load topics from file or use defaults
 */
function loadTopics(topicsFile) {
  if (topicsFile && fs.existsSync(topicsFile)) {
    logger.info(`Loading topics from: ${topicsFile}`);
    const content = fs.readFileSync(topicsFile, 'utf8');
    return JSON.parse(content);
  }
  logger.info('Using default topics');
  return DEFAULT_TOPICS;
}

/**
 * Generate video for a single topic
 */
async function generateVideo(topic, config) {
  const startTime = Date.now();
  logger.stage(`TOPIC: ${topic.title}`);
  logger.info(`URL: ${topic.url}`);
  logger.info(`Duration: ${topic.duration}`);

  try {
    // Build command
    const descriptFlag = config.useDescript ? '--use-descript' : '';
    const cmd = `node pipeline-complete.js "${topic.url}" ${descriptFlag}`.trim();

    if (config.dryRun) {
      logger.info(`[DRY RUN] Would execute: ${cmd}`);
      return {
        status: 'dry-run',
        duration: 0,
        topic: topic.id,
      };
    }

    logger.info(`Executing pipeline...`);
    execSync(cmd, { stdio: 'inherit' });

    const duration = Date.now() - startTime;
    logger.success(`✓ Generated: ${topic.id} (${(duration / 1000 / 60).toFixed(1)} min)`);

    return {
      status: 'success',
      duration,
      topic: topic.id,
      title: topic.title,
    };
  } catch (error) {
    logger.error(`Failed to generate: ${topic.id}`, error);
    return {
      status: 'failed',
      error: error.message,
      topic: topic.id,
      title: topic.title,
    };
  }
}

/**
 * Run videos sequentially
 */
async function runSequential(topics, config) {
  logger.info(`\nRunning ${topics.length} videos SEQUENTIALLY\n`);

  const results = [];
  for (const topic of topics) {
    const result = await generateVideo(topic, config);
    results.push(result);
  }
  return results;
}

/**
 * Run videos in parallel with concurrency limit
 */
async function runParallel(topics, config) {
  const parallelCount = config.parallelCount;
  logger.info(`\nRunning ${topics.length} videos in PARALLEL (${parallelCount} at a time)\n`);

  const results = [];
  for (let i = 0; i < topics.length; i += parallelCount) {
    const batch = topics.slice(i, i + parallelCount);
    logger.info(`Batch ${Math.floor(i / parallelCount) + 1}: Processing ${batch.length} videos...`);

    const batchResults = await Promise.all(
      batch.map(topic => generateVideo(topic, config))
    );
    results.push(...batchResults);
  }
  return results;
}

/**
 * Generate library summary
 */
function generateSummary(results, config) {
  const successful = results.filter(r => r.status === 'success').length;
  const failed = results.filter(r => r.status === 'failed').length;
  const dryRuns = results.filter(r => r.status === 'dry-run').length;

  const totalDuration = results.reduce((sum, r) => sum + (r.duration || 0), 0);

  logger.stage('BATCH PROCESSING COMPLETE');
  logger.summary({
    total_requested: results.length,
    successful,
    failed,
    dry_runs: dryRuns,
    total_duration: `${(totalDuration / 1000 / 60).toFixed(1)} minutes`,
    assembly_method: config.useDescript ? 'Descript (with captions)' : 'FFmpeg (no captions)',
    parallel_mode: config.parallel ? `Yes (${config.parallelCount} at a time)` : 'No (sequential)',
  });

  // Results table
  logger.info('\n📊 RESULTS:\n');
  results.forEach((result, idx) => {
    const icon = result.status === 'success' ? '✅' : result.status === 'dry-run' ? '📝' : '❌';
    logger.info(
      `${icon} ${idx + 1}. ${result.title || result.topic}: ${result.status}${
        result.duration ? ` (${(result.duration / 1000 / 60).toFixed(1)} min)` : ''
      }`
    );
  });

  // Save results to file
  const resultsFile = `./logs/batch-results-${new Date().toISOString().slice(0, 10)}.json`;
  fs.writeFileSync(resultsFile, JSON.stringify(results, null, 2));
  logger.info(`\n📁 Results saved to: ${resultsFile}`);

  return {
    successful,
    failed,
    dryRuns,
    totalDuration,
  };
}

/**
 * Main
 */
async function main() {
  const config = parseArgs();
  const topics = loadTopics(config.topicsFile);

  logger.info('\n' + '='.repeat(70));
  logger.info('BATCH VIDEO GENERATOR - SEO Content Library Builder');
  logger.info('='.repeat(70));
  logger.info(`Videos to generate: ${topics.length}`);
  logger.info(`Assembly method: ${config.useDescript ? 'Descript (captions)' : 'FFmpeg (no captions)'}`);
  logger.info(`Execution mode: ${config.parallel ? 'Parallel' : 'Sequential'}`);
  logger.info(`Dry run: ${config.dryRun ? 'Yes' : 'No'}`);
  logger.info('='.repeat(70) + '\n');

  try {
    // Run videos
    const results = config.parallel
      ? await runParallel(topics, config)
      : await runSequential(topics, config);

    // Generate summary
    generateSummary(results, config);

    logger.info('\n✅ BATCH COMPLETE\n');

  } catch (error) {
    logger.error('BATCH FAILED', error);
    process.exit(1);
  }
}

// Export for testing
module.exports = {
  DEFAULT_TOPICS,
  generateVideo,
  runSequential,
  runParallel,
  generateSummary,
};

if (require.main === module) {
  main().catch(err => {
    logger.error('Fatal error', err);
    process.exit(1);
  });
}
