<?php
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
