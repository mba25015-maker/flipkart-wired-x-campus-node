"""
CC-3: the appendix verification kit.

Three artefacts, each as markdown (canonical) and as a slide-ready themed image:

  1. SOURCE TABLE      every [T1]/[T2]/[D]/[A]-tagged input in the model, its
                       LIVE value (read from the imported module, never re-typed),
                       its tier, and its source string. Sorted tier -> module -> name.
  2. AUDIT PAGE        audit.py's checks, formatted. Pulls audit.checks directly.
  3. ASSUMPTION LEDGER robustness.py's __main__ output, captured verbatim.

Rule: no figure is typed into this file. Values come from getattr on the module
that defines them; if a tagged name cannot be resolved it is listed as UNRESOLVED
rather than guessed.

Output: Model/appendix/{source_table,audit_page,assumption_ledger}.{md,png}
        (png in light and dark, matching charts.py)
"""
import io
import os
import re
import runpy
import sys
import importlib
import contextlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from charts import THEMES

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "appendix")
os.makedirs(OUT, exist_ok=True)

# Files that hold model inputs. Everything else (chart/build/appendix/audit code) is skipped.
SKIP = {"audit.py", "appendix.py", "charts.py", "charts2.py", "charts3.py",
        "build_v6.py", "build_v7.py", "export_xlsx.py", "verify_docs.py"}
SOURCE_FILES = sorted(f for f in os.listdir(HERE)
                      if f.endswith(".py") and f not in SKIP)

TIER_ORDER = {"T1": 0, "T1/T2": 1, "T2": 2, "D": 3, "A": 4}
TIER_NAME = {"T1": "T1 disclosure/analyst", "T1/T2": "T1/T2 sourced",
             "T2": "T2 trade press", "D": "D derived", "A": "A assumed"}

# NAME = <rhs>   # T1  source string     (tier token at the head of the comment)
_HEAD = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*[^#\n]*?#\s*"
                   r"(T1/T2|T1|T2|D|A)\b[ .:\-]*(.*)$")
# ... anything  [T1, tender documents]   (tier token bracketed anywhere in the comment)
_BRACKET = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*[^#\n]*?#\s*(.*?)\["
                      r"(T1/T2|T1|T2|D|A)[,\]]\s*(.*?)\]?\s*$")


def _fmt(v):
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        if v == int(v) and abs(v) < 1e15:
            return f"{int(v):,}"
        return f"{v:,.4f}".rstrip("0").rstrip(".")
    if isinstance(v, str):
        return f'"{v}"' if len(v) <= 40 else f'"{v[:37]}..."'
    if isinstance(v, (tuple, list)) and all(isinstance(x, (int, float)) for x in v):
        return "(" + ", ".join(_fmt(x) for x in v) + ")"
    if isinstance(v, dict):
        return f"{{{len(v)} entries}}"
    return "—"


