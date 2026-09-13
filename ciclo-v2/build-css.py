# -*- coding: utf-8 -*-
"""global.css → global.css v2 (238LAB 벤치마킹 반영)
   정확 문자열 치환. 하나라도 매칭 실패하면 즉시 중단한다."""
import sys

src = open('css/global.original.css', encoding='utf-8').read()
log = []

def sub(old, new, why):
    global src
    n = src.count(old)
    if n != 1:
        print(f"[FAIL] {why}\n  매칭 {n}건: {old[:80]!r}")
        sys.exit(1)
    src = src.replace(old, new)
    log.append(why)

# ── A. 타이포 기반 ──────────────────────────────────────────────
sub("""body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'Pretendard Variable',Pretendard,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}""",
    """body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'Pretendard Variable',Pretendard,-apple-system,sans-serif;-webkit-font-smoothing:antialiased;
  font-weight:400;line-height:1.7;word-break:keep-all}""",
    "body 기본 weight 400 / line-height 1.7 / keep-all")

sub(".overline{font-family:Archivo,sans-serif;font-weight:700;font-size:13px;letter-spacing:.22em;color:var(--pt)}",
    ".overline{font-family:Archivo,sans-serif;font-weight:600;font-size:14px;letter-spacing:.24em;line-height:1.45;color:var(--pt)}",
    "눈썹 13/700/.22em → 14/600/.24em")

sub(".sec-h2{font-family:Archivo,sans-serif;font-weight:900;font-size:clamp(40px,5.5vw,80px);line-height:1;letter-spacing:-.02em;text-transform:uppercase;margin-top:16px}",
    """.sec-h2{font-weight:700;font-size:clamp(28px,3.2vw,40px);line-height:1.25;letter-spacing:-.025em;margin-top:18px;word-break:keep-all}

/* 섹션 원자 구조 슬롯 — 238LAB 문법(눈썹 → h2 → 리드 → 링크 → 증거 → 출처) */
.sec-lead{margin-top:18px;max-width:60ch;font-size:18px;line-height:1.55;font-weight:400;color:rgba(18,18,18,.7)}
.sec-link{display:inline-flex;align-items:center;gap:7px;margin-top:20px;font-size:15px;font-weight:700;color:var(--pt);
  transition:color .15s cubic-bezier(.4,0,.2,1)}
.sec-link:hover{color:var(--pt2)}
.sec-caption{margin-top:12px;font-size:13px;line-height:1.6;font-weight:400;color:rgba(18,18,18,.48)}
.section.navy .sec-lead{color:rgba(255,255,255,.72)}
.section.navy .sec-caption{color:rgba(255,255,255,.45)}
.section.navy .sec-link{color:#fff}""",
    "sec-h2 → Pretendard 700 clamp(28,3.2vw,40)/1.25/-.025em + 리드·링크·캡션 슬롯 신설")

# ── B. 버튼 · 라운드 · 호버 ─────────────────────────────────────
sub(""".btn{display:inline-flex;align-items:center;gap:8px;border-radius:999px;padding:16px 32px;font-size:15px;font-weight:700;
  transition:transform .18s cubic-bezier(.2,.8,.2,1),box-shadow .18s,border-color .18s,background .18s}""",
    """.btn{display:inline-flex;align-items:center;gap:8px;border-radius:4px;padding:16px 32px;font-size:15px;font-weight:700;
  transition:color .15s cubic-bezier(.4,0,.2,1),background .15s cubic-bezier(.4,0,.2,1),border-color .15s cubic-bezier(.4,0,.2,1)}""",
    "버튼 라운드 999→4px, 호버 트랜지션 .18s→.15s (transform/shadow 제거)")

sub(".btn-primary:hover{color:#fff;transform:translateY(-2px);box-shadow:0 14px 30px rgba(17,30,108,.32)}",
    ".btn-primary:hover{color:#fff;background:var(--pt2)}",
    "btn-primary 호버 리프트 제거 → 배경 변화")

sub(".btn-white:hover{color:var(--pt);transform:translateY(-2px)}",
    ".btn-white:hover{color:var(--pt);background:#E8E4D8}",
    "btn-white 호버 리프트 제거")

sub(".nav-cta{background:#fff;color:var(--pt);border-radius:999px;padding:9px 18px;font-size:13.5px;font-weight:700}",
    ".nav-cta{background:#fff;color:var(--pt);border-radius:4px;padding:9px 18px;font-size:13.5px;font-weight:700}",
    "nav-cta 라운드 999→4px")

