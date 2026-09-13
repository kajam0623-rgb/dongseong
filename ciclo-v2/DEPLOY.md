# 배포 체크리스트

> **먼저: WPCode 를 다 지우면 안 됩니다.**
> 지금 사이트 디자인을 그리고 있는 것도 WPCode 안에 있습니다. 다 지우면
> 화면이 워드프레스 기본 테마로 돌아갑니다.
> 지울 것 · 바꿀 것 · 손대면 안 되는 것이 섞여 있어서, 하나씩 구분해야 합니다.

---

## 0. 시작하기 전에 — 백업

WPCode 목록 화면에서 스니펫을 전부 선택 → **Export** 하세요.
JSON 한 파일로 떨어집니다. 뭔가 잘못되면 Import 로 그대로 되돌릴 수 있습니다.

커스터마이저 추가 CSS 도 따로 복사해 두세요
(외모 > 사용자 정의하기 > 추가 CSS — 전체 선택해서 메모장에 붙여넣기).

---

## 1. 스니펫 구분법

WPCode 목록에서 각 스니펫을 열어 **첫 줄**을 보고 판단하면 됩니다.

| 찾는 표시 | 정체 | 할 일 |
|---|---|---|
| `.ciclo-page{max-width:none!important` 로 시작하거나<br>안에 `#ciclo-home` 이 잔뜩 보임 | **25KB 중복 CSS 복사본** | **삭제** |
| `@import` 로 시작하는 긴 CSS | 기존 `global.css` | **내용 교체** → `css/global.css` |
| `.nav-burger` · `IntersectionObserver` · `reveal` 이 보이는 JS | 기존 `ciclo-effects.js` | **내용 교체** → `js/ciclo-effects.js` |
| 끝에 `{ "@context": "https://schema.org"` 가 붙어 있는 JS | **지금 사이트를 망가뜨리는 것** | 그 **JSON-LD 블록만 삭제**<br>(스니펫 자체는 위에서 교체되므로 사실상 같이 해결) |
| `<link rel="preconnect"` · 폰트 `<link>` 가 있는 HTML | 폰트 로딩 | **내용 교체** → `wpcode-head.html`<br>없으면 새로 추가 |
| 위 어디에도 안 맞는 것 | 아래 §2 참조 | **일단 두세요** |

### 교체는 이렇게

스니펫을 **지우고 새로 만들지 말고**, 열어서 **안의 코드만 전체 선택 → 새 내용 붙여넣기** 하세요.
지우고 다시 만들면 삽입 위치(Site Wide Header / Footer) 설정을 다시 잡아야 하고,
거기서 틀리면 폰트나 JS 가 엉뚱한 자리에 들어갑니다.

| 파일 | WPCode 종류 | 위치 |
|---|---|---|
| `css/global.css` | CSS Snippet | Site Wide Header |
| `js/ciclo-effects.js` | JavaScript Snippet | **Site Wide Footer** |
| `wpcode-head.html` | HTML Snippet | **Site Wide Header** |
| `wpcode-dequeue.php` (선택) | PHP Snippet | Run Everywhere |

---

## 2. 제가 모르는 스니펫이 있을 수 있습니다

저는 라이브 화면에 **출력된 결과**만 봤지 WPCode 목록 자체는 못 봤습니다.
아래 같은 것들이 있으면 **절대 지우지 마세요.** 지워도 화면은 멀쩡해 보여서
한참 뒤에야 알게 됩니다.

- 네이버 서치어드바이저 · 구글 서치콘솔 **소유확인 메타태그**
  → 지우면 며칠 뒤 소유확인이 풀리고 수집 데이터가 끊깁니다.
    실적 밴드의 근거 자료가 여기서 나옵니다.
- **구글 애널리틱스 / 네이버 애널리틱스 / 픽셀** 추적 코드
- 카카오 채널 · 채팅 위젯 스크립트
- 폼 전송, 예약 연동 같은 기능성 코드

