#!/usr/bin/env node
/**
 * 애니톡 캠퍼스 랜딩페이지 빌더.
 *
 *   node build.mjs                # 전체 지점 빌드
 *   node build.mjs mokdong hongdae  # 특정 지점만
 *
 * data/<slug>.json  →  sites/<slug>/ (index.html · vercel.json · robots.txt · sitemap.xml)
 *
 * sites/<slug>/ 폴더 하나가 그대로 배포 루트다. 통째로 저장소에 올리거나
 * `vercel deploy sites/<slug>` 하면 끝이고, 빌드 과정이 런타임에 필요 없다.
 *
 * 사진은 sites/<slug>/gal/ 에 넣어 두면 빌드가 자동으로 집어 간다.
 * 파일명은 data/<slug>.json 의 image.local 값과 같으면 된다.
 */

import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderPage, render404 } from './lib/render.mjs';

const ROOT = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(ROOT, 'data');
const OUT_DIR = join(ROOT, 'sites');

const readJson = (p) => JSON.parse(readFileSync(p, 'utf8'));

const allSlugs = readdirSync(DATA_DIR)
  .filter((f) => f.endsWith('.json') && f !== '_shared.json')
  .map((f) => f.replace(/\.json$/, ''));

const shared = existsSync(join(DATA_DIR, '_shared.json'))
  ? readJson(join(DATA_DIR, '_shared.json'))
  : {};

/** _shared.json 위에 지점 데이터를 얕게 덮어쓴다(한 단계 깊이까지 병합). */
function merge(base, over) {
  const out = { ...base };
  for (const [k, v] of Object.entries(over)) {
    out[k] =
      v && typeof v === 'object' && !Array.isArray(v) && base[k] && typeof base[k] === 'object' && !Array.isArray(base[k])
        ? { ...base[k], ...v }
        : v;
  }
  return out;
}

/**
 * 최종 주소를 결정한다.
 * _shared.json 의 site.baseDomain 이 비어 있으면 지점별 vercel.app 주소를 쓰고,
 * "anitok.com" 처럼 채워지면 https://<subdomain>.anitok.com 으로 한 번에 바뀐다.
 * canonical · og:url · sitemap · 형제 캠퍼스 링크가 모두 이 값을 따른다.
 */
function resolveOrigin(d) {
  const base = d.site?.baseDomain;
  const sub = d.site?.subdomain;
  if (base && sub) return `https://${sub}.${String(base).replace(/^https?:\/\//, '').replace(/\/$/, '')}`;
  return d.site.origin;
}

/** 지점 데이터를 읽고 공통값 병합 + 최종 주소 · 테마 확정까지 한 번에. */
function loadCampus(slug) {
  const d = merge(shared, readJson(join(DATA_DIR, `${slug}.json`)));
  d.site = { ...d.site, origin: resolveOrigin(d) };

  // themeName 으로 _shared.json 의 테마를 찾아 붙인다. 이름이 틀리면 빌드를 멈춘다.
  const name = d.themeName || 'red';
  const theme = (shared.themes || {})[name];
  if (!theme) {
    console.error(
      `${slug}: 알 수 없는 테마 "${name}" (가능: ${Object.keys(shared.themes || {}).join(', ')})`
    );
    process.exit(1);
  }
  d.theme = theme;
  return d;
}

const targets = process.argv.slice(2).length ? process.argv.slice(2) : allSlugs;

for (const t of targets) {
  if (!allSlugs.includes(t)) {
    console.error(`알 수 없는 지점: ${t} (가능: ${allSlugs.join(', ')})`);
    process.exit(1);
  }
}

// 푸터의 형제 캠퍼스 링크 — 전체 지점을 항상 읽어서 만든다.
// otherCampuses 는 이 저장소 밖에 있는 캠퍼스(일산)를 끼워 넣기 위한 것이다.
const siblings = [
  ...allSlugs.map(loadCampus).map((d) => ({ slug: d.slug, label: d.shortName, href: d.site.origin })),
  ...(shared.otherCampuses || []),
].sort((a, b) => a.label.localeCompare(b.label, 'ko'));

let built = 0;
const report = [];

