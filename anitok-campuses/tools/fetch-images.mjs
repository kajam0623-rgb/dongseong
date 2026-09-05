#!/usr/bin/env node
/**
 * 데이터에 적힌 원격 이미지(애니톡 자체 CDN)를 각 지점의 gal/ 폴더로 내려받는다.
 *
 *   node tools/fetch-images.mjs            # 전체 지점
 *   node tools/fetch-images.mjs mokdong    # 특정 지점만
 *
 * 내려받은 뒤 `node build.mjs` 를 다시 돌리면 페이지가 원격 URL 대신
 * 로컬 파일을 쓰도록 바뀐다. 원본 CDN이 바뀌어도 사이트는 그대로 유지된다.
 *
 * 주의: 이 스크립트는 외부 네트워크가 열린 환경(개인 PC 등)에서 실행해야 한다.
 * 이미 gal/ 에 있는 파일은 건드리지 않는다(--force 로 덮어쓰기).
 */

import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const DATA_DIR = join(ROOT, 'data');
const OUT_DIR = join(ROOT, 'sites');

const args = process.argv.slice(2);
const force = args.includes('--force');
const wanted = args.filter((a) => !a.startsWith('--'));

const slugs = readdirSync(DATA_DIR)
  .filter((f) => f.endsWith('.json') && f !== '_shared.json')
  .map((f) => f.replace(/\.json$/, ''))
  .filter((s) => !wanted.length || wanted.includes(s));

function collectSlots(d) {
  const out = [];
  const push = (s) => s && s.remote && s.local && out.push(s);
  push(d.hero?.image);
  (d.about?.figures || []).forEach(push);
  (d.classes?.groups || []).forEach((g) => (g.items || []).forEach((c) => push(c.image)));
  (d.galleries || []).forEach((g) => (g.items || []).forEach(push));
  return out;
}

let ok = 0;
let skipped = 0;
let failed = 0;

for (const slug of slugs) {
  const d = JSON.parse(readFileSync(join(DATA_DIR, `${slug}.json`), 'utf8'));
  const galDir = join(OUT_DIR, slug, 'gal');
  mkdirSync(galDir, { recursive: true });

  for (const slot of collectSlots(d)) {
    // 원격 파일 확장자를 그대로 유지한다. jpg를 받아 놓고 .webp로 저장하면
    // 브라우저는 읽지만 나중에 사람이 헷갈린다.
    const ext = (extname(new URL(slot.remote).pathname) || '.jpg').toLowerCase();
    const name = slot.local.replace(/\.[^.]+$/, '') + ext;
    const dest = join(galDir, name);

    if (existsSync(dest) && !force) {
      console.log(`건너뜀  ${slug}/${name} (이미 있음)`);
      skipped++;
      continue;
    }
    try {
      const res = await fetch(slot.remote);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const buf = Buffer.from(await res.arrayBuffer());
      writeFileSync(dest, buf);
      console.log(`받음    ${slug}/${name}  ${(buf.length / 1024).toFixed(0)}KB`);
      ok++;
      if (name !== slot.local) {
        console.log(`        ↳ data/${slug}.json 의 local 값을 "${name}" 로 바꿔 주세요`);
      }
    } catch (e) {
      console.error(`실패    ${slug}/${name}: ${e.message}`);
      failed++;
    }
  }
}

console.log(`\n완료: 받음 ${ok} · 건너뜀 ${skipped} · 실패 ${failed}`);
if (ok) console.log('이제 `node build.mjs` 를 다시 실행하세요.');
