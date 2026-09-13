# CICLO 테마

Elementor · WPCode 없이 도는 자체 테마입니다.

> 이 파일은 `theme-README.md` 가 원본이고, `build-theme.py` 가 테마 폴더 안으로
> 복사합니다. 고치실 때는 원본을 고치세요 — 테마 폴더는 빌드할 때마다 새로 만듭니다.

---

## 왜 만들었나

지금 사이트는 층이 넷입니다.

```
Hello Elementor 테마
  └ Elementor 위젯 (페이지 마크업이 JSON 안에 들어 있음)
      └ WPCode 스니펫 (CSS · JS · 폰트)
          └ 커스터마이저 추가 CSS
```

이 층들이 서로 싸워서 생긴 게 그동안 고친 문제들입니다.

| 지금 구조의 문제 | 테마에서는 |
|---|---|
| 25KB 중복 CSS 가 특정성 (1,1,0) 으로 원본 (0,1,0) 을 이김 | CSS 가 한 곳뿐이라 **구조적으로 발생 불가** |
| 커스터마이저 `max-width:820px` 가 홈까지 누름 | 템플릿이 직접 그리므로 그런 규칙이 없음 |
| JS 스니펫 하나가 죽으면 사이트 기능이 통째로 죽음 | `wp_enqueue_script` 로 정상 로드 |
| Elementor 호환 CSS 25줄 | **삭제** |
| Essential Addons 클래스에 `!important` 21개 | **삭제** — 마크업을 우리가 그림 |
| Elementor + Essential Addons 가 전 페이지에 CSS/JS 로드 | **제거** |

마지막이 가장 큽니다. 남은 성능 개선 중 제일 큰 항목입니다.

---

## 설치

1. `ciclo-theme` 폴더를 통째로 zip 으로 묶습니다
   (폴더 자체가 zip 안에 들어가야 합니다 — 안의 파일만 묶으면 안 됩니다)
2. 워드프레스 > 외모 > 테마 > 새로 추가 > **테마 업로드**
3. **활성화하기 전에** 아래 §페이지 준비 를 먼저 하세요
4. 활성화 → 화면 확인

> **되돌리기는 한 번 클릭입니다.** 외모 > 테마에서 이전 테마를 다시 활성화하면
> 즉시 원래대로 돌아갑니다. 기존 Elementor 데이터와 WPCode 스니펫은 그대로
> 남아 있으므로 잃는 것이 없습니다.
> 그래서 WPCode 를 직접 수술하는 것보다 이쪽이 안전합니다.

---

## 페이지 준비 — 슬러그가 중요합니다

템플릿은 **페이지 슬러그**로 붙습니다. 슬러그가 다르면 그 페이지만 기본
템플릿(`page.php`)으로 떨어집니다.

| 페이지 | 슬러그 | 템플릿 |
|---|---|---|
| 홈 | (설정 > 읽기 에서 홈으로 지정) | `front-page.php` |
| Work | `work` | `page-work.php` |
| About | `about` | `page-about.php` |
| Contact | `contact` | `page-contact.php` |
| Website Design | `website-design` | `page-website-design.php` |
| GEO | `geo` | `page-geo.php` |
| Blog Content | `blog-content` | `page-blog-content.php` |
| Digital Marketing | `digital-marketing` | `page-digital-marketing.php` |
| 치과 홈페이지 제작 | `dental` | `page-dental.php` |
| 칼럼 | `column` | `page-column.php` |

**페이지 내용은 비워도 됩니다.** 마크업이 템플릿 안에 있어서 에디터 내용은
쓰지 않습니다. 기존 Elementor 내용을 지울 필요도 없습니다 — 그냥 무시됩니다.

칼럼 카테고리는 슬러그 `seo` · `geo` · `hospital` · `content` · `ads` ·
`case` · `insight` 를 씁니다. 다르면 `functions.php` 의
`ciclo_column_cats()` 를 고치세요.

