#!/usr/bin/env python3
"""Build the Open Citizen Science site: the parent page plus the projects inside it.

Run from this folder:  python3 -I build.py
Writes dist/index.html and copies each project's built site into dist/<slug>/.
Open Indus already has its own address, so the parent page links to it instead of copying it.
"""
import html, json, shutil, sqlite3, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PERSONAL = HERE.parent
DIST = HERE / "dist"
e = html.escape

# Each project. ladder: one value per level L0-L4 (1 = done, 0.5 = partly, 0 = open).
PROJECTS = [
    dict(slug="indus", name="Open Indus", repo=PERSONAL / "indus-decipher", url="https://openindus.pages.dev", external=True,
         question="What did the Indus cities write?",
         goal="Decipher the Indus script by 2027",
         blurb="Four thousand short texts survive from a civilisation as large as Egypt's, and nobody can read them. We test every claimed reading, and our own ideas, against chance.",
         odds="under 1 in 10", ladder=[1, 0.5, 0, 0, 0], ladder_names=["Structure", "Sign roles", "Topic", "Meaning", "Sound"],
         mark='<path d="M16 3.56C9.18 9.28 8.74 16.32 16 23.14L21.05 27.88"/><path d="M16 3.56C22.82 9.28 23.26 16.32 16 23.14L10.95 27.88"/><path d="M11.71 17.44L8.67 19.82M20.29 17.44L23.33 19.82"/>'),
    dict(slug="mind", name="Open Mind", repo=PERSONAL / "open-mind", url="mind/index.html", external=False,
         question="Which brain activity comes with experience?",
         goal="Find the most accurate theory of human consciousness by 2027",
         blurb="Every current theory may be wrong. We test their riskiest predictions on open brain recordings, list the hard facts any true theory must explain, and build our own theory where theirs fail.",
         odds="3 to 5 in 100", ladder=[1, 1, 0.5, 0.5, 0], ladder_names=["Signal", "State", "Dissociation", "Content", "Theory"],
         mark='<path d="M5 12h14v14H5z"/><path d="M13 6h14v14H13z"/><path d="M5 12l8-6M19 12l8-6M19 26l8-6M5 26l8-6"/>'),
    dict(slug="origins", name="Open Origins", repo=PERSONAL / "open-origins", url="origins/index.html", external=False,
         question="How did chemistry become life?",
         goal="Map and test every route to the origin of life by 2027",
         blurb="Chemists have shown many single steps from simple molecules toward life, but nobody has joined them into one continuous route. We score each route step by step and seal predictions that future data can confirm.",
         odds="about 1 in 8 for the open goal", ladder=[1, 0.5, 0.5, 0, 0], ladder_names=["Building blocks", "Polymers", "Copying", "Self-replication", "Evolution"],
         mark='<path stroke-width="1.5" d="M3 27C8 27 10 19.5 16 19.5S24 27 29 27M3 23.8C8 23.8 10 16.3 16 16.3S24 23.8 29 23.8M3 20.6C8 20.6 10 13.1 16 13.1S24 20.6 29 20.6M3 17.4C8 17.4 10 9.9 16 9.9S24 17.4 29 17.4M3 14.2C8 14.2 10 6.7 16 6.7S24 14.2 29 14.2"/>'),
]

RULES = [
    ("Seal it before you look.", "Every prediction, test and pass mark is written down and fingerprinted (SHA-256) before any result is seen."),
    ("Test on data it never saw.", "Part of the data is held back, and near-copies of it never reach the people building the idea."),
    ("Plant an answer first.", "A method must recover a known, planted answer at the same scale before anything it says about the real data counts."),
    ("Let someone else try to break it.", "Every positive result goes to a red team that did not produce it."),
    ("Publish it either way.", "Failures are written up with the size of effect the test could have caught."),
]


def board_stats(repo):
    db = repo / "board" / "board.db"
    if not db.exists():
        return None
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    tasks = c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    landed = c.execute("SELECT COUNT(*) FROM landed").fetchone()[0]
    hashes = repo / "docs" / "prereg" / "HASHES.txt"
    sealed = sum(1 for l in hashes.read_text().splitlines() if l.strip()) if hashes.exists() else 0
    return tasks, landed, sealed


