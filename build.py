#!/usr/bin/env python3
"""Build the Open Citizen Science site: the parent page plus the projects inside it.

Run from this folder:  python3 -I build.py
Writes dist/index.html and copies each project's built site into dist/<slug>/.
Open Indus already has its own address, so the parent page links to it instead of copying it.
"""
import html, json, shutil, sqlite3, subprocess, sys, time
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from hero import HEROES
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
         odds="under 10%", ladder=[1, 0.5, 0, 0, 0], ladder_names=["Structure", "Sign roles", "Topic", "Meaning", "Sound"],
         mark='<path d="M16 3.56C9.18 9.28 8.74 16.32 16 23.14L21.05 27.88"/><path d="M16 3.56C22.82 9.28 23.26 16.32 16 23.14L10.95 27.88"/><path d="M11.71 17.44L8.67 19.82M20.29 17.44L23.33 19.82"/>'),
    dict(slug="mind", name="Open Mind", repo=PERSONAL / "open-mind", url="mind/index.html", external=False,
         question="Which brain activity goes with conscious experience?",
         goal="Find the most accurate theory of human consciousness by 2027",
         blurb="Every current theory may be wrong. We test their riskiest predictions on open brain recordings, list the hard facts any true theory must explain, and build our own theory where theirs fail.",
         odds="3 to 5%", ladder=[1, 1, 0.5, 0.5, 0], ladder_names=["Signal", "State", "Dissociation", "Content", "Theory"],
         mark='<path d="M5 12h14v14H5z"/><path d="M13 6h14v14H13z"/><path d="M5 12l8-6M19 12l8-6M19 26l8-6M5 26l8-6"/>'),
    dict(slug="origins", name="Open Origins", repo=PERSONAL / "open-origins", url="origins/index.html", external=False,
         question="How did chemistry become life?",
         goal="Map and test every route to the origin of life by 2027",
         blurb="Chemists have shown many single steps from simple molecules toward life, but nobody has joined them into one continuous route. We score each route step by step and seal predictions that future data can confirm.",
         odds="about 12%", ladder=[1, 0.5, 0.5, 0, 0], ladder_names=["Building blocks", "Polymers", "Copying", "Self-replication", "Evolution"],
         mark='<path stroke-width="1.5" d="M3 27C8 27 10 19.5 16 19.5S24 27 29 27M3 23.8C8 23.8 10 16.3 16 16.3S24 23.8 29 23.8M3 20.6C8 20.6 10 13.1 16 13.1S24 20.6 29 20.6M3 17.4C8 17.4 10 9.9 16 9.9S24 17.4 29 17.4M3 14.2C8 14.2 10 6.7 16 6.7S24 14.2 29 14.2"/>'),
]

RULES = [
    ("Seal it before you look.", "Every prediction, test and pass mark is written down and given a digital fingerprint that is published before any result is seen, so it cannot be quietly changed later."),
    ("Test on data it never saw.", "Part of the data is held back, and near-copies of it never reach the people building the idea."),
    ("Plant an answer first.", "We hide an answer we already know in practice data. If a method cannot find it there, we do not trust what it says about the real data."),
    ("Let someone else try to break it.", "Every positive result goes to a separate team, of people and agents, whose job is to find the flaw."),
    ("Publish it either way.", "Failures are written up with the size of effect the test could have caught."),
]


# The plain answers a first-time visitor asks for: what is this, who is it for, why these questions, what counts as success.
ABOUT = [
    ("What this is", "A public lab notebook. Agents test ideas on existing data; every result is published, failures too."),
    ("Who it is for", "Researchers who want to check or reuse the work, and anyone with an AI assistant who wants to help."),
    ("Why these questions", "Famous, unsolved, testable on open data, and an answer would be clearly right or wrong."),
    ("The goal", "A checkable result on at least one by 2027. If we fail, everything stays public for the next team."),
]


def about_section():
    cards = "".join(f'<li><h3>{e(h)}</h3><p>{e(t)}</p></li>' for h, t in ABOUT)
    return (f'<section class="wrap about" id="about" aria-labelledby="about-h"><h2 id="about-h" class="vh">About this site</h2>'
            f'<ul class="about-grid">{cards}</ul>'
            f'<p class="about-cta"><a class="btn btn-1" href="#projects">See the three projects</a>'
            f'<a class="btn btn-2" href="#help">How to help</a></p></section>')


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


