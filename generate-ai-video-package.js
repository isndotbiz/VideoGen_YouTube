#!/usr/bin/env node

/**
 * AI VIDEO GENERATION PACKAGE BUILDER
 *
 * Creates:
 * - Narration script with timing markers
 * - SVG charts/diagrams
 * - Visual cue guide (where to show each chart)
 * - Upload instructions for AI video tools
 *
 * Usage: node generate-ai-video-package.js
 */

const fs = require('fs');
const path = require('path');

function createNarrationWithMarkers() {
  return `# NARRATION SCRIPT WITH VISUAL MARKERS

## TIMING: ~17 minutes total
## Format: [TIME] - [VISUAL CUE] - [NARRATION]

---

[00:00] - [FADE IN: Title Card]
"Hey everyone! Have you ever wondered: should I use Claude Code or Codex?"

[00:05] - [SHOW DIAGRAM: Question Mark]
"You're probably asking the wrong question."

[00:10] - [SHOW DIAGRAM: VS Indicator]
"Because after extensive testing, I discovered something game-changing:"

[00:15] - [SHOW DIAGRAM: Team Icon]
"They're not competitors... they're the perfect team."

---

[00:30] - [SHOW DIAGRAM: Features 1]
"Claude Code builds brilliantly,"

[00:35] - [SHOW DIAGRAM: Features 2]
"Codex reviews meticulously,"

[00:40] - [SHOW DIAGRAM: Integration Arrow]
"and together they create bulletproof code."

---

[01:00] - [SHOW CHART: Codex Solo Results]
"Here's the problem when you use Codex alone:"

[01:10] - [HIGHLIGHT: Minimal, Basic]
"You get minimal code. Sure, it works technically, but..."

[01:20] - [SHOW COMPARISON: Codex Weak Points]
"No edge case handling. Missing quality features. Requires enhancement."

[01:35] - [TRANSITION: Arrow Right]
"It's like asking for a house and getting a tent."

---

[02:00] - [SHOW CHART: Claude Code Solo Results]
"Now look at Claude Code alone:"

[02:10] - [HIGHLIGHT: Over-Engineering]
"You get over-engineering. Ask for simple, get spacecraft."

[02:25] - [SHOW COMPLEXITY GRAPH: Going Up]
"Abstract factories for simple functions. Unnecessary design patterns."

[02:40] - [SHOW COMPARISON: Claude Code Weak Points]
"20 files when 3 would suffice. Complexity that breeds bugs."

---

[03:15] - [SHOW DIAGRAM: The Solution]
"Here's the breakthrough:"

[03:25] - [SHOW WORKFLOW: Build → Review]
"Use Claude Code to BUILD,"

[03:30] - [ARROW ANIMATION: Pass to Codex]
"then Codex to REVIEW."

[03:40] - [SHOW STRENGTHS TABLE]
"Claude Code brings creative problem-solving and comprehensive implementations."

[03:55] - [SHOW STRENGTHS TABLE: Codex Column]
"Codex brings security detection and consistency checking."

---

[04:30] - [SHOW DIAGRAM: Real World Example]
"Let me show you a real example from my WordPress theme:"

[04:45] - [SHOW TASK: Newsletter Subscription]
"The task: Add a newsletter subscription shortcode with guide."

[05:00] - [SHOW PHASE 1: Claude Code]
"Phase 1: Claude Code builds the feature"

[05:15] - [ANIMATE: Code appearing]
"It creates: shortcode, guide tab, 6 visual styles, documentation."

[05:30] - [SHOW RESULT BOX: Initial Implementation]
"Complete. Comprehensive. Ready to go... or so it seemed."

---

[06:00] - [SHOW PHASE 2: Codex Review]
"Phase 2: Codex reviews the implementation"

[06:15] - [ANIMATE: Magnifying glass]
"Codex goes into detective mode, analyzing everything."

[06:30] - [SHOW ISSUE #1: Security]
"Issue #1: Security gap - missing nonce protection"

[06:45] - [SHOW ISSUE #2: Integration]
"Issue #2: Shortcode posts to wrong endpoint"

[07:00] - [SHOW ISSUE #3: Documentation]
"Issue #3: Documentation doesn't match actual code"

[07:15] - [SHOW ISSUE #4: UI]
"Issue #4: Stray character in footer - wrong icon"

---

[07:45] - [SHOW PHASE 3: Apply Fixes]
"Phase 3: Apply the fixes"

[08:00] - [ANIMATE: Code changing]
"Codex applies each improvement methodically."

[08:15] - [SHOW BEFORE/AFTER: Security]
"Before: No nonce. After: Full nonce + honeypot protection"

[08:30] - [SHOW BEFORE/AFTER: Integration]
"Before: Wrong endpoint. After: Proper AJAX/REST integration"

[08:45] - [SHOW BEFORE/AFTER: Documentation]
"Before: Misleading. After: Accurate and complete"

[09:00] - [SHOW BEFORE/AFTER: Icons]
"Before: Broken. After: Clean proper icons"

---

[09:30] - [SHOW FINAL RESULT]
"The final implementation: bulletproof."

[09:45] - [HIGHLIGHT BENEFITS]
"Secure. Consistent. Correct. Documented."

[10:00] - [SHOW CHECKLIST: All items checked]
"Everything works. Everything is clean."

---

[10:30] - [SHOW WORKFLOW DIAGRAM: Complete Process]
"Here's the exact workflow anyone can use:"

[10:45] - [SHOW STEP 1]
"Step 1: Build with Claude Code. Let it do what it does best."

[11:00] - [SHOW STEP 2]
"Step 2: Export a git diff or code summary."

[11:15] - [SHOW STEP 3]
"Step 3: Review with Codex. Find the issues."

[11:30] - [SHOW STEP 4: Two Paths]
"Step 4: Apply fixes. Either ask Claude Code or Codex to fix it."

[11:45] - [SHOW DECISION POINT]
"Both work. Choose based on which has more context."

---

[12:15] - [SHOW STRENGTHS CHART]
"Why does this work so well?"

[12:30] - [SHOW COLUMN 1: Claude Code]
"Claude Code: Creative. Comprehensive. Context-aware. Rapid."

[12:45] - [SHOW COLUMN 2: Codex]
"Codex: Meticulous. Security-focused. Consistency-checking. Detail-oriented."

[13:00] - [SHOW COMBINED: Integration]
"Together: Unstoppable."

---

[13:30] - [SHOW PRO TIPS SECTION]
"Pro tips for maximum effectiveness:"

[13:45] - [SHOW TIP 1: Explorer]
"Tip 1: Let Claude Code explore first - it understands context."

[14:00] - [SHOW TIP 2: Specific]
"Tip 2: Be specific with Codex - tell it what to check."

[14:15] - [SHOW TIP 3: Screenshots]
"Tip 3: Include screenshots - visual proof helps."

[14:30] - [SHOW TIP 4: Always Review]
"Tip 4: Never skip the review - small issues compound."

[14:45] - [SHOW TIP 5: Tight Loop]
"Tip 5: Keep the feedback loop tight - apply fixes immediately."

---

[15:15] - [SHOW CONCLUSION SLIDE]
"Stop asking: Claude Code or Codex?"

[15:30] - [SHOW ANSWER]
"Start asking: How do I use them together?"

[15:45] - [SHOW RESULT]
"Not competitors. Collaborators."

[16:00] - [SHOW FINAL MESSAGE]
"Your next feature deserves both the creativity of Claude Code"

[16:10] - [SHOW FINAL MESSAGE 2]
"AND the precision of Codex."

[16:20] - [SHOW CTA]
"Why settle for less?"

---

[16:30] - [SHOW SUBSCRIBE CARD]
"Get weekly insights like this - join The Art of Vibe Coding newsletter."

[16:45] - [SHOW SOCIAL LINKS]
"Find me on GitHub and LinkedIn."

[17:00] - [FADE OUT: Credits]
"Thanks for watching. See you next week!"

---

## VISUAL CUE REFERENCE

See: AI_VIDEO_VISUAL_GUIDE.md for exact chart specifications
`;
}

