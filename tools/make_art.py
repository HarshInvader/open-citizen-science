"""Prepare the hero images from public-domain scans (Wikimedia Commons).
Usage: python -I tools/make_art.py <download dir>   (needs Pillow + numpy)
Writes art/*.webp, art/orrery_grey.png (the dot-print source) and art/sufi_stars.json."""
import json, sys
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter
import numpy as np

src = Path(sys.argv[1]); out = Path(__file__).resolve().parent.parent / "art"; out.mkdir(exist_ok=True)

def save(im, name, w, q=74):
    im = im.convert("RGB"); h = round(im.height * w / im.width)
    im.resize((w, h), Image.LANCZOS).save(out / name, "WEBP", quality=q, method=6)
    print(name, w, h, (out / name).stat().st_size // 1024, "KB")

save(Image.open(src / "bakhshali.jpg"), "bakhshali.webp", 900)
lib = Image.open(src / "library.jpg"); save(lib.crop((26, 218, 1894, 2150)), "library.webp", 640)
save(Image.open(src / "liber.jpg"), "liber.webp", 560)
orr = Image.open(src / "orrery.jpg"); save(orr, "orrery.webp", 1100)

# dot-print source: greyscale, contrast stretch, gamma 0.8, light unsharp
g = ImageOps.autocontrast(orr.convert("L"), cutoff=1).resize((340, 252), Image.LANCZOS)
a = np.asarray(g, dtype=np.float32) / 255
g = Image.fromarray((np.clip(a ** 0.8, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
g.save(out / "orrery_grey.png", optimize=True); print("orrery_grey.png", g.size)

# al-Sufi's Great Bear: the drawing, plus the red star dots found by colour
s = Image.open(src / "sufi.jpg").convert("RGB")
pass  # sufi is saved below in light and dark
a = np.asarray(s.resize((900, round(s.height * 900 / s.width))), dtype=np.int16)
r, gg, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 120) & (r - gg > 55) & (r - b > 45)
# connected blobs by flood fill
H, W = red.shape; seen = np.zeros_like(red); stars = []
for y, x in zip(*np.nonzero(red)):
    if seen[y, x]: continue
    stack = [(y, x)]; seen[y, x] = 1; pts = []
    while stack:
        cy, cx = stack.pop(); pts.append((cy, cx))
        for ny, nx in ((cy+1,cx),(cy-1,cx),(cy,cx+1),(cy,cx-1)):
            if 0 <= ny < H and 0 <= nx < W and red[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = 1; stack.append((ny, nx))
    if 6 <= len(pts) <= 400:
        ys, xs = zip(*pts); stars.append([round(sum(xs)/len(xs)/W, 4), round(sum(ys)/len(ys)/H, 4), len(pts)])
json.dump(stars, open(out / "sufi_stars.json", "w")); print(len(stars), "red blobs")

# al-Sufi on either page colour: paper becomes transparent; the dark version flips light and dark but keeps hues
a = np.asarray(s.resize((900, round(s.height * 900 / s.width)), Image.LANCZOS).convert("RGB"), dtype=np.float32)
alpha = np.clip((255 - a.min(axis=2) - 6) * 3.2, 0, 255)
Image.fromarray(np.dstack([a, alpha]).astype(np.uint8), "RGBA").save(out / "sufi_light.webp", "WEBP", quality=78, method=6)
hsv = np.asarray(Image.fromarray(a.astype(np.uint8)).convert("HSV"), dtype=np.float32)
hsv[..., 2] = 255 - hsv[..., 2] * 0.75 - 20            # flip brightness
hsv[..., 2] = np.clip(np.where(hsv[..., 1] > 90, 255 - hsv[..., 2] + 60, hsv[..., 2]), 0, 255)  # keep coloured marks bright
dark = np.asarray(Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB"), dtype=np.float32)
Image.fromarray(np.dstack([dark, alpha]).astype(np.uint8), "RGBA").save(out / "sufi_dark.webp", "WEBP", quality=78, method=6)
print("sufi light/dark", (out / "sufi_light.webp").stat().st_size // 1024, (out / "sufi_dark.webp").stat().st_size // 1024, "KB")