**판단이 안 서면 지우지 말고 비활성화(Deactivate)만 하세요.**
화면을 확인한 뒤 문제가 없으면 나중에 지우면 됩니다. 되돌리기가 한 번 클릭입니다.

---

## 3. 커스터마이저 추가 CSS — WPCode 가 아닙니다

홈이 820px 로 눌려 있는 문제는 **WPCode 가 아니라 커스터마이저**에 있습니다.
WPCode 를 아무리 정리해도 이건 안 고쳐집니다.

외모 > 사용자 정의하기 > 추가 CSS 에서 `max-width:820px` 규칙을 찾아
아래처럼 범위를 좁혀 주세요.

```css
body.single main.site-main>.page-header,
body.single main.site-main>.page-content,
body.archive main.site-main>.page-content,
body.blog   main.site-main>.page-content{max-width:820px;margin-left:auto;margin-right:auto}
```

지금은 `body` 조건이 없어서 홈까지 820px 로 눌립니다.

---

## 4. 순서

순서를 지켜야 합니다. 특히 1번을 건너뛰면 **나머지가 전부 헛일이 됩니다.**

1. **25KB 중복 CSS 스니펫 삭제**
   `#ciclo-home` 은 특정성 (1,1,0) 이라 원본 `global.css` 의 (0,1,0) 을 이깁니다.
   이걸 안 지우면 `global.css` 를 바꿔도 **화면이 거의 그대로입니다.**
2. **커스터마이저 추가 CSS 의 820px 규칙에 `body` 조건** (§3)
3. `global.css` 교체
4. `ciclo-effects.js` 교체
5. `wpcode-head.html` 추가/교체
6. (선택) `wpcode-dequeue.php` 추가
7. 페이지 마크업 교체 (Elementor 텍스트 위젯)

> **3·4·5 는 세트입니다.**
> CSS 만 바꾸고 JS 를 그대로 두면 구버전 JS 가 `.reveal` 을 주입해 콘텐츠가
> 보이지 않습니다. 헤드 스니펫을 안 넣으면 폰트가 적용되지 않습니다.
> 한 번에 셋 다 바꾸고 화면을 확인하세요.

---

## 5. 바꾼 뒤 확인할 것

캐시부터 비우세요 (Autoptimize · 호스팅 캐시 · 브라우저 강력 새로고침).
안 그러면 예전 화면을 보고 "안 바뀌었다" 고 판단하게 됩니다.

| 확인 | 정상이면 |
|---|---|
| 홈을 열고 F12 > Console | **빨간 에러 0개** (지금은 `SyntaxError` 가 떠 있습니다) |
| 홈 본문 폭 | 1280px 까지 씁니다 (지금은 820px) |
| 히어로 | 네이비 `CICLO.` + "GEO 웹사이트, 랜딩페이지 제작" |
| 스크롤 | 콘텐츠가 처음부터 다 보입니다 (사라졌다 나타나지 않음) |
| 휴대폰에서 `/dental` | 옆으로 밀리지 않습니다 (지금은 470px 밀립니다) |
| F12 > Network > CSS 필터 | 폰트 스타일시트가 **1장**뿐 (구글 폰트 없음) |

그다음 PageSpeed Insights 로 실제 점수를 재시면 됩니다.
로컬에서는 프록시가 폰트 CDN 을 막아 측정이 안 됩니다 — 그래서 이 패키지에
PSI 점수가 없습니다. 실제 점수가 나오면 남은 최적화(Pretendard 자체 호스팅 등)를
그 숫자를 보고 정하는 게 맞습니다.

---

## 6. 되돌리기

무엇이 잘못됐든 §0 에서 받아 둔 Export JSON 을 Import 하면 원래대로 돌아갑니다.
페이지 마크업은 워드프레스 리비전(게시물 편집 화면 우측 "리비전")으로 복구됩니다.
