/**
 * 애니톡 캠퍼스 랜딩페이지 렌더러.
 *
 * data/<slug>.json 하나를 받아 완전히 독립 실행 가능한 정적 index.html 문자열을
 * 돌려준다. 일산 사이트(ilsan-anitok.vercel.app)의 디자인 언어를 그대로 따른다:
 * 검정 배경 · 애니톡 레드(#BD0D16) 액센트 · Pretendard · 번호 레이블 · 이모지 없음.
 *
 * 일산 원본은 React UMD로 리스트를 클라이언트 렌더링하지만, 여기서는 전부
 * 빌드 타임에 정적 HTML로 굽는다. 검색엔진이 본문을 그대로 읽고, 런타임 JS는
 * 스크롤 리빌 · 모바일 메뉴 · 갤러리 라이트박스만 담당한다.
 */

/** HTML 텍스트 노드 이스케이프. 데이터의 모든 문자열은 반드시 이 함수를 거친다. */
export function esc(v) {
  return String(v ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** 속성값 안에 들어가는 URL. 스킴을 화이트리스트로 제한한다. */
function url(v) {
  const s = String(v ?? '').trim();
  if (!s) return '';
  if (/^(https?:|tel:|mailto:|#|\/)/i.test(s)) return esc(s);
  return '';
}

/** JSON-LD 안에 넣는 문자열. </script> 탈출을 막는다. */
function jsonld(obj) {
  return JSON.stringify(obj, null, 2).replace(/</g, '\\u003c');
}

const digits = (s) => String(s ?? '').replace(/[^0-9]/g, '');

/** 앞말 받침에 맞는 조사를 고른다. 예) 조사('목동만화학원','을','를') → '을' */
function 조사(word, withBatchim, withoutBatchim) {
  const last = String(word || '').trim().slice(-1);
  const code = last.charCodeAt(0);
  if (!(code >= 0xac00 && code <= 0xd7a3)) return withoutBatchim;
  return (code - 0xac00) % 28 ? withBatchim : withoutBatchim;
}

/**
 * 네이버 예약 주소.
 * data 에 links.naverBooking 이 있으면 그것을 쓰고, 없으면 네이버 플레이스 ID로
 * 예약 탭 주소를 만든다(m.place.naver.com/place/<id>/booking). 해당 업체에
 * 예약이 열려 있지 않으면 네이버가 플레이스 홈으로 넘겨 주므로 링크가 죽지 않는다.
 */
function naverBooking(d) {
  if (d.links?.naverBooking) return d.links.naverBooking;
  const m = /place\/(\d+)/.exec(d.links?.naverPlace || '');
  return m ? `https://m.place.naver.com/place/${m[1]}/booking?entry=ple` : '';
}

/* ─────────────────────────────────────────────────────────────
 * 이미지 슬롯
 *
 * 사진은 세 단계로 해결한다:
 *   1. gal/<local> 파일이 실제로 있으면 그것을 쓴다 (최우선)
 *   2. 없으면 데이터의 remote URL로 폴백 (애니톡 자체 CDN)
 *   3. 둘 다 없으면 캡션이 박힌 플레이스홀더 블록
 * 지점 사진을 gal/ 에 떨궈 넣고 다시 빌드하면 자동으로 1번으로 승격된다.
 * ───────────────────────────────────────────────────────────── */
function resolveImage(slot, present) {
  if (!slot) return null;
  if (slot.local && present.has(slot.local)) return { src: `/gal/${slot.local}`, kind: 'local' };
  if (slot.remote) return { src: slot.remote, kind: 'remote' };
  return null;
}

/** 캡션 없이 이미지(또는 플레이스홀더) 하나만. 카드·라이트박스에서 쓴다. */
function imgOnly(slot, present) {
  const img = resolveImage(slot, present);
  const label = slot?.caption || '사진 준비 중';
  if (!img) {
    return `<div class="ph" role="img" aria-label="${esc(
      label
    )}"><span class="ph-mark">ANITALK</span><span class="ph-cap">${esc(label)}</span></div>`;
  }
  return `<img src="${url(img.src)}" alt="${esc(slot.caption || '')}" loading="lazy" decoding="async">`;
}

function figure(slot, present, { className = 'fig', sizes = '' } = {}) {
  const img = resolveImage(slot, present);
  const cap = slot?.caption ? `<figcaption>${esc(slot.caption)}</figcaption>` : '';
  if (!img) {
    return `<figure class="${className} is-empty"><div class="ph" role="img" aria-label="${esc(
      slot?.caption || '사진 준비 중'
    )}"><span class="ph-mark">ANITALK</span><span class="ph-cap">${esc(
      slot?.caption || '사진 준비 중'
    )}</span></div>${cap}</figure>`;
  }
  const loading = slot.eager ? '' : ' loading="lazy" decoding="async"';
  return `<figure class="${className}"><img src="${url(img.src)}" alt="${esc(
    slot.caption || ''
  )}"${loading}${sizes ? ` sizes="${esc(sizes)}"` : ''}>${cap}</figure>`;
}

/* ───────────────────────────── CSS ───────────────────────────── */

const CSS = `
:root{
  --bg:#000000; --ink:#FFFFFF;
  --panel:#0F0F11; --panel-2:#141416; --line:#232326; --line-2:#33333A;
  --muted:#A8A8AC; --muted-2:#8A8A8A;
  /* 포인트 컬러 토큰 — 지점 테마(themeCss)가 이 값을 덮어쓴다. 기본은 애니톡 레드. */
  --accent:#BD0D16; --accent-lit:#FF3B45; --on-accent:#FFFFFF;
  --accent-line:rgba(255,255,255,.5);
  --mnav-bg:#8E0A10; --mnav-line:rgba(255,255,255,.2);
  --tag-bg:rgba(189,13,22,.92);
  --hero-grad:radial-gradient(120% 90% at 15% 10%,#2A0407 0%,#000 70%);
  --glow-grad:radial-gradient(circle,rgba(189,13,22,.55) 0%,rgba(0,0,0,0) 66%);
  --btn-hover-bg:#FFFFFF; --btn-hover-fg:var(--accent);
  --logo-filter:brightness(0) invert(1);
  --pulse:rgba(189,13,22,.55);
  --pad-y:clamp(96px,12vw,168px); --pad-x:clamp(20px,4vw,48px);
  --wrap:1400px;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{
  margin:0;background:var(--bg);color:var(--ink);
  font-family:'Pretendard Variable',Pretendard,-apple-system,BlinkMacSystemFont,system-ui,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  letter-spacing:-.03em;-webkit-font-smoothing:antialiased;overflow-x:clip;
}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
p,li,dd,dt,h1,h2,h3,h4{word-break:keep-all}
h1,h2,h3,h4{margin:0;font-weight:800;line-height:1.2}
figure{margin:0}
:focus-visible{outline:2px solid var(--accent-lit);outline-offset:3px}

.wrap{max-width:var(--wrap);margin:0 auto;padding-inline:var(--pad-x)}
.sec{padding-block:var(--pad-y)}
.sec--tint{background:var(--panel)}
.kicker{display:block;font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent-lit);margin-bottom:18px}
.h2{font-size:clamp(26px,3.2vw,40px);line-height:1.24;letter-spacing:-.04em}
.lede{margin:18px 0 0;max-width:62ch;font-size:clamp(15px,1.15vw,17px);line-height:1.8;color:var(--muted)}

/* 스크롤 진행 바 + 헤더 */
.progress{position:fixed;top:0;left:0;height:3px;width:0;background:var(--accent);z-index:80}
.hdr{position:sticky;top:0;z-index:60;background:var(--accent);color:var(--on-accent);box-shadow:0 2px 20px rgba(0,0,0,.4)}
.hdr-in{max-width:var(--wrap);margin:0 auto;padding:0 clamp(16px,3vw,36px);height:64px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.brand{display:flex;align-items:center;gap:12px;min-width:0}
/* 원본 로고는 검정 워드마크다. 헤더 글자색에 맞춰 필터로 단색 전환한다. */
.brand-logo{height:26px;width:auto;flex:0 0 auto;filter:var(--logo-filter)}
.brand-div{width:1px;height:20px;background:currentColor;opacity:.4;flex:0 0 auto}
.brand-name{font-size:clamp(14px,1.3vw,17px);font-weight:800;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
@media (max-width:520px){.brand-logo{height:22px}.brand-div,.brand-name{display:none}}
.nav{display:flex;align-items:center;gap:clamp(12px,1.6vw,26px)}
.nav a{font-size:14px;font-weight:600;padding:4px 0;border-bottom:2px solid transparent;white-space:nowrap;transition:border-color .34s cubic-bezier(.16,1,.3,1),opacity .34s cubic-bezier(.16,1,.3,1)}
.nav a:hover{border-bottom-color:currentColor}
.hdr-tel{display:inline-flex;align-items:center;gap:8px;background:var(--on-accent);color:var(--accent);font-size:14px;font-weight:800;padding:9px 18px;border-radius:999px;white-space:nowrap;transition:transform .3s cubic-bezier(.22,1.4,.36,1)}
.hdr-tel:hover{transform:translateY(-2px)}
.burger{display:none;width:42px;height:42px;border:1px solid var(--accent-line);border-radius:8px;background:none;color:var(--on-accent);cursor:pointer;padding:0;align-items:center;justify-content:center}
.burger span{display:block;width:18px;height:2px;background:currentColor;position:relative}
.burger span::before,.burger span::after{content:"";position:absolute;left:0;width:18px;height:2px;background:currentColor}
.burger span::before{top:-6px}.burger span::after{top:6px}
.mnav{display:none;background:var(--mnav-bg);color:var(--on-accent);border-top:1px solid var(--mnav-line)}
.mnav.is-open{display:block}
.mnav a{display:block;padding:15px clamp(16px,4vw,28px);font-size:15px;font-weight:600;border-bottom:1px solid var(--mnav-line)}
@media (max-width:900px){
  .nav,.hdr-tel{display:none}
  .burger{display:inline-flex}
}

/* 히어로 */
.hero{position:relative;overflow:hidden;height:min(94vh,1000px);min-height:640px;display:flex;align-items:center}
.hero-bgw{position:absolute;inset:0;overflow:hidden;will-change:transform}
.hero-bg{position:absolute;inset:0;width:100%;height:112%;object-fit:cover;object-position:center 30%;background:var(--hero-grad);font-size:0;animation:kenburns 26s cubic-bezier(.4,0,.6,1) infinite;will-change:transform}
.hero-bg--none{background:var(--hero-grad)}
.hero-glow{position:absolute;top:0;left:0;width:70vw;height:70vw;max-width:900px;max-height:900px;background:var(--glow-grad);mix-blend-mode:screen;pointer-events:none;animation:heroglow 14s ease-in-out infinite}
.hero-scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.78) 0%,rgba(0,0,0,.42) 46%,rgba(0,0,0,.12) 100%)}
.hero-scrim-b{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.2) 0%,rgba(0,0,0,0) 34%,rgba(0,0,0,.72) 100%)}
.hero-in{position:relative;width:100%;max-width:var(--wrap);margin:0 auto;padding:0 clamp(20px,4vw,56px);will-change:transform,opacity}
.tag{display:inline-flex;align-items:center;gap:8px;background:var(--tag-bg);color:var(--on-accent);border-radius:999px;padding:8px 18px;font-size:13px;font-weight:700;margin-bottom:24px}
.hero h1{font-size:clamp(34px,5.4vw,72px);line-height:1.14;letter-spacing:-.05em;text-shadow:0 6px 34px rgba(0,0,0,.8)}
.hero h1 .over{display:block;font-size:.56em;font-weight:700;letter-spacing:-.03em;margin-bottom:10px}
.hero h1 .lit{color:var(--accent-lit)}
.hero h1[data-reveal]{transform:none}
.hero h1 .w{display:inline-block;will-change:transform,opacity;opacity:0;transform:translateY(.5em);transition:opacity .42s ease-out var(--d,0ms),transform .62s cubic-bezier(.16,1,.3,1) var(--d,0ms)}
.hero h1.is-in .w{opacity:1;transform:none}
.hero-sub{margin:24px 0 0;font-size:clamp(15px,1.6vw,21px);font-weight:700;text-shadow:0 2px 16px rgba(0,0,0,.85)}
.cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}
.btn{display:inline-flex;align-items:center;gap:10px;font-size:16px;font-weight:800;padding:16px 32px;border-radius:999px;transition:transform .52s cubic-bezier(.22,1.4,.36,1),background .32s ease,color .32s ease}
.btn:hover{transform:translateY(-3px) scale(1.03)}
.hero .btn--solid{animation:pulse 2.6s ease-out infinite}
.btn--solid{background:var(--accent);color:var(--on-accent)}
.btn--solid:hover{background:var(--btn-hover-bg);color:var(--btn-hover-fg)}
.btn--ghost{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.4);color:#fff;font-weight:700;backdrop-filter:blur(8px)}
.btn--ghost:hover{background:#fff;color:#111}
.scroll-dot{position:absolute;bottom:26px;left:50%;transform:translateX(-50%);width:22px;height:34px;border:1px solid rgba(255,255,255,.5);border-radius:999px;display:flex;justify-content:center;padding-top:7px}
.scroll-dot i{width:3px;height:6px;border-radius:2px;background:#fff;animation:dot 1.9s cubic-bezier(.2,.8,.2,1) infinite}
@keyframes kenburns{0%,100%{transform:scale(1.06) translate3d(0,0,0)}50%{transform:scale(1.16) translate3d(-1.6%,-1.2%,0)}}
@keyframes heroglow{0%,100%{opacity:.25;transform:translate(-18%,-10%) scale(1)}50%{opacity:.5;transform:translate(-12%,-6%) scale(1.15)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 var(--pulse)}70%{box-shadow:0 0 0 22px rgba(0,0,0,0)}}
@keyframes dot{0%{opacity:0;transform:translateY(0)}40%{opacity:1}100%{opacity:0;transform:translateY(11px)}}

/* about */
.about-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:clamp(28px,4vw,72px);align-items:center}
.about-copy p{margin:0 0 18px;font-size:clamp(15px,1.15vw,17px);line-height:1.85;color:#D6D6D8}
.about-copy p:last-of-type{margin-bottom:0}
.badges{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
.badge{border:1px solid var(--line-2);border-radius:6px;padding:10px 16px;font-size:13px;font-weight:600;color:#D6D6D8;background:var(--panel-2)}
.about-figs{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.about-figs .fig:first-child{grid-column:1/-1}
.fig img,.fig .ph{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:12px}
.about-figs .fig:first-child img,.about-figs .fig:first-child .ph{aspect-ratio:16/9}
@media (max-width:860px){.about-grid{grid-template-columns:1fr}}

/* 플레이스홀더 */
.ph{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;background:
  repeating-linear-gradient(135deg,#141416 0 12px,#101012 12px 24px);
  border:1px solid var(--line);color:var(--muted-2);text-align:center;padding:18px}
.ph-mark{font-size:11px;font-weight:800;letter-spacing:.28em;color:#4A4A50}
.ph-cap{font-size:13px;font-weight:600;line-height:1.5;max-width:22ch}

/* 실적 카드 */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:44px}
.stat{background:var(--panel-2);border:1px solid var(--line);border-radius:14px;padding:clamp(24px,2.4vw,34px);display:flex;flex-direction:column;gap:10px}
.stat-when{font-size:12px;font-weight:700;letter-spacing:.1em;color:var(--accent-lit)}
.stat-label{font-size:15px;font-weight:700;color:#D6D6D8}
.stat-value{font-size:clamp(30px,3.4vw,46px);font-weight:800;letter-spacing:-.05em;line-height:1}
.stat-value .unit{font-size:.42em;font-weight:700;margin-left:6px;letter-spacing:-.02em;color:var(--muted)}
.stat-detail{margin:6px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:5px}
.stat-detail li{font-size:13px;line-height:1.6;color:var(--muted)}

/* 합격 명단 */
.pass{margin:44px 0 0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:0 34px}
.pass li{display:flex;align-items:baseline;gap:12px;padding:15px 2px;border-bottom:1px solid var(--line)}
.pass .yr{flex:0 0 auto;font-size:12px;font-weight:800;color:var(--accent-lit);letter-spacing:.02em}
.pass .what{flex:1 1 auto;font-size:14px;font-weight:600;line-height:1.5}
.pass .who{flex:0 0 auto;font-size:13px;color:var(--muted-2)}
.note{margin:26px 0 0;font-size:13px;line-height:1.7;color:var(--muted-2)}

/* 수업 과목 */
.class-group{margin-top:56px}
.class-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:14px;padding-bottom:16px;border-bottom:1px solid var(--line-2)}
.class-no{font-size:12px;font-weight:800;letter-spacing:.16em;color:var(--accent-lit)}
.class-name{font-size:clamp(20px,2vw,26px);letter-spacing:-.04em}
.class-range{font-size:13px;font-weight:700;color:var(--muted)}
.class-lead{margin:14px 0 0;font-size:14px;line-height:1.8;color:var(--muted);max-width:70ch}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;margin-top:26px}
.card{background:var(--panel-2);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transform-style:preserve-3d}
.card img{transform-origin:center;will-change:transform}
.card img,.card .ph{width:100%;aspect-ratio:4/3;object-fit:cover;border:0;border-radius:0}
.card-body{padding:20px;display:flex;flex-direction:column;gap:8px}
.card-eyebrow{font-size:12px;font-weight:700;letter-spacing:.08em;color:var(--accent-lit)}
.card-title{font-size:18px;letter-spacing:-.03em}
.card-desc{margin:0;font-size:13.5px;line-height:1.75;color:var(--muted)}

/* 갤러리 */
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:38px}
.gal .fig img,.gal .fig .ph{aspect-ratio:1/1;border-radius:12px}
.gal .fig{position:relative}
.gal figcaption{margin-top:9px;font-size:12.5px;color:var(--muted-2);line-height:1.5}
.gal button.shot{display:block;width:100%;padding:0;border:0;background:none;cursor:zoom-in}

/* 과정 */
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:44px;counter-reset:s}
.step{border:1px solid var(--line);border-radius:12px;padding:26px 20px;background:var(--panel-2)}
.step-no{font-size:12px;font-weight:800;letter-spacing:.16em;color:var(--accent-lit)}
.step-name{margin-top:12px;font-size:16px;font-weight:700;line-height:1.4}

/* FAQ */
.faq{margin-top:40px;border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{list-style:none;cursor:pointer;padding:22px 44px 22px 34px;position:relative;font-size:16px;font-weight:700;line-height:1.55}
.faq summary::-webkit-details-marker{display:none}
.faq summary::before{content:"Q";position:absolute;left:0;top:22px;font-size:14px;font-weight:800;color:var(--accent-lit)}
.faq summary::after{content:"";position:absolute;right:6px;top:30px;width:9px;height:9px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg);transition:transform .25s ease}
.faq details[open] summary::after{transform:rotate(-135deg)}
.faq .ans{padding:0 34px 26px;font-size:14.5px;line-height:1.85;color:var(--muted)}
.faq .ans a{color:var(--accent-lit);text-decoration:underline;text-underline-offset:3px}

/* 오시는 길 / 푸터 */
.visit{background:var(--panel);border-top:1px solid var(--line)}
.visit-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px;margin-top:44px}
.vcard{border:1px solid var(--line);border-radius:14px;padding:clamp(24px,2.4vw,32px);background:var(--panel-2);display:flex;flex-direction:column;gap:10px}
.vcard h3{font-size:13px;font-weight:800;letter-spacing:.14em;color:var(--accent-lit)}
.vcard p{margin:0;font-size:15px;line-height:1.75;color:#D6D6D8}
.vcard .big{font-size:20px;font-weight:800;letter-spacing:-.03em}
.vcard a.more{margin-top:6px;font-size:14px;font-weight:700;color:#fff;border-bottom:1px solid var(--line-2);padding-bottom:4px;align-self:flex-start}
.vcard a.more:hover{border-bottom-color:var(--accent-lit)}
.social{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}
.social a{border:1px solid var(--line-2);border-radius:6px;padding:9px 15px;font-size:13px;font-weight:600;color:#D6D6D8}
.social a:hover{border-color:var(--accent-lit);color:#fff}
.foot{border-top:1px solid var(--line);padding-block:40px;font-size:12.5px;line-height:1.9;color:var(--muted-2)}
.foot-logo{height:24px;width:auto;margin-bottom:24px;filter:brightness(0) invert(1);opacity:.85}
.foot .sites{display:flex;flex-wrap:wrap;gap:8px 18px;margin-bottom:22px}
.foot .sites a{font-size:13px;font-weight:600;color:var(--muted)}
.foot .sites a:hover{color:#fff}

/* 모바일 하단 고정 바 */
.qbar{position:fixed;left:0;right:0;bottom:0;z-index:70;display:none;grid-template-columns:1fr 1fr;gap:1px;background:var(--line)}
.qbar a{padding:15px 8px;text-align:center;font-size:14px;font-weight:800;background:#141416}
.qbar a.pri{background:var(--accent);color:var(--on-accent)}
@media (max-width:760px){.qbar{display:grid}body{padding-bottom:54px}}

/* 라이트박스 */
.lb{position:fixed;inset:0;z-index:100;background:rgba(0,0,0,.94);display:none;align-items:center;justify-content:center;padding:24px}
.lb.is-open{display:flex}
.lb img{max-width:min(1200px,92vw);max-height:88vh;width:auto;object-fit:contain;border-radius:6px}
.lb-close{position:absolute;top:18px;right:20px;width:44px;height:44px;border:1px solid var(--line-2);border-radius:50%;background:none;color:#fff;font-size:22px;cursor:pointer;line-height:1}

/* 스크롤 리빌 */
[data-reveal]{opacity:0;transform:translateY(26px);will-change:transform,opacity;transition:opacity .38s ease-out,transform .58s cubic-bezier(.16,1,.3,1)}
[data-reveal].is-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  [data-reveal]{opacity:1;transform:none;transition:none}
  .hero h1 .w{opacity:1;transform:none;transition:none}
  .hero-bg,.hero-glow,.hero .btn--solid{animation:none}
  .scroll-dot i{animation:none}
}
`;

/* ───────────────────── 모바일 최적화 · 랜딩페이지 ─────────────────────
 * 이 블록은 위 기본 스타일을 덮어쓴다. 순서를 바꾸지 말 것.
 * ───────────────────────────────────────────────────────────────── */
const CSS_MOBILE = `
/* 터치 기기 기본기 */
html{-webkit-text-size-adjust:100%}
body{-webkit-tap-highlight-color:transparent}
a,button,summary{touch-action:manipulation}

/* 화면 밖 섹션은 그릴 필요가 없다. 저사양 안드로이드에서 스크롤이 확 가벼워진다. */
.sec{content-visibility:auto;contain-intrinsic-size:auto 900px}
.hero,.visit{content-visibility:visible}

/* 히어로 — 모바일 브라우저 주소창 때문에 100vh가 잘린다. svh로 맞춘다. */
@supports (height:100svh){.hero{height:min(94svh,1000px)}}

@media (max-width:900px){
  :root{--pad-y:clamp(68px,11vw,120px)}
  .hero{height:auto;min-height:auto;padding-block:clamp(104px,22vw,150px) clamp(76px,16vw,110px)}
  @supports (height:100svh){.hero{height:auto;min-height:88svh}}
  .hero h1{font-size:clamp(29px,7.6vw,46px);line-height:1.18;letter-spacing:-.045em}
  .hero h1 .over{font-size:.6em;margin-bottom:8px}
  .hero-sub{font-size:clamp(14px,4vw,18px);margin-top:18px}
  .tag{font-size:12px;padding:7px 14px;margin-bottom:18px;line-height:1.45}
  .hero-scrim{background:linear-gradient(90deg,rgba(0,0,0,.82) 0%,rgba(0,0,0,.62) 60%,rgba(0,0,0,.42) 100%)}
  .hero-glow{width:110vw;height:110vw}
  .scroll-dot{display:none}
  .cta-row{margin-top:26px;gap:10px}
  /* 손가락으로 누르는 버튼은 화면 폭을 꽉 채우는 편이 실수가 없다. */
  .cta-row .btn{flex:1 1 100%;justify-content:center;padding:15px 20px;font-size:15px;min-height:52px}
}

@media (max-width:760px){
  .h2{font-size:clamp(22px,5.6vw,32px)}
  .lede{font-size:15px;line-height:1.75}
  .about-figs{gap:10px}
  /* 220px 최소폭이면 375px 화면에서 1열이 된다. 사진 갤러리는 2열이 훨씬 낫다. */
  .gal{grid-template-columns:repeat(auto-fill,minmax(min(46%,150px),1fr));gap:10px;margin-top:28px}
  .gal figcaption{font-size:11.5px;margin-top:7px}
  .cards{grid-template-columns:1fr;gap:12px}
  .stats{grid-template-columns:1fr;gap:10px}
  .pass{grid-template-columns:1fr}
  .steps{grid-template-columns:repeat(auto-fit,minmax(min(46%,140px),1fr));gap:10px}
  .step{padding:20px 16px}
  .visit-grid{grid-template-columns:1fr;gap:10px}
  .class-group{margin-top:38px}
  .faq summary{padding:19px 40px 19px 28px;font-size:15px}
  .faq summary::before{top:19px}
  .faq summary::after{top:26px}
  .faq .ans{padding:0 28px 22px;font-size:14px}
  .social a{padding:11px 16px}
  .foot .sites{gap:10px 16px}
  .foot .sites a{padding:4px 0}
}

@media (max-width:400px){
  :root{--pad-x:18px}
  .btn{font-size:15px;padding:15px 22px}
  .badge{font-size:12px;padding:9px 13px}
}

/* 하단 고정 바 — 3개 액션. 아이폰 홈 인디케이터를 피해서 앉힌다. */
.qbar{grid-template-columns:repeat(3,1fr);padding-bottom:env(safe-area-inset-bottom,0px);background:var(--line)}
.qbar a{display:flex;align-items:center;justify-content:center;min-height:54px;padding:10px 4px;font-size:13.5px;letter-spacing:-.04em;line-height:1.25}
.qbar a .sm{font-size:12px;font-weight:700}
@media (max-width:760px){body{padding-bottom:calc(56px + env(safe-area-inset-bottom,0px))}}
@media (max-width:340px){.qbar a{font-size:12.5px}}

/* 라이트박스 — 모바일에서 배경이 같이 스크롤되지 않게 */
.lb{overscroll-behavior:contain;padding:16px}
.lb-close{top:calc(12px + env(safe-area-inset-top,0px));right:12px}

/* ── 지역 랜딩페이지 ── */
.lp-head{padding-block:clamp(84px,10vw,132px) clamp(40px,5vw,64px);background:var(--hero-grad);border-bottom:1px solid var(--line)}
.crumb{font-size:12.5px;color:var(--muted-2);margin-bottom:20px;display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.crumb a{color:var(--muted);border-bottom:1px solid transparent}
.crumb a:hover{color:#fff;border-bottom-color:var(--accent-lit)}
.crumb span[aria-hidden]{opacity:.5}
.lp-h1{font-size:clamp(28px,4.4vw,52px);line-height:1.2;letter-spacing:-.045em}
.lp-h1 .lit{color:var(--accent-lit)}
.lp-sub{margin:20px 0 0;max-width:64ch;font-size:clamp(15px,1.2vw,18px);line-height:1.8;color:#D6D6D8}
.prose p{margin:0 0 18px;font-size:clamp(15px,1.15vw,17px);line-height:1.9;color:#D6D6D8;max-width:72ch}
.prose p:last-child{margin-bottom:0}
.lp-points{margin:32px 0 0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.lp-points li{background:var(--panel-2);border:1px solid var(--line);border-radius:12px;padding:20px 22px}
.lp-points b{display:block;font-size:15px;margin-bottom:8px;letter-spacing:-.03em}
.lp-points span{font-size:13.5px;line-height:1.75;color:var(--muted)}
@media (max-width:760px){.lp-points{grid-template-columns:1fr}}
.lp-list{margin:32px 0 0;padding:0;list-style:none;border-top:1px solid var(--line)}
.lp-list li{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;padding:15px 2px;border-bottom:1px solid var(--line);font-size:14.5px;line-height:1.6}
.lp-list .k{flex:0 0 auto;font-size:12px;font-weight:800;letter-spacing:.02em;color:var(--accent-lit);min-width:74px}
.lp-list .v{flex:1 1 220px;font-weight:600}
.lp-list .m{flex:0 0 auto;font-size:13px;color:var(--muted-2)}
.lp-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:32px}
.lp-links a{border:1px solid var(--line-2);border-radius:999px;padding:10px 18px;font-size:13.5px;font-weight:600;color:#D6D6D8;background:var(--panel-2);min-height:44px;display:inline-flex;align-items:center}
.lp-links a:hover{border-color:var(--accent-lit);color:#fff}
.lp-links a[aria-current]{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}
.lp-cta{background:var(--panel);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.lp-cta .cta-row{margin-top:28px}
.lp-cta .btn{min-height:54px}
`;

/* ─────────────────────────── 테마 ───────────────────────────
 * 지점마다 포인트 컬러가 다르다. 색은 전부 CSS 변수 한 곳에서만 갈리므로
 * data/_shared.json 의 themes 에 항목을 추가하고 지점 데이터에서 theme 이름만
 * 지정하면 된다. 마크업과 레이아웃은 전 지점이 동일하다.
 * ───────────────────────────────────────────────────────────── */
const THEME_KEYS = {
  accent: '--accent',
  accentLit: '--accent-lit',
  onAccent: '--on-accent',
  accentLine: '--accent-line',
  mnavBg: '--mnav-bg',
  mnavLine: '--mnav-line',
  tagBg: '--tag-bg',
  heroGrad: '--hero-grad',
  glowGrad: '--glow-grad',
  btnHoverBg: '--btn-hover-bg',
  btnHoverFg: '--btn-hover-fg',
  logoFilter: '--logo-filter',
  pulse: '--pulse',
};

/** 지점 테마를 :root 오버라이드로 뽑는다. 값이 없는 키는 기본(레드)을 그대로 쓴다. */
function themeCss(theme) {
  if (!theme) return '';
  const rules = Object.entries(THEME_KEYS)
    .filter(([k]) => theme[k])
    .map(([k, v]) => `${v}:${String(theme[k]).replace(/[<>]/g, '')}`)
    .join(';');
  return rules ? `\n:root{${rules}}` : '';
}

/* ───────────────────────────── JS ───────────────────────────── */

const JS = `
(function(){
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 이미지가 못 뜨면(원격 CDN 삭제·차단 등) 깨진 아이콘 대신 플레이스홀더로 바꾼다.
  document.addEventListener('error', function(e){
    var img = e.target;
    if (!img || img.tagName !== 'IMG' || img.dataset.fellBack) return;
    img.dataset.fellBack = '1';
    if (img.classList.contains('hero-bg')) {
      var d = document.createElement('div');
      d.className = 'hero-bg hero-bg--none';
      img.replaceWith(d);
      return;
    }
    var ph = document.createElement('div');
    ph.className = 'ph';
    ph.setAttribute('role', 'img');
    ph.setAttribute('aria-label', img.alt || '사진 준비 중');
    ph.innerHTML = '<span class="ph-mark">ANITALK</span><span class="ph-cap"></span>';
    ph.querySelector('.ph-cap').textContent = img.alt || '사진 준비 중';
    var btn = img.closest('button.shot');
    (btn || img).replaceWith(ph);
  }, true);

  // 스크롤 진행 바
  var bar = document.querySelector('[data-progress]');
  if (bar) {
    var tick = false;
    addEventListener('scroll', function(){
      if (tick) return; tick = true;
      requestAnimationFrame(function(){
        var h = document.documentElement.scrollHeight - innerHeight;
        bar.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + '%';
        tick = false;
      });
    }, { passive: true });
  }

  // 히어로 제목: 단어 단위로 쪼개 순차 등장 (80ms부터 38ms 간격)
  var h1 = document.querySelector('.hero h1');
  if (h1 && !rm) {
    var n = 0;
    var split = function(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(ch){
        if (ch.nodeType === 3) {
          var parts = ch.textContent.split(/(\\s+)/).filter(function(t){ return t.length; });
          if (!parts.length) return;
          var frag = document.createDocumentFragment();
          parts.forEach(function(p){
            if (/^\\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            var w = document.createElement('span');
            w.className = 'w';
            w.textContent = p;
            w.style.setProperty('--d', (80 + n++ * 38) + 'ms');
            frag.appendChild(w);
          });
          node.replaceChild(frag, ch);
        } else if (ch.nodeType === 1 && ch.tagName !== 'BR') {
          split(ch);
        }
      });
    };
    split(h1);
  }

  // 스크롤 리빌
  var pending = [];
  var targets = document.querySelectorAll('[data-reveal]');
  var play = function(el){
    var d = parseInt(el.getAttribute('data-reveal'), 10) || 0;
    setTimeout(function(){ el.classList.add('is-in'); }, d);
  };
  if (rm || !('IntersectionObserver' in window)) {
    targets.forEach(function(el){ el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        var i = pending.indexOf(e.target);
        if (i > -1) pending.splice(i, 1);
        play(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });
    targets.forEach(function(el){ pending.push(el); io.observe(el); });
  }

  // 실적 숫자 카운트업 (1.2초, ease-out cubic)
  if (!rm && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        cio.unobserve(e.target);
        var node = e.target.firstChild;
        var target = parseInt(node.textContent, 10);
        var dur = 1200, t0 = performance.now();
        var tick = function(t){
          var p = Math.min(1, (t - t0) / dur);
          node.textContent = String(Math.round(target * (1 - Math.pow(1 - p, 3))));
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.4 });
    document.querySelectorAll('.stat-value').forEach(function(el){
      var f = el.firstChild;
      if (f && f.nodeType === 3 && /^\\d+$/.test(f.textContent.trim())) cio.observe(el);
    });
  }

  // 카드 스프링 틸트 (마우스 위치 따라 기울고, 떼면 감쇠하며 복귀)
  if (!rm && matchMedia('(hover:hover)').matches) {
    document.querySelectorAll('.card, .stat, .vcard').forEach(function(card){
      var img = card.querySelector('img');
      var S = { v: 0, x: 0, tx: 0, rx: 0, ry: 0, trx: 0, try_: 0, raf: null };
      var K = 0.13, D = 0.78;
      var frame = function(){
        S.v += (S.tx - S.x) * K; S.v *= D; S.x += S.v;
        S.rx += (S.trx - S.rx) * 0.16; S.ry += (S.try_ - S.ry) * 0.16;
        var lift = S.x;
        card.style.transform = 'perspective(900px) translate3d(0,' + (-lift * 12).toFixed(2) + 'px,0) rotateX(' + S.rx.toFixed(3) + 'deg) rotateY(' + S.ry.toFixed(3) + 'deg) scale(' + (1 + lift * 0.022).toFixed(4) + ')';
        card.style.boxShadow = lift > 0.004 ? '0 ' + (lift * 26).toFixed(1) + 'px ' + (lift * 52).toFixed(1) + 'px rgba(0,0,0,' + (lift * 0.5).toFixed(3) + ')' : 'none';
        if (img) img.style.transform = 'scale(' + (1 + lift * 0.075).toFixed(4) + ')';
        var settled = Math.abs(S.tx - S.x) < 0.0012 && Math.abs(S.v) < 0.0012 && Math.abs(S.trx - S.rx) < 0.01 && Math.abs(S.try_ - S.ry) < 0.01;
        S.raf = settled ? null : requestAnimationFrame(frame);
      };
      var kick = function(){ if (S.raf == null) S.raf = requestAnimationFrame(frame); };
      card.addEventListener('mouseenter', function(){ S.tx = 1; kick(); });
      card.addEventListener('mousemove', function(ev){
        var r = card.getBoundingClientRect();
        var px = (ev.clientX - r.left) / r.width - 0.5;
        var py = (ev.clientY - r.top) / r.height - 0.5;
        S.try_ = px * 7; S.trx = -py * 7; kick();
      });
      card.addEventListener('mouseleave', function(){ S.tx = 0; S.trx = 0; S.try_ = 0; kick(); });
    });
  }

  // 스크롤 연동 패럴랙스: 임계 감쇠로 휠을 멈춘 뒤에도 잠시 미끄러진다
  var bgw = document.querySelector('[data-parallax]');
  var heroIn = document.querySelector('.hero-in');
  if (!rm && bgw) {
    var ys = scrollY, idle = 0, raf = null;
    var paint = function(y){
      var vh = innerHeight || 1;
      var p = Math.min(1, y / vh);
      bgw.style.transform = 'translate3d(0,' + (y * 0.25).toFixed(1) + 'px,0)';
      bgw.style.filter = 'brightness(' + (1 - p * 0.35).toFixed(3) + ')';
      if (heroIn) {
        heroIn.style.transform = 'translate3d(0,' + (y * 0.18).toFixed(1) + 'px,0)';
        heroIn.style.opacity = String(Math.max(0, 1 - p * 1.3).toFixed(3));
      }
    };
    var loop = function(){
      var y = scrollY;
      ys += (y - ys) * 0.14;
      if (Math.abs(y - ys) < 0.15) ys = y;
      paint(ys);
      // 관찰자가 놓친 요소도 화면에 들어왔으면 재생한다
      if (pending.length) {
        var vh = innerHeight;
        pending.slice().forEach(function(el){
          var r = el.getBoundingClientRect();
          if (r.top < vh * 0.94 && r.bottom > 0) { pending.splice(pending.indexOf(el), 1); play(el); }
        });
      }
      idle = Math.abs(y - ys) > 0.15 ? 0 : idle + 1;
      raf = idle > 90 ? null : requestAnimationFrame(loop);
    };
    var kickLoop = function(){ idle = 0; if (raf == null) raf = requestAnimationFrame(loop); };
    addEventListener('scroll', kickLoop, { passive: true });
    addEventListener('resize', kickLoop);
    raf = requestAnimationFrame(loop);
  }

  // 모바일 메뉴
  var burger = document.querySelector('[data-burger]');
  var mnav = document.querySelector('[data-mnav]');
  if (burger && mnav) {
    burger.addEventListener('click', function(){
      var open = mnav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    mnav.addEventListener('click', function(e){
      if (e.target.closest('a')) {
        mnav.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 앵커 이동 시 sticky 헤더 높이만큼 보정
  document.addEventListener('click', function(e){
    var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var id = a.getAttribute('href');
    if (!id || id === '#') return;
    var el = document.querySelector(id);
    if (!el) return;
    e.preventDefault();
    var y = el.getBoundingClientRect().top + scrollY - 76;
    scrollTo({ top: y, behavior: rm ? 'auto' : 'smooth' });
    if (history.replaceState) history.replaceState(null, '', id);
  });

  // 갤러리 라이트박스
  var lb = document.querySelector('[data-lb]');
  if (lb) {
    var lbImg = lb.querySelector('img');
    var last = null;
    document.addEventListener('click', function(e){
      var b = e.target.closest ? e.target.closest('button.shot') : null;
      if (!b) return;
      var img = b.querySelector('img');
      if (!img) return;
      last = b;
      lbImg.src = img.currentSrc || img.src;
      lbImg.alt = img.alt || '';
      lb.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      lb.querySelector('.lb-close').focus();
    });
    function close(){
      lb.classList.remove('is-open');
      lbImg.removeAttribute('src');
      document.body.style.overflow = '';
      if (last) last.focus();
    }
    lb.addEventListener('click', function(e){
      if (e.target === lb || e.target.closest('.lb-close')) close();
    });
    addEventListener('keydown', function(e){
      if (e.key === 'Escape' && lb.classList.contains('is-open')) close();
    });
  }
})();
`;

/* ─────────────────────────── 섹션 ─────────────────────────── */

function header(d, { base = '' } = {}) {
  // 랜딩페이지에서는 앵커(#about)가 그 페이지에 없다. base를 붙여 홈으로 보낸다.
  const href = (h) => (base && String(h).startsWith('#') ? base + h : h);
  const nav = (d.nav || []).map((n) => `<a href="${url(href(n.href))}">${esc(n.label)}</a>`).join('');
  const mnav = nav;
  const booking = naverBooking(d);
  return `<div class="progress" data-progress></div>
<header class="hdr">
  <div class="hdr-in">
    <a class="brand" href="${url(base || '#top')}">
      <img class="brand-logo" src="${url(d.brandLogo)}" alt="애니톡" width="98" height="26" fetchpriority="high">
      <span class="brand-div" aria-hidden="true"></span>
      <span class="brand-name">${esc(d.name)}</span>
    </a>
    <nav class="nav" aria-label="주요 메뉴">${nav}</nav>
    <a class="hdr-tel" href="tel:${esc(digits(d.phone))}">${esc(d.phone)}</a>
    <button class="burger" type="button" data-burger aria-expanded="false" aria-controls="mnav" aria-label="메뉴 열기"><span></span></button>
  </div>
  <nav class="mnav" id="mnav" data-mnav aria-label="모바일 메뉴">${mnav}${
    booking ? `<a href="${url(booking)}" target="_blank" rel="noopener">네이버 예약</a>` : ''
  }<a href="tel:${esc(digits(d.phone))}">전화 ${esc(d.phone)}</a></nav>
</header>`;
}

function hero(d, present) {
  const bg = resolveImage(d.hero.image, present);
  // 히어로 배경은 장식 요소다. 캠퍼스 이름은 h1이 이미 말하고 있으므로 alt는 비우고,
  // 이미지가 못 뜰 때 alt 텍스트가 화면 구석에 남지 않게 한다.
  const bgEl = bg
    ? `<div class="hero-bgw" data-parallax><img class="hero-bg" src="${url(bg.src)}" alt="" role="presentation" fetchpriority="high"></div>`
    : `<div class="hero-bgw" data-parallax><div class="hero-bg hero-bg--none" role="presentation"></div></div>`;
  const booking = naverBooking(d);
  // 상담 신청 → 네이버 예약 → 전화. 예약을 두 번째에 두어 가장 눈에 띄게 한다.
  const list = [...(d.hero.ctas || [])];
  if (booking) list.splice(1, 0, { label: '네이버 예약 →', href: booking });
  const ctas = list
    .map(
      (c, i) =>
        `<a class="btn ${i === 0 ? 'btn--solid' : 'btn--ghost'}" href="${url(c.href)}"${
          /^https?:/i.test(c.href) ? ' target="_blank" rel="noopener"' : ''
        }>${esc(c.label)}</a>`
    )
    .join('');
  return `<section class="hero" id="top">
  ${bgEl}
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="hero-scrim" aria-hidden="true"></div>
  <div class="hero-scrim-b" aria-hidden="true"></div>
  <div class="hero-in">
    ${d.hero.tag ? `<p class="tag" data-reveal="0">${esc(d.hero.tag)}</p>` : ''}
    <h1 data-reveal="80"><span class="over">${esc(d.hero.over)}</span>${esc(
    d.hero.line1
  )}<br><span class="lit">${esc(d.hero.line2)}</span></h1>
    <p class="hero-sub" data-reveal="160">${esc(d.hero.sub)}</p>
    <div class="cta-row" data-reveal="240">${ctas}</div>
  </div>
  <div class="scroll-dot" aria-hidden="true"><i></i></div>
</section>`;
}

function about(d, present) {
  const figs = (d.about.figures || []).map((f) => figure(f, present)).join('');
  const paras = (d.about.paragraphs || []).map((p) => `<p>${esc(p)}</p>`).join('');
  const badges = (d.about.badges || []).map((b) => `<span class="badge">${esc(b)}</span>`).join('');
  return `<section class="sec" id="about">
  <div class="wrap">
    <div class="about-grid">
      <div class="about-copy" data-reveal="0">
        <span class="kicker">${esc(d.about.kicker)}</span>
        <h2 class="h2">${esc(d.about.title)}</h2>
        <div style="margin-top:24px">${paras}</div>
        ${badges ? `<div class="badges">${badges}</div>` : ''}
      </div>
      <div class="about-figs" data-reveal="120">${figs}</div>
    </div>
  </div>
</section>`;
}

function results(d) {
  if (!d.results?.items?.length) return '';
  const cards = d.results.items
    .map(
      (s, i) => `<article class="stat" data-reveal="${i * 60}">
      ${s.when ? `<span class="stat-when">${esc(s.when)}</span>` : ''}
      <span class="stat-label">${esc(s.label)}</span>
      <span class="stat-value">${esc(s.value)}${
        s.unit ? `<span class="unit">${esc(s.unit)}</span>` : ''
      }</span>
      ${
        s.detail?.length
          ? `<ul class="stat-detail">${s.detail.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>`
          : ''
      }
    </article>`
    )
    .join('');
  return `<section class="sec sec--tint" id="results">
  <div class="wrap">
    <span class="kicker" data-reveal="0">${esc(d.results.kicker)}</span>
    <h2 class="h2" data-reveal="40">${esc(d.results.title)}</h2>
    ${d.results.lede ? `<p class="lede" data-reveal="80">${esc(d.results.lede)}</p>` : ''}
    <div class="stats">${cards}</div>
    ${d.results.note ? `<p class="note" data-reveal="0">${esc(d.results.note)}</p>` : ''}
  </div>
</section>`;
}

function passList(d) {
  if (!d.passList?.items?.length) return '';
  const rows = d.passList.items
    .map(
      (p) => `<li><span class="yr">${esc(p.year)}</span><span class="what">${esc(
        p.what
      )}</span>${p.who ? `<span class="who">${esc(p.who)}</span>` : ''}</li>`
    )
    .join('');
  return `<section class="sec" id="college">
  <div class="wrap">
    <span class="kicker" data-reveal="0">${esc(d.passList.kicker)}</span>
    <h2 class="h2" data-reveal="40">${esc(d.passList.title)}</h2>
    ${d.passList.lede ? `<p class="lede" data-reveal="80">${esc(d.passList.lede)}</p>` : ''}
    <ul class="pass" data-reveal="0">${rows}</ul>
    ${d.passList.note ? `<p class="note">${esc(d.passList.note)}</p>` : ''}
  </div>
</section>`;
}

function classes(d, present) {
  if (!d.classes?.groups?.length) return '';
  const groups = d.classes.groups
    .map((g, gi) => {
      const cards = (g.items || [])
        .map(
          (c) => `<article class="card">
        ${imgOnly(c.image, present)}
        <div class="card-body">
          <span class="card-eyebrow">${esc(c.eyebrow)}</span>
          <h4 class="card-title">${esc(c.title)}</h4>
          <p class="card-desc">${esc(c.desc)}</p>
        </div>
      </article>`
        )
        .join('');
      return `<div class="class-group" data-reveal="${gi * 60}">
      <div class="class-head">
        <span class="class-no">CLASS ${String(gi + 1).padStart(2, '0')}</span>
        <h3 class="class-name">${esc(g.name)}</h3>
        <span class="class-range">${esc(g.range)}</span>
      </div>
      <p class="class-lead">${esc(g.lead)}</p>
      <div class="cards">${cards}</div>
    </div>`;
    })
    .join('');
  return `<section class="sec sec--tint" id="classes">
  <div class="wrap">
    <span class="kicker" data-reveal="0">${esc(d.classes.kicker)}</span>
    <h2 class="h2" data-reveal="40">${esc(d.classes.title)}</h2>
    ${d.classes.lede ? `<p class="lede" data-reveal="80">${esc(d.classes.lede)}</p>` : ''}
    ${groups}
  </div>
</section>`;
}

function galleries(d, present) {
  if (!d.galleries?.length) return '';
  return d.galleries
    .map((g, gi) => {
      const shots = (g.items || [])
        .map((s) => {
          const cap = s.caption ? `<figcaption>${esc(s.caption)}</figcaption>` : '';
          // 실제 이미지가 있을 때만 라이트박스 버튼으로 감싼다
          if (!resolveImage(s, present)) {
            return `<figure class="fig is-empty">${imgOnly(s, present)}${cap}</figure>`;
          }
          return `<figure class="fig"><button class="shot" type="button" aria-label="${esc(
            s.caption || '사진 크게 보기'
          )}">${imgOnly(s, present)}</button>${cap}</figure>`;
        })
        .join('');
      return `<section class="sec${gi % 2 ? ' sec--tint' : ''}" id="${esc(g.id)}">
  <div class="wrap">
    <span class="kicker" data-reveal="0">${esc(g.kicker)}</span>
    <h2 class="h2" data-reveal="40">${esc(g.title)}</h2>
    ${g.lede ? `<p class="lede" data-reveal="80">${esc(g.lede)}</p>` : ''}
    <div class="gal" data-reveal="0">${shots}</div>
  </div>
</section>`;
    })
    .join('');
}

function process(d) {
  if (!d.process?.steps?.length) return '';
  const steps = d.process.steps
    .map(
      (s, i) => `<div class="step" data-reveal="${i * 50}">
      <span class="step-no">${String(i + 1).padStart(2, '0')}</span>
      <p class="step-name">${esc(s)}</p>
    </div>`
    )
    .join('');
  return `<section class="sec" id="process">
  <div class="wrap">
    <span class="kicker" data-reveal="0">${esc(d.process.kicker)}</span>
    <h2 class="h2" data-reveal="40">${esc(d.process.title)}</h2>
    <div class="steps">${steps}</div>
  </div>
</section>`;
}

function faq(d) {
  if (!d.faq?.items?.length) return '';
  const rows = d.faq.items
    .map(
      (f) => `<details><summary>${esc(f.q)}</summary><div class="ans">${esc(f.a)}</div></details>`
    )
    .join('');
  return `<section class="sec sec--tint" id="faq">
  <div class="wrap">
    <span class="kicker" data-reveal="0">FAQ</span>
    <h2 class="h2" data-reveal="40">${esc(d.faq.title)}</h2>
    ${d.faq.lede ? `<p class="lede" data-reveal="80">${esc(d.faq.lede)}</p>` : ''}
    <div class="faq" data-reveal="0">${rows}</div>
  </div>
</section>`;
}

function visit(d, siblings) {
  const booking = naverBooking(d);
  const social = [
    d.links.naverPlace && { label: '네이버 지도', href: d.links.naverPlace },
    d.links.blog && { label: '블로그', href: d.links.blog },
    d.links.instagram && { label: '인스타그램', href: d.links.instagram },
  ].filter(Boolean);
  const sibs = (siblings || [])
    .filter((s) => s.slug !== d.slug)
    .map((s) => `<a href="${url(s.href)}"${/^https?:/i.test(s.href) ? ' target="_blank" rel="noopener"' : ''}>${esc(s.label)}</a>`)
    .join('');
  return `<section class="sec visit" id="visit">
  <div class="wrap">
    <span class="kicker" data-reveal="0">Visit</span>
    <h2 class="h2" data-reveal="40">${esc(d.visit.title)}</h2>
    <div class="visit-grid">
      <div class="vcard" data-reveal="0">
        <h3>오시는 길</h3>
        <p>${esc(d.address.line1)}<br>${esc(d.address.line2)}</p>
        ${
          d.links.naverPlace
            ? `<a class="more" href="${url(
                d.links.naverPlace
              )}" target="_blank" rel="noopener">네이버 지도로 보기 &rarr;</a>`
            : ''
        }
      </div>
      <div class="vcard" data-reveal="60">
        <h3>전화 문의</h3>
        <p class="big">${esc(d.phone)}</p>
        <p>${esc(d.hours.line1)}<br>${esc(d.hours.line2)}</p>
        <a class="more" href="tel:${esc(digits(d.phone))}">바로 전화하기 &rarr;</a>
      </div>
      ${
        booking
          ? `<div class="vcard" data-reveal="120">
        <h3>네이버 예약</h3>
        <p>네이버 예약으로 상담 시간을 바로 잡을 수 있습니다. 원하는 날짜와 시간을 선택해 주세요.</p>
        <a class="more" href="${url(booking)}" target="_blank" rel="noopener">네이버로 예약하기 &rarr;</a>
      </div>`
          : ''
      }
      <div class="vcard" data-reveal="${booking ? 180 : 120}">
        <h3>온라인 상담</h3>
        <p>${esc(d.visit.consult)}</p>
        <a class="more" href="${url(d.links.consult)}" target="_blank" rel="noopener">상담 신청하기 &rarr;</a>
        ${social.length ? `<div class="social">${social
          .map((s) => `<a href="${url(s.href)}" target="_blank" rel="noopener">${esc(s.label)}</a>`)
          .join('')}</div>` : ''}
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="foot">
      <img class="foot-logo" src="${url(d.brandLogo)}" alt="애니톡" width="91" height="24" loading="lazy" decoding="async">
      ${sibs ? `<div class="sites"><span style="color:#5A5A5F;font-weight:700">애니톡 캠퍼스</span>${sibs}</div>` : ''}
      <div>&copy; ${new Date().getFullYear()} ANITALK. All rights reserved.</div>
    </div>
  </div>
</section>`;
}

function quickBar(d) {
  const primary = d.hero.ctas?.[0];
  const booking = naverBooking(d);
  // 모바일 하단 바는 엄지 하나로 닿는 자리다. 전환되는 행동만 셋 남긴다.
  return `<div class="qbar">
  ${booking ? `<a class="pri" href="${url(booking)}" target="_blank" rel="noopener">네이버 예약</a>` : ''}
  <a href="tel:${esc(digits(d.phone))}">전화 문의</a>
  ${primary ? `<a href="${url(primary.href)}"${/^https?:/i.test(primary.href) ? ' target="_blank" rel="noopener"' : ''}>${esc(
    d.quickBar?.primary || '상담 신청'
  )}</a>` : ''}
</div>`;
}

/* ─────────────────────── 구조화 데이터 ─────────────────────── */

function structuredData(d) {
  const org = {
    '@context': 'https://schema.org',
    '@type': 'EducationalOrganization',
    name: d.name,
    alternateName: d.alternateName || undefined,
    description: d.seo.description,
    url: d.site.origin + '/',
    telephone: d.phone,
    image: d.hero.image?.remote || undefined,
    address: {
      '@type': 'PostalAddress',
      addressCountry: 'KR',
      addressRegion: d.geo.region,
      addressLocality: d.geo.locality,
      streetAddress: d.address.street,
    },
    openingHours: d.hours.schemaOrg,
    parentOrganization: { '@type': 'Organization', name: d.company.name, url: 'https://anitok.com/' },
    sameAs: [d.links.naverPlace, d.links.blog, d.links.instagram].filter(Boolean),
  };
  if (d.geo.lat && d.geo.lng) {
    org.geo = { '@type': 'GeoCoordinates', latitude: d.geo.lat, longitude: d.geo.lng };
  }
  const blocks = [org];
  if (d.faq?.items?.length) {
    blocks.push({
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: d.faq.items.map((f) => ({
        '@type': 'Question',
        name: f.q,
        acceptedAnswer: { '@type': 'Answer', text: f.a },
      })),
    });
  }
  return blocks
    .map((b) => `<script type="application/ld+json">${jsonld(b)}</script>`)
    .join('\n');
}

function head(d, present) {
  const canonical = d.site.origin + '/';
  const ogImage = resolveImageForMeta(d, present);
  const geoMeta =
    d.geo.lat && d.geo.lng
      ? `<meta name="geo.position" content="${esc(d.geo.lat)};${esc(d.geo.lng)}">
<meta name="ICBM" content="${esc(d.geo.lat)}, ${esc(d.geo.lng)}">`
      : '';
  return `<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(d.seo.title)}</title>
<meta name="description" content="${esc(d.seo.description)}">
<meta name="keywords" content="${esc((d.seo.keywords || []).join(', '))}">
<meta name="author" content="${esc(d.name)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="${esc(canonical)}">
<link rel="icon" href="${url(d.brandFavicon)}" type="image/png">
<link rel="apple-touch-icon" href="${url(d.brandTouchIcon)}">
<link rel="alternate icon" href="/favicon.svg" type="image/svg+xml">
<meta name="geo.region" content="${esc(d.geo.regionCode)}">
<meta name="geo.placename" content="${esc(d.geo.placename)}">
${geoMeta}
<meta property="og:type" content="website">
<meta property="og:site_name" content="${esc(d.name)}">
<meta property="og:locale" content="ko_KR">
<meta property="og:url" content="${esc(canonical)}">
<meta property="og:title" content="${esc(d.seo.ogTitle || d.seo.title)}">
<meta property="og:description" content="${esc(d.seo.ogDescription || d.seo.description)}">
${ogImage ? `<meta property="og:image" content="${esc(ogImage)}">` : ''}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(d.seo.ogTitle || d.seo.title)}">
<meta name="twitter:description" content="${esc(d.seo.ogDescription || d.seo.description)}">
${ogImage ? `<meta name="twitter:image" content="${esc(ogImage)}">` : ''}
${(d.seo.verification || [])
  .map((v) => `<meta name="${esc(v.name)}" content="${esc(v.content)}">`)
  .join('\n')}
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
${
  d.analytics?.ga4
    ? `<script async src="https://www.googletagmanager.com/gtag/js?id=${esc(d.analytics.ga4)}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${esc(
        d.analytics.ga4
      )}');</script>`
    : ''
}
<meta name="theme-color" content="${esc(d.theme?.accent || '#BD0D16')}">
<link rel="stylesheet" href="/s.css">`;
}

function resolveImageForMeta(d, present) {
  // og:image는 절대 URL이어야 한다. 내려받은 로컬 파일이 실제로 있을 때만
  // 사이트 주소를 붙이고, 없으면 원격 CDN 주소를 그대로 쓴다.
  const img = resolveImage(d.hero?.image, present);
  if (!img) return '';
  return img.kind === 'local' ? d.site.origin + img.src : img.src;
}

/* ───────────────────── 지역 · 과목 랜딩페이지 ─────────────────────
 * data/<slug>.json 의 local 블록과 _shared.json 의 localSubjects 를 곱해
 * "목동만화학원", "화곡만화학원" 같은 검색어 하나에 정확히 답하는 페이지를 만든다.
 *
 * 얇은 문지기(doorway) 페이지가 되지 않도록, 각 페이지는 과목 고유의 설명 +
 * 그 캠퍼스의 실제 반 편성 · 합격 실적 · 주소 · 전화를 함께 싣는다.
 * ───────────────────────────────────────────────────────────────── */

/** local 설정을 실제 페이지 목록으로 펼친다. build 와 렌더러가 같은 목록을 본다. */
export function localPages(d) {
  const loc = d.local;
  if (!loc || !d.localSubjects) return [];
  const q = loc.qualifier ? `${loc.qualifier} ` : '';
  const make = (area, areaSlug, key, note) => {
    const sub = d.localSubjects[key];
    if (!sub) return null;
    return {
      slug: `${areaSlug}-${key}`,
      area,
      subjectKey: key,
      subject: sub,
      // 검색어 그대로가 제목이 된다. 예) 목동만화학원 / 신정 취미 웹툰학원
      keyword: q ? `${area} ${q}${sub.suffix}` : `${area}${sub.suffix}`,
      note: note || '',
    };
  };
  return [
    ...(loc.subjects || []).map((k) => make(loc.area, loc.areaSlug, k, loc.note)),
    ...(loc.nearby || []).map((n) => make(n.area, n.slug, n.subject, n.note)),
  ].filter(Boolean);
}

/** 캠퍼스의 반 편성을 한 줄짜리 목록으로 압축한다(랜딩페이지용). */
function classLines(d) {
  const out = [];
  for (const g of d.classes?.groups || []) {
    for (const it of g.items || []) {
      out.push({ k: g.name, v: it.title, m: it.eyebrow || g.range || '' });
    }
  }
  return out;
}

function resultLines(d) {
  return (d.results?.items || []).map((r) => ({
    k: r.when || '',
    v: `${r.label} — ${r.value}${r.unit ? ' ' + r.unit : ''}`,
    m: (r.detail || []).join(' · '),
  }));
}

function lpJsonLd(d, page, others) {
  const home = d.site.origin + '/';
  const here = `${d.site.origin}/${page.slug}`;
  const crumbs = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: d.name, item: home },
      { '@type': 'ListItem', position: 2, name: page.keyword, item: here },
    ],
  };
  const faq = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: (page.subject.faq || []).map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  };
  void others;
  return `<script type="application/ld+json">${jsonld(crumbs)}</script>
<script type="application/ld+json">${jsonld(faq)}</script>`;
}

function lpFoot(d) {
  return `<section class="sec visit">
  <div class="wrap">
    <div class="foot">
      <img class="foot-logo" src="${url(d.brandLogo)}" alt="애니톡" width="91" height="24" loading="lazy" decoding="async">
      <div class="sites"><a href="/">${esc(d.name)}</a><a href="${url(
    d.links.naverPlace
  )}" target="_blank" rel="noopener">네이버 지도</a></div>
      <div>${esc(d.address.line1)} ${esc(d.address.line2)} | ${esc(d.phone)}</div>
      <div>&copy; ${new Date().getFullYear()} ANITALK. All rights reserved.</div>
    </div>
  </div>
