# Example Output Structure

This shows what the pipeline generates. Your actual output will be customized for your article.

## File: dataset.jsonl

```json
{
  "id": "claude-code-vs-codex",
  "url": "https://www.nathanonn.com/claude-code-vs-codex-why-i-use-both-and-you-should-too/",
  "title": "Claude Code vs Codex: Why I Use Both and You Should Too",
  "description": "A comprehensive comparison of two powerful AI tools",
  "author": "Nathan Onn",
  "publishDate": "2024-01-15",
  "content": "[Full markdown content of article...]",
  "sections": [
    {"heading": "Introduction", "content": "...", "level": 2},
    {"heading": "What is Claude Code", "content": "...", "level": 2},
    {"heading": "What is Codex", "content": "...", "level": 2}
  ],
  "extracted_at": "2024-12-10T14:32:00.000Z",
  "language": "en",
  "word_count": 2847,
  "char_count": 15234
}
```

---

## File: video-storyboard.md (excerpt)

```markdown
# STORYBOARD: Claude Code vs Codex

**Estimated Duration:** 5 minutes
**Content Volume:** 15,234 characters, 8 major sections

## Scene Breakdown

### SCENE 1: INTRO (0:00 - 0:45)
**Visual:** Title card with animated text
**Content:** Hook + problem statement
**B-Roll:** Background tech animations, logo reveal
**Narration Duration:** 30-45 seconds

### SCENE 2: WHAT IS CLAUDE CODE (0:45 - 2:30)
**Visual:** Split screen comparison
**Content:** Key features and explanations
**B-Roll:** Relevant animations, code examples, demos
**Narration Duration:** 105 seconds
```

---

## File: video-narration.md (excerpt)

```markdown
## INTRO (30-45 seconds)

"Hey everyone! Have you ever wondered about the differences between Claude Code and Codex?

Today we're diving deep into this topic to show you exactly what you need to know.
Stick around!"

---

## MAIN CONTENT

"So here's the thing: Claude Code and Codex are two powerful AI tools that serve
different purposes. This matters because understanding their strengths helps you
choose the right tool for your workflow.

Let me show you exactly how this works...

Moving on to the key differences. Notice how each tool handles specific tasks differently.
This is important for optimizing your productivity.
```

---

## File: slide-deck.md (excerpt)

```markdown
# SLIDE DECK OUTLINE

## Slide 1: Title
- Title: Claude Code vs Codex: Why I Use Both and You Should Too
- Subtitle: A Comprehensive Comparison
- Background: Bold color or gradient

## Slide 2: What is Claude Code?
- Main point: Claude Code is an integrated development environment
- Sub-points:
  • Real-time code analysis and suggestions
  • Context-aware completions
  • Built-in testing framework
- Visual: Diagram or demo screenshot
- Transition: Fade

## Slide 3: What is Codex?
- Main point: Codex is specialized for rapid prototyping
- Sub-points:
  • Fast generation from natural language
  • Multiple language support
  • Excellent documentation generation
- Visual: Feature showcase
- Transition: Fade
```

---

## File: video-graphs.md (excerpt)

```markdown
# VISUAL GRAPHS & DIAGRAMS

## Diagram 1: Feature Comparison

┌─────────────────────────────────────┐
│   CLAUDE CODE VS CODEX FEATURES     │
└────────────────┬────────────────────┘
         │
   ┌─────┼─────┐
   │     │     │
 SPEED QUALITY SUPPORT
   │     │     │
   └─────┼─────┘
         │
    COMPARISON

## Diagram 2: Timeline

START ─────> INTRO ─────> CONTENT ─────> RECAP ─────> END
 0:00        0:30         1:00          4:00        5:00

## Diagram 3: Engagement Curve

ENGAGEMENT
    ▲
    │        ╱╲        ╱╲
    │       ╱  ╲      ╱  ╲
    │      ╱    ╲    ╱    ╲
    │     ╱      ╲  ╱      ╲
    │────────────────────────→ TIME
         Hook    Key      CTA
```

