#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""네이버 서치어드바이저 캡처 3장 — 모자이크 · WebP 변환 · 삽입.

파일과 내용 대응 (캡처를 열어 수치로 확인한 것)
  KakaoTalk_20260910_235544556.png  7.4백 클릭 · 6.4만 노출 · 1.2%  → 치과 ①
  KakaoTalk_20260910_235404303.png  1.1백 클릭 · 1.9만 노출 · 0.6%  → 치과 ②
  KakaoTalk_20260910_235453127.png   74 클릭 · 1.4만 노출 · 0.5%   → 치과 ③

가릴 곳 — 검색어 표의 상호·인명 줄
  PSI 캡처는 주소창과 썸네일만 가리면 됐는데, 이쪽은 표 안에 병원 이름이
  들어가 있다. 게다가 세 곳 다 1위가 상호 검색이었다.
    치과 ① 연세두리치과 22클릭
    치과 ② 사랑니빠지는치과 3 · 신나라치과 3 · 사랑니빠지는 2
    치과 ③ 연세365감동치과 10 · 정자동365일치과 3 · 배문석 치과 3 ·
           수원 연세365감동치과 1
  '배문석 치과'는 원장님 성함이다. 상호보다 더 조심해야 한다.
  좌표는 --grid 로 한 줄씩 실측했다(2026-09-13).

  그래프·요약 숫자·나머지 검색어는 그대로 둔다. 가린 줄이 눈에 보이는 편이
  낫다 — 사이트에 '병원명은 가렸습니다'라고 적어 뒀으니 가린 자국이 그 말을
  증명한다. 잘라내면 표를 손댄 게 안 보인다.
"""
import io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, 'assets', 'naver')
OUT  = os.path.join(HERE, 'images')
WP   = '/wp-content/uploads/ciclo/'

SHOTS = [
 dict(stem='naver-1', file='KakaoTalk_20260910_235544556.png',
      id='치과 ①', tag='수도권 · 종합진료',
      sum='740클릭 · 6.4만 노출 · CTR 1.2% · 직전 90일 대비 클릭 +12,300%',
      masks=['0.105,0.597,0.22,0.024']),                       # 연세두리치과
 dict(stem='naver-2', file='KakaoTalk_20260910_235404303.png',
      id='치과 ②', tag='인천 · 사랑니 중심',
      sum='110클릭 · 1.9만 노출 · CTR 0.6% · 직전 90일 대비 클릭 +1,733%',
      masks=['0.100,0.624,0.23,0.026',                          # 사랑니빠지는치과
             '0.100,0.710,0.23,0.026',                          # 신나라치과
             '0.100,0.795,0.23,0.026']),                        # 사랑니빠지는
 dict(stem='naver-3', file='KakaoTalk_20260910_235453127.png',
      id='치과 ③', tag='수도권 · 개원 초기',
      sum='74클릭 · 1.4만 노출 · CTR 0.5% · 직전 90일 대비 클릭 +7,300%',
      masks=['0.105,0.598,0.25,0.024',                          # 연세365감동치과
             '0.105,0.679,0.25,0.024',                          # 정자동365일치과
             '0.105,0.721,0.25,0.024',                          # 배문석 치과 (원장 성함)
             '0.105,0.886,0.25,0.024']),                        # 수원 연세365감동치과
]

def convert(s):
    src = os.path.join(SRC, s['file'])
    if not os.path.exists(src): sys.exit('없음: ' + src)
    out = os.path.join(OUT, s['stem'] + '.webp')
    cmd = ['node', os.path.join(HERE, 'tools', 'img2webp.js'),
           '--in', src, '--out', out, '--width', '1000', '--quality', '82']
    for m in s['masks']: cmd += ['--mask', m]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0: sys.exit('변환 실패 %s\n%s' % (s['stem'], r.stderr))
    print(r.stdout.rstrip())
    d = re.search(r'^DIM (\d+) (\d+)$', r.stdout, re.M)
    if not d: sys.exit('치수를 읽지 못함 %s' % s['stem'])
    return int(d.group(1)), int(d.group(2))

os.makedirs(OUT, exist_ok=True)
figs = []
for s in SHOTS:
    w, h = convert(s)
    alt = ('네이버 서치어드바이저 %s 최근 90일 화면 — %s' % (s['id'], s['sum']))
    figs.append(
'      <figure class="nv-shot">\n'
'        <img src="%s%s.webp" alt="%s"\n'
'             width="%d" height="%d" loading="lazy" decoding="async">\n'
'        <figcaption><b>%s · %s</b> · 병원 상호가 들어간 검색어는 가렸습니다</figcaption>\n'
'      </figure>\n' % (WP, s['stem'], alt, w, h, s['id'], s['tag']))

BLOCK = '    <div class="nv-shots">\n' + ''.join(figs) + '    </div>\n'

P = os.path.join(HERE, 'pages', 'Home.html')
t = io.open(P, encoding='utf-8').read()
if '<figure class="nv-shot">' in t:
    print('..  이미 들어 있음')
else:
    A = '    <div class="kw-cards">'
    if t.count(A) != 1: sys.exit('FAIL: .kw-cards 앵커 %d개' % t.count(A))
    t = t.replace(A, BLOCK + A, 1)
    io.open(P, 'w', encoding='utf-8').write(t)
    print('ok  pages/Home.html — 캡처 3장 삽입')

CSS = u'''

/* ── 서치어드바이저 캡처 ──
   세로로 긴 화면이라 3단으로 놓으면 글자가 안 읽힌다. 폭을 주고 가로로 민다.
   바로 아래 .kw-cards 가 같은 내용을 기계가 읽는 표로 다시 싣는다. */
.nv-shots{margin-top:clamp(20px,2.4vw,30px);display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,1.8vw,22px)}
.nv-shot{margin:0;min-width:0}
.nv-shot img{display:block;width:100%;height:auto;background:#fff;
  border:1px solid rgba(18,18,18,.12);border-radius:10px}
.nv-shot figcaption{margin-top:10px;font-size:12px;line-height:1.6;font-weight:400;
  color:rgba(18,18,18,.62)}
.nv-shot figcaption b{font-weight:700;color:rgba(18,18,18,.8)}
@media(max-width:860px){.nv-shots{grid-template-columns:1fr;max-width:560px}}
'''
c = os.path.join(HERE, 'css', 'global.css')
x = io.open(c, encoding='utf-8').read()
if '.nv-shots' not in x:
    io.open(c, 'w', encoding='utf-8').write(x.rstrip('\n') + '\n' + CSS)
    print('CSS 추가')
