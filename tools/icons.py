# name: (page, x0, y0, x1, y1) in full-res pixels
ICONS = {
    "arrow-bar":        ("IMG_6016", 190, 140, 380, 320),
    "star-scribble":    ("IMG_6016", 170, 360, 430, 590),
    "blob":             ("IMG_6016", 160, 595, 440, 880),
    "cross":            ("IMG_6016", 180, 910, 450, 1270),
    "slash":            ("IMG_6016", 220, 1300, 390, 1630),
    "dash":             ("IMG_6016", 103, 1880, 290, 1990),
    "bolt":             ("IMG_6016", 630, 190, 910, 530),
    "spiral-loose":     ("IMG_6016", 620, 570, 1030, 930),
    "triangle-y":       ("IMG_6016", 680, 950, 930, 1280),
    "triangle-a":       ("IMG_6016", 650, 1280, 910, 1660),
    "line-solid":       ("IMG_6016", 720, 1690, 810, 2150),
    "triangle-b":       ("IMG_6016", 980, 1290, 1240, 1660),
    "line-dashed":      ("IMG_6016", 1080, 1690, 1160, 2150),
    "dumbbell":         ("IMG_6016", 1330, 1680, 1510, 2140),
    "hatch-fine":       ("IMG_6016", 1120, 200, 1490, 570),
    "hatch-heavy":      ("IMG_6016", 1110, 600, 1480, 930),
    "burst-a":          ("IMG_6016", 1010, 932, 1540, 1265),

    "square-x":         ("IMG_6017", 150, 330, 480, 690),
    "hourglass-x":      ("IMG_6017", 600, 360, 930, 700),
    "big-x":            ("IMG_6017", 1050, 330, 1460, 700),
    "bolt-small":       ("IMG_6017", 120, 840, 385, 1030),
    "equals":           ("IMG_6017", 660, 930, 880, 1050),
    "scatter":          ("IMG_6017", 1080, 860, 1390, 1090),
    "strokes":          ("IMG_6017", 140, 1190, 430, 1480),
    "spiral-tight":     ("IMG_6017", 570, 1100, 970, 1520),
    "horizon":          ("IMG_6017", 965, 1210, 1590, 1440),
    "burst-b":          ("IMG_6017", 1140, 1460, 1500, 2010),
    "ear":              ("IMG_6017", 80, 1500, 440, 2000),
    "c-spiral":         ("IMG_6017", 580, 1550, 900, 1930),
}

# polygons (full-res, per page) painted white before cropping: strokes to drop
# (x0,y0,x1,y1,thickness) line segments painted white: strokes to drop
ERASE = {
    "IMG_6016": [
        # diagonal line framing the bottom of burst-a
        (935, 1080, 1325, 1425, 90),
    ],
}

S = 1.17
ICONS = {k: (p, int(x0*S), int(y0*S), int(x1*S), int(y1*S)) for k,(p,x0,y0,x1,y1) in ICONS.items()}
ERASE = {p: [(int(a*S), int(b*S), int(c*S), int(d*S), t) for a,b,c,d,t in segs] for p,segs in ERASE.items()}

# stable numbering = order above (page 1 then page 2); new icons get appended, numbers never shift
NUMBER = {name: i + 1 for i, name in enumerate(ICONS)}
# closed shapes whose interiors get filled solid in the "filled" variant
# name -> gap (px at 1024) to bridge in the drawn outline before filling
FILL = {"star-scribble": 81, "bolt": 141, "blob": 41, "triangle-y": 41, "triangle-a": 41, "triangle-b": 121, "dumbbell": 41}

# directional icons: "rotate" -> r90/r180/r270 (clockwise) alongside the original,
# "mirror" -> mh/mv/mhv (flip horizontal / vertical / both) for shapes whose
# direction is a handedness (spirals) rather than a heading
DIRECTIONS = {
    "arrow-bar": "rotate", "bolt": "rotate", "bolt-small": "rotate",
    # lines with no head/tail read the same at 180°, so: 0, 90, then 45, 135
    "slash": "rotate-sym", "strokes": "rotate-sym", "hatch-fine": "rotate-sym", "hatch-heavy": "rotate-sym",
    "line-solid": "rotate-sym", "line-dashed": "rotate-sym", "dash": "rotate-sym", "equals": "rotate-sym",
    "triangle-y": "rotate", "triangle-a": "rotate", "triangle-b": "rotate",
    "dumbbell": "rotate", "horizon": "rotate",
    "c-spiral": "rotate", "ear": "rotate",
    "spiral-loose": "mirror", "spiral-tight": "mirror",
    # stars: r45/r90/r135 (quarter-turn would nearly repeat them)
    "star-scribble": "rotate45", "burst-a": "rotate45", "burst-b": "rotate45", "scatter": "rotate45",
    "big-x": "rotate45", "hourglass-x": "rotate45", "square-x": "rotate45",
    "blob": "rotate45",
}

# kind -> icons (order within a kind is the library order). Numbers stay as they are.
KINDS = {
    "lines":     ["line-solid", "line-dashed", "slash", "dash", "equals", "horizon", "cross", "strokes", "hatch-fine", "hatch-heavy"],
    "arrows":    ["arrow-bar", "bolt", "bolt-small"],
    "swirls":    ["spiral-tight", "spiral-loose", "c-spiral", "ear"],
    "triangles": ["triangle-a", "triangle-b", "triangle-y"],
    "stars":     ["star-scribble", "burst-a", "burst-b", "scatter", "big-x", "hourglass-x", "square-x"],
    "blobs":     ["blob", "dumbbell"],
}
KIND = {n: k for k, ns in KINDS.items() for n in ns}
assert set(KIND) == set(ICONS), set(ICONS) ^ set(KIND)
