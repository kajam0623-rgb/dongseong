# CICLO v2 — 238LAB 벤치마킹 반영 패키지

원본 `Ciclo 회사 홈페이지 디자인 (1).zip` 을 기준으로, `references/238lab-adoption-plan.md`
실행 1~4번을 **소스에 직접 반영**한 버전이다. 오버라이드 CSS(`ciclo-patch-01/02`)는 이걸로 대체된다.

## 파일

```
ciclo-v2/
├─ css/global.css              ← 교체본 (v1은 global.original.css 로 보존)
├─ js/ciclo-effects.js         ← 교체본 (v1은 ciclo-effects.original.js)
├─ pages/                      ← import.xml 에서 추출한 페이지별 마크업
│   ├─ Home.html               ← h2 한글 문장형 반영됨
│   ├─ CICLO_Footer.html       ← h2 한글 문장형 반영됨
│   └─ (나머지 9개는 원본 그대로)
├─ build-css.py                ← 원본 CSS → v2 변환 스크립트 (44건, 정확 문자열 치환)
├─ build-pages.py              ← 원본 마크업 → v2 변환 스크립트 (13건)
└─ import.original.xml         ← 원본 보존
```

`build-*.py` 를 남겨둔 이유: 원본이 갱신되면 다시 돌려서 같은 변경을 재적용할 수 있다.
두 스크립트 모두 **매칭이 정확히 1건이 아니면 즉시 실패**하므로, 원본이 바뀌면 조용히 틀리지 않고 멈춘다.

---

## 적용 방법 (비파괴)

XML 재가져오기는 **하지 않는다.** 기존 페이지를 지우게 되고, 그동안 워드프레스에서 한 수정이 날아간다.

| 순서 | 대상 | 방법 |
|---|---|---|
| 1 | `css/global.css` | WPCode → CSS Snippet → 기존 내용 전체 교체 |
| 2 | `js/ciclo-effects.js` | WPCode → JavaScript Snippet → 기존 내용 전체 교체 |
| 3 | `pages/Home.html` | Elementor → Home 편집 → 텍스트 위젯 → 코드 보기 → 교체 |
| 4 | `pages/CICLO_Footer.html` | Elementor → CICLO Footer 템플릿 → 텍스트 위젯 교체 |
| 5 | — | Elementor > 도구 > 파일 재생성 + Autoptimize 캐시 삭제 |

**CSS 를 먼저 바꿀 것.** JS 를 먼저 바꾸면 구버전 CSS 의 `.reveal{opacity:0}` 이 남아
콘텐츠가 안 보이는 구간이 생긴다.

---

## ★ 별도로 고쳐야 하는 것 — 홈이 820px 로 눌려 있다

이건 이 패키지 밖의 문제다. 워드프레스 **커스터마이저 → 추가 CSS** 에 이 규칙이 있다:

```css
main.site-main>.page-header,
main.site-main>.page-content{max-width:820px;margin-left:auto;margin-right:auto}
```

블로그 목록·글 상세용으로 쓰신 건데 `body` 조건이 없어서 **홈까지 잡는다.**
`.section{max-width:1280px}` 으로 설계된 홈이 820px, 즉 64% 폭으로 렌더링되고 있다.

**고치는 법** — 추가 CSS 의 그 줄을 아래처럼 범위를 좁힌다:

```css
body.single main.site-main>.page-header,
body.single main.site-main>.page-content,
body.archive main.site-main>.page-content,
body.blog main.site-main>.page-content{max-width:820px;margin-left:auto;margin-right:auto}
```

`global.css` v2 에 `main.site-main>.page-content:has(.ciclo-page){max-width:none}` 방어선을
넣어 두긴 했지만, 근본 해결은 위쪽이다.

---

## 변경 내역

### CSS 44건

**타이포**
- `body` 에 `font-weight:400; line-height:1.7; word-break:keep-all` 추가
- 본문 13곳 `font-weight:500 → 400` (`.hero .lead` `.page-hero .lead` `.svc-row p` `.card p`
  `.step p` `.work-desc` `.about-body` `.mean p` `.faq-row p` `.cp-step p` `.cp-note`
  `.footer .lead` `.sidebar-contact`)
