# Advanced: MCP Integration Guide

For users who want to integrate this pipeline with Claude Code or other tools.

## What is MCP?

**Model Context Protocol** - Allows Claude to interact directly with your Node.js scripts and data files.

Benefits:
- Claude can scrape URLs directly
- Instant feedback on dataset quality
- Automated refinements
- Integration with other tools

---

## MCP Server Setup

### 1. Create MCP Configuration

File: `.claude/mcp.json`

```json
{
  "servers": {
    "firecrawl-pipeline": {
      "command": "node",
      "args": ["mcp-server.js"],
      "env": {
        "PIPELINE_PATH": "/path/to/firecrawl-mdjsonl"
      }
    }
  }
}
```

### 2. Create MCP Server Script

File: `mcp-server.js`

```javascript
#!/usr/bin/env node

/**
 * MCP Server for Firecrawl Pipeline
 * Allows Claude Code to interact with the pipeline
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const handlers = {
  'scrape': async (url) => {
    return new Promise((resolve, reject) => {
      const proc = spawn('node', ['scrape-and-convert.js', url]);
      let output = '';
      proc.stdout.on('data', (data) => output += data);
      proc.on('close', (code) => {
        if (code === 0) {
          resolve({ success: true, output });
        } else {
          reject(new Error(`Scraping failed with code ${code}`));
        }
      });
    });
  },

  'clean': async () => {
    return new Promise((resolve, reject) => {
      const proc = spawn('node', ['clean-jsonl.js']);
      let output = '';
      proc.stdout.on('data', (data) => output += data);
      proc.on('close', (code) => {
        resolve({ success: code === 0, output });
      });
    });
  },

  'generate-video': async () => {
    return new Promise((resolve, reject) => {
      const proc = spawn('node', ['generate-video-script.js']);
      let output = '';
      proc.stdout.on('data', (data) => output += data);
      proc.on('close', (code) => {
        resolve({ success: code === 0, output });
      });
    });
  },

  'get-dataset': async () => {
    if (!fs.existsSync('dataset.jsonl')) {
      return { success: false, error: 'dataset.jsonl not found' };
    }
    const content = fs.readFileSync('dataset.jsonl', 'utf8');
    return { success: true, content };
  },

  'get-files': async () => {
    const files = fs.readdirSync('.')
      .filter(f => f.endsWith('.md') || f.endsWith('.jsonl') || f.endsWith('.json'))
      .map(f => ({
        name: f,
        size: fs.statSync(f).size,
        modified: fs.statSync(f).mtime
      }));
    return { success: true, files };
  }
};

// Simple MCP interface
console.log('MCP Server Ready');
process.on('message', async (msg) => {
  const { action, params } = msg;
  const handler = handlers[action];

  if (!handler) {
    process.send({ error: `Unknown action: ${action}` });
    return;
  }

  try {
    const result = await handler(...(params || []));
    process.send({ success: true, result });
  } catch (error) {
    process.send({ success: false, error: error.message });
  }
});
```

---

## Claude Code Integration

### Use from Claude Code

```typescript
// In your Claude Code script
const mcp = await this.createMCPConnection('firecrawl-pipeline');

// Scrape a URL
const result = await mcp.call('scrape', ['https://example.com/article']);

// Get dataset
const dataset = await mcp.call('get-dataset');

// Generate video script
const video = await mcp.call('generate-video');

// List all files
const files = await mcp.call('get-files');
```

---

## Slash Command Integration

### Create Slash Command

File: `.claude/commands/scrape.md`

```markdown
---
name: scrape
description: Scrape a URL and generate video scripts
---

Scrape this URL using the Firecrawl pipeline:

{url}

Run the full pipeline:
1. Scrape and convert to JSONL
2. Clean the dataset
3. Generate video production materials

Then summarize what was created.
```

Usage:
```bash
/scrape "https://example.com/article"
```

---

## Automated Workflow

### Example: Full Automation with Claude

```
User: "Make a video from https://example.com/article"

Claude:
1. Calls MCP: scrape(url)
2. Waits for dataset.jsonl
3. Calls MCP: clean()
4. Calls MCP: generate-video()
5. Reads all generated markdown files
6. Creates step-by-step guide for user
7. Explains what to do next
```

