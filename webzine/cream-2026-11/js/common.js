/* cream 2026.11 VOL.179 — 공통: 헤더 / 목차 메뉴 / 푸터 / 등장 모션 / 이미지 확대 */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 목차 (원본 CONTENTS 페이지 그대로) ----------
     [쪽, 제목, 링크] — 링크는 각 페이지의 id="p쪽번호" 앵커 */
  var SECTIONS = [
    { key: 'trend', en: 'Trend & Focus', c: 'var(--trend)', href: 'trend.html', items: [
      ['04', 'SBS 광고상품 라인업', 'trend.html#p04'],
      ['06', 'TREND : 드라마에서 찾아보는 전문직 히어로의 쾌감', 'trend.html#p06'],
      ['08', 'FOCUS : 굿파트너2', 'trend.html#p08'],
      ['09', 'FOCUS : 나인 투 식스', 'trend.html#p09']
    ]},
    { key: 'lineup', en: 'Contents Line-up', c: 'var(--lineup)', href: 'lineup.html', items: [
      ['10', '2026 라인업', 'lineup.html#p10'],
      ['11', 'IMC 간접/가상 판매 라인업', 'lineup.html#p11'],
      ['12', '콘텐츠 라인업', 'lineup.html#p12']
    ]},
    { key: 'sales', en: 'Sales Guide', c: 'var(--sales)', href: 'sales-tv.html', items: [
      ['20', 'SBS TV 판매안', 'sales-tv.html#p20'],
      ['28', 'SBS 어드레서블 TV', 'sales-addressable.html#p28'],
      ['32', 'SBS 미디어넷 판매안', 'sales-medianet.html#p32'],
      ['42', 'SBS RD 판매안', 'sales-radio.html#p42']
    ]},
    { key: 'digital', en: 'SBS Digital', c: 'var(--digital)', href: 'digital.html', items: [
      ['45', 'SBS Digital Set-Up : 디지털 콘텐츠', 'digital.html#p45'],
      ['46', 'SBS Digital Set-Up : 디지털 스튜디오 콘텐츠 상품', 'digital.html#p46'],
      ['47', 'SBS Digital Set-Up : SBS 유튜브', 'digital.html#p47'],
      ['48', 'SBS Digital Set-Up : SBS Play', 'digital.html#p48']
    ]},
    { key: 'table', en: 'Program Table', c: 'var(--table)', href: 'table.html', items: [
      ['50', '매체 별 편성표', 'table.html#p50'],
      ['59', 'SBS M&C 마케팅 지원 제도 안내', 'support.html#p59']
    ]}
  ];
  window.CREAM_SECTIONS = SECTIONS;

  var section = document.body.getAttribute('data-section') || '';
  function esc(s) { return String(s).replace(/[&<>"]/g, function (m) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]; }); }

  function tocGroup(s) {
    return '<div class="toc-group" style="--tc:' + s.c + '"><p class="toc-group__head"><i></i>' + esc(s.en) + '</p><ol>' +
      s.items.map(function (it) { return '<li><a href="' + it[2] + '"><b>' + it[0] + '</b><em>' + esc(it[1]) + '</em></a></li>'; }).join('') +
      '</ol></div>';
  }
  window.CREAM_TOC = function () { return SECTIONS.map(tocGroup).join(''); };

  /* ---------- 헤더 ---------- */
  var hdr = document.createElement('header');
  hdr.className = 'hdr';
  hdr.innerHTML =
    '<div class="hdr__in">' +
      '<a class="hdr__logo" href="index.html" aria-label="cream 2026년 11월호 홈"><img src="images/cream-logo.png" alt="cream" width="1037" height="218"><span class="hdr__vol">2026.11<br>VOL.179</span></a>' +
      '<nav class="hdr__nav" aria-label="섹션">' + SECTIONS.map(function (s) {
        return '<a href="' + s.href + '" style="--nc:' + s.c + '"' + (s.key === section ? ' aria-current="page"' : '') + '>' + esc(s.en) + '</a>';
      }).join('') + '</nav>' +
      '<button class="hdr__burger" type="button" aria-label="목차 열기" aria-expanded="false" aria-controls="menu"><span></span></button>' +
    '</div>';
  document.body.insertBefore(hdr, document.body.firstChild);
  var skip = document.createElement('a');
  skip.className = 'skip'; skip.href = '#main'; skip.textContent = '본문 바로가기';
  document.body.insertBefore(skip, hdr);

  var menu = document.createElement('div');
  menu.className = 'menu'; menu.id = 'menu'; menu.setAttribute('aria-hidden', 'true');
  menu.innerHTML = '<div class="menu__in">' + window.CREAM_TOC() + '</div>';
  hdr.after(menu);
  var burger = hdr.querySelector('.hdr__burger');
  function setMenu(open) {
    doc.classList.toggle('is-menu', open);
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? '목차 닫기' : '목차 열기');
    menu.setAttribute('aria-hidden', !open);
  }
  burger.addEventListener('click', function () { setMenu(!doc.classList.contains('is-menu')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setMenu(false); closeZoom(); } });

  /* ---------- 오른쪽 세로 섹션 탭 ---------- */
  var cur = SECTIONS.filter(function (s) { return s.key === section; })[0];
  if (cur) {
    var tab = document.createElement('p');
    tab.className = 'side-tab'; tab.setAttribute('aria-hidden', 'true');
    tab.textContent = cur.en.toUpperCase();
    document.body.appendChild(tab);
  }

  /* ---------- 푸터 ---------- */
  var ftr = document.createElement('footer');
  ftr.className = 'ftr';
  ftr.innerHTML =
    '<div class="wrap ftr__in">' +
      '<div class="ftr__cream"><img src="images/cream-logo.png" alt="cream" width="1037" height="218"><p>2026년 11월호 (제179호)</p></div>' +
      '<div class="ftr__kakao"><img class="qr" src="images/common/qr.png" alt="cream 카카오톡 채널 QR 코드" width="215" height="215"><div><img class="talk" src="images/common/kakao.png" alt="카카오톡" width="105" height="105"><p>플친맺고 cream을<br>1등으로 받아보자!</p></div></div>' +
      '<div class="ftr__mnc"><img src="images/common/sbs-mnc.png" alt="SBS M&amp;C" width="450" height="115"><address>광고문의 : 서울특별시 양천구 목동서로 161<br>02)6262 - 2929 &nbsp;<a href="https://www.methodia.co.kr" target="_blank" rel="noopener">www.methodia.co.kr</a></address></div>' +
    '</div>';
  document.body.appendChild(ftr);

  /* ---------- 맨 위로 ---------- */
  var top = document.createElement('button');
  top.className = 'totop'; top.type = 'button'; top.setAttribute('aria-label', '맨 위로');
  top.innerHTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 13V3M3.5 7.5 8 3l4.5 4.5"/></svg>';
  document.body.appendChild(top);
  top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () { top.classList.toggle('is-on', window.scrollY > window.innerHeight * 0.8); ticking = false; });
  }, { passive: true });

  /* ---------- 등장 모션 ---------- */
  var targets = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.01 });
    var vh = window.innerHeight;
    targets.forEach(function (t) {
      if (t.getBoundingClientRect().top < vh) t.classList.add('is-in'); else io.observe(t);
    });
  } else {
    targets.forEach(function (t) { t.classList.add('is-in'); });
  }

  /* ---------- 이미지 확대 (img[data-zoom]) : 편성표 등 촘촘한 원본 지면용 ---------- */
  var zoom = null;
  function closeZoom() { if (zoom) { zoom.remove(); zoom = null; doc.style.overflow = ''; } }
  document.addEventListener('click', function (e) {
    var img = e.target.closest('img[data-zoom]');
    if (!img) return;
    zoom = document.createElement('div');
    zoom.setAttribute('role', 'dialog'); zoom.setAttribute('aria-label', '이미지 크게 보기');
    zoom.style.cssText = 'position:fixed;inset:0;z-index:300;background:rgba(0,0,0,.88);overflow:auto;-webkit-overflow-scrolling:touch;cursor:zoom-out';
    var src = img.getAttribute('data-zoom') || img.currentSrc || img.src;
    zoom.innerHTML = '<img src="' + src + '" alt="' + esc(img.alt) + '" style="max-width:none;width:max(100%,1600px);margin:0 auto;background:#fff">' +
      '<button type="button" aria-label="닫기" style="position:fixed;top:12px;right:12px;width:44px;height:44px;border-radius:50%;background:#fff;font-size:22px;line-height:1">&times;</button>';
    zoom.addEventListener('click', closeZoom);
    document.body.appendChild(zoom); doc.style.overflow = 'hidden';
  });
})();
