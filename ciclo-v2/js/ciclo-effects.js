/* CICLO 사이트 효과 v2.1 — 테마가 푸터에서 enqueue 한다
 *
 * v2.1 변경
 *   + 스크롤 등장을 되살렸다. 단 v1 과 권한 배치가 반대다(아래 주석 참고).
 *     숨기는 것도 JS 가 한다. JS 가 없거나 죽으면 모션만 없고 내용은 그대로다.
 *
 * v1 대비 변경 (238LAB 이식 플랜 D):
 *   - v1 방식의 스크롤 등장(.reveal 주입) 삭제 — 콘텐츠가 사라지는 구조였다
 *   - 히어로 패럴럭스(스크롤 시 h1 translateY/opacity) 삭제
 *   - 사이드바 토글에 접근성 보강: aria 상태 · 포커스 트랩 · 스크롤 잠금 · 포커스 복원
 *   - 현재 페이지 aria-current 표시
 *
 * 모션 삭제 근거
 *   238LAB 은 스크롤 리빌이 0개다. 의도적으로 거의 움직이지 않는다.
 *   씨클로 v1 은 .overline/.sec-h2/.card/.step/.fit/.svc-row/.faq-row/.mean/
 *   .channel/.work-grid>* 전부에 .reveal 을 붙여, 로드 시점에 22개 중 21개가
 *   opacity:0 이었다. 서비스 섹션 전체와 SELECTED WORK 가 첫 화면에 없었다.
 *   게다가 관찰자가 발화하지 않아 끝까지 스크롤해도 영구히 안 보이는 노드가
 *   5개 남았다. 지우면 그 버그도 같이 사라진다.
 *
 *   히어로 패럴럭스는 h1 을 최대 220px 끌어내리고 y=620 에서 opacity 0 으로
 *   죽였다. 히어로 카피가 스크롤 중에 읽히지 않는 원인이었다.
 *
 * ※ global.css v2 와 짝이다. 구버전 CSS 가 남아 있으면 .reveal{opacity:0} 때문에
 *   콘텐츠가 안 보인다. CSS 를 먼저 교체할 것.
 *
 * ※ 이 스니펫에 JSON-LD 를 붙이지 말 것. v1 에서 <script> 태그 없이 붙인 스키마가
 *   SyntaxError 를 내서 스니펫 전체가 실행되지 않고 있었다. 구조화 데이터는
 *   SEO 플러그인이 이미 출력한다.
 */
