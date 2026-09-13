#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""숫자 표기 — 한글 수사를 아라비아 숫자로.

왜
  "여덟 곳을 열 항목·쉰 개 체크포인트로 채점했습니다."
  이게 AI 티의 큰 원인이었다. 실무자는 이렇게 안 쓴다. 문어체 수사는
  글을 다듬은 티를 내고, 데이터를 말하는 문장에서는 더 그렇다.
  238LAB 은 세는 것을 전부 숫자로 쓴다 — "350+개", "384%", "80%",
  "최소 1개월", "약 3개월". 한 곳도 한글 수사가 없다.

규칙
  숫자로 : 실측·구조를 세는 것 — 곳 · 항목 · 개 · 점 · 단계 · 편 · 가지
  한글로 : 관용 표현 — "한 팀이", "두 번 만들게", "한 줄", "한 편"
           숫자로 바꾸면 오히려 어색한 자리다

이 파일은 표기만 바꾼다. 수치·사실·문장 구조는 건드리지 않는다.
"""
import io, glob, os, re, sys

# 긴 것부터 — "여덟 곳" 을 "여덟" 보다 먼저 잡아야 한다
MAP = [
    ('열 항목·',   '10개 항목·'),
    ('열 항목 ',   '10개 항목 '),
    ('열 항목',    '10개 항목'),
    ('여덟 곳',    '8곳'),
    ('일곱 곳',    '7곳'),
    ('다섯 개씩',  '5개씩'),
    ('다섯 개',    '5개'),
    ('네 단계',    '4단계'),
    ('세 단계',    '3단계'),
    ('여섯 가지',  '6가지'),
    ('네 가지',    '4가지'),
    ('세 가지',    '3가지'),
    ('두 항목',    '2개 항목'),
]

# 바꾸면 안 되는 자리 — 관용 표현이라 숫자로 쓰면 어색하다
KEEP = ['한 팀', '두 번 만들', '한 줄', '한 편', '한 번', '두 도구', '한 곳']

n = 0
for p in sorted(glob.glob('pages/*.html')):
    s = io.open(p, encoding='utf-8').read()
    before = s
    for a, b in MAP:
        s = s.replace(a, b)
    if s != before:
        c = sum(before.count(a) for a, _ in MAP)
        io.open(p, 'w', encoding='utf-8').write(s)
        print('  %-26s %d곳' % (os.path.basename(p), c)); n += c

print('총 %d곳' % n)

# 남은 한글 수사 확인
left = []
for p in glob.glob('pages/*.html'):
    t = io.open(p, encoding='utf-8').read()
    t = re.sub(r'<(style|script)[\s\S]*?</\1>', '', t)
    for m in re.finditer(r'(한|두|세|네|다섯|여섯|일곱|여덟|아홉|열|스물|서른|마흔|쉰)\s?(곳|개|항목|단계|가지|편|점|명)', t):
        frag = t[max(0, m.start()-16):m.end()+10].replace('\n', ' ')
        if not any(k in frag for k in KEEP):
            left.append('%s: %s' % (os.path.basename(p), frag))
if left:
    print('\n남은 한글 수사 %d건 (관용 표현이면 그대로 둔 것):' % len(left))
    for x in sorted(set(left))[:14]: print('   ', x)
