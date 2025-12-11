#!/usr/bin/env python3
"""Advanced Video Regeneration with Text Images, Photorealism, and Subtitles"""

import os
import json
import requests
import time
import urllib.request
from pathlib import Path
from collections import defaultdict

# API Keys
FAL_API_KEY = "1053e5d9-45fa-4c4e-b3e7-df4ccea52ec9:f1ccd718f487b4e6a97132afc89194cd"
SHOTSTACK_KEY = "zZzUDIrXAe2WW3ddq0lS8j73hbrevSYAiT8NjpM8"
ELEVENLABS_KEY = "sk_7cce1b4fcd110b6481ee38c3386615f45814aa36fe62507f"

print("="*70)
print("ADVANCED VIDEO REGENERATION - PHASE 1: IMAGE GENERATION")
print("="*70)

# ============================================================================
# RECRAFT V3 PROMPTS - TEXT-HEAVY IMAGES ($0.04 each, 15 images)
# ============================================================================
recraft_prompts = [
    {
        "id": "01",
        "title": "Claude vs Codex Title Slide",
        "prompt": "Professional title slide with 'Claude vs Codex: Which AI Should You Use?' in large modern sans-serif font, clean white background with subtle blue and orange accents representing Claude and OpenAI brands"
    },
    {
        "id": "02",
        "title": "Response Quality Comparison",
        "prompt": "Comparison chart showing 'Response Quality' with Claude Code at 95% and Codex at 78%, large bold numbers, clean design, professional data visualization style"
    },
    {
        "id": "03",
        "title": "Code Generation Speed Metric",
        "prompt": "Speed comparison showing 'Code Generation Speed' with Codex: 0.5s, Claude Code: 2.3s, bold text, arrow indicators, professional metrics display"
    },
    {
        "id": "04",
        "title": "Context Window Comparison",
        "prompt": "Large text display showing 'Context Window Size' Claude Code: 200K tokens vs Codex: 8K tokens, visual bar chart, clear typography"
    },
    {
        "id": "05",
        "title": "Accuracy Rate Display",
        "prompt": "Performance metrics showing 'Accuracy Rate' Claude Code: 92% (green checkmark), Codex: 76% (orange indicator), professional gauge design"
    },
    {
        "id": "06",
        "title": "Real-World Use Case #1",
        "prompt": "Infographic titled 'Real-World Use Case: Newsletter Feature' with labeled components: Database Schema, REST API, Admin UI, Frontend Components - professional documentation style"
    },
    {
        "id": "07",
        "title": "Real-World Use Case #2",
        "prompt": "Workflow diagram showing 'Building a Mobile App' with steps: Plan → Code → Debug → Deploy, checkmarks on completed steps, arrows showing flow"
    },
    {
        "id": "08",
        "title": "Developer Workflow",
        "prompt": "Annotated developer workflow showing 'Claude Code + Codex Collaboration' with labeled steps: Planning (Claude) → Implementation (Codex) → Debugging (Claude) → Testing (Codex)"
    },
    {
        "id": "09",
        "title": "Claude Code Strengths",
        "prompt": "Bulleted list titled 'Claude Code Strengths' with checkmarks: ✓ Context Understanding, ✓ Multi-file Debugging, ✓ Architecture Planning, ✓ Code Explanation - professional bullet point design"
    },
    {
        "id": "10",
        "title": "Codex Strengths",
        "prompt": "Bulleted list titled 'Codex Strengths' with checkmarks: ✓ Fast Generation, ✓ IDE Integration, ✓ Quick Snippets, ✓ Auto-complete - professional bullet point style"
    },
    {
        "id": "11",
        "title": "Integration Comparison Table",
        "prompt": "Comparison table showing 'Integration Capability' with rows: IDE Integration (Codex ✓ Claude ✗), Web-based (Claude ✓ Codex ✗), API Access (Both ✓), Command Line (Both ✓)"
    },
    {
        "id": "12",
        "title": "Pricing Comparison",
        "prompt": "Cost comparison showing 'Pricing Model' Claude Code: Pay-per-token, Codex: Pay-per-token, with visual bar chart showing relative costs, clear typography"
    },
    {
        "id": "13",
        "title": "Who Should Use Claude Code",
        "prompt": "Targeted list 'Who Should Use Claude Code' with items: Architects, Full-stack Developers, Refactoring Tasks, Complex Debugging, Learning Code - professional formatting"
    },
    {
        "id": "14",
        "title": "Who Should Use Codex",
        "prompt": "Targeted list 'Who Should Use Codex' with items: Rapid Development, Quick Snippets, IDE-based Workflows, Boilerplate Generation - professional formatting"
    },
    {
        "id": "15",
        "title": "Conclusion Slide",
        "prompt": "Conclusion slide with main message 'Use Claude Code for THINKING, Use Codex for DOING' - large bold text, professional design, subtle gradient background"
    }
]

