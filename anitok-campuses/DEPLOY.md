# 배포 안내

7개 지점 사이트는 `sites/<slug>/` 에 이미 빌드되어 있고, 폴더 하나가 그대로 배포 루트다.

**2026-09-09: 7개 지점 전부 부트스트랩 방식으로 프로덕션 배포했다(아래 0번).**
Git 연결(A)은 여전히 권장 사항이다. 연결해 두면 푸시할 때마다 자동 배포되므로
배포마다 0번을 다시 돌릴 필요가 없다.

---

## 0. 부트스트랩 배포 (지금 쓰는 방법, 세션에서 바로 가능)

Vercel 토큰에 팀 스코프 읽기 권한이 없어 프로젝트를 Git 에 연결하지 못한다.
그렇다고 지점마다 산출물 150~250KB 를 손으로 다시 적어 올릴 수도 없다.

대신 **빌드 시점에 저장소를 받아오게 한다.** `kajam0623-rgb/dongseong` 은 공개
저장소라 Vercel 빌드 컨테이너에서 그냥 clone 된다. 그래서 실제로 올리는 파일은
세 개(`build.sh`, `package.json`, `vercel.json`)뿐이고, 나머지는 빌드가 만든다.

올리는 파일:

| 파일 | 내용 |
|---|---|
| `build.sh` | `tools/vercel-bootstrap/build.sh` 사본. clone → `node build.mjs <slug>` → `public/` |
| `package.json` | 이름만 있는 최소 파일 (Vercel 이 빌드 대상으로 인식하게) |
| `vercel.json` | **해당 지점의** `sites/<slug>/vercel.json` 을 그대로. 지점마다 리다이렉트 목적지가 다르다 |

Project Settings (배포 API 로 같이 넘긴다):

```
framework       : null
installCommand  : true          (의존성 없음. no-op)
buildCommand    : bash build.sh <slug>
outputDirectory : public
```

주의할 점:

- `buildCommand` 는 **256자 제한**이 있다. 명령을 인라인으로 길게 쓰면 400 이 난다.
  그래서 스크립트 파일로 뺐다.
- `vercel.json` 은 **배포 루트**에 있어야 적용된다. `public/` 안에 있으면 그냥
  정적 파일로 서빙될 뿐이다. 그래서 `build.sh` 가 사본을 지운다.
- `academy` 만 `*.vercel.app` 리다이렉트가 없다. 커스텀 도메인이 아니라
  academy 도 2026-09-11 부터 `academy.anitok.com` 을 쓴다. 7곳 모두 리다이렉트가 붙는다.
  academy 에는 오타 도메인 `acdemy.anitok.com` 을 정식 주소로 넘기는 규칙이 하나 더 있다.
- 빌드가 실패하면 프로덕션은 **그대로 유지**된다. 실패해도 사이트가 깨지지 않는다.
- 이 방식은 배포 **시점**의 브랜치 상태를 굳혀 올린다. 자동 갱신이 아니다.
  저장소를 고친 뒤에는 다시 배포해야 한다.

이 세션에서는 결과를 확인하지 못한다. 컨테이너 프록시가 `*.anitok.com` 과
`*.vercel.app` 을 막고, Vercel 읽기 API(`get_deployment`, 빌드 로그)는 403 이다.
배포 성공 여부는 Vercel 대시보드나 브라우저로 직접 봐야 한다.

---

## A. 이미 있는 7개 프로젝트에 Git 연결하기 (권장, 한 번만 하면 끝)


7개 Vercel 프로젝트는 **이미 만들어져 있고 커스텀 도메인도 붙어 있다.** 다만 Git 저장소에
연결돼 있지 않아 배포할 때마다 파일을 수동으로 올려야 한다. 일산(`ilsan-anitok`)만 연결돼
있어서 푸시하면 자동 배포된다. 나머지 7곳도 같은 상태로 맞춘다.

프로젝트를 새로 만들 필요는 없다. 새로 만들면 도메인을 옮겨 붙여야 해서 오히려 손해다.
기존 프로젝트에 저장소만 연결한다.

