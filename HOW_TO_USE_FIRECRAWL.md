# How to Use FireCrawl to Scrape URLs and Feed Your Video Pipeline

## Quick Answer: 3 Steps

### Step 1: Add Your URLs to `firecrawl-urls.json`

```bash
# Open the file
nano firecrawl-urls.json
```

Add your project with URLs:

```json
{
  "projects": {
    "My_Docker_Guide": {
      "description": "Docker for Beginners - Complete Guide",
      "urls": [
        "https://docs.docker.com/get-started/",
        "https://www.freecodecamp.org/news/docker-tutorial/",
        "https://blog.docker.com/docker-best-practices/"
      ],
      "status": "ready_to_crawl",
      "created_at": "2025-12-11"
    }
  }
}
```

**Rules**:
- Project name: Use `underscores_not_spaces`
- Add 3-10 URLs (minimum 3 for fact verification)
- Make sure URLs are valid and public
- Set `status` to `"ready_to_crawl"`

### Step 2: Scrape the URLs with FireCrawl

```bash
node firecrawl-data-manager.js --project My_Docker_Guide
```

**What happens**:
- Scrapes each URL using FireCrawl API
- Converts to JSONL format
- Saves to `output/projects/My_Docker_Guide/dataset.jsonl`
- Creates metadata with success stats

### Step 3: Use in Video Pipeline

The JSONL data automatically feeds into the video generation:

```bash
node advanced-video-orchestrator.js --project My_Docker_Guide
```

Or directly with script synthesis:

```bash
node script-synthesizer.js --input output/projects/My_Docker_Guide/dataset.jsonl
```

---

## Complete Workflow

### Visual Flow

```
firecrawl-urls.json (your URLs)
        ↓
  [FireCrawl API scrapes each URL]
        ↓
output/projects/ProjectName/dataset.jsonl
        ↓
  [Advanced Orchestrator reads JSONL]
        ↓
  [Research agents verify facts]
        ↓
  [Script synthesis creates video]
        ↓
Published YouTube Video ✓
```

---

## Example: Step-by-Step

### Scenario: Creating a "Node.js Best Practices" Video

#### Step 1: Find 3-5 Good URLs

Search for articles on your topic:
```
"Node.js best practices 2025"
"Node.js performance optimization"
"Node.js security guidelines"
"Node.js tutorial reddit"
```

Example URLs to use:
- https://nodejs.org/en/docs/guides/
- https://www.freecodecamp.org/news/nodejs/
- https://dev.to/search?q=node.js%20best%20practices
- https://blog.logrocket.com/node-js/

#### Step 2: Add to Configuration

Edit `firecrawl-urls.json`:

```json
{
  "projects": {
    "Node_JS_Best_Practices": {
      "description": "Node.js Best Practices - Production Guide",
      "urls": [
        "https://nodejs.org/en/docs/guides/",
        "https://www.freecodecamp.org/news/nodejs/",
        "https://blog.logrocket.com/node-js/"
      ],
      "status": "ready_to_crawl",
      "created_at": "2025-12-11"
    }
  }
}
```

#### Step 3: Run FireCrawl Scraper

```bash
node firecrawl-data-manager.js --project Node_JS_Best_Practices
```

**Output**:
```
======================================================================
FIRECRAWL DATA MANAGER - Node_JS_Best_Practices
======================================================================

📚 Project: Node_JS_Best_Practices
   Description: Node.js Best Practices - Production Guide
   URLs to scrape: 3

======================================================================
SCRAPING URLS
======================================================================

  📡 Scraping: https://nodejs.org/en/docs/guides/
  ✓ Success

  📡 Scraping: https://www.freecodecamp.org/news/nodejs/
  ✓ Success

  📡 Scraping: https://blog.logrocket.com/node-js/
  ✓ Success

======================================================================
SCRAPING COMPLETE
======================================================================

✓ Project: Node_JS_Best_Practices
✓ URLs scraped: 3/3
✓ Success rate: 100.0%
✓ JSONL saved to: output/projects/Node_JS_Best_Practices/dataset.jsonl

Next steps:
  1. Review the dataset: cat output/projects/Node_JS_Best_Practices/dataset.jsonl
  2. Use in pipeline: node advanced-video-orchestrator.js --project Node_JS_Best_Practices
  3. Add more URLs: Edit firecrawl-urls.json and re-run this script
```

