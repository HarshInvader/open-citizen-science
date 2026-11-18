"""Three hero options for the parent page. A (the relay) is the live one; B and C are built as preview pages.

A  The relay: four real works on one wall, India to Baghdad to Pisa to Derby. A warm light carries the idea from
   the zero dot to the book, to Fibonacci's numerals, to the orrery's lamp.
B  The orrery, reprinted: Wright of Derby's 1766 painting as an ordered-dither print that spreads out from the lamp.
C  Checked against the sky: al-Sufi's Great Bear (964); his corrected stars light first, then the figure appears.
All images are public domain scans from Wikimedia Commons, prepared by tools/make_art.py.
"""
import html, json
from pathlib import Path

e = html.escape
HERE = Path(__file__).resolve().parent


TITLE = "Big open questions in science, tested in the open."
LEDE = ("How did life begin? Which brain activity goes with conscious experience? What did the Indus cities write? Each project "
        "sets a checkable goal, states its odds plainly, and publishes every result, the failures too. More questions will join.")


def head():
    return f'<h1 id="hero-h">{e(TITLE)}</h1>', f'<p class="lede">{e(LEDE)}</p>'


def gyaan(text):
    """The story behind a picture: shown on hover, or on tap/focus on phones."""
    return f'<span class="gyaan">{text}</span>'


def open_now(projects):
    names = {"indus": "the Indus script", "mind": "consciousness", "origins": "the origin of life"}
    links = [f'<a class="p-{p["slug"]}" href="{e(p["url"])}">{e(names.get(p["slug"], p["name"]))}</a>' for p in projects]
    return f'<p class="open-now">Open now: {", ".join(links[:-1])} and {links[-1]}.</p>' if len(links) > 1 else ""


# (file, width, height, hotspot x, y as fractions, place and time, caption, alt)
RELAY = [
    ("bakhshali.webp", 900, 515, 0.697, 0.877, "India",
     "A dot for &#8216;nothing&#8217; in the Bakhshali manuscript (carbon-dated 3rd to 10th century, still debated). In 628 Brahmagupta made zero a number with its own rules.",
     "A birch-bark page of the Bakhshali manuscript, written in ink"),
    ("library.webp", 640, 662, 0.623, 0.669, "Baghdad",
     "Around 825 al-Khwarizmi wrote on reckoning with the Indian numerals; the Latin title of that book gave us the word &#8216;algorithm&#8217;. (Library scene painted by al-Wasiti, 1237.)",
     "Scholars seated before shelves of books, a library scene painted by al-Wasiti in 1237"),
    ("liber.webp", 560, 856, 0.885, 0.36, "Pisa",
     "In 1202 Fibonacci, who learned the numerals from Arab merchants in B&#233;ja&#239;a, carried &#8216;the nine Indian figures&#8217; into Europe. His rabbit sequence was known to Indian poets centuries earlier.",
     "A page of Fibonacci's Liber Abaci with a column of numerals in the margin"),
    ("orrery.webp", 1100, 814, 0.515, 0.63, "Derby",
     "In 1766 Wright of Derby painted a lecture on a model of the solar system, given to a mixed room of curious people. Science was leaving the academy; his friends were the Lunar Society.",
     "Joseph Wright of Derby's painting of a lecture on the orrery, faces lit by a hidden lamp"),
]


def hero_relay(projects):
    h1, lede = head()
    works = []
    for i, (f, w, h, x, y, when, cap, alt) in enumerate(RELAY):
        pri = "" if i else ' fetchpriority="high"'
        works.append(
            f'<li class="work" tabindex="0" style="--ar:{w / h:.4f};--fx:{x * 100:.1f}%;--fy:{y * 100:.1f}%" data-x="{x}" data-y="{y}">'
            f'<figure><div class="frame"><img src="art/{f}" width="{w}" height="{h}" alt="{e(alt)}" decoding="async"{pri}><span class="glint" aria-hidden="true"></span>{gyaan(cap).replace('class="gyaan"', 'class="gyaan" aria-hidden="true"')}</div>'
            f'<figcaption>{e(when)}<span class="story">{cap}</span></figcaption></figure></li>')
    return f'''<section class="hero hero-relay" aria-labelledby="hero-h">
  <div class="wrap hero-text">{h1}<div>{lede}</div></div>
  <p class="wrap relay-intro">Zero passed from hand to hand, India to Baghdad to Pisa, and became everyone&#8217;s. Science moves fastest when it is shared; these projects share every step. <span class="hint">Hover over a picture for its story.</span></p>
  <div class="wall"><ol class="relay" aria-label="How zero travelled, in four works">{"".join(works)}</ol>
  <svg class="thread" aria-hidden="true"></svg></div>
  <p class="wrap credit">Manuscripts and painting: public domain, via Wikimedia Commons.</p>
</section>'''


