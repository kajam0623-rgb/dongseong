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
MASKS = {
    'mobile':  ['0.012,0.02,0.30,0.085'],
    'desktop': ['0.012,0.02,0.30,0.085'],
}

# 캡션·alt 에 들어갈 실측값 (대화로 받은 캡처 수치)
DATA = {
    'mobile': dict(
        id='치과 ④', cond='모바일 측정',
        vitals='FCP 1.0초 · LCP 1.7초 · TBT 0ms · CLS 0.003 · SI 1.8초'),
    'desktop': dict(
        id='치과 ⑤', cond='데스크톱 측정',
        vitals='FCP 0.4초 · LCP 0.6초 · TBT 10ms · CLS 0.006 · SI 0.6초'),
}

WP_PATH = '/wp-content/uploads/ciclo/'   # 워드프레스 업로드 경로


def find(stem):
    for ext in ('png', 'jpg', 'jpeg', 'webp'):
        hits = glob.glob(os.path.join(SRC, stem + '.' + ext))
        if hits:
            return hits[0]
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
        '        <figcaption><b>%s · %s</b> — 네 항목 모두 100점 · %s</figcaption>\n'
        '      </figure>\n' % (WP_PATH, stem, alt, w, h, d['id'], d['cond'], d['vitals']))


# 교체 대상: 기존 링 카드 두 장을 감싼 .psi-cards 블록
CARDS_RE = re.compile(
    r'[ \t]*<div class="psi-cards">.*?</div>\n(?=[ \t]*<p class="(?:res-note|sec-caption)")',
    re.S)


def patch(path, block):
    p = os.path.join(HERE, path)
    s = io.open(p, encoding='utf-8').read()
    n = len(CARDS_RE.findall(s))
    if n != 1:
        sys.exit('FAIL %s: .psi-cards 블록 %d개 (1개여야 함)' % (path, n))
    s = CARDS_RE.sub(block, s)
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

    block = '      <div class="psi-shots">\n' + ''.join(figs) + '      </div>\n'
    patch('pages/Home.html', block)
    patch('pages/Work.html', block.replace('      ', '    ', 1))
    print()
    print('※ images/psi-mobile.webp · psi-desktop.webp 를 워드프레스')
    print('   %s 에 업로드해야 화면에 뜹니다.' % WP_PATH)
    return 0


if __name__ == '__main__':
    sys.exit(main())