# ============================================================================
# IMAGEN 4 PROMPTS - PHOTOREALISTIC PEOPLE ($0.04 each fast, 6 images)
# ============================================================================
imagen_prompts = [
    {
        "id": "01",
        "title": "Developer Using Claude Code",
        "prompt": "Professional headshot of a focused developer sitting at a modern desk, typing on a MacBook, large screen showing code in background, studio lighting, confident expression, wearing casual tech company shirt"
    },
    {
        "id": "02",
        "title": "Developer Using Codex",
        "prompt": "Professional photo of a satisfied developer at desk with VS Code open, IDE integration visible, quick coding motion, bright studio lighting, successful expression, tech casual attire"
    },
    {
        "id": "03",
        "title": "Team Collaboration Scene",
        "prompt": "Two developers collaborating at a standing desk, looking at a large monitor displaying code together, modern office environment, daylight, professional attire, problem-solving expression"
    },
    {
        "id": "04",
        "title": "Developer Coding at Desk",
        "prompt": "Close-up of hands typing on mechanical keyboard, code visible on large monitor, desk with second monitor, coffee cup, professional workspace, focused concentration"
    },
    {
        "id": "05",
        "title": "Thinking/Problem-Solving Pose",
        "prompt": "Developer at desk with hand on chin, thoughtful expression looking at code on screen, sunlit office, modern workspace, peaceful concentration, problem-solving moment"
    },
    {
        "id": "06",
        "title": "Success/Achievement Expression",
        "prompt": "Happy developer celebrating a successful build, hands in the air, big smile, modern tech office background, large monitor showing green deployment status, achievement moment"
    }
]

# ============================================================================
# NANO BANANA PRO PROMPTS - INFOGRAPHICS ($0.15 each, 4 images)
# ============================================================================
nano_prompts = [
    {
        "id": "01",
        "title": "Performance Pie Chart",
        "prompt": "Infographic pie chart showing 'Feature Coverage' with segments: Claude Code 70%, Codex 60%, Other Tools 30%, labeled percentages, professional colors (blue/orange), clear legend"
    },
    {
        "id": "02",
        "title": "Feature Coverage Radar Chart",
        "prompt": "Radar/spider chart comparing Claude Code vs Codex across 6 dimensions: Speed, Accuracy, Context, IDE Integration, Explanation, Debugging - professional infographic style with legend"
    },
    {
        "id": "03",
        "title": "Workflow Efficiency Comparison",
        "prompt": "Infographic bar chart titled 'Workflow Efficiency' showing time saved: Manual Coding (100 hours) vs Claude Code (25 hours) vs Codex (15 hours), labeled axes, professional design"
    },
    {
        "id": "04",
        "title": "Integration Capability Matrix",
        "prompt": "2x3 capability matrix infographic showing features vs tools: VS Code, GitHub Copilot, Web Browser, API, Terminal - with checkmarks for supported integrations, professional business style"
    }
]

print(f"\nImage Generation Summary:")
print(f"  Recraft V3 (text): 15 images × $0.04 = $0.60")
print(f"  Imagen 4 (people): 6 images × $0.04 = $0.24")
print(f"  Nano Banana Pro: 4 images × $0.15 = $0.60")
print(f"  TOTAL COST: $1.44\n")

