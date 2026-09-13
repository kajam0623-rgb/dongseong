# -*- coding: utf-8 -*-
"""로고 최적화
   1) CSS 인라인 base64 PNG(23,940자) → WebP(≈6,000자). 렌더 블로킹 CSS 45%→17%
   2) <img src> 404 5건 제거 — CSS content:url() 이 실제 로고를 그리므로
      src 는 투명 1x1 GIF 로 바꿔 요청 자체를 없앤다
   3) width/height 를 실제 비율 488x566 으로 정정 (앞 패스에서 정사각으로 잘못 넣었다)
"""
import re, base64, sys, glob

PX = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
webp = base64.b64encode(open('images/mark-ciclo-white-full.webp','rb').read()).decode()

# ── 1) CSS ──────────────────────────────────────────────────────
p='css/global.css'; s=open(p,encoding='utf-8').read()
m = re.search(r'(\.nav-logo img,\.sidebar-brand img,\.footer-brand img,\.hero-mark img,\.footer-mark\{content:url\(")data:image/png;base64,[^"]+("\)[^}]*\})', s)
if not m:
    print("[FAIL] CSS 로고 규칙 못 찾음"); sys.exit(1)
before = len(s)
s = s[:m.start()] + m.group(1) + 'data:image/webp;base64,' + webp + m.group(2) + s[m.end():]
s = s.replace(m.group(1), '/* 로고: PNG base64(23,940자) → WebP base64(약 6,000자). 렌더 블로킹 CSS 18KB 절감 */\n' + m.group(1), 1)
open(p,'w',encoding='utf-8').write(s)
print(f"CSS: {before:,} → {len(s):,} chars  ({before-len(s):,} 절감)")

# ── 2)+3) 마크업 ────────────────────────────────────────────────
# 실제 로고 비율 488x566. CSS 가 height 를 정하고 width:auto 이므로 고유 치수를 준다.
# ★ 정규식을 <img ...> 태그 안으로 한정한다.
#   처음엔 width="20" height="20" 를 전역 치환했다가 카카오 아이콘 <svg> 까지
#   488x566 으로 바꿔 버튼이 594px 높이로 부풀었다. 태그 단위로 좁혔다.
fixes = [
  (r'src="/wp-content/uploads/mark-ciclo-white\.png"', f'src="{PX}"'),
]
IMG_DIM = re.compile(r'(<img\b[^>]*?)width="\d+" height="\d+"')
total=0
for f in glob.glob('pages/*.html'):
    t=open(f,encoding='utf-8').read(); n0=t
    for pat,rep in fixes: t=re.sub(pat,rep,t)
    t = IMG_DIM.sub(r'\1width="488" height="566"', t)   # <img> 안에서만
    if t!=n0:
        open(f,'w',encoding='utf-8').write(t)
        c=sum(len(re.findall(pat,n0)) for pat,_ in fixes)
        print(f"  {f}: {c}건"); total+=c
print(f"마크업 총 {total}건")

# 검증
print("\n=== 잔여 404 유발 src ===")
left=0
for f in glob.glob('pages/*.html'):
    for mm in re.finditer(r'<img[^>]*>', open(f,encoding='utf-8').read()):
        tag=mm.group(0)
        if 'mark-ciclo-white.png' in tag: print(' ',f,tag[:80]); left+=1
        if 'width=' not in tag: print('  [치수없음]',f,tag[:80]); left+=1
print(f"  {left}건")
