#!/usr/bin/env node

/**
 * PART 1 & 2 & 3: Scrape with Firecrawl, Save JSON, Convert to JSONL
 *
 * Usage:
 *   node scrape-and-convert.js <URL>
 *   node scrape-and-convert.js https://www.nathanonn.com/claude-code-vs-codex-why-i-use-both-and-you-should-too/
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// Hardcoded default URL
const DEFAULT_URL = 'https://www.nathanonn.com/claude-code-vs-codex-why-i-use-both-and-you-should-too/';

function getUrlSlug(url) {
  try {
    const urlObj = new URL(url);
    let slug = urlObj.pathname.split('/').filter(p => p).pop() || 'page';
    slug = slug.replace(/[^a-z0-9-]/gi, '').toLowerCase();
    return slug || 'page';
  } catch {
    return 'extracted-content';
  }
}

function sanitizeMarkdown(markdown) {
  if (!markdown) return '';

  // Remove excessive blank lines
  markdown = markdown.replace(/\n\n\n+/g, '\n\n');

  // Fix common markdown issues
  markdown = markdown.replace(/\*{4,}/g, '**'); // Fix multiple bold markers
  markdown = markdown.replace(/_{2,}/g, '_'); // Fix underscores

  return markdown.trim();
}

function generateId(url, title) {
  const slug = getUrlSlug(url);
  const titleSlug = (title || 'doc')
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .slice(0, 30);
  return `${titleSlug}-${slug}`.replace(/-+/g, '-');
}

async function fetchWithHttp(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`Failed to parse JSON response: ${e.message}`));
        }
      });
    }).on('error', reject);
  });
}

async function scrapeWithFirecrawl(url) {
  console.log(`📡 Scraping ${url}...`);

  try {
    // Fallback: Basic HTTP fetch and HTML parsing
    console.log('   Using direct HTTP fetch (no API required)...');

    return new Promise((resolve, reject) => {
      const client = url.startsWith('https') ? https : http;

      client.get(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        timeout: 10000
      }, (res) => {
        let html = '';
        res.on('data', chunk => html += chunk);
        res.on('end', () => {
          try {
            // Extract title
            const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
            const title = titleMatch ? titleMatch[1].trim() : 'Extracted Content';

            // Extract meta description
            const descMatch = html.match(/<meta\s+name=['"]description['"][^>]*content=['"]([^'"]+)['"]/i);
            const description = descMatch ? descMatch[1] : '';

            // Extract main content (simplified)
            const contentMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i) ||
                                 html.match(/<article[^>]*>([\s\S]*?)<\/article>/i) ||
                                 html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);

            let content = contentMatch ? contentMatch[1] : html;

            // Remove script and style tags
            content = content.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
            content = content.replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '');

            // Convert HTML to simple markdown
            content = content.replace(/<h[1-6][^>]*>([^<]*)<\/h[1-6]>/gi, '\n## $1\n');
            content = content.replace(/<p[^>]*>([^<]*)<\/p>/gi, '$1\n\n');
            content = content.replace(/<li[^>]*>([^<]*)<\/li>/gi, '- $1\n');
            content = content.replace(/<br\s*\/?>/gi, '\n');
            content = content.replace(/<[^>]+>/g, '');
            content = content.replace(/&nbsp;/g, ' ');
            content = content.replace(/&amp;/g, '&');
            content = content.replace(/&lt;/g, '<');
            content = content.replace(/&gt;/g, '>');
            content = content.replace(/&quot;/g, '"');

            resolve({
              url: url,
              title: title,
              description: description,
              markdown: content.trim(),
              metadata: {
                title: title,
                description: description,
                source: 'direct-html-parse'
              },
              sections: []
            });
          } catch (e) {
            reject(new Error(`Failed to parse HTML: ${e.message}`));
          }
        });
      }).on('error', reject).on('timeout', function() {
        this.destroy();
        reject(new Error('Request timeout'));
      });
    });
  } catch (error) {
    console.error('❌ Scraping failed:', error.message);
    throw error;
  }
}

async function convertToJsonl(jsonData, url) {
  console.log('🔄 Converting to JSONL format...');

  const title = jsonData.metadata?.title || jsonData.title || 'Extracted Content';
  const markdown = sanitizeMarkdown(jsonData.markdown || jsonData.content || jsonData.text || '');
  const sections = jsonData.sections || [];

  const jsonlObject = {
    id: generateId(url, title),
    url: url,
    title: title,
    description: jsonData.metadata?.description || '',
    author: jsonData.metadata?.author || '',
    publishDate: jsonData.metadata?.publishDate || '',
    content: markdown,
    sections: sections,
    extracted_at: new Date().toISOString(),
    language: jsonData.metadata?.language || 'en'
  };

  return jsonlObject;
}

async function main() {
  const url = process.argv[2] || DEFAULT_URL;

  console.log('═══════════════════════════════════════════════════');
  console.log('   Firecrawl → JSON → JSONL Pipeline');
  console.log('═══════════════════════════════════════════════════\n');

  try {
    // Step 1: Scrape
    const rawData = await scrapeWithFirecrawl(url);

    // Step 2: Save raw JSON
    const slug = getUrlSlug(url);
    const jsonFile = `${slug}.json`;
    fs.writeFileSync(jsonFile, JSON.stringify(rawData, null, 2));
    console.log(`✅ Saved raw JSON: ${jsonFile}`);

    // Step 3: Convert to JSONL
    const jsonlObject = await convertToJsonl(rawData, url);
    const jsonlFile = `${slug}.jsonl`;
    fs.writeFileSync(jsonlFile, JSON.stringify(jsonlObject) + '\n');
    console.log(`✅ Saved JSONL: ${jsonlFile}`);

    // Step 4: Also save as dataset.jsonl for compatibility
    fs.writeFileSync('dataset.jsonl', JSON.stringify(jsonlObject) + '\n');
    console.log(`✅ Saved as: dataset.jsonl (for video script generation)`);

    console.log('\n═══════════════════════════════════════════════════');
    console.log('   Summary');
    console.log('═══════════════════════════════════════════════════');
    console.log(`Title: ${jsonlObject.title}`);
    console.log(`Content length: ${jsonlObject.content.length} characters`);
    console.log(`Sections: ${jsonlObject.sections.length}`);
    console.log(`\nNext step: node generate-video-script.js`);

  } catch (error) {
    console.error('❌ Pipeline failed:', error.message);
    process.exit(1);
  }
}

main();
