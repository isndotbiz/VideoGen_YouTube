# Video Accessibility Guidelines: Claude Code vs Codex Comparison

## Executive Summary

This document provides comprehensive accessibility guidelines for creating an inclusive video comparing Claude Code and Codex. These guidelines ensure compliance with WCAG 2.1 AA standards (targeting AAA where feasible) and make content accessible to users with visual, auditory, cognitive, and vestibular disabilities.

---

## 1. WCAG 2.1 Color and Contrast Requirements

### 1.1 Color Contrast Ratios

#### Minimum Requirements (Level AA)
- **Normal text**: 4.5:1 contrast ratio minimum
  - Normal text = any text under 18pt (24px) or under 14pt (18.66px) bold
- **Large text**: 3:1 contrast ratio minimum
  - Large text = 18pt (24px)+ regular or 14pt (18.66px)+ bold
- **UI components/Graphics**: 3:1 contrast ratio minimum
  - Applies to icons, buttons, charts, diagrams

#### Enhanced Requirements (Level AAA - Recommended)
- **Normal text**: 7:1 contrast ratio
- **Large text**: 4.5:1 contrast ratio
- **UI components/Graphics**: 4.5:1 contrast ratio

### 1.2 Specific Color Values for Your Video

#### High Contrast Text Combinations

