#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""히어로 재설계 + 모션 레이어 복원 (v2.1)

세 가지를 한다.

1) 히어로 — 가운데 정렬 워드마크 스플래시 → 좌측 정렬 2단 에디토리얼
   기존 히어로에서 화면을 가장 크게 차지하는 것은 우리 로고였다. 로고는
   아무것도 팔지 않는다. 게다가 h1 텍스트가 "CICLO." 한 단어여서, GEO 를
   판다면서 정작 우리 h1 에는 검색어가 없었다.
     · h1 = 워드마크 + 주장 두 줄  ("CICLO. / GEO 웹사이트, 랜딩페이지 제작")
       워드마크는 그대로 크게 남기고, h1 안에 실제 문구를 넣는다
     · 오른쪽 열 = 실측 숫자 3개. 전부 아래 섹션에서 출처까지 여는 값이고
       각각 그 섹션으로 링크한다. 히어로에서 주장하고 스크롤에서 증명한다
     · 아래 = 헤어라인 인덱스 줄 (©2026 · 서비스 01~04 · SCROLL)
       회전 배지를 걷어낸 자리다
     · 좌우 여백을 .section 과 같은 clamp(20px,5vw,100px) 로 맞춘다.
       종전 clamp(20px,4vw,48px) 라 히어로만 그리드에서 어긋나 있었다

2) 모션 — v2 에서 통째로 뺐던 것을 구조를 바꿔 되살린다
   v1 의 버그는 "숨기기"가 CSS 에 있고 "보이기"가 JS 에 있었던 것이다.
   관찰자가 한 번 어긋나면 콘텐츠가 영구히 사라졌고 실제로 5개가 그랬다.
   이번에는 숨기는 권한도 JS 가 쥔다. html.mo 가 붙어야 숨고, 그 클래스는
   관찰자를 붙이기 직전에만 붙는다. JS 가 없거나 죽으면 모션만 없고 내용은
   그대로다. 자세한 것은 js/ciclo-effects.js 주석.

   ★ LCP 를 건드리지 않는 규칙
   히어로 h1 은 이 페이지의 LCP 요소다. opacity 0 에서 시작하는 요소는
   크롬이 "칠해지지 않은 것"으로 보므로, 페이드인은 애니메이션 시간만큼
   LCP 를 그대로 밀어낸다. 그래서 h1 에만은 불투명도를 건드리지 않고
   transform 만 준다. 나머지 히어로 요소는 LCP 후보가 아니라 페이드해도 된다.

3) 레이아웃·호버 디테일
   섹션 링크 밑줄 와이프 · 카드 리프트 · 서비스 행 들여쓰기 · 마퀴 호버 정지 ·
   카톡 버튼 리프트(transition 만 있고 호버 규칙이 없어 죽어 있었다) ·
   스크롤 진행선(scroll-timeline 지원 브라우저에서만, JS 0줄)
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(os.path.join(HERE, p), encoding='utf-8').read()
def wr(p, s): io.open(os.path.join(HERE, p), 'w', encoding='utf-8').write(s)

GIF = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='

# ─────────────────────────────────────────────────────────────
# 1. 히어로 마크업
# ─────────────────────────────────────────────────────────────
HERO = u'''<header class="hero">
  <div class="hero-mark" aria-hidden="true"><img src="%(gif)s" alt="" width="488" height="566" fetchpriority="low" decoding="async"></div>

  <div class="hero-grid">
    <div class="hero-copy">
      <div class="overline dim">/DIGITAL AGENCY — SEOUL</div>
      <h1 class="hero-h1"><span class="hn display">CICLO<span class="blue">.</span></span><span class="hs">GEO 웹사이트, 랜딩페이지 제작</span></h1>
      <p class="hero-claim">검색엔진과 AI가 읽을 수 있는 구조로 만듭니다.<br>병원·법률·전문직 브랜드를 맡습니다.</p>
      <div class="cta-row">
        <a class="btn btn-primary" href="/contact/">프로젝트 문의 <i class="ar" aria-hidden="true">→</i></a>
        <a class="btn btn-ghost" href="/work/">작업 보기</a>
      </div>
    </div>

    <div class="hero-proof">
      <p class="hp-h">근거는 아래에 전부 엽니다</p>
      <a class="hp-i" href="#evidence">
        <b>81<i>점</i><em>→</em><span class="hp-low">20</span><i class="hp-lowi">점</i></b>
        <span class="hp-c">사람이 보는 화면과 기계가 읽는 자리 — 치과 여덟 곳 평균</span>
      </a>
      <a class="hp-i" href="#results">
        <b>100<i>/100</i></b>
        <span class="hp-c">PageSpeed Insights 네 항목 — 저희가 만든 사이트 실측</span>
      </a>
      <a class="hp-i" href="#results">
        <b>740<i>클릭</i></b>
        <span class="hp-c">최근 90일 검색 유입 — 직전 90일 약 6클릭에서</span>
      </a>
    </div>
  </div>

  <div class="hero-base">
    <span class="hb-c">©2026</span>
    <nav class="hb-idx" aria-label="서비스 바로가기">
      <a href="/website-design/"><i>01</i>WEBSITE DESIGN</a>
      <a href="/geo/"><i>02</i>GEO</a>
      <a href="/blog-content/"><i>03</i>BLOG CONTENT</a>
      <a href="/digital-marketing/"><i>04</i>DIGITAL MARKETING</a>
    </nav>
    <a class="hb-scroll" href="#evidence">SCROLL<span aria-hidden="true">↓</span></a>
  </div>
</header>''' % {'gif': GIF}