function createVisualGuide() {
  return `# AI VIDEO VISUAL GUIDE

This shows exactly what visuals appear when in the video.

## CHARTS TO CREATE

### Chart 1: Question Mark Icon
- **Time:** 00:05
- **Duration:** 3 seconds
- **Style:** Large question mark, minimal design
- **Colors:** Blue/Purple gradient background
- **File:** chart_01_question.svg

### Chart 2: VS Indicator
- **Time:** 00:10
- **Duration:** 2 seconds
- **Style:** "CLAUDE CODE vs CODEX" split screen
- **Colors:** Left (Claude - Blue), Right (Codex - Orange), VS (Bold)
- **File:** chart_02_vs.svg

### Chart 3: Team Icon
- **Time:** 00:15
- **Duration:** 3 seconds
- **Style:** Two circles connecting = symbol, showing integration
- **Colors:** Blue + Orange connecting in middle
- **File:** chart_03_team.svg

### Chart 4: Features Comparison - Feature 1
- **Time:** 00:30
- **Duration:** 3 seconds
- **Style:** "Claude Code Builds Brilliantly" with icon
- **Colors:** Blue theme, construction/building icon
- **File:** chart_04_feature1.svg

### Chart 5: Features Comparison - Feature 2
- **Time:** 00:35
- **Duration:** 3 seconds
- **Style:** "Codex Reviews Meticulously" with icon
- **Colors:** Orange theme, magnifying glass icon
- **File:** chart_05_feature2.svg

### Chart 6: Integration Arrow
- **Time:** 00:40
- **Duration:** 3 seconds
- **Style:** Animated arrow connecting both features
- **Colors:** Gradient blue to orange
- **File:** chart_06_integration.svg

### Chart 7: Codex Solo - Minimal Results
- **Time:** 01:00
- **Duration:** 5 seconds
- **Style:** Bar chart showing "Minimal, Basic, Limited"
- **Colors:** Orange (Codex color), low bars
- **Content:**
  - Feature Completeness: 30%
  - Edge Cases Handled: 20%
  - Quality of Life: 25%
- **File:** chart_07_codex_solo.svg

### Chart 8: Codex Weaknesses
- **Time:** 01:20
- **Duration:** 4 seconds
- **Style:** List of problems with X marks
- **Colors:** Red X marks on white background
- **Content:**
  - ✗ No edge case handling
  - ✗ Missing quality features
  - ✗ Requires enhancement
  - ✗ Minimalist approach
- **File:** chart_08_codex_weak.svg

### Chart 9: Claude Code Solo - Over-Engineering Results
- **Time:** 02:00
- **Duration:** 5 seconds
- **Style:** Bar chart showing high/over-engineered results
- **Colors:** Blue (Claude color), high bars
- **Content:**
  - Complexity: 95%
  - Files Created: 90%
  - Design Patterns: 85%
  - Features Added: 100%
- **File:** chart_09_claude_solo.svg

### Chart 10: Claude Code Weaknesses
- **Time:** 02:25
- **Duration:** 4 seconds
- **Style:** List of problems with X marks
- **Colors:** Red X marks on white background
- **Content:**
  - ✗ Abstract factories for simple tasks
  - ✗ Unnecessary design patterns
  - ✗ Too many files created
  - ✗ Complexity breeds bugs
- **File:** chart_10_claude_weak.svg

### Chart 11: Complexity Graph
- **Time:** 02:25
- **Duration:** 3 seconds
- **Style:** Line graph going up exponentially
- **Colors:** Blue line, red warning zone
- **Axes:** Complexity (Y) vs Scope (X)
- **File:** chart_11_complexity.svg

### Chart 12: The Solution - Build & Review
- **Time:** 03:15
- **Duration:** 4 seconds
- **Style:** Process flow: Claude Code → [Arrow] → Codex
- **Colors:** Blue (Claude) → Arrow → Orange (Codex)
- **Icons:** Hammer/wrench for build, magnifying glass for review
- **File:** chart_12_solution.svg

### Chart 13: Strengths Comparison Table
- **Time:** 03:40
- **Duration:** 6 seconds
- **Style:** Two-column table
- **Colors:** Blue column (Claude), Orange column (Codex)
- **Content:**
  | Claude Code | Codex |
  |---|---|
  | Creative problem-solving | Security detection |
  | Comprehensive implementations | Consistency checking |
  | Deep context understanding | Attention to detail |
  | Rapid development | Edge case identification |
- **File:** chart_13_strengths.svg

### Chart 14: Real World Example - Task
- **Time:** 04:45
- **Duration:** 4 seconds
- **Style:** Document icon with task description
- **Colors:** Green highlight on white background
- **Content:** "Newsletter Subscription Shortcode + Guide Tab"
- **File:** chart_14_task.svg

### Chart 15: Phase 1 - Claude Code Results
- **Time:** 05:15
- **Duration:** 5 seconds
- **Style:** Checklist with all items checked
- **Colors:** Green checkmarks
- **Content:**
  - ✓ Newsletter subscribe form shortcode
  - ✓ Guide tab added to Theme Options
  - ✓ 6 visual styles included
  - ✓ Comprehensive documentation
  - ✓ FluentCRM integration features
- **File:** chart_15_phase1.svg

### Chart 16: Phase 2 - Issues Found
- **Time:** 06:30
- **Duration:** 8 seconds
- **Style:** 4 boxes, each showing an issue
- **Colors:** Red background, white text
- **Content:**
  | Issue #1 | Issue #2 | Issue #3 | Issue #4 |
  |---|---|---|---|
  | Security Gap | Integration Issue | Documentation Mismatch | UI Details |
  | Missing nonce | Wrong endpoint | Incorrect examples | Stray character |
- **File:** chart_16_issues.svg

### Chart 17: Before/After - Security
- **Time:** 08:15
- **Duration:** 4 seconds
- **Style:** Two boxes side by side
- **Colors:** Red (Before), Green (After)
- **Content:**
  - Before: ✗ No nonce protection
  - After: ✓ Full nonce + honeypot
- **File:** chart_17_before_after_security.svg

### Chart 18: Before/After - Integration
- **Time:** 08:30
- **Duration:** 4 seconds
- **Style:** Two boxes side by side
- **Colors:** Red (Before), Green (After)
- **Content:**
  - Before: ✗ Posts to wrong endpoint
  - After: ✓ Proper AJAX/REST integration
- **File:** chart_18_before_after_integration.svg

### Chart 19: Before/After - Documentation
- **Time:** 08:45
- **Duration:** 4 seconds
- **Style:** Two boxes side by side
- **Colors:** Red (Before), Green (After)
- **Content:**
  - Before: ✗ Misleading documentation
  - After: ✓ Accurate complete docs
- **File:** chart_19_before_after_docs.svg

### Chart 20: Before/After - UI
- **Time:** 09:00
- **Duration:** 4 seconds
- **Style:** Two boxes side by side
- **Colors:** Red (Before), Green (After)
- **Content:**
  - Before: ✗ Broken icons
  - After: ✓ Clean proper icons
- **File:** chart_20_before_after_ui.svg

### Chart 21: Final Result Checklist
- **Time:** 09:45
- **Duration:** 5 seconds
- **Style:** Comprehensive checklist
- **Colors:** All green checkmarks
- **Content:**
  - ✓ Full security with nonce + honeypot
  - ✓ Proper AJAX/REST integration
  - ✓ Consistent styling across contexts
  - ✓ Accurate documentation
  - ✓ Clean UI with proper icons
  - ✓ Hidden context field for fallback
- **File:** chart_21_final.svg

### Chart 22: Workflow Steps
- **Time:** 10:45
- **Duration:** 8 seconds
- **Style:** 4-step process flow
- **Colors:** Alternating blue and orange
- **Content:**
  1. Build with Claude Code
  2. Export code/diff
  3. Review with Codex
  4. Apply fixes
- **File:** chart_22_workflow.svg

### Chart 23: Strengths Chart
- **Time:** 12:30
- **Duration:** 6 seconds
- **Style:** Two columns with feature lists
- **Colors:** Blue (left), Orange (right)
- **Content:** Claude Code strengths vs Codex strengths
- **File:** chart_23_strengths_detail.svg

### Chart 24: Pro Tips List
- **Time:** 13:45
- **Duration:** 10 seconds (5 tips × 2 sec each)
- **Style:** Numbered list with icons
- **Colors:** White background, blue numbers
- **Content:**
  1. Let Claude Code explore first
  2. Be specific with Codex
  3. Include screenshots
  4. Never skip review
  5. Keep feedback loop tight
- **File:** chart_24_tips.svg

### Chart 25: Conclusion - Collaborators
- **Time:** 15:45
- **Duration:** 5 seconds
- **Style:** Two connected circles (team/collaboration)
- **Colors:** Blue and Orange, connected with heart/link symbol
- **Content:** "Not Competitors. Collaborators."
- **File:** chart_25_conclusion.svg

---

## COLORS TO USE

**Claude Code Theme (Blue):** #3B82F6 or #0066FF
**Codex Theme (Orange):** #F97316 or #FF8C00
**Accent (Green):** #10B981
**Error (Red):** #EF4444
**Background:** #FFFFFF or #F9FAFB

---

## TRANSITION RECOMMENDATIONS

- Between sections: Fade 0.5 seconds
- Chart appears: 0.3 second zoom-in
- Chart disappears: 0.3 second fade-out
- Text highlight: Pulse/glow effect

---

## EXPORT RECOMMENDATIONS FOR AI VIDEO TOOLS

1. **Pika Labs / Runway:** Export as PNG (1920x1080)
2. **Luma AI:** Can handle 4K but PNG/MP4 both work
3. **D-ID:** PNG works best for avatar videos

Save all charts as individual PNG files in 1920x1080 resolution.
`;
}