RELAY_JS = r"""
(function () {
  var wall = document.querySelector('.hero-relay .wall'); if (!wall) return;
  var works = [].slice.call(wall.querySelectorAll('.work')), svg = wall.querySelector('.thread');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches, NS = 'http://www.w3.org/2000/svg';
  var segs = [], spark, played = false, done = false;
  // where a hotspot (fractions of the picture) lands in the box, allowing for object-fit: cover
  function spot(li) {
    var img = li.querySelector('img'), fr = li.querySelector('.frame'), wr = wall.getBoundingClientRect(), r = fr.getBoundingClientRect();
    var fx = +li.dataset.x, fy = +li.dataset.y, iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
    var s = Math.max(r.width / iw, r.height / ih), dw = iw * s, dh = ih * s;
    var x = (r.width - dw) * fx + fx * dw, y = (r.height - dh) * fy + fy * dh;
    var g = li.querySelector('.glint'); g.style.left = x + 'px'; g.style.top = y + 'px';
    return [r.left - wr.left + x, r.top - wr.top + y];
  }
  function layout() {
    var w = wall.clientWidth, h = wall.clientHeight; svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    svg.setAttribute('width', w); svg.setAttribute('height', h); svg.innerHTML = '';
    var p = works.map(spot), tops = works.map(function (li) { return li.querySelector('.frame').getBoundingClientRect().top - wall.getBoundingClientRect().top; });
    segs = [];
    for (var i = 1; i < p.length; i++) {
      var a = p[i - 1], b = p[i], top = Math.min(tops[i - 1], tops[i]) - 46;  // arc over the frames, through the gap above
      var d = 'M' + a[0] + ' ' + a[1] + ' C' + (a[0] + (b[0] - a[0]) * 0.15) + ' ' + top + ' ' + (a[0] + (b[0] - a[0]) * 0.85) + ' ' + top + ' ' + b[0] + ' ' + b[1];
      var g = document.createElementNS(NS, 'g'), under = document.createElementNS(NS, 'path'), path = document.createElementNS(NS, 'path');
      under.setAttribute('d', d); under.setAttribute('class', 'case'); path.setAttribute('d', d); g.appendChild(under); g.appendChild(path); svg.appendChild(g);
      var L = path.getTotalLength(); [under, path].forEach(function (q) { q.style.strokeDasharray = L; q.style.strokeDashoffset = done ? 0 : L; });
      segs.push([path, L, under]);
    }
    spark = document.createElementNS(NS, 'circle'); spark.setAttribute('r', 3.5); spark.setAttribute('class', 'spark'); svg.appendChild(spark);
  }
  function light(i) { works[i].classList.add('lit'); }
  function run(seg, ms, cb) {
    var t0 = performance.now(), path = seg[0], L = seg[1]; spark.style.opacity = 1;
    (function step(t) {
      var k = Math.min(1, (t - t0) / ms), q = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2, pt = path.getPointAtLength(L * q);
      path.style.strokeDashoffset = seg[2].style.strokeDashoffset = L * (1 - q); spark.setAttribute('cx', pt.x); spark.setAttribute('cy', pt.y);
      if (k < 1) requestAnimationFrame(step); else { spark.style.opacity = 0; cb(); }
    })(t0);
  }
  function play() {
    if (played) return; played = true; layout();
    if (still) { works.forEach(function (w, i) { light(i); }); done = true; layout(); wall.classList.add('done'); return; }
    var i = 0; light(0);
    (function next() {
      if (i >= segs.length) { done = true; wall.classList.add('done'); return; }
      setTimeout(function () { run(segs[i], 1100, function () { i++; light(i); next(); }); }, 900);
    })();
  }
  var imgs = works.map(function (w) { return w.querySelector('img'); });
  var ready = Promise.all(imgs.map(function (im) { return im.complete ? 0 : new Promise(function (r) { im.onload = im.onerror = r; }); }));
  Promise.race([ready, new Promise(function (r) { setTimeout(r, 2500); })]).then(function () { setTimeout(play, 350); });
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { if (played) layout(); }, 120); });
})();
"""


def hero_orrery(projects):
    h1, lede = head()
    return f'''<section class="wrap hero hero-orrery" aria-labelledby="hero-h">
  <div class="ho-text">{h1}{lede}</div>
  <figure class="ho-fig" tabindex="0"><div class="ho-plate"><canvas width="340" height="252" aria-hidden="true"></canvas>
  <img src="art/orrery.webp" width="1100" height="814" alt="Joseph Wright of Derby's painting of a lecture on the orrery, printed in dots">{gyaan("In the 1760s a dozen friends, the Lunar Society, met each full moon to work on the hardest questions of their day. We do the same, with AI agents.")}</div>
  <figcaption>Joseph Wright of Derby, 1766. Ordinary people round a model of the sky.</figcaption></figure>
</section>'''