**Primary Option (21:1 ratio):**
- White text (#FFFFFF) on black background (#000000)
- Use for: Main captions, critical information

**Secondary Options:**
- Dark blue (#003366) on white (#FFFFFF) - 12.6:1 ratio
- Black text (#000000) on yellow (#FFD700) - 13.3:1 ratio
- White (#FFFFFF) on dark green (#004D00) - 9.5:1 ratio

#### Color Coding for Technical Comparisons

**Never rely on color alone.** Always pair color with:
- Text labels
- Icons/symbols
- Patterns/textures
- Shape differences

### 1.3 Colorblind-Accessible Palette

#### Safe Color Combinations
1. **Blue and Orange** (works for all types of colorblindness)
   - Blue: #0066CC
   - Orange: #FF6600
   - Contrast ratio between: 3.8:1

2. **Blue and Red**
   - Blue: #0066CC
   - Red: #CC0000
   - Use light blue with very dark red for maximum distinction

3. **Blue and Brown**
   - Blue: #0066CC
   - Brown: #663300

#### Colors to AVOID
- Red and green together (most common colorblind issue)
- Yellow and light green
- Pink and gray
- Red and brown

#### Implementation Strategy
- Use blue as your primary color (safe for all colorblind types)
- Add high luminance contrast (light vs. dark)
- Use patterns/icons alongside color coding
- Test with colorblind simulators

---

## 2. Text Readability Standards

### 2.1 Font Selection

#### Primary Recommendations

**For Body Text:**
- **Verdana** - Excellent for neurodivergent users
- **Open Sans** - High readability for ADHD/cognitive disorders
- **Lexend** - Optimized for disabilities including ADHD
- **Arial** - Universal clarity

**For Dyslexic Users:**
- **OpenDyslexic** - Reduces letter confusion
- **Dyslexie Font** - Evidence-based improvement for dyslexia
- Alternative: Any clear sans-serif with 1.5+ line spacing

**For Captions/Subtitles:**
- **Helvetica Medium Italic** - Classic yellow subtitle style
- **Roboto** - Clean, modern, legible on small screens
- **Arial Bold** - High contrast situations

**Avoid:**
- Serif fonts for body text
- Decorative/script fonts
- Fonts with tight letter spacing

### 2.2 Font Sizes

#### Minimum Sizes (WCAG 2.1 AA)
- **Body text**: 12px minimum (16px recommended)
- **Headings**: 18-24px minimum
- **Captions**: 14pt minimum for subtitles

#### Optimal Sizes
- **On-screen body text**: 18-24px
- **Headings**: 28-36px
- **Captions**: 16-20pt for optimal readability

### 2.3 Text Spacing Requirements

All text must support these adjustments without losing content:

- **Line height**: 1.5x the font size (minimum)
  - Example: 16px font = 24px line height
  - For dyslexic users: up to 2.5x spacing
- **Paragraph spacing**: 2x the font size
- **Letter spacing**: 0.12x the font size
- **Word spacing**: 0.16x the font size

### 2.4 Text Resizing
- Users must be able to resize text to 200% without loss of content
- Ensure responsive design doesn't break at larger text sizes

---

## 3. Motion and Animation Accessibility

### 3.1 WCAG Motion Requirements

#### Success Criterion 2.3.3 (AAA)
Motion animation triggered by interaction can be disabled, unless:
- The animation is essential to functionality
- The information being conveyed requires animation

### 3.2 Vestibular Disorder Considerations

#### Motion Triggers to Avoid/Minimize
- **Parallax scrolling** (background/foreground at different speeds)
- **Large object scaling/zooming**
- **Rapid panning**
- **Spinning/rotating elements**
- **Flashing/strobing** (NEVER exceed 3 flashes per second)

#### Effects on Users
- Dizziness
- Nausea
- Headaches
- Disorientation
- Distraction

### 3.3 Implementation Strategies

#### Provide Motion Controls
1. Add on-screen toggle to disable animations
2. Respect operating system `prefers-reduced-motion` settings
3. Offer alternative static visualizations

#### Reduced Motion Alternatives
- Replace animations with fade-in/fade-out
- Use static slides instead of transitions
- Show instant state changes instead of animated transitions
- Provide still frame alternatives

#### Animation Best Practices (when used)
- Keep animations subtle and slow
- Duration: 200-500ms maximum
- Use easing functions (ease-in-out)
- Avoid sudden movements
- Limit simultaneous animations

---

## 4. Audio Accessibility

### 4.1 Optimal Speaking Pace

#### Recommended Speed
- **Optimal**: 150-160 words per minute (WPM)
  - Sweet spot for engagement and comprehension
  - Recommended by voice coaches and experts

#### Speed Ranges by Content Type
- **Simple content**: 160-200 WPM acceptable
- **Complex technical content**: 120-150 WPM
  - Use slower end for jargon and multi-syllable terms
- **Maximum processing**: 500 WPM (human limit)
  - NEVER approach this; leaves no mental energy for learning

#### Implementation Guidelines
- **Base pace**: 150 WPM for main content
- **Vary speed for emphasis**:
  - Slow down for key concepts (120 WPM)
  - Speed up slightly for examples (170 WPM)
- **Pause strategy**:
  - 1-2 second pauses between major sections
  - 0.5 second pauses between sentences
  - 2-3 second pauses before/after code examples

### 4.2 Background Music Guidelines

#### WCAG Requirement
Non-speech sounds must be **at least 20 decibels lower** than speech content.

#### Specific Volume Levels
- **Voice/Dialogue**: -6 dB to -12 dB (peak)
- **Background music**: -18 dB to -25 dB
- **Effective range**: Voice at -17.5 dB, music at -37.5 dB

#### Professional Mixing Standards
1. **Normalize voice-over**: Peak around -6 dB
2. **Set music volume**: Start at -20 dB, adjust by genre
3. **Minimum difference**: Voice 20+ dB higher than background

#### Ducking Technique
- Automatically lower background music when voice plays
- Set fade-in/fade-out: 0.5-1 second
- Adjust sensitivity for natural results
- Apply to every voice segment

#### Music Selection
- Choose non-distracting instrumental tracks
- Avoid music with complex melodies
- Prefer ambient/atmospheric styles
- Ensure no sudden volume spikes

---

## 5. Captions and Subtitles

### 5.1 Caption Quality Standards

#### Accuracy Requirements
- **99% accuracy** in spelling and grammar
- Exact speaker words (no paraphrasing)
- Include significant sound effects
- Note speaker changes

#### Timing Standards
- Synchronize within 0.5 seconds of audio
- Display 2-3 seconds per caption minimum
- Maximum 3 lines per caption
- Reading speed: ~150-160 WPM

#### Position Guidelines
- **Default**: Bottom center
- **Offset**: 10% from bottom edge
- **Never obscure**: Speaker's face, important visuals, lower thirds
- **Alternative positions**: Top when necessary

### 5.2 Caption Styling

#### Color and Contrast (Recommended)

**Option 1: Standard (21:1 ratio)**
- White text (#FFFFFF)
- Black semi-transparent background (rgba(0,0,0,0.8))
- Works for 90% of content

**Option 2: Classic Film Style**
- Yellow text (#FFD700 or #FFF44F)
- Black background or black outline
- Helvetica Medium Italic font
- Size: 14pt

**Option 3: High Visibility**
- Yellow text (#FFD700)
- Black background
- Bold Open Sans
- Best for fast dialogue

#### Font Specifications
- **Font**: Helvetica, Roboto, Arial (sans-serif only)
- **Size**: 16-20pt (adjust for screen size)
- **Weight**: Regular or Medium (Bold for emphasis only)
- **Style**: Regular or Italic (not both)
- **Case**: Sentence case (NEVER all caps except for shouting)

#### Customization Options
Users should be able to adjust:
- Caption color
- Background opacity
- Font size
- Line height (1.5-2.0x)
- Letter spacing

### 5.3 Subtitles for Deaf and Hard of Hearing (SDH)

Include beyond standard captions:
- **Speaker identification**:
  - [Speaker name] or [Description]
  - Example: [NARRATOR] or [MALE VOICE]
- **Sound descriptions**:
  - [clicking sounds]
  - [upbeat music playing]
  - [door closes]
- **Musical cues**:
  - [Music: Dramatic orchestral theme]
  - ♪ [Song title and artist] ♪
- **Tone indicators**:
  - (sarcastically)
  - (whispering)
  - (laughing)

### 5.4 Caption File Formats
- **Primary**: WebVTT (.vtt) - best web support
- **Alternative**: SRT (.srt) - universal compatibility
- **Include**: Styling metadata in VTT files
- **Avoid**: Hardcoded/burned-in captions (unless also providing separate caption track)

---

## 6. Transcripts

### 6.1 Transcript Requirements

#### Essential Content
1. **All spoken dialogue**
2. **Speaker identification**
3. **Relevant sound effects**
4. **Important visual information**
   - On-screen text
   - Code snippets shown
   - Diagram descriptions
5. **Context for non-visual users**

### 6.2 Formatting Best Practices

#### Structure
```
[Optional timestamp: 00:03:45]

SPEAKER NAME (or Speaker 1):
Dialogue here. Multiple sentences together.

[Sound effect: keyboard typing]

SPEAKER 2:
Response dialogue.

[Visual description: Code snippet showing Python function]
```

#### Speaker Identification
- **Bold speaker labels**: **NARRATOR:**
- **Use real names** when possible
- **Fallback**: Speaker 1, Speaker 2
- **Include descriptor**: [FEMALE VOICE], [NARRATOR]
- **Identify each speaker change**

#### Timestamps
- **Optional**: Include only if adding value
- **Frequency**: At speaker changes or major sections
- **Format**: [HH:MM:SS] or [MM:SS]
- **Placement**: Before speaker label or section

#### Visual Descriptions
- Include all on-screen text
- Describe charts, diagrams, code snippets
- Note colors if used to convey meaning
- Describe relevant animations/transitions

### 6.3 Placement and Access
- Link to transcript immediately below video
- Provide downloadable versions (PDF, TXT, DOCX)
- Include transcript in video description
- Make transcript searchable and navigable

---

## 7. Audio Descriptions

### 7.1 What are Audio Descriptions?

Audio descriptions provide narration of important visual information for blind and low-vision users, inserted during natural pauses in dialogue.

### 7.2 Content to Describe

#### Essential Visual Information
- **Actions**: "Claude types code into terminal"
- **Scene changes**: "View switches to Codex interface"
- **On-screen text**: Read any text that isn't spoken
- **Charts/graphs**: Describe data and trends
- **Visual comparisons**: "Side-by-side view shows..."
- **Code snippets**: Read and describe code structure
- **Color-coded information**: "Blue bar represents Codex"

#### What NOT to Describe
- Actions that are obvious from audio
- Decorative elements
- Information already in dialogue

### 7.3 Delivery Standards

#### Timing
- Insert during natural dialogue pauses
- Keep descriptions brief (1-3 seconds)
- Don't talk over dialogue
- Match pace with video tempo

#### Voice and Style
- Professional narrator voice
- Clear, concise language
- Objective descriptions (no interpretation)
- Consistent terminology

### 7.4 Technical Implementation
- **Separate audio track**: SAP (Secondary Audio Programming) channel
- **Alternative**: Extended audio description with paused video
- **Format**: Include in video player's accessibility features
- **Labeling**: Clear "Audio Description" option in player

### 7.5 Audio Description Script Example

```
[Visual: Split screen showing Claude Code and Codex interfaces]
AD: "Screen splits to show Claude Code on the left and Codex on the right."

[Visual: Code appears in both editors]
AD: "Both editors display the same Python function."

[Visual: Typing indicators]
AD: "Cursor blinks in each interface."

[Visual: Performance chart appears]
AD: "Bar chart appears comparing response times. Claude Code shows 2.3 seconds, Codex shows 3.7 seconds."
```

---

## 8. Accessible Technical Documentation

### 8.1 Presenting Code Accessibly

#### For Screen Readers
- **Use actual code blocks** (not images)
- **Provide alt-text** for code images if unavoidable
- **Include code in transcript** with explanations
- **Announce syntax**: "Opening curly brace, closing parenthesis"

#### Visual Presentation
- **High contrast**: Use syntax highlighting with 4.5:1+ contrast
- **Readable fonts**: JetBrains Mono, Fira Code, Consolas
- **Font size**: 14-16pt minimum for code
- **Line spacing**: 1.5x minimum
- **No color-only coding**: Pair colors with bold/italic/comments

#### Accessible Color Schemes for Code
- **Solarized Dark**: High contrast, colorblind-friendly
- **One Dark Pro**: Good contrast ratios
- **GitHub Light/Dark**: Tested accessibility
- **Avoid**: Low-contrast "aesthetic" themes

### 8.2 Comparison Charts and Tables

#### For Blind/Low-Vision Users
- **Sonification**: Convert data to audio (tone = value)
- **Textual descriptions**: "Claude Code scored 8 out of 10"
- **Data tables**: Provide HTML table with headers
- **Alt text**: "Bar chart showing Claude Code (85%) vs Codex (72%)"

#### Visual Design
- **High contrast bars/lines**: 3:1 minimum
- **Patterns in addition to color**: Stripes, dots, hatching
- **Clear labels**: Direct labeling, not legend-only
- **Large text**: 14pt+ for all chart text
- **Axis labels**: Clear, high-contrast, large font

#### Chart Types by Accessibility
**Most Accessible:**
- Simple bar charts (horizontal best)
- Line graphs (thick lines, 2:1 ratio between lines)
- Data tables

**Use with Caution:**
- Pie charts (provide table alternative)
- Stacked charts (complex for screen readers)
- 3D charts (depth perception issues)

**Avoid:**
- Color-only distinctions
- Small multiples without context
- Complex interactive-only charts

### 8.3 Technical Comparison Best Practices

#### Structure
1. **Lead with summary**: "Claude Code is faster but Codex has more features"
2. **Use clear headings**: Screen reader navigation
3. **Provide context**: Explain technical terms
4. **Multiple formats**: Text, chart, table, audio

#### Language Guidelines
- **Clear, concise**: Short sentences
- **Define jargon**: First use of technical terms
- **Active voice**: "Claude Code processes requests"
- **Consistent terminology**: Same term for same concept

#### Visual Hierarchy
- **Heading levels**: Proper H1, H2, H3 structure
- **Lists**: Use actual list markup
- **Emphasis**: Bold for strong, italic for mild
- **Spacing**: Generous white space between sections

---

## 9. Specific Recommendations for Claude Code vs Codex Video

### 9.1 Visual Design

#### Color Palette
**Primary Colors:**
- Claude Code: Blue (#0066CC)
- Codex: Orange (#FF6600)
- Background: Dark gray (#1E1E1E) or white (#FFFFFF)
- Text: White on dark, black on light (21:1 ratio)

**Why This Works:**
- Blue/orange safe for all colorblind types
- High contrast for low vision users
- Professional appearance

**Secondary Indicators:**
- Claude Code: Solid patterns, circle icons
- Codex: Striped patterns, square icons
- Never rely on color alone

#### Layout
- **Split screen comparisons**: Clear vertical divider
- **Side-by-side code**: Line numbers, syntax highlighting
- **Comparison overlays**: High contrast, large text
- **Transition indicators**: Announce "Switching to Codex view"

### 9.2 Content Structure

#### Opening (0:00-0:30)
- **Visual**: Title card with high contrast
- **Audio**: Clear introduction at 150 WPM
- **Captions**: Large, centered
- **Audio description**: "Title card: Claude Code vs Codex Comparison"

#### Main Comparisons (0:30-3:00)
- **Segment each feature**: 20-30 seconds per comparison
- **Consistent structure**:
  1. Introduce feature (5s)
  2. Show Claude Code (7s)
  3. Show Codex (7s)
  4. Present results (6s)
- **Clear transitions**: 2-second pause between segments
- **Visual consistency**: Same layout for each comparison

#### Results/Conclusion (3:00-3:30)
- **Summary chart**: Bar chart with patterns
- **Key findings**: Bullet points on screen
- **Audio recap**: Slightly slower pace (140 WPM)
- **Audio description**: Full description of final chart

### 9.3 Audio Strategy

#### Voice-Over
- **Speed**: 150 WPM average
- **Slow for code**: 120 WPM when reading code
- **Natural pauses**: 2s between major sections

#### Background Music
- **Genre**: Ambient, non-distracting
- **Volume**: -25 dB (voice at -6 dB)
- **Ducking**: Reduce to -35 dB during voice
- **Avoid**: Sudden changes, complex melodies

#### Sound Effects
- **Minimal use**: Only for transitions
- **Volume**: -20 dB maximum
- **Type**: Subtle whoosh, click
- **Purpose**: Reinforce visual transitions

### 9.4 Caption Strategy

#### Styling
- **Font**: Roboto Medium
- **Size**: 18pt
- **Color**: White (#FFFFFF)
- **Background**: Black 80% opacity
- **Position**: Bottom center, 10% from edge

#### Content
- **Speaker ID**: [NARRATOR]
- **Sound effects**: [transition sound]
- **Code reading**: "Function: def process_request"
- **Timing**: 2.5s per caption minimum

### 9.5 Transcript Example

```
[00:00] Introduction

NARRATOR:
Welcome to our comparison of Claude Code and Codex. We'll evaluate speed, accuracy, and ease of use.

[Audio description: Title card displays "Claude Code vs Codex" in white text on blue background]

[00:15] Speed Comparison

NARRATOR:
First, let's compare processing speed. We'll send the same request to both platforms.

[Visual: Split screen showing both interfaces. Timers appear below each.]

[Audio description: Split screen view. Claude Code interface on left shows blue theme. Codex interface on right shows orange theme. Stopwatch timers display below each interface.]

[00:30] Results

NARRATOR:
Claude Code completed the task in 2.3 seconds. Codex finished in 3.7 seconds.

[Visual: Bar chart appears showing results]

[Audio description: Horizontal bar chart appears. Blue striped bar for Claude Code extends to 2.3 seconds. Orange dotted bar for Codex extends to 3.7 seconds.]
```

---

## 10. Testing and Validation

### 10.1 Required Testing

#### Automated Testing Tools
- **Color contrast**: WebAIM Contrast Checker, WAVE
- **Colorblind simulation**: Coblis, Color Oracle
- **Caption quality**: YouTube auto-caption check
- **Screen reader**: NVDA (free), JAWS, VoiceOver

#### Manual Testing
- **Watch with captions only** (sound off)
- **Listen with eyes closed** (audio + descriptions)
- **Colorblind simulation**: View with filters
- **Screen reader**: Navigate entire transcript
- **Reduced motion**: Test with motion disabled

### 10.2 User Testing

#### Test with Diverse Users
- Deaf/hard of hearing individuals
- Blind/low vision users
- Colorblind users
- Users with cognitive disabilities
- Users with vestibular disorders

#### Key Questions
1. Can you understand the content with captions only?
2. Do audio descriptions provide sufficient context?
3. Are colors distinguishable in comparisons?
4. Does motion cause discomfort?
5. Is the pace appropriate?

### 10.3 Validation Checklist

#### WCAG 2.1 AA Compliance
- [ ] All text has 4.5:1 contrast (normal) or 3:1 (large)
- [ ] All UI elements have 3:1 contrast
- [ ] Color is not the only way to convey information
- [ ] Text can be resized to 200% without loss
- [ ] Captions are provided for all audio
- [ ] Audio descriptions are provided for visual content
- [ ] Background audio is 20+ dB lower than speech
- [ ] Motion can be disabled or reduced

#### Enhanced Accessibility (AAA)
- [ ] Text has 7:1 contrast ratio
- [ ] Transcripts provided for all video content
- [ ] Extended audio descriptions for complex visuals
- [ ] Sign language interpretation (optional, highly accessible)

---

## 11. Implementation Timeline

### Phase 1: Pre-Production (Week 1)
- Finalize script with accessibility in mind
- Plan visual layouts with contrast requirements
- Select colorblind-safe palette
- Create audio description script
- Choose accessible fonts

### Phase 2: Production (Week 2)
- Record voice-over at 150 WPM
- Record video with pauses for audio descriptions
- Apply accessible design (colors, fonts, contrast)
- Mix audio (voice at -6dB, music at -25dB)
- Add minimal, subtle motion

### Phase 3: Post-Production (Week 3)
- Create captions (99% accuracy)
- Create SDH with sound effects
- Record audio descriptions
- Create formatted transcript
- Test with automated tools

### Phase 4: Testing (Week 4)
- Colorblind simulation testing
- Screen reader testing
- User testing with disabled individuals
- Adjust based on feedback
- Final WCAG validation

---

## 12. Resources and Tools

### Color and Contrast
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Stark Contrast Checker](https://www.getstark.co/)
- [Color Oracle](https://colororacle.org/) (Colorblind simulator)
- [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/)

### Caption and Transcript Tools
- [Rev.com](https://www.rev.com/) (Professional captioning)
- [Otter.ai](https://otter.ai/) (Automated transcription)
- [Subtitle Edit](https://www.nikse.dk/subtitleedit) (Free caption editor)
- [Aegisub](https://aegisub.org/) (Advanced subtitle editor)

### Audio Tools
- Adobe Audition (Professional audio mixing)
- Audacity (Free audio editor with ducking)
- YouTube Audio Library (Royalty-free accessible music)

### Testing Tools
- [WAVE Browser Extension](https://wave.webaim.org/extension/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [NVDA Screen Reader](https://www.nvaccess.org/) (Free)
- [VoiceOver](https://www.apple.com/accessibility/voiceover/) (Mac/iOS built-in)

### Validation
- [WCAG Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [ADA Video Compliance Checklist](https://www.3playmedia.com/resources/compliance-checklists/ada-video-compliance/)

---

## 13. Legal and Compliance Considerations

### Applicable Standards
- **WCAG 2.1 Level AA**: Minimum legal standard (EU, many US states)
- **Section 508**: US federal accessibility standard
- **ADA Title III**: Public accommodations (includes digital content)
- **CVAA**: Video programming accessibility (US)

### Requirements by Platform
- **YouTube**: Captions required for accessibility
- **Professional sites**: WCAG 2.1 AA minimum
- **Educational content**: Often requires audio descriptions
- **Government**: Section 508 compliance mandatory

### Risk Mitigation
- Document accessibility efforts
- Keep testing records
- Provide multiple formats (video, transcript, audio-only)
- Include accessibility statement
- Respond to user feedback

---

## 14. Budget Considerations

### Cost Estimates (USD)

#### Essential (Minimum Budget: $300-500)
- Professional captions: $1-3/minute = $150-450 (for 15-min video)
- Caption editing/QA: $50-100
- Basic user testing: $100
- Tools/software: $0-50 (mostly free options available)

#### Enhanced (Recommended Budget: $800-1200)
- Professional captions: $300
- Audio descriptions: $200-400
- Professional voice-over (with descriptions): $200-300
- Comprehensive user testing: $200-300
- Professional tools: $100

#### Premium (Full Accessibility: $1500-2500)
- Everything in Enhanced
- Sign language interpretation: $500-1000
- Multiple language captions: $200-400
- Extended user testing: $300-500
- Accessibility audit: $200-300

---

## 15. Quick Reference Checklist

### Visual Design
- [ ] Color contrast 4.5:1+ for text (7:1+ for AAA)
- [ ] Blue/orange palette for colorblind users
- [ ] Patterns + color for all comparisons
- [ ] Sans-serif fonts (Roboto, Helvetica, Arial)
- [ ] 18-24px font size for body text
- [ ] 1.5x line height minimum

### Audio Design
- [ ] 150 WPM speaking pace
- [ ] Voice at -6dB, music at -25dB (20dB difference)
- [ ] Pauses: 2s between sections, 0.5s between sentences
- [ ] Ducking on background music
- [ ] Minimal sound effects

### Captions
- [ ] 99% accuracy
- [ ] White on black (or yellow on black)
- [ ] 16-20pt font size
- [ ] Speaker identification
- [ ] Sound effect descriptions
- [ ] Synchronized within 0.5s

### Transcripts
- [ ] All dialogue included
- [ ] Speaker labels bolded
- [ ] Visual descriptions added
- [ ] Sound effects noted
- [ ] Accessible format (HTML, PDF, TXT)
- [ ] Linked near video

### Audio Descriptions
- [ ] Separate audio track
- [ ] Describes essential visuals
- [ ] During natural pauses
- [ ] Clear, concise narration
- [ ] Code snippets read aloud
- [ ] Charts/graphs described

### Motion
- [ ] Minimal animations
- [ ] No parallax scrolling
- [ ] Reduced motion option
- [ ] No flashing (max 3 flashes/second)
- [ ] Subtle transitions only

### Testing
- [ ] WebAIM contrast check
- [ ] Colorblind simulator
- [ ] Screen reader test
- [ ] Caption-only viewing
- [ ] Audio-only listening
- [ ] User testing with disabled individuals

---

## Conclusion

Creating accessible video content requires intentional design from pre-production through testing. By following these guidelines, your Claude Code vs Codex comparison video will:

1. **Meet WCAG 2.1 AA standards** (and target AAA where possible)
2. **Serve users with diverse disabilities** (visual, auditory, cognitive, vestibular)
3. **Maintain professional quality** (accessibility enhances, not detracts from, design)
4. **Comply with legal requirements** (ADA, Section 508, CVAA)
5. **Reach a wider audience** (accessibility benefits everyone)

Remember: Accessibility is not a feature to be added later—it must be designed in from the beginning. The best accessible design is often invisible, seamlessly serving all users regardless of ability.

---

## Sources

### WCAG Color Contrast
- [WebAIM: Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [WebAIM: Contrast and Color Accessibility](https://webaim.org/articles/contrast/)
- [Understanding WCAG 2.1 A, AA, and AAA Guidelines for Color Contrast](https://www.accessibleresources.com/post/understanding-wcag-2-1-a-aa-and-aaa-guidelines-for-color-contrast)
- [Accessible contrast ratios and A-levels explained](https://www.getstark.co/blog/accessible-contrast-ratios-and-a-levels-explained/)

### Text Readability
- [How to Pick the Perfect Font Size: WCAG Accessibility](https://www.a11y-collective.com/blog/wcag-minimum-font-size/)
- [Understanding Accessible Fonts and Typography for Section 508 Compliance](https://www.section508.gov/develop/fonts-typography/)
- [WebAIM: Typefaces and Fonts](https://webaim.org/techniques/fonts/)
- [1.4.12 Text Spacing (AA) | WCAG 2.1](https://dequeuniversity.com/resources/wcag2.1/1.4.12-text-spacing)

### Video Accessibility for Deaf/Hard of Hearing
- [Video Accessibility Guide for Content Creators (2025)](https://www.kapwing.com/resources/video-accessibility/)
- [Digital Accessibility for the d/Deaf and Hard of Hearing](https://www.audioeye.com/post/digital-accessibility-deaf-hard-of-hearing/)
- [ADA Video Compliance: The Complete Guide for 2025](https://accessibe.com/blog/knowledgebase/ada-compliance-for-videos)
- [Making Audio and Video Media Accessible | W3C WAI](https://www.w3.org/WAI/media/av/)

### Audio Descriptions
- [Audio Description: Make Your Content Accessible for All](https://adasitecompliance.com/audio-description-accessibility/)
- [Description of Visual Information | W3C WAI](https://www.w3.org/WAI/media/av/description/)
- [Understanding Success Criterion 1.2.5: Audio Description](https://www.w3.org/WAI/WCAG21/Understanding/audio-description-prerecorded.html)
- [Audio Description is also known as Video Description](https://www.ncicap.org/audio-description)

### Colorblind Design
- [Coloring for Colorblindness](https://davidmathlogic.com/colorblind/)
- [Colorblind-Friendly Palettes: Why & How to Use in Design](https://venngage.com/blog/color-blind-friendly-palette/)
- [A Detailed Guide to Color Blind Friendly Palettes](https://visme.co/blog/color-blind-friendly-palette/)
- [10 Essential Guidelines for Colorblind Friendly Design](https://www.colorblindguide.com/post/colorblind-friendly-design-3)

### Neurodivergent Accessibility
- [Best Fonts for ADHD: Improve Readability](https://www.audioeye.com/post/best-fonts-for-adhd/)
- [Font | Neurodiversity Design](https://neurodiversity.design/principles/font/)
- [Dyslexie Font - award winning dyslexia typeface](https://dyslexiefont.com/en/)
- [How WCAG benefits everyone: A focus on neurodiversity](https://www.wcag.com/blog/digital-accessibility-and-neurodiversity/)

### Motion and Animation
- [Understanding Success Criterion 2.3.3: Animation from Interactions | W3C](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)
- [Animation and motion | web.dev](https://web.dev/learn/accessibility/motion)
- [prefers-reduced-motion - CSS | MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [Accessible motion: why it's essential and how to do it right](https://medium.com/design-ibm/accessible-motion-why-its-essential-and-how-to-do-it-right-ff38afcbc7a9)

### Technical Documentation Accessibility
- [How to Write Accessible Technical Documentation](https://www.freecodecamp.org/news/best-practices-for-writing-accessible-technical-documentation/)
- [New software enables blind users to create interactive, accessible charts](https://news.mit.edu/2024/umwelt-enables-interactive-accessible-charts-creation-blind-low-vision-users-0327)
- [Write accessible documentation | Google developer documentation](https://developers.google.com/style/accessibility)
- [11 tips for designing accessible charts for visually impaired readers](https://www.datylon.com/blog/data-visualization-for-visually-impaired-users)

### Speaking Pace
- [Average Speaking Rate and Words per Minute](https://virtualspeech.com/blog/average-speaking-rate-words-per-minute)
- [Average Words Per Minute Speaking (15 Experts Examples)](https://improvepodcast.com/words-per-minute/)
- [How Your Speaking Speed Affects What People Remember](https://tctecinnovation.com/blogs/daily-blog/how-your-speaking-speed-affects-what-people-remember)

### Audio Mixing
- [G56: Mixing audio files so that non-speech sounds are at least 20 decibels lower | W3C](https://www.w3.org/TR/WCAG20-TECHS/G56.html)
- [Voice over Background Music Best Practices](https://bunnystudio.com/blog/voice-over-background-music-best-practices/)
- [How to Perfect Your Audio Levels For Video](https://www.soundstripe.com/blogs/how-to-perfect-your-audio-levels)

### Caption Styling
- [12 Best Fonts for Subtitles and Closed Captions on Video](https://www.veed.io/learn/best-font-for-subtitles)
- [Caption Style Guide: Design Better Subtitles in 2025](https://www.capcut.com/resource/caption-style)
- [Closed Caption Styling & Formatting Best Practices](https://www.3playmedia.com/blog/closed-caption-styling-formatting-best-practices-you-need-to-know/)

### Transcripts
- [Transcripts | Web Accessibility Initiative (WAI) | W3C](https://www.w3.org/WAI/media/av/transcripts/)
- [Best Practices for Accessible Video Transcripts](https://aeldata.com/best-practices-for-accessible-video-transcripts/)
- [Best Practices for Accessible Transcripts](https://www.boia.org/blog/best-practices-for-accessible-transcripts)
