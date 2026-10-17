import cv2, numpy as np, os
from icons import ICONS, ERASE, NUMBER, DIRECTIONS

import pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
W = str(REPO / "build")
os.makedirs(f"{W}/crops", exist_ok=True)

pages = {}
for p in ["IMG_6016", "IMG_6017"]:
    bw = cv2.imread(f"{W}/{p}_bw.png", 0)
    for (a, b, c, d, t) in ERASE.get(p, []):
        cv2.line(bw, (a, b), (c, d), 0, t)
    pages[p] = bw

SIZE = 1024   # square canvas
PAD = 0.12   # fraction of canvas kept clear around the ink
tiles = []
for name, (p, x0, y0, x1, y1) in ICONS.items():
    crop = pages[p][y0:y1, x0:x1]
    # drop any component that touches the crop border (neighbor spill-over)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(crop, 8)
    keep = np.zeros_like(crop)
    amax = stats[1:, 4].max() if n > 1 else 0
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a < 40:
            continue
        touches = x == 0 or y == 0 or x + w == crop.shape[1] or y + h == crop.shape[0]
        if touches and a < 0.03 * amax:   # small spill from a neighbour
            print("  dropped", name, (x, y, w, h, a))
            continue
        keep[lab == i] = 255
    ys, xs = np.where(keep > 0)
    if len(xs) == 0:
        print("EMPTY", name); continue
    keep = keep[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = keep.shape
    # 45° rotations need the diagonal to fit: pad so the ink's bounding square stays inside the canvas
    pad = 0.16 if DIRECTIONS.get(name) in ("rotate45", "rotate-sym") else PAD
    inner = int(SIZE * (1 - 2 * pad))
    s = inner / max(h, w)
    rs = cv2.resize(keep, (max(1, int(w * s)), max(1, int(h * s))), interpolation=cv2.INTER_AREA)
    canvas = np.zeros((SIZE, SIZE), np.uint8)
    oy, ox = (SIZE - rs.shape[0]) // 2, (SIZE - rs.shape[1]) // 2
    canvas[oy:oy + rs.shape[0], ox:ox + rs.shape[1]] = rs
    cv2.imwrite(f"{W}/crops/{NUMBER[name]:02d}-{name}.png", canvas)
    tiles.append((name, canvas))

# contact sheet
cols = 6
T = 220
rows = (len(tiles) + cols - 1) // cols
sheet = np.full((rows * (T + 30), cols * T, 3), 255, np.uint8)
for i, (name, c) in enumerate(tiles):
    r, k = divmod(i, cols)
    small = cv2.resize(255 - c, (T - 10, T - 10), interpolation=cv2.INTER_AREA)
    y, x = r * (T + 30), k * T
    sheet[y:y + T - 10, x + 5:x + T - 5] = cv2.cvtColor(small, cv2.COLOR_GRAY2BGR)
    cv2.putText(sheet, f"{i+1} {name}", (x + 5, y + T + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (60, 60, 60), 1, cv2.LINE_AA)
cv2.imwrite(f"{W}/contact.png", sheet)
print(len(tiles), "icons")
