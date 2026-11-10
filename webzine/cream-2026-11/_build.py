#!/usr/bin/env python3
"""cream 웹진: 10개 원본 페이지를 이어 붙여 한 장짜리 index.html 을 만든다.

원본(편집 대상): cover.html, trend.html, ... support.html, css/pages/*.css
결과물(직접 고치지 말 것): index.html, css/all-pages.css

  python3 -I _build.py
"""
import re, os
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ['cover', 'trend', 'lineup', 'sales-tv', 'sales-addressable', 'sales-medianet',
         'sales-radio', 'digital', 'table', 'support']
CSS_OF = {'cover': 'index'}  # cover.html 은 css/pages/index.css 를 쓴다

def read(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()

# ---------- CSS 범위 지정: 모든 선택자 앞에 .pg-이름 을 붙인다 ----------
def scope_selectors(sel, scope):
    out = []
    for part in sel.split(','):
        p = part.strip()
        if not p: continue
        p2 = re.sub(r'^(html|body|:root)\b', scope, p)
        out.append(p2 if p2 != p else f'{scope} {p}')
    return ','.join(out)

def scope_css(css, scope):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    res, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: res.append(css[i:]); break
        head = css[i:j].strip()
        # 짝 맞는 } 찾기
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if head.startswith(('@media', '@supports', '@container')):
            res.append(f'{head}{{{scope_css(body, scope)}}}')
        elif head.startswith('@'):
            res.append(f'{head}{{{body}}}')
        else:
            res.append(f'{scope_selectors(head, scope)}{{{body}}}')
        i = k
    return '\n'.join(res)

css_out = ['/* 자동 생성 — _build.py. 직접 고치지 말고 css/pages/*.css 를 고친다 */']
body_out, scripts = [], []
for name in PAGES:
    html = read(f'{name}.html')
    sec = re.search(r'<body[^>]*data-section="([^"]*)"', html).group(1)
    m = re.search(r'<main([^>]*)>(.*)</main>', html, re.S)
    attrs, inner = m.group(1), m.group(2)
    cls = re.search(r'class="([^"]*)"', attrs)
    inner = re.sub(r'\s*<nav class="pager".*?</nav>', '', inner, flags=re.S)
    inner_wrapped = f'<div class="{cls.group(1)}">{inner}</div>' if cls else inner
    body_out.append(f'<div class="pg pg-{name}" data-section="{sec}">\n{inner_wrapped}\n</div>')
    for s in re.findall(r'<script>(.*?)</script>', html, re.S):
        if "classList.add('js')" not in s: scripts.append(s.strip())
    cssfile = f'css/pages/{CSS_OF.get(name, name)}.css'
    if os.path.exists(os.path.join(ROOT, cssfile)):
        css_out.append(f'/* ===== {name} ===== */\n' + scope_css(read(cssfile), f'.pg-{name}'))
open(os.path.join(ROOT, 'css/all-pages.css'), 'w', encoding='utf-8').write('\n'.join(css_out) + '\n')

head = read('cover.html').split('<body')[0]
head = head.replace('css/pages/index.css', 'css/all-pages.css')
doc = (head + '<body data-section="" data-single>\n<main id="main">\n' + '\n\n'.join(body_out) +
       '\n</main>\n<script src="js/common.js"></script>\n' +
       ''.join(f'<script>{s}</script>\n' for s in scripts) + '</body>\n</html>\n')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(doc)
print('index.html', len(doc), 'bytes /', len(PAGES), 'pages')
