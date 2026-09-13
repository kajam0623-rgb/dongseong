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
| `global.css` 원본 크기 | 53,649B | 60,819B (**+13%**) — 아래 정정 참조 |
| `global.css` **gzip** | 26,361B | **19,427B** (−26%) |
| 로고 인라인 payload | PNG base64 23,962B (CSS의 **45%**) | WebP base64 6,023B (−75%) |
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

---

## ★ 정정 — CSS 크기 (2026-09-13 재측정 · 여백/대비 작업 후 갱신)

이 문서는 처음에 `global.css` 가 **37,745B 로 30% 줄었다**고 적었습니다.
그건 성능 패스 직후의 값이고, 그 뒤로 증거 밴드 · 진단 카드 · 실적 밴드 ·
About 블록의 CSS 가 들어가면서 **지금은 원본보다 큽니다.** 실측:

| | 원본 v1 | v2 현재 | 차이 |
|---|---|---|---|
| 총 바이트 | 53,649 | 60,819 | **+7,170 (+13%)** |
| **gzip** | 26,361 | **19,427** | **−6,934 (−26%)** |
| base64 로고 | 23,962 | 6,023 | −17,939 (−75%) |
| 순수 규칙 | 29,687 | 54,796 | +25,109 |
| 규칙 수 | 290 | 501 | +211 |

읽는 법:

- **실제로 전송되는 값은 gzip 쪽입니다.** 인라인 `<style>` 은 HTML 문서의 일부로
  압축돼 나가므로, 회선을 타는 양은 26.4KB → 18.2KB 로 **31% 줄었습니다.**
- 압축 전 바이트가 8% 늘어난 것은 섹션을 다섯 개 새로 만들었기 때문입니다
  (규칙 290 → 490). CSS 텍스트는 반복이 많아 압축이 잘 먹습니다.
- 압축과 무관하게 **파싱 비용은 규칙 수에 비례**합니다. 200개가 늘었으니
  공짜는 아닙니다. 다만 아래 "죽은 CSS" 표의 낭비(wp-block-library 4.2KB 가 블록
  0개에 대해, autoptimize 94~95% 미사용)에 비하면 훨씬 작은 비용입니다.
- 로고 payload 는 CSS 의 45% → 10% 로 내려왔습니다.


---

## `/dental` 랜딩 — 실측과 조치

사이트에서 가장 큰 페이지(76.7KB)이고, 홈 Featured 카드가 여기로 보냅니다.
그런데 성능 이전에 **모바일에서 레이아웃이 무너져 있었습니다.**

| 뷰포트 | 가로 오버플로 | 뷰포트보다 넓은 노드 |
|---|---|---|
| 390px | **470px** | **276개** |
| 768px | 92px | 23개 |
| 1440px | 0 | 0 |

`.page{width:860px}` 고정폭 + 미디어쿼리 2개(둘 다 카톡 버튼용)가 원인입니다.

| 항목 | 전 | 후 |
|---|---|---|
| 가로 오버플로 (390) | 470px | **0** |
| 최대 제목 (390) | 88px | **38px** |
| `will-change` 노드 | 33 | **0** |
| 무한 애니메이션 | 3 | **0** |
| Pretendard 로드 | 2벌 | 1벌 |
| 카카오 플로팅 버튼 | 2개 | 1개 |
| 스타일시트 요청 | 3 | 2 |

특히 두 가지가 성능에 직접 붙습니다:

1. **`will-change:transform,opacity` 가 `.scr.snap > *` 에** 걸려 있어 상시 합성
   레이어를 33개 만들고 있었습니다. 리빌은 한 번 끝나면 다시 안 일어나므로
   미리 레이어를 잡아둘 이유가 없습니다.
2. **`pulse` 는 `box-shadow` 애니메이션**입니다. transform/opacity 와 달리
   합성으로 처리되지 않고 **매 프레임 페인트**를 유발하는데, 무한 반복이라
   페이지를 열어 두는 내내 돕니다. 정적 링으로 바꿨습니다.

그리고 `#ciclo-dental html{scroll-snap-type:y proximity}` 는 `html` 이 `div` 의
자손일 수 없어 **한 번도 적용된 적이 없습니다**(실측 `scrollSnapType:none`).

리빌 126개는 1440/390 양쪽에서 전부 정상 발화하는 것을 확인해 남겼습니다
(끝까지 스크롤 후 잔여 0개). 메인 사이트 리빌과 달리 버그가 없습니다.

