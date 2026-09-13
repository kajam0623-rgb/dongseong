#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""검토에서 나온 나머지 3건.

1. `.dx-geo b` 대비 4.26:1 (기준 4.5)
   진단 카드에서 "AI 답변" 값을 "검색" 값보다 흐리게 둔 건 의도지만
   흐림이 조금 과했다. 흰 카드 위 네이비 α=.62 부터 통과(4.53)한다.
   위계는 유지되고(검색 값은 불투명 네이비 14.73:1) 기준만 넘긴다.

2. `/dental` 브랜드마크 태그라인이 "CREATIVE CLICKS" 로 남아 있다
   히어로를 CICLO + GEO 로 바꾸면서 죽은 문구다. 헤더 사이드바·푸터가 쓰는
   브랜드 태그라인("CREATIVE IDEAS · CLICK LOGIC")으로 통일한다 —
   About 의 /THE NAME 이 이 약자를 설명하고 있어서 사이트 전체가 맞물린다.

3. Contact 카카오 링크에 rel="noopener" 가 없다
   target="_blank" 만 있으면 새 창이 `window.opener` 로 원본 페이지를
   조작할 수 있다(리버스 탭내빙). 사이트 전체에서 이 한 곳만 빠져 있었다.
"""
import sys, io, os

HERE = os.path.dirname(os.path.abspath(__file__))

def rep(path, old, new):
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    if s.count(old) != 1:
        sys.exit('FAIL %s: %d회 — %r' % (path, s.count(old), old[:70]))
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
    print('ok  %s' % path)

rep('css/global.css',
    '.dx-geo b{color:rgba(17,30,108,.6)}',
    '.dx-geo b{color:rgba(17,30,108,.62)}  /* .6 은 흰 카드 위 4.26:1 로 AA 미달 */')

rep('pages/치과_홈페이지_제작.html',
    '<div class="bt">CREATIVE CLICKS</div>',
    '<div class="bt">CREATIVE IDEAS · CLICK LOGIC</div>')

rep('pages/Contact.html',
    'href="https://open.kakao.com/o/s8oziiEi" target="_blank"><div><div class="lab">KAKAO</div>',
    'href="https://open.kakao.com/o/s8oziiEi" target="_blank" rel="noopener"><div><div class="lab">KAKAO</div>')
