#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Elementor·Hello 테마 호환 CSS 제거 — 자체 테마에서는 전부 죽은 코드다.

지울 것 (전부 마크업에서 미사용 확인)
  1. Elementor 위젯 호환 오버라이드
     .elementor-widget-container · .elementor-heading-title · .elementor-button …
     레이아웃 클래스에 붙은 display:grid!important / flex!important 도 여기 속한다.
     Elementor 컨테이너의 flex 기본값을 이기려고 붙였던 것이라, 우리가 마크업을
     그리는 지금은 !important 없이도 그대로 적용된다.
  2. 페이지 빌더용 유틸 (.pt0 · .sec-sm · .sec-name · .on-navy · .ciclo-header …)
     빌더에서 클래스로 조판하려고 만든 것들. 마크업 사용 0건.
  3. Hello Elementor 테마 기본 마크업 브랜딩
     .wp-block-post-title · .entry-title · body.blog/.archive/.single …
     테마가 그리던 목록·글을 우리 템플릿(col-* / post-*)이 대신하므로 불필요.
  4. `main.site-main>.page-content:has(.ciclo-page)` 방어선
     커스터마이저의 820px 규칙을 막으려던 것. 우리 테마에는 그 규칙이 없다.

남길 것
  로고 `content:url(...)` — 이건 호환 코드가 아니라 실제 로고다.
  블록 한가운데 있어서 앞뒤를 따로 잘라낸다.
"""
import sys, io, os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'global.css')
s = io.open(P, encoding='utf-8').read()
before_len, before_rules = len(s.encode('utf-8')), s.count('{')

def cut(start_marker, end_marker, label, keep_end=False):
    """start_marker 가 나오는 줄부터 end_marker 직전까지 잘라낸다."""
    global s
    i = s.find(start_marker)
    if i < 0:
        sys.exit('FAIL: %s 시작을 찾지 못함' % label)
    i = s.rfind('\n', 0, i) + 1
    # 주석 여는 줄까지 포함
    j = s.find(end_marker, i)
    if j < 0:
        sys.exit('FAIL: %s 끝을 찾지 못함' % label)
    if not keep_end:
        j = s.rfind('\n', i, j) + 1
    removed = s[i:j]
    s = s[:i] + s[j:]
    print('  %-34s −%5d B · 규칙 %d개' % (label, len(removed.encode('utf-8')), removed.count('{')))

print('잘라낸 블록')

# 1) 820px 방어선 (커스터마이저 규칙 대응) — 우리 테마엔 그 규칙이 없다
cut('/* ★ 홈·랜딩 폭 방어', '/* responsive */', '홈 폭 방어선')

# 2) Elementor 호환 ~ 로고 직전
cut('/* =========================================================\n   Elementor 호환 오버라이드',
    '/* --- 로고를 CSS에 직접 내장', 'Elementor 위젯 호환')

# 3) 로고 다음(빌더 유틸) ~ 파일 끝의 테마 브랜딩 블록 끝
#    빌더 유틸 시작 ~ 칼럼 브랜딩 블록이 끝나는 지점까지 한 번에
start = s.find('/* --- 페이지 빌더용 유틸 클래스 --- */')
if start < 0:
    sys.exit('FAIL: 빌더 유틸 블록을 찾지 못함')
start = s.rfind('\n', 0, start) + 1
# 브랜딩 블록의 끝 = 그 다음에 오는 우리 컴포넌트 주석
# 다음 블록(.column-wrap / .col-side)은 우리가 쓰므로 그 주석 앞에서 멈춘다
after = s.find('   칼럼 페이지 (인블로그 스타일)', start)
if after < 0:
    sys.exit('FAIL: 브랜딩 블록 끝(칼럼 페이지 주석)을 찾지 못함')
after = s.rfind('/* =========', start, after)
if after < 0:
    sys.exit('FAIL: 칼럼 페이지 주석의 여는 줄을 찾지 못함')
removed = s[start:after]
if 'elementor' not in removed and 'entry-title' not in removed:
    sys.exit('FAIL: 잘라낼 구간이 예상과 다름 — %r' % removed[:120])
s = s[:start] + s[after:]
print('  %-34s −%5d B · 규칙 %d개' % ('빌더 유틸 + 테마 브랜딩', len(removed.encode('utf-8')), removed.count('{')))

s = re.sub(r'\n{4,}', '\n\n\n', s)
io.open(P, 'w', encoding='utf-8').write(s)

after_len, after_rules = len(s.encode('utf-8')), s.count('{')
print()
print('  크기   %d → %d B  (%+d)' % (before_len, after_len, after_len - before_len))
print('  규칙   %d → %d개  (%+d)' % (before_rules, after_rules, after_rules - before_rules))
print()
for term in ('elementor', 'entry-title', 'wp-block-post', 'site-main', 'ciclo-live'):
    print('  남은 %-14s %d건' % (term, s.count(term)))
print('  로고 content:url  %d건 (1이어야 함)' % s.count('content:url('))
