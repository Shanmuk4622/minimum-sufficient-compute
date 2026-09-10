# Study 4 — verified findings

> **September 8 extension:** the [manuscript audit](../paper/README.md) uses all six seed directions per architecture, an exact tied-budget oracle, and matched realized costs. The older common-cap sign reversal below does not survive that cost-matched comparison. The MSDNet and ImageNet early-save counts remain unchanged. The new policy-envelope and disjoint-router experiments are post hoc, not original registered Study 4 outcomes.

Verified directly from Hugging Face on **2026-09-07**. P0–P3 analysis artifacts
are present. The two P3 runs completed on **2026-09-01**, not on the audit date.
Training is complete; publication readiness still requires the checks below.

## Evidence and population

The source is dataset repository `Shanmuk4622/msc-cifar100`, revision
`a6356f6a8dee0be1c8bdbfa55e07924b62976da8`. This repository also holds Study 4's
ImageNet-100 joint runs (`p6-*`); do not infer their absence from the separate
`msc-imagenet100` repository. The latter was independently inventoried at
`e3b461cf412dc46acfa4a482638dcde014ac0813`.

The [source manifest](../docs/evidence/hf_2026-09-07/manifest.json) records immutable
URLs, byte counts, and SHA-256 hashes. Compact CSVs and run records are retained
in [the evidence snapshot](../docs/evidence/hf_2026-09-07/README.md).
The [P3 validation record](../docs/evidence/hf_2026-09-07/study4_validation.json)
records a fresh calculation from both full test parquets, not just the summary CSV.

## P3 — H5 supported for the documented MSDNet variant

| Seed | Test samples | Exits | Final-exit accuracy | Any-correct-exit oracle | Excess | Early saves |
|---|---|---|---|---|---|---|
| 1 | 10,000 | 5 | 73.93% | 81.67% | **7.74 pt** | 774 |
| 2 | 10,000 | 5 | 74.08% | 81.99% | **7.91 pt** | 791 |

Both seeds satisfy the unchanged H5 threshold of at least 2.0 points. The mean
excess is **7.825 points**. The validation checked unique sample IDs, sample and
exit counts, all three CSV statistics, and the exact equality between the excess
count and the early-right/final-wrong count.

Each run completed 240/240 epochs. Recorded training time is 3.4554 and 3.4858
hours, **6.9412 hours total on one RTX 4000 Ada**. This excludes subsequent
measurement and publishing; it is not a dual-T4 runtime estimate. Recorded full
FLOPs are 409,372,928 (0.4094 GFLOPs), superseding the planning estimate of 0.24.

The variant has 3 scales, 20 dense layers, base width 16, growth 6, and exits at
layers 4/8/12/16/20 on the coarsest scale. It omits bottleneck convolutions and
channel-reduction transitions and uses the project's linear exit classifiers.
It is **not an official MSDNet replication**. Its two seeds broaden the observed
effect beyond attached-exit backbones; they do not prove architecture independence.
The 55% recipe floor is cleared by the final-exit predictions, but that is weaker
than matching the original paper's architecture and recipe.

## P0–P2 — results retained, scope clarified

| Phase | Result | Interpretation |
|---|---|---|
| P0 | resnet20 10.64 [10.00, 11.28]; resnet32x4 8.55 [7.98, 9.10]; vgg8 9.15 [8.61, 9.71] pt | 95% bootstrap intervals over test samples, not training seeds |
| P1 | cross-seed policy minus confidence: +7.74, +7.29, +3.74, −3.05, −8.30, −13.13, −14.98 pt | Budgets 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95; medians over 15 architectures |
| P2 | resnet50 +7.39 pt; vit_small_p16 +6.91 pt | H4/H4b supported on the custom ImageNet-100 subset, 224px, one seed each |

P2 was also independently recomputed from both full test parquets during this
audit. ResNet-50 has **8,158 final-correct / 8,897 any-exit-correct / 739 early-save**
examples; ViT-S/16 has **6,323 / 7,014 / 691**, each out of 10,000. Both completed
100/100 epochs. The source CSV values match exactly. See the
[P2 validation record](../docs/evidence/hf_2026-09-07/study4_imagenet_validation.json).

