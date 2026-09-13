# 성능 — 실측 진단과 조치

측정: 2026-09-13, 헤드리스 크롬, `ciclo.kr` 라이브 + v2 로컬 렌더.

---

## ★ 먼저: 라이브에 지금 나고 있는 버그 3개

이건 성능 이전의 문제다. v2 적용과 별개로 지금 고쳐야 한다.

### 1. JavaScript 스니펫이 통째로 죽어 있다

라이브 콘솔에 **`SyntaxError: Unexpected token ':'`** 가 뜬다.

WPCode JavaScript 스니펫 하나의 끝에 JSON-LD 스키마가 `<script>` 태그 없이
그대로 붙어 있다. JS 문맥에서 `{ "@context": ... }` 는 문법 오류라
**스니펫 전체가 파싱 단계에서 실행되지 못한다.**

그 스니펫이 하려던 일:
- `document.body.classList.add('ciclo-live')`
- 테마 헤더·푸터·entry-title 숨기기
- `#content`, `.page-content` 등의 `max-width` 해제

전부 작동하지 않고 있다.

**조치**: 그 스니펫에서 JSON-LD 블록을 삭제한다.
구조화 데이터는 이미 SEO 플러그인이 9.6KB 규모로 정상 출력 중이다
(Organization · WebSite · FAQPage · Service · Offer 확인). 중복이라 지워도 손실이 없다.

### 2. 홈이 820px 로 눌려 있다

`.section{max-width:1280px}` 으로 설계된 홈이 라이브에서 **820px** 로 렌더링된다.
설계 폭의 64% 다.

원인은 두 겹이다:
- 커스터마이저 추가 CSS 의 `main.site-main>.page-content{max-width:820px}` 에 `body` 조건이 없다
- 이를 풀어주려고 넣은 `body.ciclo-live ... {max-width:none!important}` 는
  1번 버그 때문에 `ciclo-live` 클래스가 안 붙어 발동하지 않는다

또 `.ciclo-page{max-width:none!important;width:100%!important}` 도 있는데,
제약이 걸린 건 `.ciclo-page` 가 아니라 **부모인 `.page-content`** 라 효과가 없다.
고치려는 시도는 있었지만 대상을 잘못 잡았다.

**조치** — 추가 CSS 의 그 규칙에 범위를 준다:

```css
body.single main.site-main>.page-header,
body.single main.site-main>.page-content,
body.archive main.site-main>.page-content,
body.blog   main.site-main>.page-content{max-width:820px;margin-left:auto;margin-right:auto}
```

`global.css` v2 에 `main.site-main>.page-content:has(.ciclo-page){max-width:none}` 방어선도 넣었다.

### 3. 로고 이미지 5개가 전부 404

`/wp-content/uploads/ciclo/mark-ciclo-white.png` → **404**, 5개 전부 `naturalWidth:0`.

눈에 안 보였던 이유는 `global.css` 가 `content:url("data:image/png;base64,...")` 로
실제 로고를 덮어 그리고 있기 때문이다. 화면은 멀쩡한데 요청은 5번 실패하고,
DOM 상으로는 깨진 이미지 5개가 남는다.

원인: 패키지 README 는 `/wp-content/uploads/mark-ciclo-white.png` 에 올리라고 하는데
라이브 마크업은 `/wp-content/uploads/ciclo/...` 를 가리킨다. 경로 불일치.

**조치**: v2 에서 `src` 를 투명 1×1 GIF 로 바꿔 요청 자체를 없앴다.
로고는 CSS `content:url()` 이 그대로 그린다. 업로드가 필요 없다.

---

## ★ 그리고: CSS 가 두 벌 돌고 있다

라이브 인라인 `<style>` 구성:

| 스타일 | 크기 | 정체 |
|---|---|---|
| (no-id) | 49.1KB | WPCode `global.css` — `@import` 로 시작 |
| (no-id) | **25.0KB** | **`global.css` 를 `#ciclo-home` 으로 스코프한 거의 완전한 복사본** |
| `global-styles-inline-css` | 10.9KB | 워드프레스 theme.json (77% 미사용) |
| `wp-block-library-inline-css` | 4.2KB | 구텐베르크 — 페이지에 블록 0개 |
| `wp-custom-css` | 2.4KB | 커스터마이저 추가 CSS |
| `wp-emoji-styles-inline-css` | 0.3KB | 이모지 — 페이지에 이모지 0개 |

두 번째 25KB 레이어가 문제다. `#ciclo-home` 은 특정성 **(1,1,0)** 이라
원본 `global.css` 의 **(0,1,0)** 을 모든 공통 규칙에서 이긴다.

즉 **라이브가 실제로 그리고 있는 값은 `global.css` 가 아니라 그 복사본이다.**

> ⚠️ 이것 때문에 `global.css` 만 v2 로 바꾸면 **거의 아무 변화가 없다.**
> 25KB 복사본을 먼저 지워야 한다. (WPCode 스니펫 목록에서 `.ciclo-page{max-width:none!important`
> 로 시작하는 것을 찾으면 된다.)