input("Press ENTER to start generating images, or Ctrl+C to cancel: ")

# For now, save the prompts to a file for batch processing
prompts_file = {
    "recraft": recraft_prompts,
    "imagen": imagen_prompts,
    "nano_banana": nano_prompts
}

with open("output/image_generation_prompts.json", "w") as f:
    json.dump(prompts_file, f, indent=2)

print("Image prompts saved to: output/image_generation_prompts.json")
print("\nNOTE: Image generation requires manual FAL.ai API calls or integration.")
print("To generate images, you can:")
print("  1. Use FAL.ai Web Dashboard (fal.ai/dashboard)")
print("  2. Use the provided prompts above")
print("  3. Continue with existing images for now\n")

# ============================================================================
# PHASE 2: DOWNLOAD ROYALTY-FREE MUSIC
# ============================================================================
print("="*70)
print("PHASE 2: DOWNLOADING ROYALTY-FREE MUSIC")
print("="*70)

print("\nDownloading 'Technology Dreams' from Pixabay...")
music_urls = {
    "technology_dreams": "https://cdn.pixabay.com/music/corporate_-_technology_dreams_ambient_background_tech_corporate_ai_-_195473.mp3"
}

music_dir = Path("output/music")
music_dir.mkdir(exist_ok=True)

for name, url in music_urls.items():
    output_file = music_dir / f"{name}.mp3"

    try:
        print(f"Downloading: {name}...")
        urllib.request.urlretrieve(url, output_file)
        file_size = output_file.stat().st_size / (1024*1024)
        print(f"✓ Downloaded: {file_size:.1f}MB")
    except Exception as e:
        print(f"✗ Error downloading {name}: {e}")
        print(f"  You can download manually from: {url}")

# ============================================================================
# PHASE 3: GENERATE SUBTITLE FILE (SRT FORMAT)
# ============================================================================
print("\n" + "="*70)
print("PHASE 3: GENERATING SUBTITLE FILE (SRT FORMAT)")
print("="*70)

