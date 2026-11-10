/* cream 2026.11 vol.179 — common: header/menu/footer + motion */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 목차 데이터 (PDF 목차 기준) ---------- */
  var SECTIONS = [
    { key: 'trend', en: 'Trend & Focus', c: 'var(--trend)', href: 'trend.html', items: [
      ['04', 'SBS 세일즈 가이드 포인트', ''],
      ['06', 'TREND : 드라마에서 찾아보는 전문직 히어로의 쾌감', 'trend.html#trend'],
      ['08', 'FOCUS : 굿파트너2', 'trend.html#focus-goodpartner'],
      ['09', 'FOCUS : 나인 투 식스', 'trend.html#focus-ninetosix']
    ]},
    { key: 'lineup', en: 'Contents Line-up', c: 'var(--lineup)', href: '', items: [
      ['10', '2026 라인업', ''], ['11', 'IMC 간접/가상 판매 라인업', ''], ['12', '콘텐츠 라인업', '']
    ]},
    { key: 'sales', en: 'Sales Guide', c: 'var(--sales)', href: '', items: [
      ['20', 'SBS TV 판매안', ''], ['32', 'SBS 미디어넷 판매안', ''], ['42', 'SBS RD 판매안', '']
    ]},
    { key: 'digital', en: 'SBS Digital', c: 'var(--digital)', href: '', items: [
      ['45', '디지털 콘텐츠', ''], ['46', '디지털 스튜디오 콘텐츠 상품', ''], ['47', 'SBS 유튜브', ''], ['48', 'SBS Play', '']
    ]},
    { key: 'table', en: 'Program Table', c: 'var(--table)', href: '', items: [
      ['50', '매체 별 편성표', ''], ['59', 'SBS M&C 마케팅 지원 제도 안내', '']
    ]}
  ];
  window.CREAM_SECTIONS = SECTIONS;

  var page = document.body.getAttribute('data-page') || '';
  var darkHdr = document.body.hasAttribute('data-dark-header');

  function esc(s) { return String(s).replace(/[&<>"]/g, function (m) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]; }); }

  /* ---------- header ---------- */
  var nav = SECTIONS.map(function (s) {
    var cur = s.key === page ? ' aria-current="page"' : '';
    if (!s.href) return '<a class="is-soon" href="#" aria-disabled="true" title="준비 중"><i class="dot" style="color:' + s.c + '"></i>' + esc(s.en) + '</a>';
    return '<a href="' + s.href + '"' + cur + '><i class="dot" style="color:' + s.c + '"></i>' + esc(s.en) + '</a>';
  }).join('');
  var hdr = document.createElement('header');
  hdr.className = 'hdr' + (darkHdr ? ' hdr--dark' : '');
  hdr.innerHTML =
    '<div class="hdr__in">' +
      '<a class="hdr__logo" href="index.html" aria-label="cream 홈">' +
        '<img class="black" src="images/cream-logo.png" alt="cream" width="1037" height="218">' +
        '<img class="white" src="images/cream-logo-white.png" alt="" width="1037" height="218">' +
        '<span class="hdr__vol">2026.11<br>VOL.179</span>' +
      '</a>' +
      '<nav class="hdr__nav" aria-label="주요 섹션">' + nav + '</nav>' +
      '<button class="hdr__burger" type="button" aria-label="전체 메뉴 열기" aria-expanded="false" aria-controls="menu"><span></span></button>' +
    '</div>';
  document.body.insertBefore(hdr, document.body.firstChild);

  var skip = document.createElement('a');
  skip.className = 'skip'; skip.href = '#main'; skip.textContent = '본문 바로가기';
  document.body.insertBefore(skip, document.body.firstChild);

  /* ---------- full menu ---------- */
  var menu = document.createElement('div');
  menu.className = 'menu'; menu.id = 'menu';
  menu.setAttribute('aria-hidden', 'true');
  menu.innerHTML = '<div class="menu__in">' + SECTIONS.map(function (s, i) {
    return '<div class="menu__col" style="--i:' + i + '"><h3><i class="dot" style="color:' + s.c + '"></i>' + esc(s.en) + '</h3><ul>' +
      s.items.map(function (it) {
        return it[2]
          ? '<li><a href="' + it[2] + '"><b>' + it[0] + '</b>' + esc(it[1]) + '</a></li>'
          : '<li><a class="is-soon" tabindex="-1"><b>' + it[0] + '</b>' + esc(it[1]) + '</a></li>';
      }).join('') + '</ul></div>';
  }).join('') + '</div>';
  hdr.after(menu);

  var burger = hdr.querySelector('.hdr__burger');
  function setMenu(open) {
    doc.classList.toggle('is-menu', open);
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? '전체 메뉴 닫기' : '전체 메뉴 열기');
    menu.setAttribute('aria-hidden', !open);
  }
  burger.addEventListener('click', function () { setMenu(!doc.classList.contains('is-menu')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a[href]')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  hdr.querySelectorAll('.is-soon').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); }); });

  /* ---------- footer ---------- */
  var ftr = document.createElement('footer');
  ftr.className = 'ftr';
  ftr.innerHTML =
    '<div class="wrap">' +
      '<div class="ftr__top">' +
        '<div class="ftr__logo"><img src="images/cream-logo-white.png" alt="cream" width="1037" height="218"><p>SBS M&amp;C MONTHLY MAGAZINE</p></div>' +
        '<nav class="ftr__nav" aria-label="섹션">' + SECTIONS.map(function (s) {
          return s.href ? '<a href="' + s.href + '">' + esc(s.en) + '</a>' : '<a class="is-soon">' + esc(s.en) + '</a>';
        }).join('') + '</nav>' +
      '</div>' +
      '<div class="ftr__bot">' +
        '<address><strong>SBS M&amp;C</strong> 광고문의 : 서울특별시 양천구 목동서로 161 &nbsp;|&nbsp; 02)6262-2929 &nbsp;|&nbsp; <a href="https://www.methodia.co.kr" target="_blank" rel="noopener">www.methodia.co.kr</a></address>' +
        '<p>cream 2026년 11월호 (제179호)</p>' +
      '</div>' +
    '</div>';
  document.body.appendChild(ftr);

  /* ---------- to top + progress ---------- */
  var top = document.createElement('button');
  top.className = 'totop'; top.type = 'button'; top.setAttribute('aria-label', '맨 위로');
  top.innerHTML = '<svg class="ring" viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="24"/><circle cx="26" cy="26" r="24"/></svg>' +
    '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M8 13V3M3.5 7.5 8 3l4.5 4.5"/></svg>';
  document.body.appendChild(top);
  top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  var progress = document.querySelector('.progress');

  /* ---------- split text ---------- */
  document.querySelectorAll('[data-split]').forEach(function (el) {
    var label = el.textContent.replace(/\s+/g, ' ').trim();
    var i = 0;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (word) {
            if (!word) return;
            if (/^\s+$/.test(word)) { frag.appendChild(document.createTextNode(' ')); return; }
            var w = document.createElement('span');
            w.style.whiteSpace = 'nowrap'; w.style.display = 'inline-block';
            Array.from(word).forEach(function (c) {
              var o = document.createElement('span'); o.className = 'ch'; o.setAttribute('aria-hidden', 'true');
              var inner = document.createElement('span'); inner.textContent = c; o.style.setProperty('--ci', i++);
              o.appendChild(inner); w.appendChild(o);
            });
            frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    };
    walk(el);
    el.classList.add('split');
    el.setAttribute('aria-label', label);
    if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', 'none');
  });
  document.querySelectorAll('.lines').forEach(function (el) {
    Array.prototype.forEach.call(el.children, function (c, i) {
      var inner = document.createElement('span');
      while (c.firstChild) inner.appendChild(c.firstChild);
      c.appendChild(inner); c.style.setProperty('--li', i);
    });
    if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', 'none');
  });

  /* ---------- reveal ---------- */
  var targets = document.querySelectorAll('[data-reveal],[data-count]');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-in');
        if (en.target.hasAttribute('data-count')) countUp(en.target);
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });
    targets.forEach(function (t) { io.observe(t); });
    /* 첫 화면 안에 걸친 요소는 rootMargin 과 무관하게 바로 등장 */
    var vh0 = window.innerHeight;
    targets.forEach(function (t) {
      if (t.getBoundingClientRect().top < vh0) {
        t.classList.add('is-in');
        if (t.hasAttribute('data-count')) countUp(t);
        io.unobserve(t);
      }
    });
  } else {
    targets.forEach(function (t) { t.classList.add('is-in'); if (t.hasAttribute('data-count')) countUp(t, true); });
  }

  function countUp(el, instant) {
    var to = parseFloat(el.getAttribute('data-count'));
    var dec = (el.getAttribute('data-count').split('.')[1] || '').length;
    var fmt = function (v) { return v.toLocaleString('ko-KR', { minimumFractionDigits: dec, maximumFractionDigits: dec }); };
    if (instant || reduce) { el.textContent = fmt(to); return; }
    var dur = 1600, t0 = null;
    var step = function (ts) {
      if (!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      el.textContent = fmt(to * (1 - Math.pow(1 - p, 4)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  /* ---------- scroll loop: header / progress / parallax ---------- */
  var para = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
  var lastY = window.scrollY, ticking = false;
  function onScroll() {
    var y = window.scrollY, vh = window.innerHeight;
    var max = Math.max(1, doc.scrollHeight - vh);
    var p = Math.min(1, y / max);
    hdr.classList.toggle('is-solid', y > 40);
    hdr.classList.toggle('is-hidden', y > 400 && y > lastY + 4 && !doc.classList.contains('is-menu'));
    if (y < lastY - 4) hdr.classList.remove('is-hidden');
    top.classList.toggle('is-on', y > vh * 0.8);
    top.style.setProperty('--p', p.toFixed(4));
    if (progress) progress.style.setProperty('--p', p.toFixed(4));
    if (!reduce) para.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var k = parseFloat(el.getAttribute('data-parallax')) || 0.15;
      var off = (r.top + r.height / 2 - vh / 2) * -k;
      el.style.transform = 'translate3d(0,' + off.toFixed(1) + 'px,0)';
    });
    lastY = y; ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- drag-to-scroll tracks ---------- */
  document.querySelectorAll('[data-drag]').forEach(function (el) {
    var down = false, sx = 0, sl = 0, moved = false;
    el.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse') return;
      down = true; moved = false; sx = e.clientX; sl = el.scrollLeft; el.classList.add('is-drag');
    });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - sx; if (Math.abs(dx) > 4) moved = true;
      el.scrollLeft = sl - dx;
    });
    window.addEventListener('pointerup', function () { down = false; el.classList.remove('is-drag'); });
    el.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
    el.addEventListener('dragstart', function (e) { e.preventDefault(); });
    var scope = el.closest('section') || el.parentElement;
    var prev = scope.querySelector('[data-drag-prev]'), next = scope.querySelector('[data-drag-next]');
    var by = function (d) { el.scrollBy({ left: d * el.clientWidth * 0.8, behavior: reduce ? 'auto' : 'smooth' }); };
    if (prev) prev.addEventListener('click', function () { by(-1); });
    if (next) next.addEventListener('click', function () { by(1); });
    var bar = scope.querySelector('[data-drag-bar]');
    if (bar) {
      var upd = function () { var m = el.scrollWidth - el.clientWidth; bar.style.setProperty('--p', m > 0 ? (el.scrollLeft / m).toFixed(4) : 1); bar.style.setProperty('--w', (el.clientWidth / el.scrollWidth).toFixed(4)); };
      el.addEventListener('scroll', upd, { passive: true }); window.addEventListener('resize', upd); upd();
    }
  });
})();
