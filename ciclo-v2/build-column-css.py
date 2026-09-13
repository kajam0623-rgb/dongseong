#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""칼럼·글 상세 CSS — eael-* 를 col-* 로 교체하고 글 상세를 새로 쓴다.

테마에서 Essential Addons 를 걷어내면서 칼럼 목록을 WP 루프로 다시 그렸다.
그에 맞춰 CSS 도 플러그인 클래스(eael-*)에서 우리 클래스(col-*)로 바꾼다.

같이 정리되는 것
  · `!important` 12개가 사라진다. 플러그인 기본 스타일을 이기려고 붙였던 것들이라
    우리가 마크업을 그리는 지금은 필요 없다.
  · 플러그인이 마크업을 바꾸면 깨지던 의존이 없어진다.

글 상세(single.php)는 원래 스타일이 아예 없었다. 워드프레스 에디터가 만드는
h2/h3/p/ul/blockquote/img 를 읽을 만하게 잡아 준다. 사이트 토큰을 그대로 쓴다.
"""
import sys, io, os, re

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'css', 'global.css')
s = io.open(P, encoding='utf-8').read()

# ── 기존 eael 블록 찾기 ────────────────────────────────────────
start = s.find('.ciclo-column .eael-post-grid{')
if start < 0:
    sys.exit('FAIL: eael 블록을 찾지 못함')
end_marker = "@media(max-width:600px){.ciclo-column .eael-grid-post-holder"
end = s.find(end_marker, start)
if end < 0:
    sys.exit('FAIL: eael 블록 끝을 찾지 못함')
end = s.find('\n', end) + 1
old_block = s[start:end]
print('교체 대상 %d B · !important %d개' % (len(old_block), old_block.count('!important')))

NEW = """/* 칼럼 목록 — 워드프레스 루프로 직접 그린다.
   전에는 Essential Addons Post Grid 위젯이 그리고 우리가 !important 12개로
   덮어쓰는 구조였다. 테마에서 플러그인을 걷어내면서 마크업을 우리가 쥐게 돼
   덮어쓸 이유가 없어졌다. */
.col-main{min-width:0}
.col-list{margin-top:clamp(32px,3.6vw,48px);display:flex;flex-direction:column}
.col-post{display:flex;gap:clamp(20px,2.4vw,30px);align-items:flex-start;
  padding:clamp(26px,2.8vw,34px) 0;border-top:1px solid rgba(18,18,18,.12)}
.col-post:first-child{border-top:0;padding-top:0}
.col-media{flex:0 0 258px;max-width:258px;border-radius:14px;overflow:hidden;display:block}
.col-media img{width:100%;height:168px;object-fit:cover;display:block;background:var(--panel)}
.col-body{flex:1;min-width:0}
.col-title{margin:0;font-size:clamp(19px,2.2vw,24px);font-weight:800;letter-spacing:-.02em;
  line-height:1.32;word-break:keep-all}
.col-title a{color:var(--ink)}
.col-title a:hover{color:var(--pt)}
.col-excerpt{margin-top:10px;font-size:15px;line-height:1.72;color:rgba(18,18,18,.62)}
.col-meta{margin-top:14px;display:flex;flex-wrap:wrap;align-items:center;gap:10px;
  font-size:12.5px;letter-spacing:.04em;color:rgba(18,18,18,.62);font-variant-numeric:tabular-nums}
.col-cat{background:rgba(17,30,108,.08);color:var(--pt);font-weight:700;padding:3px 9px;border-radius:4px;letter-spacing:0}
.col-pager{margin-top:clamp(36px,4vw,52px);display:flex;flex-wrap:wrap;gap:8px}
.col-pager a,.col-pager .current,.col-pager .page-numbers{display:inline-flex;align-items:center;
  justify-content:center;min-width:40px;height:40px;padding:0 12px;border:1px solid rgba(18,18,18,.16);
  border-radius:4px;font-size:14px;font-weight:700;color:var(--pt)}
