# Manuscript audit — 8 September 2026

## Verdict

The manuscript is a complete, reviewable research draft. This audit found and corrected presentation and precision issues; it did not find a discrepancy in the main numerical findings. The evidence supports an empirical audit of oracle evaluation, not a new state-of-the-art router or a general impossibility result. No audit can guarantee the absence of every error, and readiness for a selective Q1 journal has not been established.

## Corrections made

- Standardized decimal rounding in generated tables. The matched-cost advantage is 14.195 percentage points before display rounding, hence **14.20**, rather than 14.19. The upper architecture-mean envelope width is displayed as **31.74**, rather than 31.73. Full-precision data remain unchanged.
- Corrected the maximum held-out cost overspend from 0.01673 to **0.01672** when rounded to five decimal places (unrounded value approximately 0.0167248).
- Split the ambiguous positive-count column into separate common-cap and matched-cost counts, each out of 15 architectures.
- Clarified that transferring a policy removes direct optimization against target correctness, not all agreement with it; stated the common-budget condition for the oracle upper bound; aligned threshold wording with the implemented inclusive comparison; excluded empty groups from the appendix division.
- Identified the cost proxy in the abstract and made explicit that the transferred logistic gate's descriptive interval includes zero.

## Verification completed

| Check | Result |
|---|---|
| Immutable input hashes | All 85 matched |
| Independent grouped linear programs | All 315 real-model/budget oracle values agreed; maximum accuracy discrepancy below 9 × 10⁻¹⁶ |
| Independently reconstructed full transferred allocations | All 630 accuracy/cost rows passed |
| Raw held-out confidence and margin rules | All 630 rows passed |
| Fresh CPU rerun, including logistic-gate fitting | All 10 analysis tables reproduced within absolute/relative tolerance 10⁻¹⁰ |
| Existing manuscript verification | All 49 checks passed, including split integrity, feasibility, seven raw joint-control counts, citation resolution, and reference checks |
| References | All 23 entries cited and resolved; 22 titles fetched again from primary metadata. The CIFAR technical-report title page was checked separately. Publication metadata and claim relevance are documented in REFERENCE_AUDIT.md; title matching alone is not claim validation. |
| PDF | Recompiled successfully; all 16 pages rendered and visually inspected, with the revised results table checked at full page size. No unresolved citations, text outside page bounds, or LaTeX box warnings. |

Machine-readable evidence is in INDEPENDENT_AUDIT.json, REPRODUCTION_AUDIT.json, VERIFICATION.json, and PDF_CHECK.json. The independent numerical audit does not import the original oracle or router implementation. The reproduction rerun does use the original analysis implementation and therefore serves a different purpose.

## Scientific limitations that remain

The logistic gate is a limited baseline; its small gain does not establish that stronger routers cannot learn useful routing. Router fitting, calibration, and evaluation images are disjoint, but earlier project decisions used the same underlying test dataset. Architecture-resampling intervals are descriptive for this fixed atlas. The cost proxy omits cumulative previous-head and router overhead and is not measured latency. Joint controls have limited seed coverage; the ImageNet subset is custom, and the multi-scale model is a documented variant.

The closest cited work already distinguishes oracle opportunity from realizability. The paper's defensible contribution is the combined empirical evidence on tied oracle allocation, cost comparisons, and source-optimal policy sensitivity. Strengthening that contribution for a selective journal requires stronger router baselines, external evaluation, and complete measured costs. See SUBMISSION_ASSESSMENT.md. Author and journal-specific declarations remain intentionally unfinished pending real author information and venue selection.