def thumb_for(p, base, nid):
    """The item's own drawing, if the project made one (each project writes assets/news/<id>.webp)."""
    site = p["repo"] / "site"
    if (site / "assets" / "news" / f"{nid}.webp").exists() or (site / "dist" / "assets" / "news" / f"{nid}.webp").exists():
        return f"{base}/assets/news/{nid}.webp"
    return ""


MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def human_date(d):
    """2026-07-22 -> 22 Jul 2026; 2026-10 -> Oct 2026; anything else as given."""
    p = d.split("-")
    try:
        if len(p) == 3: return f"{int(p[2])} {MONTHS[int(p[1]) - 1]} {p[0]}"
        if len(p) == 2: return f"{MONTHS[int(p[1]) - 1]} {p[0]}"
    except (ValueError, IndexError):
        pass
    return e(d)


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
                             url=f"{base}/news-{it['id']}.html", thumb=thumb_for(p, base, it["id"])))
    rows.sort(key=lambda r: r["date"], reverse=True)
    out = []  # the newest few from each project, then by date
    for p in PROJECTS:
        out += [r for r in rows if r["p"] is p][:3]
    return sorted(out, key=lambda r: r["date"], reverse=True)


SIGNUP = ('<form class="nsignup" action="/api/subscribe" method="post"><div class="nsu-text"><p class="nsu-h">Get the important new papers by email</p>'
          '<p class="nsu-p">Every couple of weeks: the papers that matter for these questions, in plain words, and what each project did with them. Unsubscribe in one click.</p>'
          '<fieldset class="nsu-pick"><legend class="vh">Which projects</legend>'
          + "".join(f'<label><input type="checkbox" name="projects" value="{s}" checked> {n}</label>' for s, n in (("mind", "Open Mind"), ("origins", "Open Origins"), ("indus", "Open Indus")))
          + '</fieldset></div><div class="nsu-row"><label class="vh" for="nsu-email">Email address</label><input id="nsu-email" type="email" name="email" required autocomplete="email" placeholder="you@example.com">'
          '<input type="hidden" name="source" value="home"><input class="nsu-hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">'
          '<button type="submit">Subscribe</button></div><p class="nsu-msg" role="status" aria-live="polite"></p></form>')
SIGNUP_JS = r"""(function(){var s=document.querySelector('.nsignup');if(!s)return;s.addEventListener('submit',function(ev){ev.preventDefault();
var m=s.querySelector('.nsu-msg'),b=s.querySelector('button'),p=[].map.call(s.querySelectorAll('input[name=projects]:checked'),function(x){return x.value});
if(!p.length){m.textContent='Pick at least one project.';return}b.disabled=true;m.textContent='Saving…';
fetch(s.action,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:s.email.value,projects:p,source:'home',website:s.website.value})})
.then(function(r){return r.json()}).then(function(r){if(r.ok){m.textContent='Thanks. You’re on the list.';s.classList.add('done')}else{m.textContent=r.error||'Something went wrong. Please try again.';b.disabled=false}})
.catch(function(){m.textContent='Could not reach the server. Please try again.';b.disabled=false})})})();"""


def news_section():
    def paperish(h):  # a raw paper title reads badly as a headline: lead with the plain summary instead
        return len(h) > 75 or " et al" in h or "(" in h
    def body(r):
        if paperish(r["head"]) and r["gist"]:
            return f'<span class="nhead">{e(r["gist"])}</span><span class="ngist">Paper: {e(r["head"])}</span>'
        return f'<span class="nhead">{e(r["head"])}</span><span class="ngist">{e(r["gist"])}</span>'
    def pic(r):
        return (f'<span class="nthumb"><img src="{e(r["thumb"])}" alt="" loading="lazy" width="600" height="400"></span>' if r["thumb"]
                else f'<span class="nthumb blank"><svg viewBox="0 0 32 32" aria-hidden="true">{r["p"]["mark"]}</svg></span>')
    items = "".join(f'''<li class="p-{r["p"]["slug"]}"><a href="{e(r["url"])}">{pic(r)}<span class="nmeta"><span class="ntag">{e(r["p"]["name"])}</span><time datetime="{e(r["date"])}">{human_date(r["date"])}</time></span>
<span>{body(r)}</span></a></li>''' for r in latest_news()[:6])
    links = " · ".join(f'<a href="{e((p["url"].rsplit("/", 1)[0] if not p["external"] else p["url"]) + "/news.html")}">{e(p["name"])}</a>' for p in PROJECTS)
    return f'''<section class="wrap news" id="news"><div class="news-head"><h2>Latest from the projects</h2><p>All news: {links}</p></div><ul class="nlist">{items}</ul>{SIGNUP}</section>'''


