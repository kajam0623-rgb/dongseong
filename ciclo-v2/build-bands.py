#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FAQ 금액 밴드 TODO 5칸 채우기 — 지어내지 않고 자사 공개값을 옮긴다.

출처는 이 저장소 안에 이미 있었다. `/dental` 랜딩(pages/치과_홈페이지_제작.html)의
패키지 표가 정상가·기간·페이지 수를 공개하고 있다:

  STANDARD 단일 페이지  정상가 150만원 (런칭가 70만원)  1페이지   2주  무상수정 2회
  DELUXE   얼리버드     정상가 200만원 (런칭가 90만원)  7페이지   3주  무상수정 3회
  PREMIUM  한정         정상가 320만원 (런칭가 150만원) 15페이지  4주  무상수정 5회
  유지비: 씨클로 월 이용료 0원 · 도메인+서버 실비 연 20~40만원 · 오픈 후 3개월 무상 점검

홈 FAQ 에는 **정상가**를 적는다. 사용자가 "선착순 특별가" 대신 "예산 밴드 공개"로
가기로 정했기 때문이다. 런칭가는 지우지 않고 한 줄로 안내하며 /dental 로 넘긴다
(캠페인 페이지의 실제 진행 중인 할인이라 임의로 없애지 않는다).

밴드 이름도 실제 패키지 구성에 맞춘다. 기존 초안(단일 페이지 정비 / 진료과목 분리 /
다지점·다국어)은 세 번째가 판매 중이 아닌 가상 상품이라 실제 PREMIUM 으로 교체한다.
"""
import sys, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages', 'Home.html')
s = io.open(P, encoding='utf-8').read()

def rep(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('FAIL: %d회 — %r' % (s.count(old), old[:80]))
    s = s.replace(old, new)

rep('''      <p>범위에 따라 세 구간입니다. 상담과 진단은 무료이고, 범위·일정·비용을 담은 제안서를 문의 후 보내드립니다.</p>
      <div class="bands">
        <div class="band"><span class="band-t">단일 페이지 정비 — 지금 사이트 위에서 기계용 정보와 태그를 채웁니다</span><span class="band-d">기간 <span class="band-todo">TODO</span></span><span class="band-p"><span class="band-todo">TODO</span></span></div>
        <div class="band"><span class="band-t">진료과목 분리 + 검색 구조 설계 — 페이지를 나누고 구조부터 다시 짭니다</span><span class="band-d">기간 <span class="band-todo">TODO</span></span><span class="band-p"><span class="band-todo">TODO</span></span></div>
        <div class="band"><span class="band-t">다지점·다국어 또는 콘텐츠 운영 포함</span><span class="band-d">기간 <span class="band-todo">TODO</span></span><span class="band-p">별도 협의</span></div>
      </div>
      <p>구간을 공개하는 이유는 단순합니다. 금액을 알려주지 않는 곳과 비교하실 때 기준이 있어야 하기 때문입니다.</p>''',
'''      <p>범위에 따라 세 구간입니다. 아래는 정상가이고, 상담과 진단은 무료입니다.</p>
      <div class="bands">
        <div class="band"><span class="band-t">STANDARD · 단일 페이지 — 진료·의료진·오시는길을 한 화면에, 검색 기본 세팅까지</span><span class="band-d">2주 · 1페이지 · 무상수정 2회</span><span class="band-p">150만원</span></div>
        <div class="band"><span class="band-t">DELUXE · 진료과목 분리 — 과목마다 주소를 나누고 구조화 데이터와 문답형 구조를 얹습니다</span><span class="band-d">3주 · 7페이지 · 무상수정 3회</span><span class="band-p">200만원</span></div>
        <div class="band"><span class="band-t">PREMIUM · 콘텐츠 구조까지 — 과목별 랜딩과 칼럼 주제 30개, 예약 폼 연동과 운영 교육</span><span class="band-d">4주 · 15페이지 · 무상수정 5회</span><span class="band-p">320만원</span></div>
      </div>
      <p>구간을 공개하는 이유는 단순합니다. 금액을 알려주지 않는 곳과 비교하실 때 기준이 있어야 하기 때문입니다. 범위·일정·비용을 담은 제안서는 문의 후에 보내드립니다.</p>
      <p><b>이후에 저희에게 나가는 월 이용료는 없습니다.</b> 도메인 연장비와 서버 사용료만 실비로 들고 규모에 따라 연 20~40만원 선인데, 이것도 병원 명의로 직접 결제하십니다. 오픈 후 3개월은 오류 수정과 색인 상태 점검을 무상으로 봅니다.</p>
      <p class="sec-caption" style="margin-top:14px">지금은 런칭 기념으로 선착순 열 팀까지 할인가가 적용되고 있습니다. 마감되면 위 정상가로 돌아갑니다. <a href="/dental/">치과 홈페이지 제작 페이지</a>에서 확인하실 수 있습니다.</p>''')

io.open(P, 'w', encoding='utf-8').write(s)
print('ok  pages/Home.html — band-todo %d개 남음' % s.count('band-todo'))
