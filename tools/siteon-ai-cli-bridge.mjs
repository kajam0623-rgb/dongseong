#!/usr/bin/env node
import http from 'node:http';
import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const requestDir = path.join(rootDir, 'ai-requests');
const host = '127.0.0.1';
const port = Number(process.env.SITEON_AI_PORT || 4627);
const cli = (process.env.SITEON_AI_CLI || '').trim();
const cliArgs = splitArgs(process.env.SITEON_AI_ARGS || '');
const promptMode = (process.env.SITEON_AI_PROMPT_MODE || 'stdin').toLowerCase();
const timeoutMs = Number(process.env.SITEON_AI_TIMEOUT_MS || 180000);
const maxBodyBytes = Number(process.env.SITEON_AI_MAX_BODY_MB || 80) * 1024 * 1024;

function splitArgs(input) {
  const args = [];
  let current = '';
  let quote = '';
  let escape = false;

  for (const ch of input) {
    if (escape) {
      current += ch;
      escape = false;
      continue;
    }
    if (ch === '\\') {
      escape = true;
      continue;
    }
    if (quote) {
      if (ch === quote) quote = '';
      else current += ch;
      continue;
    }
    if (ch === '"' || ch === "'") {
      quote = ch;
      continue;
    }
    if (/\s/.test(ch)) {
      if (current) {
        args.push(current);
        current = '';
      }
      continue;
    }
    current += ch;
  }

  if (current) args.push(current);
  return args;
}

function sendJson(res, status, body) {
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Cache-Control': 'no-store'
  });
  res.end(JSON.stringify(body, null, 2));
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', chunk => {
      size += chunk.length;
      if (size > maxBodyBytes) {
        reject(new Error(`Request body is larger than ${process.env.SITEON_AI_MAX_BODY_MB || 80}MB.`));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}'));
      } catch (error) {
        reject(error);
      }
    });
    req.on('error', reject);
  });
}

function buildPrompt(payload, requestPath) {
  const userRequest = payload.userRequest || payload.instruction || '';
  const taskLabel = payload.taskLabel || payload.task || 'site edit';
  const target = payload.target || 'all';
  const snapshot = payload.snapshot ? JSON.stringify(payload.snapshot, null, 2) : '';
  return [
    'You are editing a SiteOn builder project JSON.',
    'Return ONLY valid JSON. Do not return Markdown, comments, explanations, or code fences.',
    'Preferred full response: {"project": <complete updated project JSON>, "notes": "...", "imagePrompts": [], "geo": {}}.',
    'Partial response allowed: {"patch": {"fields": {}, "state": {}, "customCode": {"css": "", "headHtml": "", "bodyHtml": ""}}, "notes": "...", "imagePrompts": [], "geo": {}}.',
    'Preserve the project schema and every unrelated field.',
    'For HTML/CSS edits, prefer patch.customCode. Keep CSS scoped and responsive.',
    'For image generation, return imagePrompts with target, prompt, recommendedAspectRatio, alt, and negativePrompt.',
    'For GEO/AEO/SEO, return geo suggestions plus safe copy/schema/headHtml patches.',
    'The source request JSON is saved at:',
    requestPath,
    '',
    `Task: ${taskLabel}`,
    `Target: ${target}`,
    '',
    'Task instruction:',
    payload.instruction || '',
    '',
    'User edit request:',
    userRequest,
    '',
    'Site snapshot:',
    snapshot,
    '',
    'Current project JSON:',
    JSON.stringify(payload.project, null, 2)
  ].join('\n');
}

function tryParseJson(text) {
  if (!text || typeof text !== 'string') return null;
  const clean = text.trim().replace(/^```(?:json)?/i, '').replace(/```$/i, '').trim();
  try {
    return JSON.parse(clean);
  } catch {}
  const first = clean.indexOf('{');
  const last = clean.lastIndexOf('}');
  if (first >= 0 && last > first) {
    try {
      return JSON.parse(clean.slice(first, last + 1));
    } catch {}
  }
  return null;
}

