#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/dental — 중복 카카오 플로팅 버튼 제거.

헤더 스니펫이 사이트 전역에 `.kakao-float` 를 이미 띄운다(global.css:135).
이 페이지는 자기만의 `.kko-fab` 를 하나 더 붙여서, 모바일 우하단에 같은
카카오 버튼이 두 개 겹쳐 뜬다(390px 실측 확인). 같은 오픈채팅 링크다.

페이지 로컬 쪽을 지운다 — 전역 버튼은 모든 페이지에서 위치·크기가 일관되고
global.css 의 반응형 규칙(:706, :712)을 이미 받는다.
"""
import sys, io, os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages', '치과_홈페이지_제작.html')
s = io.open(P, encoding='utf-8').read()
before = len(s.encode('utf-8'))

def rep(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('FAIL: %d회 — %r' % (s.count(old), old[:80]))
    s = s.replace(old, new)

# 마크업
rep('''<a class="kko-fab" href="https://open.kakao.com/o/s8oziiEi" target="_blank" rel="noopener" aria-label="카카오톡 문의">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#3C1E1E" d="M12 3C6.9 3 2.8 6.2 2.8 10.2c0 2.5 1.7 4.7 4.2 6L6.2 20c-.1.3.2.5.5.4l4.1-2.4c.4 0 .8.1 1.2.1 5.1 0 9.2-3.2 9.2-7.2S17.1 3 12 3z"/></svg>
  <span>카톡 문의</span>
</a>
''',
'''<!-- 페이지 전용 카카오 버튼 제거 — 헤더 스니펫의 .kakao-float 와 겹쳐서
     모바일 우하단에 같은 버튼이 두 개 떴다. 전역 버튼 하나만 남긴다. -->
''')

# 스타일
rep('''#ciclo-dental .kko-fab{position:fixed;right:20px;bottom:20px;z-index:9999;display:flex;align-items:center;gap:8px;
  padding:13px 20px;border-radius:999px;background:#FEE500;color:#191600;text-decoration:none;
  font:700 15px/1 'Pretendard',sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.28);transition:transform .18s ease}
#ciclo-dental .kko-fab:hover{transform:translateY(-2px)}
#ciclo-dental .kko-fab svg{width:20px;height:20px;flex:none}
@media(max-width:640px){#ciclo-dental .kko-fab{right:14px;bottom:14px;padding:12px 16px;font-size:14px}}
''', '')

io.open(P, 'w', encoding='utf-8').write(s)
after = len(s.encode('utf-8'))
print('ok  pages/치과_홈페이지_제작.html  %d → %d B (%+d)' % (before, after, after - before))
