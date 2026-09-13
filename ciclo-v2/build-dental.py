#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""/dental 랜딩 v2 — 모바일 붕괴와 성능 부채 수정.

이 페이지는 홈 #work 의 Featured 카드가 가리키는 가장 큰 랜딩(76.7KB)인데
실측해 보니 상태가 가장 나빴다.

실측 (헤드리스 크롬, pv 프리뷰)
  390px  가로 오버플로 **470px** · 뷰포트보다 넓은 노드 276개
  768px  가로 오버플로 92px · 넓은 노드 23개
  1440px 정상
  → `.page{width:860px}` 고정폭에 미디어쿼리가 카톡 버튼용 2개뿐이다.
     휴대폰에서 페이지 전체가 옆으로 밀리고 글이 잘린다.

  will-change 33개 · 무한 애니메이션 3종(bob·pulse·spin)
  Pretendard 를 jsdelivr 에서 **한 번 더** 불러온다(정적 전체 CSS).
     헤드 스니펫이 이미 dynamic-subset 을 로드하므로 완전 중복이다.
  `#ciclo-dental html{scroll-snap-type:y proximity}` 은 html 이 div 의 자손일 수
     없어 매칭되지 않는다. 스냅은 처음부터 작동한 적이 없다(실측 scrollSnapType:none).
  하단에 스코프 없는 `.kko-fab` <style> 이 한 벌 더 있다.

  연락처가 사이트 나머지와 다르다:
     kajam0623@gmail.com / 010-8817-2001
     ↔ 헤더·사이드바·푸터·Contact 는 전부 kajam0623@naver.com / 010-8017-2001
  전화번호는 한 자리(80→88) 차이라 오타로 보인다. 나머지 4곳을 정본으로 맞춘다.