ORRERY_JS = r"""
(function () {
  var fig = document.querySelector('.ho-fig'); if (!fig) return;
  var cv = fig.querySelector('canvas'), cx = cv.getContext('2d'), W = cv.width, H = cv.height, LX = 175, LY = 160;
  var src = new Image(); src.src = 'art/orrery_grey.png';
  var B = [0,48,12,60,3,51,15,63,32,16,44,28,35,19,47,31,8,56,4,52,11,59,7,55,40,24,36,20,43,27,39,23,2,50,14,62,1,49,13,61,34,18,46,30,33,17,45,29,10,58,6,54,9,57,5,53,42,26,38,22,41,25,37,21];
  function css(n) { return getComputedStyle(fig).getPropertyValue(n).trim(); }
  function rgb(h) { h = h.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  src.onload = function () {
    var o = document.createElement('canvas'); o.width = W; o.height = H; var oc = o.getContext('2d'); oc.drawImage(src, 0, 0, W, H);
    var lum = oc.getImageData(0, 0, W, H).data, out = cx.createImageData(W, H), dark = css('--plate-mode') === 'dark';
    var ink = rgb(css('--dot')), warm = rgb(css('--warm')), Rmax = Math.hypot(W, H);
    function draw(R, flick) {
      var d = out.data;
      for (var y = 0; y < H; y++) for (var x = 0; x < W; x++) {
        var i = (y * W + x) * 4, l = lum[i] / 255, v = Math.max(0, (dark ? l : 1 - l) - 0.08);
        var ox = (x - W / 2) / (W / 2), oy = (y - H / 2) / (H / 2), edge = Math.max(0, Math.min(1, (1 - Math.hypot(ox, oy)) / 0.35));
        var dist = Math.hypot(x - LX, y - LY), Lr = Math.max(0, Math.min(1, 1 - (dist - R) / 40));
        if (dist < 60 && flick) Lr *= flick;
        var on = v * Lr * edge * edge > (B[(y % 8) * 8 + x % 8] + 0.5) / 64, lamp = dist < 7 && l > 0.5;
        var c = lamp ? warm : ink; d[i] = c[0]; d[i + 1] = c[1]; d[i + 2] = c[2]; d[i + 3] = on || lamp ? 255 : 0;
      }
      cx.putImageData(out, 0, 0);
    }
    fig.classList.add('live');
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { draw(Rmax); fig.classList.add('done'); return; }
    var t0 = performance.now(), last = 0;
    (function step(t) {
      var k = (t - t0 - 300) / 2300;
      if (t - last > 83) { last = t; if (k < 0) draw(0); else if (k < 1) draw(Rmax * (1 - Math.pow(1 - k, 3))); else { draw(Rmax); fig.classList.add('done'); return; } }
      requestAnimationFrame(step);
    })(t0);
  };
})();
"""


def hero_sufi(projects):
    stars = [s for s in json.loads((HERE / "art" / "sufi_stars.json").read_text()) if s[2] >= 50]
    stars.sort(key=lambda s: s[0])
    h1, lede = head()
    dots = "".join(f'<span class="star" style="left:{x * 100:.2f}%;top:{y * 100:.2f}%;--i:{i}"></span>' for i, (x, y, _) in enumerate(stars))
    return f'''<section class="wrap hero hero-sufi" aria-labelledby="hero-h">
  <div class="hs-text">{h1}{lede}</div>
  <figure class="hs-fig" tabindex="0"><div class="hs-plate"><img class="for-light" src="art/sufi_light.webp" width="900" height="888" alt="The Great Bear from al-Sufi's Book of Fixed Stars, its stars marked in red"><img class="for-dark" src="art/sufi_dark.webp" width="900" height="888" alt="">{dots}{gyaan("In 964 al-Sufi took the star catalogue everyone trusted and checked every star against the night sky, fixing what was wrong. We check today&#8217;s biggest ideas the same way.")}</div>
  <figcaption>&#8216;Abd al-Rahman al-Sufi, <i>Book of the Fixed Stars</i>. The Great Bear, its stars in red. Copy of about 1009, Bodleian Library, Oxford (MS Marsh 144); public domain, via <a class="src" href="https://commons.wikimedia.org/wiki/File:Al_Sufi_-_Book_of_Fixed_Stars_-_Ursa_Major_(The_Great_Bear)_-_Bodleian_Library_-_Marsh_144(illustrationonly).jpg">Wikimedia Commons</a>.</figcaption></figure>
</section>'''


SUFI_JS = r"""
(function () { var f = document.querySelector('.hs-fig'); if (f) requestAnimationFrame(function () { f.classList.add('stars-on'); }); })();
"""

HEROES = {"a": (hero_relay, RELAY_JS), "b": (hero_orrery, ORRERY_JS), "c": (hero_sufi, SUFI_JS)}