def latest_news(n=8):
    rows = []
    for p in PROJECTS:
        f = p["repo"] / "site" / "news.json"
        if not f.exists():
            continue
        for it in json.loads(f.read_text())["items"]:
            if it.get("section") == "landmark":
                continue
            base = p["url"].rsplit("/", 1)[0] if not p["external"] else p["url"]
            rows.append(dict(p=p, date=str(it.get("date", "")), head=it.get("head", ""), gist=it.get("gist", ""),
                             url=f"{base}/news-{it['id']}.html"))
    rows.sort(key=lambda r: r["date"], reverse=True)
    out = []  # the newest few from each project, then by date
    for p in PROJECTS:
        out += [r for r in rows if r["p"] is p][:3]
    return sorted(out, key=lambda r: r["date"], reverse=True)


def news_section():
    items = "".join(f'''<li class="p-{r["p"]["slug"]}"><a href="{e(r["url"])}"><span class="nmeta"><span class="ntag">{e(r["p"]["name"])}</span>{e(r["date"])}</span>
<span><span class="nhead">{e(r["head"])}</span><span class="ngist">{e(r["gist"])}</span></span></a></li>''' for r in latest_news())
    links = " · ".join(f'<a href="{e((p["url"].rsplit("/", 1)[0] if not p["external"] else p["url"]) + "/news.html")}">{e(p["name"])}</a>' for p in PROJECTS)
    return f'''<section class="wrap news" id="news"><div class="news-head"><h2>Latest from the projects</h2><p>All news: {links}</p></div><ul class="nlist">{items}</ul></section>'''


def meter(p):
    segs = "".join(f'<li class="seg s{int(v * 2)}"><span class="vh">{e(n)}: {"done" if v == 1 else "partly" if v else "open"}</span></li>'
                   for v, n in zip(p["ladder"], p["ladder_names"]))
    labels = f'<span>{e(p["ladder_names"][0])}</span><span>{e(p["ladder_names"][-1])}</span>'
    return f'<div class="meter"><ol class="segs" aria-label="Where the question stands, five levels">{segs}</ol><div class="ends">{labels}</div></div>'


def card(p):
    s = board_stats(p["repo"])
    if s and s[1]:
        stat = f"{s[1]} results landed · {s[2]} sealed pre-registrations"
    elif s:
        stat = f"Just started · {s[0]} tasks on the board"
    else:
        stat = "Just started"
    target = ' rel="noopener"' if p["external"] else ""
    return f"""<article class="proj p-{p['slug']}">
  <div class="proj-head">
    <svg class="mark" viewBox="0 0 32 32" aria-hidden="true">{p['mark']}</svg>
    <div><p class="pname">{e(p['name'])}</p><p class="pstat">{e(stat)}</p></div>
  </div>
  <h3>{e(p['question'])}</h3>
  <p class="pgoal">{e(p['goal'])}.</p>
  <p class="pblurb">{e(p['blurb'])}</p>
  {meter(p)}
  <div class="proj-foot"><p class="odds"><span>Honest odds by 2027</span>{e(p['odds'])}</p>
  <a class="go" href="{e(p['url'])}"{target}>Open {e(p['name'].split()[1])}<span aria-hidden="true"> →</span></a></div>
</article>"""


def page():
    cards = "\n".join(card(p) for p in PROJECTS)
    rules = "".join(f"<li><div><strong>{e(a)}</strong> {e(b)}</div></li>" for a, b in RULES)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Open Citizen Science</title>
<meta name="description" content="Big open questions in science, tested in the open by a human lead, a team of AI agents and anyone who wants to help.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='12' fill='none' stroke='%231B1A17' stroke-width='3'/%3E%3Ccircle cx='16' cy='16' r='3.5' fill='%231B1A17'/%3E%3C/svg%3E">
<link rel="preload" href="fonts/OpenIndusText-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="home.css"></head>
<body>
<header class="wrap top"><a class="logo" href="index.html"><svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="12"/><circle cx="16" cy="16" r="3.5" class="dot"/></svg>Open Citizen Science</a>
<button class="menu" type="button" aria-expanded="false" aria-controls="mainnav">Menu</button><nav aria-label="Main" id="mainnav"><a href="#projects">Projects</a><a href="#why">Why agents</a><a href="#news">News</a><a href="#method">Method</a><a href="#help">Contribute</a></nav></header>
<main id="main">
<section class="wrap hero">
  <h1>Big open questions in science, tested in the open.</h1>
  <p class="lede">How did life begin? What makes some brain activity come with experience? What did the Indus cities write? Each project sets a checkable goal, states its odds plainly, and publishes every result, the failures too. More questions will join.</p>
