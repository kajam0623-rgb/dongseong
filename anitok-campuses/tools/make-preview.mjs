#!/usr/bin/env node
/**
 * 7개 지점 사이트를 한 페이지에서 넘겨 볼 수 있는 프리뷰를 만든다.
 *
 *   node tools/make-preview.mjs [출력경로]
 *
 * 각 사이트는 srcdoc iframe 안에 통째로 들어가므로 CSS·JS가 서로 섞이지 않고,
 * 실제 배포될 마크업 그대로를 본다. 다만 샌드박스 환경에서 외부 리소스가 막히므로
 * 폰트만 Pretendard(jsDelivr) → Noto Sans KR(Google Fonts)로 바꿔 끼운다.
 */
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const OUT = process.argv[2] || join(ROOT, 'preview.html');

const ORDER = ['mokdong', 'hongdae', 'gangdong', 'bucheon', 'gwanggyo', 'gimpo', 'academy'];

const campuses = ORDER.map((slug) => {
  const data = JSON.parse(readFileSync(join(ROOT, 'data', `${slug}.json`), 'utf8'));
  const shared = JSON.parse(readFileSync(join(ROOT, 'data', '_shared.json'), 'utf8'));
  const theme = shared.themes[data.themeName];

  let html = readFileSync(join(ROOT, 'sites', slug, 'index.html'), 'utf8');
  // 프리뷰 전용 치환 — 배포본은 건드리지 않는다.
  html = html
    .replace(
      /<link rel="stylesheet" href="https:\/\/cdn\.jsdelivr\.net[^"]*">/,
      '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800;900&display=swap">'
    )
    .replace(/'Pretendard Variable',Pretendard,/, "'Noto Sans KR','Pretendard Variable',Pretendard,")
    .replace(/<link rel="icon"[^>]*>/, '')
    .replace(/<link rel="preconnect" href="https:\/\/cdn\.jsdelivr\.net"[^>]*>/, '');

  return {
    slug,
    name: data.shortName,
    full: data.name,
    phone: data.phone,
    region: data.geo.placename,
    accent: theme.accent,
    onAccent: theme.onAccent,
    themeName: data.themeName,
    origin: data.site.origin,
    html,
  };
});

// </script> 가 문자열 안에 그대로 들어가면 스크립트가 거기서 끊긴다.
const payload = JSON.stringify(campuses).replace(/<\/script/gi, '<\\/script');

const tabs = campuses
  .map(
    (c, i) => `<button class="tab" type="button" role="tab" data-i="${i}"
      aria-selected="${i === 0}" style="--tab-accent:${c.accent}">
      <span class="dot" aria-hidden="true"></span>
      <span class="tab-name">${c.name}</span>
    </button>`
  )
  .join('\n      ');

