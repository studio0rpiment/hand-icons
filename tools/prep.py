import cv2, numpy as np, sys, os, json

import pathlib
REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = str(REPO / "source")
OUT = str(REPO / "build")
os.makedirs(OUT, exist_ok=True)

def flatten(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # divide by a heavy blur to remove paper gradient
    bg = cv2.GaussianBlur(g, (0, 0), 41)
    norm = cv2.divide(g, bg, scale=255)
    return norm

for name in ["IMG_6016", "IMG_6017"]:
    img = cv2.imread(f"{SRC}/{name}.JPG")
    norm = flatten(img)
    # marker ink is well below paper; pencil ghost lines are faint
    _, bw = cv2.threshold(norm, 150, 255, cv2.THRESH_BINARY_INV)
    # remove specks
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    cv2.imwrite(f"{OUT}/{name}_norm.png", norm)
    cv2.imwrite(f"{OUT}/{name}_bw.png", bw)
    print(name, img.shape)
