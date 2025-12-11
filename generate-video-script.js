#!/usr/bin/env node

/**
 * PART 5: Generate Video Script from JSONL
 *
 * Creates:
 * - Full video script with narration
 * - Storyboard with visual markers
 * - Timing and section markers
 * - B-roll suggestions
 * - ASCII diagrams/graphs
 *
 * Usage:
 *   node generate-video-script.js
 */

const fs = require('fs');
const path = require('path');

function loadJsonl(filename = 'dataset.jsonl') {
  if (!fs.existsSync(filename)) {
    throw new Error(`JSONL file not found: ${filename}`);
  }
  const line = fs.readFileSync(filename, 'utf8').trim().split('\n')[0];
  return JSON.parse(line);
}

function generateStoryboard(data) {
  const title = data.title || 'Video Content';
  const sections = data.sections || [];
  const contentLength = data.content?.length || 0;

  // Estimate video duration: ~150 chars per 10 seconds
  const estimatedSeconds = Math.ceil(contentLength / 150) * 10;
  const estimatedMinutes = Math.ceil(estimatedSeconds / 60);

  let storyboard = `# STORYBOARD: ${title}\n\n`;
  storyboard += `**Estimated Duration:** ${estimatedMinutes} minutes\n`;
  storyboard += `**Content Volume:** ${contentLength} characters, ${sections.length} major sections\n\n`;

  storyboard += `## Scene Breakdown\n\n`;

  let cumulativeTime = 0;
  const sceneLength = estimatedSeconds / Math.max(sections.length + 2, 3); // +2 for intro/outro

  // Intro scene
  storyboard += `### SCENE 1: INTRO (0:00 - 0:${Math.ceil(sceneLength / 60)})\n`;
  storyboard += `**Visual:** Title card with animated text\n`;
  storyboard += `**Content:** Hook + problem statement\n`;
  storyboard += `**B-Roll:** Background tech animations, logo reveal\n`;
  storyboard += `**Narration Duration:** 30-45 seconds\n\n`;

  cumulativeTime = sceneLength;

  // Content scenes
  sections.slice(0, 5).forEach((section, idx) => {
    const sceneNum = idx + 2;
    const startMin = Math.floor(cumulativeTime / 60);
    const startSec = Math.round(cumulativeTime % 60);
    cumulativeTime += sceneLength;
    const endMin = Math.floor(cumulativeTime / 60);
    const endSec = Math.round(cumulativeTime % 60);

    const sectionTitle = section.heading || section.title || `Point ${idx + 1}`;
    storyboard += `### SCENE ${sceneNum}: ${sectionTitle.toUpperCase()} (${startMin}:${String(startSec).padStart(2, '0')} - ${endMin}:${String(endSec).padStart(2, '0')})\n`;
    storyboard += `**Visual:** ${generateVisualSuggestion(sectionTitle, idx)}\n`;
    storyboard += `**Content:** Key points and explanations\n`;
    storyboard += `**B-Roll:** Relevant animations, code examples, demos\n`;
    storyboard += `**Narration Duration:** ${Math.round(sceneLength / 60)}-${Math.round(sceneLength / 50)} seconds\n\n`;
  });

  // Outro scene
  const outroStart = Math.floor(cumulativeTime / 60);
  const outroStartSec = Math.round(cumulativeTime % 60);
  storyboard += `### SCENE ${Math.max(sections.length + 2, 5)}: OUTRO (${outroStart}:${String(outroStartSec).padStart(2, '0')} - ${estimatedMinutes}:00)\n`;
  storyboard += `**Visual:** Call-to-action card with social links\n`;
  storyboard += `**Content:** Summary + CTA\n`;
  storyboard += `**B-Roll:** Credits roll, subscribe prompt\n`;
  storyboard += `**Narration Duration:** 20-30 seconds\n\n`;

  return storyboard;
}

function generateVisualSuggestion(title, index) {
  const suggestions = [
    'Split screen comparison',
    'Animated diagram with arrows',
    'Code syntax highlighting',
    'Live demo walkthrough',
    'Infographic with numbers',
    'Before/after transition',
    'Feature showcase',
    'Timeline visualization'
  ];
  return suggestions[index % suggestions.length];
}

