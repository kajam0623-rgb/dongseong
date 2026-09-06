import zlib, struct, math

SIZE = 180
SS = 4                       # 4x 슈퍼샘플링 안티에일리어싱
EYE = [(17.5, 28.5), (46.5, 28.5)]
EYE_R = 4.6
C = (32.0, 34.0)             # 미소 호의 중심
R = 6.5                      # 호 반지름
T = 2.3                      # 선 두께의 절반
CAP = [(25.5, 34.0), (38.5, 34.0)]

def inside(x, y):
    for cx, cy in EYE:
        if (x - cx) ** 2 + (y - cy) ** 2 <= EYE_R ** 2:
            return True
    for cx, cy in CAP:
        if (x - cx) ** 2 + (y - cy) ** 2 <= T ** 2:
            return True
    if y >= C[1]:
        d = math.hypot(x - C[0], y - C[1])
        if R - T <= d <= R + T:
            return True
    return False

def render(path, fg):
    s = 64.0 / (SIZE * SS)
    rows = []
    for py in range(SIZE):
        row = bytearray()
        for px in range(SIZE):
            hit = 0
            for sy in range(SS):
                for sx in range(SS):
                    x = (px * SS + sx + 0.5) * s
                    y = (py * SS + sy + 0.5) * s
                    if inside(x, y):
                        hit += 1
            a = hit / (SS * SS)
            for c in range(3):
                row.append(round(255 * (1 - a) + fg[c] * a))
        rows.append(bytes(row))
    raw = b''.join(b'\x00' + r for r in rows)
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', SIZE, SIZE, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(raw, 9))
           + chunk(b'IEND', b''))
    open(path, 'wb').write(png)

render('assets/apple-touch-icon-orange.png', (0xC9, 0x48, 0x0B))
render('assets/apple-touch-icon-mono.png', (0x0B, 0x0B, 0x0C))
print('ok')