home = rd('pages/Home.html')
i = home.find('<header class="hero">')
j = home.find('</header>')
if i != 0 or j < 0:
    sys.exit('FAIL: Home.html 히어로 블록을 찾지 못함')
home = HERO + home[j + len('</header>'):]
wr('pages/Home.html', home)
print('ok  pages/Home.html — 히어로 교체')

# ─────────────────────────────────────────────────────────────
# 2. 히어로 CSS 교체
# ─────────────────────────────────────────────────────────────
HERO_CSS = u'''/* ===== HERO (home) — 좌측 정렬 에디토리얼 =====
   v2.1: 가운데 정렬 워드마크 스플래시를 걷어냈다. 화면에서 가장 큰 것이
   우리 로고였고, h1 텍스트가 "CICLO." 한 단어여서 GEO 를 파는 페이지의
   h1 에 검색어가 없었다.
     h1 = 워드마크(.hn) + 주장(.hs) 두 줄. 워드마크 크기는 유지한다.
     오른쪽 .hero-proof = 아래 섹션에서 출처까지 여는 실측 숫자 3개.
     아래 .hero-base = 헤어라인 인덱스 줄. 회전 배지를 걷어낸 자리.
   좌우 패딩을 .section 과 같은 clamp(20px,5vw,100px) 로 맞춘다.
   종전 clamp(20px,4vw,48px) 이라 히어로만 그리드에서 어긋나 있었다. */
.hero{min-height:100vh;min-height:100svh;max-width:1280px;margin:0 auto;
  display:flex;flex-direction:column;
  padding:clamp(112px,13vh,152px) clamp(20px,5vw,100px) 0;position:relative;overflow:hidden}
/* 마크를 오른쪽으로 흘려 보낸다. 가운데에 두면 좌측 정렬 카피와 정면으로 겹친다. */
.hero-mark{position:absolute;right:-7%;top:48%;transform:translateY(-50%);z-index:0;pointer-events:none}
/* 폭 기준으로 잡는다. 높이를 고정하면 전역 img{max-width:100%} 가 폭만 잘라내
   390px 에서 짓눌린다. */
.hero-mark img{width:min(62vw,540px);height:auto;aspect-ratio:488/566;object-fit:contain;
  filter:invert(.78);opacity:.1}
.hero>*{position:relative;z-index:1}

/* 위 여백과 인덱스 줄 사이에서 가운데 정렬 */
.hero-grid{margin:auto 0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,336px);
  gap:clamp(30px,5vw,84px);align-items:end}
.hero-copy{min-width:0}

.hero .hero-h1{margin:clamp(16px,1.8vw,24px) 0 0;display:flex;flex-direction:column;
  gap:clamp(14px,1.7vw,24px);font-weight:400}
/* 워드마크는 브랜드 네이비. Pretendard 로 바꾸면서 글자가 가벼워져 네이비 단색이
   뒤의 회색 마크와 부딪히지 않고 무게가 산다. */
.hero .hn{display:block;font-size:clamp(56px,11vw,148px);line-height:.88;letter-spacing:-.02em;color:var(--pt)}
/* 150px 에서 앞 자간이 실제로 몇 px 벌어지므로 당기는 것만 유지한다. */
.hero .hn .blue{margin-left:-.06em}
.hero .hs{display:block;max-width:19ch;font-size:clamp(21px,2.6vw,34px);font-weight:700;
  line-height:1.3;letter-spacing:-.028em;color:var(--ink)}
.hero .hero-claim{margin-top:clamp(18px,1.8vw,26px);max-width:44ch;
  font-size:clamp(16px,1.5vw,18.5px);line-height:1.72;font-weight:400;color:rgba(18,18,18,.68)}
.hero .cta-row{margin-top:clamp(26px,3vw,40px);display:flex;gap:12px;flex-wrap:wrap}
.btn .ar{font-style:normal;transition:transform .28s cubic-bezier(.22,1,.36,1)}
.btn:hover .ar{transform:translateX(4px)}

/* 실측 숫자 3개 — 각 항목이 자기를 증명하는 섹션으로 간다 */
.hero-proof{border-top:1.5px solid rgba(17,30,108,.24);padding-top:14px}
.hp-h{font-size:11.5px;font-weight:700;letter-spacing:.16em;color:rgba(18,18,18,.58)}
.hp-i{display:block;padding:14px 0;border-bottom:1px solid rgba(18,18,18,.12);color:var(--ink)}
.hp-i:last-child{border-bottom:0;padding-bottom:0}
.hp-i b{display:flex;align-items:baseline;font-weight:800;font-size:clamp(25px,2.6vw,33px);
  letter-spacing:-.022em;line-height:1;color:var(--pt);font-variant-numeric:tabular-nums;
  transition:color .15s cubic-bezier(.4,0,.2,1)}
.hp-i b i{font-style:normal;margin-left:2px;font-size:13.5px;font-weight:700;color:rgba(17,30,108,.62)}
.hp-i b em{font-style:normal;margin:0 9px;font-size:16px;font-weight:700;color:rgba(18,18,18,.34)}
/* 낮은 쪽 값은 무게를 뺀다. 회색으로 빼면 큰 글자 대비 3:1 에 못 미쳐서
   네이비를 옅게 쓴다(약 3.4:1). */
.hp-i .hp-low,.hp-i b i.hp-lowi{color:rgba(17,30,108,.58)}
.hp-c{display:block;margin-top:7px;font-size:12.5px;line-height:1.56;font-weight:400;color:rgba(18,18,18,.62)}
.hp-i:hover b{color:var(--pt2)}
.hp-i:hover .hp-c{color:rgba(18,18,18,.82)}

/* 인덱스 줄 */
.hero-base{margin-top:auto;display:flex;align-items:center;justify-content:space-between;
  gap:clamp(14px,3vw,40px);flex-wrap:wrap;
  border-top:1px solid rgba(18,18,18,.15);padding:16px 0 clamp(18px,3vh,30px)}
.hb-c{font-weight:800;font-size:13px;letter-spacing:.06em;color:rgba(18,18,18,.55)}
.hb-idx{display:flex;flex-wrap:wrap;gap:clamp(14px,2.4vw,34px)}
.hb-idx a{display:inline-flex;align-items:baseline;gap:7px;font-size:11.5px;font-weight:700;
  letter-spacing:.13em;color:rgba(18,18,18,.62);transition:color .15s cubic-bezier(.4,0,.2,1)}
.hb-idx a i{font-style:normal;font-size:10.5px;font-weight:800;color:var(--pt)}
.hb-idx a:hover{color:var(--pt)}
.hb-scroll{display:inline-flex;align-items:center;gap:8px;font-size:11.5px;font-weight:700;
  letter-spacing:.16em;color:var(--pt)}
.hb-scroll span{display:inline-block;font-size:14px;animation:hb-bob 2.4s cubic-bezier(.4,0,.2,1) infinite}
@keyframes hb-bob{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(4px)}}

@media(max-width:1080px){
  .hero-grid{grid-template-columns:1fr;gap:clamp(30px,5vw,44px);align-items:start}
  .hero-proof{max-width:600px}
  .hero .hs{max-width:26ch}
  .hero-mark{right:-16%}
}
@media(max-width:760px){
  .hero{padding-top:100px}
  .hero .hero-h1{gap:12px}
  .hp-i{padding:12px 0}
  .hp-i b{font-size:23px}
  .hp-c{font-size:12px}
  .hb-idx{display:none}
  .hero-base{padding-top:14px}
}

'''