### 갱신 이력

CSS 를 건드릴 때마다 다시 재야 하는 값입니다. 지금까지:

| 시점 | 총 바이트 | gzip | 규칙 수 |
|---|---|---|---|
| 원본 v1 | 53,649 | 26,361 | 290 |
| 성능 패스 직후 | 37,745 | — | — |
| 실적 밴드·About 추가 후 | 57,820 | 18,244 | 490 |
| 여백 확장·대비 상향 후 | 60,819 | 19,427 | 501 |
| **Archivo 제거·Pretendard 통일 후 (현재)** | **62,480** | **19,433** | **501** |

여백·대비 작업으로 규칙이 11개 늘고 gzip 이 1.2KB 늘었습니다. 늘어난 것
대부분이 고정값을 `clamp()` 로 바꾼 기존 선언이라 규칙 수는 거의 그대로입니다.
**gzip 기준 원본 대비 여전히 26% 작습니다.**

---

## 접근성 — 대비 실측과 조치 (2026-09-13)

사용자가 세운 "PageSpeed 100점" 목표에는 접근성 100점도 들어갑니다.
라이트하우스가 대비를 자동 검사하므로 미달이 남으면 100 이 안 나옵니다.

텍스트 노드를 가진 요소를 전수 대조했더니 **27곳이 WCAG AA 미달**이었습니다.

| 배경 | 색 | 대비 | 기준 |
|---|---|---|---|
| 크림 `#F4F1EA` | `rgba(18,18,18,.48)` | 3.23 | 4.5 |
| 패널 `#ECE7DC` | `rgba(18,18,18,.48)` | **3.16** | 4.5 |
| 크림·패널 | `rgba(18,18,18,.5)` | 3.35~3.43 | 4.5 |
| 크림·패널 | `rgba(18,18,18,.55)` | 3.90~4.00 | 4.5 |
| 네이비 `#111E6C` | `rgba(255,255,255,.35)` | **2.96** | 4.5 |
| 흰 카드 | `rgba(17,30,108,.6)` | 4.26 | 4.5 |

임계값을 계산해서(패널이 크림보다 어두워 빡빡한 쪽 기준) 올렸습니다:

```
크림·패널 위 잉크   α ≥ .62   (4.87:1)
네이비 위 흰색      α ≥ .55   (5.33:1)
흰 카드 위 네이비   α ≥ .62   (4.53:1)
```

`color:` 선언 39곳을 상향했습니다. 테두리·배경·그림자로 쓰는 `rgba` 는
대비 대상이 아니라 건드리지 않았습니다.

가장 눈에 띄는 개선은 증거 밴드 차트의 **축 눈금(0·20·40·60·80·100)** 입니다.
`rgba(255,255,255,.35)` 라 2.96:1 이었고 실제로 거의 안 보였습니다.

### 오탐 하나를 걸러냈습니다

`.ev-dot > b`(점 위 숫자 라벨)가 **1.17:1** 로 잡혔는데, 측정 스크립트가
부모인 노란 점을 배경으로 잡아서 나온 값입니다. 라벨은 실제로는 점 **위쪽
네이비 바탕**에 놓입니다(흰색 .6 on 네이비 = 5.8:1, 통과). 색을 바꾸지 않았습니다.

---

## 폰트 통일로 줄어든 요청 (2026-09-13)

Archivo 를 걷어내고 Pretendard 하나로 통일했습니다. CSS 바이트는 폴백 문자열이
길어져 1.7KB 늘었지만(gzip 은 +6B, 사실상 동일), **요청과 오리진이 줄었습니다.**

| 항목 | 전 | 후 |
|---|---|---|
| 렌더 차단 폰트 스타일시트 | 2장 | **1장** |
| 서드파티 폰트 오리진 | 3개 (googleapis · gstatic · jsdelivr) | **1개** (jsdelivr) |
| `preconnect` | 3줄 | **1줄** |
| Archivo woff2 | 3벌 (700/800/900) | **0** |

폰트 CSS 는 렌더 차단이라 한 장 줄이는 것이 바이트보다 FCP 에 크게 작용합니다.
오리진 두 개가 사라지면 DNS 조회 + TLS 핸드셰이크가 두 번 없어집니다.

남은 개선은 Pretendard 자체 호스팅입니다. 그러면 서드파티 오리진이 0이 됩니다.

