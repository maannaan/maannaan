"""
Square-crop + circular-mask operator badge from Manan-2.jpeg.
Pillow only — no rembg.

  python scripts/prep_badge.py [input.jpg] [output.png]
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "Manan-2.jpeg")
OUT = (
    sys.argv[2]
    if len(sys.argv) > 2
    else os.path.join(ROOT, "assets", "operator-badge.png")
)

SIZE = 256

im = Image.open(INP).convert("RGBA")
w, h = im.size
side = min(w, h)
# Bias crop slightly upward so the face fills the circle (talking-head shot).
left = (w - side) // 2
top = max(0, (h - side) // 2 - side // 10)
im = im.crop((left, top, left + side, top + side)).resize(
    (SIZE, SIZE), Image.LANCZOS
)

mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).ellipse((0, 0, SIZE - 1, SIZE - 1), fill=255)
out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
out.paste(im, (0, 0), mask=mask)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
out.save(OUT, "PNG")
print("wrote", OUT, out.size)
