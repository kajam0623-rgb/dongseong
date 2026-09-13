#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Work 페이지: 클라이언트 실적을 맨 앞으로.

기존 Work 는 "남의 사이트를 채점한 결과"만 있었다. 실측 캡처가 확보되면서
"우리가 맡은 뒤 움직인 숫자"를 먼저 놓고, 실태조사는 /SURVEY 로 뒤에 둔다.
(홈의 /RESULT 와 라벨이 겹치지 않게 실태조사 overline 을 SURVEY 로 바꾼다.)
"""
import sys, io

def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit('FAIL %s: 앵커 %d회 — %r' % (path, n, old[:70]))
        s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('ok  %s' % path)

PSI = '''  <div class="res-block">
    <div class="res-head">
      <h3>페이지 속도 — PageSpeed Insights 네 항목 100점</h3>
      <span class="res-src">치과 ④ 모바일 측정 · 치과 ⑤ 데스크톱 측정</span>
    </div>
    <div class="psi-cards">
      <article class="psi-card">
        <div class="res-top"><span class="res-id">치과 ④</span><span class="res-tag">모바일 측정</span></div>
        <div class="psi-scores">
          <div class="psi-s"><div class="psi-ring">100</div><small>성능</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>접근성</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>권장사항</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>검색<br>엔진 최적화</small></div>
        </div>
        <div class="psi-vitals">
          <div class="psi-v"><b>1.0초</b><small>첫 콘텐츠</small></div>
          <div class="psi-v"><b>1.7초</b><small>최대 콘텐츠</small></div>
          <div class="psi-v"><b>0ms</b><small>차단 시간</small></div>
          <div class="psi-v"><b>0.003</b><small>레이아웃 이동</small></div>
          <div class="psi-v"><b>1.8초</b><small>속도 지수</small></div>
        </div>
      </article>
      <article class="psi-card">
        <div class="res-top"><span class="res-id">치과 ⑤</span><span class="res-tag">데스크톱 측정</span></div>
        <div class="psi-scores">
          <div class="psi-s"><div class="psi-ring">100</div><small>성능</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>접근성</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>권장사항</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>검색<br>엔진 최적화</small></div>
        </div>
        <div class="psi-vitals">
          <div class="psi-v"><b>0.4초</b><small>첫 콘텐츠</small></div>
          <div class="psi-v"><b>0.6초</b><small>최대 콘텐츠</small></div>
          <div class="psi-v"><b>10ms</b><small>차단 시간</small></div>
          <div class="psi-v"><b>0.006</b><small>레이아웃 이동</small></div>
          <div class="psi-v"><b>0.6초</b><small>속도 지수</small></div>
        </div>
      </article>
    </div>
    <p class="sec-caption">모바일 측정은 느린 4G · 저사양 기기 조건이라 데스크톱보다 낮게 나오는 것이 정상입니다. 네 항목 100점은 빠르다는 뜻이고, 검색 순위를 보장하는 값이 아닙니다.</p>
  </div>
'''

BLOCK = '''<section class="section" style="padding-top:clamp(48px,6vw,80px)">
  <div class="overline">/RESULT · 저희가 맡은 사이트</div>
  <h2 class="sec-h2">맡은 뒤 숫자가 어디로 갔는지,<br>도구 화면에 찍힌 값으로 엽니다</h2>
  <p class="sec-lead">네이버 서치어드바이저와 PageSpeed Insights가 매긴 값입니다. 저희가 계산하거나 보정한 수치가 아닙니다. 병원명·주소·도메인은 가렸습니다.</p>

  <div class="dtable-wrap">
    <table class="dtable">
      <caption class="sr-only">저희가 맡은 치과 사이트의 최근 90일 검색 유입</caption>
      <thead>
        <tr>
          <th scope="col">병원</th><th scope="col">특징</th>
          <th scope="col">클릭</th><th scope="col">노출</th><th scope="col">클릭률</th><th scope="col">직전 90일 클릭</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>①</td><td>수도권 · 종합진료</td><td>740</td><td>6.4만</td><td>1.2%</td><td>약 6</td></tr>
        <tr><td>②</td><td>인천 · 사랑니 중심</td><td>110</td><td>1.9만</td><td>0.6%</td><td>약 6</td></tr>
        <tr><td>③</td><td>수도권 · 개원 초기</td><td>74</td><td>1.4만</td><td>0.5%</td><td>약 1</td></tr>
      </tbody>
    </table>
  </div>
  <p class="dtable-hint">← 표를 옆으로 밀어 보세요</p>
  <p class="res-note">증가율로 쓰면 +12,300% · +1,733% · +7,300% 입니다. 크게 보이지만 <b>세 곳 모두 시작점이 한 자리 클릭이었습니다.</b> 그래서 배수 대신 직전 90일 클릭을 같은 표에 넣었습니다. 클릭률 0.5~1.2%도 업계 평균을 넘는 값이 아닙니다. 이 표는 없던 유입이 생겼다는 사실까지만 말하고, 매출이나 내원 건수는 말하지 않습니다.</p>

''' + PSI + '''</section>

'''

patch('pages/Work.html', [
    # 히어로 리드: 실적이 생겼으므로 "공개할 작업이 없다"는 문장을 고친다
    ('<p class="lead">아직 공개할 수 있는 클라이언트 작업이 많지 않습니다. 대신 저희가 직접 한 일을 먼저 공개합니다. 치과 홈페이지 여덟 곳을 열 항목·쉰 개 체크포인트로 채점했고, 결과를 숫자 그대로 엽니다.</p>\n  <div class="chips"><span class="chip">표본 8곳</span><span class="chip">10항목 50체크포인트</span><span class="chip">2026년 8월</span></div>',
     '<p class="lead">화면 캡처 대신 숫자를 먼저 놓습니다. 저희가 맡은 사이트에서 도구가 매긴 값, 그리고 저희가 직접 채점한 치과 여덟 곳의 실태조사 결과입니다. 둘 다 근거와 한계를 같이 적었습니다.</p>\n  <div class="chips"><span class="chip">클라이언트 5곳 실측</span><span class="chip">실태조사 표본 8곳</span><span class="chip">10항목 50체크포인트</span></div>'),
    # 실적 블록 삽입 + 실태조사 라벨 변경
    ('<section class="section" style="padding-top:0">\n  <div class="overline">/RESULT · 여덟 곳 전체</div>',
     BLOCK + '<section class="section panel"><div class="wrap">\n  <div class="overline">/SURVEY · 치과 여덟 곳 실태조사</div>'),
    # 실태조사 섹션 닫는 태그를 panel 래퍼에 맞춘다
    ('  <a class="sec-link" href="https://dental-seo-report.vercel.app/" target="_blank" rel="noopener">채점 기준 쉰 개와 전체 리포트 보기 →</a>\n</section>',
     '  <a class="sec-link" href="https://dental-seo-report.vercel.app/" target="_blank" rel="noopener">채점 기준 쉰 개와 전체 리포트 보기 →</a>\n</div></section>'),
    # 방법론 섹션은 panel 이 연달아 오지 않게 일반 섹션으로
    ('<section class="section panel"><div class="wrap">\n  <div class="overline">/METHOD · 어떻게 쟀나</div>',
     '<section class="section">\n  <div class="overline">/METHOD · 어떻게 쟀나</div>'),
    ('  </div>\n</div></section>\n\n<section class="section">\n  <div class="overline">/LIMITS · 말하지 못하는 것</div>',
     '  </div>\n</section>\n\n<section class="section panel"><div class="wrap">\n  <div class="overline">/LIMITS · 말하지 못하는 것</div>'),
    ('<div class="fit"><span class="arrow">→</span><p>표본이 스무 곳을 넘으면 기준을 다시 맞추고 이 표도 갱신합니다.</p></div>\n  </div>\n</section>',
     '<div class="fit"><span class="arrow">→</span><p>표본이 스무 곳을 넘으면 기준을 다시 맞추고 이 표도 갱신합니다.</p></div>\n    <div class="fit"><span class="arrow">→</span><p>위 실적 표의 세 곳도 표본입니다. 같은 작업을 해도 지역·경쟁 상황에 따라 다르게 나옵니다. 같은 결과를 약속드리지 않습니다.</p></div>\n  </div>\n</div></section>'),
])
