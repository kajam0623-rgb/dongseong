#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""워드프레스 테마 생성 — Elementor·WPCode 의존을 전부 걷어낸다.

왜 테마인가
  지금은 층이 넷이다: Hello Elementor → Elementor 위젯 → WPCode 스니펫
  → 커스터마이저 추가 CSS. 이 층들이 서로 싸워서 생긴 게 지금까지 고친
  문제들이다(25KB 중복 CSS 가 특정성으로 이김, 커스터마이저 820px 가 홈까지
  누름, JS 스니펫 하나 죽으면 사이트가 죽음).

  테마로 가면 CSS 가 한 곳이고 특정성 싸움이 구조적으로 사라진다.
  Elementor·Essential Addons 를 뺄 수 있어 남은 최대 성능 개선이기도 하다.

만드는 방식
  마크업은 이미 브라우저로 실측 검증한 pages/*.html 을 **그대로** 옮긴다.
  새로 쓰지 않는다 — 검증을 재사용하기 위해서다.
  PHP 는 배관(enqueue·템플릿 계층·루프)만 담당한다.

칼럼만 예외다. Essential Addons Post Grid 로 돌던 글 목록이라 WP 루프로
새로 그려야 한다. 여기만 마크업이 새 것이고, 클래스도 eael-* 대신 col-* 로
바꿔 CSS 를 함께 정리한다.
"""
import io, os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'pages')
OUT = os.path.join(HERE, 'ciclo-theme')

def read(p):
    return io.open(os.path.join(HERE, p), encoding='utf-8').read()

def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8').write(text)
    return len(text.encode('utf-8'))

# 깨끗이 다시 만든다
if os.path.isdir(OUT):
    shutil.rmtree(OUT)

# ─────────────────────────────────────────────────────────────
# 페이지 슬러그 ↔ 소스 파일
# ─────────────────────────────────────────────────────────────
PAGES = [
    ('front-page',              'Home.html',            None),
    ('page-work',               'Work.html',            '/work/'),
    ('page-about',              'About.html',           '/about/'),
    ('page-contact',            'Contact.html',         '/contact/'),
    ('page-website-design',     'Website_Design.html',  '/website-design/'),
    ('page-geo',                'GEO.html',             '/geo/'),
    ('page-blog-content',       'Blog_Content.html',    '/blog-content/'),
    ('page-digital-marketing',  'Digital_Marketing.html','/digital-marketing/'),
    ('page-dental',             '치과_홈페이지_제작.html', '/dental/'),
]

header_html = read('pages/CICLO_Header.html')
footer_html = read('pages/CICLO_Footer.html')

# ─────────────────────────────────────────────────────────────
# style.css — 테마 헤더만. 실제 CSS 는 assets/css/global.css
# ─────────────────────────────────────────────────────────────
write('style.css', """/*
Theme Name: CICLO
Theme URI: https://ciclo.kr/
Description: 씨클로 자체 테마. Elementor·WPCode 없이 동작합니다. 페이지 마크업은
             템플릿에 들어 있고, 칼럼 글만 워드프레스 글쓰기로 관리합니다.
Author: CICLO
Version: 2.0
Requires at least: 6.0
Requires PHP: 7.4
License: GPL-2.0-or-later
Text Domain: ciclo
*/

/* 실제 스타일은 assets/css/global.css 에 있습니다.
   워드프레스는 이 파일의 주석 헤더만 읽고, 스타일은 functions.php 가
   assets/css/global.css 를 enqueue 합니다. 여기에 CSS 를 쓰지 마세요 —
   두 곳으로 나뉘면 예전처럼 특정성 싸움이 다시 시작됩니다. */
