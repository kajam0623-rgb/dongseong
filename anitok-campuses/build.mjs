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

import { readFileSync, writeFileSync, mkdirSync, readdirSync, existsSync, unlinkSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { renderPage, render404, renderLocal, localPages, siteCss, siteJs } from './lib/render.mjs';

const ROOT = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(ROOT, 'data');
const OUT_DIR = join(ROOT, 'sites');

const readJson = (p) => JSON.parse(readFileSync(p, 'utf8'));

/** CSS: 주석과 들여쓰기·빈 줄을 걷어낸다. 선택자/값은 손대지 않는다. */
function minCss(css) {
  return css
    .replace(/\/\*[\s\S]*?\*\//g, '')   // 주석
    .replace(/\s+/g, ' ')                 // 줄바꿈·연속 공백 → 한 칸
    .replace(/\s*([{};,])\s*/g, '$1')     // 구분자 주변 공백
    .replace(/:\s+/g, ':')                // 값 앞 공백 (calc의 +/- 는 건드리지 않는다)
    .replace(/;}/g, '}')                  // 마지막 세미콜론
    .trim();
}

/**
 * JS: 줄머리 들여쓰기와 한 줄 주석만 걷어낸다. 줄바꿈은 유지한다.
 * (줄을 합치면 ASI·정규식 리터럴에서 사고가 난다.)
 */
function minJs(js) {
  return js
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('//'))
    .join('\n');
}