def meter(p):
    segs = "".join(f'<li class="seg s{int(v * 2)}"><span class="vh">{e(n)}: {"done" if v == 1 else "partly" if v else "open"}</span></li>'
                   for v, n in zip(p["ladder"], p["ladder_names"]))
    names, lv = p["ladder_names"], p["ladder"]
    done = [n for n, v in zip(names, lv) if v == 1]
    part = [n for n, v in zip(names, lv) if 0 < v < 1]
    said = []
    if done: said.append("Done: " + ", ".join(done).lower().capitalize())
    if part: said.append("under way: " + ", ".join(part).lower())
    said.append("last step: " + names[-1].lower())
    line = "; ".join(said) + "."
    return (f'<div class="meter"><p class="mhead">Progress, five steps</p><ol class="segs" aria-label="Progress, five steps">{segs}</ol>'
            f'<p class="mline">{e(line[0].upper() + line[1:])}</p></div>')


def card(p):
    s = board_stats(p["repo"])
    if s and s[1]:
        stat = f"{s[1]} tests finished · {s[2]} predictions written down before testing"
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
  <div class="proj-foot"><p class="odds"><span>Our estimate of success by 2027</span>{e(p['odds'])}</p>
  <a class="go" href="{e(p['url'])}"{target}>Open {e(p['name'].split()[1])}<span aria-hidden="true"> →</span></a></div>
</article>"""


RESOURCES = [
    ("agents.html", "Working with agents", "Our skill file, prompts and how to start"),
    ("https://usecaddie.app/blog/agents", "Building with agents", "Practical principles, from the Caddie blog"),
    ("https://usecaddie.app/blog/agents-handbook", "Agents handbook", "A short handbook, from the Caddie blog"),
    ("https://usecaddie.app/growth/course#part-discovery", "Scientific discovery", "Three books on how discovery groups work"),
]


def nav(home=""):
    """Header nav. home='' on the home page, 'index.html' on other pages."""
    dd = "".join(f'<a href="{e(u)}"><b>{e(t)}</b><small>{e(d)}</small></a>' for u, t, d in RESOURCES)
    return (f'<button class="menu" type="button" aria-expanded="false" aria-controls="mainnav">Menu</button><nav aria-label="Main" id="mainnav">'
            f'<a href="{home}#about">About</a><a href="{home}#why">Why agents</a><a href="{home}#news">News</a><a href="{home}#method">Method</a>'
            f'<div class="dd"><button type="button" class="dd-b" aria-expanded="false" aria-controls="dd-res">Resources<svg viewBox="0 0 12 12" width="10" height="10" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div class="dd-m" id="dd-res">{dd}</div></div>'
            f'<span class="ctas"><a class="btn btn-2" href="{home}#help">Contribute</a><a class="btn btn-1" href="{home}#projects">View projects</a></span></nav>')


NAV_JS = r"""(function(){var b=document.querySelector(".menu"),n=document.getElementById("mainnav");b.addEventListener("click",function(){var o=n.classList.toggle("open");b.setAttribute("aria-expanded",o)});n.addEventListener("click",function(e){if(e.target.closest("a")){n.classList.remove("open");b.setAttribute("aria-expanded","false")}});
var d=document.querySelector(".dd"),db=d&&d.querySelector(".dd-b");if(!d)return;function set(o){d.classList.toggle("on",o);db.setAttribute("aria-expanded",o)}
db.addEventListener("click",function(ev){ev.stopPropagation();set(!d.classList.contains("on"))});document.addEventListener("click",function(ev){if(!d.contains(ev.target))set(false)});
document.addEventListener("keydown",function(ev){if(ev.key==="Escape"&&d.classList.contains("on")){set(false);db.focus()}})})();"""


def head_html(title, desc):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='12' fill='none' stroke='%231B1A17' stroke-width='3'/%3E%3Ccircle cx='16' cy='16' r='3.5' fill='%231B1A17'/%3E%3C/svg%3E">
<link rel="preload" href="fonts/OpenIndusText-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="home.css">"""


