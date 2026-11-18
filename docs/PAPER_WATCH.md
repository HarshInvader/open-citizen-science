# Paper watch (every other day)

Find the few new papers that matter for Open Mind (consciousness) and Open Origins (origin of life), add them to each project's News page, and queue them for the newsletter. Most runs should add nothing or one item. We do not add every paper.

State lives in `docs/paper_watch_state.json` (last run date, DOIs already looked at and why they were kept or dropped). Read it first; write it last.

## 1. Search (since the last run, minus 3 days of overlap)

Use the open APIs only, one request at a time, a generic User-Agent (`open-research-site/1.0`), honour Retry-After. Never send personal details.

- Europe PMC REST (`https://www.ebi.ac.uk/europepmc/webservices/rest/search`), which covers PubMed and bioRxiv/medRxiv preprints
- arXiv API (q-bio.NC, q-bio.PE, astro-ph.EP, cs.AI for machine consciousness)
- Crossref (`/works?filter=from-pub-date:...`) to confirm venue, date and authors

Queries, per project:

- Mind: consciousness AND (theory OR "integrated information" OR "global workspace" OR "neural correlates" OR anaesthesia OR propofol OR "disorders of consciousness" OR dreaming OR "serial awakening" OR psychedelic OR "perturbational complexity" OR "AI consciousness")
- Origins: "origin of life" OR abiogenesis OR prebiotic OR "RNA world" OR ribozyme OR protocell OR "hydrothermal vent" AND origin OR "assembly theory" OR biosignature OR "sample return" (Bennu, Ryugu) OR "LUCA"

## 2. Keep only what passes the bar

Keep a paper only if all are true:

1. **Relevant**: it bears on a question the project works on: a fact in the Mind constraint ledger, a theory we score, a dataset we use or could use; for Origins, one of the five topics or a claim we test.
2. **Strong**: peer-reviewed in a serious venue, or a preprint from a large consortium, a registered report, or one that is already being discussed by the field. New data or a real test beats a review or opinion. No press-release-only items.
3. **New to us**: not already in `news.json` or the state file.

At most 3 items per project per run. If in doubt, leave it out and note it in the state file as "watch" so the next run can look again once it is cited or published.

## 3. Verify before writing

Read the full text whenever it is free (find it with OpenAlex `best_oa_location`, Europe PMC full text, arXiv/bioRxiv); the abstract alone is a last resort for closed papers. Open the DOI landing page and check authors, venue, date, and every number you will quote. Set `verified: true` only after that. If the full text is closed, write only what the abstract says and say so in `tech`.

## 4. Write the item

Add to the top of `items` in `open-mind/site/news.json` or `open-origins/site/news.json`, following the file's `_about`:

- `id` (slug), `section: "latest"`, `date` (publication date), `kind` (Paper, Preprint, Dataset), `head`, `who`, `venue`, `url` (https DOI), `verified`
- `gist`: one line, the conclusion
- `plain`: a short story for anyone, no jargon, sentence case
- `tech`: for specialists: n, methods, effect sizes, caveats
- `borrow`: what this project takes from it or would test
- `status`: planned, running, done, or context
- `topic`: one of the file's `topics`

Then add a drawing for the new id in that project's `site/illustrate_news.py` in the same style as the others (one bespoke drawing per item, plus its ALT text), and run it.

## 5. Build, check, ship

1. `cd open-citizen-science && nice python3 -I build.py` (runs both projects, link check, image budget)
2. Screenshot the project's News page (headless Chrome, `python3 -m http.server 8765 --bind 127.0.0.1` from `dist`, then `pkill -f "http.server 8765"`) and look at the new card in light and dark
3. Deploy: `npx wrangler pages deploy dist --project-name opencitizenscience --branch main --commit-dirty=true`
4. Commit each changed repo: `gh auth switch -h github.com -u HarshInvader`, add paths one by one, run the leak scan `../open-citizen-science/.local/leak_scan.sh` from the repo (must print nothing; it is local only), commit, push, `gh auth switch -h github.com -u harsha-oncourse`

## 6. Newsletter draft (never send)

Append each new item to `docs/newsletter/next-<project>.md` as a heading (the gist), two sentences from `plain`, and the link. Nothing is emailed: sending waits for the user to choose a provider (see `NEWSLETTER.md`).

## 7. Report

One short message: what was added per project (title and one line each), what was looked at and dropped and why (one line), and the deploy link. If nothing passed the bar, say so in one line.

## Rules

- Laptop limits: background priority, one job at a time, nothing detached.
- Pages stay noindex until launch.
- No emoji, sentence case, plain words.
