# 애니톡 캠퍼스 랜딩페이지

`ilsan-anitok.vercel.app`(일산 캠퍼스)과 같은 형태의 정적 랜딩페이지를 나머지 7개 직영 캠퍼스에 맞춰 생성한다.

| 지점 | slug | 저장소(제안) | 배포 주소(제안) | 전화 |
|---|---|---|---|---|
| 애니톡 목동 본원 | `mokdong` | `mokdong-anitok` | mokdong-anitok.vercel.app | 02-2644-3313 |
| 홍대 애니톡 만화애니학원 | `hongdae` | `hongdae-anitok` | hongdae-anitok.vercel.app | 02-3143-3313 |
| 강동 애니톡 만화애니학원 | `gangdong` | `gangdong-anitok` | gangdong-anitok.vercel.app | 02-486-2220 |
| 부천 애니톡 만화애니학원 | `bucheon` | `bucheon-anitok` | bucheon-anitok.vercel.app | 032-329-8685 |
| 광교 애니톡 만화애니학원 | `gwanggyo` | `gwanggyo-anitok` | gwanggyo-anitok.vercel.app | 031-211-0904 |
| 김포 애니톡 만화애니학원 | `gimpo` | `gimpo-anitok` | gimpo-anitok.vercel.app | 031-985-5382 |
| 애니톡 웹툰게임 아카데미 | `academy` | `academy-anitok` | academy-anitok.vercel.app | 02-2695-9514 |

일산은 이미 `kajam0623-rgb/ilsan-anitok` 에 있으므로 여기서 다시 만들지 않는다.

## 빌드

빌드 도구도 의존성도 없다. Node 18 이상이면 된다.

```bash
node build.mjs              # 7개 지점 전부
node build.mjs mokdong      # 특정 지점만
```

`data/<slug>.json` → `sites/<slug>/` 로 굽는다. 결과 폴더에는 다음이 들어간다.

```
sites/mokdong/
├─ index.html      완전히 독립 실행 가능한 단일 페이지
├─ vercel.json     cleanUrls + gal/ 1년 immutable 캐시
├─ robots.txt
├─ sitemap.xml
├─ README.md
├─ PHOTOS.md       이 지점에 어떤 사진을 어떤 파일명으로 넣어야 하는지
└─ gal/            지점 사진 (여기에 파일을 넣으면 자동 반영)
```

`sites/<slug>/` 폴더 하나가 그대로 배포 루트다. 저장소 루트에 통째로 올리거나
`vercel deploy sites/<slug> --prod` 하면 끝이고, 런타임에 빌드가 필요 없다.

## 구조

```
anitok-campuses/
├─ build.mjs              데이터 → 사이트 생성기
├─ lib/render.mjs         페이지 렌더러 (CSS·JS·전 섹션 마크업)
├─ data/
│  ├─ _shared.json        전 지점 공통 (회사정보·메뉴·상담시간·진행단계)
│  └─ <slug>.json         지점별 내용
├─ tools/fetch-images.mjs 원격 이미지를 gal/ 로 내려받는 스크립트
└─ sites/                 빌드 결과 (배포 루트)
```

`index.html` 을 직접 고치지 말 것. 데이터(`data/<slug>.json`)나 템플릿(`lib/render.mjs`)을
고친 뒤 다시 빌드한다.

## 일산 사이트와의 차이

같은 것: 검정 배경 · 애니톡 레드(#BD0D16) 액센트 · Pretendard · 스티키 레드 헤더 ·
스크롤 진행 바 · 번호 레이블 · 이모지 없음 · 섹션 구성(히어로 → 소개 → 합격실적 →
합격명단 → 수업과목 → 갤러리 → 진행과정 → FAQ → 오시는 길).

다른 것:

- **React를 쓰지 않는다.** 일산 사이트는 목록을 React UMD로 클라이언트 렌더링하지만
  여기서는 전부 빌드 타임에 정적 HTML로 굽는다. 검색엔진이 본문을 그대로 읽고,
  런타임 JS는 스크롤 리빌 · 모바일 메뉴 · 라이트박스만 담당한다(약 2KB).
- **폰트를 자체 호스팅하지 않는다.** 일산은 Pretendard 92개 서브셋(3.1MB)을 직접
  담고 있다. 여기서는 jsDelivr의 dynamic-subset CSS를 쓴다. 자체 호스팅으로 바꾸려면
  `ilsan-anitok/fonts/` 를 각 `sites/<slug>/fonts/` 로 복사하고 `lib/render.mjs` 의
  stylesheet 링크를 교체하면 된다.
- **인라인 스타일 대신 CSS 클래스**를 쓴다. 12개 지점으로 늘어나도 한 곳만 고치면 된다.

## 사진

지점 실사진이 아직 없다. 이미지 슬롯은 세 단계로 해결된다.

1. `sites/<slug>/gal/<파일명>` 이 실제로 있으면 그것을 쓴다 (최우선)
2. 없으면 데이터의 `remote` URL로 폴백 — 현재 히어로만 해당하며, anitok.com
   캠퍼스 안내 페이지에 걸려 있는 각 지점 대표 이미지를 가리킨다
3. 둘 다 없으면 캡션이 박힌 플레이스홀더 블록이 그려진다

지점 사진이 준비되면 `sites/<slug>/PHOTOS.md` 의 파일명대로 `gal/` 에 넣고 다시 빌드하면
그대로 반영된다. 이미지가 로드에 실패해도 깨진 아이콘 대신 플레이스홀더로 대체된다.

원격 이미지를 로컬로 내려받아 두려면(외부 네트워크가 열린 환경에서):

```bash
node tools/fetch-images.mjs
node build.mjs
```

## 배포 전 확인할 것

`data/<slug>.json` 에서 아직 비어 있거나 확인이 필요한 값:

- `analytics.ga4` — 전부 `null`. 지점별 GA4 측정 ID를 넣으면 헤드에 태그가 붙는다.
  (일산은 `G-FT5DQ3M85P` 를 쓰고 있는데, 지점 트래픽을 섞지 않으려면 지점마다 새 속성을 만드는 편이 낫다.)
- `geo.lat` / `geo.lng` — 전부 `null`. 값을 넣으면 `geo.position` · `ICBM` 메타와
  JSON-LD `GeoCoordinates` 가 자동으로 붙는다. 로컬 SEO에 도움이 된다.
- 네이버 사이트 인증 — 도메인마다 따로 발급받아야 해서 넣지 않았다. 발급 후
  `seo.verification` 배열에 `{ "name": "naver-site-verification", "content": "..." }` 를 추가한다.
- 네이버 예약 URL — 일산은 예약 링크가 있지만 나머지 지점은 확인되지 않아
  1차 CTA를 anitok.com 온라인 상담으로 걸어 두었다. 지점 예약 URL이 있으면
  `hero.ctas[0].href` 를 바꾸면 된다.
- 상담 시간 — anitok.com 대표 안내(평일 13:00-22:00, 토 13:00-18:00)를 공통으로 넣었다.
  지점별로 다르면 `_shared.json` 대신 지점 파일에서 `hours` 를 덮어쓴다.

## 데이터 출처

지점 주소 · 전화 · 네이버 플레이스 · 블로그 · 인스타그램 · 합격 실적 · 운영 반 정보는
전부 anitok.com 캠퍼스 안내(`https://anitok.com/locations`) 각 지점 상세 페이지에
게시된 내용을 옮긴 것이다. 실적 수치는 지점이 스스로 밝힌 값이며, 바뀌었다면
`data/<slug>.json` 의 `results` · `passList` 를 고치면 된다.
