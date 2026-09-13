#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""모션 3차 — 데이터 블록은 카드별로 발화시킨다 + 로고 회전.

문제
  게이지와 카운트업은 돌고 있었다(실측: clip 100%→0, 숫자 21→59→83→84).
  그런데 발화 단위가 "섹션"이라, 섹션 윗변이 화면에 닿는 순간 그 안의
  카드 6장이 한꺼번에 시작한다. 아랫줄 3장은 사용자가 거기 도달하기 전에
  이미 끝나 있다. 움직임은 있는데 아무도 못 보는 상태였다.

왜 처음에 섹션 단위였나
  .section 에 content-visibility:auto 가 걸려 있어서, 화면 밖 섹션 안쪽
  요소는 rect 가 전부 0 으로 나온다. 카드 rect 로 판정하면 발화하지 않는다.

해법 — 두 단계로 나눈다
  1단계 섹션: 지금처럼 섹션 rect 로 판정해 .mo-in 을 건다(렌더링 개시).
  2단계 카드: 섹션이 켜진 뒤에는 그 안의 rect 가 진짜 값이다. 그때부터
            카드 자신의 위치로 판정해 .mo-v 를 건다.
  즉 "보이게 된 다음에만 카드 위치를 믿는다". content-visibility 와
  싸우지 않고 순서로 푼다.

로고
  360도 회전. 계속 돌리면 눈에 거슬리고 배터리도 먹으므로 호버에서만 한 바퀴.
  로고는 CSS content:url 로 들어간 이미지라 img 에 직접 transform 을 건다.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, 'css', 'global.css')
s = io.open(C, encoding='utf-8').read()

# ── 막대·점 선택자를 섹션 기준(.mo-in)에서 카드 기준(.mo-v)으로 ──
SWAP = [
("""html.mo .mo-i .ev-bar,
html.mo .mo-i .dx-track i{clip-path:inset(0 100% 0 0)}
html.mo [data-mo].mo-in .mo-i .ev-bar,
html.mo [data-mo].mo-in .mo-i .dx-track i{clip-path:inset(0 0 0 0);
  transition:clip-path .92s cubic-bezier(.22,1,.36,1) calc(var(--mo-d,0ms) + 140ms)}""",
"""/* 카드 자신이 화면에 들어온 뒤에 자란다(.mo-v). 섹션 기준으로 걸면
   아랫줄 카드가 보이기 전에 다 끝나 있다. ciclo-effects.js 주석 참고. */
html.mo .ev-bar,
html.mo .dx-track i{clip-path:inset(0 100% 0 0)}
html.mo .mo-v .ev-bar,
html.mo .mo-v .dx-track i{clip-path:inset(0 0 0 0);
  transition:clip-path .9s cubic-bezier(.22,1,.36,1) var(--bd,0ms)}"""),

("""html.mo .mo-i .ev-dot{transform:scale(0)}
html.mo [data-mo].mo-in .mo-i .ev-dot{transform:scale(1);
  transition:transform .46s cubic-bezier(.34,1.42,.5,1)}""",
"""html.mo .ev-dot{transform:scale(0)}
html.mo .mo-v .ev-dot{transform:scale(1);
  transition:transform .46s cubic-bezier(.34,1.42,.5,1)}"""),
]
for a, b in SWAP:
    if a not in s: sys.exit('FAIL: 선택자를 찾지 못함\n' + a[:80])
    s = s.replace(a, b, 1)

# nth-of-type 점 지연도 .mo-v 기준으로
s = s.replace('html.mo [data-mo].mo-in .mo-i .ev-dot:nth-of-type',
              'html.mo .mo-v .ev-dot:nth-of-type')

# .mo-now(첫 화면 즉시 표시) 예외에 .mo-v 계열도 추가
s = s.replace("""html.mo [data-mo].mo-now .mo-i,
html.mo [data-mo].mo-now .mo-i .ev-bar,
html.mo [data-mo].mo-now .mo-i .dx-track i,
html.mo [data-mo].mo-now .mo-i .ev-dot{transition:none!important}""",
"""html.mo [data-mo].mo-now .mo-i,
html.mo [data-mo].mo-now .mo-v .ev-bar,
html.mo [data-mo].mo-now .mo-v .dx-track i,
html.mo [data-mo].mo-now .mo-v .ev-dot{transition:none!important}""")

LOGO = u'''

/* ── 로고 회전 ──
   계속 돌리면 눈에 거슬리고 배터리도 먹는다. 호버에서 한 바퀴만 돈다.
   로고는 CSS content:url 로 들어간 이미지라 img 자체에 transform 을 건다. */
.nav-logo img,.sidebar-brand img,.footer-brand img{
  transition:transform .9s cubic-bezier(.22,1,.36,1)}
.nav-logo:hover img,.sidebar-brand:hover img,.footer-brand:hover img{
  transform:rotate(360deg)}
@media(prefers-reduced-motion:reduce){
  .nav-logo img,.sidebar-brand img,.footer-brand img{transition:none}
  .nav-logo:hover img,.sidebar-brand:hover img,.footer-brand:hover img{transform:none}
}
'''
s = s.rstrip('\n') + '\n' + LOGO
io.open(C, 'w', encoding='utf-8').write(s)
print('CSS — 막대·점을 카드 기준으로 전환, 로고 회전 추가')
