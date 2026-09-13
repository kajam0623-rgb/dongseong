# -*- coding: utf-8 -*-
"""헤더·사이드바 접근성/디테일 업그레이드 (플랜 5번)"""
import sys
log=[]
def sub(s, old, new, why):
    if s.count(old)!=1:
        print(f"[FAIL] {why} — 매칭 {s.count(old)}건"); sys.exit(1)
    log.append(why); return s.replace(old,new)

# ── CSS ─────────────────────────────────────────────────────────
p='css/global.css'; c=open(p,encoding='utf-8').read()

# 사이드바: 닫혀 있을 때 포커스·스크린리더에서 제외
c = sub(c, """.sidebar{position:fixed;top:0;right:0;bottom:0;width:min(380px,88vw);background:var(--pt);color:#fff;z-index:120;
  transform:translateX(105%);transition:transform .38s cubic-bezier(.16,1,.3,1);display:flex;flex-direction:column;padding:28px 32px 32px;overflow-y:auto}
.sidebar.open{transform:translateX(0)}""",
""".sidebar{position:fixed;top:0;right:0;bottom:0;width:min(380px,88vw);background:var(--pt);color:#fff;z-index:120;
  transform:translateX(105%);display:flex;flex-direction:column;padding:28px 32px 32px;overflow-y:auto;
  /* 닫힌 동안에는 visibility:hidden 으로 탭 순서와 스크린리더에서 뺀다.
     transform 만으로 밀어두면 화면 밖 링크 9개가 그대로 포커스를 받는다. */
  visibility:hidden;transition:transform .38s cubic-bezier(.16,1,.3,1),visibility 0s linear .38s}
.sidebar.open{transform:translateX(0);visibility:visible;
  transition:transform .38s cubic-bezier(.16,1,.3,1),visibility 0s linear 0s}
/* 사이드바가 열린 동안 본문 스크롤 잠금 */
body.nav-open{overflow:hidden}""",
"사이드바 닫힘 상태를 탭 순서·스크린리더에서 제외 + 본문 스크롤 잠금")

# 앵커 점프가 고정 내비에 가리지 않게
c = sub(c, "/* ===== NAV ===== */",
"""/* 고정 내비(top:16px + 높이 52px)가 앵커 대상을 가리지 않게.
   이게 없으면 Services 를 눌렀을 때 h2 가 내비 뒤에 숨는다. */
section[id],header[id],footer[id]{scroll-margin-top:96px}

/* 키보드 포커스 가시성 — 어두운 면에서는 옐로로 */
a:focus-visible,button:focus-visible{outline:2px solid var(--pt);outline-offset:3px;border-radius:2px}
.section.navy a:focus-visible,.section.navy button:focus-visible,
.footer a:focus-visible,.sidebar a:focus-visible,.sidebar button:focus-visible,
.nav a:focus-visible,.nav button:focus-visible{outline-color:var(--kakao)}

/* 본문 바로가기 */
.skip{position:absolute;left:-9999px;top:0;z-index:200;background:var(--pt);color:#fff;
  padding:12px 18px;font-size:14px;font-weight:700;border-radius:0 0 4px 0}
.skip:focus{left:0;color:#fff}

/* 현재 페이지 표시 */
.nav-links a[aria-current="page"]{color:#fff}
.nav-links a[aria-current="page"]::after{content:"";display:block;height:2px;background:var(--kakao);margin-top:3px}
.sidebar-menu a[aria-current="page"]{padding-left:6px}
.sidebar-menu a[aria-current="page"] .lab{color:var(--kakao)}

/* ===== NAV ===== */""",
"scroll-margin-top 96px · 포커스 링 · 스킵 링크 · 현재 페이지 표시")

# 사이드바 메뉴 그룹 라벨 + 인라인 font-size 를 클래스로
c = sub(c, ".sidebar-menu .lab{font-family:Archivo,sans-serif;font-weight:800;letter-spacing:-.01em;text-transform:uppercase}",
""".sidebar-menu .lab{font-family:Archivo,'Arial Black',sans-serif;font-weight:800;letter-spacing:-.01em;text-transform:uppercase;font-size:24px}
.sidebar-menu .lab-sub{font-size:19px}
/* 메뉴 그룹 라벨 — 238LAB 처럼 페이지와 서비스를 나눈다 */
.sidebar-group{margin-top:24px;margin-bottom:2px;font-family:Archivo,sans-serif;font-size:11px;
  font-weight:700;letter-spacing:.2em;color:rgba(255,255,255,.38)}""",
"사이드바 lab 크기를 클래스로 + 그룹 라벨 스타일")

