#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/dental — 상단 브랜드 줄이 사이트 네비 알약과 겹친다.

이 랜딩은 원래 단독 페이지로 만들어져서 자기 브랜드 줄(`.top .id` = 마크 + CICLO +
"치과 전문")을 갖고 있다. 사이트 안으로 들어오면 헤더 스니펫의 고정 네비 알약이
같은 자리에 떠서 로고 글자를 덮는다(390px 실측 확인).

브랜드 줄을 감추고, h1 이 고정 네비 아래에서 시작하도록 상단 여백을 준다.
h1·부제·특별가 줄은 그대로 둔다.
"""
import sys, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages', '치과_홈페이지_제작.html')
s = io.open(P, encoding='utf-8').read()

old = '  .top{padding:clamp(22px,3vw,32px) var(--P) clamp(24px,3.4vw,36px);border-bottom:1px solid var(--line);}'
new = ('''  /* 사이트 고정 네비(헤더 스니펫)와 겹치지 않게 위쪽을 비운다.
     단독 페이지 시절의 자기 브랜드 줄은 네비와 중복이라 감춘다. */
  .top{padding:clamp(96px,12vw,132px) var(--P) clamp(24px,3.4vw,36px);border-bottom:1px solid var(--line);}
  #ciclo-dental .top .id{display:none;}''')

if s.count(old) != 1:
    sys.exit('FAIL: %d회' % s.count(old))
io.open(P, 'w', encoding='utf-8').write(s.replace(old, new))
print('ok  pages/치과_홈페이지_제작.html')
