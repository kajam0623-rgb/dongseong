#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""서치어드바이저 캡처에서 읽은 값으로 실적 블록을 채운다.

캡처 3장(사용자 제공)에서 새로 읽은 것
  · 노출 증가율 — +9,099.4% / +1,486.1% / +902.9%  (카드에 없던 값)
  · 측정 조건   — 최근 90일 · PC+Mobile · 06.12~09.09 · 최근 업데이트 2026.09.09
  · 검색 키워드 TOP 30  ← 이게 제일 크다

왜 키워드가 %보다 센가
  "+12,300%" 는 배수라서 시작점이 작으면 아무 의미가 없다(그래서 바로 밑에
  직전 90일 클릭이 한 자리였다고 적어 뒀다). 반면 키워드 표는 "환자분이
  실제로 무엇을 검색해서 들어왔는가"다. 씨클로가 파는 게 정확히 그거다 —
  진료과목을 나누고 환자가 던지는 질문을 제목으로 쓰는 일.
  그 주장을 이 표가 그대로 증명한다.

  그리고 한 가지가 더 읽힌다. 상위 키워드 대부분이 병원 이름이 아니다.
  증상과 시술 질문이다. 간판 검색이 아니라 모르는 사람이 찾아온 유입이라는
  뜻이고, 이건 캡처를 안 열어보면 알 수 없는 사실이다.

병원 식별 정보는 뺀다
  캡처의 1위 키워드는 세 곳 다 병원 상호였다(연세두리치과 22클릭,
  연세365감동치과 10클릭, 신나라치과 3클릭). 원장님 성함이 들어간 줄도 있었다.
  사이트에 "병원명은 가렸습니다" 라고 적어 뒀으므로 상호·인명 줄은 싣지 않는다.
  뺀 사실 자체는 표 밑에 적는다 — 빼놓고 말 안 하면 그것도 가리는 것이다.

  CTR 이 200% 로 찍힌 줄도 뺐다(노출 1 · 클릭 2). 서치어드바이저 집계
  특성이지 성과가 아니라서, 실으면 표 전체가 의심받는다.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'pages', 'Home.html')
s = io.open(P, encoding='utf-8').read()

# ── 1. 카드에 노출 증가율 추가 ────────────────────────────────
ADD = [
 ('<div class="res-row"><dt>노출</dt><dd>6.4만</dd></div>',
  '<div class="res-row"><dt>노출</dt><dd>6.4만 <i class="up">+9,099%</i></dd></div>'),
 ('<div class="res-row"><dt>노출</dt><dd>1.9만</dd></div>',
  '<div class="res-row"><dt>노출</dt><dd>1.9만 <i class="up">+1,486%</i></dd></div>'),
 ('<div class="res-row"><dt>노출</dt><dd>1.4만</dd></div>',
  '<div class="res-row"><dt>노출</dt><dd>1.4만 <i class="up">+903%</i></dd></div>'),
 ('<span class="res-src">출처: 네이버 서치어드바이저 · 직전 90일 대비</span>',
  '<span class="res-src">출처: 네이버 서치어드바이저 · 최근 90일 · PC+Mobile · 2026.09.09 기준</span>'),
]
for a, b in ADD:
    if a not in s: sys.exit('FAIL: ' + a[:60])
    s = s.replace(a, b, 1)

# ── 2. 키워드 표 블록 ────────────────────────────────────────
KW = {
 '치과 ①': ('수도권 · 종합진료', [
    ('사랑니 발치후 식사', 21, '395', '5.3'),
    ('임플란트 식단',      20, '105', '19.0'),
    ('20대 임플란트',      17, '363', '4.7'),
    ('임플란트 수술 후 식사', 14, '479', '2.9'),
    ('임플란트 붓기 언제까지', 14, '40', '35.0'),
    ('임플란트 음식',      12, '165', '7.3'),
    ('사랑니 썩음',         9, '273', '3.3'),
    ('스케일링 피',         8, '452', '1.8'),
 ]),
 '치과 ②': ('인천 · 사랑니 중심', [
    ('혓바닥 혹',            3, '27',  '11.1'),
    ('구월동 사랑니 발치 전문', 2, '532', '0.4'),
    ('혀 자극성 섬유종',      2, '14',  '14.3'),
    ('구월동 사랑니 잘 뽑는 치과', 2, '11', '18.2'),
    ('구월동 사랑니 치과',    1, '653', '0.2'),
    ('인천 사랑니 전문 치과',  1, '554', '0.2'),
 ]),
 '치과 ③': ('수도권 · 개원 초기', [
    ('수원 사랑니 수면마취',  3, '10',  '30.0'),
    ('수원정자동치과',       2, '66',  '3.0'),
    ('수원 정자동 사랑니',    1, '86',  '1.2'),
    ('수원 미세현미경 치과',  1, '49',  '2.0'),
 ]),
}

