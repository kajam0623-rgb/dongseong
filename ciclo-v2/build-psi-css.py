#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PSI 실제 캡처용 CSS 추가 (.psi-shots / .psi-shot).

캡처 파일이 도착하면 build-psi-shots.py 가 마크업만 바꾸면 되도록
스타일을 먼저 넣어 둔다. 사용 전에는 아무 데도 적용되지 않는다.
"""
import sys, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'global.css')
s = io.open(P, encoding='utf-8').read()

ANCHOR = '@media(max-width:620px){.res-cards{grid-template-columns:1fr}.psi-vitals{grid-template-columns:repeat(3,1fr);gap:12px 8px}}\n'

CSS = """/* PSI 실제 캡처 — 재현 표(.psi-cards) 대신 도구 화면을 그대로 싣는 경우.
   캡처는 흰 배경이라 크림 지면 위에서 뜨므로 얇은 테두리로 눌러 준다.
   img 에 width/height 를 박고 여기서 height:auto 로 풀어 비율만 유지한다(CLS 0). */
.psi-shots{margin-top:clamp(18px,2.2vw,26px);display:grid;grid-template-columns:1fr 1fr;
  gap:clamp(18px,2.4vw,30px)}
.psi-shot{margin:0}
.psi-shot img{display:block;width:100%;height:auto;background:#fff;
  border:1px solid rgba(18,18,18,.14);border-radius:6px}
.psi-shot figcaption{margin-top:12px;font-size:13px;line-height:1.65;color:rgba(18,18,18,.55);
  font-variant-numeric:tabular-nums}
.psi-shot figcaption b{font-weight:700;color:rgba(18,18,18,.8)}
@media(max-width:860px){.psi-shots{grid-template-columns:1fr}}
"""

if s.count(ANCHOR) != 1:
    sys.exit('FAIL: 앵커를 찾지 못함')
io.open(P, 'w', encoding='utf-8').write(s.replace(ANCHOR, ANCHOR + CSS))
print('ok  css/global.css  (+%d B)' % len(CSS.encode('utf-8')))