writeFileSync(
  OUT,
  `<title>애니톡 캠퍼스 프리뷰</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&display=swap">
<style>
:root{
  --ground:#0B0B0D; --panel:#141417; --line:#26262B; --line-hi:#3A3A42;
  --ink:#EDEDEF; --muted:#8E8E96; --muted-2:#63636B;
  --focus:#FF7A18;
}
*,*::before,*::after{box-sizing:border-box}
body{
  margin:0;background:var(--ground);color:var(--ink);
  font-family:'IBM Plex Sans KR',-apple-system,BlinkMacSystemFont,system-ui,'Apple SD Gothic Neo',sans-serif;
  height:100dvh;display:flex;flex-direction:column;overflow:hidden;
  -webkit-font-smoothing:antialiased;
}
:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
button{font:inherit;color:inherit}

header{border-bottom:1px solid var(--line);background:var(--panel);flex:0 0 auto}
.bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding:12px clamp(12px,2vw,20px)}
.mark{display:flex;align-items:baseline;gap:9px;margin-right:2px}
.mark b{font-size:14px;font-weight:700;letter-spacing:-.02em;white-space:nowrap}
.mark span{font-size:11.5px;color:var(--muted-2);white-space:nowrap}

.tabs{display:flex;gap:5px;flex-wrap:wrap;flex:1 1 auto;min-width:0}
.tab{
  display:inline-flex;align-items:center;gap:7px;padding:7px 13px;
  background:transparent;border:1px solid var(--line);border-radius:7px;
  font-size:13px;font-weight:500;cursor:pointer;white-space:nowrap;
  transition:border-color .16s ease,background .16s ease;
}
.tab:hover{border-color:var(--line-hi)}
.tab .dot{width:7px;height:7px;border-radius:50%;background:var(--tab-accent);flex:0 0 auto;
  box-shadow:0 0 0 1px rgba(255,255,255,.14)}
.tab[aria-selected="true"]{background:var(--tab-accent);border-color:var(--tab-accent);color:#fff;font-weight:600}
.tab[aria-selected="true"] .dot{background:#fff;box-shadow:none}
.tab[data-mono][aria-selected="true"]{color:#0B0B0C}
.tab[data-mono][aria-selected="true"] .dot{background:#0B0B0C}

.widths{display:flex;gap:0;border:1px solid var(--line);border-radius:7px;overflow:hidden;flex:0 0 auto}
.widths button{padding:7px 13px;background:transparent;border:0;font-size:12.5px;cursor:pointer;color:var(--muted)}
.widths button + button{border-left:1px solid var(--line)}
.widths button[aria-pressed="true"]{background:#232329;color:var(--ink);font-weight:600}

.meta{display:flex;align-items:center;gap:0 16px;flex-wrap:wrap;
  padding:0 clamp(12px,2vw,20px) 12px;font-size:12px;color:var(--muted)}
.meta dl{display:flex;gap:7px;margin:0}
.meta dt{color:var(--muted-2)}
.meta dd{margin:0;color:var(--ink);font-variant-numeric:tabular-nums}
.meta .url{color:var(--muted-2);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px}

.stage{flex:1 1 auto;min-height:0;display:flex;justify-content:center;
  background:#000;padding:0;overflow:hidden}
.stage.narrow{padding:16px 0;background:#08080A}
iframe{width:100%;height:100%;border:0;background:#000;display:block}
.stage.narrow iframe{width:390px;max-width:100%;border:1px solid var(--line);border-radius:10px}

.note{flex:0 0 auto;border-top:1px solid var(--line);background:var(--panel);
  padding:9px clamp(12px,2vw,20px);font-size:11.5px;line-height:1.6;color:var(--muted-2)}
.note b{color:var(--muted);font-weight:600}
@media (max-width:640px){
  .mark span{display:none}
  .meta{font-size:11.5px}
}
</style>

<header>
  <div class="bar">
    <div class="mark"><b>애니톡 캠퍼스</b><span>7개 지점 랜딩페이지</span></div>
    <div class="tabs" role="tablist" aria-label="지점 선택">
      ${tabs}
    </div>
    <div class="widths" role="group" aria-label="화면 폭">
      <button type="button" data-w="wide" aria-pressed="true">데스크톱</button>
      <button type="button" data-w="narrow" aria-pressed="false">모바일</button>
    </div>
  </div>
  <div class="meta">
    <dl><dt>지점</dt><dd data-m="full"></dd></dl>
    <dl><dt>지역</dt><dd data-m="region"></dd></dl>
    <dl><dt>전화</dt><dd data-m="phone"></dd></dl>
    <dl><dt>테마</dt><dd data-m="theme"></dd></dl>
    <span class="url" data-m="origin"></span>
  </div>
</header>

<div class="stage" id="stage">
  <iframe id="frame" title="지점 사이트 미리보기"></iframe>
</div>

<p class="note"><b>이건 미리보기입니다.</b> 실제 배포될 마크업 그대로지만, 샌드박스가 외부 리소스를 막아서
히어로 사진은 뜨지 않고(플레이스홀더로 대체됨) 본문 폰트는 Pretendard 대신 Noto Sans KR로 보입니다.
Vercel에 올리면 둘 다 정상입니다. 사진 자리는 아직 지점 실사진을 넣기 전이라 비어 있습니다.</p>

<script>
const CAMPUSES = ${payload};
const frame = document.getElementById('frame');
const stage = document.getElementById('stage');
const tabEls = [...document.querySelectorAll('.tab')];
const THEME_LABEL = { orange: '오렌지', mono: '블랙앤화이트', red: '레드' };

tabEls.forEach((t) => {
  if (CAMPUSES[+t.dataset.i].themeName === 'mono') t.setAttribute('data-mono', '');
});

function show(i) {
  const c = CAMPUSES[i];
  tabEls.forEach((t, n) => t.setAttribute('aria-selected', String(n === i)));
  document.querySelector('[data-m="full"]').textContent = c.full;
  document.querySelector('[data-m="region"]').textContent = c.region;
  document.querySelector('[data-m="phone"]').textContent = c.phone;
  document.querySelector('[data-m="theme"]').textContent = THEME_LABEL[c.themeName] || c.themeName;
  document.querySelector('[data-m="origin"]').textContent = c.origin;
  frame.srcdoc = c.html;
}

tabEls.forEach((t) => t.addEventListener('click', () => show(+t.dataset.i)));

document.querySelectorAll('.widths button').forEach((b) => {
  b.addEventListener('click', () => {
    const narrow = b.dataset.w === 'narrow';
    stage.classList.toggle('narrow', narrow);
    document.querySelectorAll('.widths button').forEach((x) =>
      x.setAttribute('aria-pressed', String(x === b))
    );
  });
});

// 좌우 방향키로 지점 넘기기
addEventListener('keydown', (e) => {
  if (e.target.closest('.widths')) return;
  const cur = tabEls.findIndex((t) => t.getAttribute('aria-selected') === 'true');
  if (e.key === 'ArrowRight') show((cur + 1) % tabEls.length);
  if (e.key === 'ArrowLeft') show((cur - 1 + tabEls.length) % tabEls.length);
});

show(0);
</script>
`
);

const kb = Math.round(readFileSync(OUT).length / 1024);
console.log(`프리뷰 생성: ${OUT} (${kb}KB, ${campuses.length}개 지점)`);
