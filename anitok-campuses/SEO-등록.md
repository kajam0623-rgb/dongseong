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

**academy 만 예외다.** 지금 주소가 `academy-anitok.vercel.app` 이라 `anitok.com`
도메인 속성에 들어가지 않는다. URL 접두어로 따로 등록하거나, 서브도메인
(`academy.anitok.com`)을 붙이면 같이 해결된다.
※ 전에 말씀하신 `acdemy.anitok.com` 은 `academy` 오타인지 확인이 필요하다.

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
   https://academy-anitok.vercel.app/
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
