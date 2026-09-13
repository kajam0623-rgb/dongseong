#!/usr/bin/env node
/* 캡처 이미지 → 모자이크 → 리사이즈 → WebP
 *
 * 이 환경에는 cwebp·ImageMagick·PIL·sharp 가 전부 없다.
 * 대신 크로미움이 있으므로 캔버스를 이미지 처리기로 쓴다.
 * 픽셀화는 "작게 그린 뒤 imageSmoothing 을 끄고 다시 키우는" 고전적 방법이다.
 *
 * 사용법
 *   node tools/img2webp.js --in a.png --out a.webp [옵션]
 *
 *   --width  N        출력 최대 폭 (기본 1200). 원본이 작으면 확대하지 않는다
 *   --quality 0-100   WebP 품질 (기본 82)
 *   --mask  x,y,w,h   모자이크 영역. 0~1 비율 또는 px. 여러 번 지정 가능
 *   --block N         모자이크 블록 크기 px (기본 12)
 *   --grid            좌표 잡기용: 10% 격자와 눈금을 얹은 PNG 를 함께 저장
 *   --info            변환하지 않고 원본 크기만 출력
 *
 * 예)  node tools/img2webp.js --in psi-m.png --out psi-mobile.webp \
 *        --mask .07,.11,.42,.05 --width 1200
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf('--' + k); return i < 0 ? d : argv[i + 1]; };
const flag = k => argv.includes('--' + k);
const masks = [];
argv.forEach((a, i) => { if (a === '--mask') masks.push(argv[i + 1]); });

const IN = arg('in'), OUT = arg('out');
if (!IN) { console.error('--in 이 필요합니다'); process.exit(2); }
if (!fs.existsSync(IN)) { console.error('파일이 없습니다: ' + IN); process.exit(2); }

const MAXW = +arg('width', 1200);
const Q = +arg('quality', 82) / 100;
const BLOCK = +arg('block', 12);

(async () => {
  const b = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const p = await b.newPage();
  const ext = path.extname(IN).slice(1).toLowerCase();
  const mime = ext === 'jpg' ? 'jpeg' : ext;
  const dataUrl = `data:image/${mime};base64,` + fs.readFileSync(IN).toString('base64');

  const res = await p.evaluate(async ({ dataUrl, MAXW, Q, BLOCK, masks, wantGrid, infoOnly }) => {
    const img = new Image();
    img.src = dataUrl;
    await img.decode();
    const sw = img.naturalWidth, sh = img.naturalHeight;
    if (infoOnly) return { sw, sh };

    const scale = Math.min(1, MAXW / sw);
    const w = Math.round(sw * scale), h = Math.round(sh * scale);

    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const x = c.getContext('2d');
    x.drawImage(img, 0, 0, w, h);

    // 모자이크
    const applied = [];
    for (const m of masks) {
      const v = m.split(',').map(Number);
      if (v.length !== 4 || v.some(isNaN)) continue;
      // 값이 전부 1 이하면 비율로, 아니면 원본 px 로 본다
      const isRatio = v.every(n => n <= 1);
      let [mx, my, mw, mh] = isRatio
        ? [v[0] * w, v[1] * h, v[2] * w, v[3] * h]
        : [v[0] * scale, v[1] * scale, v[2] * scale, v[3] * scale];
      mx = Math.max(0, Math.round(mx)); my = Math.max(0, Math.round(my));
      mw = Math.min(w - mx, Math.round(mw)); mh = Math.min(h - my, Math.round(mh));
      if (mw <= 0 || mh <= 0) continue;

      const bw = Math.max(1, Math.round(mw / BLOCK)), bh = Math.max(1, Math.round(mh / BLOCK));
      const t = document.createElement('canvas');
      t.width = bw; t.height = bh;
      const tx = t.getContext('2d');
      tx.imageSmoothingEnabled = true;
      tx.drawImage(c, mx, my, mw, mh, 0, 0, bw, bh);
      x.imageSmoothingEnabled = false;
      x.drawImage(t, 0, 0, bw, bh, mx, my, mw, mh);
      x.imageSmoothingEnabled = true;
      applied.push([mx, my, mw, mh]);
    }

    let grid = null;
    if (wantGrid) {
      const g = document.createElement('canvas');
      g.width = w; g.height = h;
      const gx = g.getContext('2d');
      gx.drawImage(c, 0, 0);
      gx.font = '600 13px monospace';
      for (let i = 1; i < 10; i++) {
        const px = Math.round(w * i / 10), py = Math.round(h * i / 10);
        gx.strokeStyle = 'rgba(255,0,0,.55)'; gx.lineWidth = 1;
        gx.beginPath(); gx.moveTo(px + .5, 0); gx.lineTo(px + .5, h); gx.stroke();
        gx.beginPath(); gx.moveTo(0, py + .5); gx.lineTo(w, py + .5); gx.stroke();
        gx.fillStyle = 'rgba(255,255,255,.9)';
        gx.fillRect(px + 2, 2, 30, 16); gx.fillRect(2, py + 2, 30, 16);
        gx.fillStyle = '#c00';
        gx.fillText('.' + i, px + 5, 15); gx.fillText('.' + i, 5, py + 15);
      }
      grid = g.toDataURL('image/png');
    }

    return { sw, sh, w, h, applied, webp: c.toDataURL('image/webp', Q), grid };
  }, { dataUrl, MAXW, Q, BLOCK, masks, wantGrid: flag('grid'), infoOnly: flag('info') });

  await b.close();

  if (flag('info')) {
    console.log(`${path.basename(IN)}  원본 ${res.sw}×${res.sh}px`);
    return;
  }
  if (!OUT) { console.error('--out 이 필요합니다'); process.exit(2); }

  const buf = Buffer.from(res.webp.split(',')[1], 'base64');
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, buf);
  console.log(`${path.basename(IN)}  ${res.sw}×${res.sh} → ${res.w}×${res.h}  `
    + `${(buf.length / 1024).toFixed(1)}KB  모자이크 ${res.applied.length}곳  → ${OUT}`);
  res.applied.forEach(a => console.log('     가린 영역 ' + a.join(', ')));

  if (res.grid) {
    const gp = OUT.replace(/\.webp$/, '') + '-grid.png';
    fs.writeFileSync(gp, Buffer.from(res.grid.split(',')[1], 'base64'));
    console.log('     좌표 격자 → ' + gp);
  }
  // 후속 스크립트가 쓸 수 있게 마지막 줄에 치수를 기계 판독 형태로 남긴다
  console.log(`DIM ${res.w} ${res.h}`);
})().catch(e => { console.error(e); process.exit(1); });