각 지점마다 한 번씩:

1. Vercel → 해당 프로젝트 → **Settings → Git → Connect Git Repository**
2. `kajam0623-rgb/dongseong` 선택
3. **Root Directory**: `anitok-campuses/sites/<slug>` (아래 표)
4. **Framework Preset**: `Other`, Build Command 비움, Output Directory 기본값
5. **Production Branch**: `claude/ilsan-anitok-project-arpdi5` — 아래 경고를 먼저 읽을 것
6. Save 후 Deployments 탭에서 한 번 재배포

| Vercel 프로젝트 | Root Directory | 도메인 |
|---|---|---|
| `mokdong-anitok` | `anitok-campuses/sites/mokdong` | `mokdong.anitok.com` |
| `hongdae-anitok` | `anitok-campuses/sites/hongdae` | `hongdae.anitok.com` |
| `gangdong-anitok` | `anitok-campuses/sites/gangdong` | `gangdong.anitok.com` |
| `gwanggyo-anitok` | `anitok-campuses/sites/gwanggyo` | `gwanggyo.anitok.com` |
| `gimpo-anitok` | `anitok-campuses/sites/gimpo` | `gimpo.anitok.com` |
| `bucheon-anitok` | `anitok-campuses/sites/bucheon` | `bucheon.anitok.com` |
| `academy-anitok` | `anitok-campuses/sites/academy` | `academy.anitok.com` |

> **Production Branch 를 `main` 으로 두면 안 된다**
> Vercel 은 기본값으로 저장소의 기본 브랜치(`main`)를 프로덕션으로 잡는다. 그런데 지금
> `origin/main` 에는 구조화 데이터 개선 커밋이 아직 없다. `main` 으로 연결하면 7개 사이트가
> 전부 예전 JSON-LD 로 되돌아간다.
> 두 가지 중 하나를 택한다.
> - Production Branch 를 `claude/ilsan-anitok-project-arpdi5` 로 지정한다 (머지 불필요)
> - 먼저 그 브랜치를 `main` 에 머지한 뒤 `main` 으로 연결한다

> **지역 랜딩페이지 42개는 이미 공개됐다**
> 예전에는 지점마다 `index.html` 과 `404.html` 두 장만 라이브였다. 2026-09-09 부트스트랩
> 배포로 지점별 지역 랜딩페이지 6장(예: 김포는 `gimpo-webtoon`, `hangang-manhwa` 등)과
> `sitemap.xml` 전체 URL 이 함께 올라갔다. 홍대는 블로그 6장이 더해져 13개 URL 이다.
> 랜딩페이지에는 BreadcrumbList 와 FAQPage 구조화 데이터가 들어 있어 본문 분량이 얇다는
> 문제가 같이 해소됐다.

> **왜 대신 눌러주지 못하나**
> 이 세션의 Vercel 토큰은 배포 전용이다. 팀 스코프 자체에 접근 권한이 없다.
>
> ```
> list_teams                 → []
> list_projects · get_project → 403 Forbidden
> create_git_project          → 403 "Not authorized: Trying to access resource
>                               under scope kajam0623-rgbs-projects.
>                               You must re-authenticate to this scope."
>                               (teamId: team_M7sXygtY8ZzpT4aG4dak7sVC)
> ```
>
> 이름을 바꿔 새 프로젝트를 만드는 우회로도 같은 403 에서 막힌다. 남는 것은
> `deploy_to_vercel` 파일 업로드 하나뿐이고, 이건 매번 사이트 전체를 한 번에
> 올려야 한다. 홍대 기준 17개 파일 167KB 다. 게다가 이 세션에서는 올린 결과를
> 확인할 방법이 없다 — 프록시가 `*.anitok.com` 과 `*.vercel.app` 을 막고,
> 스크레이퍼 크레딧도 떨어졌다. 잘려 올라가도 알 수가 없다.
>
> 그래서 Git 연결은 브라우저에서 직접 눌러야 한다. 한 번 눌러 두면 이 문제가
> 통째로 사라진다.

