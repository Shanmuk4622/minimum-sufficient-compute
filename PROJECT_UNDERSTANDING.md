# Project understanding and current progress

Updated **2026-09-08**, after the repository inventory, direct Hugging Face audit, and manuscript reanalysis. This is the working knowledge document for the project. The complete first manuscript is [Oracle Headroom Is Policy-Dependent](paper/README.md).

## What changed while writing the paper

The earlier budget-dependent transfer interpretation was incomplete. Exact allocation across tied correctness groups improves the oracle by **7.88 points at budget 0.50**. At 0.80, the canonical transferred oracle is **7.43 points below confidence under a common cap**, but **14.20 points above at matched realized cost**; it spends only a median cost of **0.496**. Across source-optimal policies at that cap, target accuracy varies over a median **25.78-point** interval. Thus oracle transfer depends on policy choice and cost comparison, and is not a unique deployable ceiling.

The original learned-gate notebook reuses test images for fitting and evaluation, including its cross-seed arm. The manuscript replaces that evidence with a new disjoint router split (4,000 fitting / 2,000 calibration / 4,000 evaluation images), yielding **+0.175 points** for the transferred logistic gate at target 0.80. Its architecture-resampling interval includes zero. The underlying test set was already used in earlier project decisions, so this is not pristine external validation.

The paper's primary aggregation averages seed comparisons within each architecture, then takes the median across 15 architectures. These values intentionally differ from some older pooled-row medians. Its 23 references include recent 2026 oracle-diagnostic work; neither overthinking nor the opportunity/realizability distinction is claimed as new.

## What this project is trying to learn

The original question is whether an image's required computation is reproducible across random training seeds and transferable across architectures. Minimum Sufficient Compute (MSC) measures the smallest normalized cost at which a prediction agrees with the final prediction, exceeds a margin threshold, and stays sufficient at every larger tested budget. It is a stability-closed, final-decision-agreement quantity; it is not the same as the first exit that predicts the true label correctly.

Depth, resolution and simulated precision are separate axes. MSC masks cases whose final margin fails the threshold rather than treating all of them as identical hard examples. Seed reliability and correction for attenuation are central to interpreting cross-model agreement. A normalized FLOPs ratio is not measured latency, energy savings or a hardware-independent compute requirement.

The project evolved from a metric and distillation proposal into a more useful question: what do oracle routing measurements actually tell us about practical early-exit inference? Studies 2–4 use saved per-exit predictions to distinguish final-exit accuracy, any-correct-exit accuracy, cross-seed exit-policy transfer and restricted learned routing.

## What each study contributes

| Study | What was done | What I take from it |
|---|---|---|
| 1 — CIFAR | 15 architectures × 3 seeds, plus pilot and MSC-KD runs; three compute axes | A reusable atlas. Reliability varies by architecture; transfer survives architectural changes. PCA rejects the registered dominant-factor hypothesis, not a proof of exactly three independent latent factors. Q4's incomplete-battery figures were withdrawn. |
| 1 — ImageNet | Two-architecture pilot and 18-student method analysis on a custom 224px subset | Extends observed patterns, but does not complete the planned eight-architecture atlas. MSC-KD did not improve confidence routing at the reported point; its MSC-specific oracle gap was near zero. |
| 2 | CPU reanalysis of saved predictions and difficulty scores | Large same-seed/cross-seed oracle-policy gap; architecture/score-dependent reliability; softmax score instability on fitted training data. Neither all of the gap being noise nor unbiased debiasing is established. |
| 3 | Joint attached exits, a confidence/margin gate, and pruning | Excess persists under joint training. The old gate reuses test images; the manuscript replaces it with a disjoint experiment. Pruning is confounded and cannot establish the proposed downstream-harm mechanism. |
| 4 | Sample intervals, additional baselines, ImageNet joint exits, MSDNet variant | All planned phases have artifacts. The common-cap transfer advantage changes sign, but matched realized cost changes that interpretation. Excess survives the custom MSDNet variant in both seeds. |

**Study 1 figures that need care:** CIFAR partial results and older 13/14-architecture pair breakdowns coexist with 15-architecture summaries. Do not copy population counts without checking the originating CSV. ImageNet's B11 result does not automatically close CIFAR's O-21; they concern different students. The tiny MSC-specific B11 gap does not rule out other kinds of routing.

## Current progress

**The first LaTeX manuscript is complete and compiled.** No new backbone training or HF publishing was performed. Small CPU logistic gates were fitted in the new disjoint analysis. The historical study summaries below remain useful as provenance, while the September 8 results above and [paper data](paper/data/summary.json) control the manuscript interpretation.

Study 4's previous “not yet run” status was stale. Its P3 runs completed on 2026-09-01 and are published in `Shanmuk4622/msc-cifar100`:

