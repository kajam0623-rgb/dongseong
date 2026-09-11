# 검색 노출 등록 안내

일산만 네이버·구글에 뜨고 나머지가 안 뜨는 이유는 **사이트 문제가 아니다.**
7곳 모두 `index, follow`, `robots.txt` 허용, 사이트맵, LocalBusiness 구조화 데이터
(주소·좌표·전화·네이버플레이스·블로그·인스타), 지점 간 상호링크가 전부 들어 있다.

빠진 것은 **검색엔진에 등록하는 일** 하나다. 이건 로그인이 필요해서 사장님만 할 수 있다.

## 지금 상태

| 지점 | 구글 서치콘솔 | 네이버 서치어드바이저 |
|---|---|---|
| 일산 | 등록됨 | 등록됨 (`bfa240b5…`) |
| 목동 | 미등록 | 태그는 올라감 (`c4e31ad6…`) — **소유확인 버튼만 누르면 끝** |
| 홍대 · 강동 · 광교 · 김포 · 부천 · academy | 미등록 | 태그 없음 |

> 캠퍼스 7곳의 구글 태그는 전부 **일산 것의 복사본**이다.
> 구글의 HTML 태그 코드는 속성 하나당 하나라서, 다른 주소에 붙여도 인증되지 않는다.
> 해롭지는 않지만 아무 일도 하지 않는다. 아래 1번을 하면 이 태그는 필요 없어진다.

---

## 1. 구글 — 도메인 속성 하나로 8곳을 한 번에

지점마다 따로 할 필요가 없다. `anitok.com`을 **도메인 속성**으로 등록하면
`ilsan` · `mokdong` · `hongdae` 등 **모든 서브도메인이 한 번에 인증된다.**

1. https://search.google.com/search-console → 속성 추가
2. 왼쪽 **"도메인"** 을 고른다 (오른쪽 "URL 접두어"가 아니다 — 그건 주소마다 따로 해야 한다)
3. `anitok.com` 입력
4. 화면에 나오는 **TXT 레코드**를 도메인 DNS에 추가한다
   (가비아·후이즈 등 도메인 산 곳의 DNS 설정)
5. DNS 반영 후 "확인" — 보통 몇 분, 길면 몇 시간
6. 인증되면 좌측 **Sitemaps** 에서 지점별로 제출:
   ```
   https://ilsan.anitok.com/sitemap.xml
   https://mokdong.anitok.com/sitemap.xml
   https://hongdae.anitok.com/sitemap.xml
   https://gangdong.anitok.com/sitemap.xml
   https://gwanggyo.anitok.com/sitemap.xml
   https://gimpo.anitok.com/sitemap.xml
   https://bucheon.anitok.com/sitemap.xml
   ```

**academy 도 이제 `anitok.com` 안에 있다.** 2026-09-11 에 `academy.anitok.com` 으로 옮겼다.
따로 등록할 필요 없이 도메인 속성 하나로 8곳이 전부 인증된다.
오타 도메인 `acdemy.anitok.com` 은 정식 주소로 301 넘기게 해 두었다. Vercel 에서 아예
떼어내도 되고, 그대로 두어도 색인이 갈라지지 않는다.

---

## 2. 네이버 — 서브도메인마다 따로 등록해야 한다

네이버에는 도메인 속성 같은 개념이 없다. 그리고 **등록하지 않은 사이트는 거의 수집하지
않는다.** 링크가 아무리 걸려 있어도 안 온다. 일산만 나오는 이유가 이것이다.

1. https://searchadvisor.naver.com → 웹마스터도구 → 사이트 등록
2. 아래 6개를 하나씩 등록 (`https://` 포함, 끝에 `/`)
   ```
   https://hongdae.anitok.com/
   https://gangdong.anitok.com/
   https://gwanggyo.anitok.com/
   https://gimpo.anitok.com/
   https://bucheon.anitok.com/
   https://academy.anitok.com/
   ```
3. 소유확인 방법에서 **"HTML 태그"** 를 고르면 이런 줄이 나온다:
   ```html
   <meta name="naver-site-verification" content="1a2b3c4d5e..." />
   ```
4. **이 줄을 그대로 나(클로드)에게 붙여넣으면** 코드를 넣고 배포한다.
   6개를 한 번에 주셔도 되고, 하나씩 주셔도 된다. 어느 지점 것인지만 적어달라.
5. 배포가 끝나면 다시 서치어드바이저에서 **"소유확인"** 을 누른다
6. 확인되면 **요청 → 사이트맵 제출** 에 `https://<지점>.anitok.com/sitemap.xml`

**목동은 태그가 이미 올라가 있다.** 3~4번을 건너뛰고 소유확인만 누르면 된다.

---

## 3. 네이버 플레이스 — 지역 검색은 여기가 먼저다

"김포 만화학원" 을 치면 **플레이스가 위**에 뜨고 웹사이트는 아래다.
홈페이지 SEO 보다 이쪽이 지역 노출에는 더 직접적이다.

지점 7곳 플레이스 관리자에서 **홈페이지 주소가 각 지점 서브도메인인지** 확인한다.
대표 주소(`anitok.com`)로만 돼 있으면 지점 사이트로 신호가 가지 않는다.

사이트에는 이미 플레이스가 연결돼 있다 (`sameAs` · `hasMap`). 예를 들어 김포는
`https://m.place.naver.com/place/1052247671/home` 이다. 양쪽이 서로를 가리켜야 한다.

---

## 코드를 받으면 내가 하는 일

지점 JSON 에 한 줄만 넣으면 된다.