</section>
<section class="wrap" id="projects" aria-label="Projects"><div class="projs">
{cards}
</div></section>
<section class="wrap why" id="why">
  <h2>Agents make the slow part of science cheap</h2>
  <p class="side">Big questions rarely stall for lack of ideas. They stall because testing each idea takes people, money and years. An agent can run a test overnight, so a small open group can now try what once needed a national lab.</p>
  <ol class="why-grid"><li class="why-card"><figure><svg viewBox="0 0 240 150" role="img" aria-label="An accepted framework tipping over as unexplained results pile up beside it">
<line x1="10" y1="131" x2="230" y2="131" class="f-ground"/>
<g transform="rotate(-7 20 131)"><rect x="20" y="36" width="112" height="95" rx="8" class="f-line"/><circle cx="38" cy="58" r="3.2" class="f-solid"/><circle cx="58" cy="58" r="3.2" class="f-solid"/><circle cx="78" cy="58" r="3.2" class="f-solid"/><circle cx="98" cy="58" r="3.2" class="f-solid"/><circle cx="118" cy="58" r="3.2" class="f-solid"/><circle cx="38" cy="78" r="3.2" class="f-solid"/><circle cx="58" cy="78" r="3.2" class="f-solid"/><circle cx="78" cy="78" r="3.2" class="f-solid"/><circle cx="98" cy="78" r="3.2" class="f-solid"/><circle cx="118" cy="78" r="3.2" class="f-solid"/><circle cx="38" cy="98" r="3.2" class="f-solid"/><circle cx="58" cy="98" r="3.2" class="f-solid"/><circle cx="78" cy="98" r="3.2" class="f-solid"/><circle cx="98" cy="98" r="3.2" class="f-solid"/><circle cx="118" cy="98" r="3.2" class="f-solid"/></g>
<circle cx="146.0" cy="124" r="6" class="f-acc"/><circle cx="161.0" cy="124" r="6" class="f-acc"/><circle cx="176.0" cy="124" r="6" class="f-acc"/><circle cx="191.0" cy="124" r="6" class="f-acc"/><circle cx="206.0" cy="124" r="6" class="f-acc"/><circle cx="153.5" cy="111" r="6" class="f-acc"/><circle cx="168.5" cy="111" r="6" class="f-acc"/><circle cx="183.5" cy="111" r="6" class="f-acc"/><circle cx="198.5" cy="111" r="6" class="f-acc"/><circle cx="161.0" cy="98" r="6" class="f-acc"/><circle cx="176.0" cy="98" r="6" class="f-acc"/><circle cx="191.0" cy="98" r="6" class="f-acc"/><circle cx="168.5" cy="85" r="6" class="f-acc"/><circle cx="183.5" cy="85" r="6" class="f-acc"/><circle cx="176.0" cy="72" r="6" class="f-acc"/>
<text x="22" y="22" class="f-lab">Framework</text><text x="226" y="58" class="f-lab acc" text-anchor="end">Unexplained</text>
</svg></figure><h3>Fields change when failures pile up</h3><p><a class="book" href="https://usecaddie.app/s/the-structure-of-scientific-revolutions-50th">Kuhn&#8217;s <i>The Structure of Scientific Revolutions</i></a> shows a field shifts only when results it cannot explain become too many to ignore. Agents test ideas by the thousand, and sealed tests keep every failure on the record.</p></li><li class="why-card"><figure><svg viewBox="0 0 240 150" role="img" aria-label="A chemist, a statistician and a sceptic all feeding into one task">
<path d="M104 34 C140 34 140 75 172 75" class="f-line"/><path d="M104 75 C140 75 140 75 172 75" class="f-line"/><path d="M104 116 C140 116 140 75 172 75" class="f-line"/><circle cx="98" cy="34" r="6" class="f-solid"/><text x="86" y="38" class="f-lab" text-anchor="end">Chemist</text><circle cx="98" cy="75" r="6" class="f-solid"/><text x="86" y="79" class="f-lab" text-anchor="end">Statistician</text><circle cx="98" cy="116" r="6" class="f-solid"/><text x="86" y="120" class="f-lab" text-anchor="end">Sceptic</text><rect x="172" y="57" width="36" height="36" rx="6" class="f-acc"/>
<text x="190" y="114" class="f-lab acc" text-anchor="middle">One task</text>
</svg></figure><h3>Discoveries come from mixing experts</h3><p>Bell Labs put physicists, chemists and engineers in the same corridors, and the transistor came out of it. An agent team brings any expert to a task on demand.</p></li><li class="why-card"><figure><svg viewBox="0 0 240 150" role="img" aria-label="People and agents seated in a ring around a full moon">
<circle cx="120" cy="75" r="24" class="f-moon"/><circle cx="120.0" cy="23.0" r="6" class="f-line"/><rect x="141.0" y="25.0" width="10" height="10" rx="2" class="f-solid"/><circle cx="165.0" cy="49.0" r="6" class="f-line"/><rect x="167.0" y="70.0" width="10" height="10" rx="2" class="f-solid"/><circle cx="165.0" cy="101.0" r="6" class="f-line"/><rect x="141.0" y="115.0" width="10" height="10" rx="2" class="f-solid"/><circle cx="120.0" cy="127.0" r="6" class="f-line"/><rect x="89.0" y="115.0" width="10" height="10" rx="2" class="f-solid"/><circle cx="75.0" cy="101.0" r="6" class="f-line"/><rect x="63.0" y="70.0" width="10" height="10" rx="2" class="f-solid"/><circle cx="75.0" cy="49.0" r="6" class="f-line"/><rect x="89.0" y="25.0" width="10" height="10" rx="2" class="f-solid"/>
<circle cx="18" cy="140" r="5" class="f-line"/><text x="28" y="144.5" class="f-lab">People</text><rect x="168" y="135" width="10" height="10" rx="2" class="f-solid"/><text x="184" y="144.5" class="f-lab">Agents</text>
</svg></figure><h3>A small circle can be enough</h3><p>The Lunar Society was a dozen friends, among them Watt, Wedgwood and Erasmus Darwin, who met each full moon. We are that circle again, with agents, and anyone can join.</p></li></ol>
  <p class="why-note">Agents can also fool themselves faster than people can, so every project follows <a href="#method">the same rules</a>.</p>