| MSDNet variant | Seed 1 | Seed 2 |
|---|---|---|
| Epochs completed | 240/240 | 240/240 |
| Final-exit accuracy, recomputed from test predictions | 73.93% | 74.08% |
| Any-correct-exit oracle | 81.67% | 81.99% |
| Excess over final exit | **7.74 pt** | **7.91 pt** |
| Early-right/final-wrong examples | 774/10,000 | 791/10,000 |
| Recorded training hours, RTX 4000 Ada | 3.4554 | 3.4858 |

H5's unchanged threshold is met in **2/2 seeds**. Mean excess is **7.825 points**. The five-exit, three-scale, twenty-layer implementation differs from official MSDNet in bottlenecks, transitions and classifier heads. Report the variant explicitly; two seeds do not prove architecture independence.

P0 sample intervals remain 10.64 [10.00,11.28], 8.55 [7.98,9.10], and 9.15 [8.61,9.71] points. P2 gives +7.39/+6.91 points for ResNet-50/ViT-S/16. P1's cross-seed-policy advantage over confidence is +7.74/+7.29/+3.74 at budgets 0.40/0.50/0.60 and negative at 0.70–0.95. The observed sign transition is between 0.60 and 0.70. H6's all-budget negativity prediction is falsified.

The baseline aggregate now uses 46 shared eligible architecture/budget cells: confidence 58.10%, margin 58.38%, patience 55.62%. These are common-cell summaries under cost ≤ target + 0.01, not exact-cost matches or evidence that all three rules agree at every budget.

See [PROGRESS.md](PROGRESS.md) for the live action list and [Study 4 findings](study4/04_FINDINGS.md) for detailed evidence.

## An important new defect: D-91

MSDNet generic `metrics/final.json` reports 1.81%/1.44% accuracy, whereas the depth parquets reproduce 73.93%/74.08%. P6 ResNet/ViT generic final records similarly report 1.24%/1.56%, inconsistent with their joint-exit summaries.

The inspected source trains `MultiExitModel.heads` from `backbone.forward_features`, but `run_oracle` gives the bare backbone to `final_evaluation`. That separate backbone classifier does not participate in the joint-exit loss. The depth sweep uses the saved trained exit heads. This explains the discrepancy at source level; I did not reload checkpoints and execute the GPU model.

Use the verified depth-prediction figures for P3. Quarantine generic accuracy, calibration, confusion matrices and classifier-specific timing for joint runs until repaired. Audit their non-depth sweeps and post-hoc scores too. The P3 notebook's recipe guard reads keys absent from generic final.json; direct verification confirms its accuracy floor, but the original guard is not certified. The one-example difference between training-best accuracy and test-parquet accuracy remains explicitly recorded.

## How the repository works

- `src/msc_lib.py` is the operational library: data, model zoo, profiling, training, checkpoints, telemetry, HF synchronization, measurement and analysis.
- `msc_core.py` implements MSC, rank statistics, reliability correction, PCA and irreducibility. `msc_torch.py` holds reference model-side components; runtime counterparts also live in the main library.
- Five `build_notebooks*.py` generators produce 37 self-contained notebooks. The library is embedded, and bootstrap hashes help expose stale notebook copies. Changes belong in source/generators; notebook hand edits will be lost.
- `tools/` contains structural validators, known-answer canaries, notebook harnesses, throughput diagnostics and results generation. A passing structural check is not evidence that an unexecuted GPU path is correct.
- `benchmark/` documents measurements on an RTX 4000 Ada. The 6.7× channels-last regression is hardware/configuration specific and should not be generalized to T4.
- `docs/cifar100/`, `docs/imagenet100/`, and `study2/`–`study4/` contain protocols, results, risks and historical logs. Historical entries preserve incorrect earlier beliefs followed by corrections; live status must be distinguished from that record.

## Data and provenance

CIFAR-100 uses the standard 50,000 training / 10,000 test images. The custom ImageNet subset contains 129,395 images selected from the first 100 sorted WNIDs, with 119,395 training and 10,000 validation examples. Its 15,000-example `train_holdout` is sampled from training: it is **seen data**, not an independent holdout. CIFAR likewise uses a seen-training evaluation slice. Neither can silently serve as an independent test of a policy fitted on those same examples.

ImageNet's raw image count is about 2.6× CIFAR training size, and its training split about 2.4×; “40× data” is not an image-count comparison. The 224px versus 32px pixel-area ratio is 49×. Precision reduction is simulated, and the custom class selection prevents casual comparison with other ImageNet-100 benchmarks.

The audit retrieved public HF metadata and artifacts without credentials or writes. CIFAR revision: `a6356f6a8dee0be1c8bdbfa55e07924b62976da8`; ImageNet revision: `e3b461cf412dc46acfa4a482638dcde014ac0813`. Study 4 P6 ImageNet runs are stored in the **CIFAR-named repository**. Preserve run-level dataset identity rather than deriving it from repository names.

