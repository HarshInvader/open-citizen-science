#!/usr/bin/env python3
"""Landscape snapshot: who works on what, and roughly how many, for each project's news page.

Reads tools/paperwatch/landscape_queries.json (one entry per project: a base filter and a list of research
directions, each with an OpenAlex title-and-abstract search plus the hand-written text: bet, leading groups, now, us).
For each direction it asks OpenAlex for the past 12 months and writes the numbers, with the text, into
<repo>/site/news.json under "landscape". The site builds only render that block.

Usage (run with python3 -I from anywhere):
  landscape.py calibrate <project> <direction_id>   print the newest matching titles and top authors (1 request)
  landscape.py run <project> [--only id,id]          fetch everything and write news.json
  landscape.py write <project>                       rewrite news.json from cache only (no network; after editing text)

Numbers per direction (past 12 months, journal articles and reviews by default):
  works         meta.count of the filter
  authors       distinct author ids; exact when all matching works were fetched (up to MAX_PAGES x 200),
                otherwise extrapolated from the newest works with a Heaps-law fit (marked "est" in the data)
  institutions  distinct institution ids, same way
  trend         works per publication year, five full years plus the current partial year (one group_by request)

With a key (OPENALEX_API_KEY or ~/.config/openalex/api_key; never stored anywhere else) the budget is USD 1 a day.
OpenAlex without a key has a small shared daily budget (about USD 0.10, roughly 1 cent per 10 searches) and a
search rate limit, so every response is cached under .local/paperwatch/landscape_cache/ for CACHE_DAYS days: a rerun
within that window costs nothing, and a monthly rerun fetches fresh numbers (--fresh forces it). The run stops cleanly
when the budget is low; rerun it the next day and it continues from the cache. No key, no email: User-Agent "open-research-site/1.0" only.
"""
import datetime as dt
import hashlib
import json
import math
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

HUB = Path(__file__).resolve().parents[2]
PERSONAL = HUB.parent
CONF = Path(__file__).resolve().parent / "landscape_queries.json"
CACHE = HUB / ".local" / "paperwatch" / "landscape_cache"
RAW = HUB / ".local" / "paperwatch"
API = "https://api.openalex.org/works"
UA = {"User-Agent": "open-research-site/1.0"}
MAX_PAGES = 2          # 400 newest works per direction; beyond that, distinct counts are extrapolated
RESERVE_USD = 0.006    # leave this much of the shared daily budget for other threads
SPACING = 4.0          # seconds between uncached requests
CACHE_DAYS = 20        # cached responses older than this are fetched again, so a monthly rerun refreshes everything


class BudgetOut(Exception):
    pass


SNAP = [None]  # the snapshot date; kept across a run that spans days so the cached requests still match


def today():
    return SNAP[0] or dt.date.today()


def window(d=None):
    d = d or today()
    start = d.replace(year=d.year - 1) + dt.timedelta(days=1)
    return start.isoformat(), d.isoformat()


_last = [0.0]
KEY_FILE = Path.home() / ".config" / "openalex" / "api_key"


def api_key():
    """Optional OpenAlex key, from OPENALEX_API_KEY or ~/.config/openalex/api_key. Never printed or stored:
    the cache, the raw files and news.json only ever hold the key-free URL."""
    import os
    k = os.environ.get("OPENALEX_API_KEY", "").strip()
    if not k and KEY_FILE.exists():
        k = KEY_FILE.read_text().strip()
    return k or None


def get(params, fresh=False):
    url = API + "?" + urllib.parse.urlencode(params, safe=":,|()\"*")
    key = hashlib.sha1(url.encode()).hexdigest()[:20]
    f = CACHE / f"{key}.json"
    if f.exists() and not fresh:
        c = json.loads(f.read_text())
        age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(c["fetched"])
        if age.days < CACHE_DAYS:
            return c["body"]
    for attempt in range(40):
        wait = (0.5 if api_key() else SPACING) - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        k = api_key()
        req_url = url + ("&" + urllib.parse.urlencode({"api_key": k}) if k else "")
        try:
            with urllib.request.urlopen(urllib.request.Request(req_url, headers=UA), timeout=60) as r:
                body = json.loads(r.read())
                left = r.headers.get("x-ratelimit-remaining-usd")
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", "replace")
            if k:
                txt = txt.replace(k, "<key>")
            if e.code == 429:
                try:
                    j = json.loads(txt)
                except ValueError:
                    j = {}
                if ("daily budget" in txt.lower() or "insufficient" in txt.lower()) and "boolean" not in txt.lower():
                    raise BudgetOut(txt[:200])
                time.sleep(min(60, float(j.get("retryAfter", 15)) + 2 + attempt))
                continue
            if e.code >= 500:
                print(f"   OpenAlex {e.code}, waiting", flush=True)
                time.sleep(min(60, 10 + attempt * 5))
                continue
            raise SystemExit(f"OpenAlex {e.code} for {url}\n{txt[:400]}")
        except (urllib.error.URLError, TimeoutError):
            time.sleep(min(60, 10 + attempt * 5))
            continue
        if "meta" not in body:
            time.sleep(min(60, 15 + attempt * 2))
            continue
        CACHE.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps({"url": url, "fetched": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "body": body}))
        if left is not None and float(left) < RESERVE_USD:
            raise BudgetOut(f"daily budget nearly used (USD {left} left); rerun later, the cache keeps what is done")
        return body
    raise SystemExit(f"gave up on {url}")