</section>`;
}

export function renderLocal(d, page, { pages = [] } = {}) {
  const booking = naverBooking(d);
  const canonical = `${d.site.origin}/${page.slug}`;
  const s = page.subject;
  const title = `${page.keyword} | ${d.name}`;
  const 을를 = 조사(page.keyword, '을', '를');
  const desc = `${page.keyword}${을를} 찾고 계신가요? ${s.lede} ${d.address.line1} ${
    d.address.line2
  } · ${d.phone}`.slice(0, 155);
  const kw = [
    ...new Set(
      [
        page.keyword,
        ...(s.aliases || []).map((a) => `${page.area}${a}`),
        d.name,
        d.alternateName,
      ].filter(Boolean)
    ),
  ].join(', ');

  const cls = classLines(d);
  const res = resultLines(d);
  const others = pages.filter((p) => p.slug !== page.slug);

  return `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="keywords" content="${esc(kw)}">
<meta name="author" content="${esc(d.name)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="${esc(canonical)}">
<link rel="icon" href="${url(d.brandFavicon)}" type="image/png">
<link rel="apple-touch-icon" href="${url(d.brandTouchIcon)}">
<link rel="alternate icon" href="/favicon.svg" type="image/svg+xml">
<meta name="geo.region" content="${esc(d.geo.regionCode)}">
<meta name="geo.placename" content="${esc(d.geo.placename)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="${esc(d.name)}">
<meta property="og:locale" content="ko_KR">
<meta property="og:url" content="${esc(canonical)}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(desc)}">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<meta name="theme-color" content="${esc(d.theme?.accent || '#BD0D16')}">
<link rel="stylesheet" href="/s.css">
${lpJsonLd(d, page, others)}
</head>
<body>
${header(d, { base: '/' })}
<main>
<section class="lp-head" id="top">
  <div class="wrap">
    <nav class="crumb" aria-label="현재 위치">
      <a href="/">${esc(d.name)}</a><span aria-hidden="true">›</span><span>${esc(page.keyword)}</span>
    </nav>
    <span class="kicker">${esc(s.kicker)}</span>
    <h1 class="lp-h1">${esc(page.area)} <span class="lit">${esc(
    page.keyword.slice(page.area.length).trim()
  )}</span><br>${esc(d.name)}</h1>
    <p class="lp-sub">${esc(s.lede)}</p>
    <div class="cta-row">
      ${booking ? `<a class="btn btn--solid" href="${url(booking)}" target="_blank" rel="noopener">네이버 예약 →</a>` : ''}
      <a class="btn btn--ghost" href="tel:${esc(digits(d.phone))}">${esc(d.phone)}</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <span class="kicker" data-reveal="0">About</span>
    <h2 class="h2" data-reveal="40">${esc(page.area)}에서 ${esc(s.label)}${조사(
      s.label,
      '을',
      '를'
    )} 배운다면</h2>
    <div class="prose" style="margin-top:26px" data-reveal="80">
      ${(s.intro || []).map((t) => `<p>${esc(t)}</p>`).join('')}
      <p>${page.note ? esc(page.note) + ' ' : ''}${esc(d.name)}${조사(
    d.name,
    '은',
    '는'
  )} ${esc(d.address.line1)} ${esc(
    d.address.line2
  )}에 있습니다. 상담은 ${esc(d.hours.line1)}, ${esc(d.hours.line2)}에 받습니다.</p>
    </div>
    <ul class="lp-points" data-reveal="0">
      ${(s.points || [])
        .map((p) => `<li><b>${esc(p.t)}</b><span>${esc(p.d)}</span></li>`)
        .join('')}
    </ul>
  </div>
