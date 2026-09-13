<?php
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
