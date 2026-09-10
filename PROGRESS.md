# Project progress — 2026-09-08

**Stage: complete first LaTeX manuscript and corrected CPU reanalysis.** See [paper/README.md](paper/README.md) and the [compiled manuscript](output/pdf/main.pdf). Authors are empty. No backbone training or HF publishing was performed; small logistic gates were fitted for the new routing analysis.

| Workstream | Status | Details |
|---|---|---|
| Study 1 CIFAR atlas | 15 architectures × 3 seeds complete; historical Q5 caveats retained | [Results](docs/cifar100/10_FINAL_RESULTS.md) |
| Study 1 ImageNet-100 | Pilot/method analysis complete; planned full atlas incomplete | [Findings](docs/imagenet100/26_IN100_FINDINGS.md) |
| Study 2 | Reanalysis complete; old ceiling/noise wording superseded | [Current interpretation](PAPER_CLAIM.md) |
| Study 3 | Joint exits and restricted gate complete; pruning confounded | [Findings](study3/04_FINDINGS.md) |
| Study 4 P0–P2 | Analysis artifacts retrieved at pinned HF revision | [Findings](study4/04_FINDINGS.md) |
| Study 4 P3 | **Complete: +7.74/+7.91 pt**, independently recomputed | [Validation](docs/evidence/hf_2026-09-07/study4_validation.json) |
| Documentation | Overview, results, Study 4 and recommendation updated | [Understanding](PROJECT_UNDERSTANDING.md) |
| Manuscript | Complete first draft, 16 pages, five figures, four tables, 23 references | [Source and evidence](paper/README.md) |

## Manuscript audit completed September 8

- Downloaded all 45 frozen-model test parquets and pinned cost tables; verified sample IDs and ordered labels across models.
- Replaced the deterministic tied-budget solver with exact fractional allocation; checked it against 30 independent linear programs. Median oracle improvement at 0.50 is **7.88 points**.
- Expanded the audit to all 90 ordered pairs and seven budgets. At 0.80, transfer is **−7.43 points** relative to confidence under a common cap, but **+14.20 points** at matched realized cost. The canonical transferred policy spends only **0.496** median normalized cost.
- Solved source-optimal transfer envelopes for all 90 pairs at 0.80: median target-accuracy width **25.78 points**. This is a policy-selection range, not an attainable router guarantee.
- Found that the historical gate fit and evaluation reuse the same test images. A new disjoint 4,000/2,000/4,000 fit/calibration/evaluation split gives **+0.175 points** for the transferred logistic gate at 0.80; its descriptive architecture interval includes zero.
- Verified all seven joint-control depth prediction counts. D-91 remains quarantined rather than claiming a generic-evaluation repair.
- Rechecked 23 bibliography entries, including relevant July/August 2026 oracle-gap preprints. The paper does not claim novelty for oracle opportunity versus realizability.
- Compiled the LaTeX, checked citation/label integrity, and rendered all pages for visual review. [Verification record](paper/VERIFICATION.json).

## Completed in this audit

- Inventoried 120 initial project files, including 43 Markdown files, 37 notebooks, source, tests, benchmarks and nonresearch binaries.
- Retrieved source CSVs and P6/P7 records from HF at immutable revisions; retained compact evidence and hashes.
- Verified both MSDNet runs at 240/240 epochs and recomputed headlines from 10,000 per-image predictions each.
- Extended the results generator for P3 and corrected baseline aggregation to common eligible cells, preserving source CSVs.
- Identified D-91: generic backbone evaluation and trained-exit results address different classifiers.
- Reframed the proposed paper around seed transfer and budgets, acknowledging overthinking as prior work.

## Verification completed

All 44 retained source hashes match the pinned HF evidence. Both P3 test-parquet
recomputations agree with the source CSV. The results generator reproduces 64
rows, including eight P3 rows, and rejects missing or duplicated MSDNet seeds.
All 48 Markdown files' local references resolve. Training and GPU evaluation
were not re-executed; D-91 is documented and remains open.

The continued audit also recomputed both P2 ImageNet results from their test
parquets: ResNet-50 has 739 early saves and ViT-S/16 691, out of 10,000 each,
confirming **+7.39/+6.91 pt** despite the separate generic-evaluation mismatch.

## Next actions

1. Review the complete manuscript and its [submission assessment](paper/SUBMISSION_ASSESSMENT.md).
2. Strengthen the study with a richer sequential router, complete runtime cost accounting, and independent external validation before pursuing a selective journal submission.
3. Repair joint-run generic final evaluation as a separate maintenance task; the manuscript uses independently verified depth heads.
4. Supply actual author/declaration information and select the final venue. No authorship, funding or journal acceptance is invented.

P3 does not need retraining to update these results. A richer router, official MSDNet replication and extra seeds are optional strengthening experiments, not completed work. The pruning claim remains unresolved.

Historical logs preserve what was believed at the time. Their old “next action” instructions are superseded by this page and their dated notes.

### Manuscript audit - 8 September 2026

Completed an independent numerical audit and a fresh CPU reproduction: 315 oracle LP comparisons, 630 transfer checks, 630 raw threshold checks, 85 input hashes, and all 10 analysis tables passed. Corrected rounding and methodological wording, and clarified Table 3 counts. The main findings are unchanged. Full review: [paper/AUDIT_REPORT.md](paper/AUDIT_REPORT.md).
