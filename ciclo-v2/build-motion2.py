#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""모션 2차 — 자연스럽고 무게 있는 것만 얹는다.

1차(build-motion.py)는 등장과 막대 성장까지였다. 여기에 네 가지를 더한다.
전부 합성 속성(transform·opacity·clip-path)만 쓰므로 레이아웃을 건드리지
않고, CLS 는 그대로 0 이다.

A. 제목 줄 단위 마스크 등장
   h2 를 통째로 띄우지 않고 줄마다 아래에서 밀어 올린다. 제목에 이미
   <br> 로 줄이 나뉘어 있어 그 자리를 그대로 쓴다. 텍스트를 자르지 않고
   기존 줄바꿈을 감싸기만 해서, JS 가 죽어도 h2 는 원문 그대로 남는다.
   한글은 ㅇ·ㅍ 같은 글자가 기준선 아래로 내려가므로 overflow:hidden 에
   잘린다. padding-bottom 을 주고 같은 크기의 음수 마진으로 상쇄한다.

B. 숫자 카운트업
   데이터를 파는 페이지에서 숫자가 올라가는 건 장식이 아니라 읽는 순서를
   만든다. 다만 자릿수가 늘면 폭이 변해 글자가 밀린다. 그래서
   min-width 를 최종 자릿수로 미리 잡고 tabular-nums 로 자폭을 고정한다.
   0.9초, 감속 곡선. 정수만 올린다(3/3 · −61 같은 건 건드리지 않는다).

C. 히어로 마크 시차
   커서를 따라 배경 마크가 아주 조금(±12px) 따라온다. 마우스가 있는
   기기에서만, 그리고 rAF 로 묶어 프레임당 한 번만 쓴다.

D. 내비 스크롤 반응
   히어로를 지나면 그림자가 짙어지고 아주 조금 작아진다.
   크기를 padding 으로 줄이면 고정 요소라도 자리가 흔들리므로 transform
   으로만 줄인다.

E. 버튼 채움
   색만 바뀌던 것을 왼쪽에서 차오르게 바꾼다. 가상요소를 쓰면 z-index
   싸움이 생겨서 background-size 로 처리한다. 단색이라 그라데이션으로
   보이지 않는다.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = u'''

/* =========================================================
   모션 2차 — 제목 줄 등장 · 숫자 카운트업 · 마크 시차 · 내비 · 버튼
   전부 transform / opacity / clip-path / background-size 만 쓴다.
   레이아웃을 건드리지 않으므로 CLS 는 0 그대로다.
   ========================================================= */

/* ── A. 제목 줄 단위 마스크 등장 ──
   h2 는 블록째 페이드하지 않고 줄마다 밀어 올린다. 두 효과가 겹치면
   글자가 두 번 움직여 보이므로 블록 페이드를 끈다. */
html.mo .mo-i.sec-h2,
html.mo .mo-i .sec-h2{opacity:1;transform:none}
.sec-h2 .ln{display:block;overflow:hidden;
  /* 한글 ㅇ·ㅍ 과 괄호는 기준선 아래로 내려간다. 잘리지 않게 아래를 넓히고
     같은 크기의 음수 마진으로 줄 간격을 원래대로 되돌린다. */
  padding-bottom:.12em;margin-bottom:-.12em}
.sec-h2 .ln>i{display:block;font-style:normal}
html.mo .sec-h2 .ln>i{transform:translateY(104%)}
html.mo [data-mo].mo-in .sec-h2 .ln>i{transform:none;
  transition:transform .86s cubic-bezier(.22,1,.36,1) var(--ld,0ms)}
html.mo [data-mo].mo-now .sec-h2 .ln>i{transition:none!important}

/* ── B. 숫자 카운트업 ──
   자릿수가 늘면 폭이 변한다. 최종 자릿수만큼 미리 자리를 잡아 둔다. */
.cnt{display:inline-block;font-variant-numeric:tabular-nums;
  min-width:calc(var(--dg,2)*1ch)}
.ev-num .cnt,.psi-ring .cnt{text-align:center}

/* ── C. 히어로 마크 시차 ── */
.hero-mark{transform:translateY(-50%) translate3d(var(--mx,0px),var(--my,0px),0);
  transition:transform .9s cubic-bezier(.22,1,.36,1)}

/* ── D. 내비 스크롤 반응 ──
   padding 으로 줄이면 고정 요소라도 안쪽이 흔들린다. transform 으로만. */
.nav{transform-origin:50% 0;
  transition:transform .42s cubic-bezier(.22,1,.36,1),box-shadow .42s cubic-bezier(.22,1,.36,1)}
html.scrolled .nav{transform:scale(.965);box-shadow:0 6px 20px rgba(17,30,108,.34)}

/* ── E. 버튼 채움 ──
   가상요소 대신 background-size. z-index 다툼이 없고 단색이라
   그라데이션으로 보이지 않는다. */
.btn-primary{background-image:linear-gradient(var(--pt2),var(--pt2));
  background-repeat:no-repeat;background-size:0% 100%;
  transition:background-size .44s cubic-bezier(.22,1,.36,1),color .15s cubic-bezier(.4,0,.2,1)}
.btn-primary:hover{background-size:100% 100%}
.btn-white{background-image:linear-gradient(#E8E4D8,#E8E4D8);
  background-repeat:no-repeat;background-size:0% 100%;
  transition:background-size .44s cubic-bezier(.22,1,.36,1),color .15s cubic-bezier(.4,0,.2,1)}
.btn-white:hover{background-size:100% 100%}

@media(prefers-reduced-motion:reduce){
  .sec-h2 .ln>i{transform:none!important}
  .hero-mark{transition:none}
}
'''

p = os.path.join(HERE, 'css', 'global.css')
s = io.open(p, encoding='utf-8').read()
if '모션 2차' in s: sys.exit('이미 적용됨')
io.open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + CSS)
print('CSS 추가  %d B' % len(CSS.encode('utf-8')))
