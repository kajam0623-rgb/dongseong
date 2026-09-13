/* CICLO 사이트 효과 — WPCode > JavaScript Snippet > Site Wide Footer */
(function(){
  function ready(fn){ if(document.readyState!=='loading'){fn();} else {document.addEventListener('DOMContentLoaded',fn);} }
  ready(function(){
    // 사이드바 토글
    var burger=document.querySelector('.nav-burger'),
        closeBtn=document.querySelector('.sidebar-close'),
        side=document.querySelector('.sidebar'),
        scrim=document.querySelector('.scrim');
    function openSide(){ side&&side.classList.add('open'); scrim&&scrim.classList.add('open'); }
    function shutSide(){ side&&side.classList.remove('open'); scrim&&scrim.classList.remove('open'); }
    burger&&burger.addEventListener('click',openSide);
    closeBtn&&closeBtn.addEventListener('click',shutSide);
    scrim&&scrim.addEventListener('click',shutSide);
    document.addEventListener('keydown',function(e){ if(e.key==='Escape') shutSide(); });

    // 스크롤 등장 애니메이션
    if('IntersectionObserver' in window){
      var io=new IntersectionObserver(function(entries){
        entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
      },{threshold:0.12,rootMargin:'0px 0px -8% 0px'});
      var sel='.overline, .sec-h2, .card, .step, .fit, .svc-row, .faq-row, .mean, .channel, .work-grid > *';
      document.querySelectorAll(sel).forEach(function(el,i){
        if(el.closest('.sidebar')||el.closest('.ciclo-header')) return;
        el.classList.add('reveal');
        var p=el.parentElement, idx=p?Array.prototype.indexOf.call(p.children,el):0;
        el.style.transitionDelay=(Math.min(idx,6)*70)+'ms';
        io.observe(el);
      });
    }

    // 히어로 패럴럭스
    var title=document.querySelector('.hero .elementor-heading-title, .hero h1');
    if(title){ window.addEventListener('scroll',function(){
      var y=window.scrollY;
      title.style.transform='translateY('+Math.min(y*0.22,220)+'px)';
      title.style.opacity=String(Math.max(0,1-y/620));
    },{passive:true}); }
  });
})();