for (const slug of targets) {
  const d = loadCampus(slug);
  const outDir = join(OUT_DIR, slug);
  const galDir = join(outDir, 'gal');
  mkdirSync(galDir, { recursive: true });

  // gal/ 에 실제로 존재하는 파일만 로컬 이미지로 인정한다.
  const present = new Set(readdirSync(galDir).filter((f) => f !== '.gitkeep'));

  // git은 빈 디렉터리를 추적하지 않는다. 지점 저장소로 분리했을 때도 gal/ 이
  // 남아 있도록 자리를 잡아 둔다.
  writeFileSync(join(galDir, '.gitkeep'), '');

  const html = renderPage(d, { present, siblings });
  writeFileSync(join(outDir, 'index.html'), html);

  writeFileSync(
    join(outDir, 'robots.txt'),
    `User-agent: *\nAllow: /\n\nSitemap: ${d.site.origin}/sitemap.xml\n`
  );

  const today = new Date().toISOString().slice(0, 10);
  writeFileSync(
    join(outDir, 'sitemap.xml'),
    `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${d.site.origin}/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
`
  );

  writeFileSync(
    join(outDir, 'vercel.json'),
    JSON.stringify(
      {
        cleanUrls: true,
        headers: [
          {
            source: '/gal/(.*)',
            headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }],
          },
          {
            source: '/index.html',
            headers: [{ key: 'Cache-Control', value: 'public, max-age=0, must-revalidate' }],
          },
        ],
      },
      null,
      2
    ) + '\n'
  );

  // 파비콘 — 애니톡 레드 원 + 흰 AT. SVG 하나로 라이트/다크 탭 모두 대응된다.
  writeFileSync(
    join(outDir, 'favicon.svg'),
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="32" fill="${d.theme.faviconBg || d.theme.accent}"/>
  <text x="32" y="43" text-anchor="middle" fill="${d.theme.faviconFg || d.theme.onAccent}"
        font-family="Pretendard, -apple-system, system-ui, sans-serif"
        font-size="30" font-weight="800" letter-spacing="-1.5">AT</text>
</svg>
`
  );

  // 404 — 기본 Vercel 페이지 대신 같은 톤으로.
  writeFileSync(join(outDir, '404.html'), render404(d));

  writeFileSync(
    join(outDir, 'README.md'),
    `# ${d.repo}\n\n${d.name} 랜딩페이지 (정적 사이트)\n\n` +
      `이 폴더는 \`anitok-campuses/build.mjs\` 가 \`data/${slug}.json\` 으로부터 생성합니다.\n` +
      `여기서 직접 \`index.html\` 을 고치지 말고 데이터/템플릿을 고친 뒤 다시 빌드하세요.\n\n` +
      `- 배포 주소: ${d.site.origin}\n- 사진: \`gal/\` 에 파일을 넣고 다시 빌드하면 자동 반영됩니다.\n`
  );

  // 미해결 이미지 슬롯 집계 — 어디에 사진을 넣어야 하는지 알려 준다.
  const slots = collectSlots(d);

  // 사진 체크리스트: gal/ 에 어떤 파일명으로 무슨 사진을 넣어야 하는지.
  writeFileSync(
    join(outDir, 'PHOTOS.md'),
    `# ${d.name} — 사진 체크리스트\n\n` +
      `\`sites/${slug}/gal/\` 에 아래 파일명으로 사진을 넣고 \`node build.mjs ${slug}\` 를 다시 실행하면 반영됩니다.\n` +
      `확장자는 webp를 권장하며, jpg를 쓰려면 \`data/${slug}.json\` 의 \`local\` 값도 함께 바꾸세요.\n\n` +
      `| 파일명 | 들어갈 사진 | 현재 상태 |\n|---|---|---|\n` +
      slots
        .map((s) => {
          const state = s.local && present.has(s.local)
            ? '적용됨'
            : s.remote
              ? '임시(애니톡 CDN 이미지)'
              : '비어 있음';
          return `| \`${s.local || '-'}\` | ${s.caption || '-'} | ${state} |`;
        })
        .join('\n') +
      '\n'
  );

  const missing = slots.filter((s) => !(s.local && present.has(s.local)) && !s.remote);
  const remoteOnly = slots.filter((s) => !(s.local && present.has(s.local)) && s.remote);

  report.push({
    slug,
    theme: d.themeName || 'red',
    bytes: Buffer.byteLength(html),
    slots: slots.length,
    local: slots.length - missing.length - remoteOnly.length,
    remote: remoteOnly.length,
    missing: missing.length,
  });
  built++;
}

function collectSlots(d) {
  const out = [];
  const push = (s) => s && out.push(s);
  push(d.hero?.image);
  (d.about?.figures || []).forEach(push);
  (d.classes?.groups || []).forEach((g) => (g.items || []).forEach((c) => push(c.image)));
  (d.galleries || []).forEach((g) => (g.items || []).forEach(push));
  return out;
}

console.log(`빌드 완료: ${built}개 지점\n`);
console.log('지점       테마     크기      이미지 슬롯 (로컬/원격/비어있음)');
console.log('─'.repeat(66));
for (const r of report) {
  console.log(
    `${r.slug.padEnd(10)} ${r.theme.padEnd(8)} ${(Math.round(r.bytes / 1024) + 'KB').padEnd(9)} ` +
      `${String(r.slots).padStart(2)}개  ${r.local} / ${r.remote} / ${r.missing}`
  );
}