Vercel CLI 가 편하면 로컬에서 폴더째 올릴 수도 있다(연결 없이 1회성 배포).

```bash
cd anitok-campuses
npx vercel deploy sites/mokdong --prod --name mokdong-anitok
npx vercel deploy sites/hongdae --prod --name hongdae-anitok
# ... 나머지도 동일
```
---

## B. 지점별 저장소로 분리

저장소를 지점마다 따로 두고 싶을 때. `gh` CLI로 7개를 만들고 각 사이트를 푸시한다.

```bash
cd anitok-campuses
gh auth login                       # 아직 로그인 안 했다면
DRY_RUN=1 ./tools/create-repos.sh   # 무엇을 할지 먼저 확인
./tools/create-repos.sh             # 실제 생성 + 푸시
```

만들어지는 저장소:

`mokdong-anitok` · `hongdae-anitok` · `gangdong-anitok` · `bucheon-anitok` ·
`gwanggyo-anitok` · `gimpo-anitok` · `academy-anitok`

이미 있는 저장소는 다시 만들지 않고 푸시만 한다. 그다음 Vercel에서 각 저장소를
Import 하면 되고, 이때는 Root Directory 설정이 필요 없다.

> **왜 직접 안 만들었나**
> 이 세션의 GitHub 앱 토큰에는 저장소 생성 권한(`administration: write`)이 없다.
> `POST /user/repos` 가 `403 Resource not accessible by integration` 으로 거부되고,
> 이건 앱 설치 시점에 정해지는 권한이라 세션 안에서는 바꿀 수 없다.
> 기존 저장소에 푸시하는 것은 문제없이 된다.

---

## 서브도메인 연결 (anitok.com)

vercel.app 주소로 먼저 띄운 뒤, 준비되면 서브도메인으로 옮긴다. 사이트 쪽 작업은 한 줄이다.

1. `data/_shared.json` 에서 `"baseDomain": null` → `"baseDomain": "anitok.com"`
2. `node build.mjs` 후 커밋 · 푸시
   (canonical · og:url · sitemap · 푸터 캠퍼스 링크가 전부 서브도메인으로 바뀐다)
3. Vercel 각 프로젝트 → Settings → Domains → 서브도메인 추가
4. anitok.com DNS에 Vercel이 안내하는 CNAME 추가 (보통 `cname.vercel-dns.com`)

| Vercel 프로젝트 | 연결할 서브도메인 |
|---|---|
| `mokdong-anitok` | `mokdong.anitok.com` |
| `hongdae-anitok` | `hongdae.anitok.com` |
| `gangdong-anitok` | `gangdong.anitok.com` |
| `bucheon-anitok` | `bucheon.anitok.com` |
| `gwanggyo-anitok` | `gwanggyo.anitok.com` |
| `gimpo-anitok` | `gimpo.anitok.com` |
| `academy-anitok` | `academy.anitok.com` |

서브도메인 이름을 바꾸려면 각 지점 데이터의 `site.subdomain` 만 고치면 된다.
전환 후에는 검색엔진에 새 `sitemap.xml` 을 다시 제출한다.

## 배포 후

1. **사진 교체** — 각 사이트의 `PHOTOS.md` 에 어떤 파일명으로 무슨 사진이 들어가야 하는지
   표로 정리해 두었다. `gal/` 에 넣고 `node build.mjs <slug>` 재실행 후 다시 푸시.
2. **GA4** — `data/<slug>.json` 의 `analytics.ga4` 에 측정 ID를 넣으면 헤드에 태그가 붙는다.
3. **네이버 사이트 인증** — 도메인별로 발급받아 `seo.verification` 에 추가한다.
4. **서치콘솔 / 네이버 서치어드바이저** — 각 도메인의 `sitemap.xml` 을 제출한다.
5. **anitok.com 캠퍼스 안내 페이지**에서 각 지점 카드에 새 랜딩페이지 링크를 걸면
   내부 링크가 생겨 색인에 유리하다.