</section>

${
  cls.length
    ? `<section class="sec sec--tint">
  <div class="wrap">
    <span class="kicker" data-reveal="0">Class</span>
    <h2 class="h2" data-reveal="40">${esc(d.shortName)}에서 운영하는 반</h2>
    <p class="lede" data-reveal="80">${esc(page.keyword)}${을를} 찾아오신 분들이 실제로 등록하는 반입니다.</p>
    <ul class="lp-list" data-reveal="0">
      ${cls
        .slice(0, 6)
        .map(
          (c) =>
            `<li><span class="k">${esc(c.k)}</span><span class="v">${esc(
              c.v
            )}</span><span class="m">${esc(c.m)}</span></li>`
        )
        .join('')}
    </ul>
    <p class="note">반 편성과 진도는 첫 상담에서 지금 실력을 보고 정합니다.</p>
  </div>
</section>`
    : ''
}

<section class="sec sec--tint">
  <div class="wrap">
    <span class="kicker" data-reveal="0">FAQ</span>
    <h2 class="h2" data-reveal="40">${esc(page.keyword)} 자주 묻는 질문</h2>
    <div class="faq" data-reveal="0">
      ${(s.faq || [])
        .map(
          (f) =>
            `<details><summary>${esc(f.q)}</summary><div class="ans">${esc(f.a)}</div></details>`
        )
        .join('')}
    </div>
  </div>
