"""Build the Powerflow mark from the pixel grids.

Writes src-tauri/icons/icon.svg (the master the app icons are generated from with
`pnpm tauri icon src-tauri/icons/icon.svg`) plus the crisp 16/32px menu-bar template
icons. Run: python3 scripts/logo/make.py <powerflow repo root>"""
import os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAL = {
    'd': '#8C6217', 'e': '#AF7F22', 'm': '#C99530', 'g': '#E0AE3F',
    'l': '#E8B84A', 'p': '#F3D58A', 'h': '#F9E7B4',
}
TILE, EDGE, SHEEN = '#0A0A0A', '#1E1E1E', '#FFFFFF'


def grid(name):
    return open(os.path.join(HERE, name)).read().split()


def bevel(rows):
    """Light the bolt from the top left: a one-pixel highlight on edges facing up or left,
    a one-pixel shade on edges facing down or right."""
    n = len(rows)
    def at(x, y):
        return rows[y][x] if 0 <= x < n and 0 <= y < n else '.'
    out = []
    for y, r in enumerate(rows):
        row = ''
        for x, c in enumerate(r):
            if c == 'l':
                if at(x, y - 1) != 'l' or at(x - 1, y) != 'l':
                    c = 'p'
                elif at(x, y + 1) != 'l' or at(x + 1, y) != 'l':
                    c = 'g'
            row += c
        out.append(row)
    return out


def rgba(c):
    return tuple(int(PAL[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def sprite(rows, scale=1):
    n = len(rows)
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != '.':
                im.putpixel((x, y), rgba(c))
    return im.resize((n * scale, n * scale), Image.NEAREST)


def centred(sp, size):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    x0, y0, x1, y1 = sp.getbbox()
    im.paste(sp, ((size - (x1 - x0)) // 2 - x0, (size - (y1 - y0)) // 2 - y0), sp)
    return im


def template(rows, size):
    """macOS menu-bar template image: the bolt silhouette in black plus alpha."""
    sp = sprite(rows, max(1, size // len(rows)))
    a = sp.split()[3]
    sp = Image.new('RGBA', sp.size, (0, 0, 0, 255))
    sp.putalpha(a)
    return centred(sp, size)


def paths(rows, cell, ox, oy):
    """One <path> per colour, built from horizontal runs of the grid."""
    runs = {}
    for y, r in enumerate(rows):
        x = 0
        while x < len(r):
            c = r[x]
            e = x
            while e < len(r) and r[e] == c:
                e += 1
            if c != '.':
                runs.setdefault(c, []).append(
                    f'M{ox + x * cell} {oy + y * cell}h{(e - x) * cell}v{cell}h-{(e - x) * cell}z')
            x = e
    return '\n'.join(f'  <path fill="{PAL[c]}" d="{"".join(d)}"/>' for c, d in runs.items())


def svg(rows):
    """The app icon: the mark on the tame.gg near-black tile, drawn to the macOS 824/1024 grid."""
    S = 1024
    m, rad, b = 100, 185, 14
    n = len(rows)
    inner = 544
    cell = inner // n
    xs = [x for x in range(n) if any(r[x] != '.' for r in rows)]
    ys = [y for y in range(n) if any(c != '.' for c in rows[y])]
    w, h = (xs[-1] - xs[0] + 1) * cell, (ys[-1] - ys[0] + 1) * cell
    ox, oy = (S - w) // 2 - xs[0] * cell, (S - h) // 2 - ys[0] * cell
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}" shape-rendering="crispEdges">
  <defs>
    <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SHEEN}" stop-opacity="0.05"/>
      <stop offset="1" stop-color="{SHEEN}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect x="{m}" y="{m}" width="{S - 2 * m}" height="{S - 2 * m}" rx="{rad}" fill="{EDGE}"/>
  <rect x="{m + b}" y="{m + b}" width="{S - 2 * m - 2 * b}" height="{S - 2 * m - 2 * b}" rx="{rad - b}" fill="{TILE}"/>
  <rect x="{m + b}" y="{m + b}" width="{S - 2 * m - 2 * b}" height="{S - 2 * m - 2 * b}" rx="{rad - b}" fill="url(#sheen)"/>
{paths(rows, cell, ox, oy)}
</svg>
'''


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    icons = os.path.join(root, 'src-tauri', 'icons')
    G16, G32 = bevel(grid('grid16.txt')), bevel(grid('grid32.txt'))
    with open(os.path.join(icons, 'icon.svg'), 'w') as f:
        f.write(svg(G32))
    for n, suffix in ((16, ''), (32, '@2x')):
        template(G16, n).save(os.path.join(icons, f'trayTemplate{suffix}.png'))
    print('ok')
