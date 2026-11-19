# Open problems where agents could make fast progress

A ranked list of research problems, beyond our three projects, where an agent working overnight on public data could produce a real result in days to weeks. Each one is tested the usual way: seal the plan, recover a planted answer, compare against a fair null, red-team positives, publish either way.

Status: scouting list, made 19 November 2026. The literature checks come from web searches. Most papers were not opened in full, so every reference must be verified under rule 6 of the contributor skill before anyone builds on it. Links marked "(unverified)" were not confirmed at all.

## What we looked for

A good problem here has four things:

1. **It matters.** A positive result or a clean negative would get cited.
2. **Few people work on it.** The data sits unanalysed, or only one or two groups are involved, or the work is tedious and systematic (exhaustive searches, re-analysis across many datasets, independent re-tests of a claimed anomaly).
3. **Agents can do it.** Public data, a laptop or a modest GPU, no wet lab, no contact with people.
4. **One test decides it.** There is a pre-registerable test with a pass and fail, and a first result within weeks.

We avoided areas where big labs or collaborations are racing, since they would beat us there.

## How we scored

Each problem gets 1 to 5 on importance (I), neglect (N), tractability for agents (T) and chance of a publishable result within a month (C).

**Score = 2×I + N + T + C** (maximum 25). Importance counts double so that quick but minor re-tests don't rise to the top. The final rank also takes timing and fit with our projects into account. Where it differs from the score, the reason is given.

## The top six: start here

