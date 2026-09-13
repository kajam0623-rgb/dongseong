<?php
/**
 * SEO 제목·설명 주입 — 한 번만 실행된다.
 *
 * 페이지 10개와 칼럼 21편의 검색 제목·설명을 넣는다. Rank Math 화면에서
 * 31번 손으로 붙여넣는 대신 코드가 한 번 돌고 끝낸다.
 *
 * 언제 도나
 *   관리자 화면에 처음 들어올 때 한 번. 끝나면 옵션에 버전을 남기고
 *   그 뒤로는 다시 돌지 않는다. 나중에 손으로 고친 값을 덮어쓰지 않기
 *   위해서다. 다시 돌리려면 아래 상수의 날짜를 바꾸면 된다.
 *
 * 무엇으로 찾나
 *   페이지와 9월 칼럼 11편은 슬러그로 찾는다(영문이라 안전하다).
 *   8월 칼럼 10편은 슬러그가 한글이라 DB 저장 형태가 갈릴 수 있어
 *   제목으로 찾는다.
 *
 * 결과는 관리자 알림으로 한 번 보여 준다. 몇 개 들어갔고 무엇을 못 찾았는지.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'CICLO_SEO_META_VERSION', '2026-09-13' );

/**
 * ( 글종류, 찾는방법, 찾는값, 검색제목, 검색설명 )
 */
