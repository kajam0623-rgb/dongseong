#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""클릭되는 전체 사이트 미리보기 — 아티팩트용 다중 파일 번들.

왜 필요한가
  마크업의 링크는 전부 `/work/` 같은 절대 경로다. 워드프레스에서는 맞지만
  아티팩트 호스팅에서는 루트 경로를 서빙하지 않아서 아무 데도 안 간다.
  그래서 내부 링크를 전부 상대 경로 파일명으로 바꾼 번들을 따로 만든다.
  원본 pages/*.html 은 건드리지 않는다 — 미리보기 전용 변환이다.

폰트
  실제 사이트는 Pretendard 를 jsDelivr 에서 받는다. 아티팩트는 보안 정책상
  fonts.googleapis.com 외의 스타일시트를 막으므로 그 링크를 쓸 수 없다.
  1) 보는 기기에 Pretendard 가 깔려 있으면 실제 그대로 보이고
  2) 없으면 Noto Sans KR(구글 폰트) 로 떨어진다.
  레이아웃·모션은 실제와 같고 글자 모양만 2)에서 다르다.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = '/tmp/claude-0/-home-user-dongseong/cb1a62a7-c398-507e-91e0-95f1e9d92661/scratchpad/preview'

def rd(p): return io.open(os.path.join(HERE,p), encoding='utf-8').read()

# 소스 → 발행 파일명. Home 은 아티팩트 본문이라 index.html 이다.
PAGES = [
    ('Home',              'index.html'),
    ('Work',              'work.html'),
    ('About',             'about.html'),
    ('Contact',           'contact.html'),
    ('GEO',               'geo.html'),
    ('Website_Design',    'website-design.html'),
    ('Blog_Content',      'blog-content.html'),
    ('Digital_Marketing', 'digital-marketing.html'),
    ('치과_홈페이지_제작',   'dental.html'),
    ('칼럼',               'column.html'),
]
# 워드프레스 경로 → 발행 파일명
LINKS = [
    ('/website-design/',     'website-design.html'),
    ('/digital-marketing/',  'digital-marketing.html'),
    ('/blog-content/',       'blog-content.html'),
    ('/contact/',            'contact.html'),
    ('/column/',             'column.html'),
    ('/dental/',             'dental.html'),
    ('/about/',              'about.html'),
    ('/work/',               'work.html'),
    ('/geo/',                'geo.html'),
]
# 카테고리 페이지는 워드프레스가 만든다(테마 category.php). 미리보기에는 없으므로
# 칼럼 목록으로 보낸다 — 죽은 링크를 남기는 것보다 낫다.
CATS = 'seo geo hospital content ads case insight'.split()

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
        '?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap">')

css    = rd('css/global.css').replace(
    "'Pretendard Variable',Pretendard,-apple-system,sans-serif",
    "'Pretendard Variable',Pretendard,'Noto Sans KR',-apple-system,sans-serif")
js     = rd('js/ciclo-effects.js')
header = rd('pages/CICLO_Header.html')
footer = rd('pages/CICLO_Footer.html')

def relink(s):
    """내부 절대 경로를 발행 파일명으로. 외부 링크(https://)는 건드리지 않는다."""
    for a, b in LINKS:
        s = s.replace('href="%s"' % a, 'href="%s"' % b)
        if a.endswith('/') and a != '/#':
            s = s.replace('href="%s#' % a, 'href="%s#' % b)   # /work/#anchor
    for c in CATS:
        s = s.replace('href="/category/%s/"' % c, 'href="column.html"')
    s = re.sub(r'href="/#', 'href="index.html#', s)   # /#services 같은 홈 앵커
    s = re.sub(r'href="/"', 'href="index.html"', s)
    return s

def strip_images(s):
    # 미리보기에서는 워드프레스 업로드 경로를 비운다(아티팩트에 그 파일이 없다)
    return s.replace('/wp-content/uploads/ciclo/', '')

os.path.isdir(OUT) or os.makedirs(OUT)
hdr, ftr = relink(header), relink(footer)

BODY = u"""<main class="site-main">
%(header)s
<div class="page-content"><div class="ciclo-page" id="ciclo-home"><div id="content">
%(page)s
</div></div></div>
%(footer)s
</main>
<script>
%(js)s
</script>"""

FULL = u"""<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>%(title)s</title>
%(font)s
<style>
%(css)s
</style>
</head><body>
%(body)s
</body></html>
"""

made = []
for name, fname in PAGES:
    page = relink(strip_images(rd('pages/%s.html' % name)))
    body = BODY % dict(header=hdr, page=page, footer=ftr, js=js)
    if fname == 'index.html':
        # 아티팩트 본문 — 껍데기는 호스팅이 씌우므로 알맹이만
        doc = ('<title>CICLO</title>\n' + FONT + '\n<style>\n' + css + '\n</style>\n' + body)
        # 본문은 처음 발행한 경로에 그대로 쓴다 — 같은 아티팩트로 갱신되게
        dst = os.path.join(os.path.dirname(OUT), 'ciclo-home.html')
    else:
        doc = FULL % dict(title='CICLO — ' + name, font=FONT, css=css, body=body)
        dst = os.path.join(OUT, fname)
    io.open(dst,'w',encoding='utf-8').write(doc)
    made.append((fname, len(doc.encode('utf-8'))))

# 내부 절대 경로가 남았는지 확인
bad = 0
for fname, _ in made:
    p = (os.path.join(os.path.dirname(OUT),'ciclo-home.html') if fname=='index.html'
         else os.path.join(OUT, fname))
    left = re.findall(r'href="/(?!/)[^"]*"', io.open(p,encoding='utf-8').read())
    if left:
        bad += 1; print('★ %s 에 절대경로 남음: %s' % (fname, set(left)))

for f,n in made: print('  %-24s %7d B' % (f,n))
print('\n%d개 페이지 · 절대경로 잔존 %d건' % (len(made), bad))
sys.exit(1 if bad else 0)