| Rank | Problem | Field | I | N | T | C | Score | Why now |
|---|---|---|---|---|---|---|---|---|
| 1 | [Wide-binary gravity test on Gaia DR4](#1-wide-binary-gravity-test-on-gaia-dr4) | Astrophysics | 5 | 2 | 5 | 4 | 21 | DR4 is released on **2 Dec 2026**. Seal the protocol before then |
| 2 | [Lithium in drinking water and suicide](#2-lithium-in-drinking-water-and-suicide) | Public health | 4 | 5 | 5 | 4 | 22 | EPA's national data became final on 27 Aug 2026. No suicide analysis yet |
| 3 | [Is the Big Ring real?](#3-is-the-big-ring-real) | Cosmology | 4 | 5 | 5 | 4 | 22 | The main critique left the Big Ring untested. A new ring claim came out in 2026 |
| 4 | [Impossible numbers in published papers](#4-impossible-numbers-in-published-papers) | Meta-science | 4 | 4 | 5 | 4 | 21 | The largest checks are still 2016–17. Agents can extract the numbers, and the checks are mechanical |
| 5 | [Proto-Elamite](#5-proto-elamite) | Decipherment | 4 | 4 | 4 | 3 | 19 | A sister script to Indus with known answers to test our pipeline against. About one group works on it |
| 6 | [Galaxy spin mirror test](#6-galaxy-spin-mirror-test) | Cosmology | 3 | 5 | 5 | 5 | 21 | Cheap and decisive. The claim has never been tested on mirrored images |

Proto-Elamite is ranked above its score because it strengthens Open Indus: if our method recovers the parts of Proto-Elamite that are already known, that is the best evidence we can give that our Indus results mean something.

## The full ranked list

| Rank | Problem | Field | I | N | T | C | Score | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | Wide binaries on Gaia DR4 | Astrophysics | 5 | 2 | 5 | 4 | 21 | Fixed deadline |
| 2 | Lithium in water and suicide (UCMR5) | Public health | 4 | 5 | 5 | 4 | 22 | |
| 3 | Big Ring / Giant Arc significance | Cosmology | 4 | 5 | 5 | 4 | 22 | |
| 4 | GRIM, SPRITE and statcheck audit at scale | Meta-science | 4 | 4 | 5 | 4 | 21 | |
| 5 | Proto-Elamite syllabic layer | Decipherment | 4 | 4 | 4 | 3 | 19 | Ranked up for Indus |
| 6 | Galaxy spin mirror test | Cosmology | 3 | 5 | 5 | 5 | 21 | |
| 7 | Cosmic dipole across many analysis choices | Cosmology | 5 | 3 | 4 | 3 | 20 | |
| 8 | Lifespan drugs: slower aging or longer frailty? (ITP mice) | Biology of aging | 4 | 3 | 5 | 4 | 20 | |
| 9 | Is the brain set to criticality? | Neuroscience | 4 | 3 | 4 | 4 | 19 | Could become part of Open Mind |
| 10 | June 2025 Forbush decrease and clouds | Climate | 4 | 4 | 4 | 4 | 20 | Must seal before looking at the 2025 data |
| 11 | Solar protons and earthquakes, out-of-sample | Geophysics | 3 | 5 | 5 | 5 | 21 | Quick, minor result |
| 12 | Periods in CHIME repeating FRBs | Astrophysics | 3 | 4 | 5 | 4 | 19 | |
| 13 | Rising placebo response across all trials (AACT) | Meta-science | 3 | 4 | 5 | 4 | 19 | |
| 14 | Re-running published Mendelian randomisation studies | Epidemiology | 3 | 4 | 5 | 4 | 19 | |
| 15 | COGITATE across many analysis choices | Consciousness | 4 | 3 | 4 | 3 | 18 | Open Mind extension |
| 16 | Obelisk hosts from SRA co-occurrence | Microbiology | 4 | 4 | 3 | 3 | 18 | Compute and download cost |
| 17 | Outcome switching: registry vs journal paper | Meta-science | 4 | 3 | 4 | 3 | 18 | |
| 18 | RCT baseline screen predicting retractions | Meta-science | 4 | 3 | 4 | 3 | 18 | Pairs with #4 |
| 19 | Ionospheric earthquake precursors, false-alarm rate | Geophysics | 4 | 3 | 4 | 3 | 18 | Heavy GNSS processing |
| 20 | Gene transfer into animals: how much is contamination? | Genomics | 3 | 4 | 4 | 4 | 18 | |
| 21 | AMOC early warnings across many analysis choices | Climate | 5 | 2 | 5 | 3 | 20 | Ranked down: crowded |
| 22 | Hippocampal replay against calibrated nulls | Neuroscience | 3 | 4 | 4 | 3 | 17 | |
| 23 | EEG 1/f slope as an excitation–inhibition marker | Neuroscience | 3 | 2 | 5 | 4 | 17 | Close to Open Mind |
| 24 | Peto's paradox: does the data decide it? | Evolution | 3 | 2 | 5 | 4 | 17 | |
| 25 | Inner core: rotation or shape change? | Geophysics | 4 | 4 | 3 | 2 | 17 | Needs seismology expertise |
| 26 | Genetic code optimality across many null models | Origins | 3 | 2 | 5 | 3 | 16 | Open Origins extension, two 2026 preprints on it |
| 27 | Myth motifs and the Out-of-Africa signal | Folklore | 3 | 3 | 4 | 3 | 16 | |
| 28 | Lewontin's paradox in animals using k-mers | Population genetics | 3 | 4 | 3 | 3 | 16 | |
| 29 | De novo genes on telomere-to-telomere assemblies | Genomics | 3 | 3 | 4 | 3 | 16 | |
| 30 | Gravitational-wave echoes in GWTC-5 | Astrophysics | 3 | 3 | 4 | 3 | 16 | Small step on past work |
| 31 | Smallest 5-chromatic unit-distance graph (under 509 vertices) | Mathematics | 3 | 4 | 3 | 2 | 15 | Machine-checkable record |
| 32 | Sorting networks on 13 inputs: prove a lower bound of 44 | Computer science | 3 | 4 | 3 | 2 | 15 | |
| 33 | Erdős problems that a finite search can settle | Mathematics | 3 | 2 | 4 | 3 | 15 | Crowded with AI efforts |
| 34 | Schur S(7) and multicolour Ramsey lower bounds | Mathematics | 3 | 2 | 4 | 2 | 14 | |
| 35 | Cypro-Minoan: one script or three? | Decipherment | 3 | 3 | 3 | 2 | 14 | Corpus access unclear |
| 36 | Rongorongo: syllabary or not? | Decipherment | 3 | 3 | 3 | 2 | 14 | |
| 37 | Sleep spindle coupling and memory, re-analysed | Neuroscience | 3 | 3 | 2 | 2 | 13 | Too few open datasets |

## Top six in detail

### 1. Wide-binary gravity test on Gaia DR4

- **Question:** Do stars in wide pairs, more than about 2,000 au apart, orbit faster than Newton allows, with the roughly 1.4× gravity boost that MOND (modified Newtonian dynamics) predicts?
- **Why it matters:** It is the cleanest test of MOND that doesn't involve dark matter. Either answer will be cited.
- **Why us:** Groups disagree because they cut the sample differently, model hidden third stars differently and correct velocities differently. Gaia DR4 brings per-epoch positions and a catalogue of non-single stars, which bears directly on the hidden-third-star problem. A protocol sealed before the release and run unchanged on release day is exactly our method.
- **Data:** [Gaia archive](https://gea.esac.esa.int/archive/). DR4 is planned for 2 Dec 2026 ([ESA news](https://www.cosmos.esa.int/web/gaia/news), [release scenario](https://www.cosmos.esa.int/web/gaia/release)). Stars within 200 pc come to about 1 GB.
- **First test:** Seal the cuts, the hidden-star model and the estimator. On DR3, show the method recovers a planted γ = 1.4 boost and a planted γ = 1.0 (no boost). On 2 Dec, run it unchanged on DR4.
- **Result:** The range of likely values for γ excludes 1.0 or 1.4.
- **Crowding:** About five groups: Chae, Hernandez, Banik ([MNRAS](https://academic.oup.com/mnras/article/547/2/stag342/8497444)), and Pittordis & Sutherland ([arXiv 2504.07569](https://arxiv.org/abs/2504.07569)). Someone has already posted a pre-registered DR4 protocol ([arXiv 2608.24556](https://arxiv.org/abs/2608.24556), unverified).
- **Risk:** It is a race. Our edge is the sealed protocol, the planted-answer check and speed, not novelty.

### 2. Lithium in drinking water and suicide

- **Question:** Do US counties with more natural lithium in their public water have fewer suicides, after accounting for altitude, how rural they are and gun ownership?
- **Why it matters:** Earlier studies conflict, and each covered a few counties or one state. A national answer either way shapes the debate over trace lithium.
- **Why us:** EPA's UCMR5 measured lithium in over 10,000 water systems from 2023 to 2025. The final data came out on 27 August 2026 ([EPA](https://www.epa.gov/dwucmr/fifth-unregulated-contaminant-monitoring-rule), [Water Online](https://www.wateronline.com/doc/epa-releases-final-ucmr-drinking-water-data-for-pfas-and-lithium-0001)). The only published use so far is a dementia study ([Environmental Pollution 2026](https://www.sciencedirect.com/science/article/abs/pii/S0269749126001363)). The tedious step, linking water systems to counties, is what agents are good at.
- **Data:** UCMR5 occurrence files (the lithium reporting limit is 9 µg/L); [CDC WONDER](https://wonder.cdc.gov) county suicide counts (counts under 10 are hidden).
- **First test:** Seal a Poisson model with a spatial term. Plant a rate ratio of 0.90 per 10 µg/L into simulated counts and recover it. Nulls: shuffle lithium values between counties within a state, and use other injury deaths as a placebo outcome.
- **Result:** Pass means a protective rate ratio that survives both nulls and the placebo. Fail means the confidence interval rules out the Texas estimate (Blüml 2013).
- **Risk:** County-level comparisons can be confounded. A Danish study that followed individuals found no protection below 31 µg/L ([PMC5486313](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5486313/)). Many US levels are near the reporting limit.

### 3. Is the Big Ring real?

- **Question:** Do the Giant Arc and the Big Ring, structures about a gigaparsec across found in Mg II absorbers, stay significant once you count every place and scale the search could have looked?
- **Why it matters:** The claims challenge the standard cosmological model (ΛCDM).
- **Why us:** Sawala's group tested the Arc but said its work "does not directly address the Big Ring" ([arXiv 2505.11072](https://arxiv.org/abs/2505.11072)). A new Giant Ring claim appeared in 2026 ([arXiv 2604.17534](https://arxiv.org/abs/2604.17534)). The fair null is simple: run the claimants' own search on random skies.
- **Data:** SDSS DR16 Mg II absorber catalogues.
- **First test:** Reproduce Lopez's search. Plant a ring the size and contrast of the Big Ring into random fields and recover it. Then count how often random skies produce something as strong.
- **Result:** A global p-value for the Big Ring.
- **Crowding:** Two groups ([Sawala 2025](https://arxiv.org/abs/2502.03515); Lopez's [rebuttal](https://arxiv.org/abs/2504.14940)).
- **Risk:** The absorber sightlines are patchy, so the random skies must follow the same mask.

### 4. Impossible numbers in published papers

- **Question:** What share of open-access psychology and medical papers report means, standard deviations or p-values that are mathematically impossible?
- **Why it matters:** It measures directly how often published numbers are wrong, and it points to specific papers to correct.
- **Why us:** The baselines are still Brown & Heathers 2017 (71 papers, [link](https://journals.sagepub.com/doi/abs/10.1177/1948550616673876)) and Nuijten 2016 (statcheck, [link](https://link.springer.com/article/10.3758/s13428-015-0664-2)). A 2026 study found that LLM auditors miss the plausible-looking errors most ([arXiv 2609.09696](https://arxiv.org/abs/2609.09696), unverified). So the agent only extracts the numbers, and the checks themselves run as plain code (GRIM, GRIMMER, SPRITE, statcheck).
- **Data:** the [PMC open-access subset](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/).
- **First test:** Plant 500 known-impossible values into real tables. Pass mark: at least 90% caught and under 2% falsely flagged on Brown & Heathers' hand-checked set. Then run on 20,000 papers.
- **Result:** Error rates by field and year, a list of confirmed errors, and the code.
- **Risk:** A wrong extraction becomes a false accusation. A person checks every flag before any paper is named.

### 5. Proto-Elamite

- **Question:** Do late Proto-Elamite texts have a syllabic layer that matches the signs of Linear Elamite, which was deciphered in 2022?
- **Why it matters:** It would link Iran's earliest writing to its later script. It is also the best calibration we can get for Open Indus: a sister undeciphered script where some answers are already known.
- **Why us:** About one group works on it (Born, Sarkar, Kelley, Monroe), and 80–90% of the non-numerical signs are unread.
- **Data:** about 1,500 texts in CDLI (unverified) and the [SFU pe-decipher-toolkit](https://github.com/sfu-natlang/pe-decipher-toolkit).
- **First test:** The known parts are the planted answer. Can the Indus pipeline, given no labels, recover the number systems and the header and owner signs? If it can, test whether late sign sequences line up with Linear Elamite readings better than frequency-matched shuffles.
- **Crowding:** [Born et al. 2019](https://aclanthology.org/W19-2516.pdf); Monroe et al. 2025 ([DANES newsletter](https://opendanes.org/newsletter/2026-02.html)); a [2026 Cambridge Element](https://www.cambridge.org/core/elements/abs/protoelamite/3684B7262E21A8B6AF8657D948A5B1A6).
- **Risk:** CDLI transliterations already carry earlier scholars' sign readings, and the corpus is small.

### 6. Galaxy spin mirror test

- **Question:** Do galaxies spin one way more often than the other, as Shamir claims, or does the bias come from how spins are classified?
- **Why it matters:** The claims are extraordinary (an anisotropic universe, a "black-hole universe"). A decisive test would settle a public dispute.
- **Why us:** It is essentially Shamir against Patel & Desmond ([arXiv 2404.06617](https://arxiv.org/abs/2404.06617), [code](https://github.com/harrydesmond/GalaxySpinAnisotropy)). Their critique was about the statistics. Nobody has checked the classifier on mirror-flipped images, which is cheap and decisive.
- **Data:** [JADES at MAST](https://archive.stsci.edu/hlsp/jades), SDSS, Galaxy Zoo, HSC.
- **First test:** Classify every galaxy and its mirror image. A fair classifier gives exactly opposite answers. Then plant a 2% asymmetry and recover it at the real sample size.
- **Result:** The asymmetry survives a classifier that passes the mirror check, or it disappears.
- **Risk:** Low prestige. Many astronomers already consider the claim dead.

## The rest, briefly

- **7. Cosmic dipole.** Quasar and radio-galaxy counts show a dipole about twice what our motion predicts, reported at 3.3σ to 6.7σ depending on choices ([Bashir et al. 2026](https://arxiv.org/abs/2511.00822); [MNRAS 2025](https://academic.oup.com/mnras/article/543/4/3229/8266509)). Test: run every catalogue × mask × flux cut × estimator on shared simulated skies with a planted dipole. Data: CatWISE2020, NVSS, RACS, LoTSS-DR2.
- **8. ITP mice.** Does a drug like rapamycin slow the rate at which death risk rises with age, or does it let frail mice live longer? A 2026 worm paper ([Nat Commun](https://www.nature.com/articles/s41467-026-71780-7)) says the usual reading is wrong. Untested in mice. Data: [MPD ITP1](https://phenome.jax.org/projects/ITP1), per-mouse lifespans. "The data can't tell them apart" is itself publishable.
- **9. Criticality.** Hengen & Shew ([Neuron 2025](https://www.cell.com/neuron/fulltext/S0896-6273(25)00391-5)) list eight predictions from published summary values. Re-test them from raw data on DANDI and Allen Neuropixels, against nulls like thresholded noise that are known to fake "avalanches". Best run inside Open Mind.
- **10. June 2025 Forbush decrease.** The largest drop in cosmic rays in 20 years ([arXiv 2510.25046](https://arxiv.org/abs/2510.25046)); its effect on clouds hasn't been studied. Seal the method on historical events before opening CERES and MODIS data for 2025. One event, so a null result says little.
- **11. Solar protons and earthquakes.** Marchitelli et al. 2020 ([arXiv 2004.02300](https://arxiv.org/abs/2004.02300)) reported p < 10⁻⁵. The years 2020–2026 make a ready out-of-sample test. Data: OMNIWeb and ISC-GEM, under 100 MB. Doable overnight.
- **12. CHIME FRB periods.** No uniform search for periods across the 83 repeaters in Catalog 2. Fold each source while accounting for when CHIME was looking, and correct for searching many periods.
- **13. Placebo response.** Has the placebo-arm response risen across all conditions, and do trial size and location explain it? Data: [AACT](https://aact.ctti-clinicaltrials.org).
- **14. Mendelian randomisation re-runs.** Re-run 100 published studies from their stated [OpenGWAS](https://gwas.mrcieu.ac.uk) IDs and apply robustness checks for genetic variants that affect the outcome another way.
- **15. COGITATE.** Do the IIT and GNWT verdicts hold across every reasonable way of turning the predictions into analyses? ([data](https://www.arc-cogitate.com/data-release), [Nature 2025](https://www.nature.com/articles/s41586-025-08888-1)). For Open Mind.
- **16. Obelisk hosts.** Obelisks are a new class of RNA element. Find their bacterial hosts from which organisms keep appearing in the same samples across Logan's assemblies of the SRA. The method must first recover *S. sanguinis*, the one confirmed host ([Nat Commun 2026](https://www.nature.com/articles/s41467-026-71096-6)).
- **17–18. Trial integrity.** Compare each trial's registered primary outcome with the outcome its paper reports, for about 10,000 trials. Then test whether the Carlisle baseline screen predicts retractions, with that test sealed in advance.
- **19. Ionospheric earthquake precursors.** Find the false-alarm rate on random dates for reported pre-earthquake anomalies in GPS-derived electron counts. A 2026 study ([EPS](https://link.springer.com/article/10.1186/s40623-026-02446-3)) says they are ordinary travelling disturbances.
- **20. Gene transfer into animals.** Score 50 or more published claims of bacterial genes in animal genomes for contamination, using read coverage, long reads spanning the gene, and neighbouring animal genes.
- **21–37.** See the table. The maths records (31–34) are honest backups, with perhaps a 20–30% chance of a small record each. They are crowded with AI efforts or need far more compute.

## Considered and dropped

- **Erdős problems in general:** about 18 already solved by AI. Only the obscure ones a finite search can settle are left (kept as #33).
- **Hadamard matrices:** order 668 and the other missing orders below 2000 were constructed in August 2026.
- **Busy Beaver BB(6), covering designs, Ramsey two-colour bounds:** many people and agents already working on them.
- **Linear A:** a pre-registered structural study already exists on Zenodo. Its authors would be collaborators rather than a gap.
- **Voynich, Khitan small script:** a crowded hobbyist field, and no machine-readable corpus.
- **Hubble tension, CMB Cold Spot, Planet Nine:** too crowded, or waiting for data (LSST).
- **Fine-structure constant dipole:** needs expert spectral fitting, and ESPRESSO already reports no signal.
- **GNoME materials audit:** done by a NIST-led team in 2026. We found no strong materials or chemistry candidate, because most disputes there need wet-lab data or the paywalled ICSD.
- **Dyson-sphere candidates:** mostly explained by background galaxies.
- **Image duplication screening, GEO batch audits, economics reproducibility:** commercial tools or other agent projects already do these at scale.
- **Sleep clearance ("brain washing"):** no open data.

## What to do next

1. **Wide binaries, this week.** The protocol has to be sealed and pass its planted-answer check on DR3 before 2 Dec.
2. **Lithium and Big Ring in parallel.** Each is a clean overnight first run.
3. **Proto-Elamite inside Open Indus,** as a calibration of the pipeline.
4. Before starting any problem, open and verify every reference it relies on. These came from web searches.
