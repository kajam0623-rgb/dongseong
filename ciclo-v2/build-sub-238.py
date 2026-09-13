#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""서브페이지 238 패스 — 격언 걷어내고 근거·출처·다음 단계를 붙인다.

h2 는 앞선 패스에서 끝냈다. 서브페이지를 다시 읽어 보니 남은 문제가 둘이다.

1) 격언조 단문
     "나눠 맡기면 이음새에서 빠집니다"
     "전문성은 한 편으로 증명되지 않습니다"
     "여러 개를 적으면 하나도 안 지키게 됩니다"
   238LAB 은 격언을 쓰지 않는다. 잰 숫자를 놓고 끝낸다.
     "이삼팔랩은 2025년 기준, 350+개 프로젝트에서 평균 검색 유입 384% 증가
      개선을 만들어냈습니다."
   씨클로에는 이미 1차 데이터가 있다(치과 여덟 곳 실태조사). 격언 자리에
   그 데이터를 넣는다. 없는 숫자는 만들지 않는다.

2) 서비스 네 페이지에 출처 캡션도 다음 단계 링크도 없다
   238LAB 의 핵심 습관 두 가지가 통째로 빠져 있었다.
     · 모든 데이터 밑에 작은 회색 캡션 — 주장 → 출처 → 시점이 세트
       "25년 9월 statcounter, South Korea 기준"
     · 섹션마다 다음 행동 링크
       "업종별 성공사례 확인하기 →"
   홈·Work·About·Contact 에는 있는데 서비스 페이지에만 없었다.

실태조사 실측값 (2026년 8월, 표본 8곳, 열 항목 쉰 개 체크포인트)
  의료진 신뢰정보 81 · 지역 검색 73 · 콘텐츠 품질 73 · 콘텐츠 확장성 63
  사이트 구조 60 · 페이지 기본 세팅 58 · 도메인 위생 51 · 기술·성능 47
  AI 검색 대응 35 · 기계용 정보 표기 20
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = ('2026년 8월 측정 · 표본 8곳 · 열 항목 쉰 개 체크포인트 · '
        '공개된 HTML 소스만 확인 · 이 점수는 검색 순위나 매출을 예측하지 않습니다')
LINK = ('<a class="sec-link" href="https://dental-seo-report.vercel.app/" '
        'target="_blank" rel="noopener">채점 기준 쉰 개와 전체 리포트 보기 →</a>')

def cap(t=SRC): return '<p class="sec-caption">%s</p>' % t

# 격언 → 실측 문장
LEADS = [
('pages/Website_Design.html',
 '<p class="sec-lead">나눠 맡기면 이음새에서 빠집니다. 디자인과 검색 기본기를 같은 단계에서 설계해야 나중에 다시 뜯을 일이 없습니다.</p>',
 '<p class="sec-lead">치과 여덟 곳을 채점했을 때 제작 단계에서 정해지는 항목이 가장 낮았습니다. '
 '사이트 구조 60점, 페이지 기본 세팅 58점, 기술·성능 47점입니다. 세 항목 모두 오픈 뒤에 고치려면 화면부터 다시 뜯어야 하는 자리입니다.</p>'),
('pages/Blog_Content.html',
 '<p class="sec-lead">전문성은 한 편으로 증명되지 않습니다. 검색 의도에 맞는 글이 쌓여야 신뢰가 됩니다.</p>',
 '<p class="sec-lead">치과 여덟 곳의 콘텐츠 품질은 평균 73점이었고, 콘텐츠 확장성은 63점이었습니다. '
 '글은 있는데 쌓이는 구조가 없다는 뜻입니다.</p>'),
('pages/Digital_Marketing.html',
 '<p class="sec-lead">검색 구조가 잡히지 않은 상태에서 광고비부터 올리면, 클릭은 늘어도 그 클릭이 도착하는 페이지가 여전히 읽히지 않습니다.</p>',
 '<p class="sec-lead">치과 여덟 곳의 기술·성능 점수는 평균 47점이었습니다. '
 '광고로 데려온 방문자도 검색으로 온 방문자와 같은 페이지에 도착합니다.</p>'),
('pages/About.html',
 '<p class="sec-lead">여러 개를 적으면 하나도 안 지키게 됩니다. 제안서를 쓸 때도 이 셋으로 먼저 걸러냅니다.</p>',
 '<p class="sec-lead">기준을 셋으로 제한했습니다. 제안서를 쓸 때도 이 셋으로 먼저 걸러냅니다.</p>'),
('pages/About.html',
 '<p class="sec-lead">CICLO는 "Creative Ideas Click Logic"의 약자입니다. 창의적인 아이디어와 클릭을 만드는 논리 — 감각과 데이터 둘 다 놓치지 않겠다는 약속입니다. 사명에 논리를 넣어 두면 나중에 감으로 일할 수 없습니다.</p>',
 '<p class="sec-lead">CICLO는 "Creative Ideas Click Logic"의 약자입니다. '
 '아이디어를 내는 일과 그 아이디어가 클릭을 만드는지 재는 일을 같이 하겠다는 뜻으로 지었습니다.</p>'),
]

# 출처 캡션 + 다음 단계 링크를 서비스 네 페이지의 첫 섹션 끝에 붙인다
TAILS = [
('pages/GEO.html',
 '    <div class="card"><div class="num">06</div><h3>모니터링 리포트</h3><p>AI 답변 속 브랜드 언급과 검색 순위 변화를 매월 리포트로 드립니다.</p></div>\n  </div>\n</section>',
 '    <div class="card"><div class="num">06</div><h3>모니터링 리포트</h3><p>AI 답변 속 브랜드 언급과 검색 순위 변화를 매월 리포트로 드립니다.</p></div>\n  </div>\n  '
 + cap() + '\n  ' + LINK + '\n</section>'),
('pages/Website_Design.html',
 '    <div class="card"><div class="num">06</div><h3>유지보수</h3><p>오픈 후에도 콘텐츠 수정과 기능 업데이트를 지속적으로 지원합니다.</p></div>\n  </div>\n</section>',
 '    <div class="card"><div class="num">06</div><h3>유지보수</h3><p>오픈 후에도 콘텐츠 수정과 기능 업데이트를 지속적으로 지원합니다.</p></div>\n  </div>\n  '
 + cap() + '\n  ' + LINK + '\n</section>'),
]

n, miss = 0, []
def apply(path, old, new):
    global n
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    if old not in s:
        miss.append((path, old[:56])); return
    io.open(p,'w',encoding='utf-8').write(s.replace(old, new, 1)); n += 1

for a,b,c in LEADS: apply(a,b,c)
for a,b,c in TAILS: apply(a,b,c)

print('%d곳 적용' % n)
if miss:
    print('\n★ 못 찾음 %d건:' % len(miss))
    for a,b in miss: print('   %s\n     %s' % (a,b))
    sys.exit(1)
