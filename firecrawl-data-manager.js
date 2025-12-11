#!/usr/bin/env node
/**
 * FireCrawl Data Manager
 *
 * Manages FireCrawl URL scraping and JSONL conversion
 * - Reads URLs from firecrawl-urls.json
 * - Scrapes using FireCrawl API
 * - Converts to JSONL format
 * - Organizes by project in output/projects/
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

class FireCrawlDataManager {
  constructor() {
    this.apiKey = process.env.FIRECRAWL_API_KEY;
    this.baseUrl = 'https://api.firecrawl.dev/v0';
    this.urlsConfigPath = './firecrawl-urls.json';
    this.outputBaseDir = './output/projects';
  }

  /**
   * Load URLs from config file
   */
  loadUrlsConfig() {
    console.log('[CONFIG] Loading FireCrawl URLs configuration...\n');

    try {
      const config = JSON.parse(fs.readFileSync(this.urlsConfigPath, 'utf8'));
      return config.projects;
    } catch (error) {
      console.error('❌ Error loading firecrawl-urls.json:', error.message);
      console.log('\n📋 Create the file first with sample projects');
      process.exit(1);
    }
  }

  /**
   * Scrape single URL using FireCrawl API
   */
  async scrapeUrl(url, retries = 3) {
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        console.log(`  📡 Scraping: ${url}`);

        // In production: Call actual FireCrawl API
        // const response = await axios.post(
        //   `${this.baseUrl}/scrape`,
        //   { url },
        //   { headers: { 'Authorization': `Bearer ${this.apiKey}` } }
        // );

        // For MVP: Simulate successful scrape with mock data
        const mockData = await this.getMockScrapedData(url);

        console.log(`  ✓ Success\n`);
        return mockData;
      } catch (error) {
        if (attempt < retries) {
          const backoff = Math.pow(2, attempt - 1) * 1000;
          console.log(`  ⚠️  Attempt ${attempt} failed, retrying in ${backoff}ms...`);
          await new Promise(resolve => setTimeout(resolve, backoff));
        } else {
          console.log(`  ❌ Failed after ${retries} attempts: ${error.message}\n`);
          return null;
        }
      }
    }
  }

  /**
   * Mock scraped data (replace with real API calls)
   */
  async getMockScrapedData(url) {
    // In production: This would be real API response data
    return {
      url,
      title: `Article from ${new URL(url).hostname}`,
      description: 'This is a sample article scraped from the website',
      author: 'Sample Author',
      publishDate: new Date().toISOString().split('T')[0],
      content: `Full article content from ${url}. This would contain the actual markdown/text extracted by FireCrawl.`,
      sections: [
        { title: 'Introduction', content: 'Intro section' },
        { title: 'Main Content', content: 'Main section' },
        { title: 'Conclusion', content: 'Conclusion section' }
      ],
      metadata: {
        domain: new URL(url).hostname,
        language: 'en',
      }
    };
  }

  /**
   * Convert scraped data to JSONL format
   */
  convertToJsonl(scrapedData, projectName) {
    console.log('[CONVERT] Converting to JSONL format...\n');

    const jsonlLines = scrapedData
      .filter(item => item !== null) // Remove failed scrapes
      .map((item, index) => {
        const jsonlItem = {
          id: `${projectName.toLowerCase()}-${index + 1}-${item.url.split('/').pop() || 'page'}`,
          url: item.url,
          title: item.title,
          description: item.description,
          author: item.author || 'Unknown',
          publishDate: item.publishDate || new Date().toISOString().split('T')[0],
          content: item.content,
          sections: item.sections || [],
          extracted_at: new Date().toISOString(),
          language: item.metadata?.language || 'en',
          source_project: projectName,
        };
        return JSON.stringify(jsonlItem);
      })
      .join('\n');

    return jsonlLines;
  }

  /**
   * Save JSONL to file
   */
  saveJsonl(jsonlContent, projectName) {
    console.log('[SAVE] Saving JSONL file...\n');

    const projectDir = path.join(this.outputBaseDir, projectName);
    const jsonlPath = path.join(projectDir, 'dataset.jsonl');

    // Create directories if they don't exist
    fs.mkdirSync(projectDir, { recursive: true });

    // Write JSONL file
    fs.writeFileSync(jsonlPath, jsonlContent);

    console.log(`✓ Saved to: ${jsonlPath}\n`);

    return jsonlPath;
  }

  /**
   * Save metadata about the scrape
   */
  saveMetadata(projectName, urls, results) {
    const metadata = {
      project: projectName,
      timestamp: new Date().toISOString(),
      urls_requested: urls.length,
      urls_successful: results.filter(r => r !== null).length,
      urls_failed: results.filter(r => r === null).length,
      success_rate: `${(results.filter(r => r !== null).length / urls.length * 100).toFixed(1)}%`,
      dataFile: `output/projects/${projectName}/dataset.jsonl`,
      nextSteps: [
        `1. Review the dataset: cat output/projects/${projectName}/dataset.jsonl`,
        `2. Use in pipeline: node advanced-video-orchestrator.js --project ${projectName}`,
        `3. Add more URLs: Edit firecrawl-urls.json and re-run this script`,
      ]
    };

    const metadataPath = path.join(this.outputBaseDir, projectName, 'metadata.json');
    fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));

    return metadata;
  }

  /**
   * List all available projects
   */
  listProjects() {
    const config = this.loadUrlsConfig();

    console.log('='.repeat(70));
    console.log('AVAILABLE PROJECTS');
    console.log('='.repeat(70) + '\n');

    Object.entries(config).forEach(([name, project]) => {
      const status = project.status === 'template' ? '📋' : '✓';
      console.log(`${status} ${name}`);
      console.log(`   Description: ${project.description}`);
      console.log(`   URLs: ${project.urls.length}`);
      console.log(`   Status: ${project.status}\n`);
    });

    console.log('To scrape a project:');
    console.log('  node firecrawl-data-manager.js --project ProjectName\n');

    console.log('To add new URLs:');
    console.log('  1. Edit firecrawl-urls.json');
    console.log('  2. Add your project and URLs');
    console.log('  3. Run this script with --project flag\n');
  }

  /**
   * Main execution
   */
  async execute(projectName) {
    console.log('\n' + '='.repeat(70));
    console.log(`FIRECRAWL DATA MANAGER - ${projectName}`);
    console.log('='.repeat(70) + '\n');

    // Load config
    const projects = this.loadUrlsConfig();

    if (!projects[projectName]) {
      console.error(`❌ Project "${projectName}" not found in firecrawl-urls.json\n`);
      this.listProjects();
      process.exit(1);
    }

    const project = projects[projectName];

    if (project.status === 'template') {
      console.error(`❌ Project "${projectName}" is still a template.\n`);
      console.log('Update firecrawl-urls.json with your URLs and set status to "ready_to_crawl"\n');
      process.exit(1);
    }

    console.log(`📚 Project: ${projectName}`);
    console.log(`   Description: ${project.description}`);
    console.log(`   URLs to scrape: ${project.urls.length}\n`);

    // Scrape all URLs
    console.log('='.repeat(70));
    console.log('SCRAPING URLS');
    console.log('='.repeat(70) + '\n');

    const scrapedData = [];
    for (const url of project.urls) {
      const data = await this.scrapeUrl(url);
      scrapedData.push(data);
    }

    // Convert to JSONL
    console.log('='.repeat(70));
    const jsonlContent = this.convertToJsonl(scrapedData, projectName);

    // Save JSONL
    console.log('='.repeat(70));
    const jsonlPath = this.saveJsonl(jsonlContent, projectName);

    // Save metadata
    const metadata = this.saveMetadata(projectName, project.urls, scrapedData);

    // Summary
    console.log('='.repeat(70));
    console.log('SCRAPING COMPLETE');
    console.log('='.repeat(70) + '\n');

    console.log(`✓ Project: ${projectName}`);
    console.log(`✓ URLs scraped: ${metadata.urls_successful}/${metadata.urls_requested}`);
    console.log(`✓ Success rate: ${metadata.success_rate}`);
    console.log(`✓ JSONL saved to: ${jsonlPath}\n`);

    console.log('Next steps:');
    metadata.nextSteps.forEach((step, i) => {
      console.log(`  ${step}`);
    });

    console.log();
    return metadata;
  }
}

/**
 * CLI Interface
 */
async function main() {
  const args = process.argv.slice(2);
  const manager = new FireCrawlDataManager();

  if (args.length === 0 || args[0] === '--list') {
    manager.listProjects();
    process.exit(0);
  }

  if (args[0] === '--project' && args[1]) {
    const projectName = args[1];
    await manager.execute(projectName);
  } else {
    console.log('Usage:');
    console.log('  node firecrawl-data-manager.js --list                    (List all projects)');
    console.log('  node firecrawl-data-manager.js --project ProjectName     (Scrape a project)\n');
    console.log('Example:');
    console.log('  node firecrawl-data-manager.js --project SEO_Best_Practices\n');
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
}

module.exports = FireCrawlDataManager;
