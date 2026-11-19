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
| 2 | [Proto-Elamite](#2-proto-elamite) | Decipherment | 4 | 4 | 4 | 3 | 19 | Iran's earliest writing, mostly unread. Its known parts test our Indus method, and even a partial reading bears on the Indus language question |
| 3 | [Lithium in drinking water and suicide](#3-lithium-in-drinking-water-and-suicide) | Public health | 4 | 5 | 5 | 4 | 22 | EPA's national data became final on 27 Aug 2026. No suicide analysis yet |
| 4 | [Is the Big Ring real?](#4-is-the-big-ring-real) | Cosmology | 4 | 5 | 5 | 4 | 22 | The main critique left the Big Ring untested. A new ring claim came out in 2026 |
| 5 | [Impossible numbers in published papers](#5-impossible-numbers-in-published-papers) | Meta-science | 4 | 4 | 5 | 4 | 21 | The largest checks are still 2016–17. Agents can extract the numbers, and the checks are mechanical |
| 6 | [Galaxy spin mirror test](#6-galaxy-spin-mirror-test) | Cosmology | 3 | 5 | 5 | 5 | 21 | Cheap and decisive. No automated classifier has been tested on mirrored images |

Proto-Elamite ranks above its score for two reasons. Reading even part of it would tell us things nothing else can (see its section). And it is the best calibration we can get for Open Indus: if our method recovers the parts of Proto-Elamite that are already known, our Indus results become far more credible.

## The full ranked list

| Rank | Problem | Field | I | N | T | C | Score | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | Wide binaries on Gaia DR4 | Astrophysics | 5 | 2 | 5 | 4 | 21 | Fixed deadline |
| 2 | Proto-Elamite | Decipherment | 4 | 4 | 4 | 3 | 19 | Ranked up: what a reading would teach, and Indus calibration |
| 3 | Lithium in water and suicide (UCMR5) | Public health | 4 | 5 | 5 | 4 | 22 | |
| 4 | Big Ring / Giant Arc significance | Cosmology | 4 | 5 | 5 | 4 | 22 | |
| 5 | GRIM, SPRITE and statcheck audit at scale | Meta-science | 4 | 4 | 5 | 4 | 21 | |
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
| 18 | RCT baseline screen predicting retractions | Meta-science | 4 | 3 | 4 | 3 | 18 | Pairs with #5 |
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

**The bigger picture.** For about 90 years, galaxies and clusters have moved as if they held far more mass than we can see. The standard answer is dark matter, but decades of direct searches have not found a dark matter particle. The main alternative, MOND (modified Newtonian dynamics), says gravity itself changes when acceleration drops below a tiny threshold, about 1.2 × 10⁻¹⁰ m/s². MOND predicts galaxy rotation curves remarkably well. It struggles with galaxy clusters and the cosmic microwave background.

Galaxies can't settle the question, because any test there can be explained either way by adjusting how much dark matter there is and where. Wide binaries can. Two stars thousands of au apart pull on each other with accelerations below MOND's threshold, and a pair that size should contain essentially no dark matter. So Newton and MOND make different predictions about one simple, measurable thing: how fast the stars orbit each other. That makes this one of the few direct tests of gravity at very low accelerations.

The results so far split by group. Chae and Hernandez report a MOND-like boost. Banik, and Pittordis & Sutherland, report Newtonian orbits. The dispute is now about analysis choices, so a test whose choices are sealed in advance, run on better data, addresses the dispute itself.

- **Question:** Do stars in wide pairs, more than about 2,000 au apart, orbit faster than Newton allows, with the roughly 1.4× gravity boost that MOND predicts?
- **Why us:** The groups cut the sample differently, model hidden third stars differently and correct velocities differently. Gaia DR4 brings per-epoch positions and a catalogue of non-single stars, which bears directly on the hidden-third-star problem. A protocol sealed before the release and run unchanged on release day is exactly our method.
- **Data:** [Gaia archive](https://gea.esac.esa.int/archive/). DR4 is planned for 2 Dec 2026 ([ESA news](https://www.cosmos.esa.int/web/gaia/news), [release scenario](https://www.cosmos.esa.int/web/gaia/release)). Stars within 200 pc come to about 1 GB.
- **First test:** Seal the cuts, the hidden-star model and the estimator. On DR3, show the method recovers a planted γ = 1.4 boost and a planted γ = 1.0 (no boost). On 2 Dec, run it unchanged on DR4.
- **Result:** The range of likely values for γ excludes 1.0 or 1.4.
- **Crowding:** About five groups: Chae, Hernandez, Banik ([MNRAS](https://academic.oup.com/mnras/article/547/2/stag342/8497444)), and Pittordis & Sutherland ([arXiv 2504.07569](https://arxiv.org/abs/2504.07569)). Someone has already posted a pre-registered DR4 protocol ([arXiv 2608.24556](https://arxiv.org/abs/2608.24556), unverified).
- **Risk:** It is a race. Our edge is the sealed protocol, the planted-answer check and speed, not novelty.

### 2. Proto-Elamite

**The bigger picture.** Proto-Elamite is the earliest writing from Iran and one of the oldest scripts in the world. About 1,700 clay tablets survive, from roughly 3300–2900 BCE. That is the same time as the first writing in Mesopotamia, which it probably borrowed from in part. Most tablets come from Susa, but some were found as far east as Tepe Yahya and Shahr-i Sokhta. That puts one writing system across more than 1,000 km of the Iranian plateau, including sites on the routes that later linked Mesopotamia to the Indus. Then the script disappeared after only a few generations.

The tablets are accounts: grain, livestock, workers and rations. The number systems and some commodity signs were worked out decades ago (Englund, Damerow, Friberg). Dahl estimates that 80–90% of the non-numerical signs are still unread. Those signs include people's names, job titles and words, which are where the language is.

**What a reading, even a partial one, could teach us:**

- **Which language was spoken on the Iranian plateau 5,000 years ago.** It is usually assumed to be an early form of Elamite, but nobody has shown it. Elamite has no proven relatives. Readable names alone, even without full sentences, would give the earliest direct evidence of the language and its sounds.
- **Evidence on where Dravidian languages came from, and so on the Indus.** The Elamo-Dravidian hypothesis (McAlpin, Southworth) says Elamite and the Dravidian languages of South India are related. Most linguists consider it unproven ([overview](https://en.wikipedia.org/wiki/Elamo-Dravidian_languages)). But a 2025 genetics paper (Sequeira et al., *European Journal of Human Genetics*, [PubMed](https://pubmed.ncbi.nlm.nih.gov/41136592/)) places a "proto-Dravidian" ancestry between the Iranian plateau and the Indus valley more than 4,400 years ago. Dravidian is one of the leading candidates for the language of the Indus script. Early Elamite words would be the oldest linguistic evidence that could support or weaken that chain. Genes can't tell us what language people spoke; written words can.
- **How writing spread.** Did writing spread as a finished idea from Mesopotamia, or was it reinvented locally? Did sound-based signs appear here very early? Desset argues Proto-Elamite leads into Linear Elamite, which he read in 2022 as a mostly sound-based script ([Smithsonian](https://www.smithsonianmag.com/history/have-scholars-finally-deciphered-a-mysterious-ancient-script-180980497/)). If true, that would be one of the earliest cases of writing representing sounds. Dahl disputes both claims. A test that compares the two scripts against a fair null would help settle it.
- **How the first state on the Iranian plateau was run.** Who managed labour and goods, what titles people held, and how far the administration reached. The accounts are the only written record of it.
- **Whether our Indus method works.** Proto-Elamite is the closest thing to Indus that is partly solved. Testing on it is the strongest validation we can get.

- **Question:** Can our method, given no labels, recover what is already known about Proto-Elamite? If so, do late Proto-Elamite sign sequences line up with Linear Elamite readings better than chance?
- **Why us:** About one group does computational work on it (Born, Sarkar, Kelley, Monroe). Desset works on the Linear Elamite side, and Dahl runs the digitisation. The work suits agents: exhaustive sign-sequence statistics, alignment against a second script, and nulls that respect the structure of accounting tablets.
- **Data:** about 1,600 tablets online through CDLI (unverified URL) and the [SFU pe-decipher-toolkit](https://github.com/sfu-natlang/pe-decipher-toolkit). Linear Elamite sign readings come from Desset et al. 2022.
- **First test:** The known parts are the planted answer. Hide the number systems and the known header, owner and commodity signs, and check the pipeline recovers them without labels. If it does, seal a test of whether late sign sequences align with Linear Elamite readings better than shuffles that keep sign frequencies and tablet structure. Then use the method on the unread signs that look like names, which is where the language shows.
- **Result:** First, a validated method. Then a measured answer on the link to Linear Elamite: support, no support, or a test too weak to tell. Any readings it proposes for name signs feed back into the Elamite question.
- **Crowding:** [Born et al. 2019](https://aclanthology.org/W19-2516.pdf); Monroe, Kelley, Born & Sarkar 2025, *Near Eastern Archaeology* 88(4) ([DANES newsletter](https://opendanes.org/newsletter/2026-02.html)); a [2026 Cambridge Element](https://www.cambridge.org/core/elements/abs/protoelamite/3684B7262E21A8B6AF8657D948A5B1A6); Desset's proposed sign values for Proto-Elamite, which few accept.
- **Risk:** CDLI transliterations already build in earlier scholars' sign groupings. The corpus is small and mostly accounting. Desset's Linear Elamite readings are contested, so any link that rests on them is only as good as they are. The test should use only the signs whose readings are least disputed.

### 3. Lithium in drinking water and suicide

**The bigger picture.** About 49,000 Americans die by suicide each year. At high doses, lithium is the best-established drug for preventing suicide in bipolar disorder. Since the 1990s, studies in Texas, Japan, Austria and elsewhere have reported fewer suicides where tap water carries more natural lithium, at doses a thousand times lower. Meta-analyses mostly find an inverse link. But almost all of these compare regions rather than people, which leaves room for confounding, and a large Danish study that followed individuals found nothing below 31 µg/L. Some researchers have proposed adding lithium to water, like fluoride.

At the same time, EPA tested lithium as a possible contaminant and set a health reference level of 10 µg/L, which 24% of large systems exceed. So the US is considering regulating lithium down at roughly the levels claimed to protect against suicide. A national test, on the first nationwide data, informs both decisions.

- **Question:** Do US counties with more natural lithium in their public water have fewer suicides, after accounting for altitude, how rural they are and gun ownership?
- **Why us:** EPA's UCMR5 measured lithium in over 10,000 water systems from 2023 to 2025. The final data came out on 27 August 2026 ([EPA](https://www.epa.gov/dwucmr/fifth-unregulated-contaminant-monitoring-rule), [Water Online](https://www.wateronline.com/doc/epa-releases-final-ucmr-drinking-water-data-for-pfas-and-lithium-0001)). The only published use so far is a dementia study ([Environmental Pollution 2026](https://www.sciencedirect.com/science/article/abs/pii/S0269749126001363)). The tedious step, linking water systems to counties, is what agents are good at.
- **Data:** UCMR5 occurrence files (the lithium reporting limit is 9 µg/L); [CDC WONDER](https://wonder.cdc.gov) county suicide counts (counts under 10 are hidden).
- **First test:** Seal a Poisson model with a spatial term. Plant a rate ratio of 0.90 per 10 µg/L into simulated counts and recover it. Nulls: shuffle lithium values between counties within a state, and use other injury deaths as a placebo outcome.
- **Result:** Pass means a protective rate ratio that survives both nulls and the placebo. Fail means the confidence interval rules out the Texas estimate (Blüml 2013).
- **Risk:** County-level comparisons can be confounded. The Danish null result ([PMC5486313](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5486313/)) suggests any effect may be small. Many US levels are near the reporting limit.

### 4. Is the Big Ring real?

**The bigger picture.** Modern cosmology assumes that on large enough scales the universe looks the same everywhere and in every direction (the cosmological principle). The standard model (ΛCDM) predicts that structure stops growing above a few hundred megaparsecs. Several claimed structures are much larger: the Giant Arc (about 1 Gpc) and the Big Ring (about 400 Mpc across, 1.3 Gpc around), both found by Alexia Lopez in Mg II absorbers, along with earlier claims like the Huge Large Quasar Group. If any is real, the cosmological principle fails at those scales.

These claims sit beside other strains on ΛCDM: the Hubble tension and the cosmic dipole (#7). The weak point of every "too big" claim is the same. The search looked across many places, scales and thresholds, so the chance of finding something ring-like somewhere in random data is much larger than the chance at one fixed spot. A clean test settles one claim and gives a method for all the others.

- **Question:** Do the Giant Arc and the Big Ring stay significant once you count every place and scale the search could have looked?
- **Why us:** Sawala's group tested the Arc but said its work "does not directly address the Big Ring" ([arXiv 2505.11072](https://arxiv.org/abs/2505.11072)). A new Giant Ring claim appeared in 2026 ([arXiv 2604.17534](https://arxiv.org/abs/2604.17534)). The fair null is simple: run the claimants' own search on random skies.
- **Data:** SDSS DR16 Mg II absorber catalogues.
- **First test:** Reproduce Lopez's search. Plant a ring the size and contrast of the Big Ring into random fields and recover it. Then count how often random skies produce something as strong.
- **Result:** A global p-value for the Big Ring.
- **Crowding:** Two groups ([Sawala 2025](https://arxiv.org/abs/2502.03515); Lopez's [rebuttal](https://arxiv.org/abs/2504.14940)).
- **Risk:** The absorber sightlines are patchy, so the random skies must follow the same mask.

### 5. Impossible numbers in published papers

**The bigger picture.** Large replication projects found that only about 40% of psychology results held up when repeated, with similar problems in cancer biology and economics. Part of that is fraud, but much more is simple error: numbers mistyped, miscalculated or misreported. Nuijten's 2016 statcheck study found that about half of psychology papers contained at least one p-value inconsistent with its own test statistic, and about one in eight had an error big enough to change the conclusion.

These errors flow into meta-analyses, clinical guidelines and policy. Simple arithmetic checks can expose them. GRIM, for example, tests whether a reported mean is possible at all given the sample size, and checks like it helped expose the Cornell food lab scandal. These checks have only been run by hand, on dozens of papers. An agent pipeline could run them on tens of thousands, give the first real estimate of how common impossible numbers are, and leave a tool journals could use.

- **Question:** What share of open-access psychology and medical papers report means, standard deviations or p-values that are mathematically impossible?
- **Why us:** The baselines are still Brown & Heathers 2017 (71 papers, [link](https://journals.sagepub.com/doi/abs/10.1177/1948550616673876)) and Nuijten 2016 (statcheck, [link](https://link.springer.com/article/10.3758/s13428-015-0664-2)). A 2026 study found that LLM auditors miss the plausible-looking errors most ([arXiv 2609.09696](https://arxiv.org/abs/2609.09696), unverified). So the agent only extracts the numbers, and the checks themselves run as plain code (GRIM, GRIMMER, SPRITE, statcheck).
- **Data:** the [PMC open-access subset](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/).
- **First test:** Plant 500 known-impossible values into real tables. Pass mark: at least 90% caught and under 2% falsely flagged on Brown & Heathers' hand-checked set. Then run on 20,000 papers.
- **Result:** Error rates by field and year, a list of confirmed errors, and the code.
- **Risk:** A wrong extraction becomes a false accusation. A person checks every flag before any paper is named.

### 6. Galaxy spin mirror test

**The bigger picture.** If galaxies across the sky spin one way more often than the other, the universe has a preferred handedness. That would break the assumption that it looks the same in every direction, and some take it as a hint that our universe formed inside a black hole that was itself spinning. Lior Shamir has reported such an asymmetry for years, most recently in JWST deep fields (2025), and the claim drew wide press coverage.

There is a famous precedent. In 2008, Galaxy Zoo volunteers classified more galaxies as spinning anticlockwise. When the team showed the same galaxies mirror-flipped, the excess stayed with the volunteers rather than the galaxies: it was a bias in human perception, not the sky (Land et al. 2008). No one has run that check on the automated classifiers behind the recent claims. A classifier that isn't exactly mirror-symmetric can produce an asymmetry from nothing.

- **Question:** Do galaxies spin one way more often than the other, as Shamir claims, or does the bias come from how spins are classified?
- **Why us:** The debate is essentially Shamir against Patel & Desmond ([arXiv 2404.06617](https://arxiv.org/abs/2404.06617), [code](https://github.com/harrydesmond/GalaxySpinAnisotropy)). Their critique was about the statistics. Testing the classifier on mirrored images is cheap and decisive.
- **Data:** [JADES at MAST](https://archive.stsci.edu/hlsp/jades), SDSS, Galaxy Zoo, HSC.
- **First test:** Classify every galaxy and its mirror image. A fair classifier gives exactly opposite answers. Then plant a 2% asymmetry and recover it at the real sample size.
- **Result:** The asymmetry survives a classifier that passes the mirror check, or it disappears.
- **Risk:** Low prestige. Many astronomers already consider the claim dead.

## The rest, with their bigger picture

- **7. Cosmic dipole.** The CMB is warmer in one direction because we move through space at about 370 km/s. Distant galaxies and quasars should show the same direction with a matching size. Counts of quasars and radio galaxies show roughly twice the expected dipole, reported at 3.3σ to 6.7σ depending on choices ([Bashir et al. 2026](https://arxiv.org/abs/2511.00822); [MNRAS 2025](https://academic.oup.com/mnras/article/543/4/3229/8266509)). If the excess is real, the universe is not the same in every direction, which undermines nearly every cosmological measurement. Test: run every catalogue × mask × flux cut × estimator on shared simulated skies with a planted dipole. Data: CatWISE2020, NVSS, RACS, LoTSS-DR2.
- **8. ITP mice.** The anti-aging field wants drugs that slow aging itself, not ones that just delay a few diseases. The usual evidence is a slower rise in death risk with age, and the NIA Interventions Testing Program is the most rigorous source of such results (rapamycin, acarbose, 17α-estradiol). A 2026 worm paper ([Nat Commun](https://www.nature.com/articles/s41467-026-71780-7)) argues that the same pattern can come from frail animals simply living longer, which is the opposite of what the field wants. Untested in mice. Data: [MPD ITP1](https://phenome.jax.org/projects/ITP1), per-mouse lifespans. "The data can't tell them apart" is itself publishable, because it would mean lifespan curves can't support the claims built on them.
- **9. Criticality.** One of the broadest ideas in neuroscience is that the brain tunes itself to the edge between order and chaos, where it can process information best. Hengen & Shew ([Neuron 2025](https://www.cell.com/neuron/fulltext/S0896-6273(25)00391-5)) propose it as the brain's set point and list eight predictions, but test them only on published summary values. Random noise is known to fake the key signature ("avalanches"). Re-test from raw data on DANDI and Allen Neuropixels against those nulls. Loss of criticality under anaesthesia and sleep links directly to Open Mind.
- **10. June 2025 Forbush decrease.** Svensmark's hypothesis is that cosmic rays seed clouds, so the Sun, by shielding Earth from cosmic rays, could change climate. It is a long-running dispute because sceptics use it to downplay CO₂. Sudden cosmic-ray drops (Forbush decreases) are natural experiments. June 2025 had the largest in 20 years ([arXiv 2510.25046](https://arxiv.org/abs/2510.25046)), and its effect on clouds hasn't been studied. Seal the method on historical events before opening CERES and MODIS data for 2025. One event, so a null result says little.
- **11. Solar protons and earthquakes.** Earthquake prediction is one of the most hyped areas of geophysics. A 2020 *Scientific Reports* paper ([arXiv 2004.02300](https://arxiv.org/abs/2004.02300)) reported, at p < 10⁻⁵, that solar-wind proton density predicts large earthquakes a day later. If true, that is a new physical link. It has never been independently tested. The years 2020–2026 make a ready out-of-sample test. Data: OMNIWeb and ISC-GEM, under 100 MB. Doable overnight.
- **12. CHIME FRB periods.** Fast radio bursts are millisecond flashes from other galaxies, and what produces them is still debated. Two repeaters switch on and off on cycles (16 and about 160 days), which points to binary systems or wobbling magnetars. How many of CHIME's 83 repeaters have a cycle would show how common those mechanisms are. No one has searched them all uniformly. Fold each source while accounting for when CHIME was looking, and correct for searching many periods.
- **13. Placebo response.** In several fields, especially psychiatry and pain, drugs fail trials more often because the placebo arm keeps improving more. That raises drug development costs and may kill useful drugs. Is it happening across all of medicine, and do larger, more international trials explain it? Data: [AACT](https://aact.ctti-clinicaltrials.org).
- **14. Mendelian randomisation re-runs.** This method uses genetic variants as natural experiments to infer cause, and thousands of papers a year use it on public data, many with little scrutiny. Critics call much of it a paper mill. Re-run 100 published studies from their stated [OpenGWAS](https://gwas.mrcieu.ac.uk) IDs and apply robustness checks for genetic variants that affect the outcome another way. The result: how much of the literature holds up.
- **15. COGITATE.** The largest head-to-head test of two consciousness theories (IIT and global workspace) found that both missed some predictions ([Nature 2025](https://www.nature.com/articles/s41586-025-08888-1)). The result set off the public dispute over calling IIT "pseudoscience". The [data is public](https://www.arc-cogitate.com/data-release). Do the verdicts hold across every reasonable way of turning the predictions into analyses? For Open Mind.
- **16. Obelisk hosts.** Obelisks are a class of circular RNA elements found in 2024 in human mouth and gut microbiome data. They may be a new kind of life-like replicator, somewhere between viroids and viruses. The basic question is what they live in, and only one host is confirmed: *S. sanguinis* ([Nat Commun 2026](https://www.nature.com/articles/s41467-026-71096-6)). Find hosts from which organisms keep appearing in the same samples across Logan's assemblies of the SRA. The method must first recover *S. sanguinis* blind. This is close to Open Origins' interests.
- **17–18. Trial integrity.** Doctors and guidelines trust trials as published. If a trial quietly changes its main outcome after seeing the data, or reports baseline numbers that are too neat to be real, that trust is misplaced. Compare each trial's registered primary outcome with the outcome its paper reports, for about 10,000 trials. Then test whether the Carlisle baseline screen predicts retractions, with that test sealed in advance.
- **19. Ionospheric earthquake precursors.** Heki reported changes in the ionosphere, the charged upper atmosphere measured by GPS signals, 20–60 minutes before great earthquakes. A real precursor would give warning time that saves lives. A 2026 study ([EPS](https://link.springer.com/article/10.1186/s40623-026-02446-3)) says they are ordinary travelling disturbances. The missing number is how often the same detector fires on random days.
- **20. Gene transfer into animals.** Bacteria swap genes constantly. Whether animals pick up useful bacterial genes is a live question for how evolution works, and claims keep appearing (a November 2026 preprint claims record levels in fungus gnats). Contamination has overturned similar claims before, most famously the 2015 tardigrade genome. Score 50 or more published claims for contamination, using read coverage, long reads spanning the gene, and neighbouring animal genes.
- **21. AMOC.** Collapse of the Atlantic overturning circulation would change European and tropical climate. Early-warning statistics on sea temperatures have produced headline predictions (collapse as early as 2025–2095). They are crowded and already disputed, but no one has run one sealed test across every analysis choice.
- **22–30.** Each is a re-test of a specific claim with open data. Replay is how the brain may consolidate memories. The EEG 1/f slope is used as a biomarker for autism and schizophrenia research. Peto's paradox asks why whales don't get more cancer, with implications for cancer defence. Inner-core rotation affects models of Earth's magnetic field. Genetic code optimality is a central argument about early life (Open Origins). Myth motifs may preserve traces of migration from tens of thousands of years ago. Lewontin's paradox asks why genetic diversity barely tracks population size. De novo genes test how new genes are born. GW echoes would be evidence for exotic alternatives to black holes.
- **31–34. Maths records.** Honest backups with perhaps a 20–30% chance of a small record each. The results are machine-checkable, but the fields are crowded with AI efforts or need far more compute.
- **35–36. Cypro-Minoan and rongorongo.** Other undeciphered scripts where our Indus tools could transfer, but with smaller corpora and less clear access than Proto-Elamite.

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
2. **Proto-Elamite inside Open Indus.** First the known-answer test, then the Linear Elamite test.
3. **Lithium and Big Ring in parallel.** Each is a clean overnight first run.
4. Before starting any problem, open and verify every reference it relies on. These came from web searches.