(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') { fn(); }
    else { document.addEventListener('DOMContentLoaded', fn); }
  }

  ready(function () {
    var burger   = document.querySelector('.nav-burger'),
        closeBtn = document.querySelector('.sidebar-close'),
        side     = document.querySelector('.sidebar'),
        scrim    = document.querySelector('.scrim'),
        lastFocus = null;

    var FOCUSABLE = 'a[href],button:not([disabled]),[tabindex]:not([tabindex="-1"])';

    function openSide() {
      if (!side) return;
      lastFocus = document.activeElement;
      side.classList.add('open');
      if (scrim) { scrim.hidden = false; scrim.classList.add('open'); }
      document.body.classList.add('nav-open');
      if (burger) burger.setAttribute('aria-expanded', 'true');
      var first = side.querySelector(FOCUSABLE);
      if (first) first.focus();
    }

    function shutSide() {
      if (!side) return;
      side.classList.remove('open');
      if (scrim) {
        scrim.classList.remove('open');
        // 페이드아웃이 끝난 뒤에 감춘다
        setTimeout(function () { if (!scrim.classList.contains('open')) scrim.hidden = true; }, 300);
      }
      document.body.classList.remove('nav-open');
      if (burger) burger.setAttribute('aria-expanded', 'false');
      (lastFocus || burger || document.body).focus();
    }

    if (burger)   burger.addEventListener('click', openSide);
    if (closeBtn) closeBtn.addEventListener('click', shutSide);
    if (scrim)    scrim.addEventListener('click', shutSide);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && side && side.classList.contains('open')) shutSide();
    });

    // 포커스 트랩 — 열린 동안 탭이 사이드바 밖으로 나가지 않게
    if (side) side.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var f = side.querySelectorAll(FOCUSABLE);
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    // 사이드바 안 링크를 누르면 닫는다 (같은 페이지 앵커일 때 열린 채 남는 것 방지)
    if (side) side.addEventListener('click', function (e) {
      if (e.target.closest('a[href]')) shutSide();
    });

    // 현재 페이지 표시
    var here = (location.pathname || '/').replace(/\/+$/, '') || '/';
    document.querySelectorAll('.nav-links a[href], .sidebar-menu a[href]').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (href.charAt(0) === '#' || href.indexOf('/#') === 0 || /^https?:/.test(href)) return;
      var p = href.replace(/\/+$/, '') || '/';
      if (p === here) a.setAttribute('aria-current', 'page');
    });

    /* ── 스크롤 등장 (v2.1) ─────────────────────────────────────────
     * v2 에서 통째로 뺐던 것을 구조를 바꿔 되살린다.
     *
     * v1 의 버그는 권한 배치였다. "숨기기"가 CSS 에 있고 "보이기"가 JS 에
     * 있어서, 관찰자가 한 번 어긋나면 콘텐츠가 영구히 사라졌다. 실제로
     * 22개 중 5개가 끝까지 안 보였고 서비스 섹션 전체가 첫 화면에 없었다.
     *
     * 이번에는 숨기는 권한도 JS 가 쥔다.
     *   · CSS 기본값은 "다 보임". html.mo 가 붙어야 비로소 숨는다
     *   · html.mo 는 스크롤 감시를 걸기 직전, 같은 try 블록 안에서만 붙인다
     *   · 어디서든 예외가 나면 mo 를 떼서 원래대로 되돌린다
     * JS 가 없어도, 죽어도, 중간에 터져도 글이 사라지는 경로가 없다.
     *
     * ★ 감시 단위는 "섹션"이다. 카드 한 장 한 장을 감시하면 안 된다.
     *   .section 에는 content-visibility:auto 가 걸려 있다(성능 패스에서 넣은
     *   것으로, 첫 렌더에서 화면 밖 섹션의 레이아웃을 통째로 건너뛴다).
     *   건너뛴 서브트리 안의 요소는 상자가 없다. 카드 단위로 붙여 실측했더니
     *   끝까지 스크롤해도 1440 에서 11개, 390 에서 15개가 안 보인 채 남았다 —
     *   v1 과 같은 증상이다. 섹션 상자 자체는 contain-intrinsic-size 로 늘
     *   레이아웃되므로 안전하다. 감시는 섹션에, 계단은 그 안의 .mo-i 에 준다.
     *
     * 히어로(.hero)와 서브페이지 히어로(.page-hero)는 대상에서 뺀다. 첫 화면
     * 요소를 JS 로 숨겼다 보이면 깜빡임이 생기고, 무엇보다 그 h1 이 그 페이지의
     * LCP 요소다. opacity 0 에서 시작하면 LCP 가 애니메이션 시간만큼 밀린다.
     * 홈 히어로 입장은 global.css 의 CSS 애니메이션이 따로 맡는다.
     */
    (function () {
      if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;

      var root = document.documentElement,
          STEP = 70,   // 계단 간격(ms)
          MAXI = 6;    // 6칸(420ms)에서 끊는다. 더 주면 섹션 끝이 늦게 온다
      // 그리드는 덩어리째 띄우면 카드 여섯 장이 한꺼번에 튄다. 한 단계 내려간다.
      var GRID = '.grid-2,.grid-3,.grid-4,.dx-grid,.res-cards,.psi-cards,' +
                 '.work-grid,.svc-list,.fit-list';

      var secs = [];

      document.querySelectorAll('.section, .footer .inner').forEach(function (sec) {
        // .section > .wrap 한 겹을 쓰는 섹션이 있다. 그 안쪽을 본다.
        var host = sec;
        if (sec.children.length === 1 && sec.firstElementChild &&
            sec.firstElementChild.classList.contains('wrap')) host = sec.firstElementChild;

        var n = 0;
        function mark(el) {
          el.classList.add('mo-i');
          if (n) el.style.setProperty('--mo-d', (Math.min(n, MAXI) * STEP) + 'ms');
          n++;
        }

        Array.prototype.forEach.call(host.children, function (el) {
          if (el.matches && el.matches(GRID)) {
            Array.prototype.forEach.call(el.children, mark);
          } else {
            mark(el);
          }
        });

        if (n) { sec.setAttribute('data-mo', ''); secs.push(sec); }
      });

      if (!secs.length) return;

      /* 왜 IntersectionObserver 를 안 쓰나
       * 처음엔 썼는데, .section 의 content-visibility:auto 와 맞물려 구멍이 났다.
       * 화면에서 멀어진 섹션은 다시 건너뛰기로 돌아가면서 실제 높이가
       * contain-intrinsic-size 추정치로 되돌아간다. 그만큼 아래 내용이 위로
       * 당겨지므로, 빠르게 스크롤하면 어떤 섹션은 한 번도 뷰포트 안에 들어오지
       * 않은 채로 지나간다. 실측에서 홈 1024 기준 25개 항목이 안 보인 채 남았다.
       *
       * 그래서 "지나쳤는가"를 직접 본다. 섹션은 페이지당 열 개 안팎이라
       * rAF 로 묶은 스크롤 핸들러에서 rect 를 읽어도 비용이 없고, 무엇보다
       * 결과가 스크롤 속도에 의존하지 않는다. 윗변이 뷰포트 아래 94% 선을
       * 넘었으면(= 화면 위로 지나간 것 포함) 무조건 켠다.
       */
      var pending = secs.slice(), ticking = false, dead = false;

      function sweep(now) {
        var vh = window.innerHeight || 800, i = 0;
        while (i < pending.length) {
          var el = pending[i], r = el.getBoundingClientRect();
          if (r.top < vh * 0.94) {
            // 첫 훑기에 이미 화면 안이던 섹션은 전환 없이 그대로 켠다.
            // 첫 화면 요소가 떴다 사라졌다 하는 깜빡임을 만들지 않기 위해서다.
            if (now) el.classList.add('mo-now');
            el.classList.add('mo-in');
            pending.splice(i, 1);
          } else i++;
        }
        if (!pending.length) off();
      }

      function onScroll() {
        if (ticking || dead) return;
        ticking = true;
        requestAnimationFrame(function () {
          ticking = false;
          try { sweep(false); } catch (err) { fail(); }
        });
      }

      function off() {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('resize', onScroll);
      }

      // 무슨 일이 생기든 글이 사라지지는 않게 — mo 를 떼면 CSS 기본값(다 보임)으로 돌아간다
      function fail() { dead = true; off(); root.classList.remove('mo'); }

      try {
        root.classList.add('mo');
        sweep(true);
        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('resize', onScroll, { passive: true });
      } catch (err) { fail(); return; }

      // 지연 로드된 것이 레이아웃을 바꿨을 수 있다. 두 번 더 훑고 끝낸다.
      window.addEventListener('load', onScroll);
      setTimeout(onScroll, 1200);
    })();

    /* ── 제목 줄 단위 등장 ─────────────────────────────────────────
     * h2 를 통째로 띄우지 않고 줄마다 아래에서 밀어 올린다.
     * 제목에는 이미 <br> 로 줄이 나뉘어 있다. 그 자리를 그대로 쓴다 —
     * 글자를 쪼개지 않고 기존 줄바꿈을 감싸기만 하므로, 이 코드가 안 돌아도
     * h2 는 원문 그대로 남고 읽는 데 아무 문제가 없다.
     */
    document.querySelectorAll('.sec-h2').forEach(function (h) {
      if (h.querySelector('.ln')) return;
      var html = h.innerHTML;
      if (!/<br\s*\/?>/i.test(html)) return;          // 한 줄짜리는 둘 필요가 없다
      var lines = html.split(/<br\s*\/?>/i);
      h.innerHTML = lines.map(function (l, i) {
        return '<span class="ln" style="--ld:' + (i * 90) + 'ms"><i>' + l + '</i></span>';
      }).join('');
    });

    /* ── 숫자 카운트업 ─────────────────────────────────────────────
     * 데이터를 파는 페이지에서 숫자가 올라가는 건 장식이 아니라 읽는 순서를
     * 만든다. 정수만 올린다 — "3/3", "−61", "1.0초" 같은 건 손대지 않는다.
     * 자릿수가 늘면 폭이 변해 옆 글자가 밀리므로, 최종 자릿수만큼 min-width 를
     * 미리 잡고 tabular-nums 로 자폭을 고정한다. 그래서 CLS 가 0 으로 남는다.
     */
    (function () {
      if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;

      var SEL = '.ev-num,.ev-val,.hp-i b,.res-big b,.psi-ring,.dx-bar b,.ev-dot b';
      var jobs = [];

      document.querySelectorAll(SEL).forEach(function (el) {
        // 숫자 노드만 고른다. 뒤에 붙은 단위(<i>점</i>)는 건드리지 않는다.
        var node = null;
        for (var i = 0; i < el.childNodes.length; i++) {
          var c = el.childNodes[i];
          if (c.nodeType === 3 && /^\s*\d+\s*$/.test(c.textContent)) { node = c; break; }
        }
        if (!node) return;
        var target = parseInt(node.textContent, 10);
        if (!(target > 0)) return;

        var span = document.createElement('span');
        span.className = 'cnt';
        span.style.setProperty('--dg', String(target).length);
        span.textContent = '0';
        node.parentNode.replaceChild(span, node);
        jobs.push({ el: el, span: span, to: target, done: false });
      });

      if (!jobs.length) return;

      var EASE = function (t) { return 1 - Math.pow(1 - t, 3); };   // 감속

      function run(j) {
        if (j.done) return;
        j.done = true;
        var t0 = 0, DUR = 900;
        function step(ts) {
          if (!t0) t0 = ts;
          var k = Math.min(1, (ts - t0) / DUR);
          j.span.textContent = Math.round(EASE(k) * j.to);
          if (k < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      }

      /* 무엇을 보고 발화시키나 — 숫자 자신이 아니라 그 숫자가 든 섹션이다.
       * .section 에는 content-visibility:auto 가 걸려 있어서, 화면 밖이면
       * 안쪽 요소의 rect 가 전부 0 으로 나온다. 숫자 rect 로 판정했더니
       * bottom>0 을 못 넘겨 증거 밴드 숫자가 전부 0 에 멈춰 있었다.
       * 섹션 상자는 contain-intrinsic-size 로 늘 레이아웃되므로 안전하다.
       * 위 등장 효과가 같은 이유로 섹션 단위인 것과 같은 판단이다. */
      jobs.forEach(function (j) { j.host = j.el.closest('[data-mo]'); });

      function sweep() {
        var vh = window.innerHeight || 800, live = 0;
        jobs.forEach(function (j) {
          if (j.done) return;
          live++;
          // 히어로처럼 섹션 밖에 있는 숫자는 첫 화면이라 바로 올린다
          if (!j.host) { run(j); return; }
          var r = j.host.getBoundingClientRect();
          if (r.top < vh * 0.9 && r.bottom > 0) run(j);
        });
        if (!live) off();
      }

      var tick = false;
      function onScroll() {
        if (tick) return;
        tick = true;
        requestAnimationFrame(function () { tick = false; try { sweep(); } catch (e) { off(); } });
      }
      function off() {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('resize', onScroll);
      }

      sweep();
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll, { passive: true });
      window.addEventListener('load', onScroll);
      // 지연 로드가 레이아웃을 바꿨을 수 있다. 한 번 더 훑는다.
      setTimeout(onScroll, 1200);
    })();

    /* ── 히어로 마크 시차 · 내비 스크롤 반응 ───────────────────────── */
    (function () {
      var root = document.documentElement;

      // 내비 — 히어로를 지나면 그림자가 짙어지고 아주 조금 작아진다
      var t = false;
      function nav() {
        if (t) return;
        t = true;
        requestAnimationFrame(function () {
          t = false;
          root.classList.toggle('scrolled', (window.scrollY || 0) > 80);
        });
      }
      nav();
      window.addEventListener('scroll', nav, { passive: true });

      if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      if (window.matchMedia && !matchMedia('(pointer:fine)').matches) return;   // 터치 기기 제외

      var mark = document.querySelector('.hero-mark');
      if (!mark) return;
      var f = false;
      window.addEventListener('mousemove', function (e) {
        if (f) return;
        f = true;
        requestAnimationFrame(function () {
          f = false;
          var x = (e.clientX / window.innerWidth - .5) * 24;    // ±12px
          var y = (e.clientY / window.innerHeight - .5) * 24;
          mark.style.setProperty('--mx', x.toFixed(1) + 'px');
          mark.style.setProperty('--my', y.toFixed(1) + 'px');
        });
      }, { passive: true });
    })();

    // 구버전 잔재 정리 — 이전 스니펫이 캐시에 남아 .reveal 을 붙였을 경우 대비.
    // global.css v2 가 .reveal 을 무해화하지만 인라인 transitionDelay 는 CSS 로 못 지운다.
    document.querySelectorAll('.reveal').forEach(function (el) {
      el.classList.remove('reveal');
      el.style.transitionDelay = '';
      el.style.opacity = '';
      el.style.transform = '';
    });
  });
})();
