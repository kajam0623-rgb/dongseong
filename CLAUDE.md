# 사이트온 (SiteOn) — 한국형 병원 웹사이트 빌더

> **영역 분담 (코덱스와 합의 — AGENTS.md와 동일)**: 클로드 담당 = 디자인 폴리시 · 모바일 점검 · 온보딩 위저드 · 대비 가드 · 사이드바 UX. 코덱스 담당 = 테스트 인프라 · ZIP/Pages 내보내기 · IndexedDB · 저장 표시 · 푸터 법정정보. 담당 외 영역 수정 금지, 발견한 문제는 ISSUES.md에 기록. 작업 전 git pull 필수.

> **필독 순서**: `설계서-v4.md`(듀얼 모드: 원페이지↔멀티페이지, 컬렉션 스키마) → `설계서-v3.md`(토큰·컴포저·배포·WP). 충돌 시 v4 우선. `설계서-v3.md`가 이 문서의 상위 참조다. 토큰 3계층, 섹션 컴포저 전환, 모션 토큰, 배포(SaaS), 워드프레스 연동의 모든 구현은 설계서의 스키마와 스프린트 순서(S1~S7)를 따른다. S1 골든 테스트 없이 섹션 컴포저 전환에 착수하지 말 것.

노코드 웹사이트 빌더 SaaS의 MVP 프로토타입. 사용자가 병원 정보를 입력하면 전문 디자이너급 원페이지 사이트를 실시간 미리보기로 만들고, 독립 실행 가능한 단일 HTML로 내보낸다. 최종 목표는 한국 로컬 비즈니스(1차: 치과/병원) 대상 월구독 SaaS.

## 실행 방법

빌드 과정 없음. `사이트온-빌더.html`을 브라우저(Chrome 권장)에서 열면 끝.
- 편집 → 우측 iframe 실시간 미리보기 (srcdoc)
- 검증: "새 탭 미리보기" 버튼 또는 "HTML 내보내기"로 실제 산출물 확인

## 아키텍처 (단일 HTML 파일, ~3,000줄)

```
사이트온-빌더.html
├─ <style>            빌더 UI (다크 에디터 크롬)
├─ <body>             상단바 / 좌측 사이드바(편집 패널) / 미리보기 iframe
└─ <script>
   ├─ THEMES[10]      컬러 테마 (primary/deep/ink/soft/grad 파생값 포함)
   ├─ STYLES[6]       디자인 스타일 메타
   ├─ state           편집 상태 (단일 진실 공급원)
   ├─ UI 와이어링      테마/스타일/모션 셀렉터, 리스트 에디터, 이미지 업로드(pickImage→canvas 압축→base64)
   ├─ 저장/복원        localStorage 자동저장 + JSON 프로젝트 파일 내보내기/가져오기
   ├─ getConfig()     state → cfg. ★모든 텍스트는 여기서 esc() 이스케이프됨
   ├─ 공유 헬퍼        headMeta(SEO/OG/JSON-LD) · mobileNav(햄버거) · prodExtras(라이트박스)
   │                  PROD_CSS(모바일메뉴/라이트박스/접근성) · quickBar(플로팅 퀵바)
   │                  mapEmbed(구글지도 임베드) · naverBtn(네이버예약) · siteScript(공통 JS) · siteCommon
   ├─ generateSite(cfg) → 스타일 디스패처
   │   ├─ genSoft      소프트 모던 (밝은 톤, 카드)
   │   ├─ genClassic   클래식 신뢰형 (대학병원 문법: 유틸바+퀵메뉴 바)
   │   ├─ genPremium   프리미엄 다크 (강남 심미 문법: 세리프, 1px 라인)
   │   ├─ genSplit     모던 스플릿 (에이전시 문법: 좌우 분할, 리스트형)
   │   ├─ genPop       프렌들리 팝 (가족·소아: 파스텔, 오가닉 블롭)
   │   └─ genPhoto     포토 에디토리얼 ★레퍼런스 실측 기반 (아래 참고)
   ├─ 인라인 편집 레이어  attachEditLayer: 미리보기 iframe DOM에 직접 부착(엘리멘터식).
   │                  텍스트는 normTxt 값 매칭으로 contenteditable 태깅(buildTextRegistry),
   │                  사진은 섹션 내 n번째 아이템 ↔ state 배열 n번째 매핑(zone 함수).
   │                  내보내기/새탭에는 미부착(라이브 미리보기 전용). renderKeepScroll로 스크롤 보존
   ├─ 디자인 토큰        state.tokens(텍스트색+불투명도/그림자/밀도/라운드) → userCss()가 !important 오버라이드 생성
   ├─ 블록 라이브러리    state.blocks[] (pricing/transport/badges/event) → blocksHtml() 인라인 스타일 렌더
   ├─ 섹션 재배치/변형   state.sectionOrder + state.variants. generateSite = postProcess(generateSiteRaw())
   │                  postProcess: DOMParser로 #about~#location 직계 자식 재배열 + 의료진 list 변형 시 #doctors 교체
   ├─ 사진 보정          pickImage → openPhotoEditor(모달: 프리셋6/밝기·대비·채도/크롭5비율) → canvas 필터 적용
   ├─ 실행취소           histStack(60), render()마다 histPush, Ctrl+Z/Shift+Z, ↶↷ 버튼
   └─ 초기화 (자동저장 복원 → draw* → render)
```