---

## 내용을 고치려면

| 무엇 | 어디 |
|---|---|
| 홈·서브페이지 문구 | 해당 `*.php` 파일 (마크업이 그대로 들어 있습니다) |
| 색·타이포·여백 | `assets/css/global.css` |
| 사이드바 동작·현재 페이지 표시 | `assets/js/ciclo-effects.js` |
| 칼럼 글 | 워드프레스 글쓰기 (평소대로) |
| 칼럼 카테고리 메뉴 | `functions.php` 의 `ciclo_column_cats()` |

페이지 문구가 파일로 옮겨간 것이 이 방식의 유일한 단점입니다. 다만 지금도
Elementor 텍스트 위젯 안의 HTML 을 고치고 계셨으니 실질적인 차이는
"어디서 여느냐" 뿐입니다.

---

## 켠 뒤 확인할 것

| 확인 | 정상이면 |
|---|---|
| 홈 F12 > Console | 빨간 에러 0개 |
| 홈 본문 폭 | 1280px 까지 사용 |
| **칼럼 목록** | 글 10개 · 썸네일 · 날짜 · 카테고리 · 페이지 번호 |
| **칼럼 글 상세** | 제목 · 본문 · 이전/다음 글 |
| 카테고리 메뉴 | 클릭하면 해당 분류 글만 |
| 휴대폰 `/dental` | 옆으로 밀리지 않음 |
| F12 > Network > CSS | 스타일시트 **2장**(Pretendard + global.css) |

> ★ **칼럼 두 페이지를 먼저 봐 주세요.**
> 나머지 페이지 마크업은 브라우저 실측으로 검증했지만, 칼럼 목록과 글 상세는
> Essential Addons Post Grid 를 걷어내면서 **새로 쓴 것**입니다.
> 워드프레스 없이 테스트할 수 없어 실제 글로는 확인하지 못했습니다.

---

## 검증한 것과 못 한 것

**검증한 것**

- PHP 문법 — 18개 파일 `php -l` 전부 통과
- 템플릿 실행 — 워드프레스 함수를 스텁으로 채워 15개 템플릿을 실제로 실행,
  Fatal error 0건 (`../tools/render-theme.php`)
- 출력 HTML — doctype · `</html>` · `<body>` 1개 · `<main>` 1개 · h1 1개 ·
  PHP 잔존 0 · 경고 0
- 브라우저 실측 (1440 / 390) — CSS 적용 · 가로 넘침 0 · 겹침 0 · CLS 0 ·
  깨진 이미지 0 · JS 에러 0 · 대비 AA 미달 0

**못 한 것 (워드프레스가 없어서)**

- 템플릿 계층이 실제로 `page-work.php` 를 고르는지 — 규칙 자체는 표준입니다
- 실제 DB 의 글로 도는 칼럼 루프 — 가짜 글 3개로 대신했습니다
- 다른 플러그인(SEO · 폼 · 캐시)과의 충돌
- 관리자 화면

---

## 플러그인 정리는 나중에

테마를 켜도 Elementor 는 **일단 그대로 두세요.** 화면이 정상인 것을 며칠
확인한 뒤에 비활성화하는 편이 안전합니다. 순서는 이렇습니다.

1. 테마 활성화 → 전 페이지 확인
2. 문제 없으면 **Essential Addons** 비활성화 → 다시 확인
3. 그 다음 **Elementor** 비활성화 → 다시 확인
4. 마지막으로 **WPCode 스니펫** 비활성화 (삭제 말고 비활성화)

각 단계마다 화면을 보고 넘어가면, 문제가 생겼을 때 무엇 때문인지 바로 압니다.
WPCode 안에 서치어드바이저 소유확인이나 애널리틱스가 있을 수 있으니
4단계는 특히 하나씩 확인하세요 (자세한 내용은 상위 폴더 `DEPLOY.md`).