LOGO = '<a class="logo" href="index.html"><svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="12"/><circle cx="16" cy="16" r="3.5" class="dot"/></svg>Open Citizen Science</a>'

SKILL_RAW = "https://raw.githubusercontent.com/HarshInvader/open-citizen-science/main/skills/open-science-contributor/SKILL.md"


def agents_page():
    steps = [
        ("Pick an open task", 'Each project keeps a public list, with a ready-made prompt for every task: <a href="mind/contribute.html">Open Mind</a>, <a href="origins/contribute.html">Open Origins</a>, <a href="https://openindus.pages.dev/contribute">Open Indus</a>.'),
        ("Give your agent our rules", 'Load the skill below into Claude Code, Codex or any agent that reads instruction files. It makes the agent seal its plan, find a planted answer first, and report failures as plainly as successes.'),
        ("Send the result back", "Whichever way it goes. A careful &#8220;it did not hold up&#8221; is as useful to us as a hit."),
    ]
    steps_html = "".join(f"<li><div><strong>{t}</strong> {b}</div></li>" for t, b in steps)
    reading = [
        ("https://usecaddie.app/blog/agents", "Practical principles for building with agents", "Caddie blog", "Agents now do most of the work, so the slow part is your attention. The principles we use to build with them: plan in writing, check by evidence, keep many tasks running."),
        ("https://usecaddie.app/blog/agents-handbook", "Building with agents: a short handbook", "Caddie blog", "The same ideas as a checklist you can keep open while you work."),
        ("https://usecaddie.app/growth/course#part-discovery", "Scientific discovery", "Caddie growth library", "Kuhn, The Idea Factory and The Lunar Men, read as a short course on running a discovery group."),
    ]
    borrow = [
        ("https://github.com/anthropics/skills", "Anthropic&#8217;s skills library", "Example skills for Claude, from document tools to testing. Good models for writing your own."),
        ("https://docs.claude.com/en/docs/claude-code/skills", "How skills work in Claude Code", "Where skill files go and how an agent decides to use one."),
        ("https://agents.md", "AGENTS.md", "A plain file of instructions for coding agents, read by Codex and many others."),
        ("https://github.com/HarshInvader/open-mind/blob/main/docs/AGENT_BRIEF.md", "Open Mind agent brief", "The rules every agent on the consciousness project follows."),
        ("https://github.com/HarshInvader/open-origins/blob/main/docs/AGENT_BRIEF.md", "Open Origins agent brief", "The same for the origin-of-life project, with its own nulls and data."),
    ]
    def cards(rows, src=True):
        out = ""
        for r in rows:
            u, t = r[0], r[1]
            meta = f'<span class="rsrc">{r[2]}</span>' if src and len(r) == 4 else ""
            out += f'<li><a href="{e(u)}">{meta}<span class="rt">{t}</span><span class="rd">{r[-1]}</span></a></li>'
        return out
    body = f"""<main id="main">
<section class="wrap rhero"><p class="eyebrow">Resources</p><h1>Working with agents</h1>
<p class="lede">Every project here is run by one person and a team of AI agents. You can bring your own. This page has the rules we give ours, as a file you can load, and the writing we learned them from.</p></section>
<section class="wrap split"><div><h2>Start in three steps</h2></div><ol class="rules">{steps_html}</ol></section>
<section class="wrap split" id="skill"><div><h2>Our skill file</h2><p class="side">A skill is a short instruction file an agent loads when a task matches it. This one carries our method.</p></div>
<div class="skillbox"><p class="sk-h">open-science-contributor</p><p class="sk-d">Seal the plan, find a planted answer first, compare against a fair null, count every test, verify every citation, report failures plainly, hand the work back.</p>
<div class="sk-act"><a class="btn btn-1" href="skills/open-science-contributor/SKILL.md" download>Download SKILL.md</a><a class="btn btn-2" href="https://github.com/HarshInvader/open-citizen-science/tree/main/skills/open-science-contributor">View on GitHub</a></div>
<p class="sk-how"><strong>Claude Code:</strong> save it as <code>~/.claude/skills/open-science-contributor/SKILL.md</code>.<br><strong>Codex and other agents:</strong> paste it into the repo&#8217;s <code>AGENTS.md</code>, or give it as the first message.<br><strong>Chat assistants:</strong> paste it in before the task.</p></div></section>
<section class="wrap rsec"><h2>What we learned building with agents</h2><ul class="rgrid">{cards(reading)}</ul></section>
<section class="wrap rsec"><h2>Skills and briefs to borrow from</h2><ul class="rgrid">{cards(borrow, False)}</ul></section>
</main>"""
    return (head_html("Working with agents · Open Citizen Science", "The rules we give our AI agents, as a skill file you can load, and the writing we learned them from.")
            + f'</head>\n<body>\n<header class="wrap top">{LOGO}\n{nav("index.html")}</header>\n{body}\n<script>{NAV_JS}</script>\n'
            + f'<footer class="wrap foot"><span>Open Citizen Science</span><span>Open code, open data, open results: <a href="https://github.com/HarshInvader/open-citizen-science">GitHub</a>.</span></footer>\n</body></html>')


