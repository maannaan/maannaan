#!/usr/bin/env python3
"""
Build a wide mission-dossiers SVG (three featured-work panels) matching the
control-room chrome. Content comes from profile_config.MISSIONS.
"""
import html
import os

from profile_config import MISSIONS, PROMPT_HOST, PROMPT_USER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "mission-dossiers.svg")

W, H = 1100, 280
PAD = 24
TITLEBAR_H = 36
GAP = 12

BG = "#0b1220"
BG2 = "#111a2b"
PANEL = "#151f30"
FRAME = "#2a3548"
MUTED = "#8b9bb4"
INK = "#d7e0ea"
AMBER = "#f0b429"
TEAL = "#22d3ee"
BLUE = "#5b8def"
RED = "#ff5f56"
YELLOW = "#ffbd2e"
DOT_GREEN = "#27c93f"


def esc(s):
    return html.escape(str(s))


def main():
    n = len(MISSIONS)
    panel_w = (W - PAD * 2 - GAP * (n - 1)) / n
    panel_y = TITLEBAR_H + 16
    panel_h = H - panel_y - PAD

    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Mission dossiers — featured engineering work">'
        ),
        (
            "<style>"
            "@keyframes fadeup { from { opacity: 0; transform: translateY(8px); } "
            "to { opacity: 1; transform: translateY(0); } }"
            ".tile { opacity: 0; animation: fadeup 0.45s cubic-bezier(.2,.8,.2,1) both; }"
            "</style>"
        ),
        (
            "<defs>"
            '<linearGradient id="dbg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{BG}"/>'
            f'<stop offset="100%" stop-color="{BG2}"/>'
            "</linearGradient>"
            "</defs>"
        ),
        (
            f'<rect width="100%" height="100%" rx="14" fill="url(#dbg)" '
            f'stroke="{FRAME}" stroke-width="1"/>'
        ),
        f'<rect width="100%" height="{TITLEBAR_H}" rx="14" fill="{BG2}"/>',
        f'<rect y="{TITLEBAR_H - 14}" width="100%" height="14" fill="{BG2}"/>',
    ]

    for i, c in enumerate([RED, YELLOW, DOT_GREEN]):
        parts.append(
            f'<circle cx="{18 + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{c}"/>'
        )

    title = f"{PROMPT_USER}@{PROMPT_HOST}: ~/missions --list"
    parts.append(
        f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4}" text-anchor="middle" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{MUTED}">{esc(title)}</text>'
    )

    for i, mission in enumerate(MISSIONS):
        x = PAD + i * (panel_w + GAP)
        delay = 0.12 + i * 0.1
        parts.append(
            f'<g class="tile" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x:.1f}" y="{panel_y}" width="{panel_w:.1f}" height="{panel_h}" '
            f'rx="10" fill="{PANEL}" stroke="{FRAME}"/>'
            f'<rect x="{x:.1f}" y="{panel_y}" width="4" height="{panel_h}" '
            f'rx="2" fill="{AMBER}"/>'
            # ID chip
            f'<rect x="{x + 18:.1f}" y="{panel_y + 18}" width="58" height="20" '
            f'rx="4" fill="{BG}" stroke="{FRAME}"/>'
            f'<text x="{x + 47:.1f}" y="{panel_y + 32}" text-anchor="middle" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="11" fill="{TEAL}">{esc(mission["id"])}</text>'
            # title
            f'<text x="{x + 18:.1f}" y="{panel_y + 70}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="15" font-weight="700" fill="{INK}">{esc(mission["title"])}</text>'
            # outcome
            f'<text x="{x + 18:.1f}" y="{panel_y + 98}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="12" fill="{MUTED}">{esc(mission["outcome"])}</text>'
            # stack label + line
            f'<text x="{x + 18:.1f}" y="{panel_y + 130}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="10" fill="{BLUE}">STACK</text>'
            f'<text x="{x + 18:.1f}" y="{panel_y + 152}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="12" fill="{AMBER}">{esc(mission["stack"])}</text>'
            f"</g>"
        )

    parts.append("</svg>")
    svg = "".join(parts)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT, len(svg), "bytes;", W, "x", H)


if __name__ == "__main__":
    main()
