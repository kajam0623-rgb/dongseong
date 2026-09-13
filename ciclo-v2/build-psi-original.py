#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PSI 카드를 원본 보고서 내용에 맞춘다.

원본 캡처 두 장(사용자 제공, 2026-09-13 수령)에서 읽은 값

  휴대전화 · 2026. 8. 31. 오후 10:00:16
    성능 100 · 접근성 100 · 권장사항 100 · 검색엔진 최적화 100 · 에이전트형 브라우징 3/3
    FCP 1.0초 · LCP 1.7초 · TBT 0밀리초 · CLS 0.003 · Speed Index 1.8초
    실제 사용자의 경험 확인하기 → 데이터 없음

  데스크톱 · 2026. 8. 31. 오후 12:39:34
    성능 100 · 접근성 100 · 권장사항 100 · 검색엔진 최적화 100 · 에이전트형 브라우징 2/2
    FCP 0.4초 · LCP 0.6초 · TBT 10밀리초 · CLS 0.006 · Speed Index 0.6초
    실제 사용자의 경험 확인하기 → 데이터 없음

카드에 이미 있던 것: 네 항목 점수와 다섯 개 지표 (전부 원본과 일치)
빠져 있던 것 세 가지를 채운다
  1. 다섯 번째 항목 "에이전트형 브라우징" 3/3 · 2/2
  2. 측정 일시 — 238LAB 은 데이터마다 시점을 붙인다
  3. "실제 사용자 데이터 없음" — 원본 화면에 그렇게 찍혀 있다.
     실측 트래픽이 쌓이지 않아 CrUX 필드 데이터가 없다는 뜻이고,
     그걸 안 적으면 실사용자 기준 수치인 것처럼 읽힌다.

왜 캡처 이미지를 그대로 안 싣나
  · 두 캡처 모두 주소창에 도메인이 그대로 찍혀 있다. 사이트에는
    "병원명·주소·도메인은 가렸습니다" 라고 적어 두었다. 지우려면 모자이크를
    씌워야 하고, 모자이크 씌운 캡처는 "원본 그대로"가 아니게 된다.
  · 캡처는 이미지 두 장(수백 KB)이고 표는 텍스트다. PageSpeed 100점을
    내세우는 섹션을 이미지로 무겁게 만들 이유가 없다.
  · 무엇보다 검색엔진과 AI가 이미지 속 숫자는 못 읽는다. GEO 를 파는
    회사가 자기 근거를 기계가 못 읽는 형식으로 두면 앞뒤가 안 맞는다.
  캡처 원본이 필요하신 분께는 문의로 드리면 된다.