sub(".kakao-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:var(--kakao);color:#191919;border-radius:999px;padding:14px 0;font-size:15px;font-weight:800;transition:transform .18s,background .18s}",
    ".kakao-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:var(--kakao);color:#191919;border-radius:4px;padding:14px 0;font-size:15px;font-weight:800;transition:background .15s cubic-bezier(.4,0,.2,1)}",
    "kakao-btn 라운드 999→4px, 리프트 제거")

sub(".kakao-btn:hover{background:#FFEB33;color:#191919;transform:translateY(-1px)}",
    ".kakao-btn:hover{background:#FFEB33;color:#191919}",
    "kakao-btn 호버 리프트 제거")

sub(""".kakao-float:hover{color:#191919;transform:translateY(-2px);box-shadow:0 16px 32px rgba(0,0,0,.28)}""",
    """.kakao-float:hover{color:#191919;background:#FFEB33}""",
    "kakao-float 호버 리프트 제거 (플로팅 버튼 자체는 원형 유지)")

sub(".chip{border:1px solid rgba(18,18,18,.18);border-radius:999px;padding:6px 14px;font-size:13px;font-weight:600;color:rgba(18,18,18,.65)}",
    ".chip{border:1px solid rgba(18,18,18,.18);border-radius:4px;padding:6px 10px;font-size:13px;font-weight:600;color:rgba(18,18,18,.65)}",
    "chip 알약 → 4px 라벨, 좌우 패딩 14→10px")

sub(".other-pill{border:1.5px solid rgba(18,18,18,.2);border-radius:999px;padding:12px 24px;font-family:Archivo,sans-serif;font-weight:800;font-size:14px;text-transform:uppercase;color:var(--ink)}",
    ".other-pill{border:1.5px solid rgba(18,18,18,.2);border-radius:4px;padding:12px 24px;font-family:Archivo,sans-serif;font-weight:800;font-size:14px;text-transform:uppercase;color:var(--ink)}",
    "other-pill 알약 → 4px")

# ── C. 모션 제거 ────────────────────────────────────────────────
sub(".hero-mark img{height:min(78vh,620px);width:auto;filter:invert(.78);opacity:.1;animation:spin 40s linear infinite}",
    ".hero-mark img{height:min(78vh,620px);width:auto;filter:invert(.78);opacity:.1}",
    "히어로 원형 마크 무한회전(spin 40s) 제거")

sub(".scroll-badge svg{position:absolute;inset:0;width:100%;height:100%;animation:spin 16s linear infinite}",
    ".scroll-badge svg{position:absolute;inset:0;width:100%;height:100%}",
    "SCROLL 배지 무한회전(spin 16s) 제거")

sub(".marquee-track{display:inline-flex;animation:marquee 26s linear infinite;will-change:transform}",
    ".marquee-track{display:inline-flex;animation:marquee 40s linear infinite;will-change:transform}",
    "마퀴 26s → 40s (238LAB 동일 속도)")

sub("""/* reveal */
.reveal{opacity:0;transform:translateY(22px);transition:opacity .55s cubic-bezier(.16,1,.3,1),transform .55s cubic-bezier(.16,1,.3,1)}
.reveal.in{opacity:1;transform:none}""",
    """/* reveal — 제거됨 (238LAB은 스크롤 리빌 0개)
   ciclo-effects.js 에서 .reveal 주입 코드도 함께 삭제해야 한다.
   구버전 JS가 남아 클래스만 붙는 경우를 대비해 무해화 규칙을 남긴다. */
.reveal{opacity:1;transform:none;transition:none}

/* 모션 최소화 설정 존중 */
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;
    transition-duration:.01ms!important;scroll-behavior:auto!important}
}""",
    "스크롤 리빌 규칙 삭제 + prefers-reduced-motion 가드 추가")

# ── D. 카드 라운드 20 → 12 ──────────────────────────────────────
sub(".card{background:var(--card);border:1px solid rgba(18,18,18,.1);border-radius:20px;padding:28px 26px;transition:transform .18s cubic-bezier(.2,.8,.2,1),box-shadow .18s}",
    ".card{background:var(--card);border:1px solid rgba(18,18,18,.1);border-radius:12px;padding:28px 26px;transition:border-color .15s cubic-bezier(.4,0,.2,1)}",
    "card 라운드 20→12px, 호버 리프트 제거")
sub(".card:hover{transform:translateY(-4px);box-shadow:0 16px 34px rgba(17,30,108,.1)}",
    ".card:hover{border-color:rgba(17,30,108,.3)}",
    "card 호버 → 테두리 변화")
sub(".proc-card{border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:28px 24px;display:flex;flex-direction:column;gap:60px;transition:background .18s}",
    ".proc-card{border:1px solid rgba(255,255,255,.16);border-radius:12px;padding:28px 24px;display:flex;flex-direction:column;gap:60px;transition:background .15s cubic-bezier(.4,0,.2,1)}",
    "proc-card 라운드 20→12px")
