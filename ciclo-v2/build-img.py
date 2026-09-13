# -*- coding: utf-8 -*-
"""이미지에 width/height 지정 — CLS 제거.
   로고 mark-ciclo-white.png 의 고유 비율을 CSS 표시 크기에 맞춰 명시한다.
   실제 파일 비율은 정사각(원형 마크)으로 가정. 다르면 아래 RATIO 만 고치면 된다."""
import sys, glob, re
RATIO = 1.0  # width / height

targets = {
 # (파일, 원본 태그, 교체 태그, 설명)
 'pages/CICLO_Header.html': [
   ('<img src="/wp-content/uploads/mark-ciclo-white.png" alt="">',
    '<img src="/wp-content/uploads/mark-ciclo-white.png" alt="" width="20" height="20" decoding="async">',
    '헤더 로고 20px'),
 ],
 'pages/CICLO_Footer.html': [
   ('<img class="footer-mark" src="/wp-content/uploads/mark-ciclo-white.png" alt="">',
    '<img class="footer-mark" src="/wp-content/uploads/mark-ciclo-white.png" alt="" width="600" height="600" loading="lazy" decoding="async">',
    '푸터 배경 마크 (지연 로딩)'),
   ('<img src="/wp-content/uploads/mark-ciclo-white.png" alt="CICLO">',
    '<img src="/wp-content/uploads/mark-ciclo-white.png" alt="CICLO" width="20" height="20" loading="lazy" decoding="async">',
    '푸터 브랜드 로고 20px'),
 ],
}
log=[]
for f, subs in targets.items():
    s = open(f, encoding='utf-8').read()
    for old, new, why in subs:
        n = s.count(old)
        if n == 0:
            print(f"[SKIP] {f}: {why} — 매칭 0건"); continue
        s = s.replace(old, new); log.append(f"{f}: {why} ({n}건)")
    open(f,'w',encoding='utf-8').write(s)

# 남은 이미지 점검
print(f"OK — {len(log)}건\n")
for w in log: print(" ", w)
print("\n=== width/height 없는 img 잔여 ===")
left=0
for f in glob.glob('pages/*.html'):
    for m in re.finditer(r'<img[^>]*>', open(f,encoding='utf-8').read()):
        t=m.group(0)
        if 'width=' not in t:
            print(f"  {f}: {t[:100]}"); left+=1
print(f"  총 {left}건")