def page(hero="a"):
    hero_html, hero_js = HEROES[hero]
    cards = "\n".join(card(p) for p in PROJECTS)
    rules = "".join(f"<li><div><strong>{e(a)}</strong> {e(b)}</div></li>" for a, b in RULES)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Open Citizen Science</title>
<meta name="description" content="Big open questions in science, tested in the open by a human lead, a team of AI agents and anyone who wants to help.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='12' fill='none' stroke='%231B1A17' stroke-width='3'/%3E%3Ccircle cx='16' cy='16' r='3.5' fill='%231B1A17'/%3E%3C/svg%3E">
<link rel="preload" href="fonts/OpenIndusText-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="hero.css"></head>
<body>
<header class="wrap top"><a class="logo" href="index.html"><svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="12"/><circle cx="16" cy="16" r="3.5" class="dot"/></svg>Open Citizen Science</a>
{nav()}</header>
<main id="main">
{hero_html(PROJECTS)}
{about_section()}
<section class="wrap" id="projects" aria-label="Projects"><div class="projs">
{cards}
</div></section>
<section class="wrap why" id="why">
  <h2>Agents make the slow part of science cheap</h2>
  <p class="side">An AI agent is a program, like ChatGPT, that carries out a whole task on its own: it finds the data, writes the code, runs the test and reports back. Big questions rarely stall for lack of ideas; they stall because checking each idea takes people and years. Agents can rerun a test on published data overnight. They can&#8217;t run new experiments, so we work with data that already exists.</p>
  <ol class="why-grid"><li class="why-card"><figure><svg viewBox="0 0 240 150" role="img" aria-label="An accepted framework tipping over as unexplained results pile up beside it">