rows = []
for cid, (tag, ks) in KW.items():
    tr = '\n'.join(
      '          <div class="kw-row"><span class="kw-q">%s</span>'
      '<span class="kw-c">%d</span><span class="kw-i">%s</span>'
      '<span class="kw-r">%s%%</span></div>' % (q, c, i, r) for q, c, i, r in ks)
    rows.append(
'''      <article class="kw-card">
        <div class="res-top"><span class="res-id">%s</span><span class="res-tag">%s</span></div>
        <div class="kw-head"><span>검색어</span><span>클릭</span><span>노출</span><span>CTR</span></div>
        <div class="kw-list">
%s
        </div>
      </article>''' % (cid, tag, tr))

BLOCK = '''
  <div class="res-block">
    <div class="res-head">
      <h3>어떤 검색어로 들어왔나</h3>
      <span class="res-src">출처: 네이버 서치어드바이저 검색 키워드 · 최근 90일</span>
    </div>
    <p class="kw-lead">클릭 수가 아니라 <b>검색어</b>입니다. 세 곳 모두 상위 검색어 대부분이 병원 이름이 아니라 증상과 시술 질문이었습니다. 간판을 알고 찾아온 유입이 아니라 모르는 사람이 찾아온 유입입니다.</p>
    <div class="kw-cards">
%s
    </div>
    <p class="sec-caption">병원 상호와 원장님 성함이 들어간 검색어는 뺐습니다. 세 곳 모두 상호 검색이 1위였고, 클릭은 각각 22 · 3 · 10이었습니다. 노출 1건에 클릭 2건으로 CTR이 200%%로 찍힌 줄도 뺐습니다. 서치어드바이저 집계 특성이지 성과가 아닙니다.</p>
  </div>
''' % '\n'.join(rows)

ANCHOR = '  <div class="res-block">\n    <div class="res-head">\n      <h3>페이지 속도'
if ANCHOR not in s: sys.exit('FAIL: PSI 블록 앵커를 찾지 못함')
s = s.replace(ANCHOR, BLOCK + ANCHOR, 1)
io.open(P, 'w', encoding='utf-8').write(s)
print('키워드 블록 추가 · 카드 4곳 보강')

CSS = u'''

/* ── 검색 키워드 표 ──
   캡처에서 읽은 검색어 목록. 실적 %는 배수라 시작점이 작으면 의미가 흐려지는데,
   검색어는 "환자분이 무엇을 검색해 들어왔는가" 라서 흐려질 여지가 없다.
   씨클로가 파는 것(질문을 제목으로 쓰는 일)을 그대로 증명하는 자리다. */
.kw-lead{margin-top:clamp(16px,1.8vw,22px);max-width:74ch;font-size:15.5px;line-height:1.7;
  font-weight:400;color:rgba(18,18,18,.72)}
.kw-cards{margin-top:clamp(20px,2.4vw,30px);display:grid;grid-template-columns:repeat(3,1fr);
  gap:clamp(16px,2vw,26px)}
.kw-card{background:var(--card);border:1px solid rgba(18,18,18,.1);border-radius:12px;
  padding:clamp(20px,1.9vw,26px) clamp(18px,1.7vw,22px);
  transition:border-color .18s cubic-bezier(.4,0,.2,1),transform .28s cubic-bezier(.22,1,.36,1)}
.kw-card:hover{transform:translateY(-3px);border-color:rgba(17,30,108,.3)}
.kw-head,.kw-row{display:grid;grid-template-columns:1fr 38px 52px 46px;gap:6px;align-items:baseline}
.kw-head{margin-top:16px;padding-bottom:8px;border-bottom:1px solid rgba(18,18,18,.14);
  font-size:11px;font-weight:700;letter-spacing:.08em;color:rgba(18,18,18,.55)}
.kw-head span+span,.kw-row span+span{text-align:right;font-variant-numeric:tabular-nums}
.kw-row{padding:9px 0;border-bottom:1px solid rgba(18,18,18,.07);font-size:13px;line-height:1.4}
.kw-row:last-child{border-bottom:0}
.kw-q{font-weight:600;color:var(--ink);word-break:keep-all}
.kw-c{font-weight:800;color:var(--pt)}
.kw-i,.kw-r{font-weight:500;color:rgba(18,18,18,.6)}
/* 노출 증가율 — 카드 안 작은 배지 */
.res-rows .up{font-style:normal;margin-left:6px;font-size:11.5px;font-weight:700;
  color:rgba(17,30,108,.66)}
@media(max-width:900px){.kw-cards{grid-template-columns:1fr 1fr}}
@media(max-width:620px){.kw-cards{grid-template-columns:1fr}}
'''
c = os.path.join(HERE, 'css', 'global.css')
t = io.open(c, encoding='utf-8').read()
io.open(c, 'w', encoding='utf-8').write(t.rstrip('\n') + '\n' + CSS)
print('CSS 추가')