"""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))

def patch(path, pairs):
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    miss = [o[:60] for o, n in pairs if o not in s]
    if miss:
        for m in miss: print('   ★ 못 찾음: %s' % m)
        return 0
    for o, n in pairs: s = s.replace(o, n, 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    return len(pairs)

SCORES = '<div class="psi-s"><div class="psi-ring">100</div><small>검색엔진<br>최적화</small></div>\n        </div>'

M = [
# ── 모바일 카드 ──
('<div class="res-top"><span class="res-id">치과 ④</span><span class="res-tag">모바일 측정</span></div>',
 '<div class="res-top"><span class="res-id">치과 ④</span><span class="res-tag">모바일 측정</span></div>\n'
 '        <p class="psi-when">2026년 8월 31일 22:00 측정 · 휴대전화</p>'),
(SCORES,
 '<div class="psi-s"><div class="psi-ring">100</div><small>검색엔진<br>최적화</small></div>\n'
 '          <div class="psi-s"><div class="psi-ring psi-frac">3/3</div><small>에이전트형<br>브라우징</small></div>\n        </div>'),
('<div class="psi-v"><b>1.8초</b><small>속도 지수</small></div>\n        </div>',
 '<div class="psi-v"><b>1.8초</b><small>속도 지수</small></div>\n        </div>\n'
 '        <p class="psi-field">실제 사용자의 경험 — <b>데이터 없음</b>. 최근 방문이 적어 구글이 실사용자 기록을 쌓지 못한 상태입니다. 위 값은 실험실 측정치입니다.</p>'),
# ── 데스크톱 카드 ──
('<div class="res-top"><span class="res-id">치과 ⑤</span><span class="res-tag">데스크톱 측정</span></div>',
 '<div class="res-top"><span class="res-id">치과 ⑤</span><span class="res-tag">데스크톱 측정</span></div>\n'
 '        <p class="psi-when">2026년 8월 31일 12:39 측정 · 데스크톱</p>'),
(SCORES,
 '<div class="psi-s"><div class="psi-ring">100</div><small>검색엔진<br>최적화</small></div>\n'
 '          <div class="psi-s"><div class="psi-ring psi-frac">2/2</div><small>에이전트형<br>브라우징</small></div>\n        </div>'),
('<div class="psi-v"><b>0.6초</b><small>속도 지수</small></div>\n        </div>',
 '<div class="psi-v"><b>0.6초</b><small>속도 지수</small></div>\n        </div>\n'
 '        <p class="psi-field">실제 사용자의 경험 — <b>데이터 없음</b>. 최근 방문이 적어 구글이 실사용자 기록을 쌓지 못한 상태입니다. 위 값은 실험실 측정치입니다.</p>'),
# ── 섹션 리드·주석·캡션 ──
('<span class="res-src">출처: PageSpeed Insights (Lighthouse) · 실제 URL 측정</span>',
 '<span class="res-src">출처: PageSpeed Insights · 2026년 8월 31일 측정</span>'),
('네 항목 100점은 <b>빠르다는 뜻입니다.</b>',
 '다섯 항목 만점은 <b>빠르다는 뜻입니다.</b>'),
('PageSpeed Insights 실측 · 병원명·주소·도메인은 가렸습니다',
 'PageSpeed Insights 2026년 8월 31일 측정(실험실 기준, 실사용자 데이터 없음) · 병원명·주소·도메인은 가렸습니다'),
]

n = patch('pages/Home.html', M)
print('홈 %d곳' % n)

CSS = """
/* PSI 카드 — 원본 보고서에 있는 두 줄을 마저 싣는다.
   측정 일시와 "실사용자 데이터 없음"이 그것이다. 시점 없는 수치는 238LAB 기준으로
   근거가 아니고, 필드 데이터가 없다는 사실을 빼면 실사용자 기준값처럼 읽힌다. */
.psi-when{margin-top:8px;font-size:11.5px;font-weight:600;letter-spacing:.02em;color:rgba(18,18,18,.62);
  font-variant-numeric:tabular-nums}
/* 다섯 번째 항목은 점수가 아니라 통과 개수(3/3)다. 링 안에 들어가야 하므로 글자를 줄인다. */
.psi-ring.psi-frac{font-size:clamp(15px,1.5vw,19px);letter-spacing:-.02em}
.psi-field{margin-top:14px;padding-top:12px;border-top:1px solid rgba(18,18,18,.1);
  font-size:11.5px;line-height:1.6;font-weight:400;color:rgba(18,18,18,.66)}
.psi-field b{font-weight:800;color:var(--pt)}
@media(max-width:620px){.psi-scores{grid-template-columns:repeat(3,1fr);gap:14px 10px}}
"""
p = os.path.join(HERE, 'css', 'global.css')
s = io.open(p, encoding='utf-8').read()
anchor = '/* PSI 실제 캡처 — 재현 표(.psi-cards) 대신 도구 화면을 그대로 싣는 경우.'
if anchor not in s: sys.exit('FAIL: CSS 앵커를 찾지 못함')
s = s.replace(anchor, CSS.strip() + '\n\n' + anchor, 1)
io.open(p,'w',encoding='utf-8').write(s)
print('CSS 규칙 추가')
sys.exit(0 if n == len(M) else 1)
