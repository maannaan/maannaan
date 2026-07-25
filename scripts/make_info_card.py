"""
Build a kubectl/neofetch-style info card SVG to sit to the RIGHT of the ASCII
portrait: colored key/value rows for work, stack, and highlights.
"""
import html
import os

from profile_config import PROMPT_HOST, PROMPT_USER, ROWS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W = 500
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 108
LINE_H = 20.5
TOP_GAP = 30
BOTTOM_PAD = 14
HOST_FONT = 14
HOST_CHAR_W = 8.4

_lines = sum(1 for r in ROWS if r[0] != "gap")
_gaps = sum(1 for r in ROWS if r[0] == "gap")
H = int(TITLEBAR_H + TOP_GAP + _lines * LINE_H + _gaps * LINE_H * 0.5 + BOTTOM_PAD)

# slate + amber + steel-blue
BG = "#0b1220"
BG2 = "#111a2b"
FRAME = "#2a3548"
MUTED = "#8b9bb4"
INK = "#d7e0ea"
KEY = "#f0b429"
SECTION = "#5b8def"
GREEN = "#2dd4bf"
ACCENT = "#38bdf8"


def esc(s):
    return html.escape(s)


def rise(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.06
    return (
        f'<g opacity="0">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.35s" '
        f'begin="{delay:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 6" to="0 0" dur="0.35s" begin="{delay:.2f}s" fill="freeze"/>'
        f"</g>"
    )


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" role="img" aria-label="Manan Paliwal — role, stack, highlights">',
    f'<defs><linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0%" stop-color="{BG}"/>'
    f'<stop offset="100%" stop-color="{BG2}"/>'
    f"</linearGradient></defs>",
    f'<rect width="100%" height="100%" rx="12" fill="url(#ibg)" stroke="{FRAME}" stroke-width="1"/>',
    f'<rect width="100%" height="{TITLEBAR_H}" rx="12" fill="{BG2}"/>',
    f'<rect y="{TITLEBAR_H - 12}" width="100%" height="12" fill="{BG2}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{18 + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>')

title = f"{PROMPT_USER}@{PROMPT_HOST}: ~$ kubectl describe me"
parts.append(
    f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4}" text-anchor="middle" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
    f'font-size="12" fill="{MUTED}">{esc(title)}</text>'
)

y = TITLEBAR_H + TOP_GAP
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.5
        continue
    if kind == "host":
        host_chars = len(PROMPT_USER) + 1 + len(PROMPT_HOST)
        rule_x = KEY_X + host_chars * HOST_CHAR_W + 12
        inner = (
            f'<text x="{KEY_X}" y="{y}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="{HOST_FONT}">'
            f'<tspan fill="{GREEN}">{esc(PROMPT_USER)}</tspan>'
            f'<tspan fill="{MUTED}">@</tspan>'
            f'<tspan fill="{SECTION}">{esc(PROMPT_HOST)}</tspan>'
            f"</text>"
            f'<line x1="{rule_x}" y1="{y - 4}" x2="{W - PAD}" y2="{y - 4}" '
            f'stroke="{FRAME}" stroke-width="1"/>'
        )
    elif kind == "sec":
        title = esc(row[1])
        inner = (
            f'<text x="{KEY_X}" y="{y}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="13" fill="{SECTION}">— {title}</text>'
        )
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (
            f'<text x="{KEY_X}" y="{y}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="13" fill="{KEY}">{key}</text>'
            f'<text x="{VAL_X}" y="{y}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="13" fill="{INK}">{val}</text>'
        )
    elif kind == "bul":
        txt = esc(row[1])
        inner = (
            f'<text x="{KEY_X}" y="{y}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="13" fill="{GREEN}">▸ </text>'
            f'<text x="{KEY_X + 16}" y="{y}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="13" fill="{INK}">{txt}</text>'
        )
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(y))