sub(""".work-slot{aspect-ratio:4/3;border-radius:20px;overflow:hidden;background:#E9E4D9;display:flex;align-items:center;justify-content:center;""",
    """.work-slot{aspect-ratio:4/3;border-radius:12px;overflow:hidden;background:#E9E4D9;display:flex;align-items:center;justify-content:center;""",
    "work-slot 라운드 20→12px")
sub(".mean{border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:32px 30px}",
    ".mean{border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:32px 30px}",
    "mean 라운드 20→12px")
sub(".channel{display:flex;justify-content:space-between;align-items:center;border-radius:20px;padding:28px 30px;transition:transform .18s cubic-bezier(.2,.8,.2,1),box-shadow .18s}",
    ".channel{display:flex;justify-content:space-between;align-items:center;border-radius:12px;padding:28px 30px;transition:background .15s cubic-bezier(.4,0,.2,1),border-color .15s cubic-bezier(.4,0,.2,1)}",
    "channel 라운드 20→12px, 호버 리프트 제거")
sub(".channel.kakao:hover{color:#191919;transform:translateY(-3px);box-shadow:0 16px 34px rgba(0,0,0,.14)}",
    ".channel.kakao:hover{color:#191919;background:#FFEB33}", "channel.kakao 리프트 제거")
sub(".channel.mail:hover{color:#fff;transform:translateY(-3px);box-shadow:0 16px 34px rgba(17,30,108,.28)}",
    ".channel.mail:hover{color:#fff;background:var(--pt2)}", "channel.mail 리프트 제거")
sub(".channel.phone:hover{color:var(--ink);transform:translateY(-3px);box-shadow:0 16px 34px rgba(17,30,108,.1)}",
    ".channel.phone:hover{color:var(--ink);border-color:rgba(17,30,108,.35)}", "channel.phone 리프트 제거")
sub(".contact-proc{background:var(--panel);border-radius:20px;padding:32px 30px}",
    ".contact-proc{background:var(--panel);border-radius:12px;padding:32px 30px}",
    "contact-proc 라운드 20→12px")

# ── E. 본문 굵기 500 → 400 (13곳) ───────────────────────────────
w500 = [
 (".hero .lead{margin-top:36px;max-width:560px;font-size:clamp(16px,1.6vw,19px);line-height:1.65;font-weight:500;color:rgba(18,18,18,.72)}",
  ".hero .lead{margin-top:36px;max-width:560px;font-size:clamp(17px,1.7vw,20px);line-height:1.55;font-weight:400;color:rgba(18,18,18,.72)}",
  "hero .lead 500→400, 16-19px→17-20px, lh1.65→1.55"),
 (".page-hero .lead{margin-top:28px;max-width:620px;font-size:clamp(17px,1.8vw,21px);line-height:1.65;font-weight:500;color:rgba(18,18,18,.75)}",
  ".page-hero .lead{margin-top:28px;max-width:620px;font-size:clamp(17px,1.8vw,21px);line-height:1.6;font-weight:400;color:rgba(18,18,18,.75)}",
  "page-hero .lead 500→400"),
 (".svc-row p{font-size:16px;line-height:1.65;font-weight:500;color:rgba(18,18,18,.72)}",
  ".svc-row p{font-size:16px;line-height:1.7;font-weight:400;color:rgba(18,18,18,.72)}", "svc-row p 500→400"),
 (".card p{margin-top:10px;font-size:14.5px;line-height:1.7;color:rgba(18,18,18,.68);font-weight:500}",
  ".card p{margin-top:10px;font-size:14px;line-height:1.62;color:rgba(18,18,18,.68);font-weight:400}", "card p 500→400, 14.5→14px"),
 (".step p{margin-top:8px;font-size:14px;line-height:1.65;color:rgba(18,18,18,.65);font-weight:500}",
  ".step p{margin-top:8px;font-size:14px;line-height:1.62;color:rgba(18,18,18,.65);font-weight:400}", "step p 500→400"),
 (".work-desc{margin-top:6px;font-size:14px;font-weight:500;color:rgba(18,18,18,.6)}",
  ".work-desc{margin-top:6px;font-size:14px;line-height:1.62;font-weight:400;color:rgba(18,18,18,.6)}", "work-desc 500→400"),
 (".about-body{margin-top:28px;font-size:16px;line-height:1.75;font-weight:500;color:rgba(18,18,18,.7);max-width:560px}",
  ".about-body{margin-top:20px;font-size:16px;line-height:1.7;font-weight:400;color:rgba(18,18,18,.7);max-width:62ch}", "about-body 500→400"),
 (".mean p{margin-top:10px;font-size:15px;line-height:1.7;color:rgba(255,255,255,.7);font-weight:500}",
  ".mean p{margin-top:10px;font-size:15px;line-height:1.7;color:rgba(255,255,255,.7);font-weight:400}", "mean p 500→400"),
 (".faq-row p{font-size:16px;line-height:1.75;font-weight:500;color:rgba(18,18,18,.72)}",
  ".faq-row p{font-size:16px;line-height:1.75;font-weight:400;color:rgba(18,18,18,.72)}", "faq-row p 500→400"),
 (".cp-step p{margin-top:4px;font-size:14px;line-height:1.65;color:rgba(18,18,18,.65);font-weight:500}",
  ".cp-step p{margin-top:4px;font-size:14px;line-height:1.62;color:rgba(18,18,18,.65);font-weight:400}", "cp-step p 500→400"),
 (".cp-note{margin-top:28px;border-top:1px solid rgba(18,18,18,.14);padding-top:18px;font-size:13.5px;line-height:1.8;color:rgba(18,18,18,.6);font-weight:500}",
  ".cp-note{margin-top:28px;border-top:1px solid rgba(18,18,18,.14);padding-top:18px;font-size:13.5px;line-height:1.7;color:rgba(18,18,18,.6);font-weight:400}", "cp-note 500→400"),
 (".footer .lead{margin-top:24px;font-size:17px;font-weight:500;color:rgba(255,255,255,.75);line-height:1.65}",
  ".footer .lead{margin-top:24px;font-size:18px;font-weight:400;color:rgba(255,255,255,.75);line-height:1.55}", "footer .lead 500→400, 17→18px"),
 (".sidebar-contact{margin-top:18px;font-size:13.5px;line-height:1.9;color:rgba(255,255,255,.7);font-weight:500}",
  ".sidebar-contact{margin-top:18px;font-size:13.5px;line-height:1.8;color:rgba(255,255,255,.7);font-weight:400}", "sidebar-contact 500→400"),
]
for o,n,w in w500: sub(o,n,w)

