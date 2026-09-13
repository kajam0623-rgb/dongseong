#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""폰트를 Pretendard 하나로 통일 — Archivo 제거.

CSS 46곳 + 마크업 인라인 1곳 + 헤드 스니펫의 구글 폰트 로딩까지 걷어낸다.

성능에서 얻는 것 (이쪽이 꽤 크다)
  · 렌더 차단 스타일시트 1장 제거 (fonts.googleapis.com/css2?family=Archivo)
  · 서드파티 오리진 2개 제거 (fonts.googleapis.com · fonts.gstatic.com)
    → preconnect 2줄도 같이 사라진다. DNS+TLS 왕복 두 번이 빠진다
  · Archivo woff2 3벌(700/800/900) 다운로드 없음
  요청 수와 서드파티 의존이 함께 줄어 PSI 에 직접 붙는다.

타이포에서 조심할 것
  Archivo 는 폭이 좁은 그로테스크라 대문자를 크게 써도 한 줄에 들어갔다.
  Pretendard 는 라틴 글자가 더 넓다. 같은 font-size 로 두면
    · 히어로 워드마크 CICLO 가 넘칠 수 있다
    · 자간(-.03em)은 Archivo 기준이라 Pretendard 에서는 과하게 조인다
  그래서 이 스크립트는 치환만 하고, 넘침 여부는 뒤에서 실측해 조정한다.
"""
import sys, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PRE = "'Pretendard Variable',Pretendard,-apple-system,sans-serif"

# ── CSS ────────────────────────────────────────────────────────
p = os.path.join(HERE, 'css', 'global.css')
s = io.open(p, encoding='utf-8').read()
before = s.count('Archivo')

# 폴백까지 통째로 교체 (Arial Black / Arial Narrow 도 Archivo 전제였다)
s = re.sub(r"font-family:Archivo,'Arial Black','Helvetica Neue',sans-serif", 'font-family:' + PRE, s)
s = re.sub(r"font-family:Archivo,'Arial Black',sans-serif", 'font-family:' + PRE, s)
s = re.sub(r"font-family:Archivo,'Arial Narrow',sans-serif", 'font-family:' + PRE, s)
s = re.sub(r"font-family:Archivo,sans-serif", 'font-family:' + PRE, s)

left = s.count('Archivo')
if left:
    sys.exit('FAIL: CSS 에 Archivo %d곳 남음' % left)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok  css/global.css        Archivo %d곳 → Pretendard' % before)

# ── 마크업 (히어로 스크롤 배지 SVG 안의 인라인) ──────────────────
p = os.path.join(HERE, 'pages', 'Home.html')
s = io.open(p, encoding='utf-8').read()
n = s.count('font-family:Archivo,sans-serif')
if n != 1:
    sys.exit('FAIL: Home.html 인라인 %d곳 (1곳이어야 함)' % n)
s = s.replace('font-family:Archivo,sans-serif',
              "font-family:'Pretendard Variable',Pretendard,sans-serif")
io.open(p, 'w', encoding='utf-8').write(s)
print('ok  pages/Home.html       인라인 1곳 → Pretendard')

# ── 헤드 스니펫 — 구글 폰트 로딩 전체 제거 ──────────────────────
p = os.path.join(HERE, 'wpcode-head.html')
s = io.open(p, encoding='utf-8').read()

def drop(pat, label):
    global s
    new, k = re.subn(pat, '', s)
    if not k:
        sys.exit('FAIL: 헤드에서 %s 를 찾지 못함' % label)
    s = new
    print('ok  wpcode-head.html    %s 제거 (%d줄)' % (label, k))

drop(r'[ \t]*<link rel="preconnect" href="https://fonts\.googleapis\.com">\n', 'googleapis preconnect')
drop(r'[ \t]*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n', 'gstatic preconnect')
drop(r'[ \t]*<link rel="stylesheet"[^>]*fonts\.googleapis\.com/css2\?family=Archivo[^>]*>\n', 'Archivo 스타일시트')

s = s.replace(
    '     Archivo 웨이트 변경: 500;700;800;900 → 700;800;900',
    '     Archivo 는 걷어냈다 — 사이트 전체를 Pretendard 하나로 통일했다.\n'
    '     구글 폰트 오리진 2개(googleapis·gstatic)와 렌더 차단 스타일시트 1장,\n'
    '     woff2 3벌이 함께 사라진다.')
s = re.sub(r'\n{3,}', '\n\n', s)
io.open(p, 'w', encoding='utf-8').write(s)

print()
print('남은 Archivo 참조:',
      sum(io.open(os.path.join(HERE, f), encoding='utf-8').read().count('Archivo')
          for f in ('css/global.css', 'wpcode-head.html', 'pages/Home.html')))