---

## File: video-editing-guide.md (excerpt)

```markdown
# VIDEO EDITING GUIDE

## Timeline Markers
- `00:00` - Start (include black screen/intro)
- `00:05` - Logo reveal
- `00:30` - Main content begins
- `4:00` - Wrap-up begins
- `5:30` - Credits roll

## Transitions
- Between sections: Use fade or subtle zoom
- Key points: Use emphasis animations
- B-roll switches: Cross-fade for smooth flow

## Text Overlays
- Chapter titles with slight delay
- Key takeaways as bullet points
- Time stamps for reference
- Subscribe/like reminders at key moments

## Audio
- Background music: Royalty-free, 50% volume
- Sound effects: Use sparingly for emphasis
- Silence: 0.5s between major sections
```

---

## File: clean-report.json

```json
{
  "file": "dataset.jsonl",
  "records_processed": 1,
  "total_errors": 0,
  "total_warnings": 2,
  "timestamp": "2024-12-10T14:35:22.000Z",
  "records": [
    {
      "id": "claude-code-vs-codex",
      "title": "Claude Code vs Codex: Why I Use Both and You Should Too",
      "word_count": 2847,
      "char_count": 15234,
      "sections": 8
    }
  ]
}
```

---

## What You Do With Each File

| File | Usage |
|------|-------|
| `dataset.jsonl` | Upload to Claude for analysis, use for fine-tuning models |
| `video-storyboard.md` | Plan your shots and timing while recording |
| `video-narration.md` | Read this into a microphone in Audacity |
| `slide-deck.md` | Create slides in Canva/Figma based on this outline |
| `video-graphs.md` | Copy diagrams into your slides as visuals |
| `video-editing-guide.md` | Follow these instructions in DaVinci Resolve/Premiere |
| `clean-report.json` | Reference for data quality checks |

---

## Example Workflow With This Output

### 1. Open video-narration.md
```
Read this text naturally into a microphone
Time: ~5 minutes to read
Save as: narration.mp3
```

### 2. Create Slides Based on slide-deck.md
```
Slide 1: Title card
  - Use: video-graphs.md Diagram 1 as supporting visual

Slide 2: Claude Code overview
  - Add: Screenshots or feature icons

Slide 3: Codex overview
  - Add: Feature comparison diagram

Slide 4: Use cases
  - Add: Icons or illustrations

Slide 5: Conclusion
  - Add: CTA (Subscribe, etc.)
```

### 3. Generate AI Video (Pika Labs)
```
Upload: 5 slide images
Upload: narration.mp3
Select: Timing from video-storyboard.md
Generate: final_video.mp4
```

### 4. Edit in DaVinci Resolve
```
Import: final_video.mp4
Add: Background music (50% volume)
Follow: video-editing-guide.md timing
Add: Title cards at scene breaks
Add: Captions/subtitles
Export: final_upload.mp4
```

### 5. Upload to YouTube
```
Title: "Claude Code vs Codex: Why I Use Both"
Description: [Original article URL]
Tags: claude-code, codex, ai-tools, comparison
Thumbnail: Slide 1 screenshot
```

---

## Real Timeline Example

For a ~2800 word article:

- **Scraping:** 30 seconds
- **JSONL conversion:** 5 seconds
- **Video script generation:** 10 seconds
- **Recording narration:** 10 minutes
- **Creating slides:** 25 minutes
- **AI video generation:** 5 minutes
- **Final editing:** 15 minutes

**Total:** ~60 minutes to complete video

---

## Your Article Will Be Different

The structure above is an example. Your actual output will:
- Match YOUR article's content
- Have YOUR article's sections
- Include YOUR article's title
- Generate YOUR article's specific graphs

Just follow the same workflow with whatever your pipeline generates!