function createSVGCharts() {
  const charts = {
    'chart_01_question.svg': `<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#grad1)"/>
  <circle cx="960" cy="540" r="300" fill="white" opacity="0.1"/>
  <text x="960" y="680" font-size="400" font-weight="bold" text-anchor="middle" fill="white" font-family="Arial">?</text>
  <text x="960" y="900" font-size="60" text-anchor="middle" fill="white" font-family="Arial">Which one should I choose?</text>
</svg>`,

    'chart_02_vs.svg': `<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1920" height="1080" fill="#F9FAFB"/>
  <!-- Left side: Claude Code -->
  <rect x="100" y="200" width="700" height="680" rx="20" fill="#3B82F6" opacity="0.1" stroke="#3B82F6" stroke-width="3"/>
  <text x="450" y="500" font-size="80" font-weight="bold" text-anchor="middle" fill="#3B82F6" font-family="Arial">Claude</text>
  <text x="450" y="600" font-size="80" font-weight="bold" text-anchor="middle" fill="#3B82F6" font-family="Arial">Code</text>
  <!-- Center: VS -->
  <circle cx="960" cy="540" r="100" fill="white" stroke="#000" stroke-width="3"/>
  <text x="960" y="600" font-size="80" font-weight="bold" text-anchor="middle" fill="#000" font-family="Arial">VS</text>
  <!-- Right side: Codex -->
  <rect x="1120" y="200" width="700" height="680" rx="20" fill="#F97316" opacity="0.1" stroke="#F97316" stroke-width="3"/>
  <text x="1470" y="500" font-size="80" font-weight="bold" text-anchor="middle" fill="#F97316" font-family="Arial">Codex</text>
  <text x="1470" y="600" font-size="80" font-weight="bold" text-anchor="middle" fill="#F97316" font-family="Arial">(GPT-5)</text>
</svg>`,

    'chart_03_team.svg': `<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1920" height="1080" fill="#F9FAFB"/>
  <!-- Left circle -->
  <circle cx="600" cy="540" r="150" fill="#3B82F6"/>
  <text x="600" y="560" font-size="40" font-weight="bold" text-anchor="middle" fill="white" font-family="Arial">Claude</text>
  <!-- Right circle -->
  <circle cx="1320" cy="540" r="150" fill="#F97316"/>
  <text x="1320" y="560" font-size="40" font-weight="bold" text-anchor="middle" fill="white" font-family="Arial">Codex</text>
  <!-- Connecting line -->
  <line x1="750" y1="540" x2="1170" y2="540" stroke="#10B981" stroke-width="8"/>
  <!-- Center symbol -->
  <circle cx="960" cy="540" r="60" fill="white" stroke="#10B981" stroke-width="4"/>
  <text x="960" y="570" font-size="80" font-weight="bold" text-anchor="middle" fill="#10B981" font-family="Arial">=</text>
  <!-- Top text -->
  <text x="960" y="150" font-size="80" font-weight="bold" text-anchor="middle" fill="#000" font-family="Arial">Perfect Team</text>
</svg>`,

    'chart_04_feature1.svg': `<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1920" height="1080" fill="#F9FAFB"/>
  <rect x="300" y="300" width="1320" height="500" rx="20" fill="#3B82F6" opacity="0.1" stroke="#3B82F6" stroke-width="3"/>
  <text x="960" y="700" font-size="100" font-weight="bold" text-anchor="middle" fill="#3B82F6" font-family="Arial">Builds Brilliantly</text>
  <text x="960" y="850" font-size="60" text-anchor="middle" fill="#666" font-family="Arial">Creates comprehensive, creative implementations</text>
</svg>`,

    'chart_05_feature2.svg': `<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1920" height="1080" fill="#F9FAFB"/>
  <rect x="300" y="300" width="1320" height="500" rx="20" fill="#F97316" opacity="0.1" stroke="#F97316" stroke-width="3"/>
  <text x="960" y="700" font-size="100" font-weight="bold" text-anchor="middle" fill="#F97316" font-family="Arial">Reviews Meticulously</text>
  <text x="960" y="850" font-size="60" text-anchor="middle" fill="#666" font-family="Arial">Finds issues and ensures quality</text>
</svg>`,

    'chart_06_integration.svg': `<svg viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="arrowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#F97316;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1920" height="1080" fill="#F9FAFB"/>
  <line x1="200" y1="540" x2="1720" y2="540" stroke="url(#arrowGrad)" stroke-width="20"/>
  <!-- Arrow head -->
  <polygon points="1720,540 1600,480 1600,600" fill="url(#arrowGrad)"/>
  <text x="960" y="750" font-size="80" font-weight="bold" text-anchor="middle" fill="#000" font-family="Arial">Together = Bulletproof Code</text>
</svg>`,
  };

  return charts;
}