</section>

<section class="sec lp-cta">
  <div class="wrap">
    <span class="kicker" data-reveal="0">Visit</span>
    <h2 class="h2" data-reveal="40">상담 · 예약 안내</h2>
    <p class="lede" data-reveal="80">${esc(d.address.line1)} ${esc(d.address.line2)}<br>${esc(
    d.hours.line1
  )} · ${esc(d.hours.line2)}</p>
    <div class="cta-row" data-reveal="120">
      ${booking ? `<a class="btn btn--solid" href="${url(booking)}" target="_blank" rel="noopener">네이버 예약 →</a>` : ''}
      <a class="btn btn--ghost" href="tel:${esc(digits(d.phone))}">전화 ${esc(d.phone)}</a>
      ${
        d.links?.consult
          ? `<a class="btn btn--ghost" href="${url(
              d.links.consult
            )}" target="_blank" rel="noopener">온라인 상담</a>`
          : ''
      }
    </div>
  </div>
</section>

${
  others.length
    ? `<section class="sec">
  <div class="wrap">
    <span class="kicker" data-reveal="0">More</span>
    <h2 class="h2" data-reveal="40">다른 지역 · 과목 안내</h2>
    <div class="lp-links" data-reveal="0">
      <a href="/">${esc(d.shortName)} 홈</a>
      ${others.map((p) => `<a href="/${esc(p.slug)}">${esc(p.keyword)}</a>`).join('')}
    </div>
  </div>
</section>`
    : ''
}
</main>
${lpFoot(d)}
${quickBar(d)}
<script src="/s.js" defer></script>
</body>
</html>
`;
}

/* ─────────────────── 공유 에셋 (s.css · s.js) ───────────────────
 * 예전에는 페이지마다 CSS/JS를 통째로 인라인했다. 지역 랜딩페이지가 생기면서
 * 같은 20KB를 페이지 수만큼 복사하게 되어, 파일 둘로 빼고 전부 공유한다.
 * 두 번째 페이지부터는 브라우저 캐시에서 바로 나온다.
 * ───────────────────────────────────────────────────────────── */

export function siteCss(d) {
  return `${CSS}${CSS_MOBILE}${themeCss(d.theme)}\n`;
}

export function siteJs() {
  return `${JS}\n`;
}

/* ─────────────────────────── 404 ─────────────────────────── */

/** 기본 Vercel 404 대신 같은 톤의 페이지. 검색엔진에는 색인하지 않도록 막는다. */
export function render404(d) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>페이지를 찾을 수 없습니다 | ${esc(d.name)}</title>
<meta name="robots" content="noindex, follow">
<link rel="icon" href="${url(d.brandFavicon)}" type="image/png">
<link rel="apple-touch-icon" href="${url(d.brandTouchIcon)}">
<link rel="alternate icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="/s.css">
<style>
.nf{min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 24px;gap:20px}
.nf .code{font-size:clamp(56px,10vw,120px);font-weight:800;letter-spacing:-.06em;color:var(--accent)}
.nf p{margin:0;font-size:15px;line-height:1.8;color:var(--muted)}
</style>
</head>
<body>
<div class="nf">
  <span class="code">404</span>
  <h1 class="h2">페이지를 찾을 수 없습니다</h1>
  <p>주소가 바뀌었거나 삭제된 페이지입니다.<br>${esc(d.name)} 홈으로 돌아가 주세요.</p>
  <div class="cta-row" style="justify-content:center">
    <a class="btn btn--solid" href="/">홈으로 →</a>
    <a class="btn btn--ghost" href="tel:${esc(digits(d.phone))}">${esc(d.phone)}</a>
  </div>
</div>
</body>
</html>
`;
}

