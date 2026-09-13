#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""About · Contact v2 전환 — 마지막 남은 두 페이지.

About 문제
  - .sec-h2 에 인라인 font-size 가 3곳 (64px / 52px). 전 페이지 40px 통일에서 이탈.
  - h2 "일하는 기준" 이 명사구. 238LAB 문법(수식구 + 동사구 ~합니다)에서 벗어남.
  - 분량이 2.2KB. 회사 소개인데 "무엇을 안 하는지"와 "판별 근거"가 없다.
    238LAB About 의 핵심은 자랑이 아니라 자사 한계·거절 기준 공개다.

Contact 문제
  - 프로세스 제목이 클래스 없는 <h2> 라 타이포 시스템 밖에 있다.
  - "무료 진단" 이라고만 하고 그 안에 무엇이 들어가는지 안 적혀 있다.
    홈 증거 밴드에서 열 항목·쉰 개 체크포인트를 공개했으므로 연결해야 말이 맞는다.

두 페이지 모두 사실이 아닌 것은 쓰지 않는다. 회사 법정정보(사업자등록번호·주소)는
알 수 없어 TODO 배지로 비워 둔다 — FAQ 금액 밴드와 같은 처리다.
"""
import sys, io, os

HERE = os.path.dirname(os.path.abspath(__file__))

def patch(path, pairs):
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit('FAIL %s: 앵커 %d회 — %r' % (path, n, old[:70]))
        s = s.replace(old, new)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('ok  %s' % path)

# ─────────────────────────── CSS ───────────────────────────
CSS = r"""
/* ── About / Contact 보강 ────────────────────────────────────────── */
/* 사명 풀이처럼 영문 한 줄이 주인공인 제목. 인라인 font-size 대신 이 클래스를 쓴다. */
.sec-h2.xl{font-size:clamp(34px,5vw,64px);line-height:1.05;letter-spacing:-.03em}
/* 안 하는 일 — 카드가 아니라 목록. 자랑이 아니므로 시각적 무게를 낮춘다. */
.dont{margin-top:clamp(32px,4vw,48px);display:grid;grid-template-columns:1fr 1fr;gap:0 clamp(28px,4vw,60px)}
.dont>div{padding:22px 0;border-top:1px solid rgba(18,18,18,.14)}
.dont h3{margin:0;font-size:17px;font-weight:700;letter-spacing:-.015em}
.dont p{margin:9px 0 0;font-size:15px;line-height:1.72;color:rgba(18,18,18,.66)}
.section.navy .dont>div{border-top-color:rgba(255,255,255,.2)}
.section.navy .dont p{color:rgba(255,255,255,.66)}
/* 회사 정보 — 채우기 전에는 눈에 띄어야 한다 */
.corp{margin-top:clamp(32px,4vw,48px);display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
  gap:0 clamp(28px,4vw,60px);max-width:760px}
.corp>div{display:flex;justify-content:space-between;gap:16px;padding:12px 0;
  border-bottom:1px solid rgba(18,18,18,.12);font-size:14.5px}
