/* CICLO 사이트 효과 v2 — WPCode > JavaScript Snippet > Site Wide Footer
 *
 * v1 대비 변경 (238LAB 이식 플랜 D — 모션은 "빼기"가 방향):
 *   - 스크롤 등장 애니메이션(.reveal 주입 + IntersectionObserver) 삭제
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