모션은 유한한 것(shake·flash·리빌)만 남긴다. 무한 3종은 v2 방침(모션은 빼기)대로 제거.
특히 pulse 는 box-shadow 애니메이션이라 합성이 아니라 페인트를 매 프레임 유발한다.
"""
import sys, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'pages', '치과_홈페이지_제작.html')
s = io.open(P, encoding='utf-8').read()
before = len(s.encode('utf-8'))

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        sys.exit('FAIL: %d회 (기대 %d) — %r' % (c, n, old[:80]))
    s = s.replace(old, new)

# ── 1. 중복 Pretendard 제거 ────────────────────────────────────
rep('<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css">\n',
    '<!-- Pretendard 는 사이트 헤드 스니펫이 이미 로드한다 (dynamic-subset). 중복 링크 제거. -->\n')

# ── 2. 반응형 ─────────────────────────────────────────────────
rep('    --W:860px;\n    --P:64px;',
    '    --W:860px;\n    --P:clamp(20px,5.4vw,64px);')

rep('#ciclo-dental .page{width:var(--W);margin:0 auto;overflow:hidden;}',
    '#ciclo-dental .page{width:min(var(--W),100%);margin:0 auto;overflow:hidden;}')

rep('  .scr{padding:120px var(--P);text-align:center;}',
    '  .scr{padding:clamp(72px,11vw,120px) var(--P);text-align:center;}')
rep('#ciclo-dental .scr.sm{padding:88px var(--P);}',
    '#ciclo-dental .scr.sm{padding:clamp(56px,8vw,88px) var(--P);}')
rep('  .top{padding:32px var(--P) 36px;border-bottom:1px solid var(--line);}',
    '  .top{padding:clamp(22px,3vw,32px) var(--P) clamp(24px,3.4vw,36px);border-bottom:1px solid var(--line);}')

# 타이포 사다리 — 88/66/48/32 고정은 390px 에서 그대로 넘친다
rep('  .xxl{font-size:88px;line-height:1.14;font-weight:800;letter-spacing:-.05em;}',
    '  .xxl{font-size:clamp(38px,8.4vw,88px);line-height:1.14;font-weight:800;letter-spacing:-.05em;}')
rep('#ciclo-dental .xl{font-size:66px;line-height:1.22;font-weight:800;letter-spacing:-.045em;}',
    '#ciclo-dental .xl{font-size:clamp(32px,6.4vw,66px);line-height:1.22;font-weight:800;letter-spacing:-.045em;}')
rep('#ciclo-dental .lg{font-size:48px;line-height:1.32;font-weight:800;letter-spacing:-.038em;}',
    '#ciclo-dental .lg{font-size:clamp(26px,4.8vw,48px);line-height:1.32;font-weight:800;letter-spacing:-.038em;}')
rep('#ciclo-dental .md{font-size:32px;line-height:1.5;font-weight:700;letter-spacing:-.028em;}',
    '#ciclo-dental .md{font-size:clamp(21px,3.2vw,32px);line-height:1.5;font-weight:700;letter-spacing:-.028em;}')
rep('#ciclo-dental .bd{font-size:19px;line-height:1.9;font-weight:500;}',
    '#ciclo-dental .bd{font-size:clamp(16.5px,1.9vw,19px);line-height:1.9;font-weight:500;}')

# 브랜드 마크도 고정 112px/44px
rep('#ciclo-dental .brandmark svg{width:112px;height:112px;}',
    '#ciclo-dental .brandmark svg{width:clamp(76px,11vw,112px);height:auto;aspect-ratio:1}')
rep('    font-size:44px;font-weight:800;letter-spacing:.22em;color:#fff;',
    '    font-size:clamp(28px,4.4vw,44px);font-weight:800;letter-spacing:.22em;color:#fff;')

# 모바일 툴바가 접힐 때 100vh 가 흔들린다 (CLS)
rep('    min-height:100vh;', '    min-height:100vh;\n    min-height:100svh;')

# ── 3. 성능: will-change · 무한 애니메이션 · 죽은 규칙 ────────────
rep('''  #ciclo-dental /* 스냅 장면 전용: 진입 시 배경도 살짝 확대 */
  .scr.snap > *{will-change:transform,opacity;}
''',
'''  /* .scr.snap > *{will-change:transform,opacity} 제거 — 상시 합성 레이어 33개였다.
     리빌은 한 번 끝나면 다시 안 일어나므로 미리 레이어를 잡아둘 이유가 없다. */
''')

rep('''  /* 화살표 통통 */
  @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(9px)}}
  #ciclo-dental .chev{animation:bob 1.9s ease-in-out infinite;}
''',
'''  /* 화살표 — bob 무한 애니메이션 제거 (v2: 모션은 빼기). 위치만 남긴다. */
''')

rep('''  /* 게이지 펄스 */
  @keyframes pulse{
    0%,100%{box-shadow:0 0 0 0 rgba(232,69,60,.5)}
    50%{box-shadow:0 0 0 7px rgba(232,69,60,0)}
  }
  #ciclo-dental .pip{animation:pulse 1.8s ease-out infinite;}
''',
'''  /* 게이지 펄스 제거 — box-shadow 애니메이션은 합성이 아니라 매 프레임 페인트를
     유발한다. 무한 반복이라 페이지를 열어 두는 내내 돈다. 정적 링으로 대체. */
  #ciclo-dental .pip{box-shadow:0 0 0 4px rgba(232,69,60,.18);}
''')

rep('''  /* 배경 원 천천히 회전 */
  @keyframes spin{to{transform:rotate(360deg)}}
  #ciclo-dental .orb{
    position:absolute;border-radius:50%;pointer-events:none;
    border:1px dashed rgba(255,212,0,.22);
    animation:spin 46s linear infinite;
  }
''',
'''  /* 배경 원 — spin 46s 무한 회전 제거. 점선 원은 그대로 두되 돌지 않는다. */
  #ciclo-dental .orb{
    position:absolute;border-radius:50%;pointer-events:none;
    border:1px dashed rgba(255,212,0,.22);
  }
''')

# 죽은 스냅 규칙 — `#ciclo-dental html` 은 매칭되지 않는다
rep('''  #ciclo-dental /* 핵심 장면 = 한 스크롤에 하나씩 (스냅) */
  html{scroll-snap-type:y proximity;scroll-behavior:smooth;}
''',
'''  /* 스크롤 스냅 제거 — 원래 `#ciclo-dental html{...}` 로 쓰여 있었는데
     html 은 div 의 자손이 될 수 없어 한 번도 적용된 적이 없다(실측 확인).
     되살리는 대신 걷어낸다. 20개 장면짜리 긴 랜딩에서 스냅은 모바일에서
     스크롤을 뺏는다. .scr.snap 의 min-height 는 그대로 살려 장면감을 유지한다. */
''')

# ── 4. 중복 kko-fab <style> 제거 (스코프 없이 전역으로 샌다) ────────
rep('''<style>
.kko-fab{position:fixed;right:20px;bottom:20px;z-index:9999;display:flex;align-items:center;gap:8px;
  padding:13px 20px;border-radius:999px;background:#FEE500;color:#191600;text-decoration:none;
  font:700 15px/1 'Pretendard',sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.28);transition:transform .18s ease}
.kko-fab:hover{transform:translateY(-2px)}
.kko-fab svg{width:20px;height:20px;flex:none}
@media(max-width:640px){.kko-fab{right:14px;bottom:14px;padding:12px 16px;font-size:14px}}
</style>
''',
'''<!-- 스코프 없는 .kko-fab 스타일 한 벌 제거 — 위 #ciclo-dental .kko-fab 와 완전 중복이고,
     스코프가 없어 다른 페이지까지 영향을 줄 수 있었다. -->
''')

# ── 5. 연락처 정본화 ───────────────────────────────────────────
rep('<div>kajam0623@gmail.com &nbsp;·&nbsp; 010-8817-2001</div>',
    '<div><a href="mailto:kajam0623@naver.com">kajam0623@naver.com</a>'
    ' &nbsp;·&nbsp; <a href="tel:010-8017-2001">010-8017-2001</a></div>')

io.open(P, 'w', encoding='utf-8').write(s)
after = len(s.encode('utf-8'))
print('ok  pages/치과_홈페이지_제작.html  %d → %d B (%+d)' % (before, after, after - before))