- `.overline` 13px/700/.22em → **14px/600/.24em**
- `.sec-h2` Archivo 900 clamp(40,5.5vw,80)/lh1/uppercase
  → **Pretendard 700 clamp(28,3.2vw,40)/lh1.25/-.025em/none**
- `.footer h2` 도 같은 스케일로
- `.hero .lead` clamp(16,1.6vw,19)/1.65 → clamp(17,1.7vw,20)/1.55
- **신설**: `.sec-lead`(18px/400/1.55) · `.sec-link` · `.sec-caption`
  — 238LAB 섹션 원자 구조(눈썹 → h2 → 리드 → 링크 → 증거 → 출처)의 빈 슬롯

**모션 — 방향은 "빼기"**
- `.reveal` 규칙 삭제 (238LAB은 스크롤 리빌 0개)
- 히어로 원형 마크 `spin 40s` 제거
- SCROLL 배지 `spin 16s` 제거
- 마퀴 `26s → 40s`
- 호버 리프트 **6개 전부 제거** (`.btn-primary` -2px, `.card` -4px, `.channel` -3px,
  `.kakao-float` -2px, `.kakao-btn` -1px, `.btn-white` -2px) → 색·테두리 변화로 대체
- 호버 트랜지션 `.18s cubic-bezier(.2,.8,.2,1)` → `.15s cubic-bezier(.4,0,.2,1)`
- `prefers-reduced-motion` 가드 추가

**라운드**
- 알약 999px → **4px**: `.btn` `.nav-cta` `.chip` `.other-pill` `.kakao-btn`
- 카드 20px → **12px**: `.card` `.proc-card` `.work-slot` `.mean` `.channel` `.contact-proc`
- 유지(관례): `.nav` 플로팅 바, `.nav-burger`, `.sidebar-close`, `.kakao-float`

**레이아웃**
- `.section` 세로 패딩 `clamp(80,10vw,140)` → `clamp(80,11.2vw,160)`
  (10vw 로는 1440px 에서 144px 밖에 안 나와 238LAB 실측 160px 에 못 미쳤다)
- `.about-grid` `.8fr 1.2fr` → `1fr`
  (제목 컬럼이 242px 라 40px 한글 문장이 7줄로 터졌다)
- 420px 이하 h2 26px / 눈썹 12px / `<br>` 해제

### 마크업 13건

| 위치 | 눈썹 | h2 |
|---|---|---|
| 서비스 | `/SERVICES · WHAT WE DO` | 예쁘게 만드는 일과 검색되게 만드는 일을,<br>따로 맡기지 않으셔도 됩니다 |
| 사례 | `/WORK · SELECTED WORK` | 치과 여덟 곳을 직접 채점하고,<br>고칠 자리를 숫자로 짚었습니다 |
| 프로세스 | `/PROCESS · HOW WE WORK` | 진단부터 성장까지,<br>한 팀이 네 단계로 책임집니다 |
| 소개 | `/ABOUT · CICLO` | 예쁘기만 한 사이트가 아니라,<br>문의로 이어지는 사이트를 만듭니다 |
| FAQ | `/FAQ · QUESTIONS` | 견적서를 받으셨을 때,<br>항목을 짚으실 수 있게 적었습니다 |
| 문의(푸터) | `/CONTACT · LET'S TALK` | 무엇부터 손봐야 할지,<br>하루 안에 답을 드립니다 |

- 히어로 `Creative Clicks.` 는 **그대로 유지** (플랜 §0 결정)
- ABOUT h2 의 인라인 `style="font-size:clamp(40px,5vw,72px)"` 제거
  — CSS 를 이기고 있어서 안 지우면 한글 문장이 72px 로 나온다
- ABOUT 본문 마지막 문장은 h2 로 승격됐으므로 본문에서 삭제 (중복 제거)

### JS

- 스크롤 리빌 블록 삭제 (`.reveal` 주입 + IntersectionObserver + 70ms stagger)
- 히어로 패럴럭스 삭제 (h1 을 최대 220px 끌어내리고 y=620 에서 opacity 0 으로 죽이던 코드)
- 사이드바 토글만 유지, 포커스 이동 추가
- 구버전 캐시 대비 `.reveal` 잔재 정리 코드 추가

---

## 검증 (로컬 렌더, 1440 / 768 / 390)

