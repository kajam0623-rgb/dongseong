# 사이트온 (SiteOn) — 한국형 병원 웹사이트 빌더

노코드 웹사이트 빌더 SaaS MVP. 통합 런처를 실행하면 빌드, 로컬 서버, AI CLI 브리지를 준비하고 Chrome에서 빌더를 엽니다.

- 디자인 스타일 13종 × 컬러 테마 10종 + 커스텀 컬러
- 실시간 미리보기 (PC/태블릿/모바일), 모션 프리셋 4종
- 사진 업로드(히어로/진료과목/의료진/시설 갤러리, base64 내장), 유튜브 임베드
- 오시는길 지도 자동 임베드, 네이버 예약 연동, 플로팅 퀵바
- SEO 메타/OG/JSON-LD, 모바일 햄버거 메뉴, 라이트박스, 접근성(reduced-motion)
- 의료법 준수 (치료후기·전후사진 없음)
- 통합 런처 기준 `projects/` 폴더 저장 + IndexedDB 백업 + JSON 프로젝트 파일, 독립 HTML 내보내기

## 바로 실행

Windows에서 `Start-SiteOn.cmd`를 더블클릭하거나 아래 명령을 실행합니다.

```powershell
.\Start-SiteOn.ps1
```

실행하면 다음 작업을 한 번에 처리합니다.

- `src/` 소스를 `사이트온-빌더.html`로 빌드
- 로컬 웹 서버 실행
- AI CLI 브리지 실행
- Chrome에서 빌더 열기

직접 파일만 열어도 기본 편집은 가능하지만, 로컬 폴더 저장과 AI CLI 연동까지 쓰려면 통합 런처를 권장합니다.

## 프로젝트 저장

통합 런처(`Start-SiteOn.cmd` 또는 `.\Start-SiteOn.ps1`)로 Chrome을 열면 빌더가 로컬 서버의 저장 API를 사용합니다. 프로젝트 화면에서 새 사이트를 만들거나 `프로젝트 보관함`의 저장 버튼을 누르면 아래 위치에 파일이 남습니다.

```text
projects/{프로젝트-이름}/project.siteon.json
projects/{프로젝트-이름}/project.json
```

- `project.siteon.json`: 보관함 복원용 전체 기록
- `project.json`: 사람이 확인하기 쉬운 프로젝트 데이터
- 같은 내용은 브라우저 IndexedDB에도 백업됩니다.
- `사이트온-빌더.html`을 직접 파일로 열면 서버가 없으므로 기존처럼 브라우저 IndexedDB와 JSON 다운로드 저장만 사용합니다.

## 소스 구조와 빌드

실행 파일은 계속 `사이트온-빌더.html` 하나입니다. 코드 수정은 `src/`에서 하고, 아래 명령으로 단일 HTML을 다시 생성합니다.

```powershell
node tools/build-builder.mjs
```

- `src/builder-shell.html`: 빌더 HTML 셸
- `src/styles/builder.css`: 빌더 UI CSS
- `src/js/builder.js`: 빌더 핵심 JS
- `src/js/generators/`: 큰 테마 제너레이터 분리 위치

## AI CLI 브리지

빌더의 `AI 작업` 패널에서 `AI CLI로 수정`을 누르면 브라우저가 로컬 브리지(`http://127.0.0.1:4627`)로 요청하고, 브리지가 `codex exec`를 호출합니다.

```powershell
node tools/siteon-ai-cli-bridge.mjs
```

기본값은 PATH의 `codex`를 자동 사용합니다. 다른 CLI를 쓰려면 `SITEON_AI_CLI`, `SITEON_AI_ARGS`, `SITEON_AI_PORT` 환경변수로 덮어쓸 수 있습니다.

## AI 에이전트로 이어서 작업하기

- **Claude Code**: 이 폴더에서 `claude` 실행 → `CLAUDE.md`를 자동으로 읽습니다
- **Codex**: 이 폴더에서 실행 → `AGENTS.md`를 자동으로 읽습니다

아키텍처/규칙/로드맵은 CLAUDE.md(=AGENTS.md) 참고.

로드맵 1번(레퍼런스 이식)은 `REFERENCE_PIPELINE.md`를 먼저 읽고 진행하세요. 현재 완료된 표본은 `references/photo-editorial.md`에 정리되어 있습니다.

## 검증

`tests/golden.html`을 브라우저에서 열면 골든 테스트가 실행됩니다. 빌더를 로드한 뒤 13개 스타일 전체에 대해 `generateSite(getConfig())`를 실행하고, 필수 섹션 id, 문서 경계, 이모지 누출, 미리보기 렌더, 콘솔 에러를 확인합니다.