```json
"seo": {
  "naver": "1a2b3c4d5e..."
}
```

`seo.verification` 배열에 직접 적지 말 것. 그 배열은 `_shared.json` 의 것을
통째로 갈아끼우기 때문에, 네이버 항목만 적으면 **구글 태그가 조용히 사라진다.**
`seo.naver` 에 적으면 `build.mjs` 가 공통 배열에 얹어준다.

---

## 얼마나 걸리나

- 네이버: 등록·소유확인 후 며칠 안에 수집이 시작된다. 등록 전에는 몇 달이 지나도 안 된다.
- 구글: 사이트맵 제출 후 보통 1~3주. 제출하지 않아도 언젠가는 찾아오지만 훨씬 느리다.
- 그저께까지 각 사이트는 `index.html` 과 `404.html` 두 장뿐이었다. 지금은 지점당 8장
  (홍대 13장) 이다. 구글이 마지막으로 본 것이 2장짜리 사이트라면 순위가 올라갈 수 없다.
  **다시 크롤링되어야 평가가 바뀐다.** 사이트맵 제출이 그 시작을 앞당긴다.

---

# 부록 — 지역 랜딩페이지 중복 정리 (2026-09-11)

## 무엇이 문제였나

지점마다 지역 랜딩페이지가 6장씩, 모두 42장이 있다. 그런데 **같은 과목·다른 동네** 쌍은
본문이 거의 같았다. 실측하면 88~90% 가 겹친다.

```
gimpo-webtoon   vs  gurae-webtoon      88% 동일
hongdae-webtoon vs  yeonnam-webtoon    88% 동일
bucheon-manhwa  vs  bupyeong-manhwa    90% 동일
```

내용이 전부 `_shared.json` 의 `localSubjects[과목]` 에서 나오고, 바뀌는 것은 **동네 이름과
`note` 한 줄**뿐이기 때문이다. 구글은 이런 묶음을 도어웨이 페이지로 본다. 잘해야 하나만
남기고 나머지를 걸러내고, 나쁘면 사이트 전체 평가를 깎는다. 노출을 늘리려고 만든 페이지가
반대로 발목을 잡는 상태였다.

## 어떻게 했나

그 동네만의 내용이 **실제로 있을 때만** 독립 페이지로 두고, 없으면 `canonical` 을 같은 과목
대표 페이지로 넘긴다. 사이트맵에서도 뺀다(넣어두면 서치콘솔이 "제출된 URL이 대표 URL로
선택되지 않음"으로 잡는다).

- 방문자에게는 그대로 보인다. 페이지는 살아 있고 내용도 그대로다.
- 검색엔진에는 신호가 대표 페이지 하나로 모인다.
- 색인 대상끼리의 최고 유사도가 **88~90% → 29~30%** 로 떨어졌다. 템플릿이 같아서 생기는
  정상 범위다.

```
42장 → 색인 대상 29장 + 대표 페이지로 합친 13장
```

## 합쳐진 13장 — 내용을 채우면 되살아난다

`data/<지점>.json` 의 `local.nearby` 항목에 **`intro`** 를 넣으면 그 페이지는 즉시 제 주소를
되찾고 사이트맵에도 다시 들어간다. 빌드가 알아서 판단한다.

```json
{
  "area": "구래동",
  "slug": "gurae",
  "subject": "webtoon",
  "note": "구래동 인근 학생들이 함께 수강하고 있습니다.",
  "intro": [
    "구래동에서 오는 학생은 주로 ○○을 타고 ○분 걸립니다. 수업이 끝나는 시간에 맞춰...",
    "구래동 ○○중·○○고 학생들이 다니고 있습니다. 시험 기간에는..."
  ]
}
```

`points` 도 같은 방식으로 덮어쓸 수 있다 (`[{ "t": "제목", "d": "설명" }]`).

| 지점 | 합쳐진 페이지 | 동네 | 합쳐진 대상 |
|---|---|---|---|
| academy | `mokdong-webtoon` | 목동 | `sinjeong-webtoon` |
| academy | `yangcheon-drawing` | 양천구 | `sinjeong-drawing` |
| bucheon | `jungdong-manhwa` | 중동 | `bucheon-manhwa` |
| bucheon | `bupyeong-manhwa` | 부평 | `bucheon-manhwa` |
| gangdong | `cheonho-manhwa` | 천호 | `gangdong-manhwa` |
| gangdong | `songpa-manhwa` | 송파 | `gangdong-manhwa` |
| gimpo | `hangang-manhwa` | 한강신도시 | `gimpo-manhwa` |
| gimpo | `gurae-webtoon` | 구래동 | `gimpo-webtoon` |
| gwanggyo | `suwon-manhwa` | 수원 | `gwanggyo-manhwa` |
| gwanggyo | `yeongtong-webtoon` | 영통 | `gwanggyo-webtoon` |
| hongdae | `hapjeong-manhwa` | 합정 | `hongdae-manhwa` |
| hongdae | `yeonnam-webtoon` | 연남 | `hongdae-webtoon` |
| mokdong | `hwagok-manhwa` | 화곡 | `mokdong-manhwa` |

**무엇을 쓰면 되나.** 그 동네 학생이 실제로 어떻게 오는지(교통·소요시간), 어느 학교 학생이
다니는지, 그 동네라서 다른 점이 무엇인지. 동네마다 두세 문단이면 충분하다.
사실만 쓰면 된다 — 없는 정보를 지어내면 안 된다. 13개 중 급한 것부터 채워도 된다.
