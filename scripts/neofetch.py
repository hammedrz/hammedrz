#!/usr/bin/env python3
"""Generate the neofetch-style profile card (assets/neofetch-{dark,light}.svg).

Stdlib only. Edit INFO or ART below and re-run:  python3 scripts/neofetch.py
Every glyph gets an explicit x position, so the layout holds whatever
monospace font the viewer's browser falls back to.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent

USER, HOST = "hamed", "github"

# (key, value) rows. A value may be a list of (text, css_class) segments.
INFO = [
    ("OS", "Med student who codes"),
    ("Host", "Tehran, Iran"),
    ("Kernel", "Linux · GNOME on Wayland"),
    ("Startup", [("Medalak", "hl"), (" · AI fact-checks for health claims", "")]),
    ("Focus", "Linux · AI · Medical AI · tools for me"),
    ("Lang", [("Python", "hl"), ("  (a lot of it)", "cm")]),
    ("Frameworks", "Django · PySide6 / Qt"),
    ("AI / ML", "PyTorch · TensorFlow · Hugging Face"),
    ("LLMs", "LangChain · vLLM · local models · APIs"),
    ("Runtime", [("docker compose up -d", "hl"), ("  # for everything", "cm")]),
    ("Infra", "Linux servers · PostgreSQL · SQLite · CI"),
    ("Bots", "Telegram · Bot API + MTProto"),
    ("Shell", "zsh"),
    ("Memory", "anatomy flashcards + man pages"),
]

# A boy with glasses sitting behind a Surface Pro, seen slightly from the side:
# the tablet stands to his right showing its back (Tux sticker, hinge seam and
# the kickstand blade swung out to the desk), with a Bluetooth keyboard and a
# cable-free mouse.
ART = r"""
   ,;;;;;;;,
  ,;;;;;;;;;;;,
  ;;;;;;;;;;;;;
  ;;''''''''';;
 (_|[ o]-[ o]|
   |      J  |  .-------------.
    \  '-'  /   |             |
     '-----'    |-------------|\
  _.-'\___/'-._ |    (o<      | \
 /     | |      |    //\      |  \
/   /  ' '      |    V_/_     |   \
|  |[][][][][][]'-------------'    \ .-.
========================================
""".strip("\n").split("\n")


def art_class(r, c, ch):
    """Colour region of one art glyph."""
    if r == len(ART) - 1:                          # desk
        return "desk"
    if c >= 37:                                    # mouse
        return "srf"
    if c >= 15 and r >= 5:                         # Surface back
        if c >= 31 or (r == 7 and ch == "-"):      # kickstand blade + hinge seam
            return "kick"
        if 8 <= r <= 10 and 20 <= c <= 25:
            return "tux"
        return "srf"
    if r <= 3:
        return "hair"
    if r == 4 and ch == "o":
        return "eye"
    if r == 4 and ch in "[]-":
        return "gl"
    if r <= 7:
        return "face"
    if r == 11 and ch in "[]":                     # keyboard
        return "srf"
    return "hood"


THEMES = {
    "dark": dict(
        card="#161b22", bar="#1f2630", border="#30363d", btn="#2d343e",
        fg="#c9d1d9", muted="#7d8590", key="#ff6b8b", accent="#7ee0c3",
        hair="#c08a5e", hoodie="#ff6b8b", surface="#a3b1c2", tux="#e3b341",
        blocks=["#484f58", "#ff7b72", "#7ee787", "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", "#c9d1d9",
                "#6e7681", "#ffa198", "#aff5b4", "#f8e3a1", "#a5d6ff", "#e2c5ff", "#b3f0ff", "#ffffff"],
    ),
    "light": dict(
        card="#ffffff", bar="#f3f4f6", border="#d0d7de", btn="#e4e7eb",
        fg="#1f2328", muted="#656d76", key="#c8234d", accent="#0b7d5f",
        hair="#7a4e2d", hoodie="#c8234d", surface="#57606a", tux="#9a6700",
        blocks=["#24292f", "#cf222e", "#116329", "#9a6700", "#0969da", "#8250df", "#1b7c83", "#6e7781",
                "#57606a", "#a40e26", "#1a7f37", "#bf8700", "#218bff", "#a475f9", "#3192aa", "#8c959f"],
    ),
}

W, H = 860, 528
CW, LH, FS = 8.4, 21, 14          # info column: char advance, line height, font size
ACW, ALH, AFS = 7.6, 16.6, 12.6   # ascii art: char advance, line height, font size
ART_X, INFO_X, KEY_COLS = 34, 360, 12
TOP = 40                           # title bar height
PROMPT_Y = TOP + 32
ROW0 = PROMPT_Y + 30               # first info baseline


def glyph_text(s, x0, y, cls="", cw=CW):
    """A <text> whose glyphs are each pinned to x0 + i*cw (spaces dropped)."""
    xs, out = [], []
    for i, ch in enumerate(s):
        if ch == " ":
            continue
        xs.append(f"{x0 + i * cw:.1f}")
        out.append(escape(ch))
    if not out:
        return ""
    c = f' class="{cls}"' if cls else ""
    return f'<text x="{" ".join(xs)}" y="{y}"{c}>{"".join(out)}</text>'


def build(theme):
    t = THEMES[theme]
    css = f"""
    text {{ font-family: ui-monospace, SFMono-Regular, "JetBrains Mono", "Cascadia Mono", Menlo, Consolas, "DejaVu Sans Mono", "Liberation Mono", monospace; font-size: {FS}px; fill: {t['fg']}; }}
    .k {{ fill: {t['key']}; font-weight: 700; }}
    .u {{ fill: {t['accent']}; font-weight: 700; }}
    .hl {{ fill: {t['accent']}; }}
    .cm, .m {{ fill: {t['muted']}; }}
    .title {{ fill: {t['muted']}; font-size: 13px; font-weight: 600; }}
    .art text {{ font-size: {AFS}px; font-weight: 700; }}
    .hair {{ fill: {t['hair']}; }} .face, .eye, .shut {{ fill: {t['fg']}; }} .gl {{ fill: {t['accent']}; }}
    .hood {{ fill: {t['hoodie']}; }} .srf {{ fill: {t['surface']}; }} .tux {{ fill: {t['tux']}; }} .desk {{ fill: {t['muted']}; }} .kick {{ fill: {t['fg']}; }}
    .row {{ animation: in .45s ease-out both; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
    .eye {{ animation: eyeo 5s infinite; }}
    .shut {{ opacity: 0; animation: eyec 5s infinite; }}
    @keyframes eyeo {{ 0%, 91%, 95%, 100% {{ opacity: 1; }} 92%, 94% {{ opacity: 0; }} }}
    @keyframes eyec {{ 0%, 91%, 95%, 100% {{ opacity: 0; }} 92%, 94% {{ opacity: 1; }} }}
    .cursor {{ animation: blink 1.1s step-end infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .row, .eye, .shut, .cursor {{ animation: none; }} }}
    """
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
    p.append('<title id="t">hamed@github — neofetch</title>')
    p.append('<desc id="d">Hamed Rezaie: medical student in Tehran who codes. Linux, AI and medical AI; founder of Medalak. '
             'Python, Django, PySide6, PyTorch, TensorFlow, Hugging Face, LangChain, vLLM, Docker. '
             'Art: a boy with glasses behind a Surface Pro with a Bluetooth keyboard and mouse.</desc>')
    p.append(f"<style>{css}</style>")
    p.append(f'<defs><clipPath id="win"><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14"/></clipPath></defs>')

    # window + GNOME-style header bar
    p.append(f'<g clip-path="url(#win)"><rect width="{W}" height="{H}" fill="{t["card"]}"/>'
             f'<rect width="{W}" height="{TOP}" fill="{t["bar"]}"/>'
             f'<line x1="0" y1="{TOP}" x2="{W}" y2="{TOP}" stroke="{t["border"]}"/></g>')
    p.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{t["border"]}"/>')
    p.append(f'<text x="{W/2}" y="25" text-anchor="middle" class="title">hamed@github: ~</text>')
    for i, kind in enumerate(("min", "max", "close")):
        cx, cy = W - 26 - (2 - i) * 30, 20
        p.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{t["btn"]}"/>')
        st = f'stroke="{t["fg"]}" stroke-width="1.4" stroke-linecap="round" fill="none"'
        if kind == "min":
            p.append(f'<line x1="{cx-4}" y1="{cy+3}" x2="{cx+4}" y2="{cy+3}" {st}/>')
        elif kind == "max":
            p.append(f'<rect x="{cx-3.5}" y="{cy-3.5}" width="7" height="7" rx="1" {st}/>')
        else:
            p.append(f'<path d="M{cx-3.5} {cy-3.5} L{cx+3.5} {cy+3.5} M{cx+3.5} {cy-3.5} L{cx-3.5} {cy+3.5}" {st}/>')

    # prompt
    prompt = f"{USER}@{HOST}:~$ "
    p.append(glyph_text(f"{USER}@{HOST}", ART_X, PROMPT_Y, "u"))
    p.append(glyph_text(":~$", ART_X + len(USER + HOST) * CW + CW, PROMPT_Y, "m"))
    p.append(glyph_text("neofetch", ART_X + len(prompt) * CW, PROMPT_Y))

    # ascii scene: one <text> per colour region per row
    n_info = len(INFO) + 2
    info_mid = ROW0 + (n_info - 1) * LH / 2
    art_top = info_mid - (len(ART) - 1) * ALH / 2 + 6
    p.append('<g class="art">')
    for r, line in enumerate(ART):
        y = round(art_top + r * ALH, 1)
        classes = sorted({art_class(r, c, ch) for c, ch in enumerate(line) if ch != " "})
        for cls in classes:
            masked = "".join(ch if ch != " " and art_class(r, c, ch) == cls else " " for c, ch in enumerate(line))
            p.append(glyph_text(masked, ART_X, y, cls, cw=ACW))
        if "eye" in classes:  # closed eyes, shown briefly when the open ones hide
            shut = "".join("-" if ch != " " and art_class(r, c, ch) == "eye" else " " for c, ch in enumerate(line))
            p.append(glyph_text(shut, ART_X, y, "shut", cw=ACW))
    p.append("</g>")

    # info column
    def row(i, inner):
        return f'<g class="row" style="animation-delay:{0.15 + i * 0.06:.2f}s">{inner}</g>'

    head = f"{USER}@{HOST}"
    p.append(row(0, glyph_text(USER, INFO_X, ROW0, "u") + glyph_text("@", INFO_X + len(USER) * CW, ROW0)
                 + glyph_text(HOST, INFO_X + (len(USER) + 1) * CW, ROW0, "u")))
    p.append(row(1, glyph_text("-" * len(head), INFO_X, ROW0 + LH, "m")))
    vx = INFO_X + KEY_COLS * CW
    for i, (k, v) in enumerate(INFO, start=2):
        y = ROW0 + i * LH
        inner = glyph_text(k, INFO_X, y, "k") + glyph_text(":", INFO_X + len(k) * CW, y, "m")
        segs = v if isinstance(v, list) else [(v, "")]
        col = 0
        for text, cls in segs:
            inner += glyph_text(text, vx + col * CW, y, cls)
            col += len(text)
        p.append(row(i, inner))

    # colour blocks
    by = ROW0 + n_info * LH - 4
    for i, colr in enumerate(t["blocks"]):
        rr, cc = divmod(i, 8)
        p.append(f'<rect class="row" style="animation-delay:{0.15 + (n_info + rr) * 0.06:.2f}s" x="{INFO_X + cc * 30}" '
                 f'y="{by + rr * 17}" width="28" height="15" rx="3" fill="{colr}"/>')

    # final prompt + blinking cursor
    fy = H - 26
    p.append(glyph_text(f"{USER}@{HOST}", ART_X, fy, "u"))
    p.append(glyph_text(":~$", ART_X + len(USER + HOST) * CW + CW, fy, "m"))
    p.append(f'<rect class="cursor" x="{ART_X + len(prompt) * CW:.1f}" y="{fy - 13}" width="8.4" height="17" fill="{t["accent"]}"/>')
    p.append("</svg>")
    return "\n".join(x for x in p if x)


if __name__ == "__main__":
    for theme in THEMES:
        out = ROOT / "assets" / f"neofetch-{theme}.svg"
        out.write_text(build(theme), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))