The measured sign transition is **between 0.60 and 0.70**. Approximately 0.65 is
an interpolation, not a tested operating point. Confidence and margin differ by
at most 1.78 points in the aggregated headroom curve. Patience cannot match every
budget, so the agreement claim applies to **two rules**, not three.

**H6 as registered is falsified:** it required negativity everywhere. The
baseline-similarity observation is a useful partial result, not a replacement
registered hypothesis. Study 2's difficulty-score sweep and Study 4's cross-seed
per-exit policy sweep are different estimands. Their populations also differ:
Study 2 uses 90 ordered pairs from 45 models; P1 selects one seed direction per
architecture. Their −7.90/−8.30 point agreement at 0.80 is approximate consistency,
not an independent replication on new data.

The results generator previously pooled different eligible populations when
ranking baselines. The corrected summary uses **46 common architecture/budget
cells**: confidence 58.10%, margin 58.38%, patience 55.62%. Eligibility means
achieved cost ≤ target + 0.01, not exact matched cost. These replace the old
58.03/58.18/55.62 prose figures for this explicitly defined aggregation. The
underlying `s4_baselines.csv` and the budget-specific headroom curve are unchanged.

## D-91 — generic final evaluation addresses a different classifier

The archived `metrics/final.json` reports **1.81% / 1.44%** top-1 for the two P3
seeds, incompatible with **73.93% / 74.08%** from `pred_d5`. Training summaries
record best accuracies **73.94% / 74.09%**, a separate evaluation differing by
one test example per seed. Do not silently substitute or round these together.

Source inspection explains the large discrepancy: joint training uses
`MultiExitModel.heads` over `backbone.forward_features`, while `run_oracle`
passes the bare backbone to `final_evaluation`. The backbone's separate classifier
does not participate in that joint-exit loss. The test depth sweep, in contrast,
uses the loaded multi-exit heads. This is a source-supported diagnosis; no
checkpoint was re-executed in this audit.

**Disposition:** retain the reproducible P3 depth-oracle result. Quarantine generic
final accuracy, calibration, confusion matrices, and classifier-specific inference
timing as evidence about the trained final exit. Resolution/precision sweeps and
post-hoc difficulty scores on joint runs may also use the bare classifier and
require a targeted audit. P6 generic final records also show **1.24% for ResNet-50
and 1.56% for ViT-S/16**, while training summaries show 81.58%/63.23%. The same
code path affects other joint runs, so inspect P4/P6 artifacts before reusing
their generic evaluation fields.

The notebook's recipe check asks for `best_accuracy` or `accuracy`, whereas the
generic evaluation stores `top1_accuracy`; consequently that check can see no
usable accuracy. The direct parquet check here supplies evidence of the floor,
but does not retroactively certify that notebook guard.

Repairing evaluation and regenerating its affected artifacts is a **follow-up**;
this documentation audit does not change training code or overwrite HF artifacts.

## What the identity does and does not establish

Let C_k mean that exit k predicts the true label. Then

`P(any C_k) − P(C_K) = P(any C_k and not C_K)`.

That is complementarity / destructive overthinking. It does **not** show that
the oracle is invalid or that a deployable router cannot beat the final exit.
The cross-seed policy remains label-informed through the source model's test
correctness. It is a transfer diagnostic, not a deployable policy or an unbiased
estimate of every router's attainable accuracy. The learned gate's 1.73% capture
is specific to its features, training setup, and budget 0.80.

## Next work

1. Repair and verify the joint-run evaluation path before citing its generic metrics.
2. Audit routing costs, row alignment, and validation/test separation for the final paper.
3. Rebuild a figure from **s4_baselines.csv** for the budget-dependent claim; the older
   P0 score-routing figure answers a different question.
4. Position against prior overthinking and early-exit work; see
   [the paper recommendation](../PAPER_CLAIM.md).

No new P3 training is needed to update these results.
