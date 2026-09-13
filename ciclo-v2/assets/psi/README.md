# PSI 캡처 넣는 자리

PageSpeed Insights 리포트 캡처 두 장을 여기에 둡니다.

```
mobile.png     모바일 측정 리포트 (치과 ④)
desktop.png    데스크톱 측정 리포트 (치과 ⑤)
```

확장자는 `png` · `jpg` · `webp` 아무거나 됩니다. 원본 그대로 두세요 —
리사이즈·모자이크·WebP 변환은 스크립트가 합니다.

## 넣은 뒤

```bash
# 1) 가릴 자리 확인 (측정 URL·도메인이 찍힌 영역)
node tools/img2webp.js --in assets/psi/mobile.png --out /tmp/x.webp --grid
#    → /tmp/x-grid.png 에 10% 격자가 얹혀 나옵니다. 좌표를 읽어
#      build-psi-shots.py 의 MASKS 를 x,y,w,h (0~1 비율)로 고칩니다.

# 2) 변환 + 마크업 교체
python3 build-psi-shots.py
```

`images/psi-mobile.webp` · `psi-desktop.webp` 가 만들어지고
Home·Work 의 링 카드가 캡처 `<figure>` 로 바뀝니다.
마지막으로 그 두 파일을 워드프레스 `/wp-content/uploads/ciclo/` 에 올리면 끝입니다.

## 이 폴더는 배포물이 아닙니다

원본 캡처는 모자이크 전 상태라 저장소에만 두고 서버에 올리지 않습니다.
서버에 올라가는 건 `images/psi-*.webp` 쪽입니다.
