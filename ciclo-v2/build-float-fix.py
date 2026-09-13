#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""모바일 히어로 겹침 2건 수정 + 죽은 CSS 제거.

플레이라이트 겹침 검사 (절대·고정 배치 + 텍스트를 가진 요소 전수 대조):

  Home @390   .kakao-float "카톡 문의"  ×  .scroll-badge   31×52px
              .scroll-badge            ×  .corner.r       20×20px
  Home @360   같은 두 건이 46×52 · 34×20 으로 더 커짐
  Home @1440  겹침 0 · Work/About/Contact @390 겹침 0

원인 1 — 있지도 않은 버튼 자리를 비워 두고 있었다
  global.css 에 `.intro-float`(회사소개서 플로팅 버튼) 스타일이 살아 있고,
  그 위에 얹으려고 `.kakao-float{bottom:76px}` 로 카톡 버튼을 들어 올려 뒀다.
  그런데 **`.intro-float` 는 어느 페이지 마크업에도 없다**(전 페이지 grep 0건).
  벤치마크 문서 5-4번("모바일 플로팅 CTA 2개 중첩")을 고치면서 요소만 빼고
  CSS 를 남긴 잔재다. 그 76px 때문에 카톡 버튼이 스크롤 배지 높이로 올라와 있었다.

원인 2 — 배지와 코너 라벨이 좁은 화면에서 만난다
  `.scroll-badge` 는 108px 정원이 하단 중앙(x 141~249 @390),
  `.corner.r`("/CREATIVE CLICKS")은 우하단(x 217~367 @390). 20px 겹친다.

조치
  - 죽은 `.intro-float` 규칙 제거, `.kakao-float{bottom:76px}` 리프트 제거
    → 카톡 버튼이 기본 `bottom:20px` 로 내려온다
  - 560px 이하에서 `.scroll-badge` 와 `.corner.r` 을 감춘다
    둘 다 장식이고, 코너 라벨은 바로 아래 마퀴가 같은 문구를 반복한다.
    238LAB 도 모바일에서 챗 버튼 하나만 띄운다.
"""
import sys, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'global.css')
s = io.open(P, encoding='utf-8').read()
before = len(s.encode('utf-8'))

def rep(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('FAIL: %d회 — %r' % (s.count(old), old[:70]))
    s = s.replace(old, new)

rep('''/* intro float (회사소개서) — 카톡 버튼 아래 */
.kakao-float{bottom:76px}
.intro-float{position:fixed;right:20px;bottom:20px;z-index:90;display:flex;align-items:center;gap:8px;background:var(--pt);color:#fff;
  border-radius:999px;padding:14px 20px;font-size:14px;font-weight:800;box-shadow:0 10px 26px rgba(17,30,108,.32);transition:transform .18s cubic-bezier(.2,.8,.2,1),box-shadow .18s}
.intro-float:hover{color:#fff;background:var(--pt2);transform:translateY(-2px);box-shadow:0 16px 32px rgba(17,30,108,.4)}

/* 플로팅 버튼 크기 통일 */
.kakao-float,.intro-float{width:152px;justify-content:center;padding:14px 0}''',
'''/* 플로팅 버튼 — 카톡 하나만 띄운다.
   이전에는 .intro-float(회사소개서) 자리를 비우려고 .kakao-float{bottom:76px} 로
   들어 올려 뒀는데, .intro-float 요소는 어느 페이지에도 없다(전 페이지 grep 0건).
   그 76px 때문에 390px 에서 카톡 버튼이 스크롤 배지와 31×52px 겹쳤다.
   죽은 규칙과 리프트를 함께 걷어내고 기본 bottom:20px 로 되돌린다. */
.kakao-float{width:152px;justify-content:center;padding:14px 0}''')

rep('''@media(max-width:560px){.grid-4{grid-template-columns:1fr}}''',
'''@media(max-width:560px){
  .grid-4{grid-template-columns:1fr}
  /* 히어로 하단 장식 2종을 내린다 — 고정 카톡 버튼과 서로 부딪힌다.
     코너 라벨은 바로 아래 마퀴가 같은 문구를 반복하므로 잃는 정보가 없다. */
  .scroll-badge,.hero .corner.r{display:none}
}''')

io.open(P, 'w', encoding='utf-8').write(s)
print('ok  css/global.css  %d → %d B (%+d)' % (before, len(s.encode('utf-8')), len(s.encode('utf-8')) - before))