function ciclo_seo_meta_rows() {
	return array(
        array( 'page', 'slug',  'home', 'GEO 웹사이트·랜딩페이지 제작 | 씨클로', '검색엔진과 AI가 읽는 구조로 병원·법률·전문직 웹사이트를 만듭니다. 제작과 검색 노출을 한 팀이 같은 단계에서 설계합니다.' ),
        array( 'page', 'slug',  'work', '치과 홈페이지 8곳 채점 결과와 실적 공개', '공개된 HTML 소스를 10개 항목 50개 기준으로 채점했습니다. 저희가 맡은 사이트의 서치어드바이저·PageSpeed 실측값도 함께 공개합니다.' ),
        array( 'page', 'slug',  'about', '씨클로 소개와 일하는 기준', '씨클로가 일하는 기준 세 가지와 저희가 하지 않는 일을 적었습니다. 사업자 정보와 채점 기준도 함께 공개합니다.' ),
        array( 'page', 'slug',  'contact', '무료 홈페이지 진단 신청', '주소 하나만 주시면 치과 8곳을 채점할 때 쓴 같은 50개 항목으로 진단해 드립니다. 계약 여부와 상관없이 점수와 근거를 드립니다.' ),
        array( 'page', 'slug',  'geo', '생성형 검색 최적화(GEO) 서비스', 'ChatGPT와 구글 AI 답변에 인용되도록 사이트 구조를 설계합니다. 진단·설계·적용·모니터링 4단계로 진행합니다.' ),
        array( 'page', 'slug',  'website-design', '웹사이트 제작 서비스', '기획·디자인·구축·유지보수까지 6가지를 한 팀이 맡습니다. 검색 기본기를 제작 단계에서 같이 세팅합니다.' ),
        array( 'page', 'slug',  'blog-content', '블로그 콘텐츠 기획·집필·발행 대행', '검색 의도에 맞춘 주제를 뽑고 글을 쓰고 발행까지 맡습니다. 매월 조회·유입·전환을 리포트로 정리합니다.' ),
        array( 'page', 'slug',  'digital-marketing', '디지털 마케팅·광고 운영 대행', '광고비를 늘리기 전에 클릭이 도착하는 페이지부터 봅니다. 설계·집행·검증·리포트 4단계로 운영합니다.' ),
        array( 'page', 'slug',  'dental', '치과 홈페이지 제작', '진료과목마다 페이지를 나누고 환자분이 실제로 검색하는 질문을 제목으로 씁니다. 검색엔진과 AI가 읽는 구조까지 제작 단계에서 설계합니다.' ),
        array( 'page', 'slug',  'column', '검색·GEO 칼럼', '검색엔진최적화와 생성형 검색에 관해 직접 재고 쓴 글을 모았습니다.' ),
        array( 'post', 'slug',  'dental-homepage-10-items-score', '치과 홈페이지 8곳 채점, 10개 항목 점수 전부 공개', '치과 홈페이지 8곳을 10개 항목으로 채점했습니다. 가장 높은 81점과 가장 낮은 20점이 같은 내용을 다룹니다. 항목별 점수를 전부 엽니다.' ),
        array( 'post', 'slug',  'dental-search-vs-ai-gap', '검색은 되는데 챗지피티는 우리 치과를 모르는 이유', '8곳의 검색 점수는 39~84점으로 벌어졌는데 AI 답변 점수는 31~56점에 몰려 있었습니다. 두 점수가 갈리는 자리를 항목으로 짚습니다.' ),
        array( 'post', 'slug',  'only-one-of-eight-ai-ready', '챗지피티가 제대로 아는 치과는 8곳 중 1곳뿐', 'AI 답변 점수 중앙값은 36점이었습니다. 절반인 50점을 넘긴 곳은 8곳 중 한 곳뿐이었습니다.' ),
        array( 'post', 'slug',  'top-site-still-28', '검색 1위 치과 홈페이지도 이 항목은 28점', '검색 84점으로 표본에서 가장 높았던 곳도 기계용 정보 표기는 28점이었습니다. 30점을 넘긴 곳은 없었습니다.' ),
        array( 'post', 'slug',  'one-field-takes-40-percent', '치과 AI 노출, 항목 하나가 40%를 가져갑니다', '10개 항목 중 기계용 정보 표기 한 칸이 AI 답변 점수의 40%를 차지합니다. 8곳 중앙값은 20점이었습니다.' ),
        array( 'post', 'slug',  'seven-clinics-real-scores', '치과 7곳 기계용 정보 표기 실제 점수 12~30점', '기계용 정보 표기 항목의 7곳 세부 점수입니다. 12·15·15·20·20·28·30점으로 모여 있었습니다.' ),
        array( 'post', 'slug',  'not-zero-just-unfinished', '없는 게 아니라 절반도 안 채운 겁니다', '7곳 모두 0점은 아니었습니다. 5칸 중 한두 칸만 채워진 상태였습니다. 채울 칸이 어디인지 적었습니다.' ),
        array( 'post', 'slug',  'only-first-30k-characters', '홈페이지 소스 33만 자 중 AI가 읽는 건 앞 3만 자', '실제 병원 홈페이지 소스는 327,162자였습니다. 판정에 쓰이는 부분은 앞의 27,873자입니다.' ),
        array( 'post', 'slug',  'doctor-profile-unreadable', '원장님 이력 잘 써두셔도 챗지피티는 못 읽습니다', '의료진 신뢰정보 81점, 기계용 정보 표기 20점. 같은 이력인데 61점 차이가 납니다.' ),
        array( 'post', 'slug',  'why-treatment-pages-fail', '진료 페이지에 글은 많은데 검색이 안 되는 이유', '콘텐츠 품질은 8곳 평균 73점이었습니다. 페이지마다 같은 소개문을 복사한 경우가 자주 걸립니다.' ),
        array( 'post', 'slug',  'hours-as-image-counts-zero', '진료시간표를 이미지로 만들면 검색에선 없는 셈입니다', '채점에서 이미지 속 글자는 0자로 셉니다. 진료시간표를 그림으로 넣으면 여러 항목이 함께 깎입니다.' ),
        array( 'post', 'title', '우리 치과가 네이버에서 안 보이는 5가지 이유', '우리 치과가 네이버에서 안 보이는 5가지 이유', '홈페이지는 멀쩡한데 검색에서만 안 나오는 경우, 원인은 대체로 다섯 가지 안에 있습니다. 하나씩 확인하는 법을 적었습니다.' ),
        array( 'post', 'title', '치과 홈페이지 제작 비용, 700만원이 적정한가', '치과 홈페이지 제작 비용, 700만원이 적정한가', '견적서 네 줄을 뜯어보면 답이 나옵니다. 항목은 전부 눈에 보이는 것에만 붙어 있습니다.' ),
        array( 'post', 'title', '플레이스는 상위인데 홈페이지는 왜 안 뜨나', '플레이스는 상위인데 홈페이지는 왜 안 뜨나', '플레이스와 웹문서는 서로 다른 창구입니다. 한쪽이 잘 된다고 다른 쪽이 따라오지 않습니다.' ),
        array( 'post', 'title', '환자가 ChatGPT에 치과 물어볼 때, 우리가 인용되려면', '환자가 ChatGPT에 치과 물어볼 때 인용되는 조건', 'AI는 홈페이지를 읽고 답을 만듭니다. 읽히는 형태로 정리돼 있지 않으면 그냥 지나칩니다.' ),
        array( 'post', 'title', 'llms.txt — 국내 병원 홈페이지에 아직 없는 파일', 'llms.txt, 국내 병원 홈페이지에 아직 없는 파일', 'AI에게 이 사이트의 핵심이 어디인지 알려주는 안내문입니다. 파일 하나면 됩니다.' ),
        array( 'post', 'title', 'robots.txt가 AI 크롤러를 막고 있는지 3분 만에 확인하는 법', 'robots.txt가 AI 크롤러를 막고 있는지 3분 만에 확인하는 법', '문을 닫아놓고 손님이 안 온다고 하는 경우가 있습니다. 확인은 원장님이 직접 하실 수 있습니다.' ),
        array( 'post', 'title', '진료과목 페이지를 나눠야 하는 이유', '진료과목 페이지를 나눠야 하는 이유', '임플란트를 찾는 환자분과 교정을 찾는 환자분은 다른 말로 검색합니다. 한 페이지에 모으면 어느 쪽도 못 잡습니다.' ),
        array( 'post', 'title', '홈페이지 업체 바꿀 때 도메인 못 가져오는 이유', '홈페이지 업체 바꿀 때 도메인 못 가져오는 이유', '계약이 끝나는 날 도메인을 넘겨받지 못하는 경우가 있습니다. 명의를 먼저 확인하셔야 합니다.' ),
        array( 'post', 'title', '치과 홈페이지에 쓰면 안 되는 표현 정리', '치과 홈페이지에 쓰면 안 되는 표현 정리', '의료광고 규정은 블로그나 광고에만 적용되는 게 아닙니다. 홈페이지도 광고입니다.' ),
        array( 'post', 'title', '워드프레스 vs 자체 솔루션, 치과는 뭘 써야 하나', '워드프레스 vs 자체 솔루션, 치과는 뭘 써야 하나', '기능 비교보다 먼저 볼 게 있습니다. 3년 뒤에 이 사이트가 누구 것으로 남는가입니다.' ),
	);
}

