"""Paper watch: find new papers for each project since the last sweep.

Usage: python3 -I tools/paperwatch/sweep.py [--since YYYY-MM-DD] [--project origins|mind|indus] [--dry]
Writes .local/paperwatch/<today>/<project>.json and .md (candidates, ranked), and updates
.local/paperwatch/state.json (last sweep date and every candidate id seen, so nothing is shown twice).
Nothing here is added to any site: triage and analysis are done by a person or agent who opens each paper.
"""
import json, os, re, sys, time, html, urllib.request, urllib.parse, datetime as dt
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
HUB = os.path.dirname(os.path.dirname(HERE))
PERSONAL = os.path.dirname(HUB)
OUT = os.path.join(HUB, ".local", "paperwatch")
UA = {"User-Agent": "open-research-site/1.0"}
SRC = json.load(open(os.path.join(HERE, "sources.json")))["projects"]


def get(url, tries=3):
    for k in range(tries):
        try:
            time.sleep(0.4)
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return r.read()
        except Exception as e:  # network hiccup or 5xx: back off, then give up on this query
            err = e
            time.sleep(2 * (k + 1))
    print("  ! failed:", url[:120], err, file=sys.stderr)
    return None


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()[:120]


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def epmc(query, since, today, tag):
    q = f"({query}) AND FIRST_PDATE:[{since} TO {today}]"
    out, cursor = [], "*"
    for _ in range(3):  # at most 300 hits per query
        u = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&pageSize=100&cursorMark="
             + urllib.parse.quote(cursor) + "&query=" + urllib.parse.quote(q))
        b = get(u)
        if not b:
            break
        r = json.loads(b)
        for m in r.get("resultList", {}).get("result", []):
            venue = m.get("journalInfo", {}).get("journal", {}).get("title") or m.get("bookOrReportDetails", {}).get("publisher") or m.get("source")
            if m.get("source") == "PPR":
                venue = (m.get("bookOrReportDetails") or {}).get("publisher") or "preprint"
            out.append(dict(title=clean(m.get("title")), authors=m.get("authorString", "")[:300], venue=venue,
                            date=m.get("firstPublicationDate"), doi=m.get("doi"), abstract=clean(m.get("abstractText"))[:1500],
                            url=("https://doi.org/" + m["doi"]) if m.get("doi") else f"https://europepmc.org/article/{m.get('source')}/{m.get('id')}",
                            oa=m.get("isOpenAccess") == "Y", via="europepmc", hit=tag))
        nxt = r.get("nextCursorMark")
        if not nxt or nxt == cursor or len(r.get("resultList", {}).get("result", [])) < 100:
            break
        cursor = nxt
    return out


def crossref(term, since, today):
    u = ("https://api.crossref.org/works?rows=60&select=DOI,title,author,container-title,issued,created,abstract,type"
         f"&filter=from-created-date:{since},until-created-date:{today}&query.bibliographic=" + urllib.parse.quote(term))
    b = get(u)
    out = []
    if not b:
        return out
    for m in json.loads(b)["message"]["items"]:
        if m.get("type") not in ("journal-article", "posted-content", "proceedings-article", "book-chapter", "monograph", "book"):
            continue
        t = clean((m.get("title") or [""])[0]); ab = clean(m.get("abstract"))
        if term.lower() not in (t + " " + ab).lower():  # Crossref matching is fuzzy: keep only exact phrase hits
            continue
        au = ", ".join(f"{a.get('family','')} {a.get('given','')[:1]}".strip() for a in (m.get("author") or [])[:8])
        d = (m.get("issued") or m.get("created") or {}).get("date-parts", [[None]])[0]
        out.append(dict(title=t, authors=au, venue=(m.get("container-title") or [m.get("type")])[0],
                        date="-".join(str(x).zfill(2) for x in d if x), doi=m["DOI"], abstract=ab[:1500],
                        url="https://doi.org/" + m["DOI"], oa=None, via="crossref", hit=term))
    return out


def arxiv(cats, terms, since):
    q = "(" + " OR ".join(f"cat:{c}" for c in cats) + ") AND (" + " OR ".join(f'abs:"{t}"' for t in terms) + ")"
    u = ("http://export.arxiv.org/api/query?sortBy=submittedDate&sortOrder=descending&max_results=150&search_query="
         + urllib.parse.quote(q))
    b = get(u)
    out = []
    if not b:
        return out
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for e in ET.fromstring(b).findall("a:entry", ns):
        pub = e.findtext("a:published", "", ns)[:10]
        if pub < since:
            continue
        aid = e.findtext("a:id", "", ns).rsplit("/abs/", 1)[-1]
        out.append(dict(title=clean(e.findtext("a:title", "", ns)), authors=", ".join(a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)[:8]),
                        venue="arXiv " + aid, date=pub, doi=f"10.48550/arXiv.{re.sub(r'v[0-9]+$', '', aid)}",
                        abstract=clean(e.findtext("a:summary", "", ns))[:1500], url="https://arxiv.org/abs/" + aid,
                        oa=True, via="arxiv", hit="arxiv"))
    return out


