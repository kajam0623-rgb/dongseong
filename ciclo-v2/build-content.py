# -*- coding: utf-8 -*-
"""Why now 섹션 · FAQ 확장 · 섹션 리드 슬롯 (플랜 5·6·9·10번)"""
import sys
p='pages/Home.html'; s=open(p,encoding='utf-8').read(); log=[]
def sub(old,new,why):
    global s
    if s.count(old)!=1:
        print(f"[FAIL] {why} — 매칭 {s.count(old)}건"); sys.exit(1)
    s=s.replace(old,new); log.append(why)

# ── 1) 서비스 리드 ──────────────────────────────────────────────
sub('''  <h2 class="sec-h2">예쁘게 만드는 일과 검색되게 만드는 일을,<br>따로 맡기지 않으셔도 됩니다</h2>
  <div class="svc-list">''',
'''  <h2 class="sec-h2">예쁘게 만드는 일과 검색되게 만드는 일을,<br>따로 맡기지 않으셔도 됩니다</h2>
  <p class="sec-lead">나눠 맡기면 각자 자기 영역만 최적화합니다. 디자인 업체는 화면을, 광고 업체는 클릭 단가를 봅니다. 그 사이에서 검색엔진과 AI가 이 페이지를 읽을 수 있는지는 아무도 보지 않습니다.</p>
  <div class="svc-list">''',
 "서비스 섹션 리드 추가")

# ── 2) 프로세스 리드 ────────────────────────────────────────────
sub('''  <h2 class="sec-h2" style="color:#fff">진단부터 성장까지,<br>한 팀이 네 단계로 책임집니다</h2>
  <div class="grid-4"''',
'''  <h2 class="sec-h2" style="color:#fff">진단부터 성장까지,<br>한 팀이 네 단계로 책임집니다</h2>
  <p class="sec-lead">순서가 있습니다. 진단 없이 제작부터 시작하면 두 번 만들게 됩니다. 상담과 진단은 무료입니다.</p>
  <div class="grid-4"''',
 "프로세스 섹션 리드 추가")

# ── 3) Why now 논증 섹션 신설 (About 앞) ────────────────────────
sub('<section class="section" id="about">',
'''<section class="section" id="why">
  <div class="overline">/WHY NOW · 지금인 이유</div>
  <h2 class="sec-h2">검색은 이미 갈렸고,<br>AI 답변은 아직 갈리지 않았습니다</h2>
  <p class="sec-lead">저희가 채점한 여덟 곳에서 나온 세 가지입니다. 업계 전망이 아니라 실측값이라 확인하실 수 있습니다.</p>

  <div class="grid-3" style="margin-top:clamp(40px,5vw,64px)">
    <div class="step">
      <div class="num">01</div>
      <div class="t">아직 아무도 손대지 않았습니다</div>
      <p>기계용 정보 표기 항목에서 30점을 넘긴 곳이 한 곳도 없었습니다. SEO 종합 84점으로 가장 잘 만든 곳도 이 항목만은 28점이었습니다. 잘하는 집과 못하는 집이 갈리는 항목이 아닙니다.</p>
      <div class="stat">0<small>일곱 곳 중 30점을 넘긴 병원 수</small></div>
    </div>
    <div class="step">
      <div class="num">02</div>
      <div class="t">검색은 벌어졌고 AI는 몰려 있습니다</div>
      <p>검색 점수는 39점에서 84점까지 45점 폭으로 벌어졌습니다. 그런데 AI 답변 점수는 31점에서 56점, 25점 폭 안에 몰려 있었습니다. 검색은 이미 승부가 났고 AI는 아직 출발선입니다.</p>
      <div class="stat">45 : 25<small>검색 점수 분포 폭 대 AI 점수 분포 폭</small></div>
    </div>
    <div class="step">
      <div class="num">03</div>
      <div class="t">한 항목만 고쳐도 움직입니다</div>
      <p>한 곳에서 기계용 정보 표기만 15점에서 78점으로 올렸습니다. 다른 항목은 거의 건드리지 않았는데 AI 종합이 32점에서 46점이 됐습니다. 사이트를 새로 만들지 않고 나온 결과입니다.</p>
      <div class="stat">32 → 46<small>구조화 데이터만 고친 뒤 AI 종합 점수</small></div>
    </div>
  </div>

  <p class="sec-caption">2026년 8월 측정 · 표본 8곳 · 열 항목 쉰 개 체크포인트 · 공개된 HTML 소스만 확인 · 이 점수는 검색 순위나 매출을 예측하지 않습니다</p>
  <a class="sec-link" href="https://dental-seo-report.vercel.app/" target="_blank" rel="noopener">채점 기준과 여덟 곳 결과 전부 보기 →</a>
</section>

<section class="section" id="about">''',
 "Why now 논증 섹션 신설 (씨클로 자체 데이터 3건 + 출처 캡션)")

