# cream 2026년 11월호 (VOL.179) 웹진

SBS M&C 월간 매거진 cream 11월호 PDF를 웹진으로 옮긴 정적 사이트. 빌드 없음 — `index.html`을 열면 된다.

## 진행 단계
- [x] 1단계: 메인(`index.html`) + Trend & Focus(`trend.html`)
- [ ] Contents Line-up / Sales Guide / SBS Digital / Program Table / Contact

## 구조
- `css/common.css` — 토큰(섹션 컬러 5종), 헤더·전체메뉴·푸터, 리빌 모션
- `css/main.css`, `css/article.css` — 페이지별 스타일
- `js/common.js` — 목차 데이터(`SECTIONS`), 헤더/메뉴/푸터 주입, 스크롤 리빌·글자 분할·패럴랙스·카운트업·드래그 트랙
- `images/` — PDF에서 추출한 이미지(고해상도 원본으로 교체 권장)

## 모션 규칙
- `data-reveal` (기본 페이드업 / `fade` / `clip` / `clip-x` / `line`), `--d`로 지연(초)
- `data-split` 글자 단위 등장, `.lines` 줄 단위 등장, `data-parallax="0.1"`, `data-count="7800"`
- `clip`은 대상의 **자식**을 잘라낸다(대상 자체를 자르면 IntersectionObserver가 면적 0으로 보고 발동하지 않음)
- `prefers-reduced-motion` 사용자는 모든 모션 해제
