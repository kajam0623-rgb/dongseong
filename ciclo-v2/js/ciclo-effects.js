/* CICLO 사이트 효과 v2 — WPCode > JavaScript Snippet > Site Wide Footer
 *
 * v1 대비 변경 (238LAB 이식 플랜 D — 모션은 "빼기"가 방향):
 *   - 스크롤 등장 애니메이션(.reveal 주입 + IntersectionObserver) 전부 삭제
 *   - 히어로 패럴럭스(스크롤 시 h1 translateY/opacity) 삭제
 *   - 사이드바 토글만 남김
 *
 * 삭제 근거
 *   238LAB은 스크롤 리빌이 0개다. 의도적으로 거의 움직이지 않는다.
 *   씨클로 v1은 .overline/.sec-h2/.card/.step/.fit/.svc-row/.faq-row/.mean/
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
 */
(function(){
  function ready(fn){
    if (document.readyState !== 'loading') { fn(); }
    else { document.addEventListener('DOMContentLoaded', fn); }
  }

  ready(function(){
    // ── 사이드바 토글 ────────────────────────────────────────
    var burger   = document.querySelector('.nav-burger'),
        closeBtn = document.querySelector('.sidebar-close'),
        side     = document.querySelector('.sidebar'),
        scrim    = document.querySelector('.scrim');

    function openSide(){
      side  && side.classList.add('open');
      scrim && scrim.classList.add('open');
      closeBtn && closeBtn.focus();
    }
    function shutSide(){
      side  && side.classList.remove('open');
      scrim && scrim.classList.remove('open');
      burger && burger.focus();
    }

    burger   && burger.addEventListener('click', openSide);
    closeBtn && closeBtn.addEventListener('click', shutSide);
    scrim    && scrim.addEventListener('click', shutSide);
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape') shutSide();
    });

    // ── 구버전 잔재 정리 ─────────────────────────────────────
    // 이전 스니펫이 캐시에 남아 .reveal 을 붙였을 경우를 대비한 안전장치.
    // global.css v2 가 .reveal 을 무해화하지만, 인라인 transitionDelay 는
    // CSS 로 못 지우므로 여기서 털어낸다.
    document.querySelectorAll('.reveal').forEach(function(el){
      el.classList.remove('reveal');
      el.style.transitionDelay = '';
      el.style.opacity = '';
      el.style.transform = '';
    });
  });
})();
