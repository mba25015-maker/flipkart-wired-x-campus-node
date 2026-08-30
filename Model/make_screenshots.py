"""
REGENERATE THE TERMINAL SCREENSHOTS ON A-1 FROM A REAL RUN.

The two images on slide 11 were captured when audit.py ran 311 checks and verify_deck ran 80.
They kept showing 311/311 and 80/80 while the tiles beside them said 336 and 116 - on the page  # scan:allow
whose entire argument is that nothing drifts. An image is as capable of going stale as a
literal, and it is harder to notice because no assertion reads pixels.

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

def grab(script, out, keep=None, head=14, width=1180):
    """Capture a module's live stdout. `keep` filters to the lines that carry the argument."""
    lines = capture(script)
    if keep:
        lines = [l for l in lines if any(k in l for k in keep)] or lines
    lines = [l for l in lines if l.strip()][:head]
    shot([f"$ python3 Model/{script}"] + lines, os.path.join(OUT, out), w=width)

if __name__ == "__main__":
    # ALL SIX ARE GENERATED. Four of them (S3-S6) were captured on 29 Aug 12:35 and never
    # refreshed, so they kept showing the pre-correction model - campus AOV Rs580 on the solver  # scan:allow
    # panel, the old ROCE ladder, the old district screen - under slides whose text had moved on.
    # An image is the one thing on a slide that no assertion can read, which makes hand-captured
    # screenshots the most reliable place in a package for a stale number to survive.
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

    grab("solver.py",          "S3_solver_repurpose.png",
         keep=("minimise","subject","burn","Repurpose","Hold","Wind","Rs","OPTIM","threshold"), head=15)
    grab("roce.py",            "S4_roce_hurdle.png",
         keep=("Capital employed","AOV for","ROCE","hurdle","DuPont","margin","turnover","payback","IRR"), head=15, width=1080)
    grab("aishe_district.py",  "S5_aishe_districts.png",
         keep=("Register","districts","candidates","uncontested","contested","stacked","screen"), head=13)
    grab("basket.py",          "S6_basket_regression.png",
         keep=("Target","Starting","Gap","non-grocery","R2","AOV =","ladder","reach"), head=13)