# ── F. 레이아웃 ─────────────────────────────────────────────────
sub(".section{padding:clamp(80px,10vw,140px) clamp(20px,5vw,100px);max-width:1280px;margin:0 auto}",
    ".section{padding:clamp(80px,10vw,160px) clamp(20px,5vw,100px);max-width:1280px;margin:0 auto}",
    "섹션 세로 패딩 140→160px (238LAB 실측치)")

sub(".about-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(32px,5vw,80px);align-items:start}",
    ".about-grid{display:grid;grid-template-columns:1fr;gap:clamp(20px,3vw,28px);align-items:start}",
    "about-grid 2단(.8fr 1.2fr) → 1단 (한글 문장형 h2가 242px 컬럼에서 7줄로 터짐)")

sub(".footer h2{margin-top:18px;font-family:Archivo,sans-serif;font-weight:900;font-size:clamp(44px,7vw,96px);line-height:.95;letter-spacing:-.03em;text-transform:uppercase}",
    ".footer h2{margin-top:18px;font-weight:700;font-size:clamp(28px,3.2vw,40px);line-height:1.25;letter-spacing:-.025em;word-break:keep-all}",
    "푸터 h2 → 섹션 h2와 동일 스케일")

# ── G. 820px 눌림 방어 ──────────────────────────────────────────
sub("""/* responsive */""",
    """/* ★ 홈·랜딩 폭 방어
   워드프레스 추가 CSS 의 main.site-main>.page-content{max-width:820px} 가
   body 조건 없이 걸려 있어 1280px 로 설계된 홈까지 820px 로 눌린다.
   근본 해결은 그 규칙에 body:not(.home) 같은 조건을 붙이는 것이고,
   아래는 그때까지의 방어선이다. */
main.site-main>.page-content:has(.ciclo-page){max-width:none}

/* responsive */""",
    "820px 눌림 방어 규칙 추가")

sub("""@media(max-width:560px){.grid-4{grid-template-columns:1fr}}""",
    """@media(max-width:560px){.grid-4{grid-template-columns:1fr}}
@media(max-width:420px){
  .sec-h2 br,.footer h2 br{display:none}
  .sec-h2,.footer h2{font-size:26px}
  .overline{font-size:12px;letter-spacing:.18em}
  .sec-lead{font-size:16px}
}""",
    "420px 이하 h2/눈썹/리드 축소 규칙 추가")

open('css/global.css','w',encoding='utf-8').write(src)
print(f"OK — {len(log)}건 적용, {len(src)} chars\n")
for i,w in enumerate(log,1): print(f"{i:2}. {w}")