""")

# ─────────────────────────────────────────────────────────────
# functions.php
# ─────────────────────────────────────────────────────────────
write('functions.php', r"""<?php
/**
 * CICLO 테마 — 배관
 *
 * 여기서 하는 일은 네 가지뿐입니다.
 *   1. CSS·JS·폰트 enqueue
 *   2. 워드프레스가 기본으로 끼얹는 안 쓰는 CSS 걷어내기
 *   3. 테마 기본 지원 선언
 *   4. 칼럼 목록에 쓸 요약문 다듬기
 *
 * 페이지 디자인은 전부 템플릿 파일과 assets/css/global.css 에 있습니다.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'CICLO_VER', '2.0.0' );

/* ── 1. 에셋 ───────────────────────────────────────────────── */
add_action( 'wp_enqueue_scripts', function () {

	// Pretendard — 사이트 전체가 이 폰트 하나입니다.
	// 자체 호스팅으로 바꾸려면 이 한 줄의 주소만 내부 경로로 바꾸면 됩니다.
	wp_enqueue_style(
		'ciclo-pretendard',
		'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css',
		array(),
		null
	);

	wp_enqueue_style(
		'ciclo',
		get_theme_file_uri( 'assets/css/global.css' ),
		array( 'ciclo-pretendard' ),
		CICLO_VER
	);

	wp_enqueue_script(
		'ciclo',
		get_theme_file_uri( 'assets/js/ciclo-effects.js' ),
		array(),
		CICLO_VER,
		true   // 푸터에서 로드 — 렌더를 막지 않습니다
	);
}, 5 );

// 폰트 CDN 에 미리 연결해 둡니다 (DNS + TLS 를 앞당김)
add_filter( 'wp_resource_hints', function ( $hints, $relation ) {
	if ( 'preconnect' === $relation ) {
		$hints[] = array( 'href' => 'https://cdn.jsdelivr.net', 'crossorigin' );
	}
	return $hints;
}, 10, 2 );

/* ── 2. 안 쓰는 워드프레스 기본 CSS 정리 ────────────────────────
 *
 * 홈 기준 실측: wp-block-library 4.2KB(블록 0개) · global-styles 10.9KB(77% 미사용)
 *              · 이모지 0.3KB(이모지 0개) = 15.4KB, 전부 렌더 차단.
 *
 * 이 테마는 구텐베르크 블록을 쓰지 않습니다. 나중에 블록으로 페이지를 만들게
 * 되면 아래 wp_dequeue_style('wp-block-library') 줄을 지우세요.
 */
add_action( 'wp_enqueue_scripts', function () {
	wp_dequeue_style( 'wp-block-library' );
	wp_dequeue_style( 'wp-block-library-theme' );
	wp_dequeue_style( 'global-styles' );
	wp_dequeue_style( 'classic-theme-styles' );
}, 100 );

remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
remove_action( 'admin_print_styles', 'print_emoji_styles' );

// 워드프레스가 넣는 잡다한 head 태그 중 안 쓰는 것
remove_action( 'wp_head', 'wp_generator' );                 // 워드프레스 버전 노출
remove_action( 'wp_head', 'wlwmanifest_link' );             // Windows Live Writer
remove_action( 'wp_head', 'rsd_link' );                     // Really Simple Discovery
remove_action( 'wp_head', 'wp_shortlink_wp_head' );

/* ── 3. 테마 지원 ──────────────────────────────────────────── */
add_action( 'after_setup_theme', function () {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'comment-form', 'gallery', 'caption', 'style', 'script' ) );
	add_theme_support( 'automatic-feed-links' );

	// 칼럼 목록의 썸네일 — 258×168 로 그립니다(2배 대응해서 516×336)
	add_image_size( 'ciclo-col', 516, 336, true );
} );

/* ── 4. 칼럼 목록 요약문 ────────────────────────────────────── */
add_filter( 'excerpt_length', function () { return 55; }, 999 );
add_filter( 'excerpt_more',   function () { return '…'; } );

/**
 * 본문 첫 문단에서 요약을 뽑습니다.
 * 수동 요약문이 있으면 그것을 우선합니다.
 */
function ciclo_excerpt( $len = 90 ) {
	$t = has_excerpt() ? get_the_excerpt() : wp_strip_all_tags( get_the_content() );
	$t = trim( preg_replace( '/\s+/u', ' ', $t ) );
	if ( mb_strlen( $t ) > $len ) {
		$t = mb_substr( $t, 0, $len ) . '…';
	}
	return $t;
}