# ── 4) FAQ 리드 + 7문항 확장 ────────────────────────────────────
sub('''  <h2 class="sec-h2">견적서를 받으셨을 때,<br>항목을 짚으실 수 있게 적었습니다</h2>
  <div class="faq">''',
'''  <h2 class="sec-h2">견적서를 받으셨을 때,<br>항목을 짚으실 수 있게 적었습니다</h2>
  <p class="sec-lead">보장할 수 없는 것은 보장할 수 없다고 씁니다. 저희가 겪은 것도 같이 적었습니다.</p>
  <div class="faq">''',
 "FAQ 섹션 리드 추가")

OLD_FAQ_START = '    <div class="faq-row"><h3>씨클로는 어떤 회사인가요?</h3><p>씨클로(CICLO)는 병원·법률·전문직처럼 신뢰가 곧 매출인 분야의 디지털을 만드는 에이전시입니다. 웹사이트 디자인부터 GEO, 블로그 콘텐츠, 디지털 마케팅까지 한 팀이 처음부터 끝까지 책임집니다.</p></div>'
NEW_FAQ = '''    <div class="faq-row"><h3>씨클로는 어떤 회사인가요?</h3><div class="faq-a">
      <p>병원·법률·전문직처럼 신뢰가 곧 매출인 분야의 디지털을 만듭니다. 웹사이트 디자인, GEO, 블로그 콘텐츠, 광고 운영을 한 팀이 맡습니다.</p>
      <p>한 팀으로 가는 이유가 있습니다. 나눠 맡기면 각자 자기 영역만 최적화합니다. 디자인 업체는 화면을, 광고 업체는 클릭 단가를 봅니다. 그 사이에서 &ldquo;검색엔진과 AI가 이 페이지를 읽을 수 있는가&rdquo;는 아무도 보지 않습니다. 저희가 치과 여덟 곳을 채점했을 때 가장 낮게 나온 항목이 정확히 그 자리였습니다.</p>
    </div></div>'''
sub(OLD_FAQ_START, NEW_FAQ, "FAQ 1 밀도 상향")

sub('    <div class="faq-row"><h3>GEO(생성형 검색 최적화)가 무엇인가요?</h3><p>ChatGPT·Gemini·네이버 AI 같은 생성형 검색이 답변할 때 브랜드를 먼저 추천하도록 콘텐츠와 사이트 구조, 구조화 데이터를 최적화하는 작업입니다. SEO가 검색 순위라면, GEO는 AI 답변 안에 인용되도록 만드는 전략입니다.</p></div>',
'''    <div class="faq-row"><h3>GEO(생성형 검색 최적화)가 무엇인가요?</h3><div class="faq-a">
      <p>ChatGPT·Gemini·네이버 AI가 답변할 때 인용되도록 만드는 작업입니다. SEO가 검색 순위라면 GEO는 AI 답변 안에 들어가는 것입니다.</p>
      <p>다만 둘은 분리된 기술이 아닙니다. AI는 검색 지면에서 만들어진 데이터를 근거로 답을 씁니다. SEO 기반이 없는 상태에서 GEO만 따로 하는 건 성립하지 않습니다.</p>
      <p>지금은 격차가 크지 않습니다. 저희 조사에서 검색 점수는 39점에서 84점까지 벌어졌는데, AI 점수는 31점에서 56점 사이에 몰려 있었습니다. 검색은 신경 쓴 곳과 안 쓴 곳이 갈렸고, AI는 아직 다 같이 낮습니다.</p>
    </div></div>''',
 "FAQ 2 밀도 상향")

sub('    <div class="faq-row"><h3>웹사이트 제작 기간과 비용은 어떻게 되나요?</h3><p>프로젝트 범위에 따라 다릅니다. 상담과 진단은 무료이며, 범위·일정·비용을 담은 제안서를 문의 후 보내드립니다. 카카오톡·메일·전화로 편하게 문의해 주세요.</p></div>',
'''    <div class="faq-row"><h3>제작 기간과 비용은 어떻게 되나요?</h3><div class="faq-a">
      <p>범위에 따라 세 구간입니다. 상담과 진단은 무료이고, 범위·일정·비용을 담은 제안서를 문의 후 보내드립니다.</p>
      <div class="bands">
        <div class="band"><span class="band-t">단일 페이지 정비 — 지금 사이트 위에서 기계용 정보와 태그를 채웁니다</span><span class="band-d">기간 <span class="band-todo">TODO</span></span><span class="band-p"><span class="band-todo">TODO</span></span></div>
        <div class="band"><span class="band-t">진료과목 분리 + 검색 구조 설계 — 페이지를 나누고 구조부터 다시 짭니다</span><span class="band-d">기간 <span class="band-todo">TODO</span></span><span class="band-p"><span class="band-todo">TODO</span></span></div>
        <div class="band"><span class="band-t">다지점·다국어 또는 콘텐츠 운영 포함</span><span class="band-d">기간 <span class="band-todo">TODO</span></span><span class="band-p">별도 협의</span></div>
      </div>
      <p>구간을 공개하는 이유는 단순합니다. 금액을 알려주지 않는 곳과 비교하실 때 기준이 있어야 하기 때문입니다.</p>
    </div></div>''',
 "FAQ 3 → 기간·예산 밴드 (금액은 TODO 플레이스홀더)")

