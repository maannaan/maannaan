#!/usr/bin/env python3
"""
Build a wide animated platform control-room SVG for the GitHub profile README.

Reads identity + panel data from profile_config.py and embeds the circular
operator badge (assets/operator-badge.png) as a base64 data URI so a single
<img src="control-room.svg"> works on GitHub.
"""
import base64
import html
import os

from profile_config import (
    CERT_CHIP,
    CLOUDS,
    FOCUS_TILES,
    FULL_NAME,
    LOCATION,
    PIPELINE_STAGES,
    PROMPT_HOST,
    PROMPT_USER,
    ROLE_LINE,
    TAGLINE,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
BADGE_PATH = os.path.join(ROOT, "assets", "operator-badge.png")
OUT = os.path.join(ROOT, "control-room.svg")

W, H = 1100, 460
PAD = 24
TITLEBAR_H = 36

BG = "#0b1220"
BG2 = "#111a2b"
PANEL = "#151f30"
FRAME = "#2a3548"
MUTED = "#8b9bb4"
INK = "#d7e0ea"
AMBER = "#f0b429"
BLUE = "#5b8def"
TEAL = "#22d3ee"
GREEN = "#2dd4bf"
RED = "#ff5f56"
YELLOW = "#ffbd2e"
DOT_GREEN = "#27c93f"


def esc(s):
    return html.escape(str(s))


def load_badge_data_uri():
    with open(BADGE_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def main():
    badge_uri = load_badge_data_uri()

    y0 = TITLEBAR_H + 14
    op_y = y0 + 44
    badge_cx, badge_cy, badge_r = 78, op_y + 44, 36

    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{esc(FULL_NAME)} — platform control room">'
        ),
        (
            "<style>"
            "@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.45; } }"
            "@keyframes fadeup { from { opacity: 0; transform: translateY(8px); } "
            "to { opacity: 1; transform: translateY(0); } }"
            ".live { animation: pulse 1.6s ease-in-out infinite; }"
            ".tile { opacity: 0; animation: fadeup 0.45s cubic-bezier(.2,.8,.2,1) both; }"
            "</style>"
        ),
        (
            "<defs>"
            '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{BG}"/>'
            f'<stop offset="100%" stop-color="{BG2}"/>'
            "</linearGradient>"
            f'<clipPath id="badgeClip">'
            f'<circle cx="{badge_cx}" cy="{badge_cy}" r="{badge_r}"/>'
            "</clipPath>"
            "</defs>"
        ),
        (
            f'<rect width="100%" height="100%" rx="14" fill="url(#bg)" '
            f'stroke="{FRAME}" stroke-width="1"/>'
        ),
        f'<rect width="100%" height="{TITLEBAR_H}" rx="14" fill="{BG2}"/>',
        f'<rect y="{TITLEBAR_H - 14}" width="100%" height="14" fill="{BG2}"/>',
    ]

    for i, c in enumerate([RED, YELLOW, DOT_GREEN]):
        parts.append(
            f'<circle cx="{18 + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{c}"/>'
        )

    title = f"{PROMPT_USER}@{PROMPT_HOST}: ~/control-room --live"
    parts.append(
        f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4}" text-anchor="middle" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{MUTED}">{esc(title)}</text>'
    )

    # top status strip
    parts.append(
        f'<rect x="{PAD}" y="{y0}" width="{W - PAD * 2}" height="28" rx="8" '
        f'fill="{PANEL}" stroke="{FRAME}"/>'
    )
    parts.append(
        f'<circle class="live" cx="{PAD + 16}" cy="{y0 + 14}" r="4" fill="{GREEN}"/>'
    )
    parts.append(
        f'<text x="{PAD + 28}" y="{y0 + 18}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{GREEN}">LIVE</text>'
    )
    parts.append(
        f'<text x="{PAD + 72}" y="{y0 + 18}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{MUTED}">·</text>'
    )
    parts.append(
        f'<text x="{PAD + 86}" y="{y0 + 18}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{INK}">{esc(TAGLINE)}</text>'
    )

    chip_x = W - PAD - 12
    for label, fill in [(LOCATION, MUTED), (CERT_CHIP, AMBER)]:
        tw = 8 + len(label) * 7.2
        chip_x -= tw + 10
        parts.append(
            f'<rect x="{chip_x}" y="{y0 + 5}" width="{tw}" height="18" rx="4" '
            f'fill="{BG}" stroke="{FRAME}"/>'
        )
        parts.append(
            f'<text x="{chip_x + tw / 2}" y="{y0 + 17}" text-anchor="middle" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="10" fill="{fill}">{esc(label)}</text>'
        )

    # operator row
    parts.append(
        f'<rect x="{PAD}" y="{op_y}" width="{W - PAD * 2}" height="88" rx="10" '
        f'fill="{PANEL}" stroke="{FRAME}"/>'
    )
    parts.append(
        f'<circle cx="{badge_cx}" cy="{badge_cy}" r="{badge_r + 2}" fill="none" '
        f'stroke="{AMBER}" stroke-width="2"/>'
    )
    parts.append(
        f'<image href="{badge_uri}" xlink:href="{badge_uri}" '
        f'x="{badge_cx - badge_r}" y="{badge_cy - badge_r}" '
        f'width="{badge_r * 2}" height="{badge_r * 2}" '
        f'clip-path="url(#badgeClip)"/>'
    )
    parts.append(
        f'<text x="132" y="{op_y + 34}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="22" font-weight="700" fill="{INK}">{esc(FULL_NAME)}</text>'
    )
    parts.append(
        f'<text x="132" y="{op_y + 56}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="13" fill="{AMBER}">{esc(ROLE_LINE)}</text>'
    )
    parts.append(
        f'<text x="132" y="{op_y + 76}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{MUTED}">'
        f"operator · multi-cloud · automate everything</text>"
    )

    # cloud lanes
    lane_y = op_y + 102
    lane_h = 52
    gap = 10
    n = len(CLOUDS)
    lane_w = (W - PAD * 2 - gap * (n - 1)) / n
    for i, cloud in enumerate(CLOUDS):
        x = PAD + i * (lane_w + gap)
        delay = 0.1 + i * 0.08
        parts.append(
            f'<g class="tile" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x:.1f}" y="{lane_y}" width="{lane_w:.1f}" height="{lane_h}" '
            f'rx="8" fill="{PANEL}" stroke="{FRAME}"/>'
            f'<circle class="live" cx="{x + 16:.1f}" cy="{lane_y + 18}" r="4" fill="{GREEN}"/>'
            f'<text x="{x + 28:.1f}" y="{lane_y + 22}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="13" font-weight="700" fill="{TEAL}">{esc(cloud["name"])}</text>'
            f'<text x="{x + 16:.1f}" y="{lane_y + 40}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="11" fill="{MUTED}">{esc(cloud["detail"])}</text>'
            f"</g>"
        )

    # pipeline rail
    pipe_y = lane_y + lane_h + 16
    parts.append(
        f'<rect x="{PAD}" y="{pipe_y}" width="{W - PAD * 2}" height="64" rx="10" '
        f'fill="{PANEL}" stroke="{FRAME}"/>'
    )
    parts.append(
        f'<text x="{PAD + 14}" y="{pipe_y + 18}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="11" fill="{BLUE}">PIPELINE</text>'
    )

    stages = PIPELINE_STAGES
    stage_count = len(stages)
    rail_x0 = PAD + 40
    rail_x1 = W - PAD - 40
    rail_y = pipe_y + 40
    parts.append(
        f'<line x1="{rail_x0}" y1="{rail_y}" x2="{rail_x1}" y2="{rail_y}" '
        f'stroke="{FRAME}" stroke-width="2"/>'
    )
    for i, stage in enumerate(stages):
        t = i / (stage_count - 1) if stage_count > 1 else 0
        cx = rail_x0 + t * (rail_x1 - rail_x0)
        delay = 0.25 + i * 0.18
        parts.append(
            f"<g>"
            f'<circle cx="{cx:.1f}" cy="{rail_y}" r="8" fill="{BG2}" '
            f'stroke="{FRAME}" stroke-width="2">'
            f'<animate attributeName="fill" from="{BG2}" to="{AMBER}" dur="0.25s" '
            f'begin="{delay:.2f}s" fill="freeze"/>'
            f'<animate attributeName="stroke" from="{FRAME}" to="{AMBER}" dur="0.25s" '
            f'begin="{delay:.2f}s" fill="freeze"/>'
            f"</circle>"
            f'<text x="{cx:.1f}" y="{rail_y - 14}" text-anchor="middle" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="11" fill="{INK}" opacity="0">'
            f"{esc(stage)}"
            f'<animate attributeName="opacity" from="0" to="1" dur="0.2s" '
            f'begin="{delay:.2f}s" fill="freeze"/>'
            f"</text>"
            f"</g>"
        )
        if i < stage_count - 1:
            nx = rail_x0 + ((i + 1) / (stage_count - 1)) * (rail_x1 - rail_x0)
            parts.append(
                f'<line x1="{cx + 8:.1f}" y1="{rail_y}" x2="{nx - 8:.1f}" y2="{rail_y}" '
                f'stroke="{FRAME}" stroke-width="2" stroke-dasharray="4 3">'
                f'<animate attributeName="stroke" from="{FRAME}" to="{TEAL}" dur="0.2s" '
                f'begin="{delay + 0.12:.2f}s" fill="freeze"/>'
                f"</line>"
            )

    # focus tiles
    tile_y = pipe_y + 78
    tile_h = H - tile_y - PAD
    tn = len(FOCUS_TILES)
    tile_w = (W - PAD * 2 - gap * (tn - 1)) / tn
    for i, tile in enumerate(FOCUS_TILES):
        x = PAD + i * (tile_w + gap)
        delay = 0.55 + i * 0.1
        parts.append(
            f'<g class="tile" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x:.1f}" y="{tile_y}" width="{tile_w:.1f}" height="{tile_h}" '
            f'rx="8" fill="{PANEL}" stroke="{FRAME}"/>'
            f'<rect x="{x:.1f}" y="{tile_y}" width="4" height="{tile_h}" rx="2" fill="{AMBER}"/>'
            f'<text x="{x + 18:.1f}" y="{tile_y + 28}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="14" font-weight="700" fill="{INK}">{esc(tile["title"])}</text>'
            f'<text x="{x + 18:.1f}" y="{tile_y + 50}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="12" fill="{MUTED}">{esc(tile["body"])}</text>'
            f"</g>"
        )

    parts.append("</svg>")
    svg = "".join(parts)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT, len(svg), "bytes;", W, "x", H)


if __name__ == "__main__":
    main()
