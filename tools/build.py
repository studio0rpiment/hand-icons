"""Rebuild everything from source/ photos: python tools/build.py
Needs: opencv-python, numpy, potracer, cairosvg (pip install -r tools/requirements.txt)"""
import pathlib, runpy, shutil, sys
T = pathlib.Path(__file__).resolve().parent
R = T.parent
sys.path.insert(0, str(T))
for step in ["prep", "split", "vectorize", "build_lib", "build_catalog"]:
    print(f"== {step}")
    runpy.run_path(str(T / f"{step}.py"), run_name="__main__")
B = R / "build"
for f in ["hand-icons.svg", "hand-icons.css", "hand-icons.json"]:
    shutil.copy(B / "lib" / f, R / "dist" / f)
for f in (B / "lib" / "react").iterdir():
    shutil.copy(f, R / "src" / "react" / f.name)
shutil.copy(B / "lib" / "catalog-standalone.html", R / "docs" / "index.html")
shutil.copy(B / "icons" / "library-sheet.png", R / "docs" / "library-sheet.png")
shutil.rmtree(R / "svg", ignore_errors=True)
for kind in (B / "icons").iterdir():
    if not (kind / "svg").is_dir():
        continue
    for mode, out in [("outline", "line"), ("filled", "fill")]:
        dst = R / "svg" / kind.name / out
        dst.mkdir(parents=True)
        for f in (kind / "svg" / mode).glob("??-*.svg"):
            stem = f.stem
            if "-r" in stem[3:] and stem.rsplit("-", 1)[1] in ("r45", "r90", "r135", "r180", "r270", "mh", "mv", "mhv"):
                continue  # directions live in the sprite and the release zip
            shutil.copy(f, dst / f.name)
# release zip: every variant/direction as svg + png
shutil.make_archive(str(R / "build" / "hand-icons-export"), "zip", B / "icons")
print("done →", R / "dist", R / "docs", R / "svg", B / "hand-icons-export.zip")
