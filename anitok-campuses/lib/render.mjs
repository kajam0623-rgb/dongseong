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
  --bg:#000000; --ink:#FFFFFF; --accent:#BD0D16; --accent-lit:#FF3B45;
  --panel:#0F0F11; --panel-2:#141416; --line:#232326; --line-2:#33333A;
  --muted:#A8A8AC; --muted-2:#8A8A8A;
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
.hdr{position:sticky;top:0;z-index:60;background:var(--accent);box-shadow:0 2px 20px rgba(0,0,0,.4)}
.hdr-in{max-width:var(--wrap);margin:0 auto;padding:0 clamp(16px,3vw,36px);height:64px;display:flex;align-items:center;justify-content:space-between;gap:20px}
.brand{display:flex;align-items:center;gap:11px;min-width:0}
.brand-mark{width:38px;height:38px;border-radius:50%;background:#fff;color:var(--accent);display:grid;place-items:center;font-size:15px;font-weight:800;letter-spacing:-.05em;flex:0 0 auto}
.brand-name{font-size:clamp(15px,1.4vw,18px);font-weight:800;letter-spacing:-.02em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.nav{display:flex;align-items:center;gap:clamp(12px,1.6vw,26px)}
.nav a{font-size:14px;font-weight:600;padding:4px 0;border-bottom:2px solid transparent;white-space:nowrap;transition:border-color .3s ease,opacity .3s ease}
.nav a:hover{border-bottom-color:#fff}
.hdr-tel{display:inline-flex;align-items:center;gap:8px;background:#fff;color:var(--accent);font-size:14px;font-weight:800;padding:9px 18px;border-radius:999px;white-space:nowrap;transition:transform .3s cubic-bezier(.22,1.4,.36,1)}
.hdr-tel:hover{transform:translateY(-2px)}
.burger{display:none;width:42px;height:42px;border:1px solid rgba(255,255,255,.5);border-radius:8px;background:none;color:#fff;cursor:pointer;padding:0;align-items:center;justify-content:center}
.burger span{display:block;width:18px;height:2px;background:#fff;position:relative}
.burger span::before,.burger span::after{content:"";position:absolute;left:0;width:18px;height:2px;background:#fff}
.burger span::before{top:-6px}.burger span::after{top:6px}
.mnav{display:none;background:#8E0A10;border-top:1px solid rgba(255,255,255,.25)}
.mnav.is-open{display:block}
.mnav a{display:block;padding:15px clamp(16px,4vw,28px);font-size:15px;font-weight:600;border-bottom:1px solid rgba(255,255,255,.14)}
@media (max-width:900px){
  .nav,.hdr-tel{display:none}
  .burger{display:inline-flex}
}

/* 히어로 */
.hero{position:relative;overflow:hidden;height:min(94vh,1000px);min-height:640px;display:flex;align-items:center}
.hero-bg{position:absolute;inset:0;width:100%;height:112%;object-fit:cover;object-position:center 30%;background:radial-gradient(120% 90% at 15% 10%,#2A0407 0%,#000 70%);font-size:0;animation:kenburns 26s cubic-bezier(.4,0,.6,1) infinite;will-change:transform}
.hero-bg--none{background:radial-gradient(120% 90% at 15% 10%,#2A0407 0%,#000 70%)}
.hero-glow{position:absolute;top:0;left:0;width:70vw;height:70vw;max-width:900px;max-height:900px;background:radial-gradient(circle,rgba(189,13,22,.55) 0%,rgba(0,0,0,0) 66%);mix-blend-mode:screen;pointer-events:none}
.hero-scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.78) 0%,rgba(0,0,0,.42) 46%,rgba(0,0,0,.12) 100%)}
.hero-scrim-b{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.2) 0%,rgba(0,0,0,0) 34%,rgba(0,0,0,.72) 100%)}
.hero-in{position:relative;width:100%;max-width:var(--wrap);margin:0 auto;padding:0 clamp(20px,4vw,56px)}
.tag{display:inline-flex;align-items:center;gap:8px;background:rgba(189,13,22,.92);border-radius:999px;padding:8px 18px;font-size:13px;font-weight:700;margin-bottom:24px}
.hero h1{font-size:clamp(34px,5.4vw,72px);line-height:1.14;letter-spacing:-.05em;text-shadow:0 6px 34px rgba(0,0,0,.8)}
.hero h1 .over{display:block;font-size:.56em;font-weight:700;letter-spacing:-.03em;margin-bottom:10px}
.hero h1 .lit{color:var(--accent-lit)}
.hero-sub{margin:24px 0 0;font-size:clamp(15px,1.6vw,21px);font-weight:700;text-shadow:0 2px 16px rgba(0,0,0,.85)}
.cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}
.btn{display:inline-flex;align-items:center;gap:10px;font-size:16px;font-weight:800;padding:16px 32px;border-radius:999px;transition:transform .5s cubic-bezier(.22,1.4,.36,1),background .3s ease,color .3s ease}
.btn:hover{transform:translateY(-3px)}
.btn--solid{background:var(--accent);color:#fff}
.btn--solid:hover{background:#fff;color:var(--accent)}
.btn--ghost{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.4);color:#fff;font-weight:700;backdrop-filter:blur(8px)}
.btn--ghost:hover{background:#fff;color:#111}
.scroll-dot{position:absolute;bottom:26px;left:50%;transform:translateX(-50%);width:22px;height:34px;border:1px solid rgba(255,255,255,.5);border-radius:999px;display:flex;justify-content:center;padding-top:7px}
.scroll-dot i{width:3px;height:6px;border-radius:2px;background:#fff;animation:dot 1.9s cubic-bezier(.2,.8,.2,1) infinite}
@keyframes kenburns{0%,100%{transform:scale(1) translateY(0)}50%{transform:scale(1.08) translateY(-1.5%)}}
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
.card{background:var(--panel-2);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
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
.foot .sites{display:flex;flex-wrap:wrap;gap:8px 18px;margin-bottom:22px}
.foot .sites a{font-size:13px;font-weight:600;color:var(--muted)}
.foot .sites a:hover{color:#fff}

/* 모바일 하단 고정 바 */
.qbar{position:fixed;left:0;right:0;bottom:0;z-index:70;display:none;grid-template-columns:1fr 1fr;gap:1px;background:var(--line)}
.qbar a{padding:15px 8px;text-align:center;font-size:14px;font-weight:800;background:#141416}
.qbar a.pri{background:var(--accent)}
@media (max-width:760px){.qbar{display:grid}body{padding-bottom:54px}}

/* 라이트박스 */
.lb{position:fixed;inset:0;z-index:100;background:rgba(0,0,0,.94);display:none;align-items:center;justify-content:center;padding:24px}
.lb.is-open{display:flex}
.lb img{max-width:min(1200px,92vw);max-height:88vh;width:auto;object-fit:contain;border-radius:6px}
.lb-close{position:absolute;top:18px;right:20px;width:44px;height:44px;border:1px solid var(--line-2);border-radius:50%;background:none;color:#fff;font-size:22px;cursor:pointer;line-height:1}

/* 스크롤 리빌 */
[data-reveal]{opacity:0;transform:translateY(26px);transition:opacity .8s cubic-bezier(.16,1,.3,1),transform .8s cubic-bezier(.16,1,.3,1)}
[data-reveal].is-in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){
  [data-reveal]{opacity:1;transform:none;transition:none}
  .hero-bg{animation:none}
  .scroll-dot i{animation:none}
}
`;

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

  // 스크롤 리빌
  var targets = document.querySelectorAll('[data-reveal]');
  if (rm || !('IntersectionObserver' in window)) {
    targets.forEach(function(el){ el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (!e.isIntersecting) return;
        var d = parseInt(e.target.getAttribute('data-reveal'), 10) || 0;
        setTimeout(function(){ e.target.classList.add('is-in'); }, d);
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.06 });
    targets.forEach(function(el){ io.observe(el); });
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

function header(d) {
  const nav = (d.nav || []).map((n) => `<a href="${url(n.href)}">${esc(n.label)}</a>`).join('');
  const mnav = (d.nav || []).map((n) => `<a href="${url(n.href)}">${esc(n.label)}</a>`).join('');
  return `<div class="progress" data-progress></div>
<header class="hdr">
  <div class="hdr-in">
    <a class="brand" href="#top">
      <span class="brand-mark" aria-hidden="true">${esc(d.markText || 'AT')}</span>
      <span class="brand-name">${esc(d.name)}</span>
    </a>
    <nav class="nav" aria-label="주요 메뉴">${nav}</nav>
    <a class="hdr-tel" href="tel:${esc(digits(d.phone))}">${esc(d.phone)}</a>
    <button class="burger" type="button" data-burger aria-expanded="false" aria-controls="mnav" aria-label="메뉴 열기"><span></span></button>
  </div>
  <nav class="mnav" id="mnav" data-mnav aria-label="모바일 메뉴">${mnav}<a href="tel:${esc(
    digits(d.phone)
  )}">전화 ${esc(d.phone)}</a></nav>
</header>`;
}

function hero(d, present) {
  const bg = resolveImage(d.hero.image, present);
  // 히어로 배경은 장식 요소다. 캠퍼스 이름은 h1이 이미 말하고 있으므로 alt는 비우고,
  // 이미지가 못 뜰 때 alt 텍스트가 화면 구석에 남지 않게 한다.
  const bgEl = bg
    ? `<img class="hero-bg" src="${url(bg.src)}" alt="" role="presentation" fetchpriority="high">`
    : `<div class="hero-bg hero-bg--none" role="presentation"></div>`;
  const ctas = (d.hero.ctas || [])
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
      <div class="vcard" data-reveal="120">
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
      ${sibs ? `<div class="sites"><span style="color:#5A5A5F;font-weight:700">애니톡 캠퍼스</span>${sibs}</div>` : ''}
      <div>${esc(d.company.name)} | 대표 ${esc(d.company.ceo)} | 사업자등록번호 ${esc(
    d.company.bizNo
  )}</div>
      <div>${esc(d.company.address)} | 대표전화 ${esc(d.company.tel)}</div>
      <div>&copy; ${new Date().getFullYear()} ANITALK. All rights reserved.</div>
    </div>
  </div>
</section>`;
}

function quickBar(d) {
  const primary = d.hero.ctas?.[0];
  return `<div class="qbar">
  ${primary ? `<a class="pri" href="${url(primary.href)}"${/^https?:/i.test(primary.href) ? ' target="_blank" rel="noopener"' : ''}>${esc(
    d.quickBar?.primary || '상담 신청'
  )}</a>` : ''}
  <a href="tel:${esc(digits(d.phone))}">전화 ${esc(d.phone)}</a>
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

function head(d) {
  const canonical = d.site.origin + '/';
  const ogImage = resolveImageForMeta(d);
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
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
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
<style>${CSS}</style>`;
}

function resolveImageForMeta(d) {
  const h = d.hero?.image;
  if (!h) return '';
  if (h.local) return d.site.origin + '/gal/' + h.local;
  return h.remote || '';
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
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>${CSS}
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

export function renderPage(d, { present = new Set(), siblings = [] } = {}) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
${head(d)}
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
</main>
${visit(d, siblings)}
${quickBar(d)}
<div class="lb" data-lb aria-hidden="true"><button class="lb-close" type="button" aria-label="닫기">&times;</button><img alt=""></div>
<script>${JS}</script>
</body>
</html>
`;
}
