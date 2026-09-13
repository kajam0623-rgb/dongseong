#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PageSpeed Insights 실제 캡처를 실적 밴드에 넣는다.

왜 이미지인가
  점수를 HTML 로 다시 그리면 "저희가 적은 숫자"가 되고, 캡처는 "도구가 찍은
  화면"이 된다. 238LAB 문법에서 제3자 도구 캡처는 재현 표보다 강한 증거다.
  그래서 PSI 블록만 캡처로 바꾼다. 네이버 유입 카드는 병원명 노출 위험이
  커서 HTML 재현을 유지한다.

성능은 이렇게 지킨다 (PSI 100점 목표와 충돌하지 않게)
  · WebP 품질 82, 최대 폭 1200px
  · width/height 속성 명시 → CLS 0
  · loading="lazy" — 실적 밴드는 첫 화면 아래라 LCP 후보가 아니다
  · alt 에 점수를 전부 적는다. 이미지가 안 떠도, 스크린리더도, AI 도 읽는다
    (GEO 를 파는 회사가 이미지에 데이터를 가둬 두면 안 된다)

쓰는 법
  1) 캡처 두 장을 assets/psi/ 에 넣는다
       assets/psi/mobile.png    (모바일 측정 리포트)
       assets/psi/desktop.png   (데스크톱 측정 리포트)
       확장자는 png·jpg·webp 아무거나.
  2) 좌표를 잡는다 — 도메인이 찍힌 자리를 가려야 한다
       node tools/img2webp.js --in assets/psi/mobile.png --info
       node tools/img2webp.js --in assets/psi/mobile.png --out /tmp/x.webp --grid
       나온 -grid.png 를 보고 아래 MASKS 의 비율을 맞춘다 (x,y,w,h · 0~1)
  3) python3 build-psi-shots.py
       → images/psi-*.webp 생성 + Home/Work 마크업 교체 + 실제 치수 기입

  파일이 없으면 아무것도 바꾸지 않고 안내만 하고 끝난다.
