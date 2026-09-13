#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""실적 밴드 다듬기 — PSI 점수 라벨 정렬.

"검색 엔진 최적화" 만 2~3줄로 흘러 링 4개의 아래 라벨 밑선이 어긋났다.
라벨을 PSI 한국어 UI 표기(`검색엔진 최적화`)로 맞추고 개행 위치를 고정한 뒤,
small 에 2줄 최소 높이를 줘서 4개 라벨의 블록 높이를 맞춘다.
"""
import sys, io, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))

def patch(path, pairs, expect=None):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        n = s.count(old)
        if expect is not None and n != expect:
            sys.exit('FAIL %s: 앵커 %d회 (기대 %d) — %r' % (path, n, expect, old[:60]))
        if expect is None and n != 1:
            sys.exit('FAIL %s: 앵커 %d회 — %r' % (path, n, old[:60]))
        s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('ok  %s' % os.path.relpath(path, HERE))

patch(os.path.join(HERE, 'css/global.css'), [
    ('.psi-s small{display:block;margin-top:8px;font-size:11.5px;line-height:1.35;color:rgba(18,18,18,.55)}',
     '.psi-s small{display:block;margin-top:8px;min-height:calc(1.35em*2);font-size:11.5px;line-height:1.35;\n'
     '  color:rgba(18,18,18,.55)}'),
])

for name in ('Home', 'Work'):
    p = os.path.join(HERE, 'pages/%s.html' % name)
    patch(p, [('<small>검색<br>엔진 최적화</small>', '<small>검색엔진<br>최적화</small>')], expect=2)
