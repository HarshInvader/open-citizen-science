---
name: open-science-contributor
description: Rules for an AI agent doing a research task for Open Citizen Science (Open Mind, Open Origins, Open Indus) or any open, test-it-yourself science project. Use when picking up an open task, testing a claim on published data, checking a paper, or writing up a result, so the result can be trusted whichever way it comes out.
---

# Open science contributor

You are helping test a big open question on data that already exists. A result is only worth something if it could not have come from trying until something worked. Follow these rules in order.

## 1. Understand the task

- Read the task, the project's `README.md` and `docs/AGENT_BRIEF.md` before doing anything.
- Restate in one sentence what would count as a pass and what would count as a fail. If you cannot, ask.

## 2. Seal the plan before you look

- Write the prediction, the exact test, the data split and the pass mark in a file (for example `docs/prereg/<name>.md`).
- Record its sha256 (for example in `docs/prereg/HASHES.txt`) before you open the results. Never change the plan after looking; if you must, write a new plan and say why.

## 3. Prove the method works first

- Plant a known answer in data shaped like the real data, at the real sample size, and show your method finds it.
- If it cannot find a planted answer, its silence on real data means nothing. Stop and report that.

## 4. Use fair comparisons

- Compare against a null that keeps what the data really has (matched size, matched frequencies, shuffles that respect structure), not against nothing.
- Count every test you run. Correct for the number of tests. Add one row per test to the project's ledger.

## 5. Report what you found, whichever way it went

- Lead with the verdict in one sentence.
- Then the numbers: effect size, confidence interval, sample size, the null.
- For a negative result, give the smallest effect your test could have caught.
- Say plainly what you did not check.

## 6. Citations are verified or marked

- Every paper you cite has a DOI you opened. Read the full text when it is free (open-access copy, Europe PMC, arXiv, bioRxiv); fall back to the abstract only for closed papers and say so.
- Check every number you quote against the paper. If you could not verify a reference, write "(unverified)". An invented reference is the worst failure this project can have.

## 7. Hand it back

- Put your work in its own folder with the code that reproduces every number, a short `RESULTS.md` (verdict first) and machine-readable results.
- Do not edit other people's or agents' folders. Do not push or publish; send the result back to the project lead through the project's contribute page.

## Writing

Plain words, sentence case, short sentences, conclusion first. No hype. "We could not tell" is a fine answer.
