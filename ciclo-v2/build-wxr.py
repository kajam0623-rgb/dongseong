#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""워드프레스 가져오기 파일(WXR) 생성 — 페이지 10개 + 칼럼 카테고리 7개.

무엇을 만드나
  · 페이지 10개 — 템플릿이 슬러그로 붙으므로 **본문은 비운다**.
    디자인과 문구는 전부 테마의 *.php 안에 있다. 페이지는 "주소를 만들어
    주는 껍데기"일 뿐이다. 이게 이 구조의 핵심이다.
  · 칼럼 카테고리 7개 — 테마 사이드바 메뉴가 이 슬러그를 찾는다.
  · 칼럼 샘플 글 1편 — 목록·상세가 제대로 나오는지 바로 확인하라고 넣는다.
    확인 뒤 지우면 된다.

왜 본문이 비어 있나
  기존 방식은 페이지 마크업을 Elementor 의 `_elementor_data` JSON 안에
  이스케이프해서 넣었다. 그래서 문구 하나 고치려면 JSON 을 다시 만들어야 했고,
  가져오기를 다시 하면 기존 편집이 날아갔다. 테마 템플릿에 두면 파일만 고치면
  되고, 가져오기는 처음 한 번이면 끝난다.

WXR 은 RSS 2.0 확장이다. 워드프레스 기본 가져오기 도구가 읽는다.
"""
import io, os, datetime, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'ciclo-import.xml')

SITE = 'https://ciclo.kr'
AUTHOR = 'ciclo'
AUTHOR_NAME = 'CICLO'
AUTHOR_EMAIL = 'kajam0623@naver.com'

now = datetime.datetime(2026, 9, 13, 9, 0, 0)

# (제목, 슬러그, 메뉴순서) — 슬러그가 테마 템플릿 이름과 짝이다
PAGES = [
    ('홈',                  'home',                1),
    ('Work',               'work',                2),
    ('About',              'about',               3),
    ('Contact',            'contact',             4),
    ('칼럼',                'column',              5),
    ('Website Design',     'website-design',      6),
    ('GEO',                'geo',                 7),
    ('Blog Content',       'blog-content',        8),
    ('Digital Marketing',  'digital-marketing',   9),
    ('치과 홈페이지 제작',    'dental',             10),
]

CATS = [
    ('검색엔진최적화 (SEO)', 'seo'),
    ('GEO · AI 검색',       'geo'),
    ('병의원 마케팅',        'hospital'),
    ('블로그 콘텐츠',        'content'),
    ('광고 운영',           'ads'),
    ('고객 사례',           'case'),
    ('인사이트',            'insight'),
]

SAMPLE_BODY = """<p>이 글은 <strong>테마가 제대로 붙었는지 확인하는 용도</strong>입니다.
칼럼 목록과 이 상세 화면이 정상으로 보이면 지우셔도 됩니다.</p>

<h2>확인할 것</h2>
<p>목록에서는 썸네일·제목·요약·날짜·카테고리가 한 줄로 놓이고, 상세에서는
제목 아래 본문이 한 단으로 흐릅니다. 아래 요소들이 사이트 톤으로 보이는지
같이 봐 주세요.</p>

<ul>
<li>목록 항목은 이렇게 보입니다</li>
<li>줄 간격과 글머리 기호 위치</li>
</ul>

<h3>인용</h3>
<blockquote><p>인용문은 왼쪽에 네이비 선이 붙고 옅은 배경이 깔립니다.</p></blockquote>

<h3>표</h3>
<table>
<thead><tr><th>항목</th><th>값</th></tr></thead>
<tbody><tr><td>검색</td><td>84</td></tr><tr><td>AI 답변</td><td>56</td></tr></tbody>
</table>

