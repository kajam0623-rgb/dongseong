#!/usr/bin/env node
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const projectsDir = path.join(root, 'projects');
const projectRecordFile = 'project.siteon.json';
const projectDataFile = 'project.json';
const requestBodyLimit = Number(process.env.SITEON_PROJECT_BODY_LIMIT || 80 * 1024 * 1024);
const host = '127.0.0.1';
const portArgIndex = process.argv.indexOf('--port');
const port = Number(
  process.env.SITEON_WEB_PORT ||
  (portArgIndex >= 0 ? process.argv[portArgIndex + 1] : '') ||
  8765
);

const contentTypes = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.jpg', 'image/jpeg'],
  ['.jpeg', 'image/jpeg'],
  ['.png', 'image/png'],
  ['.webp', 'image/webp'],
  ['.svg', 'image/svg+xml; charset=utf-8']
]);

function sendJson(res, status, body) {
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  res.end(JSON.stringify(body));
}

function safeProjectSlug(value = 'siteon-project') {
  const raw = String(value || 'siteon-project').normalize('NFC').trim().toLowerCase();
  const clean = raw
    .replace(/[\\/:*?"<>|]+/g, '-')
    .replace(/[^\p{L}\p{N}\s_.-]+/gu, '-')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^[-.]+|[-.]+$/g, '');
  return (clean || 'siteon-project').slice(0, 64);
}

function assertInside(parent, target) {
  const relative = path.relative(parent, target);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error('Resolved path escaped the allowed directory.');
  }
}

function projectDirFor(slug) {
  const safeSlug = safeProjectSlug(slug);
  const target = path.resolve(projectsDir, safeSlug);
  assertInside(projectsDir, target);
  return { slug: safeSlug, target };
}

async function readJsonFile(file) {
  const text = await fsp.readFile(file, 'utf8');
  return JSON.parse(text);
}

function normalizeStoredRecord(input, fallbackSlug = '') {
  const payload = input?.record || input || {};
  const project = payload.project && typeof payload.project === 'object' ? payload.project : payload;
  const workspace = project?.state?.workspace || {};
  const name = String(payload.name || project?.fields?.f_name || workspace.name || 'SiteOn Project').trim() || 'SiteOn Project';
  const id = String(payload.id || workspace.id || `project_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`);
  const rootName = payload.folder?.root || workspace.slug || project?.fields?.f_export_root || fallbackSlug || name || id;
  const folder = { ...(payload.folder || {}), root: safeProjectSlug(rootName) };
  return {
    ...payload,
    id,
    name,
    createdAt: payload.createdAt || workspace.createdAt || payload.updatedAt || '',
    updatedAt: payload.updatedAt || payload.createdAt || '',
    folder,
    project
  };
}

function normalizeProjectRecord(input) {
  const now = new Date().toISOString();
  const record = normalizeStoredRecord(input);
  record.createdAt = record.createdAt || now;
  record.updatedAt = now;

  if (record.project?.state && typeof record.project.state === 'object') {
    record.project.state.workspace = {
      ...(record.project.state.workspace || {}),
      id: record.id,
      name: record.name,
      slug: record.folder.root,
      createdAt: record.createdAt,
      updatedAt: record.updatedAt
    };
  }

  return record;
}

async function writeProjectRecord(record) {
  const { target } = projectDirFor(record.folder?.root || record.name || record.id);
  await fsp.mkdir(target, { recursive: true });
  await fsp.writeFile(path.join(target, projectRecordFile), JSON.stringify(record, null, 2), 'utf8');
  await fsp.writeFile(path.join(target, projectDataFile), JSON.stringify(record.project || {}, null, 2), 'utf8');

  if (record.folder?.assets) {
    await fsp.writeFile(path.join(target, 'assets.json'), JSON.stringify(record.folder.assets, null, 2), 'utf8');
  }

  if (record.folder?.theme || record.folder?.assets?.theme) {
    const themeDir = path.join(target, 'theme');
    assertInside(projectsDir, themeDir);
    await fsp.mkdir(themeDir, { recursive: true });
    await fsp.writeFile(
      path.join(themeDir, 'theme.json'),
      JSON.stringify(record.folder.theme || record.folder.assets.theme || {}, null, 2),
      'utf8'
    );
  }

  return record;
}

async function listProjectRecords() {
  await fsp.mkdir(projectsDir, { recursive: true });
  const entries = await fsp.readdir(projectsDir, { withFileTypes: true });
  const rows = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const { target } = projectDirFor(entry.name);
    try {
      const stored = await readJsonFile(path.join(target, projectRecordFile));
      rows.push(normalizeStoredRecord(stored, entry.name));
    } catch {
      try {
        const project = await readJsonFile(path.join(target, projectDataFile));
        rows.push(normalizeStoredRecord({ project, folder: { root: entry.name } }, entry.name));
      } catch {
        // Ignore incomplete project folders.
      }
    }
  }

  return rows.sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''));
}

