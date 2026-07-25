#!/usr/bin/env python3
"""
Render data/contributions.json as a GitHub-style contribution heatmap SVG
with a cool teal→blue intensity ramp and one-shot reveal animation.
"""
import datetime
import json
import os

from profile_config import PROMPT_HOST, PROMPT_USER

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

# cool teal → steel-blue ramp (unique vs GitHub green)
PALETTE = ["#152033", "#164e63", "#0e7490", "#0891b2", "#22d3ee", "#67e8f9"]

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 22
LEFT_LABEL_W = 30
TOP_LABEL_H = 20
TITLEBAR_H = 30

BG = "#0b1220"
BG2 = "#111a2b"
FRAME = "#2a3548"
MUTED = "#8b9bb4"
TEXT = "#d7e0ea"
ACCENT = "#f0b429"
TEAL = "#22d3ee"
GOLD = "#f0b429"

COL_T = 0.018
ROW_T = 0.045
CELL_DUR = 0.42


def level_for(count):
    if count == 0:
        return 0
    if count <= 5:
        return 1
    if count <= 15:
        return 2
    if count <= 30:
        return 3
    if count <= 50:
        return 4
    return 5


def build_grid(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # sunday=0
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data):
    days = data["days"]
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 88
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@keyframes cell {{
  0% {{ opacity: 0; transform: translateY(-6px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
.c {{ opacity: 0; animation: cell {CELL_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both; }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" role="img" '
        f'aria-label="{data["username"]} contribution graph">',
        f"<style>{css}</style>",
        f'<defs><linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{BG}"/>'
        f'<stop offset="100%" stop-color="{BG2}"/>'
        f"</linearGradient></defs>",
        f'<rect width="100%" height="100%" rx="12" fill="url(#hbg)" stroke="{FRAME}" stroke-width="1"/>',
        f'<rect width="100%" height="{TITLEBAR_H}" rx="12" fill="{BG2}"/>',
        f'<rect y="{TITLEBAR_H - 12}" width="100%" height="12" fill="{BG2}"/>',
    ]
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(
            f'<circle cx="{18 + i * 16}" cy="{TITLEBAR_H / 2}" r="5" fill="{dotcol}"/>'
        )

    title = f"{PROMPT_USER}@{PROMPT_HOST}: ~/contributions --graph"
    parts.append(
        f'<text x="{canvas_w / 2}" y="{TITLEBAR_H / 2 + 4}" text-anchor="middle" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="12" fill="{MUTED}">{title}</text>'
    )

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(
            f'<text x="{x}" y="{TITLEBAR_H + 14}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="10" fill="{MUTED}">{label}</text>'
        )

    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(
            f'<text x="{PAD}" y="{y:.1f}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="10" fill="{MUTED}">{wname}</text>'
        )

    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            plural = "s" if count != 1 else ""
            color = PALETTE[lvl]
            parts.append(
                f'<rect class="c" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" '
                f'rx="2" fill="{color}" style="animation-delay:{delay:.3f}s">'
                f"<title>{date_s}: {count} contribution{plural}</title>"
                f"</rect>"
            )

    leg_y = grid_top + art_h + 6
    leg_x = canvas_w - PAD - (len(PALETTE) * (CELL - 1) + 70)
    parts.append(
        f'<text x="{leg_x - 28}" y="{leg_y + CELL - 2}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="10" fill="{MUTED}">Less</text>'
    )
    lx = leg_x + 8
    for lvl, color in enumerate(PALETTE):
        parts.append(
            f'<rect x="{lx}" y="{leg_y}" width="{CELL - 2}" height="{CELL - 2}" '
            f'rx="2" fill="{color}"/>'
        )
        lx += CELL
    parts.append(
        f'<text x="{lx + 4}" y="{leg_y + CELL - 2}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="10" fill="{MUTED}">More</text>'
    )

    sep_y = leg_y + CELL + 14
    parts.append(
        f'<line x1="{PAD}" y1="{sep_y}" x2="{canvas_w - PAD}" y2="{sep_y}" '
        f'stroke="{FRAME}" stroke-width="1"/>'
    )

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    total = data["total_contributions"]
    last_year = data.get("last_year_contributions", total)
    best = data["best_day"]
    rng = data["range"]

    ly = sep_y + 24
    parts.append(
        f'<text x="{PAD}" y="{ly}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="13">'
        f'<tspan fill="{ACCENT}" font-weight="700">{total:,}</tspan>'
        f'<tspan fill="{MUTED}"> contributions all-time · </tspan>'
        f'<tspan fill="{TEAL}" font-weight="700">{last_year:,}</tspan>'
        f'<tspan fill="{MUTED}"> in the last year</tspan></text>'
    )
    parts.append(
        f'<text x="{canvas_w - PAD}" y="{ly}" text-anchor="end" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="11" fill="{MUTED}">since {rng["start"]}</text>'
    )
    ly += 24
    parts.append(
        f'<text x="{PAD}" y="{ly}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="13" fill="{MUTED}">current streak '
        f'<tspan fill="{TEXT}" font-weight="700">{cs} days</tspan>'
        f" · longest "
        f'<tspan fill="{TEXT}" font-weight="700">{ls} days</tspan></text>'
    )
    parts.append(
        f'<text x="{canvas_w - PAD}" y="{ly}" text-anchor="end" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
        f'font-size="11" fill="{MUTED}">best day {best["count"]} on {best["date"]}</text>'
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
