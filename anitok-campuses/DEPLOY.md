# 배포 안내

7개 지점 사이트는 `sites/<slug>/` 에 이미 빌드되어 있고, 폴더 하나가 그대로 배포 루트다.
방법은 두 가지다. **A가 더 빠르고, 저장소를 새로 만들 필요가 없다.**

---

## A. 지금 있는 저장소 하나로 7개 사이트 배포 (권장, 새 저장소 불필요)

Vercel은 프로젝트마다 **Root Directory**를 따로 지정할 수 있다. 저장소는 `kajam0623-rgb/dongseong`
하나를 쓰고, 프로젝트만 7개 만들면 지점별로 도메인이 갈린다.

각 지점마다 한 번씩 반복한다.

1. [vercel.com/new](https://vercel.com/new) → `kajam0623-rgb/dongseong` **Import**
2. **Project Name**: `mokdong-anitok` (그대로 `mokdong-anitok.vercel.app` 이 된다)
3. **Root Directory**: `Edit` 를 눌러 `anitok-campuses/sites/mokdong` 선택
4. **Framework Preset**: `Other`, Build Command 비움, Output Directory 기본값
5. **Branch**: `claude/ilsan-anitok-project-arpdi5`
   (main에 머지한 뒤에는 main으로 바꿔도 된다)
6. Deploy

| 프로젝트 이름 | Root Directory |
|---|---|
| `mokdong-anitok` | `anitok-campuses/sites/mokdong` |
| `hongdae-anitok` | `anitok-campuses/sites/hongdae` |
| `gangdong-anitok` | `anitok-campuses/sites/gangdong` |
| `bucheon-anitok` | `anitok-campuses/sites/bucheon` |
| `gwanggyo-anitok` | `anitok-campuses/sites/gwanggyo` |
| `gimpo-anitok` | `anitok-campuses/sites/gimpo` |
| `academy-anitok` | `anitok-campuses/sites/academy` |

Vercel CLI가 편하면 저장소를 로컬에 받은 뒤 한 줄씩:

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

## 배포 후

1. **사진 교체** — 각 사이트의 `PHOTOS.md` 에 어떤 파일명으로 무슨 사진이 들어가야 하는지
   표로 정리해 두었다. `gal/` 에 넣고 `node build.mjs <slug>` 재실행 후 다시 푸시.
2. **GA4** — `data/<slug>.json` 의 `analytics.ga4` 에 측정 ID를 넣으면 헤드에 태그가 붙는다.
3. **좌표** — `geo.lat` / `geo.lng` 를 채우면 geo 메타와 JSON-LD 좌표가 붙는다. 로컬 SEO에 도움이 된다.
4. **네이버 사이트 인증** — 도메인별로 발급받아 `seo.verification` 에 추가한다.
5. **서치콘솔 / 네이버 서치어드바이저** — 각 도메인의 `sitemap.xml` 을 제출한다.
6. **anitok.com 캠퍼스 안내 페이지**에서 각 지점 카드에 새 랜딩페이지 링크를 걸면
   내부 링크가 생겨 색인에 유리하다.