### Prompt for Automation

```markdown
Using the Firecrawl pipeline MCP:

1. Scrape the URL: {URL}
2. Clean the JSONL dataset
3. Generate video production materials
4. Read COMPLETE_VIDEO_SCRIPT.md
5. Create a simple 3-step guide for the user to make the video
6. Suggest which tools they should use (Canva, Pika Labs, etc.)
```

---

## Advanced: Custom MCP Tools

### Add Custom Metrics Tool

```javascript
const handlers = {
  'analyze-content': async () => {
    const data = JSON.parse(
      fs.readFileSync('dataset.jsonl', 'utf8').split('\n')[0]
    );

    return {
      title: data.title,
      wordCount: data.content.split(/\s+/).length,
      estimatedVideoLength: Math.ceil(data.content.length / 150),
      sections: data.sections.length,
      readabilityScore: calculateReadability(data.content)
    };
  }
};
```

### Use in Claude

```
Analyze the content quality of my dataset and suggest improvements.

Using the analyze-content MCP tool, check:
- Word count (should be 1500+)
- Number of sections (should be 5+)
- Readability score (target: 70+)
- Estimated video length

Then suggest improvements if needed.
```

---

## Integration with Other Tools

### With Webhook Receivers

```javascript
const express = require('express');
const app = express();

app.post('/webhook/scrape', async (req, res) => {
  const { url } = req.body;
  const result = await handlers.scrape(url);
  res.json(result);
});

app.listen(3000, () => console.log('Webhook ready'));
```

### With GitHub Actions

```yaml
name: Auto-generate video scripts

on:
  workflow_dispatch:
    inputs:
      url:
        description: 'URL to scrape'
        required: true

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: node orchestrate.js "${{ github.event.inputs.url }}"
      - uses: actions/upload-artifact@v2
        with:
          name: video-scripts
          path: '*.md'
```

---

## Security Notes

⚠️ **Important for MCP**

1. **Validate URLs**
```javascript
const url = new URL(userInput); // Throws if invalid
if (!['https:', 'http:'].includes(url.protocol)) throw new Error('Invalid protocol');
```

2. **Sandbox file operations**
```javascript
const allowedPath = path.resolve('/safe/directory');
const userPath = path.resolve(userInput);
if (!userPath.startsWith(allowedPath)) throw new Error('Path outside allowed directory');
```

3. **Rate limiting**
```javascript
const limiter = new RateLimiter({ points: 5, duration: 3600 }); // 5 per hour
await limiter.consume(1);
```

---

## Testing MCP Connection

```bash
# Test the server
node -e "
const cp = require('child_process');
const server = cp.fork('mcp-server.js');

server.send({ action: 'get-files' });
server.on('message', (msg) => {
  console.log('MCP Response:', msg);
  process.exit(0);
});
"
```

---

## Troubleshooting MCP

**Issue: "MCP server not responding"**
```bash
# Check if server is running
ps aux | grep mcp-server

# Restart Claude Code
# Verify .claude/mcp.json exists
```

**Issue: "Permission denied"**
```bash
# Make scripts executable
chmod +x mcp-server.js
chmod +x *.js
```

**Issue: "Cannot find module"**
```bash
# From the MCP server directory
npm install
```

---

## Example: Automated Batch Processing

```javascript
// batch-process.js
const fs = require('fs');
const urls = fs.readFileSync('urls.txt', 'utf8').split('\n');

for (const url of urls) {
  if (!url.trim()) continue;

  console.log(`Processing: ${url}`);
  await orchestrate(url);
  await new Promise(r => setTimeout(r, 5000)); // Rate limit
}
```

Run:
```bash
node batch-process.js
```

---

## Production Deployment

### Docker

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .

ENV PIPELINE_PATH=/app
EXPOSE 3000

CMD ["node", "mcp-server.js"]
```

Build and run:
```bash
docker build -t firecrawl-pipeline .
docker run -p 3000:3000 firecrawl-pipeline
```

---

## More Resources

- MCP Spec: https://modelcontextprotocol.io/
- Claude Code Docs: https://claude.com/claude-code
- Node.js Child Process: https://nodejs.org/api/child_process.html

---

**Tip:** For most users, the basic scripts are sufficient. MCP is for advanced automation and integration.