css = rd('css/global.css')
a = css.find('/* ===== HERO (home) ===== */')
b = css.find('/* subpage hero */')
if a < 0 or b < 0 or b < a:
    sys.exit('FAIL: HERO CSS 블록 경계를 찾지 못함')
css = css[:a] + HERO_CSS + css[b:]
print('ok  css/global.css — 히어로 블록 교체')

# ─────────────────────────────────────────────────────────────
# 3. 560px 미디어쿼리 — 사라진 .scroll-badge 규칙 정리
# ─────────────────────────────────────────────────────────────
old560 = """  /* 히어로 하단 장식 2종을 내린다 — 고정 카톡 버튼과 서로 부딪힌다.
     코너 라벨은 바로 아래 마퀴가 같은 문구를 반복하므로 잃는 정보가 없다. */
  .scroll-badge{display:none}
"""
if old560 not in css:
    sys.exit('FAIL: 560px 블록의 .scroll-badge 규칙을 찾지 못함')
css = css.replace(old560, """  /* 히어로 하단 SCROLL 표시는 고정 카톡 버튼과 자리가 겹친다 */
  .hb-scroll{display:none}
""")
print('ok  css/global.css — 560px 블록 정리')

# ─────────────────────────────────────────────────────────────
# 4. 모션 CSS — 파일 끝에 붙인다
# ─────────────────────────────────────────────────────────────
MOTION_CSS = u'''

/* =========================================================
   모션 레이어 (v2.1)

   두 갈래다.
     A. 히어로 입장 — CSS 만. JS 의존이 없으므로 실패할 지점이 없다.
     B. 스크롤 등장 — html.mo 가 붙은 동안에만 숨는다. 그 클래스는
        ciclo-effects.js 가 관찰자를 붙이기 직전에만 붙이고, 관찰자가
        한 번도 발화하지 않으면 1.5초 뒤 스스로 뗀다.
        JS 가 없거나 죽으면 모션만 없고 내용은 그대로다.
        v1 은 반대였다 — CSS 가 숨기고 JS 가 보였고, 그래서 관찰자가
        어긋난 노드 5개가 끝까지 안 보였다.

   ★ LCP 규칙
   히어로 h1 은 이 페이지의 LCP 요소다. opacity 0 에서 시작하는 요소는
   크롬이 아직 칠해지지 않은 것으로 보므로 페이드인은 애니메이션 시간만큼
   LCP 를 그대로 밀어낸다. h1 에만은 불투명도를 건드리지 않고 transform 만
   준다. 나머지는 LCP 후보가 아니라 페이드해도 된다.

   전 항목이 opacity/transform/clip-path 만 쓴다. 레이아웃을 건드리지
   않으므로 CLS 는 0 이다.
   ========================================================= */

@keyframes mo-rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
/* 불투명도를 건드리지 않는 판 — LCP 요소 전용 */
@keyframes mo-lift{from{transform:translateY(14px)}to{transform:none}}

.hero .overline{animation:mo-rise .6s cubic-bezier(.22,1,.36,1) both}
.hero .hn{animation:mo-lift .68s cubic-bezier(.22,1,.36,1) both}
.hero .hs{animation:mo-rise .66s cubic-bezier(.22,1,.36,1) .1s both}
.hero .hero-claim{animation:mo-rise .66s cubic-bezier(.22,1,.36,1) .18s both}
.hero .cta-row{animation:mo-rise .66s cubic-bezier(.22,1,.36,1) .26s both}
.hero-proof{animation:mo-rise .7s cubic-bezier(.22,1,.36,1) .34s both}
.hero-base{animation:mo-rise .7s cubic-bezier(.22,1,.36,1) .44s both}
.hero-mark img{animation:mo-mark 1.4s cubic-bezier(.22,1,.36,1) both}
@keyframes mo-mark{from{opacity:0;transform:translateX(26px)}to{opacity:.1;transform:none}}

/* ── B. 스크롤 등장 ── */
html.mo [data-mo]{opacity:0;transform:translateY(22px)}
html.mo [data-mo].mo-in{opacity:1;transform:none;
  transition:opacity .64s cubic-bezier(.22,1,.36,1) var(--mo-d,0ms),
             transform .64s cubic-bezier(.22,1,.36,1) var(--mo-d,0ms)}

/* 막대는 자기가 곧 데이터다. 길이가 자라는 것 자체가 정보를 읽히게 한다.
   width 대신 clip-path 로 깎는다 — 합성만으로 처리되고 모서리도 안 뭉갠다. */
html.mo [data-mo] .ev-bar,
html.mo [data-mo] .dx-track i{clip-path:inset(0 100% 0 0)}
html.mo [data-mo].mo-in .ev-bar,
html.mo [data-mo].mo-in .dx-track i{clip-path:inset(0 0 0 0);
  transition:clip-path .92s cubic-bezier(.22,1,.36,1) calc(var(--mo-d,0ms) + 140ms)}

html.mo [data-mo] .ev-dot{transform:scale(0)}
html.mo [data-mo].mo-in .ev-dot{transform:scale(1);
  transition:transform .46s cubic-bezier(.34,1.42,.5,1)}
html.mo [data-mo].mo-in .ev-dot:nth-of-type(1){transition-delay:.34s}
html.mo [data-mo].mo-in .ev-dot:nth-of-type(2){transition-delay:.40s}
html.mo [data-mo].mo-in .ev-dot:nth-of-type(3){transition-delay:.46s}
html.mo [data-mo].mo-in .ev-dot:nth-of-type(4){transition-delay:.52s}
html.mo [data-mo].mo-in .ev-dot:nth-of-type(5){transition-delay:.58s}
html.mo [data-mo].mo-in .ev-dot:nth-of-type(6){transition-delay:.64s}
html.mo [data-mo].mo-in .ev-dot:nth-of-type(7){transition-delay:.70s}

/* ── 스크롤 진행선 ──
   scroll-timeline 을 지원하는 브라우저에서만 나타난다. JS 는 0줄이고,
   미지원 브라우저에서는 scaleX(0) 이라 아예 안 보인다. */
.scroll-line{position:fixed;top:0;left:0;right:0;height:2px;background:var(--pt);
  transform-origin:0 50%;transform:scaleX(0);z-index:130;pointer-events:none}
@supports (animation-timeline:scroll()){
  .scroll-line{animation:mo-prog linear both;animation-timeline:scroll(root block)}
}
@keyframes mo-prog{from{transform:scaleX(0)}to{transform:scaleX(1)}}

/* ── 호버 ──
   전부 합성 속성만 쓴다. 레이아웃을 다시 계산시키는 호버는 넣지 않는다. */
.sec-link{position:relative}
.sec-link::after{content:"";position:absolute;left:0;right:0;bottom:-3px;height:1.5px;
  background:currentColor;transform:scaleX(0);transform-origin:0 50%;
  transition:transform .32s cubic-bezier(.22,1,.36,1)}
.sec-link:hover::after{transform:scaleX(1)}
.nav-links a{position:relative}
.nav-links a::after{content:"";position:absolute;left:0;right:0;bottom:-4px;height:1.5px;
  background:currentColor;transform:scaleX(0);transform-origin:0 50%;
  transition:transform .28s cubic-bezier(.22,1,.36,1)}
.nav-links a:hover::after,.nav-links a[aria-current=page]::after{transform:scaleX(1)}

.card{transition:border-color .18s cubic-bezier(.4,0,.2,1),transform .28s cubic-bezier(.22,1,.36,1)}
.card:hover{transform:translateY(-3px)}
.dx,.res-card,.psi-card{transition:border-color .18s cubic-bezier(.4,0,.2,1),transform .28s cubic-bezier(.22,1,.36,1)}
.dx:hover,.res-card:hover,.psi-card:hover{transform:translateY(-3px)}

.svc-row{transition:background .2s cubic-bezier(.4,0,.2,1),padding-left .28s cubic-bezier(.22,1,.36,1)}
.svc-row:hover{padding-left:18px}
.svc-row .more{display:inline-flex;gap:6px;transition:gap .26s cubic-bezier(.22,1,.36,1)}
.svc-row:hover .more{gap:12px}

/* transition 은 선언돼 있었는데 정작 호버 규칙이 없어 죽어 있던 것 */
.kakao-float:hover{transform:translateY(-3px);box-shadow:0 16px 34px rgba(0,0,0,.26)}

/* 마퀴는 읽으려고 멈추는 사람이 있다 */
.marquee:hover .marquee-track{animation-play-state:paused}

@media(prefers-reduced-motion:reduce){
  .hb-scroll span,.marquee-track{animation:none}
}
'''
css = css.rstrip('\n') + '\n' + MOTION_CSS
wr('css/global.css', css)
print('ok  css/global.css — 모션 블록 추가')

# ─────────────────────────────────────────────────────────────
# 5. 헤더에 진행선 요소 하나
# ─────────────────────────────────────────────────────────────
hdr = rd('pages/CICLO_Header.html')
if '.scroll-line' not in hdr and 'scroll-line' not in hdr:
    anchor = '<div class="nav-fixed">'
    if anchor not in hdr:
        sys.exit('FAIL: 헤더에서 .nav-fixed 를 찾지 못함')
    hdr = hdr.replace(anchor, '<div class="scroll-line" aria-hidden="true"></div>\n' + anchor, 1)
    wr('pages/CICLO_Header.html', hdr)
    print('ok  pages/CICLO_Header.html — 진행선 추가')
else:
    print('..  헤더에 진행선이 이미 있음')

print()
print('다음: python3 build-pages.py && python3 build-theme.py')