def zenodo(term, since):
    u = "https://zenodo.org/api/records?sort=mostrecent&size=50&q=" + urllib.parse.quote(f'"{term}"')
    b = get(u)
    out = []
    if not b:
        return out
    for h in json.loads(b).get("hits", {}).get("hits", []):
        md = h.get("metadata", {})
        if (md.get("publication_date") or "") < since:
            continue
        out.append(dict(title=clean(md.get("title")), authors=", ".join(c.get("name", "") for c in md.get("creators", [])[:8]),
                        venue="Zenodo " + str(h.get("id")), date=md.get("publication_date"), doi=h.get("doi"),
                        abstract=clean(md.get("description"))[:1500], url=h.get("links", {}).get("self_html") or f"https://zenodo.org/records/{h.get('id')}",
                        oa=True, via="zenodo", hit=term))
    return out


def known_urls(p):
    try:
        d = json.load(open(os.path.join(PERSONAL, p["repo"], p["news"])))
    except Exception:
        return set()
    items = d["items"] if isinstance(d, dict) else d
    return {norm_title(x.get("url", "")) for x in items} | {norm_title(x.get("head", "")) for x in items}


def score(c, p):
    s = 0
    v = (c.get("venue") or "").lower()
    if any(x.lower() == v or (len(x) > 5 and x.lower() in v) for x in p["venues"]):
        s += 2
    text = (c["title"] + " " + c.get("abstract", "")).lower()
    s += min(3, sum(k.lower() in text for k in p["keywords"]))
    if c["hit"].startswith("author:"):
        s += 2
    if not c.get("abstract"):
        s -= 1
    return s


def main():
    a = sys.argv[1:]
    today = dt.date.today().isoformat()
    os.makedirs(OUT, exist_ok=True)
    sp = os.path.join(OUT, "state.json")
    state = json.load(open(sp)) if os.path.exists(sp) else {}
    projects = [a[a.index("--project") + 1]] if "--project" in a else list(SRC)
    for name in projects:
        p = SRC[name]
        st = state.setdefault(name, {"last": None, "seen": []})
        if "--since" in a:
            since = a[a.index("--since") + 1]
        elif st["last"]:  # overlap 3 days so late-indexed papers are not missed; 'seen' removes repeats
            since = (dt.date.fromisoformat(st["last"]) - dt.timedelta(days=3)).isoformat()
        else:
            since = (dt.date.today() - dt.timedelta(days=30)).isoformat()
        print(f"[{name}] since {since}", flush=True)
        cands = []
        kw = p["keywords"]
        for i in range(0, len(kw), 6):  # OR keywords in small groups to keep queries short
            grp = " OR ".join(f'"{k}"' for k in kw[i:i + 6])
            cands += epmc(f"TITLE_ABS:({grp})", since, today, "kw:" + ", ".join(kw[i:i + 6]))
        for person in p["people"]:
            cands += epmc(f'AUTH:"{person}"', since, today, "author:" + person)
        for k in kw:
            cands += crossref(k, since, today)
        if p.get("arxiv"):
            cands += arxiv(p["arxiv"]["cats"], p["arxiv"]["terms"], since)
        for z in p.get("zenodo", []):
            cands += zenodo(z, since)
        known = known_urls(p) | set(st["seen"])
        uniq = {}
        for c in cands:
            key = (c.get("doi") or "").lower() or norm_title(c["title"])
            if not c["title"] or key in known or norm_title(c["title"]) in known or norm_title(c["url"]) in known:
                continue
            if key in uniq:
                if c["hit"] not in uniq[key]["hit"]:
                    uniq[key]["hit"] += "; " + c["hit"]
                if not uniq[key].get("abstract") and c.get("abstract"):
                    uniq[key]["abstract"] = c["abstract"]
                continue
            uniq[key] = c
        rows = sorted(uniq.values(), key=lambda c: (-score(c, p), c.get("date") or ""), reverse=False)
        for c in rows:
            c["score"] = score(c, p)
        d = os.path.join(OUT, today)
        os.makedirs(d, exist_ok=True)
        json.dump(dict(project=name, since=since, until=today, n=len(rows), candidates=rows), open(os.path.join(d, f"{name}.json"), "w"), indent=1)
        with open(os.path.join(d, f"{name}.md"), "w") as f:
            f.write(f"# {name}: {len(rows)} new candidates, {since} to {today}\n\n")
            for i, c in enumerate(rows, 1):
                f.write(f"{i}. [{c['score']}] {c['title']} | {c['authors'][:90]} | {c['venue']} | {c['date']} | {c['url']} | via {c['via']} ({c['hit'][:80]})\n")
        print(f"[{name}] {len(cands)} hits, {len(rows)} new candidates -> {d}/{name}.md", flush=True)
        if "--dry" not in a:
            st["last"] = today
            st["seen"] = sorted(set(st["seen"]) | set(uniq))
    if "--dry" not in a:
        json.dump(state, open(sp, "w"), indent=1)


if __name__ == "__main__":
    main()