function runCli(prompt) {
  if (!cli) {
    return Promise.resolve({
      ok: true,
      skipped: true,
      stdout: '',
      stderr: '',
      message: 'SITEON_AI_CLI is not set. The request and prompt files were saved.'
    });
  }

  return new Promise(resolve => {
    const args = promptMode === 'arg' ? [...cliArgs, prompt] : cliArgs;
    const child = spawn(cli, args, {
      cwd: rootDir,
      stdio: ['pipe', 'pipe', 'pipe'],
      windowsHide: true
    });
    let stdout = '';
    let stderr = '';
    let done = false;

    const finish = result => {
      if (done) return;
      done = true;
      clearTimeout(timer);
      resolve(result);
    };
    const timer = setTimeout(() => {
      child.kill();
      finish({ ok: false, stdout, stderr, error: `CLI timed out after ${timeoutMs}ms.` });
    }, timeoutMs);

    child.stdout.on('data', data => { stdout += data.toString(); });
    child.stderr.on('data', data => { stderr += data.toString(); });
    child.on('error', error => finish({ ok: false, stdout, stderr, error: error.message }));
    child.on('close', code => finish({ ok: code === 0, code, stdout, stderr }));

    if (promptMode === 'arg') child.stdin.end();
    else child.stdin.end(prompt);
  });
}

async function handleAiEdit(req, res) {
  const payload = await readJson(req);
  const validSchemas = new Set(['siteon/ai-cli-edit-v1', 'siteon/ai-cli-edit-v2']);
  if (!payload || !validSchemas.has(payload.schema)) {
    sendJson(res, 400, { ok: false, error: 'Invalid schema.' });
    return;
  }
  if ((!payload.instruction || typeof payload.instruction !== 'string') && (!payload.userRequest || typeof payload.userRequest !== 'string')) {
    sendJson(res, 400, { ok: false, error: 'Missing instruction.' });
    return;
  }
  if (!payload.project || typeof payload.project !== 'object') {
    sendJson(res, 400, { ok: false, error: 'Missing project JSON.' });
    return;
  }

  await mkdir(requestDir, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const requestPath = path.join(requestDir, `${stamp}-request.json`);
  const promptPath = path.join(requestDir, `${stamp}-prompt.txt`);
  await writeFile(requestPath, JSON.stringify(payload, null, 2), 'utf8');
  const prompt = buildPrompt(payload, requestPath);
  await writeFile(promptPath, prompt, 'utf8');

  const cliResult = await runCli(prompt);
  const parsed = tryParseJson(cliResult.stdout);
  sendJson(res, cliResult.ok ? 200 : 500, {
    ok: cliResult.ok,
    cliConfigured: Boolean(cli),
    skipped: Boolean(cliResult.skipped),
    requestPath,
    promptPath,
    result: parsed,
    stdout: cliResult.stdout,
    stderr: cliResult.stderr,
    error: cliResult.error,
    message: cliResult.message
  });
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.method === 'OPTIONS') {
      sendJson(res, 204, {});
      return;
    }
    if (req.method === 'GET' && req.url === '/health') {
      sendJson(res, 200, { ok: true, cliConfigured: Boolean(cli), promptMode, port });
      return;
    }
    if (req.method === 'POST' && req.url === '/ai-edit') {
      await handleAiEdit(req, res);
      return;
    }
    sendJson(res, 404, { ok: false, error: 'Not found.' });
  } catch (error) {
    sendJson(res, 500, { ok: false, error: error.message || String(error) });
  }
});

server.listen(port, host, () => {
  console.log(`SiteOn AI CLI bridge listening on http://${host}:${port}`);
  console.log(cli ? `CLI: ${cli} ${cliArgs.join(' ')}` : 'CLI is not configured. Set SITEON_AI_CLI to enable execution.');
});
