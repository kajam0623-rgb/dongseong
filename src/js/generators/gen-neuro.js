/* ═══════ 스타일 13: 뉴로 AI 클론 (AI·데이터 의료 솔루션형) ═══════ */
function genNeuro(cfg){
  const T=cfg.theme, C=siteCommon(cfg);
  const services=(cfg.services||[]);
  const doctors=(cfg.doctors||[]);
  const gallery=(cfg.gallery||[]);
  const solutionTabs=services.slice(0,4);
  const familyItems=[
    {k:'Official',t:'예약·상담',d:'상담부터 예약까지 한 번에 연결합니다',h:cfg.naverUrl||('tel:'+cfg.phone)},
    {k:'Care',t:'환자 안내',d:'진료 전후 필요한 정보를 빠르게 안내합니다',h:'#about'},
    {k:'Media',t:'시설·장비',d:'진료 환경과 장비 이미지를 확인합니다',h:'#gallery'},
    {k:'Support',t:'오시는 길',d:'위치와 진료시간을 바로 확인합니다',h:'#location'}
  ];
  const servicesHTML = services.map((s,i)=>`
    <article class="ne-service v5-sv" data-reveal data-ne-motion="service-card" style="--d:${(i*0.07).toFixed(2)}s">
      <a href="#services" aria-label="${s.title}">
        <div class="ne-service-img">${s.img?`<img src="${s.img}" alt="${s.title}" loading="lazy" decoding="async" data-lb>`:`<span>0${i+1}</span>`}</div>
        <div class="ne-service-tx"><small>${String(i+1).padStart(2,'0')} SOLUTION</small><h3>${s.title}</h3><p>${s.desc}</p></div>
      </a>
    </article>`).join('');
  const tabButtons = solutionTabs.map((s,i)=>`<button type="button" class="${i===0?'active':''}" data-ne-tab="${i}">${s.title}</button>`).join('');
  const tabPanels = solutionTabs.map((s,i)=>`
    <article class="ne-tab-panel ${i===0?'active':''}" data-ne-panel="${i}" data-ne-motion="solution-panel">
      <div>
        <span>0${i+1} / ONE STOP</span>
        <h3>${s.title}</h3>
        <p>${s.desc}</p>
        <ul>
          <li>정밀 상담</li>
          <li>데이터 기반 안내</li>
          <li>개인별 계획</li>
        </ul>
      </div>
      <figure>${s.img?`<img src="${s.img}" alt="${s.title}" loading="lazy" decoding="async" data-lb>`:`<span>AI ${String(i+1).padStart(2,'0')}</span>`}</figure>
    </article>`).join('');
  return `<!DOCTYPE html>
<html lang="ko" data-motion="${cfg.motion}">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${cfg.name} — ${cfg.slogan}</title><meta name="description" content="${cfg.desc}">
${headMeta(cfg)}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<style>
:root{--primary:${T.primary};--deep:${T.deep};--ink:${T.ink};--soft:${T.soft};--grad:${T.grad};--spd:${cfg.speed};--nav-fg:#fff;--mnav-bg:rgba(4,10,28,.98);--mnav-accent:${T.primary};--ne-navy:#050a24;--ne-blue:#102eff;--ne-cyan:#36d8ff;--ne-mint:#18cbb8;--ne-line:rgba(255,255,255,.16)}
${X_BASE_CSS}
html,body{background:#fff}
body{font-family:'Pretendard Variable',Pretendard,-apple-system,sans-serif;color:#111827;letter-spacing:0}
h1,h2,h3,p,span,a,b,small,button,label{letter-spacing:0}
.wrap{max-width:1240px}
section{padding:clamp(92px,10vw,150px) 24px}
nav{height:70px;padding:0 clamp(18px,3vw,54px);color:#fff;background:transparent}
nav .brand{display:flex;align-items:center;gap:8px;color:#fff;font-size:16px;font-weight:900}
nav .brand::before{content:"";width:18px;height:18px;border:2px solid currentColor;border-radius:5px;transform:rotate(45deg);display:inline-block}
nav .links{gap:30px}
nav .links a{color:rgba(255,255,255,.78);font-size:13px}
nav .links a:hover{color:#fff}
nav .btn-call{background:#fff;color:#06102f;border-radius:4px;padding:11px 20px}
nav.scrolled{background:rgba(4,10,28,.82);backdrop-filter:blur(16px);box-shadow:0 1px 0 rgba(255,255,255,.1)}
.burger i{background:#fff}
.ne-hero{position:relative;min-height:100svh;display:grid;place-items:center;overflow:hidden;isolation:isolate;background:linear-gradient(180deg,#aeb3c5 0%,#eef2f8 30%,#05103c 31%,#050a24 100%);padding:100px 24px 70px;color:#fff}
.ne-hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,255,255,.38),rgba(255,255,255,0) 28%,rgba(5,10,36,.12) 29%,rgba(5,10,36,.9) 100%);pointer-events:none;z-index:-2}
.ne-hero::after{content:"";position:absolute;inset:28% -10% -24%;background:radial-gradient(circle at 70% 18%,rgba(54,216,255,.28),transparent 28%),radial-gradient(circle at 42% 38%,rgba(16,46,255,.28),transparent 36%);filter:blur(22px);opacity:.78;z-index:-1}
.ne-hero-inner{position:relative;z-index:1;width:min(1240px,100%);display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(42px,6vw,100px);align-items:center}
.ne-hero-copy{position:relative;z-index:2}
.ne-kicker{display:block;margin-bottom:16px;color:#e7ecff;font-size:13px;font-weight:850}
.ne-hero h1{color:#fff;font-size:clamp(58px,12vw,154px);line-height:.88;font-weight:900;max-width:760px;text-transform:none;letter-spacing:-.02em}
.ne-hero h1 .ne-word{display:block;overflow:hidden}
.ne-hero h1 .ne-word:last-child{text-align:right}
.ne-hero p{max-width:560px;margin-top:24px;color:rgba(255,255,255,.82);font-size:clamp(16px,1.7vw,21px);line-height:1.65}
.ne-hero .btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:36px}
.ne-hero .btns a{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 28px;border-radius:4px;text-decoration:none;font-weight:850;font-size:14px}
.ne-hero .b1{background:#fff;color:#06102f}
.ne-hero .b2{border:1px solid rgba(255,255,255,.44);color:#fff}
.ne-visual{position:relative;min-height:470px;display:grid;place-items:center;perspective:1100px}
.ne-visual::before{content:"";position:absolute;width:min(560px,92vw);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(54,216,255,.26),transparent 58%);filter:blur(8px);opacity:.84}
.ne-visual-img{position:absolute;inset:4% 0 9%;overflow:hidden;border-radius:8px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);opacity:.45}
.ne-visual-img img{width:100%;height:100%;object-fit:cover;filter:saturate(.86) contrast(1.05)}
.ne-brain-orbit{position:absolute;width:min(500px,80vw);aspect-ratio:1;border:1px solid rgba(255,255,255,.22);border-radius:50%;transform:rotateX(58deg) rotateZ(-18deg);box-shadow:0 0 80px rgba(54,216,255,.12)}
.ne-brain-orbit::before,.ne-brain-orbit::after{content:"";position:absolute;inset:12%;border:1px solid rgba(54,216,255,.24);border-radius:50%}
.ne-brain-orbit::after{inset:24%;border-color:rgba(255,255,255,.18)}
.ne-brain-core{position:relative;width:min(260px,48vw);aspect-ratio:1;border-radius:45% 55% 48% 52%;background:radial-gradient(circle at 34% 26%,rgba(255,255,255,.82),rgba(255,255,255,.18) 30%,rgba(54,216,255,.2) 55%,rgba(16,46,255,.24));border:1px solid rgba(255,255,255,.44);box-shadow:0 24px 90px rgba(0,0,0,.24),inset 0 0 48px rgba(54,216,255,.3);overflow:hidden}
.ne-brain-core::before{content:"";position:absolute;inset:18%;border:1px solid rgba(255,255,255,.38);border-radius:48% 52% 46% 54%;box-shadow:28px 0 0 -22px rgba(255,255,255,.28),-26px 20px 0 -21px rgba(255,255,255,.24),14px -24px 0 -18px rgba(54,216,255,.28)}
.ne-brain-core::after{content:"";position:absolute;inset:-20%;background:linear-gradient(115deg,transparent 34%,rgba(255,255,255,.34) 45%,transparent 56%);transform:translateX(-46%)}
.ne-node{position:absolute;width:10px;height:10px;border-radius:50%;background:#7df3ff;box-shadow:0 0 22px #36d8ff}
.ne-node.n1{left:12%;top:28%}.ne-node.n2{right:10%;top:42%}.ne-node.n3{left:42%;bottom:9%}
.ne-wave{position:absolute;left:4%;right:4%;bottom:8%;display:grid;gap:9px;opacity:.78}
.ne-wave i{display:block;height:1px;background:linear-gradient(90deg,transparent,rgba(125,243,255,.95),transparent);transform-origin:left center}
.ne-scan{position:absolute;right:0;bottom:0;width:min(330px,60vw);aspect-ratio:1.12;border:1px solid rgba(255,255,255,.28);border-radius:8px;background:linear-gradient(135deg,rgba(255,255,255,.12),rgba(255,255,255,.03));box-shadow:0 28px 90px rgba(0,0,0,.24);overflow:hidden}
.ne-scan::before{content:"";position:absolute;inset:34px;border:1px solid rgba(54,216,255,.45);border-radius:8px;background:repeating-linear-gradient(90deg,rgba(54,216,255,.12) 0 1px,transparent 1px 34px),repeating-linear-gradient(0deg,rgba(54,216,255,.1) 0 1px,transparent 1px 34px)}
.ne-scan::after{content:"";position:absolute;left:0;right:0;top:18%;height:2px;background:#7df3ff;box-shadow:0 0 28px #36d8ff}
.ne-scan b{position:absolute;left:34px;right:28px;bottom:34px;font-size:clamp(28px,4.2vw,54px);line-height:.98;font-weight:900;color:#fff;word-break:keep-all}
.ne-scan small{position:absolute;right:34px;top:32px;color:#36d8ff;font-size:12px;font-weight:900}
.ne-scroll{position:absolute;left:50%;bottom:24px;transform:translateX(-50%);z-index:1;color:rgba(255,255,255,.82);font-size:12px;font-weight:900}
.ne-scroll::after{content:"";display:block;width:1px;height:52px;background:rgba(255,255,255,.55);margin:10px auto 0}
.ne-statement{min-height:88svh;display:grid;place-items:center;text-align:center;background:linear-gradient(180deg,#050a24,#07145a);color:#cbd4ff}
.ne-statement h2{max-width:1120px;margin:0 auto;color:#cbd4ff;font-size:clamp(34px,5.4vw,78px);line-height:1.55;font-weight:900}
.ne-about{background:#f4f6fb}
.ne-about-grid{display:grid;grid-template-columns:.78fr 1.22fr;gap:clamp(36px,6vw,96px);align-items:end}
.ne-label{display:block;margin-bottom:18px;color:var(--ne-blue);font-size:12px;font-weight:900;text-transform:uppercase}
.ne-title{font-size:clamp(34px,5vw,70px);line-height:1.05;font-weight:900;color:#071024}
.ne-copy{margin-top:18px;color:#4b5565;font-size:17px;line-height:1.85;max-width:640px}
.ne-about-panel{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.ne-about-panel a{min-height:230px;display:flex;flex-direction:column;justify-content:flex-end;padding:28px;border-radius:8px;background:#fff;text-decoration:none;color:#071024;border:1px solid #e4e9f2;transition:.28s}
.ne-about-panel a:hover{transform:translateY(-4px);border-color:#b9c8ff;box-shadow:0 22px 58px rgba(8,20,62,.12)}
.ne-about-panel b{font-size:22px}
.ne-about-panel span{margin-top:8px;color:#667084;font-size:14px;line-height:1.6}
.ne-marquee{overflow:hidden;background:#06102f;color:#fff;border-block:1px solid rgba(255,255,255,.14)}
.ne-marquee-track{display:flex;width:max-content;animation:ne-mar 26s linear infinite}
.ne-marquee span{display:inline-flex;align-items:center;gap:14px;padding:16px 28px;font-size:14px;font-weight:900;white-space:nowrap}
.ne-marquee i{width:18px;height:18px;border:2px solid currentColor;border-radius:5px;transform:rotate(45deg)}
@keyframes ne-mar{to{transform:translateX(-50%)}}
.ne-solution{background:#fff}
.ne-center{text-align:center;margin-bottom:48px}
.ne-center .ne-copy{margin-left:auto;margin-right:auto}
.ne-tabs{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:30px}
.ne-tabs button{border:0;border-bottom:2px solid transparent;background:transparent;color:#8b94a6;padding:12px 18px;font:850 14px/1 inherit;cursor:pointer}
.ne-tabs button.active{color:var(--ne-blue);border-color:var(--ne-blue)}
.ne-tab-panel{display:none;grid-template-columns:.92fr 1.08fr;gap:30px;align-items:stretch;max-width:1040px;margin:0 auto;border:1px solid #e8edf5;border-radius:8px;overflow:hidden;background:#fff}
.ne-tab-panel.active{display:grid}
.ne-tab-panel>div{padding:clamp(32px,4vw,54px)}
.ne-tab-panel span{display:block;margin-bottom:16px;color:var(--ne-blue);font-size:12px;font-weight:900}
.ne-tab-panel h3{font-size:clamp(28px,3.4vw,44px);font-weight:900;color:#071024}
.ne-tab-panel p{margin-top:16px;color:#5f6879;line-height:1.82}
.ne-tab-panel ul{display:flex;gap:8px;flex-wrap:wrap;list-style:none;margin:26px 0 0;padding:0}
.ne-tab-panel li{border:1px solid #dce4f0;border-radius:4px;padding:8px 12px;font-size:12px;font-weight:850;color:#24324a}
.ne-tab-panel figure{min-height:360px;background:#f0f4fb;display:grid;place-items:center;overflow:hidden}
.ne-tab-panel figure img{width:100%;height:100%;object-fit:cover}
.ne-tab-panel figure span{font-size:clamp(54px,8vw,112px);font-weight:900;color:#cbd6ea}
.ne-lineup{background:#f7f9fd}
.ne-service-grid{display:grid;grid-template-columns:repeat(4,minmax(230px,1fr));gap:16px;overflow-x:auto;padding-bottom:8px}
.ne-service{min-width:230px;border-radius:8px;background:#101827;overflow:hidden;border:1px solid rgba(15,23,42,.1)}
.ne-service a{display:grid;text-decoration:none;color:#fff;height:100%}
.ne-service-img{aspect-ratio:1/1;background:#071024;display:grid;place-items:center;overflow:hidden}
.ne-service-img img{width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.16,1,.3,1)}
.ne-service-img span{font-size:52px;font-weight:900;color:rgba(255,255,255,.22)}
.ne-service:hover img{transform:scale(1.06)}
.ne-service-tx{padding:22px}
.ne-service-tx small{display:block;margin-bottom:10px;color:#88dfff;font-size:11px;font-weight:900}
.ne-service-tx h3{color:#fff;font-size:20px;font-weight:900}
.ne-service-tx p{margin-top:9px;color:rgba(255,255,255,.68);font-size:13.5px;line-height:1.65}
.ne-stats{background:#fff}
.ne-stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}
.ne-stat{min-height:190px;padding:28px;border:1px solid #e4eaf3;background:#f8fafc;border-radius:8px;display:flex;flex-direction:column;justify-content:space-between}
.ne-stat:nth-child(even){background:#eef5ff}
.ne-stat .stat-value{display:flex;align-items:flex-end;gap:3px;color:#102eff;font-size:clamp(42px,5.4vw,74px);line-height:.9;font-weight:900}
.ne-stat .stat-number{font:inherit}
.ne-stat .stat-unit{font-size:.42em;color:#18cbb8;font-weight:900}
.ne-stat .stat-label{display:block;color:#263246;font-size:16px;font-weight:850;line-height:1.45}
.ne-year{background:#fff;padding-top:0}
.ne-year-grid{display:grid;grid-template-columns:1fr auto;gap:28px;align-items:end;border-top:1px solid #e7edf6;padding-top:64px}
.ne-year b{font-size:clamp(72px,14vw,190px);line-height:.78;color:#102eff;font-weight:900}
.ne-partners{margin-top:34px;display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.ne-partners span{height:38px;border:1px solid #e5ebf3;border-radius:4px;display:grid;place-items:center;color:#7b8495;font-size:11px;font-weight:800;background:#fff}
.ne-doctors{background:#f6f8fc}
.ne-doctor-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.ne-doctor{background:#fff;border:1px solid #e5ebf3;border-radius:8px;overflow:hidden}
.ne-doctor .im{aspect-ratio:4/4.6;background:#eaf0f8;display:grid;place-items:center;overflow:hidden}
.ne-doctor img{width:100%;height:100%;object-fit:cover}
.ne-doctor .ph{font-size:68px;font-weight:900;color:#b8c5d8}
.ne-doctor .tx{padding:24px}
.ne-doctor h3{font-size:22px;color:#071024}
.ne-doctor h3 small{font-size:.64em;color:#748097}
.ne-doctor .r{margin-top:6px;color:#102eff;font-weight:850}
.ne-doctor .t{margin-top:8px;color:#626d7f;font-size:14px;line-height:1.65}
.ne-gallery{background:#fff}
.ne-gallery-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.ne-gallery figure{border-radius:8px;overflow:hidden;background:#eef3fb}
.ne-gallery .im{aspect-ratio:4/3;display:grid;place-items:center;overflow:hidden}
.ne-gallery img{width:100%;height:100%;object-fit:cover;transition:transform .55s cubic-bezier(.16,1,.3,1)}
.ne-gallery figure:hover img{transform:scale(1.05)}
.ne-gallery .ph{font-size:38px;font-weight:900;color:#b6c2d5}
.ne-gallery figcaption{padding:14px 16px;color:#38445a;font-size:14px;font-weight:800;background:#fff}
.ne-media{background:#f7f9fd}
.ne-news{max-width:960px;margin:0 auto;border-top:2px solid #071024}
.ne-news a{display:grid;grid-template-columns:120px 1fr 110px;gap:22px;align-items:center;padding:20px 0;border-bottom:1px solid #e2e8f1;color:#111827;text-decoration:none}
.ne-news small{color:#102eff;font-weight:900}
.ne-news b{font-size:16px}
.ne-news span{color:#7b8495;font-size:13px;text-align:right}
.ne-booking{background:#060606;color:#fff}
.ne-booking .ne-title{color:#fff}
.ne-booking .ne-copy{color:rgba(255,255,255,.7)}
.ne-booking .x-bk-wrap{margin-top:40px}
.ne-booking .x-bk{background:#0f1116;border-color:#2b303a;border-radius:8px}
.ne-booking .x-bk label{color:#e6ebf5}
.ne-booking .x-bk input,.ne-booking .x-bk select,.ne-booking .x-bk textarea{background:#fff;border-radius:4px}
.ne-booking .x-bk button{background:#102eff;border-radius:4px}
.ne-booking .x-bkside .tel{color:#fff}
.ne-location{background:#fff}
.ne-location .x-loc>div{border-radius:8px}
.qbar{border-radius:6px}
${PROD_CSS}
${userCss(cfg)}
.ne-hero h1 .ne-word{transition:transform .9s cubic-bezier(.16,1,.3,1),opacity .9s ease}
.ne-hero h1:not(.in) .ne-word{transform:translateY(112%);opacity:0}
.ne-hero h1.in .ne-word:nth-child(2){transition-delay:.13s}
.ne-wave i{animation:ne-wave calc(2.8s*var(--spd)) ease-in-out infinite alternate}
.ne-wave i:nth-child(2){animation-delay:.28s}.ne-wave i:nth-child(3){animation-delay:.56s}
.ne-node{animation:ne-pulse calc(2.2s*var(--spd)) ease-in-out infinite}
.ne-node.n2{animation-delay:.3s}.ne-node.n3{animation-delay:.62s}
.ne-brain-core{animation:ne-brain calc(6.8s*var(--spd)) ease-in-out infinite alternate}
.ne-brain-core::after{animation:ne-shine calc(4.4s*var(--spd)) ease-in-out infinite}
.ne-scroll::after{animation:ne-scroll calc(1.9s*var(--spd)) ease-in-out infinite}
.ne-tab-panel.motion-replay{animation:ne-panel-in .48s cubic-bezier(.16,1,.3,1)}
.ne-partners span{transition:transform .34s ease,border-color .34s ease,color .34s ease}
.ne-partners span:hover{transform:translateY(-4px);border-color:#b9c8ff;color:#102eff}
html[data-motion="soft"] .ne-scan::after,html[data-motion="dynamic"] .ne-scan::after{animation:ne-scan calc(3.2s*var(--spd)) ease-in-out infinite}
html[data-motion="dynamic"] .ne-scan{animation:ne-float calc(5.8s*var(--spd)) ease-in-out infinite alternate}
html[data-motion="minimal"] .ne-scan::after{animation:ne-scan calc(5s*var(--spd)) linear infinite}
html[data-motion="none"] .ne-marquee-track,html[data-motion="none"] .ne-scan,html[data-motion="none"] .ne-scan::after,html[data-motion="none"] .ne-wave i,html[data-motion="none"] .ne-node,html[data-motion="none"] .ne-brain-core,html[data-motion="none"] .ne-brain-core::after,html[data-motion="none"] .ne-scroll::after{animation:none!important}
@keyframes ne-wave{from{transform:scaleX(.24);opacity:.28}to{transform:scaleX(1);opacity:1}}
@keyframes ne-pulse{0%,100%{transform:scale(.72);opacity:.4}50%{transform:scale(1.35);opacity:1}}
@keyframes ne-brain{from{transform:translate3d(-6px,-8px,0) rotate(-2deg)}to{transform:translate3d(8px,8px,0) rotate(3deg)}}
@keyframes ne-shine{0%{transform:translateX(-58%)}48%,100%{transform:translateX(58%)}}
@keyframes ne-scroll{0%,100%{transform:scaleY(.46);transform-origin:top;opacity:.44}50%{transform:scaleY(1);opacity:1}}
@keyframes ne-panel-in{from{opacity:.65;transform:translateY(18px) scale(.985)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes ne-scan{0%,100%{top:16%;opacity:.45}50%{top:78%;opacity:1}}
@keyframes ne-float{from{transform:translateY(-10px)}to{transform:translateY(12px)}}
@media(prefers-reduced-motion:reduce){.ne-marquee-track,.ne-scan,.ne-scan::after,.ne-wave i,.ne-node,.ne-brain-core,.ne-brain-core::after,.ne-scroll::after{animation:none!important}}
@media(max-width:980px){
  .ne-hero-inner,.ne-about-grid,.ne-tab-panel,.ne-year-grid{grid-template-columns:1fr}
  .ne-visual{min-height:340px}
  .ne-service-grid{grid-template-columns:repeat(2,1fr)}
  .ne-partners{grid-template-columns:repeat(3,1fr)}
}
@media(max-width:700px){
  .ne-hero{padding-top:92px;background:linear-gradient(180deg,#aeb3c5 0%,#eef2f8 24%,#05103c 25%,#050a24 100%)}
  .ne-hero h1{font-size:clamp(54px,18vw,96px)}
  .ne-hero h1 span{text-align:left}
  .ne-visual{min-height:280px}
  .ne-about-panel,.ne-service-grid,.ne-gallery-grid{grid-template-columns:1fr}
  .ne-tabs{justify-content:flex-start;overflow-x:auto;flex-wrap:nowrap}
  .ne-tab-panel figure{min-height:240px}
  .ne-news a{grid-template-columns:1fr;gap:8px}
  .ne-news span{text-align:left}
}
</style></head>
<body>
<nav id="nav">
  ${logoBrand(cfg, `<a class="brand" href="#">${cfg.name}</a>`)}
  <div class="links">
    ${cfg.sections.about?'<a href="#about">About</a>':''}
    ${cfg.sections.services?'<a href="#services">Solution</a>':''}
    ${cfg.sections.doctors?'<a href="#doctors">Team</a>':''}
    ${cfg.sections.gallery?'<a href="#gallery">Facility</a>':''}
    ${cfg.sections.location?'<a href="#location">Contact</a>':''}
  </div>
  <a class="btn-call" href="${cfg.naverUrl||('tel:'+cfg.phone)}" ${cfg.naverUrl?'target="_blank" rel="noopener"':''}>${cfg.naverUrl?'예약문의':'전화문의'}</a>
  ${mobileNav(cfg)}
</nav>
<header class="ne-hero">
  ${heroVideo(cfg)}
  <div class="ne-hero-inner">
    <div class="ne-hero-copy" data-ne-motion="hero-copy">
      <span class="ne-kicker" data-reveal data-ne-motion="hero-kicker">Comprehensive Clinic Platform</span>
      <h1 data-reveal data-ne-motion="hero-title" style="--d:.08s"><span class="ne-word">All</span><span class="ne-word">Care</span></h1>
      <p data-reveal data-ne-motion="hero-copy" style="--d:.18s">${cfg.slogan}<br>${cfg.desc}</p>
      <div class="btns" data-reveal data-ne-motion="hero-actions" style="--d:.28s">
        ${heroCtaPrimary(cfg,'b1')}
        ${heroCta2(cfg,{cls:'b2',onDark:true,fallbackHref:'#services',fallbackText:'솔루션 보기'})}
      </div>
    </div>
    <div class="ne-visual" data-reveal data-ne-motion="hero-visual" style="--d:.2s">
      ${cfg.heroImg?`<div class="ne-visual-img"><img src="${cfg.heroImg}" alt="${cfg.name} 대표 이미지" decoding="async"></div>`:''}
      <div class="ne-brain-orbit" aria-hidden="true"><i class="ne-node n1"></i><i class="ne-node n2"></i><i class="ne-node n3"></i></div>
      <div class="ne-brain-core" aria-hidden="true"></div>
      <div class="ne-wave" aria-hidden="true"><i></i><i></i><i></i></div>
      <div class="ne-scan"><small>AI DATA</small><b>${cfg.name}</b></div>
    </div>
  </div>
  <div class="ne-scroll">SCROLL</div>
</header>

${cfg.sections.about?`<section id="about" class="ne-statement"><div class="wrap"><h2 data-reveal data-ne-motion="statement">${cfg.slogan}<br>${cfg.desc}</h2></div></section>
<section class="ne-about"><div class="wrap ne-about-grid">
  <div data-reveal data-ne-motion="section-copy"><span class="ne-label">AI · Data</span><h2 class="ne-title">정확한 상담에서<br>치료 계획까지</h2><p class="ne-copy">${cfg.desc}</p></div>
  <div class="ne-about-panel" data-reveal data-ne-motion="panel-grid" style="--d:.14s">
    <a href="#services"><b>One Stop Solution</b><span>평가, 설명, 진료, 관리 흐름을 한 화면에서 안내합니다.</span></a>
    <a href="#location"><b>Clinic Information</b><span>${cfg.addr}<br>${(cfg.hours||'').split('\n')[0]||''}</span></a>
    <a href="${cfg.naverUrl||('tel:'+cfg.phone)}"><b>Fast Reservation</b><span>상담과 예약 동선을 짧고 명확하게 연결합니다.</span></a>
    <a href="#gallery"><b>Facility Preview</b><span>방문 전 시설과 장비를 투명하게 확인합니다.</span></a>
  </div>
</div></section>`:''}

<div class="ne-marquee" data-reveal data-ne-motion="marquee" aria-hidden="true"><div class="ne-marquee-track">
  ${Array.from({length:10},()=>`<span><i></i>${cfg.name} Comprehensive Clinic Care</span>`).join('')}
</div></div>

${cfg.sections.services?`<section id="services" class="ne-solution"><div class="wrap">
  <div class="ne-center" data-reveal data-ne-motion="section-copy"><span class="ne-label">One Stop Solution</span><h2 class="ne-title">진료 흐름을 한 번에 이해하는<br>솔루션 구조</h2><p class="ne-copy">진료 항목을 목적별로 나누고, 필요한 설명과 예약 동선을 같은 위치에서 제공합니다.</p></div>
  ${solutionTabs.length?`<div class="ne-tabs" data-reveal data-ne-motion="tabs">${tabButtons}</div><div data-reveal data-ne-motion="solution-panel-wrap" style="--d:.12s">${tabPanels}</div>`:''}
</div></section>
<section class="ne-lineup"><div class="wrap">
  <div class="ne-center" data-reveal data-ne-motion="section-copy"><span class="ne-label">Line Up</span><h2 class="ne-title">차별화된 진료 라인업</h2><p class="ne-copy">주요 진료와 장비·프로그램을 카드형으로 빠르게 탐색합니다.</p></div>
  <div class="ne-service-grid">${servicesHTML}</div>
</div></section>`:''}

${cfg.sections.stats?`<section id="stats" class="ne-stats"><div class="wrap">
  <div class="ne-center" data-reveal data-ne-motion="section-copy"><span class="ne-label">Data</span><h2 class="ne-title">숫자로 확인하는 신뢰</h2><p class="ne-copy">설정한 통계 수치와 문구가 그대로 반영됩니다.</p></div>
  <div class="ne-stat-grid" data-reveal data-ne-motion="counter-grid">${statsHTML(cfg,'ne-stat')}</div>
</div></section>
<section class="ne-year"><div class="wrap">
  <div class="ne-year-grid" data-reveal data-ne-motion="year"><div><span class="ne-label">Global Partnership Network</span><p class="ne-copy">각 분야의 전문 파트너와 함께 더 나은 의료 경험을 설계합니다.</p></div><b>2026</b></div>
  <div class="ne-partners" data-reveal data-ne-motion="partners" aria-label="파트너 네트워크">${['Medical','AI Data','Care','Clinic','Research','Academy','Platform','Lab','Partner','Local','Media','Support'].map(x=>`<span>${x}</span>`).join('')}</div>
</div></section>`:''}

${cfg.sections.doctors?`<section id="doctors" class="ne-doctors"><div class="wrap">
  <div class="ne-center" data-reveal data-ne-motion="section-copy"><span class="ne-label">Medical Team</span><h2 class="ne-title">전문 의료진</h2><p class="ne-copy">진료 철학과 전문 분야를 명확하게 보여줍니다.</p></div>
  <div class="ne-doctor-grid">${doctors.map((d,i)=>`<article class="ne-doctor v5-dr" data-reveal data-ne-motion="doctor-card" style="--d:${(i*0.08).toFixed(2)}s"><div class="im">${d.img?`<img src="${d.img}" alt="${d.name}" loading="lazy" decoding="async">`:`<span class="ph">${C.initial(d.name)}</span>`}</div><div class="tx"><h3>${d.name} <small>원장</small></h3><p class="r">${d.role}</p><p class="t">${d.tag}</p></div></article>`).join('')}</div>
</div></section>`:''}

${cfg.sections.gallery && gallery.length?`<section id="gallery" class="ne-gallery"><div class="wrap">
  <div class="ne-center" data-reveal data-ne-motion="section-copy"><span class="ne-label">Facility</span><h2 class="ne-title">시설 · 장비 미리보기</h2><p class="ne-copy">실제 진료 공간과 장비 이미지를 갤러리로 구성합니다.</p></div>
  <div class="ne-gallery-grid">${gallery.map((g,i)=>`<figure class="ne-gallery-item x-gal gal-item" data-reveal data-ne-motion="gallery-card" style="--d:${(i*0.06).toFixed(2)}s"><div class="im">${g.img?`<img src="${g.img}" alt="${g.caption}" loading="lazy" decoding="async" data-lb>`:`<span class="ph">0${i+1}</span>`}</div><figcaption>${g.caption}</figcaption></figure>`).join('')}</div>
</div></section>`:''}

${cfg.sections.video && C.videoId?`<section id="video" class="ne-media"><div class="wrap">
  <div class="ne-center" data-reveal data-ne-motion="section-copy"><span class="ne-label">Media</span><h2 class="ne-title">소개 영상</h2><p class="ne-copy">병원 소개와 주요 장비를 영상으로 안내합니다.</p></div>
  <div class="x-video" data-reveal data-ne-motion="media-frame"><iframe src="https://www.youtube.com/embed/${C.videoId}" title="병원 소개 영상" allowfullscreen></iframe></div>
</div></section>`:''}

<section class="ne-media"><div class="wrap">
  <div class="ne-center" data-reveal data-ne-motion="section-copy"><span class="ne-label">Family Site</span><h2 class="ne-title">빠른 연결</h2><p class="ne-copy">예약, 시설, 오시는 길, 상담 동선을 한 곳에 모았습니다.</p></div>
  <div class="ne-news" data-reveal data-ne-motion="news-list">${familyItems.map((item,i)=>`<a href="${item.h}"><small>${item.k}</small><b>${item.t} — ${item.d}</b><span>0${i+1}</span></a>`).join('')}</div>
</div></section>

${cfg.sections.booking?`<section id="booking" class="ne-booking"><div class="wrap">
  <div data-reveal data-ne-motion="section-copy"><span class="ne-label">Inquiry</span><h2 class="ne-title">예약 문의</h2><p class="ne-copy">남겨주시면 확인 후 연락드립니다.</p></div>
  ${(()=>{
    const svcOptions=services.map(s=>`<option>${s.title}</option>`).join('');
    return `<div class="x-bk-wrap"><form class="x-bk" id="bkForm" data-reveal data-ne-motion="booking-form"><label>성함</label><input type="text" name="이름" required placeholder="홍길동"><label>연락처</label><input type="tel" name="연락처" required placeholder="010-0000-0000"><label>희망 진료</label><select name="진료">${svcOptions}<option>기타 / 상담</option></select><label>문의 내용 (선택)</label><textarea name="내용" placeholder="증상이나 희망 시간대를 적어주세요"></textarea><button type="submit">예약 문의 보내기</button><div class="bk-done" id="bkDone">접수되었습니다. 확인 후 빠르게 연락드리겠습니다.</div></form><div class="x-bkside" data-reveal data-ne-motion="contact-card" style="--d:.12s"><a class="tel" href="tel:${cfg.phone}">${cfg.phone}</a><p>진료 시간 내에는 전화 예약이 가장 빠릅니다.</p><p style="font-size:13.5px;color:rgba(255,255,255,.58)">${(cfg.hours||'').split('\n')[0]||''}</p>${naverBtn(cfg,4)}</div></div>`;
  })()}
</div></section>`:''}

${blocksHtml(cfg)}
${cfg.sections.faq?faqBlock(cfg,{bg:'#fff'}):''}
${cfg.sections.location?`<section id="location" class="ne-location"><div class="wrap">
  <div class="ne-center" data-reveal data-ne-motion="section-copy"><span class="ne-label">Contact</span><h2 class="ne-title">진료시간 · 오시는 길</h2></div>
  <div class="x-loc" data-reveal data-ne-motion="contact-card"><div><h3>진료시간</h3><p>${C.nl2br(cfg.hours)}</p></div><div><h3>오시는 길</h3><p>${cfg.addr}</p><p class="tel2">${cfg.phone}</p></div></div>
  ${mapEmbed(cfg,8)}
</div></section>`:''}

${footerHTML(cfg)}
${quickBar(cfg)}
${prodExtras(cfg)}
${siteScript(cfg)}
<script>
(function(){
  document.documentElement.classList.add('neuro-ready');
  var buttons=[].slice.call(document.querySelectorAll('[data-ne-tab]'));
  var panels=[].slice.call(document.querySelectorAll('[data-ne-panel]'));
  buttons.forEach(function(btn){
    btn.addEventListener('click',function(){
      var id=btn.getAttribute('data-ne-tab');
      buttons.forEach(function(b){ b.classList.toggle('active',b===btn); });
      panels.forEach(function(p){
        var active=p.getAttribute('data-ne-panel')===id;
        p.classList.toggle('active',active);
        if(active){
          p.classList.remove('motion-replay');
          void p.offsetWidth;
          p.classList.add('motion-replay');
        }
      });
    });
  });
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var noMotion=document.documentElement.getAttribute('data-motion')==='none';
  function runCount(el){
    if(el.dataset.neCounted==='1') return;
    el.dataset.neCounted='1';
    var raw=(el.dataset.rawValue||el.textContent||'').trim();
    var target=parseFloat(raw.replace(/,/g,''));
    if(!isFinite(target)||reduce||noMotion) return;
    var decimals=(raw.split('.')[1]||'').length;
    var hasComma=raw.indexOf(',')>-1;
    var start=performance.now();
    var duration=1250;
    function tick(now){
      var t=Math.min(1,(now-start)/duration);
      var eased=1-Math.pow(1-t,3);
      var value=target*eased;
      var text=decimals?value.toFixed(decimals):String(Math.round(value));
      if(hasComma) text=Number(text).toLocaleString('en-US',{minimumFractionDigits:decimals,maximumFractionDigits:decimals});
      el.textContent=text;
      if(t<1) requestAnimationFrame(tick);
      else el.textContent=raw;
    }
    requestAnimationFrame(tick);
  }
  var numbers=[].slice.call(document.querySelectorAll('.ne-stat .stat-number'));
  numbers.forEach(function(el){ el.dataset.rawValue=(el.textContent||'').trim(); });
  if(numbers.length){
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            numbers.forEach(runCount);
            io.disconnect();
          }
        });
      },{threshold:.28});
      var box=document.querySelector('.ne-stat-grid')||numbers[0];
      io.observe(box);
    }else{
      numbers.forEach(runCount);
    }
  }
})();
<\/script>
</body></html>`;
}
