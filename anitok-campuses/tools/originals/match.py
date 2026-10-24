"""시안에서 잘라 쓴 작품 썸네일(work-06~10)의 원본을 예전 anitok.com 이미지 중에서 찾는다.

작업 환경에서는 cdn.imweb.me 에 닿지 않아 GitHub Actions 에서 한 번 돌린다.
후보를 모두 받아 가운데 정사각(사이트 썸네일과 같은 자르기)의 16x16 흑백 지문을
비교하고, 가까운 순서대로 보고서와 대조표를 out/ 에 남긴다. 거리가 충분히 작은
것만 원본으로 저장한다(긴 변 2400px 이하로 줄인 JPEG).
"""
import io, os, urllib.request
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
GAL = os.path.join(HERE, '..', '..', 'sites', 'gimpo', 'gal')
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
TARGETS = ['work-%02d' % i for i in range(6, 11)]
LIMIT = 14  # 같은 그림이면 대개 한 자릿수, 다른 그림은 20 이상

def square(im):
    w, h = im.size; s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))

def sig(im, n=16):
    return list(square(im.convert('RGB')).convert('L').resize((n, n), Image.LANCZOS).getdata())

def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)

targets = {t: Image.open(os.path.join(GAL, t + '.webp')).convert('RGB') for t in TARGETS}
tsig = {t: (sig(im), sig(im, 32)) for t, im in targets.items()}
def crawl(start, limit=600):
    """anitok.com 안의 페이지를 돌며 cdn.imweb.me 이미지 주소를 모은다."""
    import re, urllib.parse
    seen, queue, imgs = set(), list(start), set()
    while queue and len(seen) < limit:
        page = queue.pop(0)
        if page in seen:
            continue
        seen.add(page)
        try:
            req = urllib.request.Request(page, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'ignore')
        except Exception:
            continue
        for m in re.findall(r'https?:\\?/\\?/cdn\.imweb\.me[^"\'\s)<>]+?\.(?:jpe?g|png|webp|gif)', html, re.I):
            imgs.add(m.replace('\\/', '/'))
        for href in re.findall(r'href="([^"#]+)"', html):
            u = urllib.parse.urljoin(page, href.replace('&amp;', '&'))
            host = urllib.parse.urlparse(u).netloc
            if host.endswith('anitok.com') and not re.search(r'\.(jpe?g|png|webp|gif|pdf|zip)$', u, re.I) \
                    and 'idx=' not in u.split('?')[0] and u not in seen and len(queue) < 4000:
                queue.append(u)
    print('crawled', len(seen), 'pages,', len(imgs), 'images')
    return imgs

urls = set(open(os.path.join(HERE, 'urls.txt')).read().split())
urls |= crawl(['https://anitok.com/', 'https://www.anitok.com/'])
open(os.path.join(OUT, 'urls-found.txt'), 'w').write('\n'.join(sorted(urls)) + '\n')
def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=40).read())); im.load()
    return im.convert('RGB')

# 지문과 작은 썸네일만 들고 있는다. 원본은 고른 뒤에 다시 받는다.
cands = []
for url in sorted(urls)[:2500]:
    try:
        im = fetch(url)
        if min(im.size) < 300:
            continue
        tn = square(im); tn.thumbnail((256, 256))
        cands.append((url, im.size, sig(im), sig(im, 32), tn))
    except Exception as e:
        print('ERR', url, e)
print('candidates', len(cands))

report = []
for t, (s16, s32) in tsig.items():
    ranked = sorted(cands, key=lambda c: dist(s16, c[2]) + dist(s32, c[3]))[:5]
    report.append('== ' + t)
    sheet = Image.new('RGB', (6 * 260, 300), 'white'); d = ImageDraw.Draw(sheet)
    th = targets[t].copy(); th.thumbnail((256, 256)); sheet.paste(th, (2, 2)); d.text((4, 266), t, fill='black')
    for k, (url, size, c16, c32, tn) in enumerate(ranked):
        score = (dist(s16, c16) + dist(s32, c32)) / 2
        report.append('%.1f %s %dx%d' % (score, url, size[0], size[1]))
        sheet.paste(tn, ((k + 1) * 260 + 2, 2))
        d.text(((k + 1) * 260 + 4, 266), '%.1f %s' % (score, url.rsplit('/', 1)[-1]), fill='black')
    sheet.save(os.path.join(OUT, t + '-sheet.jpg'), quality=80)
    if not ranked:
        continue
    url, size, c16, c32, tn = ranked[0]
    if (dist(s16, c16) + dist(s32, c32)) / 2 <= LIMIT:
        big = fetch(url); big.thumbnail((2400, 2400), Image.LANCZOS)
        big.save(os.path.join(OUT, t + '-full.jpg'), quality=90, optimize=True, progressive=True)
        report.append('SAVED ' + t + '-full.jpg')
open(os.path.join(OUT, 'report.txt'), 'w').write('\n'.join(report) + '\n')
print('\n'.join(report))
