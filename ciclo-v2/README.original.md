# CICLO 워드프레스(Elementor) 이식 패키지 — Hello Elementor + 전역 헤더/푸터 + 칼럼(블로그)

`import.xml` 하나로 **9개 페이지 + 전역 헤더/푸터**가 생성됩니다.
- 홈, Website Design, GEO, Blog Content, Digital Marketing, Work, About, Contact
- **칼럼** — 인블로그 스타일 글 목록(EA Post Grid). 글은 워드프레스 **글**로 작성
- **CICLO Header / CICLO Footer** — 전 사이트 공통 상단 내비·푸터(칼럼·글 상세까지)

---

## 준비물 (플러그인 4개)

| 플러그인 | 용도 |
|---|---|
| **Elementor** (무료) | 페이지 빌더 |
| **Essential Addons for Elementor** (무료) | 칼럼의 글 목록 위젯(EA Post Grid) |
| **Header Footer & Blocks Template Builder** (무료, 포스트타입 `elementor-hf`) 또는 UAE | 전역 헤더/푸터 |
| **WPCode** (무료) | 전역 CSS·JS 삽입 |

> 테마는 **Hello Elementor** 그대로 사용합니다.
> 헤더/푸터 빌더가 있어야 CICLO Header/Footer가 전 페이지에 뜹니다.

---

## 설치 순서

### 1. 이미지 업로드
`images/`의 로고 2개를 **미디어 > 새로 추가**. (참조 경로 `/wp-content/uploads/mark-ciclo-white.png`.
로고는 `global.css`에도 내장돼 있어 내비/히어로/푸터는 안 깨집니다.)

### 2. XML 가져오기
**도구 > 가져오기 > WordPress** → `import.xml`.
- 재가져오기라면 **기존 CICLO 페이지 삭제 + 휴지통 비우기** 먼저.
- 페이지 9개 + 헤더/푸터 2개 생성.

### 3. Elementor 파일 재생성
**Elementor > 도구 > 파일 및 데이터 재생성**.

### 4. 전역 CSS (WPCode · CSS Snippet · Auto Insert / Site Wide)
`css/global.css` 전체 붙여넣기. (폰트 `@import`가 맨 위에 포함 → 폰트 자동 적용)

### 5. JS 효과 (WPCode · JavaScript Snippet · Site Wide Footer) — 각각
- `js/ciclo-effects.js` (사이드바·스크롤 효과)
- `js/img-fallback.js` (이미지 경로 보정)

### 6. 헤더/푸터 표시 확인
Header Footer & Blocks 설정에서 `CICLO Header`·`CICLO Footer`가
**전체 사이트(Entire Site)** 로 지정됐는지 확인. (XML에 이미 넣어둠)

### 7. 홈페이지 지정
**설정 > 읽기 > 정적인 페이지 > 홈페이지: Home**.

### 8. 칼럼(글) 작성 & 카테고리
- **글 > 새로 추가**로 작성 → **대표 이미지** 지정(썸네일로 보임), **카테고리** 선택.
- 목록은 `/column/`(칼럼 페이지)에서 인블로그 스타일 카드로 자동 표시됩니다.
- 칼럼 페이지 왼쪽 메뉴의 카테고리 링크는 `/category/seo/`처럼 되어 있습니다.
  실제 카테고리 슬러그에 맞춰 각 링크를 수정하거나, 그 슬러그로 카테고리를 만드세요.
  (Elementor에서 칼럼 페이지 편집 > 왼쪽 텍스트 위젯에서 링크·이름 수정)

### 9. 캐시 삭제 후 시크릿 창 확인.

---

## 편집
- 8개 페이지: 텍스트 위젯 1개에 원본 마크업 → 문구·링크 편집.
- 칼럼 페이지: 왼쪽 카테고리 메뉴(텍스트 위젯) + 오른쪽 **EA Post Grid** 위젯.
  글 수·정렬·발췌 길이 등은 그 위젯 설정에서 조절.
- 헤더/푸터: `CICLO Header`/`CICLO Footer` 템플릿에서 편집(전 사이트 반영).
- 색·간격·호버·애니메이션·칼럼 카드 디자인 = `global.css` 클래스.

## 파일 구성
```
wordpress-import/
├─ import.xml            ← 9개 페이지 + 전역 헤더/푸터
├─ css/global.css        ← 전역 CSS(폰트·로고 내장 · 칼럼 인블로그 스타일 포함)
├─ js/ciclo-effects.js · js/img-fallback.js
├─ images/               ← 로고 (미디어 업로드용)
├─ templates/*.json      ← 페이지·헤더·푸터 개별 백업
└─ README.md
```

## 문제 해결
| 증상 | 해결 |
|---|---|
| 헤더/푸터 안 뜸 | Header Footer & Blocks 미설치 또는 표시위치 미지정 |
| 칼럼 목록이 비었거나 위젯 오류 | Essential Addons 활성화 확인 → 3번 재생성 → 글이 1개 이상 있는지 |
| 칼럼 카드 디자인 안 먹음 | 4번 CSS 미적용 |
| 스타일 전혀 안 먹음 | CSS Snippet에 `<link>`/HTML 혼입, 또는 Auto Insert 아님 |
| 테마 헤더/"Hello world" 기본화면 | 7번 홈페이지 지정 안 됨 |
| 방문자에게 옛 화면 | 9번 캐시 |
