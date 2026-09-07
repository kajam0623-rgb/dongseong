# 배포 안내

7개 지점 사이트는 `sites/<slug>/` 에 이미 빌드되어 있고, 폴더 하나가 그대로 배포 루트다.
**지금 필요한 것은 A 하나뿐이다.** 프로젝트와 도메인은 이미 있고, Git 연결만 빠져 있다.
B 는 지점마다 저장소를 따로 두고 싶을 때의 대안이라 지금은 볼 필요 없다.

---

## A. 이미 있는 7개 프로젝트에 Git 연결하기 (지금 해야 할 것)

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
| `academy-anitok` | `anitok-campuses/sites/academy` | `academy-anitok.vercel.app` |

> **Production Branch 를 `main` 으로 두면 안 된다**
> Vercel 은 기본값으로 저장소의 기본 브랜치(`main`)를 프로덕션으로 잡는다. 그런데 지금
> `origin/main` 에는 구조화 데이터 개선 커밋이 아직 없다. `main` 으로 연결하면 7개 사이트가
> 전부 예전 JSON-LD 로 되돌아간다.
> 두 가지 중 하나를 택한다.
> - Production Branch 를 `claude/ilsan-anitok-project-arpdi5` 로 지정한다 (머지 불필요)
> - 먼저 그 브랜치를 `main` 에 머지한 뒤 `main` 으로 연결한다

> **연결하면 지역 랜딩페이지 42개가 같이 공개된다**
> 지금 라이브에는 지점마다 `index.html` 과 `404.html` 두 장만 올라가 있다. 저장소에는
> 지점마다 지역 랜딩페이지 6장이 더 들어 있고(예: 김포는 `gimpo-webtoon`, `hangang-manhwa` 등),
> `sitemap.xml` 도 7개 URL 을 담고 있다. Git 을 연결하면 이것들이 그대로 배포된다.
> 랜딩페이지에는 BreadcrumbList 와 FAQPage 구조화 데이터가 들어 있어 본문 분량이 얇다는
> 문제(지점 330~460자 vs 일산 4,661자)가 같이 해소된다. 원치 않으면 연결 전에 알려달라.

> **왜 대신 눌러주지 못하나**
> 이 세션의 Vercel 토큰은 배포 전용이다. `list_teams` 는 빈 배열을 주고
> `list_projects` · `get_project` 는 `403 Forbidden` 이라, 기존 프로젝트의 Git 설정을
> 읽거나 바꿀 방법이 없다. MCP 의 `create_git_project` 도 "이미 있는 미연결 프로젝트를
> 다시 연결하지는 않는다"고 명시돼 있어 쓸 수 없다. 브라우저에서 직접 눌러야 한다.

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
