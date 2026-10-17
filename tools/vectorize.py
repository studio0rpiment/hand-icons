import cv2, numpy as np, os, glob, json
import potrace, cairosvg
from icons import FILL, NUMBER, DIRECTIONS, KINDS, KIND

import pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
W = str(REPO / "build")
OUT = str(REPO / "build" / "icons")
VARIANTS = ["filled", "outline"]
COLORS = {"black": "#000000", "white": "#ffffff"}
SIZES = [512, 128]
for kind in KINDS:
    for v in VARIANTS:
        os.makedirs(f"{OUT}/{kind}/svg/{v}", exist_ok=True)
        for c in COLORS:
            os.makedirs(f"{OUT}/{kind}/png/{v}-{c}", exist_ok=True)

VIEW = 1024      # canvas the crops were made on
STROKE = 6       # outline stroke width in viewBox units (~0.6% of canvas)
MIN_HOLE = 150   # marker-dropout holes smaller than this (px² at 1024) are filled

def fill_holes(bw, max_area=None):
    """Fill enclosed background regions. max_area=None fills every hole (solid shape)."""
    inv = (bw == 0).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(inv, 4)
    out = bw.copy()
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        touches = x == 0 or y == 0 or x + w == bw.shape[1] or y + h == bw.shape[0]
        if touches:
            continue  # outside background
        if max_area is None or a < max_area:
            out[lab == i] = 255
    return out

def trace(bitmap):
    bm = potrace.Bitmap(bitmap == 0)   # potracer: False = ink
    path = bm.trace(turdsize=8, alphamax=0.8, opticurve=True, opttolerance=0.2)
    d = []
    for curve in path:
        s = curve.start_point
        d.append(f"M{s.x:.1f} {s.y:.1f}")
        for seg in curve:
            if seg.is_corner:
                c, e = seg.c, seg.end_point
                d.append(f"L{c.x:.1f} {c.y:.1f}L{e.x:.1f} {e.y:.1f}")
            else:
                c1, c2, e = seg.c1, seg.c2, seg.end_point
                d.append(f"C{c1.x:.1f} {c1.y:.1f} {c2.x:.1f} {c2.y:.1f} {e.x:.1f} {e.y:.1f}")
        d.append("Z")
    return "".join(d)

C = VIEW / 2
TRANSFORMS = {
    "": "", "r45": f"rotate(45 {C} {C})", "r135": f"rotate(135 {C} {C})", "r90": f"rotate(90 {C} {C})", "r180": f"rotate(180 {C} {C})", "r270": f"rotate(270 {C} {C})",
    "mh": f"translate({VIEW} 0) scale(-1 1)", "mv": f"translate(0 {VIEW}) scale(1 -1)",
    "mhv": f"translate({VIEW} {VIEW}) scale(-1 -1)",
}
def variants_for(name):
    d = DIRECTIONS.get(name)
    return [""] + ({"rotate": ["r90", "r180", "r270"], "rotate45": ["r90", "r45", "r135"], "rotate-sym": ["r90", "r45", "r135"], "mirror": ["mh", "mv", "mhv"]}.get(d, []))

def svg(d, mode, color="currentColor", direction=""):
    tf = f' transform="{TRANSFORMS[direction]}"' if direction else ""
    if mode == "line-solid":
        # d is (fill_path, ink_path). Fill colour via CSS --icon-fill; falls back to a 35% tint.
        fill_d, ink_d = d
        fc = "var(--icon-fill, currentColor)" if color == "currentColor" else color
        fo = ' fill-opacity="var(--icon-fill-opacity, 0.35)"' if color == "currentColor" else ' fill-opacity="0.35"'
        body = (f'<g{tf}><path class="fill" d="{fill_d}" fill="{fc}"{fo} fill-rule="evenodd"/>'
                f'<path class="line" d="{ink_d}" fill="{color}" fill-rule="evenodd"/></g>')
    elif mode == "filled":
        body = f'<path d="{d}" fill="{color}" fill-rule="evenodd"{tf}/>'
    else:
        body = (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{STROKE}" '
                f'stroke-linejoin="round" stroke-linecap="round"{tf}/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VIEW} {VIEW}" '
            f'width="{VIEW}" height="{VIEW}">{body}</svg>')

index = []
for f in sorted(glob.glob(f"{W}/crops/*.png")):
    stem = os.path.splitext(os.path.basename(f))[0]      # e.g. 03-blob
    name = stem.split("-", 1)[1]
    bw = cv2.imread(f, 0)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    bw = fill_holes(bw, MIN_HOLE)
    if name in FILL:
        # bridge small gaps in the drawn outline so the interior reads as enclosed,
        # then keep the original ink plus the enclosed interior
        bridged = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (FILL[name], FILL[name])))
        solid = cv2.bitwise_or(bw, fill_holes(bridged))
    else:
        solid = bw
    paths = {"filled": trace(solid), "outline": trace(bw)}
    paths["line-solid"] = (paths["filled"], paths["outline"])
    for direction in variants_for(name):
        fstem = f"{stem}-{direction}" if direction else stem
        for mode in VARIANTS:
            if mode == "line-solid" and name not in FILL:
                continue
            # SVG uses currentColor so it follows CSS `color` — set color:#fff to invert
            open(f"{OUT}/{KIND[name]}/svg/{mode}/{fstem}.svg", "w").write(svg(paths[mode], mode, direction=direction))
            for cname, hexc in COLORS.items():
                s = svg(paths[mode], mode, hexc, direction)
                for px in SIZES:
                    cairosvg.svg2png(bytestring=s.encode(), output_width=px, output_height=px,
                                     write_to=f"{OUT}/{KIND[name]}/png/{mode}-{cname}/{fstem}-{px}.png")
    index.append({"number": NUMBER[name], "name": name, "kind": KIND[name], "file": stem, "solid": name in FILL,
                  "directions": variants_for(name)})