스타일은 12종이다(soft/classic/premium/split/pop/photo/luxe/process/magazine/curve/bold/showcase). 신규 6종(luxe~showcase)은 X_BASE_CSS+stdTail+stdNav 공유 베이스 위에 히어로·진료과목·CSS 오버라이드로 차별화한다.

각 제너레이터는 **완전한 독립 HTML 문자열**을 반환한다(내장 CSS/JS, base64 이미지 포함). 미리보기와 내보내기가 동일한 함수를 쓴다.

## 디자인 시스템 규칙 (사용자가 강하게 요구한 것 — 반드시 유지)

**금지 (AI 클리셰):** 알약(pill) 배지, 그라데이션 버튼/텍스트, 형광펜 밑줄 강조, 플로팅 통계 카드 + 이모지 아이콘 조합, 과한 바운스 이징, 라운드 20px 초과 남발 (프렌들리 팝 스타일만 예외적으로 큰 라운드 허용)

**타이포:** 제목 자간 -0.035em(포토 스타일은 normal)·행간 1.2 내외 / 본문 행간 1.7~1.8 / 레이블 자간 +0.1~0.16em / 전 문단 `word-break:keep-all`

**여백:** 섹션 패딩 `clamp(90px,11vw,150px)` 이상 (포토 스타일은 210px까지). 라운드는 6px(버튼)/12~14px(카드) 2단계.

**레퍼런스 실측값 (genPhoto의 근거, 사용자 제공 사이트 분석):**
- brighteyesclinic.com: 제목 60px/600/행간1.3/자간normal, 본문 18px/400/1.7, 풀블리드 단색 블록, 라운드 0~5px
- doodoorim-clinic.com: 풀스크린 실사진 히어로, 50:50 사진:패널 교차, "진료철학 02"식 번호 레이블, 인라인 빠른상담 바, 사이드 QUICK 탭

상세 실측 기록은 `references/photo-editorial.md`에 있다. 로드맵 1번을 이어갈 때는 `REFERENCE_PIPELINE.md`를 먼저 읽고, 새 URL을 같은 형식으로 실측한 뒤 신규 `gen*` 스타일을 추가한다.

## 의료법 준수 (절대 어기지 말 것)

- **환자 치료후기/경험담 섹션 금지** (의료법 제56조) — 이미 전부 제거됨. 다시 추가하지 말 것
- **치료 전후 비교사진 금지** — 갤러리는 "시설·장비" 용도로만
- 효과 보장 문구("100% 성공" 등) 카피로 생성 금지

## 작업 규칙

1. 사용자 텍스트 입력은 반드시 `getConfig()`의 `esc()`를 거친다. 제너레이터에 raw 값 직접 사용 금지 (예외: `addrRaw`는 지도 URL용, `heroImg` 등 base64는 비이스케이프)
2. 새 스타일 추가 시 체크리스트: STYLES 항목 + STYLE_ICONS SVG + 디스패처 분기 + **전 섹션 패리티**(services/stats/doctors/gallery/video/booking/location) + `${headMeta(cfg)}` + `${mobileNav(cfg)}` + `${quickBar(cfg)}` + `${prodExtras(cfg)}` + `${siteScript(cfg)}` + `:root{--nav-fg;--mnav-bg;--mnav-accent}` + `${PROD_CSS}` + 모든 `[data-reveal]` 모션 4종(soft/dynamic/minimal/none) 대응
3. 빌더 스크립트는 HTML `<script>` 안이므로 문자열 내 닫는 스크립트 태그는 `<\/script>`로 이스케이프
4. `const` 선언(renderSoon 등)을 선언 전에 값으로 참조하면 TDZ 에러로 초기화 전체가 죽는다. 핸들러는 `()=>renderSoon()` 형태로
5. 검증: 브라우저에서 12개 스타일 전부 `generateSite(getConfig())` 호출이 `<!DOCTYPE`로 시작, `</html>`로 끝나는지 + 콘솔 에러 0건
6. 이모지 사용 금지(사용자 요구). 아이콘은 번호(01~) 또는 stroke SVG만. 유일한 허용 글리프는 ✚(의료 십자)
7. 인라인 편집 레지스트리: 텍스트 필드를 새로 추가하면 `buildTextRegistry`에도 등록해야 미리보기에서 클릭 편집된다. 사진 영역을 새 스타일에 추가하면 `attachEditLayer`의 zone 셀렉터 목록에 아이템 클래스를 추가할 것

## 로드맵 (다음 작업 우선순위)

1. **레퍼런스 이식 파이프라인 반복** — 사용자가 URL 주면: `REFERENCE_PIPELINE.md` 절차대로 실측(타이포/여백/컬러/구조) → 신규 gen* 작성. genPhoto가 표본
2. **업종 확장** — 카페/포