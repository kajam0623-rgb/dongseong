<?php
/**
 * 테마 템플릿을 워드프레스 없이 실행해서 HTML 을 뽑는다.
 *
 * 왜 필요한가
 *   이 환경에는 워드프레스도 MySQL 도 없다. 그런데 PHP CLI 는 있다.
 *   워드프레스가 제공하는 함수를 최소한으로 흉내 내면 템플릿을 실제로
 *   실행시킬 수 있고, 나온 HTML 을 지금까지 쓰던 브라우저 검사에
 *   그대로 태울 수 있다.
 *
 *   즉 "PHP 가 문법 오류 없이 돌아간다"를 넘어 **무엇을 출력하는지**까지
 *   확인한다. 정의되지 않은 함수를 부르면 PHP 가 Fatal error 를 내므로,
 *   워드프레스 API 를 잘못 쓴 곳도 여기서 걸린다.
 *
 * 확인하지 못하는 것 (정직하게)
 *   · 템플릿 계층 — 워드프레스가 page-work.php 를 고르는지 (규칙은 표준)
 *   · 실제 DB 를 읽는 루프 결과 — 여기서는 가짜 글로 대신한다
 *   · 플러그인·다른 테마와의 충돌
 *
 * 사용법
 *   php tools/render-theme.php front-page > out.html
 *   php tools/render-theme.php page-column --posts=3 > out.html
 */

$slug = $argv[1] ?? 'front-page';
$nposts = 3;
foreach ( array_slice( $argv, 2 ) as $a ) {
	if ( preg_match( '/^--posts=(\d+)$/', $a, $m ) ) { $nposts = (int) $m[1]; }
}

define( 'ABSPATH', __DIR__ . '/../ciclo-theme/' );
$THEME = ABSPATH;

/* ── 가짜 글 ─────────────────────────────────────────────── */
$POSTS = array();
for ( $i = 1; $i <= $nposts; $i++ ) {
	$POSTS[] = (object) array(
		'ID'    => $i,
		'title' => "치과 홈페이지에서 기계가 읽는 자리 점검하기 {$i}",
		'date'  => sprintf( '2026-0%d-1%d', ( $i % 9 ) + 1, $i % 9 ),
		'cat'   => array( 'seo' => '검색엔진최적화 (SEO)' ),
		'body'  => '<p>본문 문단입니다. 실제 글은 워드프레스 에디터에서 작성합니다.</p>'
		         . '<h2>소제목</h2><p>두 번째 문단입니다.</p><ul><li>목록 항목</li><li>또 하나</li></ul>',
	);
}
$CUR = null;
$IDX = -1;

/* ── 워드프레스 함수 스텁 ─────────────────────────────────── */
function language_attributes() { echo 'lang="ko"'; }
function bloginfo( $k ) { echo $k === 'charset' ? 'UTF-8' : 'CICLO'; }
function body_class( $c = '' ) { echo 'class="ciclo-live ' . esc_attr( is_array( $c ) ? implode( ' ', $c ) : $c ) . '"'; }
// 에셋은 절대 경로로 건다 — 렌더 결과를 어느 폴더에 두든 CSS·JS 가 붙어야
// 브라우저 검사가 의미를 갖는다 (상대경로로 두면 조용히 안 붙고, 그러면
// "가로 넘침"처럼 CSS 부재가 원인인 가짜 문제가 잔뜩 잡힌다)
function ciclo_asset( $rel ) { return 'file://' . realpath( __DIR__ . '/../ciclo-theme/' . $rel ); }
function wp_head() { echo "<title>CICLO</title>\n"
	. '<link rel="stylesheet" href="' . ciclo_asset( 'assets/css/global.css' ) . '">' . "\n"; }
function wp_footer() { echo '<script src="' . ciclo_asset( 'assets/js/ciclo-effects.js' ) . '"></script>' . "\n"; }
function wp_body_open() {}
function get_header() { global $THEME; require $THEME . 'header.php'; }
function get_footer() { global $THEME; require $THEME . 'footer.php'; }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return esc_html( $s ); }
function esc_url( $s ) { return esc_html( $s ); }
function wp_kses_post( $s ) { return $s; }
function wp_strip_all_tags( $s ) { return strip_tags( (string) $s ); }
function home_url( $p = '/' ) { return $p; }
function get_theme_file_uri( $p ) { return ciclo_asset( $p ); }
function add_action() {} function add_filter() {} function remove_action() {}
function add_theme_support() {} function add_image_size() {}
function wp_enqueue_style() {} function wp_enqueue_script() {} function wp_dequeue_style() {}
function get_query_var( $k ) { return 0; }
function is_page( $s = '' ) { return true; }
function is_category( $s = '' ) { return false; }
function get_page_by_path( $p ) { return (object) array( 'ID' => 99 ); }
function get_permalink( $p = null ) { return '/column/'; }
function get_category_by_slug( $s ) { return (object) array( 'slug' => $s, 'name' => $s ); }
function get_category_link( $t ) { return '/category/' . $t->slug . '/'; }
function single_cat_title( $x = '', $echo = true ) { $t = 'GEO · AI 검색'; if ( $echo ) { echo $t; } return $t; }
function category_description() { return ''; }
function has_post_thumbnail() { return true; }
function the_post_thumbnail( $size = '', $attr = array() ) {
	// 1×1 투명 GIF — 실제 썸네일 자리를 비율만 맞춰 차지한다
	echo '<img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="'
	   . ' width="516" height="336" alt="" loading="lazy" decoding="async">';
}
function has_excerpt() { return false; }
function get_the_excerpt() { global $CUR; return wp_strip_all_tags( $CUR->body ); }
function get_the_content() { global $CUR; return $CUR->body; }
function the_content() { global $CUR; echo $CUR->body; }
function the_title() { global $CUR; echo esc_html( $CUR->title ); }
function get_the_title( $p = null ) { global $CUR; return $CUR ? $CUR->title : '제목'; }
function the_permalink() { global $CUR; echo '/column/post-' . $CUR->ID . '/'; }
function get_the_date( $f = '' ) { global $CUR; return $f === 'c' ? $CUR->date . 'T09:00:00+09:00' : $CUR->date; }
function get_the_category() { global $CUR; $o = array(); foreach ( $CUR->cat as $s => $n ) { $o[] = (object) array( 'slug' => $s, 'name' => $n ); } return $o; }
function have_posts() { global $IDX, $POSTS; return $IDX + 1 < count( $POSTS ); }
function the_post() { global $IDX, $CUR, $POSTS; $CUR = $POSTS[ ++$IDX ]; }
function wp_reset_postdata() { global $IDX; $IDX = -1; }
function paginate_links( $a = array() ) { return array( '<span class="current">1</span>', '<a href="/column/page/2/">2</a>' ); }
function the_posts_pagination( $a = array() ) { echo '<nav class="col-pager"><span class="current">1</span><a href="#">2</a></nav>'; }
function get_previous_post() { return (object) array( 'ID' => 1 ); }
function get_next_post() { return (object) array( 'ID' => 2 ); }

class WP_Query {
	public $max_num_pages = 2;
	public function __construct( $a = array() ) {}
	public function have_posts() { return have_posts(); }
	public function the_post() { the_post(); }
}

/* functions.php 의 헬퍼가 필요하다 */
require $THEME . 'functions.php';

$file = $THEME . $slug . '.php';
if ( ! file_exists( $file ) ) {
	fwrite( STDERR, "없는 템플릿: $slug\n" );
	exit( 2 );
}
require $file;
