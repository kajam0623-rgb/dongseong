<?php
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
