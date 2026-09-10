# Reference and novelty audit — 2026-09-08

## Two verification passes

The bibliography has **23 entries**, all cited in the manuscript. First, titles, ordered authors and dates were retrieved from arXiv citation metadata, PMLR proceedings metadata, or publisher-deposited Crossref records. Published conference records were additionally checked for six entries. The CIFAR reference was checked against the primary technical-report source; its author is Alex Krizhevsky, without adding a supervisor as a coauthor from secondary bibliographies.

Second, `verify_manuscript.py` independently retrieved the 22 machine-readable primary records again and checked title identity, then checked all citation keys, publication-source title presence, and the absence of unreferenced bibliography entries. Results and source hashes are retained in [second_pass.json](references/second_pass.json), with metadata and the supported claim for every entry in [audit.json](references/audit.json). The primary-source snapshots are retained for audit. Several sources remain explicitly cited as arXiv preprints; no publication venue or date was guessed for those entries.

OpenReview's browser challenge was not accepted as evidence. For MSDNet, the actual [ICLR 2018 conference entry](https://iclr.cc/virtual/2018/poster/278) verifies the published version. ViT is cited via its verified arXiv record rather than treating a challenge page as a verified conference record.

## Claims checked against prior work

- **Destructive overthinking is established prior work.** Kaya, Hong and Dumitras, ICML 2019, explicitly discuss correct intermediate predictions becoming incorrect. The manuscript credits that work and does not claim novelty for the early-save identity.
- **Multi-scale early exits are established.** The MSDNet reference is ICLR 2018. Our model is a variant; no official replication claim is made.
- **Learned budgeted routing is established.** EENet is discussed as learned scheduling under an inference budget. The logistic diagnostic here is not a competitive reproduction of that method.
- **Frozen-backbone exit augmentation is established.** PTEENet (verified 2025 preprint) is included, preventing an unsupported novelty claim for post-trained exit heads.
- **Confidence and patience rules are established.** The calibration paper and patience-based early-exit paper support distinct background statements; budget calibration is not described as probability calibration or risk control.
- **FLOPs differ from latency.** The ShuffleNetV2 reference supports the need for device-level measurement; our prefix proxy is clearly limited.
- **Oracle opportunity versus realizability is not a new distinction.** [Shihab et al., August 2026](https://arxiv.org/abs/2608.08265) separate oracle opportunity, signal-restricted opportunity, and learned-router gain in multi-LLM routing, with selection-valid inference. This directly overlaps the broad motivation and is cited in both the introduction and related work. Our narrower contribution concerns early-exit allocation, cost matching and source-optimal transfer selection; we do not claim their population guarantees.
- **Stochastic oracle-gap decomposition has recent prior work.** [Chen, July 2026](https://arxiv.org/abs/2607.03436) studies single-draw decoding noise and repeated sampling. Our fixed trained classifiers across seeds are a different stochastic object. The manuscript neither claims priority for questioning oracle gaps nor imports a noise decomposition without its assumptions.

## Contemporary paper with unresolved publication timing

The search surfaced Omar Dib, “When to stop: Learned routing and risk control for early exit networks,” DOI [10.1016/j.knosys.2026.116702](https://doi.org/10.1016/j.knosys.2026.116702). Crossref confirms the title and author but records an October 2026 publication date and no online-publication date, later than this audit. The publisher search excerpt was visible, but the paper's availability chronology could not be established. It is **not inserted as a verified already-published reference**, and no claim that our work predates it is made. Check the full publication record before submission. The manuscript already acknowledges that richer and sequentially trained routing methods are not evaluated.

## Novelty judgment

The defensible contribution is the combined empirical audit of solver discontinuities, realized-cost matching, and the range of target scores among source-optimal policies. Fractional allocation and linear programming are elementary tools here, not new general optimization methods. Neither repeated searching nor metadata verification proves priority or exhaustive coverage. The manuscript therefore avoids “first,” “universal ceiling,” “pure noise,” “unbiased debiasing,” and “Q1-ready” claims.

The source text, citations and numerical statements were also reviewed together after compilation. Reference metadata checks establish bibliographic identity; they are not a substitute for expert review of the manuscript's interpretation.
