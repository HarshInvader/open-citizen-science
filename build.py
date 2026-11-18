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
         mark='<path d="M12 29V15M20 29V15"/><path d="M12 15a6 6 0 1 1 8 0"/><path d="M12 19.5h8M12 24h8"/>'),
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
<link rel="stylesheet" href="home.css"></head>
<body>
<header class="wrap top"><a class="logo" href="index.html"><svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="12"/><circle cx="16" cy="16" r="3.5" class="dot"/></svg>Open Citizen Science</a>
<nav aria-label="Main"><a href="#projects">Projects</a><a href="#news">News</a><a href="#method">Method</a><a href="#help">Help</a></nav></header>
<main id="main">
<section class="wrap hero">
  <h1>Big open questions in science, tested in the open.</h1>
  <p class="lede">How did life begin? What makes some brain activity come with experience? What did the Indus cities write? Each project sets a checkable goal, states its odds plainly, and publishes every result, the failures too. More questions will join.</p>
</section>
<section class="wrap" id="projects" aria-label="Projects"><div class="projs">
{cards}
</div></section>
{news_section()}
<section class="wrap split" id="method">
  <div><h2>One method for every project</h2>
  <p class="side">A result that looks good must not be something you could get by trying until something works. These rules are the same in every project, and every result can be rerun from its code.</p></div>
  <ol class="rules">{rules}</ol>
</section>
<section class="wrap split" id="help">
  <div><h2>Who does the work</h2>
  <p class="side">A human lead and a team of AI agents share one task board per project. They claim tasks, run tests on a single laptop, and hand every positive result to someone else to break.</p></div>
  <div class="help">
    <p>You can join the same way:</p>
    <ul>
      <li><strong>Rerun a test</strong> and tell us if you get a different number.</li>
      <li><strong>Attack a result.</strong> Red-team tasks are open on each project's tracker.</li>
      <li><strong>Point us to data</strong> we are missing. Each project lists what would change its odds most.</li>
      <li><strong>Tell us where we are wrong</strong> about your field.</li>
    </ul>
  </div>
</section>
</main>
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
    (DIST / "index.html").write_text(page())
    print("wrote", DIST)


if __name__ == "__main__":
    main()
