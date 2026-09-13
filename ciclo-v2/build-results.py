#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""실적 밴드 (#results) 신설 — 플랜 A-3 "실적이 없다면 가상 사례를 만들지 말 것"의 해제.

사용자가 제공한 실측 캡처 5장(네이버 서치어드바이저 3 · PageSpeed Insights 2)의
수치를 근거로, 진단(#work)과 방법론(#process) 사이에 "고친 뒤 숫자가 어디로 갔나"를
넣는다. 캡처 이미지 자체는 디스크에 없으므로 HTML/CSS 로 재현했다.
(이미지 임베드보다 전송량 0 + 병원명 유출 위험 0 이라 성능 목표에도 맞다.)

238LAB 문법 준수: eyebrow → h2(한글 문장형) → lead → 근거 → 자사 한계 고백 → 출처 캡션.
증가율 세 자리·네 자리는 시작점이 낮았기 때문이라는 것을 같은 블록에서 밝힌다.
"""
import sys, io, re

def patch(path, pairs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit('FAIL %s: 앵커 %d회 발견 — %r' % (path, n, old[:70]))
        s = s.replace(old, new)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('ok  %s' % path)

# ─────────────────────────────── CSS ───────────────────────────────
CSS = r"""
/* ── 실적 밴드 (#results) ─────────────────────────────────────────
   네이버 서치어드바이저 · PageSpeed Insights 실측 캡처의 재현.
   팔레트는 씨클로 시스템(네이비/크림/옐로) 유지 — PSI 초록을 들이지 않는다. */
.res-block{margin-top:clamp(36px,4.4vw,60px)}
.res-block+.res-block{margin-top:clamp(52px,6vw,84px)}
.res-head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:10px 20px;
  padding-bottom:12px;border-bottom:1px solid rgba(18,18,18,.16)}
.res-head h3{margin:0;font-size:15px;font-weight:700;letter-spacing:-.01em}
.res-src{font-size:12.5px;font-weight:400;color:rgba(18,18,18,.5)}
.res-cards{margin-top:clamp(18px,2.2vw,26px);display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(14px,1.6vw,20px)}
.res-card{background:var(--card);border-top:2px solid var(--pt);padding:22px 22px 20px;display:flex;flex-direction:column}
.res-top{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px}
.res-id{font-family:Archivo,sans-serif;font-weight:800;font-size:13.5px;letter-spacing:.02em;color:var(--pt)}
.res-tag{font-size:11.5px;font-weight:600;color:rgba(18,18,18,.5);background:rgba(18,18,18,.05);padding:3px 8px;border-radius:4px}
.res-big{margin-top:16px;display:flex;align-items:baseline;gap:8px;font-variant-numeric:tabular-nums}
.res-big b{font-family:Archivo,'Arial Black',sans-serif;font-weight:900;font-size:clamp(38px,4.4vw,54px);
  line-height:.94;letter-spacing:-.03em;color:var(--pt)}
.res-big span{font-size:14px;font-weight:600;color:rgba(18,18,18,.55)}
.res-delta{margin-top:10px;display:inline-flex;align-items:center;gap:6px;align-self:flex-start;
  font-size:13px;font-weight:700;color:var(--pt);background:rgba(17,30,108,.08);padding:5px 10px;border-radius:4px}
.res-delta i{font-style:normal}
.res-rows{margin-top:16px;padding-top:14px;border-top:1px solid rgba(18,18,18,.1);display:flex;flex-direction:column;gap:7px}
.res-row{display:flex;justify-content:space-between;gap:12px;font-size:13.5px;font-variant-numeric:tabular-nums}
.res-row dt{color:rgba(18,18,18,.55)}
.res-row dd{margin:0;font-weight:700}
.res-note{margin-top:clamp(20px,2.4vw,28px);max-width:64ch;padding:18px 20px;background:rgba(17,30,108,.05);
  border-left:2px solid var(--pt);font-size:15px;line-height:1.72;color:rgba(18,18,18,.72)}