/** 칼럼 카테고리 메뉴 — 슬러그와 표시 이름 */
function ciclo_column_cats() {
	return array(
		'seo'      => '검색엔진최적화 (SEO)',
		'geo'      => 'GEO · AI 검색',
		'hospital' => '병의원 마케팅',
		'content'  => '블로그 콘텐츠',
		'ads'      => '광고 운영',
		'case'     => '고객 사례',
		'insight'  => '인사이트',
	);
}

/**
 * SEO 제목·설명 주입 — 페이지 10개 + 칼럼 21편.
 * 관리자 화면에 처음 들어올 때 한 번만 돌고, 끝나면 다시 돌지 않습니다.
 * 자세한 것은 inc/seo-meta.php 주석.
 */
require_once get_theme_file_path( 'inc/seo-meta.php' );
""")

# ─────────────────────────────────────────────────────────────
# header.php / footer.php
# ─────────────────────────────────────────────────────────────
# 헤더 마크업에서 현재 페이지 표시는 JS 가 붙이므로 그대로 옮긴다.
write('header.php', """<?php
/**
 * 사이트 헤더 — 고정 네비 · 사이드바 · 카카오 플로팅 버튼
 *
 * 마크업은 pages/CICLO_Header.html 을 그대로 옮긴 것입니다.
 * 브라우저 실측으로 검증된 마크업이라 손대지 않았습니다.
 * 현재 페이지 표시(aria-current)는 assets/js/ciclo-effects.js 가 붙입니다.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
?>
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
""" + header_html.rstrip('\n') + """
<main id="content" class="site-main">
""")

write('footer.php', """<?php
/**
 * 사이트 푸터 — pages/CICLO_Footer.html 을 그대로 옮긴 것입니다.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
?>
</main>
""" + footer_html.rstrip('\n') + """
<?php wp_footer(); ?>
</body>
</html>
""")

# ─────────────────────────────────────────────────────────────
# 페이지 템플릿
# ─────────────────────────────────────────────────────────────
TPL = """<?php
/**
 * %(title)s
 *
 * 마크업은 %(src)s 를 그대로 옮긴 것입니다.
 * 브라우저 실측(1440 / 768 / 390 / 360px)으로 검증된 마크업이라 손대지
 * 않았습니다. 내용을 고치려면 이 파일을 고치면 됩니다.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
?>
<div class="ciclo-page" id="%(id)s">
%(body)s
</div>
<?php
get_footer();
"""

made = []
for slug, src, url in PAGES:
    body = read('pages/' + src).rstrip('\n')
    # 캡처 이미지 경로를 테마 안 경로로 바꾼다. 정적 HTML 에서는 워드프레스
    # 업로드 경로(/wp-content/uploads/ciclo/)를 쓰지만, 테마가 이미지를 들고
    # 있으므로 미디어에 따로 올릴 필요가 없다.
    body = re.sub(
        r'src="/wp-content/uploads/ciclo/([A-Za-z0-9._-]+)"',
        lambda m: ('src="<?php echo esc_url( get_theme_file_uri( \'assets/img/%s\' ) ); ?>"'
                   % m.group(1)),
        body)
    pid = 'ciclo-home' if slug == 'front-page' else 'ciclo-' + slug.replace('page-', '')
    txt = TPL % dict(
        title=('홈 (front-page)' if url is None else '페이지 ' + url),
        src='pages/' + src, id=pid, body=body)
    made.append((slug + '.php', write(slug + '.php', txt)))

# ─────────────────────────────────────────────────────────────
# 칼럼 — 여기만 마크업이 새 것이다 (EA Post Grid → WP 루프)
# ─────────────────────────────────────────────────────────────
COL_SIDE = """    <aside class="col-side">
      <div class="lbl" id="col-menu-lbl">MENU</div>
      <nav aria-labelledby="col-menu-lbl">
        <a href="<?php echo esc_url( get_permalink( get_page_by_path( 'column' ) ) ); ?>"<?php echo ( is_page( 'column' ) && ! is_category() ) ? ' class="active" aria-current="page"' : ''; ?>>Home</a>
<?php foreach ( ciclo_column_cats() as $slug => $name ) :
	$term = get_category_by_slug( $slug );
	if ( ! $term ) { continue; }
	$cur = is_category( $slug ); ?>
        <a href="<?php echo esc_url( get_category_link( $term ) ); ?>"<?php echo $cur ? ' class="active" aria-current="page"' : ''; ?>><?php echo esc_html( $name ); ?></a>
<?php endforeach; ?>
      </nav>
    </aside>
"""

COL_ITEM = """        <article class="col-post">
<?php if ( has_post_thumbnail() ) : ?>
          <a class="col-media" href="<?php the_permalink(); ?>" aria-hidden="true" tabindex="-1"><?php
            the_post_thumbnail( 'ciclo-col', array( 'alt' => '', 'loading' => 'lazy', 'decoding' => 'async' ) );
          ?></a>
<?php endif; ?>
          <div class="col-body">
            <h2 class="col-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
            <p class="col-excerpt"><?php echo esc_html( ciclo_excerpt() ); ?></p>
            <div class="col-meta">
              <time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( get_the_date( 'Y.m.d' ) ); ?></time>
<?php $cats = get_the_category(); if ( $cats ) : ?>
              <span class="col-cat"><?php echo esc_html( $cats[0]->name ); ?></span>
<?php endif; ?>
            </div>
          </div>
        </article>
"""

write('page-column.php', """<?php
/**
 * 칼럼 목록 — /column/
 *
 * ★ 이 파일만 마크업이 새 것입니다.
 *   기존에는 Essential Addons 의 Post Grid 위젯이 그리던 자리라,
 *   플러그인을 걷어내면서 워드프레스 루프로 다시 썼습니다.
 *   클래스도 eael-* 대신 col-* 로 바꿔 CSS 를 함께 정리했습니다.
 *
 *   나머지 페이지와 달리 브라우저 실측 검증을 거치지 않았습니다.
 *   테마를 켜신 뒤 이 페이지를 먼저 확인해 주세요.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();

$paged = max( 1, get_query_var( 'paged' ), get_query_var( 'page' ) );
$q = new WP_Query( array(
	'post_type'      => 'post',
	'post_status'    => 'publish',
	'posts_per_page' => 10,
	'paged'          => $paged,
) );
?>
<div class="ciclo-page ciclo-column">
  <div class="column-wrap">
""" + COL_SIDE + """
    <div class="col-main">
      <div class="overline">/COLUMN · 네이버 칼럼</div>
      <h1 class="sec-h2">검색과 AI가 읽는 방식에 대해<br>저희가 확인한 것들을 적습니다</h1>

      <div class="col-list">
<?php if ( $q->have_posts() ) : while ( $q->have_posts() ) : $q->the_post(); ?>
""" + COL_ITEM + """<?php endwhile; else : ?>
        <p class="sec-lead">아직 발행한 글이 없습니다.</p>
<?php endif; ?>
      </div>

<?php
$links = paginate_links( array(
	'total'     => $q->max_num_pages,
	'current'   => $paged,
	'type'      => 'array',
	'prev_text' => '←',
	'next_text' => '→',
) );
if ( $links ) : ?>
      <nav class="col-pager" aria-label="칼럼 목록 페이지"><?php echo implode( '', $links ); ?></nav>
<?php endif;
wp_reset_postdata(); ?>
    </div>
  </div>
</div>
<?php
get_footer();
""")

# 카테고리 아카이브 — 목록과 같은 모양
write('category.php', """<?php
/**
 * 칼럼 카테고리 — /category/{slug}/
 * page-column.php 와 같은 모양으로 그립니다.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header(); ?>
<div class="ciclo-page ciclo-column">
  <div class="column-wrap">
""" + COL_SIDE + """
    <div class="col-main">
      <div class="overline">/COLUMN · <?php echo esc_html( single_cat_title( '', false ) ); ?></div>
      <h1 class="sec-h2"><?php echo esc_html( single_cat_title( '', false ) ); ?></h1>
<?php if ( category_description() ) : ?>
      <div class="sec-lead"><?php echo wp_kses_post( category_description() ); ?></div>
<?php endif; ?>

      <div class="col-list">
<?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
""" + COL_ITEM + """<?php endwhile; else : ?>
        <p class="sec-lead">이 분류에는 아직 글이 없습니다.</p>
<?php endif; ?>
      </div>

<?php the_posts_pagination( array( 'prev_text' => '←', 'next_text' => '→', 'class' => 'col-pager' ) ); ?>
    </div>
  </div>
</div>
<?php get_footer();
""")

# 칼럼 글 상세
write('single.php', """<?php
/**
 * 칼럼 글 — 읽기에만 집중한 한 단 레이아웃입니다.
 * 본문은 워드프레스 에디터가 만든 것을 그대로 출력하고,
 * assets/css/global.css 의 .post-body 가 타이포를 잡습니다.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
while ( have_posts() ) : the_post(); ?>
<div class="ciclo-page">
  <article class="post-wrap">
    <header class="post-head">
      <div class="overline"><?php
        $cats = get_the_category();
        echo '/COLUMN' . ( $cats ? ' · ' . esc_html( $cats[0]->name ) : '' );
      ?></div>
      <h1 class="post-title"><?php the_title(); ?></h1>
      <div class="post-meta">
        <time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>"><?php echo esc_html( get_the_date( 'Y년 n월 j일' ) ); ?></time>
      </div>
    </header>

<?php if ( has_post_thumbnail() ) : ?>
    <figure class="post-cover"><?php the_post_thumbnail( 'large', array( 'loading' => 'eager', 'fetchpriority' => 'high' ) ); ?></figure>
<?php endif; ?>

    <div class="post-body"><?php the_content(); ?></div>

    <footer class="post-foot">
      <a class="sec-link" href="<?php echo esc_url( get_permalink( get_page_by_path( 'column' ) ) ); ?>">← 칼럼 목록으로</a>
    </footer>
  </article>

<?php
$prev = get_previous_post();
$next = get_next_post();
if ( $prev || $next ) : ?>
  <nav class="post-nav" aria-label="이전 다음 글">
<?php if ( $prev ) : ?>
    <a class="post-nav-item" href="<?php echo esc_url( get_permalink( $prev ) ); ?>"><span>이전 글</span><b><?php echo esc_html( get_the_title( $prev ) ); ?></b></a>
<?php endif; if ( $next ) : ?>
    <a class="post-nav-item next" href="<?php echo esc_url( get_permalink( $next ) ); ?>"><span>다음 글</span><b><?php echo esc_html( get_the_title( $next ) ); ?></b></a>
<?php endif; ?>
  </nav>
<?php endif; ?>
</div>
<?php
endwhile;
get_footer();
""")

# 일반 페이지 폴백 — 템플릿이 없는 페이지는 에디터 내용을 그대로 그린다
write('page.php', """<?php
/**
 * 일반 페이지 폴백
 *
 * 전용 템플릿이 없는 페이지(나중에 워드프레스에서 새로 만든 것)는
 * 에디터에 쓴 내용을 그대로 그립니다.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
while ( have_posts() ) : the_post(); ?>
<div class="ciclo-page">
  <article class="post-wrap">
    <header class="post-head">
      <h1 class="post-title"><?php the_title(); ?></h1>
    </header>
    <div class="post-body"><?php the_content(); ?></div>
  </article>
</div>
<?php
endwhile;
get_footer();
""")

write('index.php', """<?php
/**
 * 폴백 — 워드프레스가 요구하는 필수 파일입니다.
 * 보통은 category.php / single.php / page-*.php 가 먼저 잡히고
 * 여기까지 오지 않습니다.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header(); ?>
<div class="ciclo-page ciclo-column">
  <div class="column-wrap">
    <div class="col-main">
      <div class="overline">/ARCHIVE</div>
      <h1 class="sec-h2">글 목록</h1>
      <div class="col-list">
<?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
        <article class="col-post">
          <div class="col-body">
            <h2 class="col-title"><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
            <p class="col-excerpt"><?php echo esc_html( ciclo_excerpt() ); ?></p>
          </div>
        </article>
<?php endwhile; else : ?>
        <p class="sec-lead">글이 없습니다.</p>
<?php endif; ?>
      </div>
<?php the_posts_pagination( array( 'prev_text' => '←', 'next_text' => '→' ) ); ?>
    </div>
  </div>
</div>
<?php get_footer();
""")

write('404.php', """<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header(); ?>
<div class="ciclo-page">
  <header class="page-hero">
    <div class="overline">/404</div>
    <h1 class="display">Page<br><span class="blue">Not Found</span></h1>
    <p class="lead">주소가 바뀌었거나 삭제된 페이지입니다. 아래에서 찾으시는 것으로 가실 수 있습니다.</p>
  </header>
  <section class="section" style="padding-top:0">
    <div class="other-pills">
      <a class="other-pill" href="<?php echo esc_url( home_url( '/' ) ); ?>">홈 →</a>
      <a class="other-pill" href="<?php echo esc_url( home_url( '/work/' ) ); ?>">Work →</a>
      <a class="other-pill" href="<?php echo esc_url( home_url( '/column/' ) ); ?>">칼럼 →</a>
      <a class="other-pill" href="<?php echo esc_url( home_url( '/contact/' ) ); ?>">문의 →</a>
    </div>
  </section>
</div>
<?php get_footer();
""")


# 설치 안내 — 빌더가 테마 폴더를 통째로 다시 만들기 때문에 소스는 바깥에 둔다
shutil.copy(os.path.join(HERE, 'theme-README.md'), os.path.join(OUT, 'README.md'))

# SEO 제목·설명 주입 — 페이지 10개 + 칼럼 21편을 한 번에 넣는다.
# Rank Math 화면에서 31번 손으로 붙여넣는 대신 테마가 한 번 돌고 끝낸다.
os.makedirs(os.path.join(OUT, 'inc'), exist_ok=True)
shutil.copy(os.path.join(HERE, 'php', 'seo-meta.php'),
            os.path.join(OUT, 'inc', 'seo-meta.php'))
print('SEO   inc/seo-meta.php (페이지 10 · 칼럼 21)')

os.makedirs(os.path.join(OUT, 'assets', 'img'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'assets', 'css'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'assets', 'js'), exist_ok=True)
shutil.copy(os.path.join(HERE, 'css', 'global.css'), os.path.join(OUT, 'assets', 'css', 'global.css'))
shutil.copy(os.path.join(HERE, 'js', 'ciclo-effects.js'), os.path.join(OUT, 'assets', 'js', 'ciclo-effects.js'))

# 캡처 WebP — 테마 안으로 넣는다. 워드프레스 미디어에 따로 올릴 필요가 없고,
# 테마를 지웠다 다시 켜도 이미지가 같이 따라온다.
import glob as _glob
_shots = sorted(_glob.glob(os.path.join(HERE, 'images', 'psi-*.webp')) +
                _glob.glob(os.path.join(HERE, 'images', 'naver-*.webp')))
for _p in _shots:
    shutil.copy(_p, os.path.join(OUT, 'assets', 'img', os.path.basename(_p)))
if _shots:
    print('캡처  %d장 → assets/img/' % len(_shots))

print('생성한 템플릿')
for name, size in made:
    print('  %-32s %7d B' % (name, size))
for extra in ('header.php', 'footer.php', 'page-column.php', 'category.php',
              'single.php', 'page.php', 'index.php', '404.php',
              'functions.php', 'style.css'):
    p = os.path.join(OUT, extra)
    print('  %-32s %7d B' % (extra, os.path.getsize(p)))
print()
print('에셋  assets/css/global.css · assets/js/ciclo-effects.js')
