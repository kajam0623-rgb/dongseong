#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""히어로·증거 밴드 문체 교정 + 남은 표기 정리.

앞선 패스에서 못 잡은 것들
  1. 줄표(—) 20회. 히어로 증거 3줄이 전부 "A — B" 한 모양이었다.
     세 줄이 같은 틀이면 그게 또 운율이다. 모양을 흩는다.
  2. 은유 반복 — "자리" 14회, "칸" 4회.
     "기계가 읽는 자리", "중앙값 자리", "이 2칸이 비면".
     한 번은 표현이고 열네 번은 버릇이다. 항목 이름 그대로 쓴다.
  3. "표본이 스무 곳" — 숫자 패스에서 놓친 한글 수사.
  4. "네 항목 100점" — PSI 카드를 원본에 맞추며 5개 항목이 됐는데
     본문 세 곳이 '네 항목'으로 남아 수치가 서로 어긋나 있었다.
     사실 오류라 문체와 별개로 고쳐야 한다.
  5. "그대로 열어 뒀습니다" · "항목을 짚어 보실 수" — 앞에서 센 반복어.
"""
import io, os, sys

E = [
# ── 히어로 증거 3줄: 전부 "A — B" 였다. 셋을 다른 모양으로 ──
('pages/Home.html',
 '<span class="hp-c">사람이 보는 화면과 기계가 읽는 자리 — 치과 8곳 평균</span>',
 '<span class="hp-c">치과 8곳 평균. 사람이 보는 화면과 기계가 읽는 정보의 차이</span>'),
('pages/Home.html',
 '<span class="hp-c">PageSpeed Insights 네 항목 — 저희가 만든 사이트 실측</span>',
 '<span class="hp-c">저희가 만든 사이트의 PageSpeed Insights 5개 항목 실측</span>'),
('pages/Home.html',
 '<span class="hp-c">최근 90일 검색 유입 — 직전 90일 약 6클릭에서</span>',
 '<span class="hp-c">최근 90일 검색 유입. 직전 90일은 약 6클릭이었습니다</span>'),

# ── 증거 밴드: 은유를 항목 이름으로 ──
('pages/Home.html',
 '가장 높은 칸과 가장 낮은 칸이 같은 정보를 다룹니다.',
 '점수가 가장 높은 항목과 가장 낮은 항목이 같은 정보를 다룹니다.'),
('pages/Home.html',
 '<span class="ev-cap">기계가 읽는 자리</span>',
 '<span class="ev-cap">기계가 읽는 정보</span>'),
('pages/Home.html',
 '검색엔진과 AI가 읽는 형식으로 옮겨져 있지 않았을 뿐입니다.',
 '검색엔진과 AI가 읽는 형식으로는 옮겨져 있지 않았습니다.'),
('pages/Home.html',
 '병원 이름과 주소만 나오면 20점 근처, 조사 표본의 중앙값 자리입니다.',
 '병원 이름과 주소만 나오면 20점 근처로, 조사 표본의 중앙값입니다.'),
('pages/Home.html',
 '나머지 8개 항목을 올려도 이 2칸이 비면 AI는 다른 사이트를 인용합니다.',
 '나머지 8개 항목을 올려도 이 2개가 비면 AI는 다른 사이트를 인용합니다.'),
('pages/Home.html',
 '표본이 스무 곳을 넘으면 기준을 다시 맞추고 갱신합니다.',
 '표본이 20곳을 넘으면 기준을 다시 맞추고 갱신합니다.'),
('pages/Home.html',
 '점수 옆에 그 점수가 나온 근거를 같이 답니다.',
 '점수마다 근거를 같이 적었습니다.'),
('pages/Home.html',
 '채점 기준 50개와 8곳 결과를 그대로 열어 뒀습니다. 다른 업체 견적서를 받으셨을 때 항목을 짚어 보실 수 있습니다.',
 '채점 기준 50개와 8곳 결과를 전부 공개했습니다. 다른 업체 견적서를 받으셨을 때 항목별로 대조해 보실 수 있습니다.'),

# ── 수치 어긋남: PSI 는 5개 항목이다 ──
('pages/Home.html', '다섯 항목 만점은', '5개 항목 만점은'),
('pages/Work.html', '네 항목 100점</h3>', '5개 항목 만점</h3>'),
('pages/Work.html', '네 항목 100점은 빠르다는', '5개 항목 만점은 빠르다는'),
('pages/Work.html', '페이지 속도 — PageSpeed Insights 네 항목',
                    '페이지 속도 · PageSpeed Insights 5개 항목'),
]

HERE = os.path.dirname(os.path.abspath(__file__))
n, miss = 0, []
for path, old, new in E:
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    if old not in s: miss.append((path, old[:54])); continue
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1)); n += 1

print('%d곳 교체' % n)
if miss:
    print('\n★ 못 찾음 %d건' % len(miss))
    for a, b in miss: print('   %s  %s' % (a, b))
    sys.exit(1)