async function findProjectRecord(idOrSlug) {
  const direct = projectDirFor(idOrSlug);
  try {
    const stored = await readJsonFile(path.join(direct.target, projectRecordFile));
    return normalizeStoredRecord(stored, direct.slug);
  } catch {
    const rows = await listProjectRecords();
    return rows.find(row => row.id === idOrSlug || row.folder?.root === idOrSlug || row.folder?.root === direct.slug) || null;
  }
}

async function findProjectDir(idOrSlug) {
  const direct = projectDirFor(idOrSlug);
  try {
    await fsp.access(direct.target);
    return direct.target;
  } catch {
    const row = await findProjectRecord(idOrSlug);
    if (!row) return direct.target;
    return projectDirFor(row.folder?.root || row.id).target;
  }
}

function readRequestJson(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', chunk => {
      size += chunk.length;
      if (size > requestBodyLimit) {
        reject(new Error('Project payload is too large.'));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => {
      if (!chunks.length) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(Buffer.concat(chunks).toString('utf8')));
      } catch (error) {
        reject(error);
      }
    });
    req.on('error', reject);
  });
}

async function handleProjectsApi(req, res, url) {
  const parts = url.pathname.split('/').filter(Boolean);
  if (parts[0] !== 'api' || parts[1] !== 'projects') return false;

  if (parts.length === 2 && req.method === 'GET') {
    sendJson(res, 200, { ok: true, root: projectsDir, projects: await listProjectRecords() });
    return true;
  }

  if (parts.length === 2 && req.method === 'POST') {
    const record = normalizeProjectRecord(await readRequestJson(req));
    await writeProjectRecord(record);
    sendJson(res, 200, { ok: true, root: projectsDir, project: record });
    return true;
  }

  const id = parts[2] ? decodeURIComponent(parts[2]) : '';
  if (parts.length === 3 && id && req.method === 'GET') {
    const project = await findProjectRecord(id);
    if (!project) {
      sendJson(res, 404, { ok: false, error: 'Project not found.' });
      return true;
    }
    sendJson(res, 200, { ok: true, root: projectsDir, project });
    return true;
  }

  if (parts.length === 3 && id && req.method === 'DELETE') {
    const target = await findProjectDir(id);
    assertInside(projectsDir, target);
    await fsp.rm(target, { recursive: true, force: true });
    sendJson(res, 200, { ok: true });
    return true;
  }

  sendJson(res, 405, { ok: false, error: 'Method not allowed.' });
  return true;
}

function resolveRequestPath(reqUrl) {
  const url = new URL(reqUrl, `http://${host}:${port}`);
  let pathname = decodeURIComponent(url.pathname);
  if (pathname === '/') pathname = '/사이트온-빌더.html';
  const target = path.resolve(root, pathname.replace(/^\/+/, ''));
  const relative = path.relative(root, target);
  if (relative.startsWith('..') || path.isAbsolute(relative)) return null;
  return target;
}

async function handleRequest(req, res) {
  const url = new URL(req.url || '/', `http://${host}:${port}`);

  if (req.url === '/siteon-health') {
    sendJson(res, 200, { ok: true, root, projectsDir, port });
    return;
  }

  if (await handleProjectsApi(req, res, url)) return;

  if (req.method !== 'GET' && req.method !== 'HEAD') {
    sendJson(res, 405, { ok: false, error: 'Method not allowed.' });
    return;
  }

  const target = resolveRequestPath(req.url || '/');
  if (!target) {
    sendJson(res, 403, { ok: false, error: 'Forbidden.' });
    return;
  }

  const stat = await fsp.stat(target).catch(() => null);
  if (!stat?.isFile()) {
    sendJson(res, 404, { ok: false, error: 'Not found.' });
    return;
  }

  res.writeHead(200, {
    'Content-Type': contentTypes.get(path.extname(target).toLowerCase()) || 'application/octet-stream',
    'Content-Length': stat.size,
    'Cache-Control': 'no-store'
  });

  if (req.method === 'HEAD') {
    res.end();
    return;
  }

  fs.createReadStream(target).pipe(res);
}

const server = http.createServer((req, res) => {
  handleRequest(req, res).catch(error => {
    sendJson(res, 500, { ok: false, error: error?.message || 'Internal server error.' });
  });
});

server.listen(port, host, () => {
  console.log(`SiteOn static server listening on http://${host}:${port}`);
});
