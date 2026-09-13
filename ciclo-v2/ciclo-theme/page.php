<?php
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