| 항목 | 결과 |
|---|---|
| h2 | 40 / 28 / 26px, `text-transform:none`, 전부 2~3줄 |
| 눈썹 | 14px/600/ls 3.36px(=.24em), 모바일 12px |
| 본문 | `.svc-row p` 16px/400/27.2px(1.7) |
| 라운드 | `.chip` `.btn` 4px |
| 남은 애니메이션 | `marquee 40s` **1개뿐** (spin 2개 제거 확인) |
| 호버 리프트 | **0개** |
| `.reveal` 노드 | **0개** |
| 섹션 패딩 | 1440에서 **160px** |
| 가로 오버플로 | 0 (세 뷰포트 전부) |
| JS 에러 | 0 |
| `.section` 폭 | 1440에서 **1280px** (의도한 설계 폭) |

뷰포트보다 넓게 잡히는 요소 3~6개는 전부 의도된 것이다 —
마퀴 트랙(부모 `overflow:hidden`), 히어로 장식 마크, 푸터 마크.
`opacity:0` 요소 1개는 사이드바 스크림(`pointer-events:none`)이다.

---

## 아직 안 한 것 (플랜 5~10번)

소스가 있으니 이제 가능해진 작업들:

| # | 작업 | 비고 |
|---|---|---|
| ~~5~~ | ~~섹션 리드·링크·출처 슬롯~~ | ✅ 6개 섹션에 배치 |
| ~~6~~ | ~~**증거 밴드** 신설~~ | ✅ 완료 |
| ~~7~~ | ~~**진단 카드 6장**~~ | ✅ 완료 |
| 8 | 기간·예산 밴드 | ⚠️ **구조만 완료. 금액 미정 — 아래 TODO** |
| ~~9~~ | ~~`Why now` 논증 섹션~~ | ✅ 완료 |
| ~~10~~ | ~~FAQ 5 → 7문항~~ | ✅ 완료. 전용 페이지 분리는 미착수 |

---

## ⚠️ TODO — 금액을 채워야 한다

FAQ 3번 "제작 기간과 비용" 에 세 구간짜리 밴드 UI 를 넣었는데,
**금액과 기간은 제가 알 수 없어서 `TODO` 로 비워 뒀습니다.** 5곳입니다.

`pages/Home.html` 에서 `band-todo` 로 검색하면 바로 나옵니다:

```html
<span class="band-d">기간 <span class="band-todo">TODO</span></span>
<span class="band-p"><span class="band-todo">TODO</span></span>
```

빨간 배지로 눈에 띄게 해 뒀으니 **채우기 전에 배포하면 안 됩니다.**
구간 이름(단일 페이지 정비 / 진료과목 분리 + 구조 설계 / 다지점·다국어)은
초안이니 실제 상품 구성에 맞게 고치셔도 됩니다.

이 항목은 Work 페이지의 "런칭 특별가 선착순" 문구와 양립하지 않습니다.
밴드 공개로 가기로 하셨으니 그 문구는 걷어내야 합니다.

---

## 홈 섹션 순서 (v2 최종)

| # | 섹션 | 상태 |
|---|---|---|
| 1 | 히어로 `Creative Clicks.` | 유지 |
| 2 | 마퀴 | 유지 (26s → 40s) |
| 3 | **증거 밴드** `#evidence` | 신설 |
| 4 | 서비스 `#services` | h2 한글화 + 리드 |
| 5 | 사례 `#work` | **진단 카드 6장** + 리드·링크·출처 |
| 6 | 프로세스 `#process` | h2 한글화 + 리드 |
| 7 | **Why now** `#why` | 신설 |
| 8 | 소개 `#about` | h2 한글화 + 1단 전환 |
| 9 | FAQ `#faq` | **5 → 7문항**, 답변 밀도 상향 |
| 10 | 푸터 | h2 한글화 |

## Why now 섹션

238LAB 은 이 자리에 statcounter 점유율 같은 공개 통계를 쓴다.
씨클로는 **자체 실측값**이 있으므로 그걸 쓴다. 남의 숫자보다 강하다.

| # | 주장 | 수치 |
|---|---|---|
| 01 | 아직 아무도 손대지 않았습니다 | **0** — 일곱 곳 중 30점 넘긴 병원 수 |
| 02 | 검색은 벌어졌고 AI는 몰려 있습니다 | **45 : 25** — 검색 분포 폭 대 AI 분포 폭 |
| 03 | 한 항목만 고쳐도 움직입니다 | **32 → 46** — 구조화만 고친 뒤 AI 종합 |

