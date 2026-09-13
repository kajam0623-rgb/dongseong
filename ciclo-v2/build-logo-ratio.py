#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""로고·마크 비율 깨짐 수정 (사용자 제보 "로고가 찌그러지더라고").

실측 (플레이라이트, 원본 비율 488:566 = 0.862 대비):

  요소            @1440         @768                  @390                   @360
  hero-mark       534×620 정상  384×620  −28.2%       195×620  **−63.5%**    180×620 −66.3%
  footer-mark     539×625 정상  488×566 정상          390×646  −30.0%        360×646 −35.4%
  sidebar-brand   227×22 (부모 폭까지 늘어남)  ← 전 폭에서
  footer-brand    488×20 (부모 폭까지 늘어남)  ← 전 폭에서
  nav-logo        17.2×20 정상 (유일하게 width:auto 가 명시돼 있다)

원인 1 — 높이 고정 + 폭 제약의 충돌
  전역에 `img{max-width:100%;height:auto}` 가 있는데
  `.hero-mark img{height:min(78vh,620px)}` 가 height 를 다시 고정한다.
  좁은 화면에서는 max-width 가 폭만 잘라내고 높이는 620px 그대로 남아
  가로로 짓눌린 마크가 된다. 390px 에서 195×620, 즉 원본보다 2.7배 홀쭉하다.

원인 2 — content:url() 로 바꾼 요소에 width 가 없다
  `.nav-logo img` 만 `width:auto` 가 적혀 있고 `.sidebar-brand img`·`.footer-brand img`
  는 height 만 있다. content:url() 로 교체된 요소는 그 상태에서 고유 비율을 잃고
  부모 폭까지 늘어난다(227px·488px 실측). object-fit 기본값이 fill 이라 그대로 늘어난 채 그려진다.

조치 — 마크는 어떤 폭에서도 488:566 을 유지한다
  · 높이 기준 → **폭 기준 + aspect-ratio** 로 바꾼다. 폭은 vw 로 제한되므로
    좁은 화면에서 높이가 알아서 따라 줄고, 데스크톱 최대치는 종전과 같다
    (534px 폭 = 620px 높이).
  · 모든 로고에 `width:auto`·`aspect-ratio`·`object-fit:contain` 을 명시한다.
    셋 중 하나만 있어도 대개 되지만, content:url() 교체·테마 CSS·Elementor
    오버라이드가 겹치는 환경이라 셋 다 걸어 둔다.
"""
import sys, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'global.css')
s = io.open(P, encoding='utf-8').read()
before = len(s.encode('utf-8'))

def rep(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('FAIL: %d회 — %r' % (s.count(old), old[:70]))
    s = s.replace(old, new)

# 1. 히어로 마크 — 높이 고정을 폭 기준으로
rep('.hero-mark img{height:min(78vh,620px);width:auto;filter:invert(.78);opacity:.1}',
    '/* 폭 기준으로 잡는다. 높이를 고정하면 전역 img{max-width:100%} 가 폭만 잘라내\n'
    '   390px 에서 195×620(비율 −63.5%)까지 짓눌렸다. 534px 폭 = 종전 620px 높이. */\n'
    '.hero-mark img{width:min(84vw,534px);height:auto;aspect-ratio:488/566;object-fit:contain;\n'
    '  filter:invert(.78);opacity:.1}')

# 2. 푸터 배경 마크
rep('.footer-mark{position:absolute;right:-6%;bottom:-20%;height:90%;width:auto;opacity:.07;pointer-events:none}',
    '.footer-mark{position:absolute;right:-6%;bottom:-20%;height:90%;width:auto;max-width:64vw;\n'
    '  aspect-ratio:488/566;object-fit:contain;opacity:.07;pointer-events:none}')

# 3. 브랜드 로고 3종 — width:auto 가 없어 부모 폭까지 늘어나던 것
rep('.sidebar-brand img{height:22px}',
    '.sidebar-brand img{height:22px;width:auto;aspect-ratio:488/566;object-fit:contain}')
rep('.footer-brand img{height:20px}',
    '.footer-brand img{height:20px;width:auto;aspect-ratio:488/566;object-fit:contain}')
rep('.nav-logo img{height:20px;width:auto}',
    '.nav-logo img{height:20px;width:auto;aspect-ratio:488/566;object-fit:contain}')

# 4. 코너 라벨이 카톡 버튼과 겹치던 것 (데스크톱)
#    플로팅 버튼을 bottom:20px 로 되돌리면서 생긴 충돌 — 라벨을 버튼 위로 올린다
rep(".hero .corner.r{right:clamp(16px,6vw,120px);bottom:56px;",
    ".hero .corner.r{right:clamp(16px,6vw,120px);bottom:96px;")

io.open(P, 'w', encoding='utf-8').write(s)
print('ok  css/global.css  %d → %d B (%+d)' % (before, len(s.encode('utf-8')), len(s.encode('utf-8')) - before))
