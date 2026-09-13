# -*- coding: utf-8 -*-
"""서브페이지 4개(서비스) v2 전환 — h2 한글 문장형 · 리드 슬롯 · 인라인 font-size 제거"""
import sys
log=[]

COPY = {
 'Website_Design': {
   'incl_h2':  '기획부터 유지보수까지,<br>여섯 가지를 한 번에 맡습니다',
   'incl_lead':'나눠 맡기면 이음새에서 빠집니다. 디자인과 검색 기본기를 같은 단계에서 설계해야 나중에 다시 뜯을 일이 없습니다.',
   'how_h2':   '네 단계로 진행하고,<br>단계마다 확인받습니다',
   'for_h2':   '이런 상태라면,<br>지금이 고칠 때입니다',
 },
 'GEO': {
   'incl_h2':  'AI가 읽을 수 있게,<br>비어 있는 여섯 자리를 채웁니다',
   'incl_lead':'저희가 치과 여덟 곳을 채점했을 때 가장 낮게 나온 항목이 정확히 이 자리였습니다. 기계용 정보 표기 평균 20점, 30점을 넘긴 곳은 없었습니다.',
   'how_h2':   '진단부터 모니터링까지,<br>네 단계로 갑니다',
   'for_h2':   '검색은 되는데 AI 답변에<br>안 나온다면 이 작업입니다',
 },
 'Blog_Content': {
   'incl_h2':  '쓰는 일부터 발행까지,<br>여섯 가지를 대행합니다',
   'incl_lead':'전문성은 한 편으로 증명되지 않습니다. 검색 의도에 맞는 글이 쌓여야 신뢰가 됩니다.',
   'how_h2':   '키워드부터 리포트까지,<br>네 단계로 돌립니다',
   'for_h2':   '쓸 말은 있는데<br>쓸 시간이 없다면',
 },
 'Digital_Marketing': {
   'incl_h2':  '광고비를 늘리기 전에,<br>여섯 가지를 먼저 봅니다',
   'incl_lead':'검색 구조가 잡히지 않은 상태에서 광고비부터 올리면, 클릭은 늘어도 그 클릭이 도착하는 페이지가 여전히 읽히지 않습니다.',
   'how_h2':   '설계부터 리포트까지,<br>네 단계로 운영합니다',
   'for_h2':   '클릭은 나오는데<br>문의가 안 온다면',
 },
}

for name, c in COPY.items():
    p = f'pages/{name}.html'
    s = open(p, encoding='utf-8').read()
    def sub(old, new, why):
        nonlocal_s = None
        if s.count(old) != 1:
            print(f"[FAIL] {name}: {why} — 매칭 {s.count(old)}건"); sys.exit(1)
        log.append(f"{name}: {why}")
        return s.replace(old, new)

    # 1) /WHAT'S INCLUDED 에 h2 + 리드 신설 (원래 눈썹만 있고 주장이 없었다)
    s = sub('''  <div class="overline">/WHAT'S INCLUDED</div>
  <div class="grid-3">''',
f'''  <div class="overline">/WHAT'S INCLUDED</div>
  <h2 class="sec-h2">{c['incl_h2']}</h2>
  <p class="sec-lead">{c['incl_lead']}</p>
  <div class="grid-3" style="margin-top:clamp(32px,4vw,48px)">''',
 "WHAT'S INCLUDED 에 h2 + 리드 신설")

    # 2) 진행 순서 → 문장형 + 인라인 font-size 제거
    s = sub('<h2 class="sec-h2" style="font-size:clamp(30px,4vw,52px)">진행 순서</h2>',
            f'<h2 class="sec-h2">{c["how_h2"]}</h2>',
            "HOW IT WORKS h2 문장형 + 인라인 font-size 제거")

    # 3) 이런 분께 필요합니다 → 문장형 + 인라인 font-size 제거
    s = sub('<h2 class="sec-h2" style="font-size:clamp(30px,4vw,52px)">이런 분께 필요합니다</h2>',
            f'<h2 class="sec-h2">{c["for_h2"]}</h2>',
            "FOR YOU h2 문장형 + 인라인 font-size 제거")

    open(p, 'w', encoding='utf-8').write(s)

print(f"OK — {len(log)}건\n")
for w in log: print("  ", w)