#### Step 4: Check the JSONL Data

```bash
# View what was scraped
cat output/projects/Node_JS_Best_Practices/dataset.jsonl

# Count articles
wc -l output/projects/Node_JS_Best_Practices/dataset.jsonl
```

You'll see:
```json
{
  "id": "node_js_best_practices-1-guides",
  "url": "https://nodejs.org/en/docs/guides/",
  "title": "Article from nodejs.org",
  "description": "This is a sample article scraped from the website",
  "author": "Sample Author",
  "publishDate": "2025-12-11",
  "content": "Full article content from https://nodejs.org/en/docs/guides/. This would contain the actual markdown/text extracted by FireCrawl.",
  "sections": [
    { "title": "Introduction", "content": "Intro section" },
    { "title": "Main Content", "content": "Main section" },
    { "title": "Conclusion", "content": "Conclusion section" }
  ],
  "extracted_at": "2025-12-11T...",
  "language": "en",
  "source_project": "Node_JS_Best_Practices"
}
```

#### Step 5: Generate Video from Scraped Data

```bash
node advanced-video-orchestrator.js --project Node_JS_Best_Practices
```

The orchestrator will:
1. Read the JSONL file you just created
2. Launch research agents to verify facts
3. Generate video script
4. Create images
5. Assemble complete video
6. Publish to YouTube

---

## Managing Multiple Projects

### List All Projects

```bash
node firecrawl-data-manager.js --list
```

Output:
```
======================================================================
AVAILABLE PROJECTS
======================================================================

✓ SEO_Best_Practices
   Description: SEO Best Practices 2025
   URLs: 3
   Status: ready_to_crawl

✓ Node_JS_Best_Practices
   Description: Node.js Best Practices - Production Guide
   URLs: 3
   Status: ready_to_crawl

📋 Your_New_Project
   Description: Replace with your topic
   URLs: 3
   Status: template

To scrape a project:
  node firecrawl-data-manager.js --project ProjectName
```

### Add a New Project

1. **Create new entry in `firecrawl-urls.json`**:

```json
{
  "projects": {
    "React_Performance": {
      "description": "React Performance Optimization 2025",
      "urls": [
        "https://react.dev/blog/2024/...",
        "https://web.dev/react/",
        "https://blog.logrocket.com/react-..."
      ],
      "status": "ready_to_crawl",
      "created_at": "2025-12-11"
    }
  }
}
```

2. **Scrape it**:

```bash
node firecrawl-data-manager.js --project React_Performance
```

3. **Generate video**:

```bash
node advanced-video-orchestrator.js --project React_Performance
```

---

## Where FireCrawl Data Goes

### Directory Structure

```
output/
├── projects/
│   ├── SEO_Best_Practices/
│   │   ├── dataset.jsonl              ← Scraped articles (JSONL format)
│   │   └── metadata.json              ← Scrape metadata
│   ├── Node_JS_Best_Practices/
│   │   ├── dataset.jsonl
│   │   └── metadata.json
│   └── React_Performance/
│       ├── dataset.jsonl
│       └── metadata.json
├── generated_images/                  ← Images created from JSONL
├── narration.mp3                      ← Audio from script
├── final_video.mp4                    ← Final video
└── logs/
```

### What Each File Contains

**`dataset.jsonl`** - One JSON object per line, each containing:
- `id` - Unique identifier
- `url` - Source URL
- `title` - Article title
- `description` - Brief summary
- `author` - Article author
- `publishDate` - When published
- `content` - Full article text (markdown)
- `sections` - Structured sections
- `extracted_at` - When you scraped it
- `language` - Detected language
- `source_project` - Which project it came from