function createPikaLabsGuide() {
  return `# AI VIDEO GENERATION GUIDE
## Using Pika Labs, Runway, or Luma AI

---

## OPTION 1: PIKA LABS (Recommended - Fastest & Easiest)

### What You'll Need
- Narration MP3 (from video-narration.md)
- Chart PNG files (generated from SVG files)
- Free account at https://pika.art

### Step-by-Step Process

**Step 1: Create Project**
1. Go to https://pika.art
2. Sign up (free account includes credits)
3. Click "New Project"
4. Name it: "Claude Code vs Codex"

**Step 2: Set Up Timeline**
1. Click "Create video"
2. Select "Duration: 17 minutes" OR "Custom: 1020 seconds"
3. Frame rate: 30 fps
4. Resolution: 1920x1080

**Step 3: Upload Your Assets**
1. Upload all PNG chart files (chart_01 through chart_25)
2. Upload narration.mp3
3. Tag each image with timing (00:05, 00:10, etc.)

**Step 4: Create Scenes**

For each scene:
- Select chart image
- Set duration (from VIDEO NARRATION WITH MARKERS)
- Add audio segment (copy from narration)
- Add transition (fade recommended)

**Example Scene 1:**
- Image: chart_01_question.png
- Duration: 5 seconds (00:00 to 00:05)
- Audio: "Hey everyone! Have you ever wondered about Claude Code or Codex?"
- Transition: Fade in

**Example Scene 2:**
- Image: chart_02_vs.png
- Duration: 5 seconds (00:05 to 00:10)
- Audio: "You're probably asking the wrong question."
- Transition: Fade

(Continue for all 25 charts...)

**Step 5: Add Narration**
1. Upload video-narration.mp3 as full background audio
2. Sync with chart transitions
3. Adjust volume (narration: 100%, background music: 50%)

**Step 6: Add Transitions**
- Between each scene: Fade (0.5 seconds)
- Duration: Check timing in visual guide

**Step 7: Generate**
1. Click "Generate Video"
2. Wait 5-10 minutes
3. Download as MP4 (1920x1080)

**Step 8: Download & Edit**
1. Download as video.mp4
2. (Optional) Import into DaVinci Resolve for final polish
3. Upload to YouTube

### Timeline Example for Pika Labs

\`\`\`
00:00-00:05: chart_01_question.png + narration "Hey everyone..."
00:05-00:10: chart_02_vs.png + narration "You're asking..."
00:10-00:15: chart_03_team.png + narration "They're not competitors..."
00:15-00:30: [continue pattern...]
...
17:00: End
\`\`\`

---

## OPTION 2: RUNWAY GEN-2 (More Control)

### Advantages
- Better control over transitions
- Multiple generation models
- Better for complex animations

### Process

**Step 1: Prepare Assets**
- Export all charts as PNG (1920x1080)
- Prepare narration.mp3
- Create a shot list (see next section)

**Step 2: Upload to Runway**
1. Go to https://app.runwayml.com
2. Create new project
3. Upload images and audio

**Step 3: Create Storyboard**
For each chart image:
- Add text prompt: "Professional chart showing [description], fade transition"
- Duration: 3-5 seconds
- Add previous image: Link to next chart

**Step 4: Generate**
1. Select "Gen-2" model
2. Click generate for each transition
3. Takes 2-3 minutes per transition

**Step 5: Compile**
1. Use Runway's timeline editor
2. Import all generated clips
3. Add narration track
4. Export as final video

---

## OPTION 3: LUMA AI (Most Cinematic)

### Advantages
- Best visual quality
- Realistic transitions
- Most cinematic results

### Process

**Step 1: Prepare**
- Same chart assets as Pika
- Narration ready

**Step 2: Upload**
1. Go to https://lumalabs.ai
2. Create project
3. Upload images

**Step 3: Configure**
- Set video style: "Professional presentation"
- Quality: 4K (optional)
- Duration: Match your narration timing

**Step 4: Generate**
- Takes longer (10-15 min) but results are cinematic
- Download as 4K MP4

**Step 5: Edit**
- Optional: Import into DaVinci Resolve
- Add narration (overlay audio)
- Export and upload

---

## QUICK COMPARISON

| Feature | Pika Labs | Runway | Luma AI |
|---------|-----------|--------|---------|
| Speed | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐ Medium | ⭐⭐ Slow |
| Ease | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐ Medium | ⭐⭐⭐ Medium |
| Quality | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best |
| Control | ⭐⭐⭐ Basic | ⭐⭐⭐⭐ Advanced | ⭐⭐⭐ Good |
| Cost | Free tier | Free tier | Free tier |
| **Recommendation** | ✅ Best for beginners | For advanced users | For premium quality |

---

## RECOMMENDED WORKFLOW

### Fastest (30 minutes total)
1. Export all SVG → PNG (1920x1080)
2. Use Pika Labs
3. Upload images + narration
4. Let AI generate video
5. Download & upload to YouTube

### Best Quality (45 minutes total)
1. Create charts in Pika Labs
2. Generate video
3. Download
4. Import into DaVinci Resolve
5. Add background music
6. Final color grading
7. Export & upload

### Most Control (60+ minutes)
1. Generate with Runway Gen-2
2. Have fine-tune control over each transition
3. Compile in Runway
4. Export
5. Edit in DaVinci Resolve
6. Upload

---

## PRO TIPS

### For Pika Labs
- Keep narration clear and loud (normalize audio first)
- Chart images should have high contrast
- Use solid backgrounds (avoid busy patterns)
- Test with 2-3 scenes first before doing all 25

### For Runway
- Write detailed prompts for each transition
- Use same camera angle throughout
- Reference images help (show "before" and "after")
- Generate one transition at a time to monitor quality

### For Luma AI
- Cinematic style works best
- Wait for full generation (don't interrupt)
- 4K export is worth the wait
- Can upscale from lower resolution if needed

---

## COMMON ISSUES & FIXES

**"Video looks jerky"**
→ Increase number of frames between charts (add 1-2 second pauses)

**"Narration doesn't sync"**
→ Check timing in NARRATION_WITH_MARKERS.md
→ Manually adjust audio track position

**"Charts look pixelated"**
→ Ensure PNG files are 1920x1080 minimum
→ Regenerate from SVG at higher resolution

**"Audio is too quiet"**
→ Normalize audio in Audacity before uploading
→ Increase narration track volume to 100%

**"Transitions feel abrupt"**
→ Add fade effect (0.5-1 second) between scenes
→ Slow down chart change timing

---

## FINAL STEP: UPLOAD TO YOUTUBE

Once you have your final video.mp4:

1. **Title:** "Claude Code vs Codex: Why I Use Both (And You Should Too)"

2. **Description:**
\`\`\`
Watch the full article: [Your Article URL]

In this video, I show you why Claude Code and Codex aren't competitors—they're collaborators.

Learn:
- Why using just one limits you
- How to use them together for bulletproof code
- A real-world example from my WordPress theme
- The exact workflow I use for every feature

Timestamps:
00:00 - Intro
01:00 - The Problem with Codex Alone
02:00 - The Problem with Claude Code Alone
03:15 - The Solution: Using Both
04:30 - Real World Example
09:30 - Final Results
10:30 - The Workflow
13:30 - Pro Tips
15:15 - Conclusion

Resources:
- Original Article: [Your Article URL]
- Newsletter: The Art of Vibe Coding
- GitHub: [Your GitHub]
- LinkedIn: [Your LinkedIn]

#ClaudeCode #Codex #AI #Development
\`\`\`

3. **Tags:**
   - claude-code
   - codex
   - gpt-5
   - ai-development
   - code-review
   - programming
   - ai-tools

4. **Thumbnail:**
   - Use chart_02_vs.png (Claude Code vs Codex)
   - Add text: "Both, Not Either"
   - Add arrow pointing to "Watch Now"

5. **Category:** Education / How-To

6. **Visibility:** Public

Done! Your video is live.
`;
}

