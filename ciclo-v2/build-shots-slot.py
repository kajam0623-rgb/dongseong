#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""긴 주석 두 덩이를 빼고 그 자리를 원본 캡처 자리로 바꾼다.

무엇을 빼나 (사용자 지시)
  1. 네이버 유입 카드 밑  — "증가율이 세 자리·네 자리로 보이는 이유를…" 5줄
  2. PSI 카드 밑          — "5개 항목 만점은 빠르다는 뜻입니다…" 3줄
  둘 다 길고, 카드가 이미 말하고 있는 걸 다시 설명하고 있었다.

  다만 1번에는 지우면 안 되는 사실이 하나 들어 있다 — 세 곳 모두 직전 90일
  클릭이 한 자리였다는 것. 그게 없으면 +12,300% 가 실제보다 크게 읽힌다.
  카드 안에 이미 "직전 90일 클릭 약 6" 줄이 있으므로 정보는 남지만,
  섹션 맨 아래 sec-caption 에 한 줄로 옮겨 붙여 둔다.

무엇을 넣나
  그 자리에 도구 원본 캡처를 넣는다. 캡처 파일이 아직 없으므로 지금은
  자리만 만들고(주석), 파일이 들어오면 build-psi-shots.py 가 채운다.
  마크업을 미리 넣어 두면 빈 이미지가 뜨므로 넣지 않는다.
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def cut(path, marker, label):
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    i = s.find(marker)
    if i < 0: return None
    j = s.find('</p>', i) + 4
    # 앞 들여쓰기와 뒤 줄바꿈까지 걷어낸다
    a = s.rfind('\n', 0, i) + 1
    b = j + 1 if s[j:j+1] == '\n' else j
    removed = s[a:b]
    io.open(p, 'w', encoding='utf-8').write(s[:a] + s[b:])
    print('  %-16s −%d자  %s' % (label, len(removed), label))
    return removed

n = 0
if cut('pages/Home.html', '<p class="res-note">증가율이 세 자리', '네이버 유입 카드 주석'): n += 1
if cut('pages/Home.html', '<p class="res-note">5개 항목 만점은', 'PSI 카드 주석'): n += 1

# 지우면 안 되는 사실 한 줄을 섹션 캡션으로 옮긴다
p = os.path.join(HERE, 'pages/Home.html')
s = io.open(p, encoding='utf-8').read()
OLD = '<p class="sec-caption">네이버 서치어드바이저 최근 90일 기준(2026년 9월 측정)'
if OLD in s and '직전 90일 클릭이 한 자리' not in s:
    s = s.replace(OLD,
        '<p class="sec-caption"><b>세 곳 모두 직전 90일 클릭이 한 자리였습니다.</b> '
        '740클릭은 6클릭에서, 74클릭은 1클릭에서 온 값이라 배수만 보시면 실제 크기를 잘못 읽게 됩니다. · '
        '네이버 서치어드바이저 최근 90일 기준(2026년 9월 측정)', 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('  캡션에 이월      직전 90일 클릭 한 자리 사실')
    n += 1

print('\n%d곳 처리' % n)

# 캡처 자리 준비
for d, who in [('assets/psi', 'PageSpeed Insights'), ('assets/naver', '네이버 서치어드바이저')]:
    os.path.isdir(os.path.join(HERE, d)) or os.makedirs(os.path.join(HERE, d))
NAVER = os.path.join(HERE, 'assets', 'naver', 'README.md')
if not os.path.exists(NAVER):
    io.open(NAVER, 'w', encoding='utf-8').write(
"""# 서치어드바이저 캡처 넣는 자리

네이버 서치어드바이저 최근 90일 화면 캡처를 여기에 둡니다.
파일 이름은 아무거나 됩니다 — 스크립트가 순서대로 배정합니다.

```
치과 ① 수도권 · 종합진료   740클릭
치과 ② 인천 · 사랑니 중심   110클릭
치과 ③ 수도권 · 개원 초기    74클릭
```

가릴 곳: **사이트 주소(도메인)** · 좌측 사이트 목록에 뜨는 병원명.
리사이즈·모자이크·WebP 변환은 `build-psi-shots.py` 가 합니다.
원본 그대로 두세요.
""")
    print('assets/naver/ 자리 생성')
