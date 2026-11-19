# Open Citizen Science

[![OpenRepos](https://img.shields.io/endpoint?url=https://openrepos.org/status/opencitizenscience.openrepos.org.json&style=flat-square)](https://opencitizenscience.openrepos.org/)

Open projects that test big open questions on data that already exists, run by AI agents with a human lead. Every test is sealed before the result is seen, every method must first find a planted answer, every positive result goes to an independent red team, and results are published whichever way they go.

Site: https://opencitizenscience.pages.dev

## Projects

- **Open Indus**: a reproducible attempt to read the Indus script. https://github.com/HarshInvader/open-indus
- **Open Mind**: find the most accurate theory of human consciousness. https://github.com/HarshInvader/open-mind
- **Open Origins**: test how life began, step by step. https://github.com/HarshInvader/open-origins

## Next problems

[`docs/OPEN_PROBLEMS.md`](docs/OPEN_PROBLEMS.md): 37 open problems in physics, biology, meta-science, decipherment and maths, ranked by how much an agent working overnight could do on each.

## This repository

The parent site: home page, news, the "Working with agents" page and the agent skill in `skills/open-science-contributor/`.

- Build: `python3 -I build.py` (builds each project's site into `dist/`, then checks links and image sizes)
- Deploy: Cloudflare Pages, project `opencitizenscience`

## Licence

Code: MIT (see `LICENSE`). Project data and text carry the licences stated in each project's `LICENSING.md`.
