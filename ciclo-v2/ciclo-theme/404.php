<?php
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
