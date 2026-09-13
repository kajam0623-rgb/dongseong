#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""히어로 교체 — "Creative Clicks." → "CICLO" + GEO 포지셔닝.

요청: 크리에이티브 클릭 대신 그냥 ciclo, 그리고 "geo 웹사이트, 랜딩페이지 제작".

바뀌는 것
  h1    Creative / Clicks.        → CICLO
  리드  "클릭을 고객으로 바꾸는 디자인" → "GEO 웹사이트, 랜딩페이지 제작"
  배지  스크롤 링의 CREATIVE CLICKS → GEO · WEBSITE · LANDING PAGE

왜 h1 이 한 단어여도 되나
  기존 h1 은 두 줄짜리 영문 표어였고 무엇을 파는지는 리드에 있었다. 이제
  h1 은 이름, 바로 아래 줄이 파는 것이다. 검색·AI 쪽에서도 이 편이 낫다
  — "무엇을 하는 회사인가"가 페이지 최상단 텍스트에 한 줄로 박힌다.

h1 한 단어는 clamp 상한(168px)에서 너무 커 보이므로 전용 크기를 준다.
글자 수가 6자로 줄어 자간도 조금 벌린다(-.03em → -.02em).
"""
import sys, io, os

HERE = os.path.dirname(os.path.abspath(__file__))

def rep(path, old, new):
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    if s.count(old) != 1:
        sys.exit('FAIL %s: %d회 — %r' % (path, s.count(old), old[:70]))
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
    print('ok  %s' % path)

# ── 마크업 ──────────────────────────────────────────────────────
rep('pages/Home.html',
    '  <h1 class="display">Creative <br><span class="blue">Clicks.</span></h1>\n'
    '  <p class="lead">클릭을 고객으로 바꾸는 디자인.<br>병원·법률·전문직을 위한 웹사이트와 검색 마케팅, 씨클로가 만듭니다.</p>',
    '  <h1 class="display hero-name">CICLO</h1>\n'
    '  <p class="lead hero-claim"><b>GEO 웹사이트, 랜딩페이지 제작</b><br>'
    '검색엔진과 AI가 읽을 수 있는 구조로 만듭니다. 병원·법률·전문직 전문.</p>')

rep('pages/Home.html',
    '<textPath href="#ring" textLength="286" lengthAdjust="spacing">CICLO · CREATIVE CLICKS · SCROLL ·</textPath>',
    '<textPath href="#ring" textLength="286" lengthAdjust="spacing">GEO · WEBSITE · LANDING PAGE ·</textPath>')

# ── CSS ────────────────────────────────────────────────────────
rep('css/global.css',
    '.hero h1{margin-top:22px;font-size:clamp(64px,11vw,168px)}',
    '.hero h1{margin-top:22px;font-size:clamp(64px,11vw,168px)}\n'
    '/* 한 단어 워드마크 — 두 줄 표어보다 글자가 커 보이므로 상한을 낮추고\n'
    '   자간을 조금 되돌린다(.display 의 -.03em 은 긴 문장 기준이다). */\n'
    '.hero h1.hero-name{font-size:clamp(58px,13vw,150px);letter-spacing:-.02em}\n'
    '.hero .hero-claim{margin-top:30px;max-width:none}\n'
    '.hero .hero-claim b{display:inline-block;margin-bottom:10px;font-weight:700;\n'
    '  font-size:clamp(19px,2vw,25px);letter-spacing:-.02em;color:var(--ink)}')
