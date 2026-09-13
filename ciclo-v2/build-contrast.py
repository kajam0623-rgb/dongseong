#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""대비 미달 텍스트 색 상향 — WCAG AA (4.5:1).

사용자가 세운 목표가 "PageSpeed 100점"이고 거기엔 접근성 100점도 들어간다.
라이트하우스는 대비를 자동 검사하므로, 미달이 남아 있으면 100점이 안 나온다.

실측 (헤드리스 크롬, 텍스트 노드를 가진 요소 전수 대조)
  홈·Work·About·Contact 에서 **27곳**이 AA 미달.

  크림/패널 배경 위 잉크          네이비 배경 위 흰색
    α .48 → 3.23 / 3.16            α .35 → 2.96
    α .50 → 3.43 / 3.35
    α .55 → 4.00 / 3.90

임계값을 계산했다 (패널 #ECE7DC 가 크림보다 어두워 더 빡빡한 쪽을 기준으로).
    크림·패널 위 잉크   α ≥ .62  (4.87:1)
    네이비 위 흰색      α ≥ .55  (5.33:1)

그래서 .35/.4/.45/.48/.5/.55 를 .62(잉크) / .55(흰색)로 올린다.
.6 이상은 이미 통과하므로 두고, 큰 글자(24px 이상)는 3:1 이면 되지만
같은 토큰을 공유하므로 함께 올린다 — 진해져서 나빠지는 곳은 없다.

★ 오탐 하나를 걸러냈다
  `.ev-dot > b` 가 1.17:1 로 잡혔는데, 측정 스크립트가 부모인 노란 점을
  배경으로 잡아서다. 라벨은 실제로는 점 **위쪽 네이비 바탕**에 놓인다
  (흰색 .6 on 네이비 = 5.8:1, 통과). 색을 바꾸지 않는다.

  선 색·테두리·배경으로 쓰는 rgba 는 대비 대상이 아니라 건드리지 않는다.
  `color:` 선언만 바꾼다.
"""
import sys, io, os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'global.css')
s = io.open(P, encoding='utf-8').read()

INK_MIN, WHITE_MIN = 0.62, 0.55
changed = {}

def bump(m):
    kind, a = m.group(1), float(m.group(2))
    lo = INK_MIN if kind.startswith('18') else WHITE_MIN
    if a >= lo:
        return m.group(0)
    key = 'rgba(%s,%s)' % (kind, m.group(2))
    changed[key] = changed.get(key, 0) + 1
    return 'color:rgba(%s,%s)' % (kind, ('%.2f' % lo).lstrip('0'))

# color: 선언만. 테두리·배경·그림자는 제외된다.
s2 = re.sub(r'color:rgba\((18,18,18|255,255,255),(\.\d+)\)', bump, s)

if not changed:
    sys.exit('바꿀 것이 없습니다')

io.open(P, 'w', encoding='utf-8').write(s2)
print('ok  css/global.css')
for k in sorted(changed, key=lambda x: -changed[x]):
    tgt = INK_MIN if '18,18,18' in k else WHITE_MIN
    print('   %-30s %2d곳 → %.2f' % (k, changed[k], tgt))
