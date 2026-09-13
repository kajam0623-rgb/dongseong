# -*- coding: utf-8 -*-
"""성능 패스 — PageSpeed 목표. 정확 문자열 치환."""
import sys
p='css/global.css'; s=open(p,encoding='utf-8').read(); log=[]
def sub(old,new,why):
    global s
    if s.count(old)!=1:
        print(f"[FAIL] {why} — 매칭 {s.count(old)}건"); sys.exit(1)
    s=s.replace(old,new); log.append(why)

# 1) @import 제거 — 직렬 요청 체인 해소
sub("""@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css');
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&display=swap');
/* CICLO — static site styles */""",
"""/* CICLO — static site styles (v2)
 *
 * ★ 폰트 @import 를 여기서 제거했다.
 *   @import 는 "global.css 다운로드 → 파싱 → 폰트 CSS 2개 요청 → 폰트 파일 요청" 으로
 *   직렬 3왕복이 되어 FCP/LCP 를 직접 깎는다.
 *   WPCode > HTML Snippet > Site Wide Header 에 wpcode-head.html 을 넣으면
 *   preconnect 와 함께 병렬로 받는다. 그 스니펫이 없으면 폰트가 안 뜬다.
 */""",
 "@import 2개 제거 (직렬 요청 체인 → head preconnect+link 로 이관)")

# 2) .overline 600 → 700 (Archivo 에 600 이 없어 브라우저가 700 으로 대체 중이었다)
sub(".overline{font-family:Archivo,sans-serif;font-weight:600;font-size:14px;letter-spacing:.24em;line-height:1.45;color:var(--pt)}",
    ".overline{font-family:Archivo,'Arial Narrow',sans-serif;font-weight:700;font-size:14px;letter-spacing:.24em;line-height:1.45;color:var(--pt)}",
    ".overline 600→700 (Archivo 에 600 웨이트가 없어 어차피 700 으로 대체되던 값)")

# 3) 디스플레이 폰트 폴백을 금속적으로 가까운 것으로 → 스왑 시 레이아웃 이동 감소
sub(".arch{font-family:Archivo,sans-serif}",
    ".arch{font-family:Archivo,'Arial Black','Helvetica Neue',sans-serif}",
    "Archivo 폴백을 Arial Black 으로 (swap 시 CLS 감소)")
sub(".display{font-family:Archivo,sans-serif;font-weight:900;letter-spacing:-.03em;text-transform:uppercase;line-height:.92}",
    ".display{font-family:Archivo,'Arial Black','Helvetica Neue',sans-serif;font-weight:900;letter-spacing:-.03em;text-transform:uppercase;line-height:.92}",
    ".display 폴백 강화 (히어로 h1 = LCP 요소)")

# 4) will-change 상시 레이어 제거
sub(".marquee-track{display:inline-flex;animation:marquee 40s linear infinite;will-change:transform}",
    ".marquee-track{display:inline-flex;animation:marquee 40s linear infinite}",
    "marquee-track will-change 제거 (상시 컴포지터 레이어 → 메모리 낭비)")

# 5) 히어로 100vh → 100svh (모바일 툴바 리사이즈 점프 방지)
sub(".hero{min-height:100vh;display:flex;",
    ".hero{min-height:100vh;min-height:100svh;display:flex;",
    "히어로 min-height 에 100svh 추가 (모바일 주소창 리사이즈 CLS 방지)")

# 6) 이미지 안전판
sub("h1,h2,h3,p{margin:0}\nimg{display:block}",
    "h1,h2,h3,p{margin:0}\nimg{display:block;max-width:100%;height:auto}",
    "img max-width/height 안전판")

# 7) 화면 밖 섹션 렌더링 건너뛰기
sub("""/* ★ 홈·랜딩 폭 방어""",
"""/* 화면 밖 섹션은 렌더링을 건너뛴다 (긴 페이지 초기 렌더 비용 절감).
   contain-intrinsic-size 의 auto 키워드가 실제 높이를 기억하므로
   스크롤바 점프가 생기지 않는다. */
.section,.footer{content-visibility:auto;contain-intrinsic-size:auto 700px}
.hero{content-visibility:visible}

/* ★ 홈·랜딩 폭 방어""",
 "화면 밖 섹션 content-visibility:auto (히어로는 제외)")

open(p,'w',encoding='utf-8').write(s)
print(f"OK — {len(log)}건\n")
for i,w in enumerate(log,1): print(f"{i}. {w}")