def filt(proj, d, start, end):
    base = d.get("filter", proj["base_filter"])
    return f'title_and_abstract.search:{d["search"]},{base},from_publication_date:{start},to_publication_date:{end}'


def check_url(proj, d, start, end):
    return API + "?" + urllib.parse.urlencode({"filter": filt(proj, d, start, end)}, safe=":,|()\"*")


def page(proj, d, start, end, n, fresh=False):
    return get({"filter": filt(proj, d, start, end), "per_page": 200, "page": n, "sort": "publication_date:desc",
                "select": "id,display_name,publication_date,authorships,primary_location"}, fresh)


def heaps(works, key):
    """Distinct items in the newest n works, and at n/2 (for the extrapolation exponent)."""
    seen, half = set(), None
    for i, w in enumerate(works):
        if i == len(works) // 2:
            half = len(seen)
        seen |= key(w)
    return len(seen), half or len(seen)


def a_ids(w):
    return {a["author"]["id"] for a in w["authorships"] if a.get("author", {}).get("id")}


def i_ids(w):
    return {i["id"] for a in w["authorships"] for i in a.get("institutions", []) if i.get("id")}


def estimate(total, fetched, works, key):
    d, dh = heaps(works, key)
    if fetched >= total or fetched < 40:
        return d, False
    beta = max(0.5, min(1.0, math.log(max(d, 1) / max(dh, 1)) / math.log(2)))
    return int(round(d * (total / fetched) ** beta)), True


def measure(proj, d, fresh=False):
    start, end = window()
    p1 = page(proj, d, start, end, 1, fresh)
    total = p1["meta"]["count"]
    works = list(p1["results"])
    for n in range(2, MAX_PAGES + 1):
        if len(works) >= total:
            break
        works += page(proj, d, start, end, n, fresh)["results"]
    y0 = today().year - 5
    yr = get({"filter": filt(proj, d, f"{y0}-01-01", end), "group_by": "publication_year"}, fresh)
    by = {int(g["key"]): g["count"] for g in yr["group_by"]}
    authors, a_est = estimate(total, len(works), works, a_ids)
    insts, i_est = estimate(total, len(works), works, i_ids)
    # candidate leading groups: most frequent authors in the fetched works, with their most common institution
    ac, aname, ainst = Counter(), {}, defaultdict(Counter)
    ic, iname = Counter(), {}
    for w in works:
        for a in w["authorships"]:
            au = a.get("author") or {}
            if au.get("id"):
                ac[au["id"]] += 1
                aname[au["id"]] = au.get("display_name")
                for i in a.get("institutions", []):
                    ainst[au["id"]][i.get("display_name")] += 1
        for i in {(i["id"], i.get("display_name")) for a in w["authorships"] for i in a.get("institutions", []) if i.get("id")}:
            ic[i[0]] += 1
            iname[i[0]] = i[1]
    top_a = [{"name": aname[k], "works": c, "inst": (ainst[k].most_common(1)[0][0] if ainst[k] else None), "id": k} for k, c in ac.most_common(25)]
    top_i = [{"name": iname[k], "works": c, "id": k} for k, c in ic.most_common(20)]
    # leading groups: authors of the 100 most-cited matching papers of the past three years (last author counts double)
    cited = get({"filter": filt(proj, d, f"{today().year - 3}-01-01", end), "per_page": 100, "sort": "cited_by_count:desc",
                 "select": "id,display_name,publication_year,cited_by_count,authorships"}, fresh)["results"]
    ls, lname, linst, lcit = Counter(), {}, defaultdict(Counter), Counter()
    for w in cited:
        for a in w["authorships"]:
            au = a.get("author") or {}
            if not au.get("id"):
                continue
            ls[au["id"]] += 2 if a.get("author_position") == "last" else 1
            lcit[au["id"]] += w.get("cited_by_count") or 0
            lname[au["id"]] = au.get("display_name")
            for i in a.get("institutions", []):
                linst[au["id"]][i.get("display_name")] += 1
    lead = [{"name": lname[k], "score": c, "cites": lcit[k], "inst": (linst[k].most_common(1)[0][0] if linst[k] else None), "id": k}
            for k, c in sorted(ls.items(), key=lambda kv: (-kv[1], -lcit[kv[0]]))[:30]]
    venues = Counter(((w.get("primary_location") or {}).get("source") or {}).get("display_name") for w in works)
    return {
        "works": total, "authors": authors, "institutions": insts, "estimated": a_est or i_est, "fetched": len(works),
        "author_ids": sorted({x for w in works for x in a_ids(w)}),
        "trend": {"years": list(range(y0, today().year + 1)), "counts": [by.get(y, 0) for y in range(y0, today().year + 1)]},
        "titles": [w["display_name"] for w in works[:60]], "top_authors": top_a, "lead_candidates": lead,
        "top_cited": [f'{w["publication_year"]} [{w.get("cited_by_count")}] {w["display_name"]}' for w in cited[:30]], "top_institutions": top_i,
        "top_venues": venues.most_common(12), "check_url": check_url(proj, d, start, end), "window": [start, end],
    }


