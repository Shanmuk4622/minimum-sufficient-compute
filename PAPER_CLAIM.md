# Current paper claim — 2026-09-08

**The manuscript is now written:** [Oracle Headroom Is Policy-Dependent: A Seed-Transfer Audit of Early-Exit Networks](paper/README.md).

Its contribution is an empirical audit of **exact oracle allocation, realized-cost matching, and selection sensitivity among source-optimal policies**. The main evidence is new post-hoc CPU analysis on 45 models, not the old sign-reversal or overlapping-gate result. At budget 0.80, the same canonical transferred policy is −7.43 points below confidence under a common cap and +14.20 points above at matched realized cost. Its source-optimal target-accuracy envelope has a median width of 25.78 points. The corrected disjoint transferred logistic gate gains only 0.175 points, with a descriptive interval including zero.

The general oracle-opportunity/realizability distinction has direct 2026 prior work, now cited. No claim of priority, pure-noise decomposition, router impossibility, or Q1 acceptance is made. See the [reference audit](paper/REFERENCE_AUDIT.md) and [submission assessment](paper/SUBMISSION_ASSESSMENT.md).

## Historical recommendation — September 7

The following records the recommendation before solver, cost and gate-split checks. It is superseded by the manuscript where those analyses differ.

**Working title: _From Oracle Accuracy to Usable Compute Savings: A Seed-Transfer Audit of Early-Exit Networks_.**

The strongest coherent paper combines Studies 2–4, with Study 1 providing the atlas and infrastructure. It is an empirical evaluation paper. This is a recommendation; the manuscript will be written later. See [RESULTS.md](RESULTS.md) and [Study 4 findings](study4/04_FINDINGS.md).

## The question

How much of a label-informed early-exit oracle's apparent advantage transfers between training seeds, and how does that transfer compare with practical exit rules as the compute budget changes?

## Evidence available

| Evidence | Number | Defensible use |
|---|---|---|
| Frozen CIFAR atlas | 15 architectures × 3 seeds; 90 ordered pairs from 45 models | Breadth within a specified benchmark and recipe collection |
| Any-correct-exit advantage over final exit | median +6.86 pt | Complementarity; an exact set identity |
| Same-seed versus cross-seed oracle-policy accuracy | median paired difference +22.41 pt at 0.80 | Seed-transfer gap, not automatically pure noise or statistical bias |
| Joint attached exits | +10.64 resnet20, +8.55 resnet32x4, +9.15 vgg8 | Effect survives joint training in three one-seed comparisons |
| Confidence/margin learned gate | median cross-seed capture 1.73% at 0.80 | Result for this restricted gate, not an impossibility bound |
| Budget sweep | +7.74/+7.29/+3.74 pt at 0.40/0.50/0.60; negative at 0.70–0.95 | Transfer advantage depends on budget |
| Custom ImageNet-100 joint exits | +7.39 resnet50, +6.91 ViT-S/16 | Replication at 224px, one seed each |
| MSDNet variant | +7.74/+7.91 pt, seeds 1/2; mean 7.825 | H5 supported for the documented variant |

Numbers are medians of the stated per-row quantities unless described otherwise. Separately aggregated medians need not subtract. Ordered seed pairs share models and examples: these are not 90 independent experiments.

## Correcting the old thesis

The previous version claimed that an oracle above final-layer accuracy cannot be reached by any router, while later warning against the same claim. **That impossibility claim is unsupported.** An early classifier may be right when the final one is wrong; a router that identifies those cases could beat final-layer accuracy.

The identity `P(any correct exit) − P(final correct)` equals the early-save probability. It establishes complementarity. It neither invalidates a label-informed oracle nor proves those cases have no learnable signal. The cross-seed policy still uses true test labels through source-seed correctness. It is not deployable and is not established as an unbiased instrument. Use **seed-transfer gap**, retaining historical CSV names for reproducibility.

A negative cross-seed-policy-minus-confidence result does not prove there is no attainable headroom. A positive result at tight budgets does not establish that a trained router can capture it. The sign transition is bracketed by 0.60 and 0.70, not measured at 0.65. The baseline agreement within 1.78 points concerns confidence and margin; patience misses some budgets.

## Prior work and novelty

Correct intermediate predictions becoming wrong at the final layer were already studied as **destructive overthinking** by [Kaya, Hong and Dumitras, ICML 2019](https://proceedings.mlr.press/v97/kaya19a.html). The early-save identity and existence of that behavior cannot be our novelty claim.

[Huang et al., MSDNet, ICLR 2018](https://arxiv.org/abs/1703.09844) is the architecture reference. Our variant differs in bottlenecks, transitions and heads. Its result does not establish architecture independence.

**Candidate contribution:** a reproducible comparison of same-seed oracle behavior, seed-transfer policies, restricted learned routing, and budget-dependent baseline gaps across frozen, joint and multi-scale regimes. This is proposed positioning, not a verified claim of being first. A dedicated citation/novelty audit remains necessary, including recent learned-routing work. Distinguish correctness oracles from final-prediction-agreement oracles.

## Suggested paper structure

1. Define the any-correct-exit oracle, budget-constrained oracle policy, seed-transfer evaluation and deployable sequential rules.
2. Describe datasets, exact variants, seeds, joint/frozen recipes, calibration splits, achieved costs and aggregation.
3. Quantify complementarity across the frozen atlas, joint controls, ImageNet and MSDNet variant; connect it to overthinking.
4. Present seed transfer versus compute budget as the principal figure.
5. Report what the restricted learned gate captures, with its feature and budget limits.
6. Explain uncertainty, shared-seed dependence, variant limitations and reproducibility.

Use three main visuals: the budget curve; paired frozen/joint excess with sample intervals; and a compact ImageNet/MSDNet replication table. Keep the MSC axis atlas as background or supplementary material. Pruning answers a separate question.

## Work before submission

| Priority | Work | Why |
|---|---|---|
| Required | Repair joint-run generic final evaluation and verify affected artifacts | D-91: generic final.json evaluates a different classifier; this alone does not require retraining |
| Required | Audit sample alignment, achieved oracle/baseline cost, sequential features and calibration/test separation | Establish fair budget and information access |
| Required | Replace old all-budget/no-router/noise-only language | Those inferences exceed the evidence |
| Required | Complete literature and novelty audit | Overthinking is prior work; novelty must rest on the evaluation contribution |
| Required | Uncertainty over the correct units | Sample bootstraps do not estimate seed variation; ordered pairs are dependent |
| Required | Rebuild the main figure from s4_baselines.csv | P0's older score-routing curve answers a different question |
| Optional | Stronger feature-based gate across budgets | Tests accessibility of the gap to a richer policy |
| Optional | Official MSDNet configuration and more seeds | Reduces variant and seed-scope limitations |

**P3 is complete.** Its recorded training cost was 6.9412 hours, already spent. Do not request another run just because an old page says “built.” Completion is not a promise of acceptance or journal ranking. Choose a venue after the claim and novelty audit; the earlier “Q1-ready” guarantees are withdrawn.

## Other paper directions

The MSC atlas remains a separate measurement-paper candidate, represented by the [historical Study 1 draft](PAPER.md). Its PCA result rejects the registered one-factor threshold; it does not prove exactly three independent latent dimensions. Family/accuracy confounding and disattenuation assumptions require explicit treatment.

Softmax reliability on fitted training data is another candidate. Its association with saturation is strong (+0.832 across architectures), but correlation does not establish causation. Study 3 pruning was confounded and does not establish downstream harm. Keep that claim separate until a controlled follow-up is designed.