async function main() {
  console.log('═══════════════════════════════════════════════════');
  console.log('   AI Video Generation Package Builder');
  console.log('═══════════════════════════════════════════════════\n');

  try {
    // 1. Create narration with markers
    const narration = createNarrationWithMarkers();
    fs.writeFileSync('AI_VIDEO_NARRATION_WITH_MARKERS.md', narration);
    console.log('✅ Saved: AI_VIDEO_NARRATION_WITH_MARKERS.md');

    // 2. Create visual guide
    const visual = createVisualGuide();
    fs.writeFileSync('AI_VIDEO_VISUAL_GUIDE.md', visual);
    console.log('✅ Saved: AI_VIDEO_VISUAL_GUIDE.md');

    // 3. Create SVG charts
    const charts = createSVGCharts();
    Object.entries(charts).forEach(([name, content]) => {
      fs.writeFileSync(name, content);
    });
    console.log(`✅ Saved: ${Object.keys(charts).length} SVG chart templates`);

    // 4. Create Pika Labs guide
    const pikaGuide = createPikaLabsGuide();
    fs.writeFileSync('PIKA_LABS_GUIDE.md', pikaGuide);
    console.log('✅ Saved: PIKA_LABS_GUIDE.md');

    console.log('\n═══════════════════════════════════════════════════');
    console.log('   AI Video Package Complete!');
    console.log('═══════════════════════════════════════════════════\n');

    console.log('📦 Generated Files:');
    console.log('   1. AI_VIDEO_NARRATION_WITH_MARKERS.md');
    console.log('      → Narration script with exact timing markers');
    console.log('');
    console.log('   2. AI_VIDEO_VISUAL_GUIDE.md');
    console.log('      → Exact specs for all 25 charts');
    console.log('');
    console.log('   3. SVG Chart Templates (6 samples)');
    console.log('      → Ready to use in design tools');
    console.log('');
    console.log('   4. PIKA_LABS_GUIDE.md');
    console.log('      → Step-by-step instructions for AI video generation');
    console.log('');

    console.log('🎯 NEXT STEPS:');
    console.log('');
    console.log('STEP 1: Create your charts (2 options)');
    console.log('   Option A: Use AI to generate charts');
    console.log('   Option B: Create in Figma/Canva using specs');
    console.log('');
    console.log('STEP 2: Export charts as PNG (1920x1080)');
    console.log('');
    console.log('STEP 3: Record narration from AI_VIDEO_NARRATION_WITH_MARKERS.md');
    console.log('   (or use TTS: Google TTS, ElevenLabs, Natural Reader)');
    console.log('');
    console.log('STEP 4: Follow PIKA_LABS_GUIDE.md to generate video');
    console.log('');
    console.log('STEP 5: Upload to YouTube');
    console.log('');

    console.log('📊 CHART SPECIFICATIONS:');
    console.log('   - 25 total charts (10 SVG templates included)');
    console.log('   - All charts: 1920x1080 PNG');
    console.log('   - Colors: Blue (#3B82F6), Orange (#F97316)');
    console.log('   - Duration: ~17 minutes total video');
    console.log('');

    console.log('💡 FASTEST OPTION:');
    console.log('   1. Use the 6 SVG samples as templates');
    console.log('   2. Duplicate & customize for remaining charts');
    console.log('   3. Export all as PNG at 1920x1080');
    console.log('   4. Upload to Pika Labs (5 min setup)');
    console.log('   5. Let AI generate video (10 min wait)');
    console.log('   6. Download & upload to YouTube');
    console.log('   Total time: ~30 minutes');
    console.log('');

    console.log('🎬 Your video is ready to create!');

  } catch (error) {
    console.error('❌ Failed:', error.message);
    process.exit(1);
  }
}

main();
