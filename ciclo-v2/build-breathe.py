#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""콘텐츠 내부 여백 확장 — "빽빽하다" 제보 반영.

섹션 사이 여백(160/160)은 238LAB 실측치와 같아서 건드리지 않는다.
빽빽한 것은 **섹션 안쪽**이었다. 실측:

  카드 패딩        .dx 24/22 · .res-card 22/22/20 · .psi-card 22/22/20
  그리드 간격      .dx-grid 14~20 · .res-cards 14~20 · .grid-4 16 고정
  수직 리듬        눈썹→h2 18 · h2→리드 18 · →캡션 12
  행간            리드 1.55 · 진단노트 1.62

한글은 글자에 속공간이 없어서 같은 수치라도 라틴 문자보다 더 빽빽하게 읽힌다.
238LAB 도 한글 본문을 1.70 으로 깐다(리드만 1.556). 카드 안 여백과 그리드
간격을 올리고, 눈썹·제목·리드·캡션 사이의 리듬을 넓힌다.
"""
import sys, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'global.css')
s = io.open(P, encoding='utf-8').read()

def rep(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('FAIL: %d회 — %r' % (s.count(old), old[:78]))
    s = s.replace(old, new)

# ── 1. 수직 리듬 — 눈썹 → h2 → 리드 → 링크 → 캡션 ────────────────
rep('margin-top:18px;word-break:keep-all}',
    'margin-top:clamp(18px,1.8vw,26px);word-break:keep-all}')
rep('.sec-lead{margin-top:18px;max-width:60ch;font-size:18px;line-height:1.55;',
    '.sec-lead{margin-top:clamp(18px,1.7vw,24px);max-width:60ch;font-size:18px;line-height:1.68;')
rep('.sec-link{display:inline-flex;align-items:center;gap:7px;margin-top:20px;',
    '.sec-link{display:inline-flex;align-items:center;gap:7px;margin-top:clamp(22px,2vw:28px);')
rep('.sec-caption{margin-top:12px;font-size:13px;line-height:1.6;',
    '.sec-caption{margin-top:clamp(16px,1.6vw,22px);font-size:13px;line-height:1.7;')

# ── 2. 카드 안쪽 여백 ────────────────────────────────────────────
rep('.card{background:var(--card);border:1px solid rgba(18,18,18,.1);border-radius:12px;padding:28px 26px;',
    '.card{background:var(--card);border:1px solid rgba(18,18,18,.1);border-radius:12px;\n'
    '  padding:clamp(26px,2.4vw,34px) clamp(24px,2.2vw,30px);')
rep('.proc-card{border:1px solid rgba(255,255,255,.16);border-radius:12px;padding:28px 24px;',
    '.proc-card{border:1px solid rgba(255,255,255,.16);border-radius:12px;\n'
    '  padding:clamp(28px,2.5vw,36px) clamp(24px,2.2vw,30px);')
rep('.mean{border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:32px 30px}',
    '.mean{border:1px solid rgba(255,255,255,.18);border-radius:12px;\n'
    '  padding:clamp(30px,2.8vw,40px) clamp(28px,2.4vw,34px)}')
rep('.res-card{background:var(--card);border-top:2px solid var(--pt);padding:22px 22px 20px;',
    '.res-card{background:var(--card);border-top:2px solid var(--pt);\n'
    '  padding:clamp(24px,2.2vw,30px) clamp(22px,2vw,28px) clamp(22px,2vw,26px);')
rep('.psi-card{background:var(--card);border-top:2px solid var(--pt);padding:22px 22px 20px}',
    '.psi-card{background:var(--card);border-top:2px solid var(--pt);\n'
    '  padding:clamp(24px,2.2vw,30px) clamp(22px,2vw,28px) clamp(22px,2vw,26px)}')

# ── 3. 그리드 간격 ──────────────────────────────────────────────
rep('.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,2vw,24px);margin-top:28px}',
    '.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,2.2vw,30px);\n'
    '  margin-top:clamp(28px,3vw,40px)}')
rep('.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:36px}',
    '.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(16px,2vw,26px);\n'
    '  margin-top:clamp(32px,3.4vw,44px)}')
rep('.dx-grid{margin-top:clamp(32px,4vw,48px);display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(14px,1.6vw,20px)}',
    '.dx-grid{margin-top:clamp(32px,4vw,52px);display:grid;grid-template-columns:repeat(3,1fr);\n'
    '  gap:clamp(16px,2vw,26px)}')
rep('.res-cards{margin-top:clamp(18px,2.2vw,26px);display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(14px,1.6vw,20px)}',
    '.res-cards{margin-top:clamp(22px,2.6vw,32px);display:grid;grid-template-columns:repeat(3,1fr);\n'
    '  gap:clamp(16px,2vw,26px)}')
rep('.psi-cards{margin-top:clamp(18px,2.2vw,26px);display:grid;grid-template-columns:1fr 1fr;gap:clamp(14px,1.6vw,20px)}',
    '.psi-cards{margin-top:clamp(22px,2.6vw,32px);display:grid;grid-template-columns:1fr 1fr;\n'
    '  gap:clamp(16px,2vw,26px)}')

# ── 4. 목록·행간 ────────────────────────────────────────────────
rep('.fit{display:flex;gap:16px;align-items:baseline;padding:18px 4px;',
    '.fit{display:flex;gap:16px;align-items:baseline;padding:clamp(20px,1.9vw,26px) 4px;')
rep('.fit-list{margin-top:32px;', '.fit-list{margin-top:clamp(32px,3.4vw,44px);')
rep('.dx-note{font-size:14px;line-height:1.62;', '.dx-note{font-size:14px;line-height:1.75;')

io.open(P, 'w', encoding='utf-8').write(s)
print('ok  css/global.css')