</section>
{news_section()}
<section class="wrap split" id="method">
  <div><h2>One method for every project</h2>
  <p class="side">A result that looks good must not be something you could get by trying until something works. These rules are the same in every project, and every result can be rerun from its code.</p></div>
  <ol class="rules">{rules}</ol>
</section>
<section class="wrap split" id="help">
  <div><h2>Contribute</h2>
  <p class="side">A human lead and a team of AI agents share one task board per project. You can add your own agent to the team, and each task it takes is a test we could not otherwise afford to run.</p></div>
  <div class="help">
    <p>Point your AI agent, on your own subscription, at an open task. Each project gives a ready-made prompt per task: <a href="mind/contribute.html">Open Mind</a>, <a href="origins/contribute.html">Open Origins</a>, <a href="https://openindus.pages.dev/contribute">Open Indus</a>. Your agent seals its plan, checks a planted answer, runs the test and sends the result back as a pull request, whichever way it goes.</p>
    <p>Other ways to help:</p>
    <ul>
      <li><strong>Rerun a test</strong> and tell us if you get a different number.</li>
      <li><strong>Attack a result.</strong> Red-team tasks are open on each project's tracker.</li>
      <li><strong>Point us to data</strong> we are missing. Each project lists what would change its odds most.</li>
      <li><strong>Tell us where we are wrong</strong> about your field.</li>
    </ul>
  </div>
</section>
</main>
<script>(function(){{var b=document.querySelector(".menu"),n=document.getElementById("mainnav");b.addEventListener("click",function(){{var o=n.classList.toggle("open");b.setAttribute("aria-expanded",o)}});n.addEventListener("click",function(e){{if(e.target.tagName==="A"){{n.classList.remove("open");b.setAttribute("aria-expanded","false")}}}})}})();</script>
<footer class="wrap foot"><span>Open Citizen Science</span><span>Open code, open data, open results: <a href="https://github.com/HarshInvader/open-citizen-science">GitHub</a>. Updated {time.strftime('%d %b %Y').lstrip('0')}.</span></footer>
</body></html>"""


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for p in PROJECTS:
        if p["external"]:
            continue
        subprocess.run([sys.executable, "-I", "site/build.py"], cwd=p["repo"], check=True)
        shutil.copytree(p["repo"] / "site" / "dist", DIST / p["slug"])
    shutil.copy(HERE / "home.css", DIST / "home.css")
    shutil.copytree(HERE / "fonts", DIST / "fonts")
    (DIST / "index.html").write_text(page())
    print("wrote", DIST)


if __name__ == "__main__":
    main()
