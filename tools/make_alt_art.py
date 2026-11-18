"""Alternate hero drawings in the al-Sufi style: paper made transparent, a light and a dark version.
Usage: python -I tools/make_alt_art.py <dir with durer.jpg and galileo.jpg>
Writes art/durer_{light,dark}.webp and art/galileo_{light,dark}.webp."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps

src = Path(sys.argv[1])
out = Path(__file__).resolve().parent.parent / "art"


def lift(im, name, gain=3.2, floor=6, width=900):
    im = im.convert("RGB")
    im.thumbnail((width, width * 2), Image.LANCZOS)
    a = np.asarray(ImageOps.autocontrast(im, cutoff=1)).astype(np.float32)
    mn = a.min(axis=2)
    alpha = np.clip((255 - mn - floor) * gain, 0, 255)
    light = np.dstack([a * 0.92, alpha])  # ink slightly warm-dark, paper gone
    hsv = np.asarray(Image.fromarray(a.astype(np.uint8)).convert("HSV")).astype(np.float32)
    hsv[..., 2] = 255 - hsv[..., 2] * 0.85
    dark = np.asarray(Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB")).astype(np.float32)
    dark = dark * np.array([1.0, 0.97, 0.9])  # parchment tint on the dark page
    for tag, rgb in (("light", light[..., :3]), ("dark", dark)):
        Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha]).astype(np.uint8), "RGBA").save(
            out / f"{name}_{tag}.webp", "WEBP", quality=62, method=6)
    print(name, im.size)


# Dürer 1515: drop the title line, keep the whole sky and the four astronomers
d = Image.open(src / "durer.jpg")
lift(d.crop((16, 68, d.width - 16, d.height - 16)), "durer", gain=2.6, floor=14)
# Galileo 1610: the half-lit moon cut out on its disc, real tones in both themes (inverting would swap day and night)
g = Image.open(src / "galileo.jpg").convert("L")
g = ImageOps.autocontrast(g.crop((120, 40, 840, 760)), cutoff=1)
g = g.resize((720, 720), Image.LANCZOS)
yy, xx = np.mgrid[0:720, 0:720]
r = np.hypot(xx - 356, yy - 354)
mask = np.clip((348 - r) * 1.5, 0, 255).astype(np.uint8)
t = np.asarray(g).astype(np.float32)
rgb = np.dstack([t * 0.99, t * 0.95, t * 0.86])  # warm paper tone
Image.fromarray(np.dstack([rgb, mask]).astype(np.uint8), "RGBA").save(out / "galileo.webp", "WEBP", quality=66, method=6)
for f in ("galileo_light.webp", "galileo_dark.webp"):
    (out / f).unlink(missing_ok=True)
print("galileo", (out / "galileo.webp").stat().st_size // 1024, "KB")
