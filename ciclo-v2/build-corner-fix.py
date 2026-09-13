#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""히어로 우하단 코너 라벨 제거 — 고정 카톡 버튼과 구조적으로 자리가 겹친다.

`.corner.r`("/CREATIVE CLICKS")은 히어로 기준 우하단 절대배치,
`.kakao-float`는 뷰포트 기준 우하단 고정배치다. 히어로 높이(min-height:100vh
+ 패딩)가 뷰포트보다 크면 둘의 하단 기준선이 어긋나 결국 겹친다.
bottom 값을 56 → 96px 로 올려 봐도 1440×844 에서 86×20px 로 다시 겹쳤다
(히어로 900px > 뷰포트 844px). 값으로 피할 수 있는 충돌이 아니다.

그래서 라벨을 뺀다. 잃는 정보가 없다 — 같은 문구가 히어로 h1("CREATIVE
CLICKS."), 바로 아래 마퀴, 푸터 태그라인에 이미 세 번 더 있다.
좌하단 ©2026 은 버튼과 반대편이라 그대로 둔다.
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

rep('pages/Home.html',
    '  <div class="corner r">/CREATIVE CLICKS</div>\n', '')

rep('css/global.css',
    '.hero .corner.r{right:clamp(16px,6vw,120px);bottom:96px;font-family:Archivo,sans-serif;font-weight:700;font-size:12px;letter-spacing:.14em;opacity:.55}\n',
    '/* .hero .corner.r 제거 — 뷰포트 고정 카톡 버튼과 자리가 구조적으로 겹친다.\n'
    '   같은 문구가 h1·마퀴·푸터 태그라인에 이미 있다. */\n')

rep('css/global.css',
    '  .scroll-badge,.hero .corner.r{display:none}',
    '  .scroll-badge{display:none}')