/* ─────────────────────────── 진입점 ─────────────────────────── */

function localIndex(d) {
  const pages = localPages(d);
  if (!pages.length) return '';
  const cfg = d.local || {};
  return `<section class="sec sec--tint" id="local">
  <div class="wrap">
    <span class="kicker" data-reveal="0">${esc(cfg.kicker || 'Local')}</span>
    <h2 class="h2" data-reveal="40">${esc(cfg.title || '지역별 · 과목별 안내')}</h2>
    <p class="lede" data-reveal="80">${esc(cfg.lede || '')}</p>
    <div class="lp-links" data-reveal="0">${pages
      .map((p) => `<a href="/${esc(p.slug)}">${esc(p.keyword)}</a>`)
      .join('')}</div>
  </div>
</section>`;
}

export function renderPage(d, { present = new Set(), siblings = [] } = {}) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
${head(d, present)}
${structuredData(d)}
</head>
<body>
${header(d)}
<main>
${hero(d, present)}
${about(d, present)}
${results(d)}
${passList(d)}
${classes(d, present)}
${galleries(d, present)}
${process(d)}
${faq(d)}
${localIndex(d)}
</main>
${visit(d, siblings)}
${quickBar(d)}
<div class="lb" data-lb aria-hidden="true"><button class="lb-close" type="button" aria-label="닫기">&times;</button><img alt=""></div>
<script src="/s.js" defer></script>
</body>
</html>
`;
}