order = {n: i for i, n in enumerate(n for ns in KINDS.values() for n in ns)}
index.sort(key=lambda e: order[e["name"]])
json.dump(index, open(f"{OUT}/index.json", "w"), indent=1)
with open(f"{OUT}/README.md", "w") as r:
    r.write("# Hand-drawn icons\n\nNumbers are stable: new icons are appended, existing numbers never change.\n\n")
    r.write("Folders are grouped by kind: `lines/`, `arrows/`, `swirls/`, `triangles/`, `stars/`, `blobs/`. Inside each:\n\n")
    r.write("- `svg/filled`, `svg/outline` — vector, drawn in `currentColor`; set CSS `color` to recolour or invert.\n")
    r.write("- `png/<variant>-black`, `png/<variant>-white` — transparent PNGs at 512 and 128 px.\n")
    r.write("- *filled*: closed shapes solid (marked below), open strokes as drawn. *outline*: hollow trace of the ink.\n")
    r.write("\n")
    r.write("- Directional icons also come as `-r90`, `-r180`, `-r270` (rotated clockwise) `-r45`, `-r90`, `-r135` for the stars, blob and symmetric lines, or `-mh`, `-mv`, `-mhv` (mirrored horizontally / vertically / both). The unsuffixed file is as drawn.\n\n")
    r.write("| # | kind | name | solid fill | directions |\n|---|---|---|---|---|\n")
    for e in index:
        r.write(f"| {e['number']:02d} | {e['kind']} | {e['name']} | {'yes' if e['solid'] else ''} | {' '.join(e['directions'][1:])} |\n")

# library sheet: four sections side by side — dark line | dark fill | light line | light fill
# one row per icon, a tile per direction
T = 104
maxd = max(len(e["directions"]) for e in index)
SECTIONS = [("dark line", "outline-black", 255), ("dark fill", "filled-black", 255),
            ("light line", "outline-white", 30), ("light fill", "filled-white", 30)]
LAB = 150
secw = LAB + maxd * T
KH = 34  # kind header height
rows = []  # ("kind", name) or ("icon", entry)
for kind, ns in KINDS.items():
    rows.append(("kind", kind))
    rows += [("icon", e) for e in index if e["kind"] == kind]
H = 40 + sum(KH if r[0] == "kind" else T for r in rows)
sheet = np.full((H, len(SECTIONS) * secw, 3), 255, np.uint8)
def comp(path, bg):
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    a = im[:, :, 3:4].astype(np.float32) / 255.0
    out = im[:, :, :3].astype(np.float32) * a + bg * (1 - a)
    return cv2.resize(out.astype(np.uint8), (T - 6, T - 6), interpolation=cv2.INTER_AREA)
for s, (title, folder, bg) in enumerate(SECTIONS):
    x0 = s * secw
    sheet[:, x0:x0 + secw] = bg
    fg = (40, 40, 40) if bg == 255 else (220, 220, 220)
    cv2.putText(sheet, title.upper(), (x0 + 8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, fg, 2, cv2.LINE_AA)
    y = 40
    for r in rows:
        if r[0] == "kind":
            cv2.putText(sheet, r[1].upper(), (x0 + 8, y + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, fg, 2, cv2.LINE_AA)
            cv2.line(sheet, (x0 + 8, y + 30), (x0 + secw - 12, y + 30), (128, 128, 128), 1)
            y += KH
            continue
        e = r[1]
        cv2.putText(sheet, f"{e['number']:02d} {e['name']}", (x0 + 8, y + T // 2 + 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, fg, 1, cv2.LINE_AA)
        for j, dname in enumerate(e["directions"]):
            f = e["file"] + (f"-{dname}" if dname else "")
            x = x0 + LAB + j * T
            sheet[y + 3:y + T - 3, x + 3:x + T - 3] = comp(f"{OUT}/{e['kind']}/png/{folder}/{f}-512.png", bg)
            if dname:
                cv2.putText(sheet, dname, (x + 5, y + T - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (128, 128, 128), 1, cv2.LINE_AA)
        y += T
    cv2.line(sheet, (x0 + secw - 1, 0), (x0 + secw - 1, H), (128, 128, 128), 2)
cv2.imwrite(f"{OUT}/library-sheet.png", sheet)
print("sheet", sheet.shape)