function generateNarration(data) {
  const title = data.title || 'Content';
  const description = data.description || 'Check this out!';

  let narration = `# VIDEO NARRATION SCRIPT\n\n`;

  narration += `## INTRO (30-45 seconds)\n`;
  narration += `"Hey everyone! Have you ever wondered about ${title}? \n`;
  narration += `Today we're diving deep into this topic to show you exactly what you need to know. \n`;
  narration += `Stick around!"\n\n`;

  narration += `---\n\n`;

  // Main content narration
  narration += `## MAIN CONTENT\n\n`;
  narration += `[Reference the article/document content here]\n\n`;
  narration += `"So here's the thing: [KEY POINT 1]. This matters because [EXPLANATION]. \n`;
  narration += `Let me show you exactly how this works..."\n\n`;

  narration += `"Moving on to [KEY POINT 2]. Notice how [OBSERVATION]. \n`;
  narration += `This is important for [CONSEQUENCE]."\n\n`;

  narration += `---\n\n`;

  narration += `## OUTRO (20-30 seconds)\n`;
  narration += `"That's what you need to know about ${title}. \n`;
  narration += `If you found this helpful, smash that like button and subscribe for more content like this. \n`;
  narration += `What do you think? Drop a comment below. Thanks for watching!"\n\n`;

  return narration;
}

function generateGraphs(data) {
  let graphs = `# VISUAL GRAPHS & DIAGRAMS\n\n`;

  graphs += `## Diagram 1: Content Structure Map\n`;
  graphs += `\`\`\`\n`;
  graphs += `┌─────────────────────────────────────┐\n`;
  graphs += `│         ${(data.title || 'Topic').toUpperCase()}        │\n`;
  graphs += `└────────────────┬────────────────────┘\n`;
  graphs += `         │\n`;
  graphs += `   ┌─────┼─────┐\n`;
  graphs += `   │     │     │\n`;
  graphs += `  KEY   KEY   KEY\n`;
  graphs += `  PT 1  PT 2  PT 3\n`;
  graphs += `   │     │     │\n`;
  graphs += `   └─────┼─────┘\n`;
  graphs += `         │\n`;
  graphs += `    CONCLUSION\n`;
  graphs += `\`\`\`\n\n`;

  graphs += `## Diagram 2: Timeline\n`;
  graphs += `\`\`\`\n`;
  graphs += `START ─────> INTRO ─────> CONTENT ─────> RECAP ─────> END\n`;
  graphs += ` 0:00        0:30         1:00          ${Math.ceil((data.content?.length || 1000) / 150)}:00        ${Math.ceil((data.content?.length || 1000) / 150)}:30\n`;
  graphs += `\`\`\`\n\n`;

  graphs += `## Diagram 3: Engagement Points\n`;
  graphs += `\`\`\`\n`;
  graphs += `ENGAGEMENT\n`;
  graphs += `    ▲\n`;
  graphs += `    │        ╱╲        ╱╲\n`;
  graphs += `    │       ╱  ╲      ╱  ╲\n`;
  graphs += `    │      ╱    ╲    ╱    ╲\n`;
  graphs += `    │     ╱      ╲  ╱      ╲\n`;
  graphs += `    │────────────────────────→ TIME\n`;
  graphs += `    Hooks    Key Points  CTA\n`;
  graphs += `\`\`\`\n\n`;

  return graphs;
}

function generateEditingGuide(data) {
  let guide = `# VIDEO EDITING GUIDE\n\n`;

  guide += `## Timeline Markers\n`;
  guide += `- \`00:00\` - Start (include black screen/intro)\n`;
  guide += `- \`00:05\` - Logo reveal\n`;
  guide += `- \`00:30\` - Main content begins\n`;
  guide += `- \`${Math.ceil((data.content?.length || 1000) / 300)}:00\` - Wrap-up begins\n`;
  guide += `- \`${Math.ceil((data.content?.length || 1000) / 150)}:30\` - Credits roll\n\n`;

  guide += `## Transitions\n`;
  guide += `- Between sections: Use fade or subtle zoom\n`;
  guide += `- Key points: Use emphasis animations\n`;
  guide += `- B-roll switches: Cross-fade for smooth flow\n\n`;

  guide += `## Text Overlays\n`;
  guide += `- Chapter titles with slight delay\n`;
  guide += `- Key takeaways as bullet points\n`;
  guide += `- Time stamps for reference\n`;
  guide += `- Subscribe/like reminders at key moments\n\n`;

  guide += `## Audio\n`;
  guide += `- Background music: Royalty-free, 50% volume\n`;
  guide += `- Sound effects: Use sparingly for emphasis\n`;
  guide += `- Silence: 0.5s between major sections\n\n`;

  return guide;
}