"""
import sys, io, os, re, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'assets', 'psi')
OUTDIR = os.path.join(HERE, 'images')

# 가릴 영역 (x, y, w, h — 0~1 비율). PSI 리포트는 상단에 측정 URL 이 찍힌다.
# --grid 로 확인한 뒤 맞추면 된다. 비워 두면 모자이크 없이 변환만 한다.
# --grid 로 실측한 값이다(2026-09-13). 두 곳을 가린다.
#   1) 주소창의 도메인 글자 — 주소창 틀은 남긴다. 틀이 남아야 진짜 리포트
#      화면이라는 게 보이고, 그게 캡처를 싣는 이유다.
#   2) 우측 사이트 썸네일 — 병원 로고와 원장님 사진이 그대로 들어 있다.
#      도메인보다 이쪽이 더 직접적인 식별 정보인데 놓치기 쉽다.
MASKS = {
    'mobile':  ['0.033,0.060,0.200,0.048',    # https://...  (1200x1269 기준)
                '0.648,0.482,0.140,0.245'],   # 사이트 썸네일
    'desktop': ['0.033,0.052,0.190,0.046',    # https://...  (1200x1288 기준)
                '0.582,0.498,0.340,0.225'],   # 사이트 썸네일
}

# 캡션·alt 에 들어갈 실측값 (대화로 받은 캡처 수치)
DATA = {
    'mobile': dict(
        id='치과 ④', cond='모바일 측정',
        when='2026년 8월 31일 22:00 · 주소와 사이트 미리보기는 가렸습니다',
        vitals='FCP 1.0초 · LCP 1.7초 · TBT 0ms · CLS 0.003 · SI 1.8초 · 에이전트형 브라우징 3/3'),
    'desktop': dict(
        id='치과 ⑤', cond='데스크톱 측정',
        when='2026년 8월 31일 12:39 · 주소와 사이트 미리보기는 가렸습니다',
        vitals='FCP 0.4초 · LCP 0.6초 · TBT 10ms · CLS 0.006 · SI 0.6초 · 에이전트형 브라우징 2/2'),
}

WP_PATH = '/wp-content/uploads/ciclo/'   # 워드프레스 업로드 경로


def find(stem):
    """assets/psi/ 에서 캡처 파일을 찾는다.

    1순위는 mobile.* / desktop.* 다.
    없으면 그 폴더의 이미지를 파일명으로 판별한다 — 카톡이나 깃허브로 올리면
    KakaoTalk_20260907_193951534.png 같은 이름 그대로 들어오기 때문이다.
    이름으로 못 가리면 남은 이미지를 알파벳 순으로 mobile → desktop 에 배정하고
    무엇을 무엇으로 봤는지 찍어 준다. 틀렸으면 파일만 맞바꿔 다시 돌리면 된다.
    """
    for ext in ('png', 'jpg', 'jpeg', 'webp'):
        hits = glob.glob(os.path.join(SRC, stem + '.' + ext))
        if hits:
            return hits[0]

    imgs = sorted(p for e in ('png', 'jpg', 'jpeg', 'webp')
                  for p in glob.glob(os.path.join(SRC, '*.' + e)))
    if not imgs:
        return None

    # 파일명에 힌트가 있으면 쓴다
    KEY = {'mobile': ('mobile', 'mob', '모바일', '휴대'),
           'desktop': ('desktop', 'desk', 'pc', '데스크')}
    for p in imgs:
        low = os.path.basename(p).lower()
        if any(k in low for k in KEY[stem]):
            return p

    # 힌트가 없으면 순서대로 — mobile 이 먼저다
    named = {p for st in ('mobile', 'desktop')
             for k in KEY[st] for p in imgs if k in os.path.basename(p).lower()}
    rest = [p for p in imgs if p not in named]
    idx = 0 if stem == 'mobile' else 1
    if len(rest) > idx:
        print('   ※ %s ← %s (파일명에 힌트가 없어 순서로 배정했습니다)'
              % (stem, os.path.basename(rest[idx])))
        return rest[idx]
    return None


def convert(stem):
    src = find(stem)
    out = os.path.join(OUTDIR, 'psi-%s.webp' % stem)
    cmd = ['node', os.path.join(HERE, 'tools', 'img2webp.js'),
           '--in', src, '--out', out, '--width', '1200', '--quality', '82']
    for m in MASKS.get(stem, []):
        cmd += ['--mask', m]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('변환 실패 (%s)\n%s' % (stem, r.stderr))
    print(r.stdout.rstrip())
    dim = re.search(r'^DIM (\d+) (\d+)$', r.stdout, re.M)
    if not dim:
        sys.exit('치수를 읽지 못했습니다 (%s)' % stem)
    return int(dim.group(1)), int(dim.group(2))


def figure(stem, w, h):
    d = DATA[stem]
    alt = ('PageSpeed Insights %s 결과 — 성능 100, 접근성 100, 권장사항 100, '
           '검색엔진 최적화 100. %s' % (d['cond'], d['vitals']))
    return (
        '      <figure class="psi-shot">\n'
        '        <img src="%spsi-%s.webp" alt="%s"\n'
        '             width="%d" height="%d" loading="lazy" decoding="async">\n'
        '        <figcaption><b>%s · %s</b> · %s</figcaption>\n'
        '      </figure>\n' % (WP_PATH, stem, alt, w, h, d['id'], d['cond'], d['when']))


# 캡처는 표를 대신하지 않고 표 위에 얹는다.
# 캡처는 "도구가 찍은 화면"이고 표는 "기계가 읽는 값"이라 하는 일이 다르다.
# 검색엔진과 AI 는 이미지 속 숫자를 못 읽는다. GEO 를 파는 회사가 자기 근거를
# 기계가 못 읽는 형식으로만 두면 앞뒤가 안 맞는다. 둘 다 둔다.
ANCHOR = '    <div class="psi-cards">'


def patch(path, block):
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    if '<figure class="psi-shot">' in s:
        print('..  %s — 이미 캡처가 들어 있음' % path); return
    if s.count(ANCHOR) != 1:
        print('..  %s — .psi-cards 없음, 건너뜀' % path); return
    s = s.replace(ANCHOR, '    <div class="psi-shots">\n' + block + '    </div>\n' + ANCHOR, 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('ok  %s' % path)


def main():
    missing = [k for k in ('mobile', 'desktop') if not find(k)]
    if missing:
        print('캡처 파일이 아직 없습니다: ' + ', '.join(missing))
        print()
        print('  아래 위치에 넣어 주세요 (png·jpg·webp 아무거나):')
        for k in ('mobile', 'desktop'):
            mark = '있음' if find(k) else '없음'
            print('    assets/psi/%-12s  [%s]' % (k + '.png', mark))
        print()
        print('  넣은 뒤 좌표를 확인하고:')
        print('    node tools/img2webp.js --in assets/psi/mobile.png --out /tmp/x.webp --grid')
        print('    (나온 /tmp/x-grid.png 로 가릴 영역을 정한 뒤 이 파일의 MASKS 수정)')
        print()
        print('  그리고 다시: python3 build-psi-shots.py')
        print()
        print('마크업은 바꾸지 않았습니다. 지금 화면은 기존 링 카드 그대로입니다.')
        return 1

    os.makedirs(OUTDIR, exist_ok=True)
    figs = []
    for stem in ('mobile', 'desktop'):
        w, h = convert(stem)
        figs.append(figure(stem, w, h))

    block = ''.join(figs)
    patch('pages/Home.html', block)
    patch('pages/Work.html', block)
    print()
    print('※ build-theme.py 가 webp 를 테마 안으로 복사하고 경로를 바꿉니다.')
    print('   워드프레스 미디어에 따로 올리실 필요 없습니다.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
