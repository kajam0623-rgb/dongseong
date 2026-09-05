# 실태조사 리포트 배포판

**게시 중 — https://dental-seo-report.vercel.app**

`index.html` 하나와 `og.png` 하나. 빌드 과정 없음.

## 지금 상태

Vercel 개인 계정에 파일 직접 업로드 방식으로 올렸다. 배포 보호는 꺼져 있어 누구나 열린다.
`index.html`은 올라가 있고 **`og.png`는 아직 안 올라갔다.** 링크를 카카오톡이나 슬랙에
붙이면 카드 이미지가 비어 보인다.

## og.png 올리는 법

둘 중 하나.

1. Vercel 프로젝트 화면에서 이 폴더를 통째로 다시 올린다
2. vercel.com에서 GitHub 저장소를 붙이고 Root Directory를 `deploy`로 잡는다.
   이쪽이 낫다. 이미지도 같이 올라가고 앞으로 푸시할 때마다 자동 반영된다.
   다만 Vercel은 기본 브랜치에서 빌드하므로 이 브랜치를 먼저 병합해야 한다.

## 원본과 뭐가 다른가

`실태조사-리포트.html`은 아티팩트용이라 `<head>`가 없다. 배포판은 검색엔진과 AI가 읽을 수
있게 아래를 넣었다.

- `<!doctype>` · `<html lang="ko">` · charset · viewport
- title(본문 h1과 다르게, 표본 수까지 넣음) · description 122자 · canonical
- `robots: max-image-preview:large` — 검색 결과에 큰 썸네일이 걸린다
- 오픈그래프 10개 · 트위터 카드 4개 · og:image 1200×630
- JSON-LD 세 덩어리
  - `Report` — 제목, 발행일, 저자, 다룬 주제
  - `Dataset` — 표본 수, 측정 기간, 측정 방법, 측정한 값 셋(검색 39~84 / AI 답변 31~56 / 기계용 정보 표기 12~30)
  - `Organization`

리포트에서 "일곱 곳 모두 비어 있다"고 지적한 그 칸을, 리포트 자신이 채운 상태로 올라가 있다.

## 확인할 것

1. 구글 리치 결과 테스트에 URL을 넣어 `Report`와 `Dataset`이 잡히는지 본다
2. 카카오톡에 링크를 붙여 og 카드가 뜨는지 본다 (og.png 올린 뒤에)
3. 네이버 서치어드바이저에 사이트를 등록한다
4. 구글 서치콘솔에 URL 검사 후 색인 요청

## 남은 것

조직명이 "사이트온"으로 들어가 있다. 실제 상호가 정해지면 `index.html`에서
`author`, `og:site_name`, JSON-LD의 `Organization.name` 세 곳을 바꾼다.

폰트를 구글 폰트에서 받아온다. 외부 요청이라 첫 화면이 늦어질 수 있다.
`Pretendard`와 시스템 폰트로 떨어지게 되어 있으니 그대로 둬도 되고,
직접 호스팅하려면 woff2를 받아 `@font-face`로 바꾼다.