<line x1="10" y1="131" x2="230" y2="131" class="f-ground"/>
<g transform="rotate(-7 20 131)"><rect x="20" y="36" width="112" height="95" rx="8" class="f-line"/><circle cx="38" cy="58" r="3.2" class="f-solid"/><circle cx="58" cy="58" r="3.2" class="f-solid"/><circle cx="78" cy="58" r="3.2" class="f-solid"/><circle cx="98" cy="58" r="3.2" class="f-solid"/><circle cx="118" cy="58" r="3.2" class="f-solid"/><circle cx="38" cy="78" r="3.2" class="f-solid"/><circle cx="58" cy="78" r="3.2" class="f-solid"/><circle cx="78" cy="78" r="3.2" class="f-solid"/><circle cx="98" cy="78" r="3.2" class="f-solid"/><circle cx="118" cy="78" r="3.2" class="f-solid"/><circle cx="38" cy="98" r="3.2" class="f-solid"/><circle cx="58" cy="98" r="3.2" class="f-solid"/><circle cx="78" cy="98" r="3.2" class="f-solid"/><circle cx="98" cy="98" r="3.2" class="f-solid"/><circle cx="118" cy="98" r="3.2" class="f-solid"/></g>
<circle cx="146.0" cy="124" r="6" class="f-acc"/><circle cx="161.0" cy="124" r="6" class="f-acc"/><circle cx="176.0" cy="124" r="6" class="f-acc"/><circle cx="191.0" cy="124" r="6" class="f-acc"/><circle cx="206.0" cy="124" r="6" class="f-acc"/><circle cx="153.5" cy="111" r="6" class="f-acc"/><circle cx="168.5" cy="111" r="6" class="f-acc"/><circle cx="183.5" cy="111" r="6" class="f-acc"/><circle cx="198.5" cy="111" r="6" class="f-acc"/><circle cx="161.0" cy="98" r="6" class="f-acc"/><circle cx="176.0" cy="98" r="6" class="f-acc"/><circle cx="191.0" cy="98" r="6" class="f-acc"/><circle cx="168.5" cy="85" r="6" class="f-acc"/><circle cx="183.5" cy="85" r="6" class="f-acc"/><circle cx="176.0" cy="72" r="6" class="f-acc"/>
<text x="22" y="22" class="f-lab">Framework</text><text x="226" y="58" class="f-lab acc" text-anchor="end">Unexplained</text>
</svg></figure><h3>Fields change when failures pile up</h3><p><a class="book" href="https://usecaddie.app/s/the-structure-of-scientific-revolutions-50th">Kuhn&#8217;s <i>The Structure of Scientific Revolutions</i></a> shows a field shifts only when results it cannot explain become too many to ignore. Agents can test many ideas quickly, and we count every test we run, so a lucky hit can&#8217;t pass as a finding and every failure stays on the record.</p></li><li class="why-card"><figure><svg viewBox="0 0 240 150" role="img" aria-label="A chemist, a statistician and a sceptic all feeding into one task">
<path d="M104 34 C140 34 140 75 172 75" class="f-line"/><path d="M104 75 C140 75 140 75 172 75" class="f-line"/><path d="M104 116 C140 116 140 75 172 75" class="f-line"/><circle cx="98" cy="34" r="6" class="f-solid"/><text x="86" y="38" class="f-lab" text-anchor="end">Chemist</text><circle cx="98" cy="75" r="6" class="f-solid"/><text x="86" y="79" class="f-lab" text-anchor="end">Statistician</text><circle cx="98" cy="116" r="6" class="f-solid"/><text x="86" y="120" class="f-lab" text-anchor="end">Sceptic</text><rect x="172" y="57" width="36" height="36" rx="6" class="f-acc"/>
<text x="190" y="114" class="f-lab acc" text-anchor="middle">One task</text>
</svg></figure><h3>Discoveries come from mixing experts</h3><p>In <a class="book" href="https://usecaddie.app/s/the-idea-factory-bell-labs-and-the-great-age"><i>The Idea Factory</i></a>, Bell Labs puts physicists, chemists and engineers in the same corridors, and the transistor comes out of it. Agents can draft a chemist&#8217;s or a statistician&#8217;s checks in minutes; then real experts review them.</p></li><li class="why-card"><figure><svg viewBox="0 0 240 150" role="img" aria-label="A ring of people and agents meeting round a full moon, with one empty seat marked You"><circle cx="120" cy="70" r="26" class="f-moon"/><text x="120" y="67" class="f-lab acc" text-anchor="middle">Full</text><text x="120" y="80" class="f-lab acc" text-anchor="middle">moon</text><circle cx="120.0" cy="22.0" r="6" class="f-line"/><rect x="141.0" y="23.4" width="10" height="10" rx="2" class="f-solid"/><circle cx="165.0" cy="46.0" r="6" class="f-line"/><rect x="167.0" y="65.0" width="10" height="10" rx="2" class="f-solid"/><circle cx="165.0" cy="94.0" r="6" class="f-line"/><rect x="141.0" y="106.6" width="10" height="10" rx="2" class="f-solid"/><circle cx="120.0" cy="118.0" r="6.5" class="f-you"/><rect x="89.0" y="106.6" width="10" height="10" rx="2" class="f-solid"/><circle cx="75.0" cy="94.0" r="6" class="f-line"/><rect x="63.0" y="65.0" width="10" height="10" rx="2" class="f-solid"/><circle cx="75.0" cy="46.0" r="6" class="f-line"/><rect x="89.0" y="23.4" width="10" height="10" rx="2" class="f-solid"/><text x="120" y="141" class="f-lab acc" text-anchor="middle">You</text><circle cx="18" cy="137" r="5" class="f-line"/><text x="28" y="141.5" class="f-lab">People</text><rect x="182" y="132" width="10" height="10" rx="2" class="f-solid"/><text x="197" y="141.5" class="f-lab">Agents</text></svg></figure><h3>Big change can start in a small circle</h3><p>In 1760s Birmingham about a dozen friends, among them Watt, Wedgwood and Erasmus Darwin, met each full moon to share experiments; the moon lit their ride home. Their circle, told in <a class="book" href="https://usecaddie.app/s/the-lunar-men-the-inventors-of-the-modern"><i>The Lunar Men</i></a>, helped start the Industrial Revolution. Ours is people and agents, and the seats are open.</p></li></ol>
  <p class="why-note">Agents can also fool themselves faster than people can, so every project follows <a href="#method">the same rules</a>. The three books are also a short course on running a discovery group: <a class="book" href="https://usecaddie.app/growth/course#part-discovery">Scientific discovery</a>.</p>
