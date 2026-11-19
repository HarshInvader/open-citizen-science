# Paper watch: how new papers get onto the project sites

Runs every other day for Open Origins, Open Mind and Open Indus. The sources it checks are in `sources.json`. Edit that file to add a journal, a preprint server, a search term or a leading author.

## 1. Sweep (automatic, about 15 minutes)
`python3 -I tools/paperwatch/sweep.py`

- It searches Europe PMC (journals and bioRxiv/medRxiv preprints), Crossref (every publisher, including humanities journals), arXiv and Zenodo.
  - Searches cover each project's keywords and leading authors, and start 3 days before the last sweep.
- It writes ranked candidates to `.local/paperwatch/<date>/<project>.md` and `.json`.
- Anything already on a news page, or already shown in an earlier sweep, is skipped.

## 2. Triage (agent)
Triage every dated folder in `.local/paperwatch/` that has no `LOG.md` yet, not only today's. The first backfill sweep (2026-11-19) is one of these. Read each project's candidate list. Keep a paper only if at least one of these holds:
- it is a primary result that changes what the field believes about the project's core question, at a strong venue or from a leading lab;
- it is new open data, code or a benchmark this project could test on;
- it directly tests, supports or refutes a theory or claim this project works on, including our own past results (see the project's `docs/NEGATIVE_ATLAS.md` and experiment `RESULTS.md` files);
- it is a major critique, replication or failed replication in an active dispute.

Drop the rest:
- reviews that add nothing;
- off-topic hits from author searches;
- conference abstracts;
- minor technical papers.

**Expect 0 to 5 papers per project per sweep.** None is a fine outcome. Never add a paper because of its venue alone.

## 3. Read and analyse (agent)
For each kept paper:
- **Open it.** Read the DOI landing page and at least the abstract. Read the open full text when it is legal (Europe PMC, PMC, the publisher's open-access page, arXiv, bioRxiv). Never use Sci-Hub or get around a paywall. Use the User-Agent `open-research-site/1.0` and no personal details.
- **Check the basics:** who, venue, date and the DOI. Every number written must appear in what was opened. If only the abstract was read, write "(abstract only)" in `tech`.
- **Write the analysis**, using that project's `site/news.json` fields:
  - `head`: a plain claim, with the authors in brackets;
  - `gist`: one line;
  - `plain`: a short story for anyone;
  - `tech`: methods, key numbers and caveats, for specialists;
  - `borrow`: what this project takes from the paper, or how it bears on our tests and results. Be specific: name the task, experiment or prediction it affects. If it suggests a new sealed test, say so in one sentence.
  - `status`: planned, running, done or context;
  - `topic`: one of the file's `topics`;
  - `section`: "latest";
  - `kind`: "Paper" or "Preprint";
  - `url`: https://doi.org/…;
  - `verified`: true only after the checks above.
- **Style:** plain words, one idea per sentence, no hype, honest about limits. Never invent a number or a reference.
- Insert new items at the top of `items`, newest first.

## 4. Publish
1. **Origins and Mind** are built into the hub:
   - run `cd open-citizen-science && nice python3 -I build.py`;
   - then deploy with `npx wrangler pages deploy dist --project-name opencitizenscience --branch main --commit-dirty=true`.
2. **Indus** is its own site (openindus.pages.dev):
   - follow the build and deploy notes in `indus-decipher` (its `site/build.py`);
   - if they are unclear, update `site/news.json` only and note it for the Indus thread.
3. **Commit and push each changed repo** using the push routine in `.local/thread_rules.md`:
   - add files one by one;
   - the leak scan must print nothing;
   - end the message with the co-author line.
4. **Write a run log** to `.local/paperwatch/<date>/LOG.md`. For each project, list:
   - the candidate count;
   - what was added and why;
   - notable rejects, each with a one-line reason;
   - any paper that should change our plans, which also goes to the owner's summary.