function ciclo_seo_meta_find( $type, $by, $needle ) {
	if ( 'title' === $by ) {
		// get_page_by_title() 은 워드프레스 6.2에서 폐기됐다. WP_Query 의
		// title 파라미터(4.4+)를 쓴다.
		$q = new WP_Query( array(
			'title'          => $needle,
			'post_type'      => $type,
			'post_status'    => array( 'publish', 'draft', 'private' ),
			'posts_per_page' => 1,
			'fields'         => 'ids',
			'no_found_rows'  => true,
		) );
		return empty( $q->posts ) ? 0 : (int) $q->posts[0];
	}

	// 슬러그. 한글 슬러그는 저장 형태가 갈릴 수 있어 원문과 디코딩본을 모두 본다.
	foreach ( array_unique( array( $needle, urldecode( $needle ) ) ) as $name ) {
		$hit = get_posts( array(
			'name'           => $name,
			'post_type'      => $type,
			'post_status'    => array( 'publish', 'draft', 'private' ),
			'posts_per_page' => 1,
			'fields'         => 'ids',
		) );
		if ( ! empty( $hit ) ) {
			return (int) $hit[0];
		}
	}
	return 0;
}

function ciclo_seo_meta_run() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	if ( get_option( 'ciclo_seo_meta_done' ) === CICLO_SEO_META_VERSION ) {
		return;
	}

	$done = 0;
	$miss = array();

	foreach ( ciclo_seo_meta_rows() as $row ) {
		list( $type, $by, $needle, $title, $desc ) = $row;

		$id = ciclo_seo_meta_find( $type, $by, $needle );
		if ( ! $id ) {
			$miss[] = $needle;
			continue;
		}

		update_post_meta( $id, 'rank_math_title', $title );
		update_post_meta( $id, 'rank_math_description', $desc );
		$done++;
	}

	update_option( 'ciclo_seo_meta_done', CICLO_SEO_META_VERSION );
	update_option( 'ciclo_seo_meta_report', array( 'done' => $done, 'miss' => $miss ) );
}
add_action( 'admin_init', 'ciclo_seo_meta_run' );

/**
 * 결과 알림 — 한 번 보여 주고 지운다.
 */
function ciclo_seo_meta_notice() {
	$r = get_option( 'ciclo_seo_meta_report' );
	if ( ! $r ) {
		return;
	}
	delete_option( 'ciclo_seo_meta_report' );

	$msg = sprintf( '씨클로 — 검색 제목·설명 %d개를 넣었습니다.', (int) $r['done'] );
	$cls = 'notice-success';

	if ( ! empty( $r['miss'] ) ) {
		$cls  = 'notice-warning';
		$msg .= ' 다음은 찾지 못했습니다(글이 없거나 제목이 다릅니다): '
			. esc_html( implode( ' · ', $r['miss'] ) );
	}

	printf( '<div class="notice %s is-dismissible"><p>%s</p></div>',
		esc_attr( $cls ), wp_kses_post( $msg ) );
}
add_action( 'admin_notices', 'ciclo_seo_meta_notice' );
