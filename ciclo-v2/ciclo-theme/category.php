<?php
/**
 * 칼럼 카테고리 — /category/{slug}/
 * page-column.php 와 같은 모양으로 그립니다.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header(); ?>
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
      <div class="overline">/COLUMN · <?php echo esc_html( single_cat_title( '', false ) ); ?></div>
      <h1 class="sec-h2"><?php echo esc_html( single_cat_title( '', false ) ); ?></h1>
<?php if ( category_description() ) : ?>
      <div class="sec-lead"><?php echo wp_kses_post( category_description() ); ?></div>
<?php endif; ?>

      <div class="col-list">
<?php if ( have_posts() ) : while ( have_posts() ) : the_post(); ?>
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
        <p class="sec-lead">이 분류에는 아직 글이 없습니다.</p>
<?php endif; ?>
      </div>

<?php the_posts_pagination( array( 'prev_text' => '←', 'next_text' => '→', 'class' => 'col-pager' ) ); ?>
    </div>
  </div>
</div>
<?php get_footer();
