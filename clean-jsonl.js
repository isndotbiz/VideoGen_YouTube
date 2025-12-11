#!/usr/bin/env node

/**
 * PART 4: Clean JSONL for AI Ingestion
 *
 * Fixes:
 * - Broken markdown formatting
 * - Excessive whitespace
 * - Malformed sections
 * - Special character encoding
 * - Logical structure
 *
 * Usage:
 *   node clean-jsonl.js
 *   node clean-jsonl.js dataset.jsonl
 */

const fs = require('fs');

function cleanMarkdown(markdown) {
  if (!markdown || typeof markdown !== 'string') return '';

  let cleaned = markdown;

  // Remove control characters except newlines and tabs
  cleaned = cleaned.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '');

  // Fix broken unicode
  cleaned = cleaned.replace(/\u00a0+/g, ' '); // Non-breaking spaces
  cleaned = cleaned.replace(/\u200b/g, ''); // Zero-width spaces

  // Fix multiple spaces
  cleaned = cleaned.replace(/ {2,}/g, ' ');

  // Remove excessive blank lines
  cleaned = cleaned.replace(/\n\n\n+/g, '\n\n');

  // Fix markdown headers
  cleaned = cleaned.replace(/^([^\n#]+)#+\s+/gm, '$1'); // Remove stray hashes
  cleaned = cleaned.replace(/^#+\s{2,}/gm, '#'); // Fix header spacing

  // Fix bold/italic
  cleaned = cleaned.replace(/\*{2,}([^\*]+)\*{2,}/g, '**$1**'); // Multiple asterisks
  cleaned = cleaned.replace(/_+([^_]+)_+/g, '_$1_'); // Multiple underscores

  // Fix links
  cleaned = cleaned.replace(/\[([^\]]+)\]\s*\(\s*([^)]+)\s*\)/g, '[$1]($2)');

  // Fix code blocks
  cleaned = cleaned.replace(/```\s+/g, '```\n');
  cleaned = cleaned.replace(/\s+```/g, '\n```');

  // Remove trailing whitespace from lines
  cleaned = cleaned.split('\n').map(line => line.trimEnd()).join('\n');

  // Remove leading/trailing whitespace overall
  cleaned = cleaned.trim();

  return cleaned;
}

function restructureSections(sections) {
  if (!Array.isArray(sections)) return [];

  return sections
    .filter(s => s && typeof s === 'object')
    .map(section => ({
      heading: (section.heading || section.title || section.name || '').trim(),
      content: cleanMarkdown(section.content || section.text || section.body || ''),
      level: section.level || 2,
      subsections: Array.isArray(section.subsections) ? section.subsections.length : 0
    }))
    .filter(s => s.heading || s.content); // Only keep non-empty sections
}

function validateJsonl(jsonlObject) {
  const errors = [];
  const warnings = [];

  // Required fields
  if (!jsonlObject.id) errors.push('Missing required field: id');
  if (!jsonlObject.title) errors.push('Missing required field: title');
  if (!jsonlObject.url) errors.push('Missing required field: url');

  // Data quality
  if (!jsonlObject.content || typeof jsonlObject.content !== 'string') {
    errors.push('Missing or invalid content field');
  }
  if (jsonlObject.content && jsonlObject.content.length < 100) {
    warnings.push('Content is very short (< 100 characters)');
  }
  if (jsonlObject.content && jsonlObject.content.length > 1000000) {
    warnings.push('Content is very large (> 1MB)');
  }

  // Metadata
  if (!jsonlObject.extracted_at) warnings.push('Missing extraction timestamp');
  if (!jsonlObject.language) warnings.push('Missing language field');

  return { errors, warnings };
}

async function cleanJsonlFile(filename) {
  console.log(`📝 Reading: ${filename}`);

  if (!fs.existsSync(filename)) {
    throw new Error(`File not found: ${filename}`);
  }

  const content = fs.readFileSync(filename, 'utf8').trim();
  const lines = content.split('\n').filter(line => line.trim());

  console.log(`📊 Processing ${lines.length} JSONL line(s)...`);

  const cleaned = lines.map((line, idx) => {
    try {
      const obj = JSON.parse(line);

      return {
        id: (obj.id || `doc-${idx + 1}`).toLowerCase().replace(/[^a-z0-9-]/g, ''),
        url: obj.url || '',
        title: (obj.title || '').trim(),
        description: (obj.description || '').trim(),
        author: (obj.author || '').trim(),
        publishDate: obj.publishDate || '',
        language: obj.language || 'en',
        content: cleanMarkdown(obj.content),
        sections: restructureSections(obj.sections),
        extracted_at: obj.extracted_at || new Date().toISOString(),
        word_count: (obj.content || '').split(/\s+/).length,
        char_count: (obj.content || '').length
      };
    } catch (e) {
      console.warn(`⚠️  Line ${idx + 1}: Invalid JSON, skipping`);
      return null;
    }
  }).filter(Boolean);

  console.log(`✅ Cleaned ${cleaned.length} record(s)`);

  // Save cleaned version
  const outputFile = `${filename}.cleaned`;
  fs.writeFileSync(
    outputFile,
    cleaned.map(obj => JSON.stringify(obj)).join('\n') + '\n'
  );

  // Validate
  let totalErrors = 0;
  let totalWarnings = 0;

  cleaned.forEach((obj, idx) => {
    const { errors, warnings } = validateJsonl(obj);
    if (errors.length > 0) {
      console.error(`❌ Record ${idx + 1} errors:`);
      errors.forEach(e => console.error(`   - ${e}`));
      totalErrors += errors.length;
    }
    if (warnings.length > 0) {
      console.warn(`⚠️  Record ${idx + 1} warnings:`);
      warnings.forEach(w => console.warn(`   - ${w}`));
      totalWarnings += warnings.length;
    }
  });

  // Save validation report
  const report = {
    file: filename,
    records_processed: cleaned.length,
    total_errors: totalErrors,
    total_warnings: totalWarnings,
    timestamp: new Date().toISOString(),
    records: cleaned.map(obj => ({
      id: obj.id,
      title: obj.title,
      word_count: obj.word_count,
      char_count: obj.char_count,
      sections: obj.sections.length
    }))
  };

  fs.writeFileSync(
    'clean-report.json',
    JSON.stringify(report, null, 2)
  );

  console.log('\n═══════════════════════════════════════════════════');
  console.log('   Cleaning Complete');
  console.log('═══════════════════════════════════════════════════');
  console.log(`Cleaned file: ${outputFile}`);
  console.log(`Report: clean-report.json`);
  console.log(`\nStats:`);
  console.log(`  Records: ${cleaned.length}`);
  console.log(`  Errors: ${totalErrors}`);
  console.log(`  Warnings: ${totalWarnings}`);

  return { cleaned, report };
}

async function main() {
  const filename = process.argv[2] || 'dataset.jsonl';

  console.log('═══════════════════════════════════════════════════');
  console.log('   JSONL Cleaner for AI Ingestion');
  console.log('═══════════════════════════════════════════════════\n');

  try {
    await cleanJsonlFile(filename);
    console.log('\n✅ Cleaning successful. Your JSONL is AI-ready!');
  } catch (error) {
    console.error('❌ Cleaning failed:', error.message);
    process.exit(1);
  }
}

main();