/** HTML: 줄머리 공백과 빈 줄만. 줄바꿈은 남겨 인라인 요소 사이 공백을 보존한다. */
function minHtml(html) {
  return html
    .split('\n')
    .map((l) => l.replace(/^[\t ]+/, ''))
    .filter((l) => l !== '')
    .join('\n');
}

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

  // 같은 사진에 서로 다른 캡션이 붙는 것을 막는다. 소개 섹션은 히어로 사진을
  // 건너뛰고 갤러리는 건너뛰지 않아서, 캡션을 손으로 적으면 한 칸씩 밀린 채로
  // "학원 공간"과 "수업 현장"이 같은 사진에 동시에 달리는 일이 생겼다.
  // local 과 remote 를 따로 본다. 같은 사진이라도 about-1.webp / gal-2.webp 처럼
  // 로컬 파일명은 다를 수 있어서, remote 까지 봐야 어긋난 캡션이 잡힌다.
  // 히어로는 alt="" 로 나가므로 캡션이 화면에 안 보인다. 보이는 캡션만 본다.
  const captioned = [
    ...(d.about?.figures || []),
    ...(d.galleries || []).flatMap((g) => g.items || []),
  ];
  const capOf = new Map();
  for (const slot of captioned) {
    if (!slot.caption) continue;
    for (const key of [slot.local, slot.remote]) {
      if (!key) continue;
      const seen = capOf.get(key);
      if (seen && seen !== slot.caption) {
        console.error(
          `${slug}: 같은 사진에 캡션이 두 개다 — ${key}\n  "${seen}" vs "${slot.caption}"`
        );
        process.exit(1);
      }
      capOf.set(key, slot.caption);
    }
  }

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

  const html = minHtml(renderPage(d, { present, siblings }));
  writeFileSync(join(outDir, 'index.html'), html);

  // CSS/JS는 모든 페이지가 공유한다. 페이지마다 인라인하면 20KB씩 중복된다.
  writeFileSync(join(outDir, 's.css'), minCss(siteCss(d)));
  writeFileSync(join(outDir, 's.js'), minJs(siteJs()));

  // 지역 · 과목 랜딩페이지 (목동만화학원 / 화곡만화학원 …)
  const pages = localPages(d);
  const keepHtml = new Set(['index.html', '404.html', ...pages.map((p) => `${p.slug}.html`)]);
  for (const f of readdirSync(outDir)) {
    if (f.endsWith('.html') && !keepHtml.has(f)) unlinkSync(join(outDir, f));
  }
  for (const page of pages) {
    writeFileSync(join(outDir, `${page.slug}.html`), minHtml(renderLocal(d, page, { pages })));
  }

  writeFileSync(
    join(outDir, 'robots.txt'),
    `User-agent: *\nAllow: /\n\nSitemap: ${d.site.origin}/sitemap.xml\n`
  );

  const today = new Date().toISOString().slice(0, 10);
  const urlEntry = (loc, priority) =>
    `  <url>\n    <loc>${loc}</loc>\n    <lastmod>${today}</lastmod>\n` +
    `    <changefreq>monthly</changefreq>\n    <priority>${priority}</priority>\n  </url>`;
  writeFileSync(
    join(outDir, 'sitemap.xml'),
    `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[
  urlEntry(`${d.site.origin}/`, '1.0'),
  ...pages.map((p) => urlEntry(`${d.site.origin}/${p.slug}`, '0.8')),
].join('\n')}
</urlset>
`
  );

  // 자체 도메인으로 옮긴 지점은 *.vercel.app 으로 들어온 요청을 301 로 넘긴다.
  // 미리보기 주소까지 한 번에 걸리게 호스트를 정규식으로 잡았다. 색인이
  // 두 주소로 갈라지는 것과, 예전 링크가 그대로 살아 있는 것을 같이 막는다.
  const onVercelHost = /\.vercel\.app$/.test(new URL(d.site.origin).hostname);
  const vercelRedirects = onVercelHost
    ? []
    : [
        {
          source: '/:path*',
          has: [{ type: 'host', value: '(?<vhost>.*)\\.vercel\\.app' }],
          destination: `${d.site.origin}/:path*`,
          permanent: true,
        },
      ];

  writeFileSync(
    join(outDir, 'vercel.json'),
    JSON.stringify(
      {
        cleanUrls: true,
        ...(vercelRedirects.length ? { redirects: vercelRedirects } : {}),
        headers: [
          {
            source: '/gal/(.*)',
            headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }],
          },
          {
            source: '/(s.css|s.js)',
            headers: [{ key: 'Cache-Control', value: 'public, max-age=86400, must-revalidate' }],
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

  // 파비콘 — 애니톡 로고(웃는 얼굴 마크)를 그대로 옮겼다. 글자 'AT' 대신
  // 브랜드 마크를 쓰라는 요청. 흰 라운드 사각 바탕 + 브랜드 컬러 마크로
  // 일산 캠퍼스 아이콘과 같은 모양이며, 벡터라 16px 탭에서도 뭉개지지 않는다.
  const markFill = d.theme.faviconBg || d.theme.accent;
  writeFileSync(
    join(outDir, 'favicon.svg'),
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="애니톡">
  <rect x="1.5" y="1.5" width="61" height="61" rx="15" fill="#FFFFFF" stroke="#E2E2E4" stroke-width="3"/>
  <circle cx="17.5" cy="28.5" r="4.6" fill="${markFill}"/>
  <circle cx="46.5" cy="28.5" r="4.6" fill="${markFill}"/>
  <path d="M25.5 34a6.5 6.5 0 0 0 13 0" fill="none" stroke="${markFill}"
        stroke-width="4.6" stroke-linecap="round"/>
</svg>
`
  );

  // PNG 대체본 — SVG 파비콘을 못 읽는 브라우저용. 애니톡 로고 원본을 그대로
  // 복사한다(외부 CDN 은 핫링크가 막혀 탭에서 비어 보였다).
  for (const icon of ['icon-16.png', 'icon-32.png']) {
    writeFileSync(join(outDir, icon), readFileSync(join(ROOT, 'assets', icon)));
  }

  // iOS 홈 화면 아이콘 — 애플은 SVG 를 안 읽어서 180px PNG 가 따로 필요하다.
  // 모서리는 iOS 가 알아서 둥글리므로 흰 정사각 그대로 둔다. 마크 색만 다른
  // 두 벌을 미리 그려 뒀고(assets/apple-touch-icon-*.png), 캠퍼스 강조색에
  // 맞는 쪽을 고른다. 새 테마 색이 생기면 tools/make-touch-icon.py 로 추가.
  const TOUCH = { '#C9480B': 'orange', '#0B0B0C': 'mono' };
  const touch = TOUCH[markFill.toUpperCase()] || 'orange';
  writeFileSync(
    join(outDir, 'apple-touch-icon.png'),
    readFileSync(join(ROOT, 'assets', `apple-touch-icon-${touch}.png`))
  );

  // 404 — 기본 Vercel 페이지 대신 같은 톤으로.
  writeFileSync(join(outDir, '404.html'), minHtml(render404(d)));

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
    pages: pages.length,
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
