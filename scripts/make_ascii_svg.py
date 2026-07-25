"""
Convert a portrait photo into a clean, monochrome ASCII-art SVG that "types"
itself in like a terminal, then holds.

Monochrome is deliberate -- one fill color + density ramp + high contrast
reads as neat and legible on GitHub (SMIL animations run; JS does not).
"""
from PIL import Image, ImageEnhance, ImageFilter
import html
import os
import sys

from profile_config import FULL_NAME, PROMPT_HOST, PROMPT_USER

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-prepped.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "ascii-portrait.svg")

COLS = 100
ROWS = 53
CELL_W = 8
CELL_H = 15
RAMP = " .`:-=+*cs#%@"

CONTRAST = 1.05
BRIGHTNESS = 1.0
GAMMA = 1.18
SHARPEN = False
WHITE_FLOOR = 0.80

PAD = 20
TITLEBAR_H = 30
STATUS_H = 30
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + ART_H + STATUS_H + PAD

# slate terminal palette (infra control-plane)
BG = "#0b1220"
BG2 = "#111a2b"
FRAME = "#2a3548"
TITLE_TEXT = "#8b9bb4"
INK = "#d7e0ea"
CURSOR = "#f0b429"

ROW_DUR = 0.11
STAGGER = 0.11

im = Image.open(SRC).convert("L")
if SHARPEN:
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=140, threshold=2))
im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
im = ImageEnhance.Contrast(im).enhance(CONTRAST)
im = im.resize((COLS, ROWS), Image.LANCZOS)
px = im.load()

STATIC = bool(os.environ.get("STATIC"))

rows_txt = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        lum = px[x, y] / 255.0
        lum = pow(lum, GAMMA)
        if lum >= WHITE_FLOOR:
            chars.append(" ")
            continue
        idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
        idx = max(0, min(len(RAMP) - 1, idx))
        chars.append(RAMP[idx])
    rows_txt.append("".join(chars))

art_top = TITLEBAR_H + PAD * 0.35
font_size = CELL_H * 0.86

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" role="img" '
    f'aria-label="{html.escape(FULL_NAME)} — ASCII portrait">'
)
parts.append(
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0%" stop-color="{BG}"/>'
    f'<stop offset="100%" stop-color="{BG2}"/>'
    f"</linearGradient></defs>"
)
parts.append(f'<rect width="100%" height="100%" rx="12" fill="url(#bg)" stroke="{FRAME}" stroke-width="1"/>')
parts.append(f'<rect width="100%" height="{TITLEBAR_H}" rx="12" fill="{BG2}"/>')
parts.append(f'<rect y="{TITLEBAR_H - 12}" width="100%" height="12" fill="{BG2}"/>')

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{18 + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>')

title = f"{PROMPT_USER}@{PROMPT_HOST}: ~$ ./portrait.sh"
parts.append(
    f'<text x="{CANVAS_W / 2}" y="{TITLEBAR_H / 2 + 4}" text-anchor="middle" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
    f'font-size="12" fill="{TITLE_TEXT}">{html.escape(title)}</text>'
)

for ry, line in enumerate(rows_txt):
    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    safe = html.escape(line)
    clip_id = f"r{ry}"
    text = (
        f'<text x="{PAD}" y="{y:.2f}" xml:space="preserve" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="{font_size:.2f}" fill="{INK}">{safe}</text>'
    )

    if STATIC:
        parts.append(text)
        continue

    parts.append(
        f'<clipPath id="{clip_id}">'
        f'<rect x="{PAD}" y="{row_y:.2f}" width="0" height="{CELL_H}">'
        f'<animate attributeName="width" from="0" to="{ART_W}" '
        f'dur="{ROW_DUR}s" begin="{delay:.3f}s" fill="freeze"/>'
        f"</rect></clipPath>"
    )
    parts.append(f'<g clip-path="url(#{clip_id})">{text}</g>')
    cursor_x_end = PAD + ART_W
    parts.append(
        f'<rect x="{PAD}" y="{row_y + 2:.2f}" width="7" height="{CELL_H - 4}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.9;1" '
        f'dur="{ROW_DUR}s" begin="{delay:.3f}s" fill="freeze"/>'
        f'<animate attributeName="x" from="{PAD}" to="{cursor_x_end}" '
        f'dur="{ROW_DUR}s" begin="{delay:.3f}s" fill="freeze"/>'
        f"</rect>"
    )

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 19
STATUS_FONT = 13
CHAR_W = STATUS_FONT * 0.6
status_prefix = f"{PROMPT_USER}@{PROMPT_HOST}:~$ whoami "
cursor_x = PAD + (len(status_prefix) + len(FULL_NAME)) * CHAR_W + 4

parts.append(f'<rect y="{status_line_y:.2f}" width="100%" height="{STATUS_H}" fill="{BG2}"/>')
parts.append(
    f'<text x="{PAD}" y="{status_y:.2f}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
    f'font-size="{STATUS_FONT}" fill="{TITLE_TEXT}">'
    f'{html.escape(status_prefix)}'
    f'<tspan fill="{INK}">{html.escape(FULL_NAME)}</tspan></text>'
)
parts.append(
    f'<rect x="{cursor_x:.2f}" y="{status_y - 11:.2f}" width="7" height="14" fill="{CURSOR}">'
    f'<animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>'
    f"</rect>"
)

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", CANVAS_W, "x", CANVAS_H)