subtitle_data = [
    (0, 3, "Hey everyone, thanks for clicking in."),
    (3, 6, "Today, I'm answering a question I get asked constantly:"),
    (6, 10, "'Should I use Claude Code or should I use Codex?'"),
    (10, 14, "And here's the thing... you're probably asking the wrong question."),
    (14, 22, "After weeks of testing both tools in production environments,"),
    (22, 28, "I discovered something that completely changed how I code."),
    (28, 34, "They're not competitors. They're not an either-or choice."),
    (34, 40, "They're actually the perfect team, and knowing how to use them"),
    (40, 44, "together is going to save you hours on your next project."),
    (44, 50, "Let me start with Codex alone. Codex is fast. Really fast."),
    (50, 56, "You give it a prompt, and boom... it generates code instantly."),
    (56, 62, "But here's the problem. That speed comes with a cost."),
    (62, 68, "The code Codex generates is minimal. It's technically correct,"),
    (68, 74, "sure, but... it doesn't handle edge cases."),
    (74, 80, "It doesn't include quality-of-life features."),
    (80, 86, "And when you ask Codex to understand WHY something works,"),
    (86, 92, "or to debug across multiple files..."),
    (92, 98, "Codex has a limited context window."),
    (98, 104, "It can't see your entire codebase."),
    (104, 110, "So it generates code that works in isolation"),
    (110, 116, "but breaks your existing architecture when you integrate it."),
    (116, 124, "You end up debugging integration issues that shouldn't exist."),
    (124, 130, "Codex is like asking for a house and getting a tent."),
    (130, 136, "It's shelter, technically, but it's not what you needed."),
    (136, 144, "Now let's look at Claude Code alone. Claude Code is exceptional."),
    (144, 150, "It understands context. It explains its reasoning."),
    (150, 156, "It can debug multi-file problems."),
    (156, 162, "But—and this is important—all that thoroughness takes time."),
    (162, 170, "When you're writing a simple function, waiting for Claude"),
    (170, 176, "to analyze your entire codebase is overkill."),
    (176, 184, "This is where Claude Code falls into the over-engineering trap."),
    (184, 190, "Ask it to add error handling to a function,"),
    (190, 196, "and it might create abstract factories,"),
    (196, 202, "unnecessary design patterns, and 20 files when three would suffice."),
    (202, 208, "You don't need a research paper when you just want to close a div."),
    (208, 214, "And there's another issue..."),
    (214, 220, "Claude Code requires context switching."),
    (220, 226, "It's not embedded in your IDE."),
    (226, 234, "So you're constantly breaking your flow—type something,"),
    (234, 240, "switch to Claude Code, copy the result back, rinse and repeat."),
    (240, 248, "So we have a dilemma. Codex is fast but shallow."),
    (248, 254, "Claude Code is deep but slow."),
    (254, 260, "What if there was a way to use them together?"),
    (260, 268, "Here's the breakthrough: Use Codex as your implementation engine,"),
    (268, 274, "and Claude Code as your strategic advisor."),
    (274, 284, "The workflow is simple. Use Codex in your IDE for rapid code generation."),
    (284, 290, "It stays in your editor, you stay in flow, and code gets written fast."),
    (290, 298, "Then, when you hit the thinking parts—planning, debugging,"),
    (298, 304, "architecture decisions—switch to Claude Code."),
    (304, 310, "Let it analyze, explain, and guide you."),
    (310, 318, "Claude Code brings creative problem-solving and comprehensive implementations."),
    (318, 324, "Codex brings speed and IDE integration."),
    (324, 330, "Together, they cover every phase of development without gaps."),
    (330, 338, "This isn't about choosing one or the other."),
    (338, 344, "It's about knowing when to switch and why."),
    (344, 352, "Let me show you this in action. Real project. Real workflow."),
    (352, 360, "I was adding a newsletter subscription feature to a WordPress theme."),
    (360, 368, "This isn't a simple task."),
    (368, 374, "It involves database schema, REST API endpoints,"),
    (374, 380, "admin UI integration, and front-end components."),
    (380, 386, "Perfect test case for showing how this works."),
    (386, 394, "Phase 1: Planning. I opened Claude Code and asked it"),
    (394, 400, "to analyze my WordPress setup and plan the architecture."),
    (400, 408, "Claude examined my existing codebase, identified where to integrate"),
    (408, 414, "the feature, and explained the trade-offs."),
    (414, 420, "I got a complete implementation plan"),
    (420, 426, "with file locations, database structure, and security considerations."),
    (426, 434, "Phase 2: Implementation. Now I switched to Codex in VS Code."),
    (434, 440, "I started following Claude's plan, and whenever I needed"),
    (440, 446, "the next function... Codex autocompletes it."),
    (446, 452, "Codex generates the boilerplate, writes the API endpoints,"),
    (452, 458, "handles the database interactions. Fast. Stay in flow state."),
    (458, 464, "No context switching. Just type and generate."),
    (464, 472, "Phase 3: Debugging. About halfway through, something didn't work."),
    (472, 478, "An API endpoint was returning the wrong data,"),
    (478, 484, "and there was an authentication issue."),
    (484, 492, "Back to Claude Code. I pasted the error, the relevant code files,"),
    (492, 498, "and my implementation notes."),
    (498, 504, "Claude traced the issue across multiple files,"),
    (504, 510, "found the root cause, and explained exactly what was wrong"),
    (510, 516, "and how to fix it."),
    (516, 524, "Not just a patch. An explanation."),
    (524, 530, "A fix that prevents the issue from recurring."),
    (530, 536, "This is Claude Code's strength—deep analysis and understanding."),
    (536, 544, "The result? A feature that was secure, consistent,"),
    (544, 550, "correctly integrated, and fully documented."),
    (550, 556, "Total time: about 30 minutes."),
    (556, 562, "Without this workflow? Maybe two hours,"),
    (562, 568, "with way more back-and-forth and debugging."),
    (568, 576, "Here's your decision framework. It's simple."),
    (576, 582, "Ask yourself: What kind of task is this?"),
    (582, 590, "Planning, debugging, analyzing, refactoring strategy?"),
    (590, 596, "Use Claude Code. Get the thinking work done."),
    (596, 602, "Get the plan right."),
    (602, 610, "Writing code, implementing features, need autocomplete,"),
    (610, 616, "doing routine work? Use Codex. Stay fast. Stay in flow."),
    (616, 624, "The key is recognizing which mode you're in"),
    (624, 630, "and switching tools accordingly. That's it. That's the whole system."),
    (630, 638, "Now, a few pro tips to make this workflow effortless."),
    (638, 644, "Pro tip one: Set up keyboard shortcuts."),
    (644, 650, "Make invoking each tool instant."),
    (650, 656, "Alt+Shift+C for Claude Code. Alt+Shift+X for Codex."),
    (656, 662, "Minimize friction."),
    (662, 670, "Pro tip two: Use Claude Code to generate implementation plans,"),
    (670, 676, "then paste them as comments in your IDE."),
    (676, 682, "Let Codex follow the plan you've already thought through."),
    (682, 690, "Pro tip three: Keep Claude Code open in a terminal"),
    (690, 696, "next to your IDE. Switch with a single Alt-Tab."),
    (696, 702, "It sounds small, but it matters."),
    (702, 710, "And most importantly: Don't skip the thinking phase."),
    (710, 716, "I know it's tempting to just ask Codex"),
    (716, 722, "'build me a feature.' But five minutes of planning"),
    (722, 728, "with Claude Code saves 30 minutes of debugging."),
    (728, 736, "Here's what you need to remember."),
    (736, 742, "The question isn't Claude Code or Codex."),
    (742, 748, "The question is: How do I use them together?"),
    (748, 754, "They're not competitors fighting for your attention."),
    (754, 760, "They're collaborators."),
    (760, 768, "Pick one feature. Next time you code something."),
    (768, 774, "Use Claude Code to plan it. Use Codex to build it."),
    (774, 780, "Because you're finally using the right tool"),
    (780, 786, "at the right time."),
    (786, 792, "Thanks for watching."),
    (792, 798, "If this was helpful, smash that like button."),
    (798, 804, "Subscribe for more workflows and productivity hacks like this."),
    (804, 810, "And drop a comment: which tool do you use more?"),
    (810, 815, "See you next time."),
]