open(p,'w',encoding='utf-8').write(c)

# ── 헤더 마크업 ─────────────────────────────────────────────────
p='pages/CICLO_Header.html'; h=open(p,encoding='utf-8').read()

h = sub(h, '<div class="nav-fixed"><nav class="nav">',
        '<a class="skip" href="#content">본문 바로가기</a>\n<div class="nav-fixed"><nav class="nav" aria-label="주 메뉴">',
        "스킵 링크 + nav aria-label")
h = sub(h, '<button class="nav-burger" aria-label="메뉴"><span></span><span></span></button>',
        '<button class="nav-burger" type="button" aria-label="메뉴 열기" aria-expanded="false" aria-controls="ciclo-sidebar"><span></span><span></span></button>',
        "버거에 aria-expanded / aria-controls / type")
h = sub(h, '<div class="scrim"></div>\n<aside class="sidebar">',
        '<div class="scrim" hidden></div>\n<aside class="sidebar" id="ciclo-sidebar" role="dialog" aria-modal="true" aria-label="사이트 메뉴">',
        "사이드바 dialog 시맨틱")
h = sub(h, '<button class="sidebar-close" aria-label="닫기">×</button>',
        '<button class="sidebar-close" type="button" aria-label="메뉴 닫기">×</button>',
        "닫기 버튼 type/label")

# 메뉴 그룹화 + 인라인 style 제거
h = sub(h, '''    <a href="/"><span class="lab" style="font-size:24px">Home</span><span class="ko">홈</span></a>
    <a href="/website-design/"><span class="lab" style="font-size:19px">Website Design</span><span class="ko">웹사이트 디자인</span></a>
    <a href="/geo/"><span class="lab" style="font-size:19px">GEO</span><span class="ko">생성형 검색 최적화</span></a>
    <a href="/blog-content/"><span class="lab" style="font-size:19px">Blog Content</span><span class="ko">블로그 콘텐츠</span></a>
    <a href="/digital-marketing/"><span class="lab" style="font-size:19px">Digital Marketing</span><span class="ko">디지털 마케팅</span></a>
    <a href="/work/"><span class="lab" style="font-size:24px">Work</span><span class="ko">작업 사례</span></a>
    <a href="/column/"><span class="lab" style="font-size:24px">칼럼</span><span class="ko">네이버 칼럼</span></a>
    <a href="/about/"><span class="lab" style="font-size:24px">About</span><span class="ko">회사 소개</span></a>
    <a href="/contact/"><span class="lab" style="font-size:24px">Contact</span><span class="ko">문의</span></a>''',
'''    <a href="/"><span class="lab">Home</span><span class="ko">홈</span></a>
  </div>
  <div class="sidebar-group">/SERVICES</div>
  <div class="sidebar-menu">
    <a href="/website-design/"><span class="lab lab-sub">Website Design</span><span class="ko">웹사이트 디자인</span></a>
    <a href="/geo/"><span class="lab lab-sub">GEO</span><span class="ko">생성형 검색 최적화</span></a>
    <a href="/blog-content/"><span class="lab lab-sub">Blog Content</span><span class="ko">블로그 콘텐츠</span></a>
    <a href="/digital-marketing/"><span class="lab lab-sub">Digital Marketing</span><span class="ko">디지털 마케팅</span></a>
  </div>
  <div class="sidebar-group">/PAGES</div>
  <div class="sidebar-menu">
    <a href="/work/"><span class="lab">Work</span><span class="ko">작업 사례</span></a>
    <a href="/column/"><span class="lab">칼럼</span><span class="ko">네이버 칼럼</span></a>
    <a href="/about/"><span class="lab">About</span><span class="ko">회사 소개</span></a>
    <a href="/contact/"><span class="lab">Contact</span><span class="ko">문의</span></a>''',
 "사이드바 메뉴 그룹화(/SERVICES · /PAGES) + 인라인 font-size 제거")

# target=_blank 에 rel 보강
h = h.replace('target="_blank"><svg width="18"', 'target="_blank" rel="noopener"><svg width="18"')
h = h.replace('target="_blank" title="카카오톡 문의"', 'target="_blank" rel="noopener" title="카카오톡 문의"')
log.append("target=_blank 2곳에 rel=noopener")

open(p,'w',encoding='utf-8').write(h)
print(f"OK — {len(log)}건\n")
for i,w in enumerate(log,1): print(f"{i}. {w}")