Compact source CSVs and run records, immutable URLs, byte counts and hashes are in [the evidence snapshot](docs/evidence/hf_2026-09-07/README.md). Both P3 test parquets were downloaded and recalculated; large data stays under ignored `msc_results/`. The result generator defaults to the pinned snapshot so the tables can be regenerated from a fresh checkout.

## Research claims that need discipline

1. `P(any correct exit) − P(final correct)` measures complementary predictions, not router impossibility. Destructive overthinking is already prior work.
2. A cross-seed policy using source-model correctness still uses labels. It is a diagnostic, not a deployable oracle correction or a proven bound on all learned policies.
3. The historical gate's 1.73% capture uses overlapping test images and is not held-out generalization evidence. The new disjoint gate remains restricted to exit-local confidence features; it does not test richer representations.
4. Ninety ordered pairs reuse 45 models, 15 architectures and the same examples. Uncertainty must respect those dependencies.
5. Sample bootstrap intervals are not seed intervals. One ImageNet joint seed per architecture cannot estimate training variation.
6. Saturation correlating with loss of score reliability is not proof of causation. The pruning design does not establish downstream harm.
7. A weak dominant PCA component does not prove an exact latent dimensionality, nor does transfer prove distillation improves routing.

## The manuscript now written

**Oracle Headroom Is Policy-Dependent: A Seed-Transfer Audit of Early-Exit Networks.** [Source and PDF](paper/README.md).

The manuscript centers exact budget allocation, cost matching, and the range of target scores among source-optimal policies. The atlas supplies breadth; joint training, ImageNet and the MSDNet variant are bounded complementarity controls. Pruning is excluded from the main empirical narrative.

The [reference audit](paper/REFERENCE_AUDIT.md) checks 23 references and credits both destructive overthinking and recent oracle-opportunity diagnostics. The paper makes no claim of priority or guaranteed publication. [PAPER_CLAIM.md](PAPER_CLAIM.md) records the current claim and preserves the superseded recommendation; [submission assessment](paper/SUBMISSION_ASSESSMENT.md) lists material remaining strengthening work.

## Future training notebook requirements

The user's current instructions take precedence over older offline-workstation instructions: deliver Kaggle-compatible `.ipynb` files, support dual T4, use `HF_TOKEN` from secrets and namespace `Shanmuk4622`, prefer Kaggle dataset sources, record complete progress, and sync on roughly 30-minute intervals, major completion and handled interruption with rate-limit-aware batching.

Existing code primarily resumes from **epoch-boundary** checkpoints containing optimizer/scheduler/scaler/RNG state. That is not exact interrupted-batch recovery. A future exact-step requirement needs sampler position, in-progress gradient accumulation and other necessary state to be saved and verified. It must be implemented and tested rather than promised from current checkpoint wording.

Abrupt machine loss cannot trigger an immediate network upload; only the last confirmed remote checkpoint survives it. Handled interrupts should flush promptly, subject to connectivity and service throttling. Treat 20GB persistent output and larger temporary scratch as user planning constraints to verify in the actual session; neither available capacity nor service quotas are guaranteed by this document. The older Study 3/4 `enable_hf=False` path does not meet periodic remote-save requirements unchanged.

No training notebook was requested or delivered in this documentation audit.

## Verification of this update

The source verifier passed all 44 retained HF file hashes and both P3 parquet
recomputations. Results regeneration is stable at 64 rows (eight for P3), and
missing/duplicated seed controls are rejected. All 48 Markdown files' local
references resolve. These checks validate the documentation update and reported
P3 arithmetic; they do not close D-91 or replace a GPU evaluation test.

The continued verification also covers both P2 ImageNet test parquets: 739/691
early saves out of 10,000, exactly reproducing +7.39/+6.91 points. All four P2/P3
raw-data checks are repeatable with `tools/verify_study4_evidence.py`; the
[P2 validation record](docs/evidence/hf_2026-09-07/study4_imagenet_validation.json)
retains the counts and source hashes.

## Review coverage and limits

The initial inventory contained **120 files**: **43 Markdown**, **31 Python** (including three ignored generated core copies), **37 notebooks**, seven other text/data files, and two binaries. All file bytes were read for inventory/hashes, all text was loaded, all notebook cells parsed and duplicated cells extracted for structural review. The document/state/claim review covered all Markdown files; source review followed definitions, interfaces, generators and the relevant training/measurement/reporting paths. This is not a claim that every source line was dynamically tested or every embedded library version is current.

The two binaries are a Python bytecode cache and `notebooks/Microsoft.Services.Store.winmd`, Windows metadata unrelated to the research. They were inventoried, not executed or removed. `.git` internals were excluded from the research-file census. Existing untracked user files were preserved.

[REPOSITORY_REVIEW.md](REPOSITORY_REVIEW.md) lists every initial file with its role and initial hash. Existing historical manuscripts were not overwritten. The manuscript audit subsequently recalculated all 45 frozen-model depth tables and all seven joint controls, and ran new CPU routing and allocation analyses. No backbone checkpoint inference was rerun.