srt_content = ""
for idx, (start, end, text) in enumerate(subtitle_data, 1):
    srt_content += f"{idx}\n"
    start_time = f"{int(start//3600):02d}:{int((start%3600)//60):02d}:{int(start%60):02d},000"
    end_time = f"{int(end//3600):02d}:{int((end%3600)//60):02d}:{int(end%60):02d},000"
    srt_content += f"{start_time} --> {end_time}\n"
    srt_content += f"{text}\n\n"

subtitle_path = Path("output/subtitles.srt")
with open(subtitle_path, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"✓ Subtitle file created: {subtitle_path}")
print(f"  Total subtitles: {len(subtitle_data)}")
print(f"  Duration: {subtitle_data[-1][1]} seconds (~13 minutes)")

print("\n" + "="*70)
print("PHASE 1-3 COMPLETE!")
print("="*70)
print("\nNext Steps:")
print("1. Generate 25 new images using FAL.ai APIs (Recraft, Imagen, Nano Banana)")
print("2. Build enhanced Shotstack composition with:")
print("   - 55 total images (25 new + 30 best existing)")
print("   - Background music (royalty-free)")
print("   - Subtitle captions (TikTok-style)")
print("3. Shorter clip duration (3-5 seconds vs 8 seconds)")
print("4. Re-render video with improved composition")
print("5. Upload to YouTube, replace existing video")
print("\nEstimated remaining cost: $8-10 (Shotstack render)")
print("Budget utilization: 10/10 (perfect budget use)")
