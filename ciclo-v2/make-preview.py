#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""로컬 검증용 프리뷰 생성기.

워드프레스 출력 구조(page-content > .ciclo-page#ciclo-home > #content)를 그대로
재현해서, 라이브에 붙일 때와 같은 셀렉터 조건으로 측정할 수 있게 한다.

사용법: python3 make-preview.py Home Work GEO ...
출력:   <scratchpad>/pv-<name>.html
"""
import sys, io, os

SCRATCH = '/tmp/claude-0/-home-user-dongseong/cb1a62a7-c398-507e-91e0-95f1e9d92661/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))

def read(p):
    return io.open(os.path.join(HERE, p), encoding='utf-8').read()

head   = read('wpcode-head.html')
css    = read('css/global.css')
js     = read('js/ciclo-effects.js')
header = read('pages/CICLO_Header.html')
footer = read('pages/CICLO_Footer.html')

TPL = u"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>CICLO v2 — %(name)s</title>
%(head)s
<style>
%(css)s
</style>
</head><body class="ciclo-live">
<main class="site-main">
%(header)s
<div class="page-content"><div class="ciclo-page" id="ciclo-home"><div id="content">
%(page)s
</div></div></div>
%(footer)s
</main>
<script>
%(js)s
</script>
</body></html>
"""

names = sys.argv[1:] or ['Home']
for name in names:
    page = read('pages/%s.html' % name)
    out = TPL % dict(name=name, head=head, css=css, js=js,
                     header=header, footer=footer, page=page)
    dst = os.path.join(SCRATCH, 'pv-%s.html' % name)
    io.open(dst, 'w', encoding='utf-8').write(out)
    print('%-28s %7d B' % (dst, len(out.encode('utf-8'))))
