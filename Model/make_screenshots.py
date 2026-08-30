"""
REGENERATE ALL SIX PUBLICATION SCREENSHOTS FROM REAL RUNS.

The appendix images are generated from the same scripts that the public notebooks execute.
This prevents audit counts, model outputs, and narrative labels from drifting independently.

So the images are now GENERATED from the live command output, and verify_deck bans the stale
strings from the deck text. Run this AFTER release.py step 2, so the output being photographed
is the output of the run that is about to be stamped.
"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT  = os.path.join(HERE, "assets", "screenshots")

BG, FG, DIM, OK_, HI = (13, 22, 41), (222, 232, 248), (128, 146, 175), (110, 214, 160), (255, 194, 32)
def _font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
              "/System/Library/Fonts/Menlo.ttc", "/Library/Fonts/Courier New.ttf"):
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

def shot(lines, path, w=1180, pad=22, sz=17, lh=25):
    img = Image.new("RGB", (w, pad*2 + lh*len(lines) + 34), BG)
    d = ImageDraw.Draw(img); f = _font(sz)
    for i, col in enumerate(((240,95,85), (245,190,80), (110,214,160))):
        d.ellipse([22+i*20, 15, 32+i*20, 25], fill=col)
    d.line([0, 36, w, 36], fill=(38, 52, 78))
    y = 48
    for ln in lines:
        col = FG
        if ln.startswith("$"): col = HI
        elif " PASS " in ln or ln.strip().startswith("PASS") or "pass" in ln or "tie out" in ln: col = OK_
        elif ln.startswith("  ") and not ln.strip(): col = DIM
        elif "FAIL" in ln: col = (240, 120, 110)
        elif ln.startswith("=") or ln.startswith("-"): col = DIM
        d.text((26, y), ln[:96], font=f, fill=col); y += lh
    os.makedirs(OUT, exist_ok=True)
    img.save(path); print("  wrote", os.path.relpath(path, ROOT), img.size)

def capture(script):
    r = subprocess.run([sys.executable, os.path.join(HERE, script)],
                       capture_output=True, text=True, cwd=ROOT)
    return r.stdout.strip().split("\n")

def first(lines, n):
    """Keep a terminal capture legible while preserving the headline result."""
    return lines[:n] + (["  ... output continues in the linked notebook"] if len(lines) > n else [])

if __name__ == "__main__":
    a = capture("audit.py")
    head = [l for l in a if l.strip().startswith(("OK", "FAIL"))]
    tail = [l for l in a if "checks pass" in l]
    shot(["$ python3 Model/audit.py"] + head[:7] + ["  ..."] + head[-4:] + [""] + tail,
         os.path.join(OUT, "S1_audit.png"))

    d = capture("verify_deck.py")
    dh = [l for l in d if l.strip().startswith(("OK", "FAIL"))]
    dt = [l for l in d if "deck checks" in l]
    shot(["$ python3 Model/verify_deck.py"] + dh[:5] + ["  ..."] + dh[-3:] + [""] + dt,
         os.path.join(OUT, "S2_deck.png"))

    shot(["$ python3 Model/solver.py"] + first(capture("solver.py"), 33),
         os.path.join(OUT, "S3_solver_repurpose.png"), w=1680, sz=14, lh=20)

    shot(["$ python3 Model/roce.py"] + first(capture("roce.py"), 55),
         os.path.join(OUT, "S4_roce_hurdle.png"), w=1680, sz=15, lh=22)

    shot(["$ python3 Model/aishe_district.py"] + first(capture("aishe_district.py"), 32),
         os.path.join(OUT, "S5_aishe_districts.png"), w=1680, sz=14, lh=20)

    shot(["$ python3 Model/basket.py"] + first(capture("basket.py"), 35),
         os.path.join(OUT, "S6_basket_regression.png"), w=1680, sz=14, lh=20)
