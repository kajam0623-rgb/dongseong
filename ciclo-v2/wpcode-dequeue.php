<?php
/**
 * CICLO — 쓰지 않는 워드프레스 기본 CSS 걷어내기
 *
 * 넣는 곳: WPCode > + Add Snippet > Add Your Custom Code > **PHP Snippet**
 *          위치는 "Run Everywhere", 저장 후 Active 로 켜면 됩니다.
 *          (WPCode 를 안 쓰신다면 자식 테마 functions.php 끝에 붙여도 같습니다.
 *           단 부모 테마 functions.php 에 직접 넣지 마세요 — 테마 업데이트에 날아갑니다.)
 *
 * 왜 지우나 — 홈 기준 실측입니다
 *
 *   스타일시트                크기      미사용 규칙
 *   wp-emoji-styles          0.3KB     100%   페이지에 이모지 0개
 *   wp-block-library         4.2KB      59%   구텐베르크 — 페이지에 블록 0개
 *   global-styles(theme.json) 10.9KB    77%
 *                            ─────
 *                            15.4KB    거의 전부 죽은 CSS
 *
 * 이 사이트는 페이지를 Elementor 텍스트 위젯 + 자체 CSS 로 그립니다.
 * 구텐베르크 블록도, 이모지도 쓰지 않으므로 위 세 벌은 순수한 낭비입니다.
 * 렌더 차단 CSS 라 바이트보다 FCP 에 크게 작용합니다.
 *
 * ⚠️ 넣고 나서 확인할 것
 *   global-styles 는 theme.json 의 색·타이포 프리셋입니다. 프런트에는 영향이
 *   없지만, 워드프레스 편집기 화면에서 색상 팔레트가 달라 보일 수 있습니다.
 *   한 번 열어 확인해 보시고 불편하면 그 줄만 지우면 됩니다.
 *
 *   혹시 나중에 구텐베르크 블록으로 페이지를 만들게 되면 wp-block-library 는
 *   되살려야 합니다. 그때는 이 스니펫을 끄면 됩니다.
 */

add_action( 'wp_enqueue_scripts', function () {
	// 구텐베르크 블록 스타일 — 이 사이트는 블록을 쓰지 않는다
	wp_dequeue_style( 'wp-block-library' );
	wp_dequeue_style( 'wp-block-library-theme' );

	// theme.json 프리셋 — 프런트에서 77% 미사용
	wp_dequeue_style( 'global-styles' );

	// 클래식 에디터 호환 스타일
	wp_dequeue_style( 'classic-theme-styles' );
}, 100 );

// 이모지 — 페이지에 이모지가 0개다. 스타일과 감지 스크립트 둘 다 뺀다
remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
remove_action( 'admin_print_styles', 'print_emoji_styles' );
