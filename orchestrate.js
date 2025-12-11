#!/usr/bin/env node

/**
 * COMPLETE PIPELINE ORCHESTRATOR
 *
 * Automates:
 * 1. Scrape with Firecrawl
 * 2. Save JSON
 * 3. Convert to JSONL
 * 4. Clean JSONL
 * 5. Generate video script
 *
 * Usage:
 *   node orchestrate.js <URL>
 *   node orchestrate.js https://example.com/article
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const DEFAULT_URL = 'https://www.nathanonn.com/claude-code-vs-codex-why-i-use-both-and-you-should-too/';

function log(message, emoji = '•') {
  console.log(`${emoji} ${message}`);
}

function section(title) {
  console.log(`\n${'═'.repeat(60)}`);
  console.log(`   ${title}`);
  console.log(`${'═'.repeat(60)}\n`);
}

function runCommand(cmd, description) {
  try {
    log(`Running: ${description}`, '⚙️');
    const output = execSync(cmd, { encoding: 'utf8', stdio: 'pipe' });
    log(`Complete: ${description}`, '✅');
    return { success: true, output };
  } catch (error) {
    log(`Failed: ${description}`, '❌');
    console.error(error.message);
    return { success: false, error };
  }
}

async function main() {
  const url = process.argv[2] || DEFAULT_URL;

  console.log(`
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        FIRECRAWL → JSONL → VIDEO SCRIPT PIPELINE          ║
║                                                            ║
║  Complete Automation: Scrape → Clean → Generate Scripts   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
  `);

  section('PIPELINE CONFIGURATION');
  log(`URL: ${url}`, '📍');
  log(`Start time: ${new Date().toLocaleString()}`, '🕐');

  section('STEP 1: SCRAPE & CONVERT TO JSONL');
  let result1 = runCommand(
    `node scrape-and-convert.js "${url}"`,
    'Firecrawl scrape + JSON/JSONL conversion'
  );

  if (!result1.success) {
    log('Pipeline stopped at Step 1', '⛔');
    process.exit(1);
  }

  section('STEP 2: CLEAN JSONL FOR AI');
  let result2 = runCommand(
    `node clean-jsonl.js dataset.jsonl`,
    'JSONL cleaning and validation'
  );

  if (!result2.success) {
    log('Continuing despite cleaning issues...', '⚠️');
  }

  section('STEP 3: GENERATE VIDEO PRODUCTION MATERIALS');
  let result3 = runCommand(
    `node generate-video-script.js`,
    'Video script, storyboard, and production guide generation'
  );

  if (!result3.success) {
    log('Video generation had issues, check output', '⚠️');
  }

  section('PIPELINE COMPLETE');

  // Summary
  const files = fs.readdirSync('.')
    .filter(f => {
      const ext = path.extname(f);
      return ext === '.jsonl' || ext === '.json' || ext === '.md';
    })
    .sort();

  log('Generated files:', '📦');
  files.forEach(file => {
    const size = fs.statSync(file).size;
    const sizeKb = (size / 1024).toFixed(1);
    console.log(`   ✓ ${file} (${sizeKb} KB)`);
  });

  console.log(`
╔════════════════════════════════════════════════════════════╗
║                     WHAT'S NEXT?                          ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║ 1. REVIEW VIDEO MATERIALS                                ║
║    └─ Open: COMPLETE_VIDEO_SCRIPT.md                      ║
║                                                            ║
║ 2. RECORD NARRATION                                       ║
║    └─ Use: video-narration.md as your script             ║
║    └─ Tools: Audacity, Adobe Premiere, or similar        ║
║                                                            ║
║ 3. CREATE VISUAL SLIDES                                  ║
║    └─ Use: slide-deck.md in Figma, Canva, or PPT        ║
║    └─ Include: Graphs from video-graphs.md               ║
║                                                            ║
║ 4. GENERATE AI VIDEO                                      ║
║    └─ Tools: Pika Labs, Runway Gen-2, or Luma AI        ║
║    └─ Input: Storyboard + narration + slide images       ║
║                                                            ║
║ 5. FINAL EDITING                                          ║
║    └─ Use: video-editing-guide.md for transitions        ║
║    └─ Tools: DaVinci Resolve, Adobe Premiere             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

📊 PIPELINE STATISTICS
─────────────────────────────────────────────────────────────
  Total files generated: ${files.length}
  Completion time: ${new Date().toLocaleString()}
  Status: READY FOR VIDEO PRODUCTION

🎬 QUICK REFERENCE
─────────────────────────────────────────────────────────────
  Master script:     COMPLETE_VIDEO_SCRIPT.md
  Narration:         video-narration.md
  Storyboard:        video-storyboard.md
  Visual slides:     slide-deck.md
  Graphs/diagrams:   video-graphs.md
  Editing guide:     video-editing-guide.md
  Raw data:          dataset.jsonl
  Validation:        clean-report.json

✨ Pipeline complete! Your video production materials are ready.
  `);

}

main().catch(err => {
  console.error('Pipeline error:', err);
  process.exit(1);
});
