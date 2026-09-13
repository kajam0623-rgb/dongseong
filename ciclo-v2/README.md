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
| 5 | 섹션마다 `.sec-lead` · `.sec-link` · `.sec-caption` 채우기 | CSS 슬롯은 이미 만들어 둠 |
| 6 | **증거 밴드** 신설 (치과 8곳 채점 데이터) | 히어로 직후 |
| 7 | **진단 카드 6장** (A~H 익명) | 현재 목업 1장 대체 |
| 8 | 기간·예산 밴드 공개 + 주차 타임라인 | Work 의 "런칭 특별가 선착순" 과 택일 |
| 9 | `Why now` 논증 섹션 | 출처 캡션 포함 |
| 10 | FAQ 5 → 7문항 + 전용 페이지 분리 | |

7번은 4번(사례 h2 "여덟 곳을 채점했다")과 짝이라 먼저 하는 게 맞다.
지금은 제목만 바뀌고 내용은 목업이라 어긋나 있다.