<p>본문 링크는 <a href="https://ciclo.kr/column/">이렇게</a> 밑줄로 보입니다.</p>
"""


def cdata(t):
    return '<![CDATA[' + t.replace(']]>', ']]]]><![CDATA[>') + ']]>'


def page_item(title, slug, order, pid):
    return f"""	<item>
		<title>{cdata(title)}</title>
		<link>{SITE}/{slug}/</link>
		<pubDate>{now.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
		<dc:creator>{cdata(AUTHOR)}</dc:creator>
		<guid isPermaLink="false">{SITE}/?page_id={pid}</guid>
		<description></description>
		<content:encoded>{cdata('')}</content:encoded>
		<excerpt:encoded>{cdata('')}</excerpt:encoded>
		<wp:post_id>{pid}</wp:post_id>
		<wp:post_date>{cdata(now.strftime('%Y-%m-%d %H:%M:%S'))}</wp:post_date>
		<wp:post_date_gmt>{cdata(now.strftime('%Y-%m-%d %H:%M:%S'))}</wp:post_date_gmt>
		<wp:comment_status>{cdata('closed')}</wp:comment_status>
		<wp:ping_status>{cdata('closed')}</wp:ping_status>
		<wp:post_name>{cdata(slug)}</wp:post_name>
		<wp:status>{cdata('publish')}</wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>{order}</wp:menu_order>
		<wp:post_type>{cdata('page')}</wp:post_type>
		<wp:post_password>{cdata('')}</wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
	</item>
"""


def post_item(title, slug, body, pid, cat_name, cat_slug):
    return f"""	<item>
		<title>{cdata(title)}</title>
		<link>{SITE}/{slug}/</link>
		<pubDate>{now.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
		<dc:creator>{cdata(AUTHOR)}</dc:creator>
		<guid isPermaLink="false">{SITE}/?p={pid}</guid>
		<description></description>
		<content:encoded>{cdata(body)}</content:encoded>
		<excerpt:encoded>{cdata('')}</excerpt:encoded>
		<wp:post_id>{pid}</wp:post_id>
		<wp:post_date>{cdata(now.strftime('%Y-%m-%d %H:%M:%S'))}</wp:post_date>
		<wp:post_date_gmt>{cdata(now.strftime('%Y-%m-%d %H:%M:%S'))}</wp:post_date_gmt>
		<wp:comment_status>{cdata('closed')}</wp:comment_status>
		<wp:ping_status>{cdata('closed')}</wp:ping_status>
		<wp:post_name>{cdata(slug)}</wp:post_name>
		<wp:status>{cdata('publish')}</wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type>{cdata('post')}</wp:post_type>
		<wp:post_password>{cdata('')}</wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<category domain="category" nicename="{cat_slug}">{cdata(cat_name)}</category>
	</item>
"""


parts = []
parts.append(f"""<?xml version="1.0" encoding="UTF-8" ?>
<!--
  CICLO 워드프레스 가져오기 파일
  ================================================================
  만드는 것
    · 페이지 10개  (본문 비어 있음 — 디자인은 테마 템플릿에 있습니다)
    · 칼럼 카테고리 7개
    · 칼럼 샘플 글 1편 (확인용, 지우셔도 됩니다)

  넣는 법
    도구 > 가져오기 > WordPress > 실행 > 이 파일 선택
    "작성자 할당"은 본인 계정으로, "첨부 파일 내려받기"는 체크 안 해도 됩니다.

  ★ 먼저 CICLO 테마를 활성화한 뒤에 가져오세요.
    페이지는 슬러그로 템플릿과 짝을 이룹니다. 본문이 비어 있는 것이 정상입니다.

  가져온 뒤 한 가지만 설정하세요
    설정 > 읽기 > "홈페이지 표시"를 "정적인 페이지"로 바꾸고
    홈페이지 = 홈, 글 페이지 = (비워 둠)
    ※ 글 페이지에 "칼럼"을 지정하면 안 됩니다. 그러면 워드프레스가
       page-column.php 대신 글 목록 템플릿을 씁니다.
-->
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
	<title>CICLO</title>
	<link>{SITE}</link>
	<description>씨클로 GEO 홈페이지 제작</description>
	<pubDate>{now.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
	<language>ko-KR</language>
	<wp:wxr_version>1.2</wp:wxr_version>
	<wp:base_site_url>{SITE}</wp:base_site_url>
	<wp:base_blog_url>{SITE}</wp:base_blog_url>

	<wp:author>
		<wp:author_id>1</wp:author_id>
		<wp:author_login>{cdata(AUTHOR)}</wp:author_login>
		<wp:author_email>{cdata(AUTHOR_EMAIL)}</wp:author_email>
		<wp:author_display_name>{cdata(AUTHOR_NAME)}</wp:author_display_name>
		<wp:author_first_name>{cdata('')}</wp:author_first_name>
		<wp:author_last_name>{cdata('')}</wp:author_last_name>
	</wp:author>
""")

for i, (name, slug) in enumerate(CATS, start=2):
    parts.append(f"""	<wp:category>
		<wp:term_id>{i}</wp:term_id>
		<wp:category_nicename>{cdata(slug)}</wp:category_nicename>
		<wp:category_parent>{cdata('')}</wp:category_parent>
		<wp:cat_name>{cdata(name)}</wp:cat_name>
	</wp:category>
""")

parts.append('\n')
for i, (title, slug, order) in enumerate(PAGES):
    parts.append(page_item(title, slug, order, 1001 + i))

parts.append(post_item(
    '테마 설치 확인용 샘플 글',
    'ciclo-theme-check',
    SAMPLE_BODY,
    2001,
    'GEO · AI 검색', 'geo'))

parts.append('</channel>\n</rss>\n')

io.open(OUT, 'w', encoding='utf-8').write(''.join(parts))

size = os.path.getsize(OUT)
print('ok  ciclo-import.xml  %d B' % size)
print('    페이지 %d · 카테고리 %d · 샘플 글 1' % (len(PAGES), len(CATS)))