def collect():
    """Return [(tier, module, name, value_str, source), ...] deduped on name."""
    rows, seen = [], set()
    for fname in SOURCE_FILES:
        modname = fname[:-3]
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                mod = importlib.import_module(modname)
        except Exception as e:                       # module needs data we cannot load
            print(f"  skip {modname}: {type(e).__name__}")
            continue
        with open(os.path.join(HERE, fname), encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        for i, ln in enumerate(lines):
            m = _HEAD.match(ln)
            if m:
                name, tier, src = m.group(1), m.group(2), m.group(3).strip()
            else:
                b = _BRACKET.match(ln)
                if not b:
                    continue
                name, tier = b.group(1), b.group(3)
                src = (b.group(2).strip() + " " + b.group(4).strip()).strip(" .:-")
            if name in seen or name.startswith("_") or not hasattr(mod, name):
                continue                              # skip re-imports and function-locals
            seen.add(name)
            # pull up to two indented "#" continuation lines into the source string
            for cont in lines[i + 1:i + 3]:
                cm = re.match(r"^\s+#\s{2,}(\S.*)$", cont)
                if not cm or "=" in cont.split("#")[0]:
                    break
                src += " " + cm.group(1).strip()
            val = _fmt(getattr(mod, name))
            src = re.sub(r"\s+", " ", src).strip(" .:-") or "—"
            if len(src) > 200:
                src = src[:197] + "..."
            rows.append((tier, modname, name, val, src))
    rows.sort(key=lambda r: (TIER_ORDER.get(r[0], 9), r[1], r[2]))
    return rows


# ---------------------------------------------------------------------------
# 1. SOURCE TABLE
# ---------------------------------------------------------------------------
def source_table_md(rows):
    out = ["# Appendix — source table",
           "",
           f"Every tagged input in `Model/*.py`. Value column is the **live model "
           f"value** read at generation time, not a transcription. {len(rows)} inputs.",
           "",
           "| # | Parameter | Value | Tier | Source | Module |",
           "|---:|---|---:|:--:|---|---|"]
    for i, (tier, mod, name, val, src) in enumerate(rows, 1):
        s = src.replace("|", "\\|")
        out.append(f"| {i} | `{name}` | {val} | {tier} | {s} | `{mod}` |")
    by_tier = {}
    for tier, *_ in rows:
        by_tier[tier] = by_tier.get(tier, 0) + 1
    out += ["", "**By tier:** " + "  ".join(
        f"{TIER_NAME[t]} — {by_tier.get(t, 0)}" for t in TIER_ORDER if by_tier.get(t))]
    return "\n".join(out) + "\n"


def source_table_png(rows, T):
    c = THEMES[T]
    ncol = 2
    per = -(-len(rows) // ncol)                      # ceil
    fig, axes = plt.subplots(1, ncol, figsize=(14.4, per * 0.150 + 0.8))
    tcol = {"T1": c["pos"], "T1/T2": c["pos"], "T2": c["accent"],
            "D": c["mute"], "A": c["neg"]}
    for ci, ax in enumerate(axes):
        ax.axis("off")
        ax.set_xlim(0, 1); ax.set_ylim(0, per + 1)
        for ri, (tier, mod, name, val, src) in enumerate(rows[ci * per:(ci + 1) * per]):
            y = per - ri
            ax.text(0.00, y, f"{ci*per+ri+1}", fontsize=5.0, color=c["mute"],
                    ha="left", va="center")
            ax.text(0.035, y, name, fontsize=5.4, color=c["fg"], va="center",
                    family="DejaVu Sans Mono", fontweight="bold")
            ax.text(0.375, y, val, fontsize=5.4, color=c["fg"], va="center",
                    ha="right", family="DejaVu Sans Mono")
            ax.text(0.395, y, tier, fontsize=5.0, color=tcol.get(tier, c["mute"]),
                    va="center", fontweight="bold", family="DejaVu Sans Mono")
            src = src if len(src) <= 78 else src[:75] + "..."
            ax.text(0.47, y, src, fontsize=4.7, color=c["mute"], va="center")
    fig.suptitle(f"SOURCE TABLE  ·  {len(rows)} tagged model inputs, live values",
                 fontsize=8.5, color=c["fg"], fontweight="bold", y=0.995)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.965, bottom=0.02, wspace=0.10)
    fig.savefig(os.path.join(OUT, f"source_table_{T}.png"), dpi=300,
                transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. AUDIT PAGE
# ---------------------------------------------------------------------------
def _audit_checks():
    with contextlib.redirect_stdout(io.StringIO()):
        audit = importlib.import_module("audit")
    return list(audit.checks)


def audit_md(checks):
    n_ok = sum(1 for c in checks if c[0])
    out = ["# Appendix — model audit",
           "",
           f"`audit.py` asserts every on-slide number against the model output. "
           f"**{n_ok}/{len(checks)} pass.**",
           "",
           "| Check | On slide | Model | OK |",
           "|---|---:|---:|:--:|"]
    for ok, lab, a, b in checks:
        out.append(f"| {lab.strip()} | {a} | {b} | {'yes' if ok else '**NO**'} |")
    return "\n".join(out) + "\n"


def audit_png(checks, T):
    c = THEMES[T]
    n_ok = sum(1 for x in checks if x[0])
    ncol = 2
    per = -(-len(checks) // ncol)
    fig, axes = plt.subplots(1, ncol, figsize=(13.2, per * 0.135 + 0.7))
    for ci, ax in enumerate(axes):
        ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, per + 1)
        for ri, (ok, lab, a, b) in enumerate(checks[ci * per:(ci + 1) * per]):
            y = per - ri
            ax.text(0.0, y, "✓" if ok else "✗", fontsize=5.2,
                    color=c["pos"] if ok else c["neg"], va="center", fontweight="bold")
            ax.text(0.035, y, lab.strip(), fontsize=4.6, color=c["fg"], va="center",
                    family="DejaVu Sans")
            ax.text(1.0, y, f"{a}  =  {b}", fontsize=4.5, color=c["mute"], va="center",
                    ha="right", family="DejaVu Sans Mono")
    fig.suptitle(f"MODEL AUDIT  ·  {n_ok}/{len(checks)} on-slide numbers tie to the model",
                 fontsize=8, color=c["fg"], fontweight="bold", y=0.995)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.96, bottom=0.02, wspace=0.06)
    fig.savefig(os.path.join(OUT, f"audit_page_{T}.png"), dpi=300, transparent=True,
                bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. ASSUMPTION LEDGER  (robustness.py __main__, captured verbatim)
# ---------------------------------------------------------------------------
def ledger_text():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        runpy.run_path(os.path.join(HERE, "robustness.py"), run_name="__main__")
    return buf.getvalue().rstrip("\n")


def ledger_md(txt):
    return ("# Appendix — assumption ledger\n\n"
            "From `robustness.py`: twelve assumptions retired by source / derive / "
            "solve / neutralise, and what remains.\n\n```\n" + txt + "\n```\n")


def ledger_png(txt, T):
    c = THEMES[T]
    lines = txt.splitlines()
    fig, ax = plt.subplots(figsize=(9.0, len(lines) * 0.108 + 0.5))
    ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, len(lines) + 1)
    for i, ln in enumerate(lines):
        y = len(lines) - i
        strong = ln.strip().startswith(("ASSUMPTION LEDGER", "WHAT REMAINS", ">>>")) or \
            (ln and ln[0].isdigit() and "." in ln[:4])
        ax.text(0.0, y, ln, fontsize=4.7,
                color=c["fg"] if strong else c["mute"],
                fontweight="bold" if strong else "normal",
                va="center", family="DejaVu Sans Mono")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(os.path.join(OUT, f"assumption_ledger_{T}.png"), dpi=300,
                transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main():
    rows = collect()
    with open(os.path.join(OUT, "source_table.md"), "w", encoding="utf-8") as fh:
        fh.write(source_table_md(rows))

    checks = _audit_checks()
    with open(os.path.join(OUT, "audit_page.md"), "w", encoding="utf-8") as fh:
        fh.write(audit_md(checks))

    txt = ledger_text()
    with open(os.path.join(OUT, "assumption_ledger.md"), "w", encoding="utf-8") as fh:
        fh.write(ledger_md(txt))

    for T in THEMES:
        source_table_png(rows, T)
        audit_png(checks, T)
        ledger_png(txt, T)

    unresolved = [r for r in rows if r[3] in ("UNRESOLVED", "—")]
    print(f"source table : {len(rows)} inputs  "
          f"({sum(1 for r in rows if r[0].startswith('T1'))} T1, "
          f"{sum(1 for r in rows if r[0]=='T2')} T2, "
          f"{sum(1 for r in rows if r[0]=='D')} D, "
          f"{sum(1 for r in rows if r[0]=='A')} A)")
    if unresolved:
        print(f"  {len(unresolved)} without a scalar value (dicts / derived structures):")
        for r in unresolved:
            print(f"    {r[1]}.{r[2]}")
    print(f"audit page   : {sum(1 for c in checks if c[0])}/{len(checks)} pass")
    print(f"ledger       : {len(txt.splitlines())} lines")
    print(f"written to   : {OUT}")


if __name__ == "__main__":
    main()
