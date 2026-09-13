#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""히어로 워드마크 색 확정 — 검정 + 네이비 마침표.

시안 3종을 같은 화면에 렌더해 비교했다(HERO-a/b/c × 1440·390).

  A 검정 단색      깔끔하지만 히어로에 브랜드 컬러가 CTA 버튼에만 남는다.
                   서브페이지 히어로는 전부 검정+네이비 조합인데 홈만 빠진다.
  B 네이비 단색    150px 짜리 네이비 덩어리가 뒤의 회색 C 마크와 두 개의
                   어두운 덩어리로 부딪힌다. 시선이 판매 문구까지 안 내려온다.
  C 검정+네이비 . ★ 마침표 하나로 브랜드 컬러가 돌아오고, 가장 무거운 덩어리는
                   검정 워드마크가 유지한다. 예전 "Clicks." 의 마침표와도 이어진다.

C 를 적용한다. 150px 에서는 마침표 앞 자간이 실제로 몇 px 벌어지므로 조금 당긴다.

같이 고치는 것 — 모바일에서 리드가 3줄로 깨진다
  "…구조로 만듭니다.<br>병원·법률·…" 의 <br> 가 390px 에서 "만듭니다." 만
  한 줄에 남긴다. 좁은 화면에서는 <br> 을 풀되, 그러면 "만듭니다.병원" 으로
  붙으므로 제목에 했던 것과 같이 <br> 앞에 공백을 넣어 둔다.
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

rep('pages/Home.html',
    '<h1 class="display hero-name">CICLO</h1>',
    '<h1 class="display hero-name">CICLO<span class="blue">.</span></h1>')

# <br> 앞 공백 — 모바일에서 br 을 풀 때 단어가 붙지 않게
rep('pages/Home.html',
    '구조로 만듭니다.<br>병원·법률·전문직 브랜드를 맡습니다.',
    '구조로 만듭니다. <br>병원·법률·전문직 브랜드를 맡습니다.')

rep('css/global.css',
    ".hero h1.hero-name{font-size:clamp(58px,13vw,150px);letter-spacing:-.02em}",
    ".hero h1.hero-name{font-size:clamp(58px,13vw,150px);letter-spacing:-.02em}\n"
    "/* 마침표는 브랜드 컬러 한 점. 150px 에서는 앞 자간이 실제로 몇 px 벌어지므로 당긴다. */\n"
    ".hero h1.hero-name .blue{margin-left:-.06em}")

rep('css/global.css',
    '  .scroll-badge{display:none}',
    '  .scroll-badge{display:none}\n'
    '  /* 좁은 화면에서는 리드의 강제 개행을 푼다 — "만듭니다." 만 한 줄에 남았다 */\n'
    '  .hero .hero-claim br{display:none}')
