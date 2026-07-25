#!/usr/bin/env python3
"""
Render data/contributions.json as a compact terminal-style stats card.

No contribution grid — GitHub already shows that on the profile. This keeps
all-time totals, last-year count, streaks, and best day.
"""
import json
import os

from profile_config import PROMPT_HOST, PROMPT_USER

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

W = 860
H = 132
PAD = 22
TITLEBAR_H = 30

BG = "#0b1220"
BG2 = "#111a2b"
FRAME = "#2a3548"
MUTED = "#8b9bb4"
TEXT = "#d7e0ea"
ACCENT = "#f0b429"
TEAL = "#22d3ee"


def render(data):
    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    total = data["total_contributions"]
    last_year = data.get("last_year_contributions", total)
    best = data["best_day"]
    rng = data["range"]
    active = data.get("active_days", 0)
    avg = data.get("avg_per_active_day", 0)

    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{data["username"]} contribution stats">'
        ),
        (
            "<style>"
            "@keyframes fadeup { from { opacity: 0; transform: translateY(6px); } "
            "to { opacity: 1; transform: translateY(0); } }"
            ".row { opacity: 0; animation: fadeup 0.4s cubic-bezier(.2,.8,.2,1) both; }"
            "</style>"
        ),
        (
            '<defs><linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{BG}"/>'
            f'<stop offset="100%" stop-color="{BG2}"/>'
            "</linearGradient></defs>"
        ),
        (
            f'<rect width="100%" height="100%" rx="12" fill="url(#hbg)" '
            f'stroke="{FRAME}" stroke-width="1"/>'
        ),
        f'<rect width="100%" height="{TITLEBAR_H}" rx="12" fill="{BG2}"/>',
        f'<rect y="{TITLEBAR_H - 12}" width="100%" height="12" fill="{BG2}"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(
            f'<circle cx="{18 + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>'
        )

    title = f"{PROMPT_USER}@{PROMPT_HOST}: ~/contributions --stats"
    parts.append(
        f'<text x="{W / 2}" y="{TITLEBAR_H / 2 + 4}" text-anchor="middle" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{MUTED}">{title}</text>'
    )

    y1 = TITLEBAR_H + 34
    parts.append(
        f'<g class="row" style="animation-delay:0.08s">'
        f'<text x="{PAD}" y="{y1}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="14">'
        f'<tspan fill="{ACCENT}" font-weight="700">{total:,}</tspan>'
        f'<tspan fill="{MUTED}"> contributions all-time · </tspan>'
        f'<tspan fill="{TEAL}" font-weight="700">{last_year:,}</tspan>'
        f'<tspan fill="{MUTED}"> in the last year</tspan></text>'
        f'<text x="{W - PAD}" y="{y1}" text-anchor="end" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{MUTED}">since {rng["start"]}</text>'
        f"</g>"
    )

    y2 = y1 + 28
    parts.append(
        f'<g class="row" style="animation-delay:0.18s">'
        f'<text x="{PAD}" y="{y2}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="13" fill="{MUTED}">current streak '
        f'<tspan fill="{TEXT}" font-weight="700">{cs} days</tspan>'
        f" · longest "
        f'<tspan fill="{TEXT}" font-weight="700">{ls} days</tspan>'
        f" · active "
        f'<tspan fill="{TEXT}" font-weight="700">{active:,}</tspan>'
        f" days"
        f" · avg "
        f'<tspan fill="{TEXT}" font-weight="700">{avg}</tspan>'
        f"/day</text>"
        f'<text x="{W - PAD}" y="{y2}" text-anchor="end" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{MUTED}">best day '
        f'<tspan fill="{TEAL}" font-weight="700">{best["count"]}</tspan>'
        f' on {best["date"]}</text>'
        f"</g>"
    )

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    with open(IN_PATH, encoding="utf-8") as f:
        data = json.load(f)
    svg = render(data)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")
