import { chromium } from 'playwright-core';
const [url, out, domain, scheme = 'dark'] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 2, colorScheme: scheme });
await p.goto(url, { waitUntil: 'networkidle' });
await p.evaluate((domain) => {
  const h1 = document.querySelector('h1');
  const row = h1.closest('section') || h1.parentElement.parentElement;   // hero row: text + figure
  const header = document.querySelector('header');
  // keep only header + hero row
  let n = row;
  while (n && n !== document.body) {
    for (const s of [...n.parentElement.children]) if (s !== n && !s.contains(header) && s !== header && s.tagName !== 'SCRIPT' && s.tagName !== 'STYLE') s.style.display = 'none';
    n = n.parentElement;
  }
  // header: brand only
  const brand = header.querySelector('a.logo, a.brand');
  for (const el of header.querySelectorAll('nav, button, a, [class*=toggle], [class*=theme]')) if (!el.contains(brand) && el !== brand) el.style.display = 'none';
  for (const el of row.querySelectorAll('.actions, .btn, .vh, .kicker')) el.style.display = 'none';
  header.style.borderBottom = '0';
  const st = document.createElement('style');
  st.textContent = `html,body{overflow:hidden!important;height:630px} *{animation:none!important;transition:none!important}`;
  document.head.append(st);
  // centre the hero in the space under the header; shrink it if it does not fit
  row.style.margin = '0'; row.style.paddingTop = '0'; row.style.paddingBottom = '0';
  const hb = header.getBoundingClientRect().bottom;
  const r = row.getBoundingClientRect();
  const avail = 630 - hb - 40;
  const k = Math.min(1, avail / r.height);
  const dy = hb + (avail - r.height * k) / 2 + 8 - r.top;
  row.style.transformOrigin = 'top center';
  row.style.transform = `translateY(${dy}px) scale(${k})`;
  const tag = document.createElement('div');
  tag.textContent = domain;
  const ink = getComputedStyle(h1).color;
  Object.assign(tag.style, { position: 'fixed', right: '48px', top: (header.querySelector('a.logo, a.brand').getBoundingClientRect().top + header.querySelector('a.logo, a.brand').getBoundingClientRect().height/2 - 11) + 'px', font: '500 22px/1 ' + getComputedStyle(document.body).fontFamily, color: ink, opacity: '0.72', letterSpacing: '0.01em', zIndex: 9999 });
  document.body.append(tag);
}, domain);
await p.waitForTimeout(800);
await p.screenshot({ path: out });
await b.close();