부작용도 있다. JS 도 두 벌이라 리빌 IntersectionObserver 가 서로 다른 셀렉터로
두 번 등록되고, 히어로 패럴럭스 스크롤 핸들러도 두 번 붙는다.
(2번 스크립트는 1번 버그로 죽어 있어 현재는 1벌만 실행되지만, 고치면 두 벌이 된다.)

### 죽은 CSS 비율 (홈 기준 실측)

| 스타일시트 | 규칙 수 | 미사용 |
|---|---|---|
| `wp-emoji-styles` | 1 | **100%** |
| autoptimize `86dbb4…` | 64 | **94%** |
| autoptimize `a480d2…` | 37 | **95%** |
| `global-styles-inline` | 86 | 77% |
| `wp-block-library` | 44 | 59% (블록 0개이므로 실질 100%) |

**조치 (functions.php 또는 WPCode PHP 스니펫)** — 구텐베르크 블록과 이모지를 쓰지 않으므로:

```php
add_action('wp_enqueue_scripts', function () {
    wp_dequeue_style('wp-block-library');
    wp_dequeue_style('wp-block-library-theme');
    wp_dequeue_style('global-styles');
    wp_dequeue_style('classic-theme-styles');
}, 100);
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
```

`global-styles` 는 theme.json 색·타이포 프리셋이라, 지운 뒤 에디터 화면을
한 번 확인하는 편이 좋다. 프런트에는 영향이 없다.

---

## v2 에서 한 조치

| 항목 | 전 | 후 |
|---|---|---|
| `global.css` 크기 | 53,649B | **37,745B** (−30%) |
| 로고 인라인 payload | PNG base64 23,940자 (CSS의 **45%**) | WebP base64 ≈6,000자 |
| 폰트 로딩 | `@import` ×2 (직렬 3왕복) | head `<link>` + `preconnect` (병렬) |
| Archivo 웨이트 | 500·700·800·900 (500 미사용, 600 필요한데 없음) | **700·800·900** |
| `will-change` 노드 | 1 (상시 컴포지터 레이어) | **0** |
| 무한 애니메이션 | 3 (spin 40s, spin 16s, marquee 26s) | **1** (marquee 40s) |
| 스크롤 리빌 | 22 노드 | **0** |
| 히어로 패럴럭스 | 스크롤마다 h1 transform+opacity 기록 | 삭제 |
| 이미지 치수 | 5개 전부 없음 | **5개 전부 명시** (488×566 실제 비율) |
| 이미지 404 | 5건 | **0건** |
| `content-visibility` | 없음 | 섹션·푸터 6곳 `auto` |
| 히어로 높이 | `100vh` | `100vh` + `100svh` (모바일 툴바 CLS) |
| 디스플레이 폰트 폴백 | `sans-serif` | `'Arial Black'` (swap 시 이동 감소) |

### v2 로컬 검증 (1440 / 390)

```
CLS 0 · 깨진 이미지 0 · 치수 없는 이미지 0
실행 중 애니메이션 1 · will-change 0 · reveal 노드 0
가로 오버플로 0 · JS 에러 0
로고 렌더 17×20px (488:566 비율 정확)
```

---

## 남은 것 — 여기서 PSI 점수가 더 나온다

CSS·JS 쪽은 정리됐다. 남은 건 워드프레스 구성이다.

| 순위 | 항목 | 근거 |
|---|---|---|
| 1 | 위 **버그 3개** 수정 | 성능 이전에 기능 문제 |
| 2 | 25KB 중복 CSS 레이어 제거 | v2 가 먹으려면 필수 |
| 3 | `wp-block-library` · `global-styles` · emoji dequeue | 15.4KB, 대부분 죽은 CSS |
| 4 | Pretendard **jsdelivr 16요청** | CSS 1 + woff2 서브셋 15개, 전부 서드파티 오리진 |
| 5 | Elementor·Essential Addons 전역 로딩 점검 | EA Post Grid 는 `/column` 에서만 쓰는데 전역 enqueue 되는지 확인 |
| 6 | 로고를 SVG 로 | 현재 WebP 4.5KB → SVG 면 1KB 미만. 원본 벡터 필요 |

4번은 자체 호스팅이 정답이지만 서브셋 파일이 많다. 한글 사이트에서는
dynamic-subset 방식이 전송량 자체는 작으니, 요청 수와 전송량 중 무엇을
줄일지 실제 PSI 결과를 보고 정하는 게 낫다.

---

## 측정에 대한 정직한 한계

- **이 문서에 PSI 점수는 없다.** 로컬 환경은 프록시가 폰트 CDN 을 막아
  FCP·LCP 가 12초로 찍힌다. 실제 점수는 배포 후 PageSpeed Insights 에서 재야 한다.
- 라이브 실측(FCP 920ms · TTFB 778ms · 25요청 · DOM 368노드)은 **캐시가 더운 상태**라
  전송량이 21KB 로 나왔다. 최초 방문 수치가 아니다.
- 위 표의 "후" 값은 전부 v2 로컬 렌더에서 확인한 것이고, 라이브 적용 후 재측정이 필요하다.