새 컴포넌트를 만들지 않고 기존 `.grid-3` + `.step` 을 재사용했다. `.stat` 줄만 얹었다.

## FAQ 7문항

238LAB FAQ 의 4요소(단정 첫문장 · 실무 근거 · 자사 한계 고백 · 판별 기준)를 적용.
문항당 2~4문단.

1. 씨클로는 어떤 회사인가요?
2. GEO가 무엇인가요?
3. 제작 기간과 비용은 어떻게 되나요? ← **밴드 TODO**
4. **노출 성과를 보장해 주시나요?** (신규 — "아니요"로 시작)
5. **지금 홈페이지를 새로 만들어야 하나요?** (신규 — "대부분은 아닙니다")
6. 병원·법률 등 규정이 까다로운 분야도 가능한가요?
7. 웹사이트만 제작하고 마케팅은 따로 맡길 수 있나요?

4번·5번이 핵심이다. 파는 쪽에 불리한 답을 먼저 하는 것이 238LAB FAQ 의 작동 원리다.

## 헤더·사이드바 접근성

| 결함 | 조치 |
|---|---|
| 닫힌 사이드바의 링크 9개가 탭 순서에 남음 | `visibility:hidden` (닫는 애니메이션은 transition delay 로 유지) |
| `aria-expanded` / `aria-controls` 없음 | 버거에 추가 |
| dialog 시맨틱 없음 | `role="dialog"` `aria-modal="true"` |
| 포커스 트랩·스크롤 잠금·포커스 복원 없음 | 전부 추가 |
| 앵커 점프가 고정 내비에 가림 | `section[id]{scroll-margin-top:96px}` |
| `rel="noopener"` 누락 2곳 | 추가 |
| 사이드바 9개 평면 나열 | `/SERVICES` · `/PAGES` 그룹화 |
| 스킵 링크·포커스 링 없음 | 추가 (어두운 면은 옐로 아웃라인) |

실제 키보드 조작으로 검증: 탭 25회에 숨은 사이드바 도달 안 함 · 열림 시 포커스 자동 이동 ·
탭 30회에도 트랩 유지 · ESC 후 버거로 포커스 복원.


---

## 증거 밴드 (완료)

히어로·마퀴 직후, `#services` 앞에 `<section class="section navy evidence" id="evidence">` 신설.
238LAB 의 "히어로 → 즉시 증거" 문법을 씨클로 데이터로 채운 것이다.

구성 (전부 씨클로 자체 실측값, 지어낸 숫자 없음):

| 요소 | 내용 | 출처 |
|---|---|---|
| 헤드라인 | 81점 → 20점, 낙차 −61 | 10항목 채점 최고/최저 |
| 막대 차트 | 열 항목 평균, 눈금 0/20/40/60/80/100 | `/dental-homepage-10-items-score` |
| 강조 2행 | AI 검색 대응 35 · 기계용 정보 표기 20 (옐로) | 리포트 "붉은 두 항목" |
| 도트플롯 | 7곳 개별 12·15·15·20·20·28·30 + 30점 임계선 | `/seven-clinics-real-scores` |
| 자가 점검 | 소스 보기 → Ctrl+F → `ld+json` | 칼럼 공통 |
| CTA | 리포트 원문 / 우리 병원 점수 받기 | `dental-seo-report.vercel.app` |
| 한계 고지 | 표본 8곳, 순위·매출 예측 아님 | 238LAB FAQ 4요소 중 "한계" |

설계 규칙:
- **옐로는 이 섹션에서 단 한 용도** — AI 노출을 결정하는 두 항목. 버튼에는 쓰지 않았다.
- 눈금을 20 단위로 끊었다. 채점이 체크포인트 5개×20점이라 점수가 그 단위로만 떨어진다.
  25나 10으로 끊으면 데이터에 없는 정밀도를 암시하게 된다.
- 560px 이하에서는 라벨을 막대 위로 올린다. 한 줄에 두면 "기계용 정보 표기" 가 잘리는데,
  하필 그게 이 차트의 결론이라 잘리면 안 된다.