function generateSlideOutlines(data) {
  const sections = data.sections || [];
  let slides = `# SLIDE DECK OUTLINE\n\n`;

  slides += `## Slide 1: Title\n`;
  slides += `- Title: ${data.title}\n`;
  slides += `- Subtitle: ${data.description || 'Key Insights'}\n`;
  slides += `- Background: Bold color or gradient\n\n`;

  sections.slice(0, 8).forEach((section, idx) => {
    const title = section.heading || section.title || `Point ${idx + 1}`;
    slides += `## Slide ${idx + 2}: ${title}\n`;
    slides += `- Main point: [Extract from content]\n`;
    slides += `- Sub-points: 2-3 bullet points\n`;
    slides += `- Visual: Diagram or photo\n`;
    slides += `- Transition: Fade\n\n`;
  });

  slides += `## Slide ${Math.max(sections.length + 2, 10)}: Summary\n`;
  slides += `- Key takeaways (3 main points)\n`;
  slides += `- Call-to-action\n`;
  slides += `- Contact/Social info\n\n`;

  return slides;
}

async function main() {
  console.log('═══════════════════════════════════════════════════');
  console.log('   Video Script Generator from JSONL');
  console.log('═══════════════════════════════════════════════════\n');

  try {
    const data = loadJsonl();
    console.log(`📖 Loaded: ${data.title}`);

    // Generate all components
    const storyboard = generateStoryboard(data);
    const narration = generateNarration(data);
    const graphs = generateGraphs(data);
    const editingGuide = generateEditingGuide(data);
    const slides = generateSlideOutlines(data);

    // Combine into master script
    let masterScript = `# COMPLETE VIDEO PRODUCTION SCRIPT\n`;
    masterScript += `## "${data.title}"\n`;
    masterScript += `**Generated:** ${new Date().toLocaleString()}\n`;
    masterScript += `**Source:** ${data.url}\n\n`;
    masterScript += `---\n\n`;
    masterScript += storyboard;
    masterScript += `---\n\n`;
    masterScript += narration;
    masterScript += `---\n\n`;
    masterScript += slides;
    masterScript += `---\n\n`;
    masterScript += graphs;
    masterScript += `---\n\n`;
    masterScript += editingGuide;

    // Save files
    const slug = data.id || 'video-script';

    fs.writeFileSync('video-storyboard.md', storyboard);
    console.log('✅ Saved: video-storyboard.md');

    fs.writeFileSync('video-narration.md', narration);
    console.log('✅ Saved: video-narration.md');

    fs.writeFileSync('video-graphs.md', graphs);
    console.log('✅ Saved: video-graphs.md');

    fs.writeFileSync('video-editing-guide.md', editingGuide);
    console.log('✅ Saved: video-editing-guide.md');

    fs.writeFileSync('slide-deck.md', slides);
    console.log('✅ Saved: slide-deck.md');

    fs.writeFileSync('COMPLETE_VIDEO_SCRIPT.md', masterScript);
    console.log('✅ Saved: COMPLETE_VIDEO_SCRIPT.md');

    console.log('\n═══════════════════════════════════════════════════');
    console.log('   Video Production Materials Ready');
    console.log('═══════════════════════════════════════════════════');
    console.log('\nGenerated files:');
    console.log('  1. COMPLETE_VIDEO_SCRIPT.md (master file)');
    console.log('  2. video-storyboard.md');
    console.log('  3. video-narration.md');
    console.log('  4. slide-deck.md');
    console.log('  5. video-graphs.md');
    console.log('  6. video-editing-guide.md');
    console.log('\nNext steps:');
    console.log('  • Review the storyboard');
    console.log('  • Record narration using video-narration.md');
    console.log('  • Use slide-deck.md to create visuals in design tool');
    console.log('  • Feed into AI video tools: Pika Labs, Runway, or Luma AI');

  } catch (error) {
    console.error('❌ Failed:', error.message);
    process.exit(1);
  }
}

main();