.col-pager a:hover{border-color:var(--pt);background:rgba(17,30,108,.05)}
.col-pager .current{background:var(--pt);border-color:var(--pt);color:#fff}
@media(max-width:600px){
  .col-post{flex-direction:column;gap:14px}
  .col-media{flex-basis:auto;max-width:none;width:100%}
  .col-media img{height:200px}
}

/* 칼럼 글 상세 — 읽기 한 단.
   본문은 워드프레스 에디터가 만든 것이라 태그를 예측할 수 없다.
   h2/h3/p/ul/ol/blockquote/img/code 를 사이트 토큰으로 잡아 둔다. */
.post-wrap{max-width:760px;margin:0 auto;
  padding:clamp(96px,11vw,150px) clamp(20px,5vw,48px) clamp(60px,7vw,90px)}
.post-head{padding-bottom:clamp(26px,3vw,36px);border-bottom:1px solid rgba(18,18,18,.14)}
.post-title{margin:18px 0 0;font-size:clamp(28px,4vw,44px);font-weight:800;line-height:1.28;
  letter-spacing:-.028em;word-break:keep-all}
.post-meta{margin-top:18px;font-size:13.5px;color:rgba(18,18,18,.62);font-variant-numeric:tabular-nums}
.post-cover{margin:clamp(30px,3.4vw,44px) 0 0;border-radius:14px;overflow:hidden}
.post-cover img{width:100%;height:auto;display:block}

.post-body{margin-top:clamp(32px,3.6vw,48px);font-size:17px;line-height:1.85;
  color:rgba(18,18,18,.86);word-break:keep-all}
.post-body>*+*{margin-top:1.15em}
.post-body h2{margin-top:2em;font-size:clamp(21px,2.4vw,27px);font-weight:800;line-height:1.35;
  letter-spacing:-.02em}
.post-body h3{margin-top:1.7em;font-size:clamp(18px,2vw,21px);font-weight:700;line-height:1.4;
  letter-spacing:-.015em}
.post-body ul,.post-body ol{padding-left:1.3em}
.post-body li+li{margin-top:.5em}
.post-body a{color:var(--pt);text-decoration:underline;text-underline-offset:3px}
.post-body img{max-width:100%;height:auto;border-radius:10px}
.post-body figure{margin:1.6em 0}
.post-body figcaption{margin-top:10px;font-size:13px;color:rgba(18,18,18,.62)}
.post-body blockquote{margin:1.6em 0;padding:18px 22px;background:rgba(17,30,108,.05);
  border-left:2px solid var(--pt);font-size:16px;line-height:1.8}
.post-body blockquote p{margin:0}
.post-body code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.9em;
  background:rgba(18,18,18,.06);padding:2px 6px;border-radius:4px}
.post-body pre{overflow-x:auto;padding:18px 20px;background:var(--panel);border-radius:8px}
.post-body pre code{background:none;padding:0}
.post-body hr{margin:2.2em 0;border:0;border-top:1px solid rgba(18,18,18,.14)}
.post-body table{width:100%;border-collapse:collapse;font-size:15px}
.post-body th,.post-body td{padding:11px 10px;border-bottom:1px solid rgba(18,18,18,.12);text-align:left}

.post-foot{margin-top:clamp(40px,4.4vw,60px);padding-top:clamp(26px,3vw,34px);
  border-top:1px solid rgba(18,18,18,.14)}

.post-nav{max-width:760px;margin:0 auto;padding:0 clamp(20px,5vw,48px) clamp(80px,9vw,120px);
  display:grid;grid-template-columns:1fr 1fr;gap:clamp(14px,1.8vw,22px)}
.post-nav-item{display:block;padding:22px 24px;border:1px solid rgba(18,18,18,.14);border-radius:12px;
  transition:border-color .15s cubic-bezier(.4,0,.2,1)}
.post-nav-item:hover{border-color:var(--pt)}
.post-nav-item span{display:block;font-size:12px;font-weight:700;letter-spacing:.14em;color:rgba(18,18,18,.62)}
.post-nav-item b{display:block;margin-top:9px;font-size:15.5px;font-weight:700;line-height:1.5;
  letter-spacing:-.015em;color:var(--ink);word-break:keep-all}
.post-nav-item.next{text-align:right}
@media(max-width:600px){.post-nav{grid-template-columns:1fr}.post-nav-item.next{text-align:left}}
"""

s = s[:start] + NEW + s[end:]
io.open(P, 'w', encoding='utf-8').write(s)
print('ok  css/global.css — col-* / post-* 로 교체')
print('    남은 eael 참조: %d' % s.count('eael'))