</section>
{news_section()}
<section class="wrap split" id="method">
  <div><h2>One method for every project</h2>
  <p class="side">A result that looks good must not be something you could get by trying until something works. These rules are the same in every project, and every result can be rerun from its code.</p></div>
  <ol class="rules">{rules}</ol>
</section>
<section class="wrap split" id="help">
  <div><h2>Contribute</h2>
  <p class="side">Each project is run by one person and a team of AI agents, with a public list of open tasks. Anyone can pick one up.</p></div>
  <div class="help">
    <p><strong>No coding needed:</strong></p>
    <ul>
      <li><strong>Tell us where we are wrong</strong> about your field. Historians, linguists, clinicians and chemists catch what agents miss.</li>
      <li><strong>Point us to data</strong> we are missing. Each project lists what would change its odds most.</li>
      <li><strong>Check a result.</strong> Each finding says what was tested; tell us if it does not hold up.</li>
    </ul>
    <p><strong>If you use an AI assistant</strong> (Claude, ChatGPT or similar), give it an open task. Each project has a ready-made prompt per task: <a href="mind/contribute.html">Open Mind</a>, <a href="origins/contribute.html">Open Origins</a>, <a href="https://openindus.pages.dev/contribute">Open Indus</a>. It writes down its plan, checks it can find a planted answer, runs the test and sends the result back to us, whichever way it goes.</p>
  </div>
</section>
</main>
<script>{hero_js}{SIGNUP_JS}</script>
<script>{NAV_JS}</script>
<footer class="wrap foot"><span>Open Citizen Science</span><span>Open code, open data, open results: <a href="https://github.com/HarshInvader/open-citizen-science">GitHub</a>. Updated {time.strftime('%d %b %Y').lstrip('0')}.</span><span class="fcredit">Star drawing: al-Sufi, <i>Book of the Fixed Stars</i>, Bodleian Library MS Marsh 144, public domain, via <a href="https://commons.wikimedia.org/wiki/File:Al_Sufi_-_Book_of_Fixed_Stars_-_Ursa_Major_(The_Great_Bear)_-_Bodleian_Library_-_Marsh_144(illustrationonly).jpg">Wikimedia Commons</a>.</span></footer>
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
    shutil.copy(HERE / "hero.css", DIST / "hero.css")
    shutil.copytree(HERE / "fonts", DIST / "fonts")
    shutil.copytree(HERE / "art", DIST / "art", ignore=shutil.ignore_patterns("*.json"))
    (DIST / "index.html").write_text(page("c"))  # al-Sufi's stars, until a better one
    (DIST / "agents.html").write_text(agents_page())
    shutil.copytree(HERE / "skills", DIST / "skills")
    for k in ("a", "b", "d", "e", "f"):  # the other hero options, as preview pages
        (DIST / f"hero-{k}.html").write_text(page(k))
    print("wrote", DIST)


if __name__ == "__main__":
    main()
