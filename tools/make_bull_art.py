"""Al-Sufi's Taurus (Bodleian MS Marsh 144, p. 196) in the same look as the bear hero.
Usage: python -I tools/make_bull_art.py <dir with taurus.jpg>
Writes art/bull_{light,dark}.webp and art/bull_stars.json."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image

src = Path(sys.argv[1]); out = Path(__file__).resolve().parent.parent / "art"
s = Image.open(src / "taurus.jpg").convert("RGB").crop((118, 132, 636, 912))
W = 900; s = s.resize((W, round(s.height * W / s.width)), Image.LANCZOS)
a = np.asarray(s, dtype=np.float32)
# paper out: distance below the local paper tone; then fade the crop edges so no page edge shows
# local paper tone (stains included) from a wide blur, so only ink and paint stay
from PIL import ImageFilter
mn = Image.fromarray(a.min(axis=2).astype(np.uint8))
paper = np.asarray(mn.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(14)), dtype=np.float32)
ink = paper - a.min(axis=2)
sat = a.max(axis=2) - a.min(axis=2)
alpha = np.clip((ink - 26) * 5.0, 0, 255)
alpha = np.maximum(alpha, np.clip((sat - 70) * 4, 0, 255))  # keep the red stars whole
H = a.shape[0]; yy, xx = np.mgrid[0:H, 0:W]
edge = np.minimum.reduce([xx, W - 1 - xx, yy, H - 1 - yy]).astype(np.float32)
alpha *= np.clip(edge / 24, 0, 1)
alpha = np.where(alpha < 90, 0, alpha)  # no faint paper haze left as a box
Image.fromarray(np.dstack([a, alpha]).astype(np.uint8), "RGBA").save(out / "bull_light.webp", "WEBP", quality=74, method=6)
hsv = np.asarray(Image.fromarray(a.astype(np.uint8)).convert("HSV"), dtype=np.float32)
hsv[..., 2] = 255 - hsv[..., 2] * 0.75 - 20
hsv[..., 2] = np.clip(np.where(hsv[..., 1] > 90, 255 - hsv[..., 2] + 60, hsv[..., 2]), 0, 255)
dark = np.asarray(Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB"), dtype=np.float32)
Image.fromarray(np.dstack([dark, alpha]).astype(np.uint8), "RGBA").save(out / "bull_dark.webp", "WEBP", quality=74, method=6)
# red star dots
ai = a.astype(np.int16); r, g, b = ai[..., 0], ai[..., 1], ai[..., 2]
red = (r > 110) & (r - g > 50) & (r - b > 40)
seen = np.zeros_like(red); stars = []
for y, x in zip(*np.nonzero(red)):
    if seen[y, x]: continue
    st = [(y, x)]; seen[y, x] = 1; pts = []
    while st:
        cy, cx = st.pop(); pts.append((cy, cx))
        for ny, nx in ((cy+1,cx),(cy-1,cx),(cy,cx+1),(cy,cx-1)):
            if 0 <= ny < H and 0 <= nx < W and red[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = 1; st.append((ny, nx))
    if 40 <= len(pts) <= 2000:
        ys, xs = zip(*pts); stars.append([round(sum(xs)/len(xs)/W, 4), round(sum(ys)/len(ys)/H, 4), len(pts)])
json.dump({"size": [W, H], "stars": stars}, open(out / "bull_stars.json", "w"))
print(W, H, len(stars), "stars", sorted(p[2] for p in stars), (out / "bull_light.webp").stat().st_size // 1024, "KB")