sub('    <div class="faq-row"><h3>병원·법률 등 규정이 까다로운 분야도 가능한가요?</h3><p>네. 의료광고·법률광고처럼 규정과 톤이 중요한 전문 분야의 문법을 이해하고, 신뢰를 해치지 않는 방식으로 콘텐츠와 마케팅을 진행합니다.</p></div>',
'''    <div class="faq-row"><h3>노출 성과를 보장해 주시나요?</h3><div class="faq-a">
      <p>아니요. 보장한다는 표현은 쓰지 않습니다.</p>
      <p>검색 순위는 경쟁 상황과 콘텐츠 축적에 따라 달라지고, 알고리즘은 공개돼 있지 않습니다. 저희가 채점한 열 항목도 읽을 수 있는 상태인지를 잰 것이지 순위를 예측하는 값이 아닙니다.</p>
      <p>대신 착수 전에 목표를 숫자로 합의하고 계약서에 적습니다. 색인률이나 구조화 데이터 점수처럼 나중에 직접 확인하실 수 있는 항목으로만 잡습니다.</p>
      <p>&ldquo;몇 위 보장&rdquo;을 말하는 곳은 한 번 더 확인해 보시길 권합니다. 순위를 보장하려면 알고리즘을 알아야 하는데, 아는 사람은 없습니다.</p>
    </div></div>

    <div class="faq-row"><h3>지금 홈페이지를 새로 만들어야 하나요?</h3><div class="faq-a">
      <p>대부분은 아닙니다.</p>
      <p>저희가 채점한 여덟 곳 중 디자인이 문제였던 곳은 없었습니다. 점수가 낮게 나온 곳도 화면은 대부분 좋았습니다. 무너진 자리는 기계가 읽는 층이었고, 그건 대개 지금 사이트 위에서 고칠 수 있습니다.</p>
      <p>다시 만들지 여부를 가르는 건 사이트 구조 한 항목입니다. 진료과목이 각각 주소를 갖고 있으면 고쳐 쓰는 쪽이 빠르고, 전부 한 페이지에 얹혀 있으면 새로 만드는 편이 결국 쌉니다.</p>
      <p>진단은 무료입니다. 고쳐 쓸 수 있는데 새로 만들자고 하지는 않습니다.</p>
    </div></div>

    <div class="faq-row"><h3>병원·법률 등 규정이 까다로운 분야도 가능한가요?</h3><div class="faq-a">
      <p>네. 의료광고·법률광고의 문법을 전제로 씁니다.</p>
      <p>치료 전후 비교 사진, 환자 후기, 효과 보장 문구는 애초에 만들지 않습니다. 심의 대상인지를 먼저 가르고, 규정을 피해 가는 게 아니라 규정 안에서 신뢰가 보이도록 씁니다.</p>
    </div></div>''',
 "FAQ 4·5 신설(보장 안 함 / 새로 만들 필요 없음) + 규정 문항 밀도 상향")

sub('    <div class="faq-row"><h3>웹사이트만 제작하고 마케팅은 따로 맡길 수 있나요?</h3><p>가능합니다. 각 서비스를 개별로도, 통합으로도 진행합니다. 다만 한 팀이 전 과정을 맡을 때 메시지가 일관되고 성과가 더 잘 이어집니다.</p></div>',
'''    <div class="faq-row"><h3>웹사이트만 제작하고 마케팅은 따로 맡길 수 있나요?</h3><div class="faq-a">
      <p>가능합니다. 각 서비스를 개별로도 진행합니다.</p>
      <p>다만 순서는 말씀드립니다. 검색 구조가 잡히지 않은 상태에서 광고비부터 올리면, 클릭은 늘어도 그 클릭이 도착하는 페이지가 여전히 읽히지 않습니다. 저희가 채점한 곳들에서 가장 흔했던 순서 착오가 그것이었습니다.</p>
    </div></div>''',
 "FAQ 7 밀도 상향")

open(p,'w',encoding='utf-8').write(s)
print(f"OK — {len(log)}건, Home.html {len(s):,} chars\n")
for i,w in enumerate(log,1): print(f"{i}. {w}")
