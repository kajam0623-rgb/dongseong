<?php
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
    <aside class="col-side">
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

    <div class="col-main">
      <div class="overline">/COLUMN · 네이버 칼럼</div>
      <h1 class="sec-h2">검색과 AI가 읽는 방식에 대해<br>저희가 확인한 것들을 적습니다</h1>

      <div class="col-list">
<?php if ( $q->have_posts() ) : while ( $q->have_posts() ) : $q->the_post(); ?>
        <article class="col-post">
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
<?php endwhile; else : ?>
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