def trend_word(counts):
    full = counts[:-1]  # last entry is the current, partial year
    xs = [i for i, c in enumerate(full) if c > 0]
    if len(xs) < 3:
        return "too few papers to call a trend", 0.0
    ys = [math.log(full[i]) for i in xs]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    g = math.exp(slope) - 1
    return ("rising" if g > 0.05 else "falling" if g < -0.05 else "steady"), round(g, 3)


def roughly(n):
    if n < 20:
        return str(n)
    if n < 100:
        return str(int(round(n, -1)))
    if n < 1000:
        return str(int(round(n, -1)))
    return f"{int(round(n, -2)):,}"


def write(pkey, proj, raw):
    dirs = []
    for d in proj["directions"]:
        m = raw.get(d["id"])
        if not m:
            continue
        word, g = trend_word(m["trend"]["counts"])
        dirs.append({
            "id": d["id"], "name": d["name"], "bet": d["bet"],
            "works": m["works"], "authors": m["authors"], "institutions": m["institutions"], "estimated": m["estimated"],
            "trend": {**m["trend"], "partial_last": True, "word": word, "growth": g},
            "query": {"search": d["search"], "filter": d.get("filter", proj["base_filter"]), "window": m["window"], "url": m["check_url"]},
            "groups": d.get("groups", []), "now": d.get("now", ""), "now_ids": d.get("now_ids", []), "us": d.get("us", ""),
        })
    dirs.sort(key=lambda x: -x["authors"])
    fetched_sum = sum(len(raw[d["id"]]["author_ids"]) for d in dirs)
    union = len(set().union(*[set(raw[d["id"]]["author_ids"]) for d in dirs])) if dirs else 0
    est_sum = sum(d["authors"] for d in dirs)
    people = int(round(est_sum * (union / fetched_sum if fetched_sum else 1)))
    works = sum(d["works"] for d in dirs)
    landscape = {
        "updated": today().isoformat(),
        "method": proj["method"],
        "headline": proj["headline"].format(people=roughly(people), n=len(dirs)),
        "totals": {"authors": people, "works_sum": works, "overlap_ratio": round(union / fetched_sum, 3) if fetched_sum else 1},
        "directions": dirs,
    }
    f = PERSONAL / proj["repo"] / "site" / "news.json"
    news = json.loads(f.read_text())
    news.pop("field_now", None)
    out = {}
    for k, v in news.items():  # keep key order, landscape where field_now was (after _about)
        out[k] = v
        if k == "_about":
            out["landscape"] = landscape
    out.setdefault("landscape", landscape)
    out["landscape"] = landscape
    f.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {f}: {len(dirs)} directions, ~{people} authors")


def main(argv):
    conf = json.loads(CONF.read_text())
    fresh = "--fresh" in argv
    argv = [a for a in argv if a != "--fresh"]
    if len(argv) < 2:
        raise SystemExit(__doc__)
    cmd, pkey = argv[0], argv[1]
    proj = conf[pkey]
    rawf = RAW / f"landscape_{pkey}.raw.json"
    raw = json.loads(rawf.read_text()) if rawf.exists() else {}
    snaps = sorted({m["window"][1] for m in raw.values()})
    if snaps and (dt.date.today() - dt.date.fromisoformat(snaps[-1])).days < CACHE_DAYS and not fresh:
        SNAP[0] = dt.date.fromisoformat(snaps[-1])  # continue the unfinished or recent snapshot
    else:
        raw = {}
    if cmd == "calibrate":
        d = next(x for x in proj["directions"] if x["id"] == argv[2])
        start, end = window()
        p = page(proj, d, start, end, 1, fresh)
        print(p["meta"]["count"], "works;", check_url(proj, d, start, end))
        for w in p["results"][:40]:
            print(" -", w["publication_date"], w["display_name"][:120])
        return
    if cmd == "run":
        only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
        try:
            for d in proj["directions"]:
                if only and d["id"] not in only:
                    continue
                print("..", d["id"], flush=True)
                raw[d["id"]] = measure(proj, d, fresh)
                RAW.mkdir(parents=True, exist_ok=True)
                rawf.write_text(json.dumps(raw, ensure_ascii=False, indent=1))
                m = raw[d["id"]]
                print(f'   {m["works"]} works, {m["authors"]} authors, {m["institutions"]} inst{" (est)" if m["estimated"] else ""}, trend {m["trend"]["counts"]}', flush=True)
        except BudgetOut as e:
            print("STOPPED:", e)
        finally:
            RAW.mkdir(parents=True, exist_ok=True)
            rawf.write_text(json.dumps(raw, ensure_ascii=False, indent=1))
        if all(d["id"] in raw for d in proj["directions"]):
            write(pkey, proj, raw)
        else:
            print("not all directions fetched yet; news.json left unchanged")
        return
    if cmd == "write":
        write(pkey, proj, raw)
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