검증 (1440/768/390): 막대 폭이 값과 ±1% 이내 일치, 도트 7개 위치 정확,
라벨 잘림 0, CLS 0, 가로 오버플로 0, JS 에러 0.


---

## 서브페이지 5개 (완료)

### 서비스 4개 — Website Design · GEO · Blog Content · Digital Marketing

네 페이지가 동일 골격이라 같은 변환을 적용했다.

**발견한 문제**
- `/WHAT'S INCLUDED` 섹션에 **h2 가 아예 없었다.** 눈썹 다음 바로 카드 6장이라
  섹션이 무슨 주장을 하는지 문장으로 나오지 않았다.
- 나머지 h2 는 `진행 순서` / `이런 분께 필요합니다` — 명사구지 문장이 아니다.
- **인라인 `style="font-size:clamp(30px,4vw,52px)"` 가 8곳**에 박혀 있었다.
  홈 ABOUT h2 에서 잡았던 것과 같은 문제로, CSS 를 이겨서 v2 스케일이 안 먹는다.

**적용한 h2** (전부 238LAB 공식: `[수식구] + , + [동사구 ~합니다]` 2줄)

| 페이지 | WHAT'S INCLUDED | HOW IT WORKS | FOR YOU |
|---|---|---|---|
| Website Design | 기획부터 유지보수까지,<br>여섯 가지를 한 번에 맡습니다 | 네 단계로 진행하고,<br>단계마다 확인받습니다 | 이런 상태라면,<br>지금이 고칠 때입니다 |
| GEO | AI가 읽을 수 있게,<br>비어 있는 여섯 자리를 채웁니다 | 진단부터 모니터링까지,<br>네 단계로 갑니다 | 검색은 되는데 AI 답변에<br>안 나온다면 이 작업입니다 |
| Blog Content | 쓰는 일부터 발행까지,<br>여섯 가지를 대행합니다 | 키워드부터 리포트까지,<br>네 단계로 돌립니다 | 쓸 말은 있는데<br>쓸 시간이 없다면 |
| Digital Marketing | 광고비를 늘리기 전에,<br>여섯 가지를 먼저 봅니다 | 설계부터 리포트까지,<br>네 단계로 운영합니다 | 클릭은 나오는데<br>문의가 안 온다면 |

GEO 페이지 리드에는 자체 실측값을 넣었다 — "기계용 정보 표기 평균 20점, 30점을 넘긴 곳은 없었습니다."

### Work — 전면 재작성

기존 상태: `프로젝트 이미지 준비 중` 빈 슬롯 **6칸**, 히어로 리드는
"프로젝트 이미지는 준비되는 대로 업데이트됩니다."
**실적이 없다는 사실을 6칸으로 광고하고 있었다.**

바꾼 방향은 홈과 같다. 없는 사례를 기다리지 말고, 실제로 한 일을 공개한다.

| 섹션 | 내용 |
|---|---|
| 히어로 | "아직 공개할 수 있는 클라이언트 작업이 많지 않습니다. 대신 저희가 직접 한 일을 먼저 공개합니다." |
| `/RESULT` | **여덟 곳 전체 표** — A–H, 유형·검색·AI 답변·격차·구조화·사이트 구조 + 중앙값 |
| `/METHOD` | 채점 방법 3장 — 열 항목 쉰 개 / 있다·없다로만 / 공개된 소스만 |
| `/LIMITS` | 한계 4가지 — 표본 8곳, 순위 예측 아님, 디자인 평가 아님, 20곳 넘으면 갱신 |

표에서 **구조화 데이터 열만 배경 톤으로 묶었다.** 색을 새로 들이지 않고 요점을 표시하는 방법이다.
7열이라 좁은 화면에서는 가로 스크롤하고, 스크롤 힌트를 700px 이하에서만 띄운다.

### 검증 (6개 페이지 × 1440 / 390)

| 항목 | 결과 |
|---|---|
| h2 크기 | 전 페이지 **40px / 26px 통일** |
| 인라인 font-size | **0건** (8건 제거) |
| h2 줄 수 | 최대 2줄 (모바일 3줄) |
| 칩 라운드 | 4px |
| Work 표 | 1440 넘침 없음 · 390 가로 스크롤 |
| 가로 오버플로 | 0 |
| CLS | 0 |
| 깨진 이미지 | 0 |
| JS 에러 | 0 |
