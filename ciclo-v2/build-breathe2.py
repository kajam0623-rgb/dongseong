#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""여백 확장 2차 — 1차에서 빠진 블록들.

1차(build-breathe.py) 뒤 재측정에서 `.dx` 진단 카드가 24/22 그대로였다.
홈에서 여섯 장 깔리는 주요 블록인데 빠뜨렸다. 같이 놓친 것들도 함께 잡는다:

  .dx        24/22, 내부 gap 16
  .faq-a     문단 사이 gap 12 — 답변이 4~5문단이라 가장 빽빽하게 읽히는 자리
  .res-note  18/20
  .ev-check  20/22
  .step      padding-top 18
  .corp>div  12
  .work-feature .wf-copy  내부 gap 22
"""
import sys, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'global.css')
s = io.open(P, encoding='utf-8').read()

def rep(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('FAIL: %d회 — %r' % (s.count(old), old[:78]))
    s = s.replace(old, new)

rep('  padding:24px 22px;display:flex;flex-direction:column;gap:16px}',
    '  padding:clamp(26px,2.3vw,32px) clamp(24px,2.1vw,28px);\n'
    '  display:flex;flex-direction:column;gap:clamp(16px,1.6vw,20px)}')

# FAQ 답변 문단 간격 — 한 답변이 4~5문단이라 여기가 제일 빽빽하다
rep('.faq-a{display:flex;flex-direction:column;gap:12px}',
    '.faq-a{display:flex;flex-direction:column;gap:clamp(14px,1.4vw,18px)}')

rep('.res-note{margin-top:clamp(20px,2.4vw,28px);max-width:64ch;padding:18px 20px;',
    '.res-note{margin-top:clamp(22px,2.6vw,32px);max-width:64ch;\n'
    '  padding:clamp(22px,2vw,26px) clamp(22px,2vw,26px);')

rep('.ev-check{margin-top:clamp(26px,3vw,36px);padding:20px 22px;',
    '.ev-check{margin-top:clamp(26px,3vw,36px);padding:clamp(22px,2.2vw,28px) clamp(22px,2.2vw,26px);')

rep('.step{border-top:2px solid var(--pt);padding-top:18px}',
    '.step{border-top:2px solid var(--pt);padding-top:clamp(20px,1.9vw,26px)}')

rep('.corp>div{display:flex;justify-content:space-between;gap:16px;padding:12px 0;',
    '.corp>div{display:flex;justify-content:space-between;gap:16px;padding:clamp(14px,1.3vw,18px) 0;')

rep('.work-feature .wf-copy{padding:clamp(30px,3.6vw,52px);display:flex;flex-direction:column;gap:22px}',
    '.work-feature .wf-copy{padding:clamp(32px,3.8vw,56px);display:flex;flex-direction:column;\n'
    '  gap:clamp(22px,2.2vw,28px)}')

io.open(P, 'w', encoding='utf-8').write(s)
print('ok  css/global.css')
