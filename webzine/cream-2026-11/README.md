# cream 2026년 11월호 (VOL.179) 웹진

SBS M&C 월간 매거진 cream 11월호 PDF를 **원본 지면 디자인 그대로** 옮긴 정적 사이트. 빌드 없음 — `index.html`을 열면 된다.

## 페이지 (원본 쪽수)
| 파일 | 섹션 | 쪽 |
|---|---|---|
| index.html | 표지 + 목차 | 1–2 |
| trend.html | Trend & Focus | 3–9 |
| lineup.html | Contents Line-up | 10–17 |
| sales-tv.html | Sales Guide · SBS-TV | 18–27 |
| sales-addressable.html | Sales Guide · 어드레서블 TV | 28–30 |
| sales-medianet.html | Sales Guide · 미디어넷 | 31–41 |
| sales-radio.html | Sales Guide · 라디오 | 42–43 |
| digital.html | SBS Digital | 44–48 |
| table.html | Program Table (편성표 = 원본 지면 이미지, 누르면 확대) | 49–58 |
| support.html | 마케팅 지원 제도 · CONTACT POINT · 뒤표지 | 59–62 |

각 쪽은 `<section id="p쪽번호">` — 목차 링크가 이 앵커로 간다.

## 구조
- `_template.html` — 새 페이지 시작점(head, 폰트, 간지, 페이저)
- `css/common.css` — PDF 실측 섹션 컬러, 라인·점 제목(`.pg-title`), 소제목(`.sub`), 컬러 헤더 표(`.tbl`), 간지(`.divider`) 등 공통 컴포넌트
- `css/pages/*.css` — 페이지 전용 스타일
- `js/common.js` — 목차 데이터(`SECTIONS`), 헤더·목차 메뉴·푸터 주입, 등장 모션, `img[data-zoom]` 확대
- `images/<페이지>/` — PDF 300dpi 렌더/추출 이미지

## 원칙
- 원본에 없는 장식 금지(그라데이션·그림자·이모지·카운트업 등). 모션은 `data-reveal` 페이드업만.
- 텍스트·숫자는 PDF 그대로(원문 오탈자 포함).
