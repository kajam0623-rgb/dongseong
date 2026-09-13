#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""제목 <br> 앞에 공백 삽입 — 420px 이하에서 단어가 붙어버리는 버그 수정.

증상
  global.css 의 `@media(max-width:420px){.sec-h2 br,.footer h2 br{display:none}}` 로
  좁은 화면에서는 제목의 강제 개행을 풀어 자연스럽게 흐르게 하는데,
  마크업이 `않았습니다,<br>고친` 이라 br 이 사라지면 `않았습니다,고친` 으로 붙는다.
  홈·서브 전 페이지 제목에서 같은 증상이 난다.

검증한 대안들
  br::after{content:" "}        → 렌더되지 않음 (Chrome). 실패
  br{display:inline;content:" "} → br 이 그대로 개행함. 실패
  마크업에 `, <br>` 로 공백 추가 → 데스크톱 줄 폭 501/128px 로 동일(변화 없음),
                                   모바일에서 `않았습니다, 고친` 으로 정상. 채택

대상은 h1·h2 안의 <br> 뿐이다. 카드 안 <br>(.psi-s small 등)은 숨기는 규칙이 없어
건드리지 않는다.
"""
import io, os, re, glob

H = re.compile(r'<(h1|h2)\b[^>]*>.*?</\1>', re.S)
BR = re.compile(r'(?<=[^\s>])<br\s*/?>')

total = 0
for path in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages', '*.html'))):
    s = io.open(path, encoding='utf-8').read()
    hits = [0]

    def fix(m):
        block = m.group(0)
        new, n = BR.subn(' <br>', block)
        hits[0] += n
        return new

    out = H.sub(fix, s)
    if hits[0]:
        io.open(path, 'w', encoding='utf-8').write(out)
        total += hits[0]
        print('%-34s %2d개' % (os.path.basename(path), hits[0]))

print('합계 %d개' % total)