.corp dt{color:rgba(18,18,18,.55)}
.corp dd{margin:0;font-weight:700;text-align:right}
@media(max-width:700px){.dont,.corp{grid-template-columns:1fr}}
"""
ANCHOR = '@media(max-width:620px){.res-cards{grid-template-columns:1fr}.psi-vitals{grid-template-columns:repeat(3,1fr);gap:12px 8px}}\n'
patch('css/global.css', [(ANCHOR, ANCHOR + CSS)])

# ─────────────────────────── About ───────────────────────────
DONT = '''
<section class="section panel"><div class="wrap">
  <div class="overline">/WHAT WE DON'T DO · 하지 않는 일</div>
  <h2 class="sec-h2">할 수 있는 것보다,<br>하지 않는 것을 먼저 적습니다</h2>
  <p class="sec-lead">고를 때 필요한 건 잘한다는 말이 아니라 무엇을 안 하는지입니다. 아래 네 가지가 필요하시면 저희는 맞지 않습니다.</p>
  <div class="dont">
    <div>
      <h3>검색 순위를 보장하지 않습니다</h3>
      <p>순위는 검색엔진이 정하고 기준도 계속 바뀝니다. 저희가 약속할 수 있는 것은 읽히는 상태로 만들어 두는 것까지입니다. 1페이지를 보장한다는 말은 저희 쪽에서 나오지 않습니다.</p>
    </div>
    <div>
      <h3>환자 후기와 전후 사진을 쓰지 않습니다</h3>
      <p>치료 경험담과 치료 전후 비교 사진은 의료법이 막고 있습니다. 효과가 좋은 소재인 것은 알지만, 원장님 쪽에 남는 위험이라 제안 자체를 하지 않습니다. 갤러리는 시설·장비까지입니다.</p>
    </div>
    <div>
      <h3>진단 없이 새로 만들자고 하지 않습니다</h3>
      <p>먼저 지금 사이트를 채점합니다. 구조가 살아 있으면 고쳐 쓰는 편이 싸고 빠릅니다. 실제로 한 곳은 기계용 정보 표기 한 항목만 손봐서 AI 종합 점수가 32점에서 46점이 됐습니다. 새로 만들지 않았습니다.</p>
    </div>
    <div>
      <h3>설명할 수 없는 작업은 청구하지 않습니다</h3>
      <p>무엇을 왜 했는지 원장님이 다시 설명하실 수 있어야 합니다. 리포트에 쓰지 못할 작업은 하지 않고, 다른 업체로 옮기실 때 가져가실 수 있게 만듭니다.</p>
    </div>
  </div>
</div></section>
'''

RECORD = '''
<section class="section">
  <div class="overline">/RECORD · 공개해 둔 것</div>
  <h2 class="sec-h2">말로 하는 대신,<br>채점표를 먼저 공개했습니다</h2>
  <p class="sec-lead">에이전시를 고를 때 확인할 것은 포트폴리오 화면이 아니라 판단 기준입니다. 저희 기준은 전부 열려 있습니다.</p>
  <div class="fit-list">
    <div class="fit"><span class="arrow">→</span><p><b>채점 기준 쉰 개.</b> 열 항목마다 확인할 것을 다섯 개씩, 전부 있다·없다로만 답할 수 있게 정해 두고 공개했습니다. 다른 사람이 다시 재도 같은 점수가 나옵니다.</p></div>
    <div class="fit"><span class="arrow">→</span><p><b>치과 여덟 곳 실태조사.</b> 저희가 직접 채점한 결과를 익명 처리해서 숫자 그대로 열었습니다. 좋게 나온 곳도 나쁘게 나온 곳도 그대로 있습니다.</p></div>
    <div class="fit"><span class="arrow">→</span><p><b>맡은 사이트의 실측값.</b> 네이버 서치어드바이저와 PageSpeed Insights 화면에 찍힌 값입니다. 증가율이 커 보이는 곳은 시작점이 낮았다는 사실도 같이 적었습니다.</p></div>
    <div class="fit"><span class="arrow">→</span><p><b>못 하는 말도 적어 둡니다.</b> 표본이 여덟 곳이라 업계 전체를 대표하지 못한다는 것, 이 점수가 매출을 예측하지 않는다는 것을 조사 페이지에 그대로 써 뒀습니다.</p></div>
  </div>
  <a class="sec-link" href="/work/">실태조사 결과와 실적 전부 보기 →</a>

  <div class="overline dim" style="margin-top:clamp(56px,6vw,84px)">/COMPANY</div>
  <div class="corp">
    <div><dt>상호</dt><dd>씨클로 (CICLO)</dd></div>
    <div><dt>대표</dt><dd><span class="band-todo">TODO</span></dd></div>
    <div><dt>사업자등록번호</dt><dd><span class="band-todo">TODO</span></dd></div>
    <div><dt>소재지</dt><dd><span class="band-todo">TODO</span></dd></div>
    <div><dt>이메일</dt><dd>kajam0623@naver.com</dd></div>
    <div><dt>전화</dt><dd>010-8017-2001</dd></div>
  </div>
  <p class="sec-caption">사업자 정보를 적어두지 않은 에이전시는 거르셔도 됩니다. 저희 것도 확인하실 수 있게 적어 둡니다.</p>
</section>
'''

patch('pages/About.html', [
    # 히어로 리드 — 나열이 아니라 무엇을 책임지는지
    ('<p class="lead">씨클로는 병원·법률·전문직처럼 신뢰가 곧 매출인 분야의 디지털을 만드는 에이전시입니다. 디자인부터 검색, 콘텐츠, 광고까지 — 한 팀이 처음부터 끝까지 책임집니다.</p>',
     '<p class="lead">씨클로는 병원·법률·전문직처럼 신뢰가 곧 매출인 분야의 디지털을 만듭니다. 디자인부터 검색, 콘텐츠, 광고까지 한 팀이 맡고, 무엇을 왜 했는지 숫자로 남깁니다.</p>'),
    # 인라인 font-size 제거 → 클래스
    ('<h2 class="sec-h2" style="color:#fff;font-size:clamp(34px,5vw,64px);line-height:1.05">Creative Ideas, <br>Click Logic.</h2>',
     '<h2 class="sec-h2 xl" style="color:#fff">Creative Ideas, <br>Click Logic.</h2>'),
    # VALUES — 명사구 제목을 문장형으로, 리드 추가, 01 을 실측 근거로
    ('<h2 class="sec-h2" style="font-size:clamp(30px,4vw,52px)">일하는 기준</h2>\n  <div class="grid-3">',
     '<h2 class="sec-h2">일하는 기준을 셋으로 좁혔고,<br>나머지는 다 여기서 나옵니다</h2>\n'
     '  <p class="sec-lead">여러 개를 적으면 하나도 안 지키게 됩니다. 제안서를 쓸 때도 이 셋으로 먼저 걸러냅니다.</p>\n'
     '  <div class="grid-3" style="margin-top:clamp(32px,4vw,48px)">'),
    ('<div class="card"><div class="num">01</div><h3>증거로 말합니다</h3><p>"잘하고 있다"가 아니라 숫자와 리포트로 보여드립니다. 모든 작업은 측정 가능한 목표에서 시작합니다.</p></div>',
     '<div class="card"><div class="num">01</div><h3>증거로 말합니다</h3><p>"잘하고 있다"가 아니라 채점표로 보여드립니다. 치과 여덟 곳을 열 항목·쉰 개 체크포인트로 직접 재서 공개한 것도 같은 이유입니다. 재현되지 않는 숫자는 쓰지 않습니다.</p></div>'),
    # 마지막 섹션 뒤에 두 섹션 추가
    ('<div class="card"><div class="num">03</div><h3>전문 분야의 언어</h3><p>병원·법률처럼 규정과 톤이 중요한 분야의 문법을 이해하고, 신뢰를 해치지 않는 방식으로 알립니다.</p></div>\n  </div>\n</section>',
     '<div class="card"><div class="num">03</div><h3>전문 분야의 언어</h3><p>병원·법률처럼 규정과 톤이 중요한 분야의 문법을 이해하고, 신뢰를 해치지 않는 방식으로 알립니다. 의료광고 심의에 걸릴 표현은 초안 단계에서 걸러냅니다.</p></div>\n  </div>\n</section>\n'
     + DONT + RECORD),
])

# ─────────────────────────── Contact ───────────────────────────
PREP = '''
<section class="section panel"><div class="wrap">
  <div class="overline">/FREE CHECK · 무료 진단에 들어가는 것</div>
  <h2 class="sec-h2">무료라고 대충 보지 않습니다,<br>같은 쉰 개 항목으로 잽니다</h2>
  <p class="sec-lead">치과 여덟 곳을 채점할 때 쓴 기준을 그대로 씁니다. 계약 여부와 상관없이 점수와 근거를 드립니다.</p>
  <div class="grid-3" style="margin-top:clamp(32px,4vw,48px)">
    <div class="card"><div class="num">01</div><h3>열 항목 채점</h3><p>검색 기본기부터 기계가 읽는 정보 표기까지, 항목마다 다섯 개씩 쉰 개를 확인합니다. 있다·없다로만 답하는 항목이라 판단이 들어가지 않습니다.</p></div>
    <div class="card"><div class="num">02</div><h3>격차 표시</h3><p>검색 점수와 AI 답변 점수를 따로 냅니다. 여덟 곳 전부 AI 쪽이 낮았는데, 그 격차가 어디서 생기는지 항목으로 짚어 드립니다.</p></div>
    <div class="card"><div class="num">03</div><h3>고칠 순서</h3><p>전부 고치자고 하지 않습니다. 지금 사이트를 살릴 수 있는지, 어느 항목부터 손대면 점수가 움직이는지 순서로 드립니다.</p></div>
  </div>
  <p class="sec-caption">공개된 HTML 소스만 확인합니다. 관리자 계정이나 내부 자료를 요청하지 않습니다.</p>
</div></section>

<section class="section">
  <div class="overline">/BEFORE YOU WRITE · 미리 알려주시면</div>
  <h2 class="sec-h2">이 네 가지를 같이 주시면,<br>첫 답변이 훨씬 구체해집니다</h2>
  <p class="sec-lead">없어도 괜찮습니다. 주소 하나만 주셔도 진단은 시작됩니다.</p>
  <div class="fit-list">
    <div class="fit"><span class="arrow">→</span><p><b>지금 쓰시는 홈페이지 주소.</b> 이것만 있으면 저희가 먼저 채점해서 답장에 점수를 담아 드립니다.</p></div>
    <div class="fit"><span class="arrow">→</span><p><b>주력 진료과목 두세 개.</b> 전체를 고르게 올리는 것보다 어디를 먼저 올릴지가 순서를 정합니다.</p></div>
    <div class="fit"><span class="arrow">→</span><p><b>지금 하고 계신 광고나 블로그.</b> 이미 하고 계신 것과 겹치면 빼야 합니다. 중복해서 제안드리지 않으려고 여쭙습니다.</p></div>
    <div class="fit"><span class="arrow">→</span><p><b>목표 시점.</b> 개원일이나 이전 일정이 있으면 역산해서 일정을 짭니다.</p></div>
  </div>
  <p class="sec-caption">상담·진단은 무료이고, 진단 후 영업 연락은 드리지 않습니다. 평일 10:00–19:00 · 하루 안에 답변드립니다.</p>
</section>
'''

patch('pages/Contact.html', [
    ('<p class="lead">프로젝트 문의, 견적, 협업 제안 — 무엇이든 편하게 남겨주세요. 하루 안에 답변드립니다.</p>',
     '<p class="lead">지금 쓰시는 홈페이지 주소 하나만 주셔도 됩니다. 저희가 먼저 채점해서, 하루 안에 점수와 고칠 순서를 담아 답장드립니다.</p>'),
    # 타이포 시스템 밖에 있던 h2 를 편입
    ('<h2>문의 후 이렇게 진행됩니다</h2>',
     '<h2 class="sec-h2">문의 후 세 단계로 진행되고,<br>두 번째까지는 무료입니다</h2>'),
    ('<div class="cp-note">상담·견적은 무료입니다.<br>영업 연락은 드리지 않습니다.</div>\n    </div>\n  </div>\n</section>',
     '<div class="cp-note">상담·견적은 무료입니다. <br>영업 연락은 드리지 않습니다.</div>\n    </div>\n  </div>\n</section>\n' + PREP),
])