.res-note b{font-weight:700;color:var(--ink)}
/* PageSpeed */
.psi-cards{margin-top:clamp(18px,2.2vw,26px);display:grid;grid-template-columns:1fr 1fr;gap:clamp(14px,1.6vw,20px)}
.psi-card{background:var(--card);border-top:2px solid var(--pt);padding:22px 22px 20px}
.psi-scores{margin-top:18px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.psi-s{text-align:center}
.psi-ring{width:clamp(44px,5vw,58px);height:clamp(44px,5vw,58px);margin:0 auto;border:3px solid var(--pt);
  border-radius:50%;display:grid;place-items:center;font-family:Archivo,sans-serif;font-weight:800;
  font-size:clamp(14px,1.5vw,17px);color:var(--pt);font-variant-numeric:tabular-nums}
.psi-s small{display:block;margin-top:8px;font-size:11.5px;line-height:1.35;color:rgba(18,18,18,.55)}
.psi-vitals{margin-top:18px;padding-top:14px;border-top:1px solid rgba(18,18,18,.1);
  display:grid;grid-template-columns:repeat(5,1fr);gap:8px;font-variant-numeric:tabular-nums}
.psi-v{text-align:left}
.psi-v b{display:block;font-family:Archivo,sans-serif;font-weight:800;font-size:14.5px;letter-spacing:-.01em}
.psi-v small{display:block;margin-top:4px;font-size:11px;line-height:1.3;color:rgba(18,18,18,.5)}
@media(max-width:900px){.res-cards{grid-template-columns:1fr 1fr}.psi-cards{grid-template-columns:1fr}}
@media(max-width:620px){.res-cards{grid-template-columns:1fr}.psi-vitals{grid-template-columns:repeat(3,1fr);gap:12px 8px}}
"""

ANCHOR_CSS = '@media(max-width:700px){.dtable-hint{display:block}}\n'
patch('css/global.css', [(ANCHOR_CSS, ANCHOR_CSS + CSS)])

# ─────────────────────────────── Home ───────────────────────────────
NAVER_NOTE = (
  '<p class="res-note">증가율이 세 자리·네 자리로 보이는 이유를 같이 적습니다. '
  '<b>세 곳 모두 직전 90일 클릭이 한 자리였습니다.</b> 740클릭은 6클릭에서 온 값이고, '
  '74클릭은 1클릭에서 온 값입니다. 배수만 보시면 실제 크기를 잘못 읽게 됩니다. '
  '저희가 말할 수 있는 것은 "없던 유입이 생겼다"까지이고, '
  '이 숫자로 매출이나 내원 건수를 말하지는 않겠습니다.</p>'
)

RESULTS = '''
<section class="section panel" id="results"><div class="wrap">
  <div class="overline">/RESULT · 저희가 맡은 사이트</div>
  <h2 class="sec-h2">진단에서 멈추지 않았습니다,<br>고친 뒤 숫자가 어디로 갔는지도 엽니다</h2>
  <p class="sec-lead">네이버 서치어드바이저와 PageSpeed Insights가 매긴 값을 그대로 옮겼습니다. 저희가 계산한 수치가 아니라 두 도구의 화면에 찍힌 값입니다. 병원명과 주소는 가렸습니다.</p>

  <div class="res-block">
    <div class="res-head">
      <h3>검색 유입 — 최근 90일</h3>
      <span class="res-src">출처: 네이버 서치어드바이저 · 직전 90일 대비</span>
    </div>
    <div class="res-cards">
      <article class="res-card">
        <div class="res-top"><span class="res-id">치과 ①</span><span class="res-tag">수도권 · 종합진료</span></div>
        <div class="res-big"><b>740</b><span>클릭</span></div>
        <div class="res-delta"><i>↑</i>직전 90일 대비 +12,300%</div>
        <dl class="res-rows">
          <div class="res-row"><dt>노출</dt><dd>6.4만</dd></div>
          <div class="res-row"><dt>클릭률</dt><dd>1.2%</dd></div>
          <div class="res-row"><dt>직전 90일 클릭</dt><dd>약 6</dd></div>
        </dl>
      </article>
      <article class="res-card">
        <div class="res-top"><span class="res-id">치과 ②</span><span class="res-tag">인천 · 사랑니 중심</span></div>
        <div class="res-big"><b>110</b><span>클릭</span></div>
        <div class="res-delta"><i>↑</i>직전 90일 대비 +1,733%</div>
        <dl class="res-rows">
          <div class="res-row"><dt>노출</dt><dd>1.9만</dd></div>
          <div class="res-row"><dt>클릭률</dt><dd>0.6%</dd></div>
          <div class="res-row"><dt>직전 90일 클릭</dt><dd>약 6</dd></div>
        </dl>
      </article>
      <article class="res-card">
        <div class="res-top"><span class="res-id">치과 ③</span><span class="res-tag">수도권 · 개원 초기</span></div>
        <div class="res-big"><b>74</b><span>클릭</span></div>
        <div class="res-delta"><i>↑</i>직전 90일 대비 +7,300%</div>
        <dl class="res-rows">
          <div class="res-row"><dt>노출</dt><dd>1.4만</dd></div>
          <div class="res-row"><dt>클릭률</dt><dd>0.5%</dd></div>
          <div class="res-row"><dt>직전 90일 클릭</dt><dd>약 1</dd></div>
        </dl>
      </article>
    </div>
    ''' + NAVER_NOTE + '''
  </div>

  <div class="res-block">
    <div class="res-head">
      <h3>페이지 속도 — 저희가 만든 사이트 실측</h3>
      <span class="res-src">출처: PageSpeed Insights (Lighthouse) · 실제 URL 측정</span>
    </div>
    <div class="psi-cards">
      <article class="psi-card">
        <div class="res-top"><span class="res-id">치과 ④</span><span class="res-tag">모바일 측정</span></div>
        <div class="psi-scores">
          <div class="psi-s"><div class="psi-ring">100</div><small>성능</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>접근성</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>권장사항</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>검색<br>엔진 최적화</small></div>
        </div>
        <div class="psi-vitals">
          <div class="psi-v"><b>1.0초</b><small>첫 콘텐츠</small></div>
          <div class="psi-v"><b>1.7초</b><small>최대 콘텐츠</small></div>
          <div class="psi-v"><b>0ms</b><small>차단 시간</small></div>
          <div class="psi-v"><b>0.003</b><small>레이아웃 이동</small></div>
          <div class="psi-v"><b>1.8초</b><small>속도 지수</small></div>
        </div>
      </article>
      <article class="psi-card">
        <div class="res-top"><span class="res-id">치과 ⑤</span><span class="res-tag">데스크톱 측정</span></div>
        <div class="psi-scores">
          <div class="psi-s"><div class="psi-ring">100</div><small>성능</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>접근성</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>권장사항</small></div>
          <div class="psi-s"><div class="psi-ring">100</div><small>검색<br>엔진 최적화</small></div>
        </div>
        <div class="psi-vitals">
          <div class="psi-v"><b>0.4초</b><small>첫 콘텐츠</small></div>
          <div class="psi-v"><b>0.6초</b><small>최대 콘텐츠</small></div>
          <div class="psi-v"><b>10ms</b><small>차단 시간</small></div>
          <div class="psi-v"><b>0.006</b><small>레이아웃 이동</small></div>
          <div class="psi-v"><b>0.6초</b><small>속도 지수</small></div>
        </div>
      </article>
    </div>
    <p class="res-note">네 항목 100점은 <b>빠르다는 뜻이지 잘 팔린다는 뜻이 아닙니다.</b> 다만 앞의 실태조사에서 본 대로, 기계가 읽는 자리가 비어 있으면 속도만 좋아도 검색과 AI 답변에서는 불리합니다. 저희는 이 두 가지를 같은 단계에서 맞춥니다.</p>
  </div>

  <p class="sec-caption">네이버 서치어드바이저 최근 90일 기준(2026년 9월 측정) · PageSpeed Insights 실측 · 병원명·주소·도메인은 가렸습니다 · 클릭률 1.2%는 업계 평균을 넘는 값이 아닙니다. 이 표는 유입이 늘었다는 사실까지만 말합니다 · 같은 조건에서 같은 결과를 보장하지 않습니다</p>
  <a class="sec-link" href="/contact/">우리 사이트는 지금 몇 점인지 무료로 진단받기 →</a>
</div></section>
'''

patch('pages/Home.html', [
    ('\n<section class="section navy" id="process">',
     RESULTS + '<section class="section navy" id="process">'),
])
