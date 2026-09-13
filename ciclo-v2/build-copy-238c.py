#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""카피 재작성 3차 — 본문에 남은 "~가 아니라 ~입니다" 다섯 곳.

h2 는 2차에서 끝냈고, 본문에 다섯 개가 남아 있었다. 같은 반전 수법이다.
(css/global.css 안의 주석 한 건은 코드 설명이라 그대로 둔다)
"""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))

E = [
('pages/About.html',
 '고를 때 필요한 건 잘한다는 말이 아니라 무엇을 안 하는지입니다.',
 '에이전시를 고를 때는 그 회사가 무엇을 안 하는지를 보셔야 합니다.'),
('pages/About.html',
 '에이전시를 고를 때 확인할 것은 포트폴리오 화면이 아니라 판단 기준입니다. 저희 기준은 전부 열려 있습니다.',
 '포트폴리오 화면보다 판단 기준을 보셔야 합니다. 저희 기준은 전부 열려 있습니다.'),
('pages/Digital_Marketing.html',
 '감이 아니라 데이터로 운영합니다.',
 '데이터로 운영합니다.'),
('pages/Home.html',
 '잘 만든 집과 그렇지 않은 집이 갈리는 항목이 아니라, 아직 아무도 손대지 않은 항목입니다.',
 '표본 여덟 곳 모두가 아직 손대지 않은 항목입니다.'),
('pages/치과_홈페이지_제작.html',
 '작업 범위를 줄이는 것이 아니라, 초기 사례를 확보하기 위한 가격입니다.',
 '작업 범위는 그대로이고, 초기 사례를 확보하기 위한 가격입니다.'),
]

n, miss = 0, []
for path, old, new in E:
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    if old not in s: miss.append((path, old[:50])); continue
    io.open(p,'w',encoding='utf-8').write(s.replace(old, new, 1)); n += 1

print('%d곳 교체' % n)
if miss:
    for a,b in miss: print('   ★ 못 찾음 %s  %s' % (a,b))
    sys.exit(1)
