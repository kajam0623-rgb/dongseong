# -*- coding: utf-8 -*-
"""페이지 마크업 v2 — 섹션 h2 한글 문장형 전환 (플랜 A-2 / 패치 02)"""
import sys, shutil

def load(p): return open(p, encoding='utf-8').read()
def save(p,s): open(p,'w',encoding='utf-8').write(s)

log=[]
def sub(src, old, new, why):
    n = src.count(old)
    if n != 1:
        print(f"[FAIL] {why}\n  매칭 {n}건: {old[:90]!r}"); sys.exit(1)
    log.append(why)
    return src.replace(old, new)

# ── Home ────────────────────────────────────────────────────────
h = load('pages/Home.html')

h = sub(h, '<div class="overline">/SERVICES</div>',
           '<div class="overline">/SERVICES · WHAT WE DO</div>', "SERVICES 눈썹에 영문 h2 흡수")
h = sub(h, '<h2 class="sec-h2">What we do</h2>',
           '<h2 class="sec-h2">예쁘게 만드는 일과 검색되게 만드는 일을,<br>따로 맡기지 않으셔도 됩니다</h2>',
           "SERVICES h2 한글 문장형")

h = sub(h, '<div class="overline">/WORK</div>',
           '<div class="overline">/WORK · SELECTED WORK</div>', "WORK 눈썹")
h = sub(h, '<h2 class="sec-h2">Selected work</h2>',
           '<h2 class="sec-h2">치과 여덟 곳을 직접 채점하고,<br>고칠 자리를 숫자로 짚었습니다</h2>',
           "WORK h2 한글 문장형")

h = sub(h, '<div class="overline light">/PROCESS</div>',
           '<div class="overline light">/PROCESS · HOW WE WORK</div>', "PROCESS 눈썹")
h = sub(h, '<h2 class="sec-h2" style="color:#fff">How we work</h2>',
           '<h2 class="sec-h2" style="color:#fff">진단부터 성장까지,<br>한 팀이 네 단계로 책임집니다</h2>',
           "PROCESS h2 한글 문장형 (color:#fff 유지)")

h = sub(h, '<div class="overline">/ABOUT</div>',
           '<div class="overline">/ABOUT · CICLO</div>', "ABOUT 눈썹")
# ★ 인라인 font-size 가 CSS 를 이기므로 반드시 제거
h = sub(h, '<h2 class="sec-h2" style="font-size:clamp(40px,5vw,72px)">Ciclo</h2>',
           '<h2 class="sec-h2">예쁘기만 한 사이트가 아니라,<br>문의로 이어지는 사이트를 만듭니다</h2>',
           "ABOUT h2 한글 문장형 + 인라인 font-size 제거(CSS를 이기던 값)")

h = sub(h, '<div class="overline">/FAQ</div>',
           '<div class="overline">/FAQ · QUESTIONS</div>', "FAQ 눈썹")
h = sub(h, '<h2 class="sec-h2">Questions</h2>',
           '<h2 class="sec-h2">견적서를 받으셨을 때,<br>항목을 짚으실 수 있게 적었습니다</h2>',
           "FAQ h2 한글 문장형")

# ABOUT 본문 마지막 문장은 h2 로 승격됐으므로 중복 제거
old_body = '웹사이트 디자인부터 검색 노출(GEO), 블로그 콘텐츠, 광고 운영까지 — 한 팀이 처음부터 끝까지 책임집니다. 예쁘기만 한 사이트가 아니라, 문의로 이어지는 사이트를 만듭니다'
new_body = '웹사이트 디자인부터 검색 노출(GEO), 블로그 콘텐츠, 광고 운영까지 — 한 팀이 처음부터 끝까지 책임집니다'
if h.count(old_body) == 1:
    h = h.replace(old_body, new_body); log.append("ABOUT 본문 중복 문장 제거 (h2로 승격됨)")
else:
    print(f"[WARN] ABOUT 본문 중복 문장 매칭 {h.count(old_body)}건 — 수동 확인 필요")

save('pages/Home.html', h)

# ── Footer ──────────────────────────────────────────────────────
f = load('pages/CICLO_Footer.html')
f = sub(f, '<div class="overline light">/CONTACT</div>',
           "<div class=\"overline light\">/CONTACT · LET'S TALK</div>", "CONTACT 눈썹")
f = sub(f, '<h2>Let\'s talk<span style="opacity:.5">.</span></h2>',
           '<h2>무엇부터 손봐야 할지,<br>하루 안에 답을 드립니다</h2>', "푸터 h2 한글 문장형")
save('pages/CICLO_Footer.html', f)

print(f"OK — {len(log)}건 적용\n")
for i,w in enumerate(log,1): print(f"{i:2}. {w}")