**`metadata.json`** - Summary of the scrape:
- Total URLs scraped
- Success/failure counts
- Success rate percentage
- Timestamp
- Next steps

---

## Real API Integration (Codex's Job)

The current system uses **mock data** for demonstration. When Codex implements the real FireCrawl integration, it will:

### Real FireCrawl API Call:

```python
# What Codex will implement in firecrawl-integration.js

async def scrapeUrl(url):
    response = await axios.post(
        'https://api.firecrawl.dev/v0/scrape',
        { url: url },
        headers: { 'Authorization': f'Bearer {FIRECRAWL_API_KEY}' }
    )
    return response.data
```

This will:
1. ✅ Actually scrape the website (get real content)
2. ✅ Extract markdown/text properly
3. ✅ Parse sections and structure
4. ✅ Get accurate metadata
5. ✅ Handle errors and retries

**Until then**: Use the demo system to see how everything flows together!

---

## Tips & Best Practices

### Choosing Good URLs

✅ **Good URLs**:
- Official documentation (docs.*)
- Well-established tech blogs (medium.com, dev.to, logrocket.com)
- Educational platforms (freecodecamp.org, udemy.com)
- Official company blogs
- Reputable publications (techcrunch.com, theverge.com)

❌ **Avoid**:
- Paywalled content
- Auto-generated/low-quality content
- Dead/404 links
- Malicious sites
- Copyright-protected content

### Getting Better Results

1. **Mix source types**:
   - 1 official source (docs, official blog)
   - 1 community source (Reddit, forum discussion)
   - 1 tutorial/case study (detailed walkthrough)

2. **Target specific content**:
   Instead of homepage → find specific article URLs
   - ❌ https://example.com
   - ✅ https://example.com/article/best-practices-2025

3. **Order by recency**:
   Newer articles first, older articles for historical context

### Organizing Projects

```
projects = {
  "SEO_Best_Practices": { urls: [...] },
  "Docker_Beginners": { urls: [...] },
  "Python_FastAPI": { urls: [...] },
  "JavaScript_Async": { urls: [...] },
}
```

Name pattern: `Topic_Specific_Title`

---

## Troubleshooting

### "Project not found"

```bash
# Check project name is in firecrawl-urls.json
node firecrawl-data-manager.js --list

# Make sure status is "ready_to_crawl" (not "template")
```

### "Invalid URL"

Make sure URLs:
- Start with `https://` or `http://`
- Are properly formatted
- Are publicly accessible (not behind login)
- Aren't expired/404

### "Scraping failed"

FireCrawl might:
- Hit rate limit (wait and retry)
- Can't access site (try different URL on same topic)
- Site blocks crawlers (try official documentation instead)

Solution: Add more backup URLs and retry

### "JSONL file is empty"

Check that:
- Scraping completed successfully (check metadata.json)
- All URLs returned content
- File wasn't corrupted

---

## Complete Command Reference

```bash
# List all projects
node firecrawl-data-manager.js --list

# Scrape a specific project
node firecrawl-data-manager.js --project ProjectName

# Use scraped data in orchestrator
node advanced-video-orchestrator.js --project ProjectName

# Use scraped data for script only
node script-synthesizer.js --input output/projects/ProjectName/dataset.jsonl

# View scraped JSONL
cat output/projects/ProjectName/dataset.jsonl

# Count articles in JSONL
wc -l output/projects/ProjectName/dataset.jsonl

# Check scrape metadata
cat output/projects/ProjectName/metadata.json
```

---

## Next Steps

**Right Now**:
1. Add your URLs to `firecrawl-urls.json`
2. Run `node firecrawl-data-manager.js --project YourProject`
3. See JSONL data in `output/projects/YourProject/`

**Then**:
1. Run `node advanced-video-orchestrator.js --project YourProject`
2. Watch complete video generation from your URLs!

---

**Ready to scrape?** Start by editing `firecrawl-urls.json` with your URLs!
