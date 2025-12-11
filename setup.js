#!/usr/bin/env node

/**
 * Production-Ready Setup Script for Video Generation Pipeline (Node.js)
 * Handles API authentication, credential management, and configuration
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const https = require('https');

// ANSI Color Codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

const API_INFO = {
  FAL_API_KEY: {
    name: 'FAL.ai',
    url: 'https://fal.ai/dashboard/keys',
    description: 'AI image & video generation',
    required: true,
    example: 'fal_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  },
  ELEVENLABS_API_KEY: {
    name: 'ElevenLabs',
    url: 'https://elevenlabs.io/app/settings/api-keys',
    description: 'Text-to-speech voice synthesis',
    required: true,
    example: 'el_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  },
  YOUTUBE_API_KEY: {
    name: 'YouTube Data API',
    url: 'https://console.cloud.google.com/apis/credentials',
    description: 'YouTube API access (read-only)',
    required: false,
    example: 'AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  },
  SHOTSTACK_API_KEY: {
    name: 'Shotstack',
    url: 'https://dashboard.shotstack.io/register',
    description: 'Video editing API',
    required: true,
    example: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  }
};

const OPTIONAL_FIELDS = {
  ELEVENLABS_VOICE_ID: {
    name: 'ElevenLabs Voice ID',
    description: 'Specific voice to use (optional)',
    default: '21m00Tcm4TlvDq8ikWAM'
  },
  SHOTSTACK_ENV: {
    name: 'Shotstack Environment',
    description: 'sandbox or v1 (production)',
    default: 'sandbox'
  },
  VIDEO_WIDTH: {
    name: 'Video Width',
    description: 'Default video width in pixels',
    default: '1920'
  },
  VIDEO_HEIGHT: {
    name: 'Video Height',
    description: 'Default video height in pixels',
    default: '1080'
  }
};

class AuthManager {
  constructor() {
    this.envPath = '.env';
    this.credentials = {};
    this.loadEnv();
  }

  loadEnv() {
    if (fs.existsSync(this.envPath)) {
      const content = fs.readFileSync(this.envPath, 'utf8');
      content.split('\n').forEach(line => {
        const match = line.match(/^([A-Z_]+)=(.*)$/);
        if (match) {
          this.credentials[match[1]] = match[2];
        }
      });
    }
  }

  getCredential(key) {
    return this.credentials[key] || process.env[key];
  }

  setCredential(key, value) {
    this.credentials[key] = value;
    this.saveEnv();
  }

  saveEnv() {
    const lines = Object.entries(this.credentials)
      .map(([key, value]) => `${key}=${value}`)
      .join('\n');
    fs.writeFileSync(this.envPath, lines + '\n');
  }

  async testFalAi() {
    const apiKey = this.getCredential('FAL_API_KEY');
    if (!apiKey) return { success: false, message: 'API key not found' };

    return new Promise((resolve) => {
      const options = {
        hostname: 'fal.run',
        path: '/fal-ai/fast-sdxl',
        method: 'GET',
        headers: {
          'Authorization': `Key ${apiKey}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      };

      const req = https.request(options, (res) => {
        if (res.statusCode === 200 || res.statusCode === 404) {
          resolve({ success: true, message: 'Authentication successful' });
        } else if (res.statusCode === 401) {
          resolve({ success: false, message: 'Invalid API key' });
        } else {
          resolve({ success: false, message: `Error: ${res.statusCode}` });
        }
      });

      req.on('error', (e) => {
        resolve({ success: false, message: `Connection error: ${e.message}` });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({ success: false, message: 'Request timeout' });
      });

      req.end();
    });
  }

  async testElevenLabs() {
    const apiKey = this.getCredential('ELEVENLABS_API_KEY');
    if (!apiKey) return { success: false, message: 'API key not found' };

    return new Promise((resolve) => {
      const options = {
        hostname: 'api.elevenlabs.io',
        path: '/v1/user',
        method: 'GET',
        headers: {
          'xi-api-key': apiKey
        },
        timeout: 10000
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          if (res.statusCode === 200) {
            try {
              const parsed = JSON.parse(data);
              const tier = parsed.subscription?.tier || 'free';
              const chars = parsed.subscription?.character_count || 0;
              resolve({ success: true, message: `Connected (Tier: ${tier}, Chars: ${chars})` });
            } catch (e) {
              resolve({ success: true, message: 'Connected' });
            }
          } else if (res.statusCode === 401) {
            resolve({ success: false, message: 'Invalid API key' });
          } else {
            resolve({ success: false, message: `Error: ${res.statusCode}` });
          }
        });
      });

      req.on('error', (e) => {
        resolve({ success: false, message: `Connection error: ${e.message}` });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({ success: false, message: 'Request timeout' });
      });

      req.end();
    });
  }

  async testYouTube() {
    const apiKey = this.getCredential('YOUTUBE_API_KEY');
    const clientId = this.getCredential('YOUTUBE_CLIENT_ID');

    if (!apiKey && !clientId) {
      return { success: false, message: 'No credentials found' };
    }

    if (!apiKey) {
      return { success: true, message: 'OAuth configured (needs full setup)' };
    }

    return new Promise((resolve) => {
      const options = {
        hostname: 'www.googleapis.com',
        path: '/youtube/v3/search?part=snippet&q=test&maxResults=1&key=' + apiKey,
        method: 'GET',
        timeout: 10000
      };

      const req = https.request(options, (res) => {
        if (res.statusCode === 200) {
          resolve({ success: true, message: 'API key valid' });
        } else if (res.statusCode === 403) {
          resolve({ success: false, message: 'Invalid API key or quota exceeded' });
        } else {
          resolve({ success: false, message: `Error: ${res.statusCode}` });
        }
      });

      req.on('error', (e) => {
        resolve({ success: false, message: `Connection error: ${e.message}` });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({ success: false, message: 'Request timeout' });
      });

      req.end();
    });
  }

  async testShotstack() {
    const apiKey = this.getCredential('SHOTSTACK_API_KEY');
    const env = this.getCredential('SHOTSTACK_ENV') || 'sandbox';

    if (!apiKey) return { success: false, message: 'API key not found' };

    const hostname = env === 'sandbox'
      ? 'api.shotstack.io'
      : 'api.shotstack.io';
    const basePath = env === 'sandbox' ? '/stage' : '/v1';

    return new Promise((resolve) => {
      const options = {
        hostname: hostname,
        path: `${basePath}/sources`,
        method: 'GET',
        headers: {
          'x-api-key': apiKey,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      };

      const req = https.request(options, (res) => {
        if (res.statusCode === 200) {
          resolve({ success: true, message: `Connected (${env} environment)` });
        } else if (res.statusCode === 401) {
          resolve({ success: false, message: 'Invalid API key' });
        } else if (res.statusCode === 403) {
          resolve({ success: false, message: 'Insufficient permissions' });
        } else {
          resolve({ success: false, message: `Error: ${res.statusCode}` });
        }
      });

      req.on('error', (e) => {
        resolve({ success: false, message: `Connection error: ${e.message}` });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({ success: false, message: 'Request timeout' });
      });

      req.end();
    });
  }

  async testAll() {
    console.log(`\n${colors.magenta}Testing API Connections...${colors.reset}\n`);

    const tests = [
      { name: 'FAL.ai', fn: () => this.testFalAi() },
      { name: 'ElevenLabs', fn: () => this.testElevenLabs() },
      { name: 'YouTube', fn: () => this.testYouTube() },
      { name: 'Shotstack', fn: () => this.testShotstack() }
    ];

    const results = {};

    for (const test of tests) {
      process.stdout.write(`${colors.cyan}Testing ${test.name}...${colors.reset} `);
      const result = await test.fn();
      results[test.name] = result;

      if (result.success) {
        console.log(`${colors.green}✓ ${result.message}${colors.reset}`);
      } else {
        console.log(`${colors.red}✗ ${result.message}${colors.reset}`);
      }
    }

    return results;
  }

  createConfigFile() {
    const config = {
      apis: {
        fal: {
          enabled: !!this.getCredential('FAL_API_KEY'),
          api_key_env: 'FAL_API_KEY',
          base_url: 'https://fal.run'
        },
        elevenlabs: {
          enabled: !!this.getCredential('ELEVENLABS_API_KEY'),
          api_key_env: 'ELEVENLABS_API_KEY',
          voice_id: this.getCredential('ELEVENLABS_VOICE_ID') || '21m00Tcm4TlvDq8ikWAM',
          base_url: 'https://api.elevenlabs.io/v1'
        },
        youtube: {
          enabled: !!(this.getCredential('YOUTUBE_API_KEY') || this.getCredential('YOUTUBE_CLIENT_ID')),
          api_key_env: 'YOUTUBE_API_KEY',
          client_id_env: 'YOUTUBE_CLIENT_ID',
          base_url: 'https://www.googleapis.com/youtube/v3'
        },
        shotstack: {
          enabled: !!this.getCredential('SHOTSTACK_API_KEY'),
          api_key_env: 'SHOTSTACK_API_KEY',
          environment: this.getCredential('SHOTSTACK_ENV') || 'sandbox',
          base_url: 'https://api.shotstack.io'
        }
      },
      settings: {
        output_dir: this.getCredential('OUTPUT_DIR') || './output',
        video_width: parseInt(this.getCredential('VIDEO_WIDTH') || '1920'),
        video_height: parseInt(this.getCredential('VIDEO_HEIGHT') || '1080'),
        video_fps: parseInt(this.getCredential('VIDEO_FPS') || '30'),
        debug: this.getCredential('DEBUG') === 'true',
        api_timeout: parseInt(this.getCredential('API_TIMEOUT') || '30'),
        max_retries: parseInt(this.getCredential('MAX_RETRIES') || '3')
      }
    };

    fs.writeFileSync('config.json', JSON.stringify(config, null, 2));
    console.log(`${colors.green}✓ Created config.json${colors.reset}`);
  }
}

// Helper function for user input
function askQuestion(query) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise(resolve => {
    rl.question(query, answer => {
      rl.close();
      resolve(answer);
    });
  });
}

async function promptApiKey(key, info) {
  console.log(`\n${colors.bright}${info.name}${colors.reset}`);
  console.log(`  Purpose: ${info.description}`);
  console.log(`  Get your key: ${colors.cyan}${info.url}${colors.reset}`);
  console.log(`  Example: ${info.example}`);

  if (info.required) {
    console.log(`  ${colors.yellow}(Required)${colors.reset}`);
  } else {
    console.log(`  ${colors.green}(Optional - press Enter to skip)${colors.reset}`);
  }

  const value = await askQuestion(`\n  Enter ${info.name} API key: `);

  if (!value && info.required) {
    console.log(`  ${colors.red}This field is required!${colors.reset}`);
    return promptApiKey(key, info);
  }

  return value.trim();
}

async function interactiveSetup() {
  console.log(`
${colors.magenta}${'='.repeat(70)}
   VIDEO GENERATION PIPELINE - SETUP WIZARD
${'='.repeat(70)}${colors.reset}

This wizard will help you configure all required API credentials.
You'll be prompted for each API key. Keys are stored in .env file.

${colors.yellow}SECURITY REMINDER:${colors.reset}
  • Never commit .env to version control
  • Keep your API keys secure
  • Use environment-specific keys for dev/prod

${colors.magenta}${'='.repeat(70)}${colors.reset}
`);

  // Check for existing .env
  if (fs.existsSync('.env')) {
    console.log(`${colors.yellow}Found existing .env file!${colors.reset}`);
    const response = await askQuestion('Do you want to (o)verwrite, (u)pdate, or (c)ancel? [o/u/c]: ');

    if (response.toLowerCase() === 'c') {
      console.log('Setup cancelled.');
      return;
    }
  } else {
    // Create from template
    if (fs.existsSync('.env.example')) {
      fs.copyFileSync('.env.example', '.env');
      console.log(`${colors.green}Created .env file from template${colors.reset}`);
    }
  }

  const manager = new AuthManager();

  // Collect required API keys
  console.log(`\n${colors.blue}${'─'.repeat(70)}`);
  console.log('  STEP 1: Required API Keys');
  console.log(`${'─'.repeat(70)}${colors.reset}\n`);

  for (const [key, info] of Object.entries(API_INFO)) {
    if (info.required) {
      const value = await promptApiKey(key, info);
      if (value) {
        manager.setCredential(key, value);
        console.log(`${colors.green}✓ Saved ${info.name}${colors.reset}`);
      }
    }
  }

  // Collect optional API keys
  console.log(`\n${colors.blue}${'─'.repeat(70)}`);
  console.log('  STEP 2: Optional API Keys');
  console.log(`${'─'.repeat(70)}${colors.reset}\n`);

  for (const [key, info] of Object.entries(API_INFO)) {
    if (!info.required) {
      const response = await askQuestion(`Configure ${info.name}? [y/N]: `);
      if (response.toLowerCase() === 'y') {
        const value = await promptApiKey(key, info);
        if (value) {
          manager.setCredential(key, value);
          console.log(`${colors.green}✓ Saved ${info.name}${colors.reset}`);
        }
      }
    }
  }

  // Collect optional configuration
  console.log(`\n${colors.blue}${'─'.repeat(70)}`);
  console.log('  STEP 3: Optional Configuration');
  console.log(`${'─'.repeat(70)}${colors.reset}\n`);

  for (const [key, info] of Object.entries(OPTIONAL_FIELDS)) {
    console.log(`${colors.bright}${info.name}${colors.reset}`);
    console.log(`  ${info.description}`);
    console.log(`  Default: ${info.default}`);
    const value = await askQuestion('  Enter value (or press Enter for default): ');
    manager.setCredential(key, value || info.default);
    console.log(`${colors.green}✓ Set ${info.name}${colors.reset}\n`);
  }

  // Test connections
  console.log(`\n${colors.blue}${'─'.repeat(70)}`);
  console.log('  STEP 4: Testing API Connections');
  console.log(`${'─'.repeat(70)}${colors.reset}`);

  const results = await manager.testAll();

  // Create config file
  console.log(`\n${colors.blue}${'─'.repeat(70)}`);
  console.log('  STEP 5: Creating Configuration File');
  console.log(`${'─'.repeat(70)}${colors.reset}\n`);

  manager.createConfigFile();

  // Final summary
  console.log(`\n${colors.blue}${'─'.repeat(70)}`);
  console.log('  SETUP COMPLETE');
  console.log(`${'─'.repeat(70)}${colors.reset}\n`);

  const total = Object.keys(results).length;
  const passed = Object.values(results).filter(r => r.success).length;

  console.log(`API Connections: ${colors.green}${passed}/${total} successful${colors.reset}\n`);

  if (passed === total) {
    console.log(`${colors.green}${'='.repeat(70)}`);
    console.log('  ✓ All API connections successful!');
    console.log('  ✓ Configuration saved to .env');
    console.log('  ✓ Pipeline configuration saved to config.json');
    console.log(`${'='.repeat(70)}${colors.reset}\n`);
    console.log(`${colors.bright}Next steps:${colors.reset}`);
    console.log('  1. Review config.json');
    console.log('  2. Test individual API calls');
    console.log('  3. Run your video generation pipeline\n');
  }
}

async function quickTest() {
  console.log(`\n${colors.magenta}Testing Existing Configuration${colors.reset}\n`);

  if (!fs.existsSync('.env')) {
    console.log(`${colors.red}No .env file found. Run setup first:${colors.reset}`);
    console.log('  node setup.js\n');
    return;
  }

  const manager = new AuthManager();
  const results = await manager.testAll();

  const total = Object.keys(results).length;
  const passed = Object.values(results).filter(r => r.success).length;

  console.log(`\n${colors.magenta}${'='.repeat(70)}${colors.reset}`);
  if (passed === total) {
    console.log(`${colors.green}All ${total} API connections successful!${colors.reset}`);
  } else if (passed > 0) {
    console.log(`${colors.yellow}${passed}/${total} API connections successful${colors.reset}`);
  } else {
    console.log(`${colors.red}No API connections successful${colors.reset}`);
  }
  console.log(`${colors.magenta}${'='.repeat(70)}${colors.reset}\n`);
}

function showHelp() {
  console.log(`
${colors.magenta}${'='.repeat(70)}
   VIDEO GENERATION PIPELINE - SETUP
${'='.repeat(70)}${colors.reset}

${colors.bright}USAGE:${colors.reset}
  node setup.js              Run interactive setup wizard
  node setup.js test         Test existing configuration
  node setup.js help         Show this help message

${colors.bright}REQUIRED APIS:${colors.reset}
  • FAL.ai: AI image & video generation
    ${colors.cyan}https://fal.ai/dashboard/keys${colors.reset}

  • ElevenLabs: Text-to-speech
    ${colors.cyan}https://elevenlabs.io/app/settings/api-keys${colors.reset}

  • Shotstack: Video editing API
    ${colors.cyan}https://dashboard.shotstack.io/register${colors.reset}

${colors.bright}FILES CREATED:${colors.reset}
  • .env              Environment variables (credentials)
  • config.json       Pipeline configuration

${colors.magenta}${'='.repeat(70)}${colors.reset}
`);
}

// Main execution
async function main() {
  const command = process.argv[2];

  if (command === 'test') {
    await quickTest();
  } else if (command === 'help') {
    showHelp();
  } else if (!command) {
    await interactiveSetup();
  } else {
    console.log(`${colors.red}Unknown command: ${command}${colors.reset}`);
    console.log("Run 'node setup.js help' for usage information.\n");
    process.exit(1);
  }
}

main().catch(error => {
  console.error(`\n${colors.red}Error: ${error.message}${colors.reset}\n`);
  process.exit(1);
});
