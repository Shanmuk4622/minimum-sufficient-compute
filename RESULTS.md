# Results — every headline number, generated from the artifacts

**Do not hand-edit.** Regenerate with `python tools/build_results.py`.
Machine-readable copy: [`RESULTS.csv`](RESULTS.csv).

**September 8 manuscript extension:** these are archived study summaries, not the new paper-analysis tables.
See [`paper/README.md`](paper/README.md) for exact oracle allocation, realized-cost matching,
source-optimal policy envelopes, and the disjoint router experiment. Historical gate capture
reused test images for fitting and evaluation and is not held-out generalization evidence.

Source CSVs are on HuggingFace at
[`Shanmuk4622/msc-cifar100`](https://huggingface.co/datasets/Shanmuk4622/msc-cifar100)
under `analysis/`. The default input is the pinned 2026-09-07 snapshot;
pass `--results-root` explicitly to use another analysis tree.
Provenance: [`manifest.json`](docs/evidence/hf_2026-09-07/manifest.json).

Differences are aggregated per row; subtracting separately aggregated levels need not reproduce them.
Study 2 has 90 ordered seed pairs from 45 models, not 90 independent training runs.
Historical CSV fields `oracle_cross` / `honest_headroom` describe seed-transfer diagnostics,
not proven upper bounds on deployable routing. See [`PAPER_CLAIM.md`](PAPER_CLAIM.md).
MSDNet values use the trained final exit; generic `metrics/final.json` is quarantined
because it evaluates a different classifier. See [`Study 4 findings`](study4/04_FINDINGS.md).

## Study 2 — oracle ceiling

| metric | scope | value | source |
|---|---|---|---|
| confidence baseline | CIFAR-100, 90 seed pairs, rho=0.80 | **62.39 %** | `s2_true_oracle.csv` |
| full compute | CIFAR-100, 90 seed pairs, rho=0.80 | **71.21 %** | `s2_true_oracle.csv` |
| oracle, in-seed | CIFAR-100, 90 seed pairs, rho=0.80 | **78.3 %** | `s2_true_oracle.csv` |
| oracle, cross-seed | CIFAR-100, 90 seed pairs, rho=0.80 | **54.5 %** | `s2_true_oracle.csv` |
| in-seed - baseline | CIFAR-100, 90 seed pairs, rho=0.80 | **12.2 pt** | `s2_true_oracle.csv` |
| cross-seed - baseline | CIFAR-100, 90 seed pairs, rho=0.80 | **-7.9 pt** | `s2_true_oracle.csv` |
| optimism bias | CIFAR-100, 90 seed pairs, rho=0.80 | **22.41 pt** | `s2_true_oracle.csv` |
| early-right/final-wrong pool | CIFAR-100, 90 seed pairs, rho=0.80 | **6.86 pt** | `s2_true_oracle.csv` |
| oracle ABOVE own full-compute accuracy | 90/90 ordered seed-pair rows (45 trained models) | **6.86 pt** | `s2_true_oracle.csv` |

## Study 2 — reliability atlas

| metric | scope | value | source |
|---|---|---|---|
| rho_seed range across the grid | 15 archs x 5 scores | **0.667 rho** | `s2_reliability_grid.csv` |
| rho_seed minimum | mixer_nano / entropy | **0.207 rho** | `s2_reliability_grid.csv` |
| rho_seed maximum | mobilenetv2 / ce_loss | **0.874 rho** | `s2_reliability_grid.csv` |

## Study 2 — memorisation collapse

| metric | scope | value | source |
|---|---|---|---|
| Spearman(softmax saturation, rho_seed drop) | 15 architectures | **0.832 rho** | `s2_memorisation.csv` |
| Spearman(train accuracy, rho_seed drop) | 15 architectures | **0.746 rho** | `s2_memorisation.csv` |
| Spearman(TEST accuracy (control), rho_seed drop) | 15 architectures | **-0.114 rho** | `s2_memorisation.csv` |
| largest rho_seed drop, test -> train_holdout | convnext_femto | **0.558 rho** | `s2_memorisation.csv` |

## Study 3 — Q1 joint exits

| metric | scope | value | source |
|---|---|---|---|
| excess, resnet20 | frozen | **6.69 pt** | `s3_q1_comparison.csv` |
| excess, resnet20 | JOINT | **10.64 pt** | `s3_q1_comparison.csv` |
| excess, resnet32x4 | frozen | **6.42 pt** | `s3_q1_comparison.csv` |
| excess, resnet32x4 | JOINT | **8.55 pt** | `s3_q1_comparison.csv` |
| excess, vgg8 | frozen | **7.95 pt** | `s3_q1_comparison.csv` |
| excess, vgg8 | JOINT | **9.15 pt** | `s3_q1_comparison.csv` |
| H1: excess >= 2.0 pt under joint training | 3/3 architectures | **9.15 pt** | `s3_q1_comparison.csv` |
| change frozen -> joint (raw median) | 3 architectures | **2.13 pt** | `s3_q1_comparison.csv` |

## Study 3 — Q2 learned router

| metric | scope | value | source |
|---|---|---|---|
| capture fraction, in-seed | 3 architectures, rho=0.80 | **2.36 %** | `s3_router_capture.csv` |
| capture fraction, cross-seed | 3 architectures, rho=0.80 | **1.73 %** | `s3_router_capture.csv` |
| oracle gap available to be captured | median over architectures | **11.62 pt** | `s3_router_capture.csv` |

## Study 3 — Q3 pruning

| metric | scope | value | source |
|---|---|---|---|
| target accuracy, rand | keep 30% | **19.16 %** | `s3_pruning.csv` |
| target accuracy, sat | keep 30% | **16.46 %** | `s3_pruning.csv` |
| target accuracy, uns | keep 30% | **7.92 %** | `s3_pruning.csv` |
| target accuracy, rand | keep 50% | **25.58 %** | `s3_pruning.csv` |
| target accuracy, sat | keep 50% | **25.05 %** | `s3_pruning.csv` |
| target accuracy, uns | keep 50% | **14.76 %** | `s3_pruning.csv` |
| target accuracy, full | keep 100% | **70.24 %** | `s3_pruning.csv` |

## Study 4 — P0 bootstrap CI

| metric | scope | value | source |
|---|---|---|---|
| excess, resnet20 | 95% CI over 10,000 TEST SAMPLES (not seeds) | **10.64  [10.00, 11.28] pt** | `s4_bootstrap.csv` |
| excess, resnet32x4 | 95% CI over 10,000 TEST SAMPLES (not seeds) | **8.55  [7.98, 9.10] pt** | `s4_bootstrap.csv` |
| excess, vgg8 | 95% CI over 10,000 TEST SAMPLES (not seeds) | **9.15  [8.61, 9.71] pt** | `s4_bootstrap.csv` |
| intervals excluding zero | 3 joint runs | **3 of 3** | `s4_bootstrap.csv` |

## Study 4 — P2 ImageNet-100 @224px

| metric | scope | value | source |
|---|---|---|---|
| excess, resnet50 | 1 seed; per-run identity | **7.39 pt** | `s4_imagenet_excess.csv` |
| full-compute accuracy, resnet50 | 1 seed | **81.58 %** | `s4_imagenet_excess.csv` |
| excess, vit_small_p16 | 1 seed; per-run identity | **6.91 pt** | `s4_imagenet_excess.csv` |
| full-compute accuracy, vit_small_p16 | 1 seed | **63.23 %** | `s4_imagenet_excess.csv` |
| H4: excess >= 2.0 pt | 2 of 2 archs | **6.91 pt (min)** | `s4_imagenet_excess.csv` |
| H4b: the TRANSFORMER alone | vit_small_p16 | **6.91 pt** | `s4_imagenet_excess.csv` |

## Study 4 — P1 honest headroom vs budget

| metric | scope | value | source |
|---|---|---|---|
| cross-seed oracle - confidence, rho=0.40 | median over 15 CIFAR architectures | **7.74 pt** | `s4_baselines.csv` |
| cross-seed oracle - confidence, rho=0.50 | median over 15 CIFAR architectures | **7.29 pt** | `s4_baselines.csv` |
| cross-seed oracle - confidence, rho=0.60 | median over 15 CIFAR architectures | **3.74 pt** | `s4_baselines.csv` |
| cross-seed oracle - confidence, rho=0.70 | median over 15 CIFAR architectures | **-3.05 pt** | `s4_baselines.csv` |
| cross-seed oracle - confidence, rho=0.80 | median over 15 CIFAR architectures | **-8.3 pt** | `s4_baselines.csv` |
| cross-seed oracle - confidence, rho=0.90 | median over 15 CIFAR architectures | **-13.13 pt** | `s4_baselines.csv` |
| cross-seed oracle - confidence, rho=0.95 | median over 15 CIFAR architectures | **-14.98 pt** | `s4_baselines.csv` |
| budgets with POSITIVE honest headroom | confidence baseline | **[0.4, 0.5, 0.6] rho** | `s4_baselines.csv` |

## Study 4 — P1 baseline independence

| metric | scope | value | source |
|---|---|---|---|
| max \|confidence - margin\| headroom gap | difference of architecture medians across 7 target budgets | **1.78 pt** | `s4_baselines.csv` |

## Study 4 — P1 baseline strength

| metric | scope | value | source |
|---|---|---|---|
| confidence, common eligible cells | median over 46 shared arch/budget cells; cost <= target + 0.01 (not exact cost matching) | **58.1 %** | `s4_baselines.csv` |
| margin, common eligible cells | median over 46 shared arch/budget cells; cost <= target + 0.01 (not exact cost matching) | **58.38 %** | `s4_baselines.csv` |
| patience, common eligible cells | median over 46 shared arch/budget cells; cost <= target + 0.01 (not exact cost matching) | **55.62 %** | `s4_baselines.csv` |

## Study 4 — P3 MSDNet variant

| metric | scope | value | source |
|---|---|---|---|
| final-exit accuracy | seed 1; 5 joint exits; 10,000 test samples | **73.93 %** | `s4_msdnet.csv` |
| any-correct-exit oracle | seed 1; 5 joint exits; 10,000 test samples | **81.67 %** | `s4_msdnet.csv` |
| oracle excess | seed 1; 5 joint exits; 10,000 test samples | **7.74 pt** | `s4_msdnet.csv` |
| final-exit accuracy | seed 2; 5 joint exits; 10,000 test samples | **74.08 %** | `s4_msdnet.csv` |
| any-correct-exit oracle | seed 2; 5 joint exits; 10,000 test samples | **81.99 %** | `s4_msdnet.csv` |
| oracle excess | seed 2; 5 joint exits; 10,000 test samples | **7.91 pt** | `s4_msdnet.csv` |
| H5: excess >= 2.0 pt in both seeds | documented variant; not an official MSDNet replication | **2 of 2** | `s4_msdnet.csv` |
| mean excess | 2 seeds; descriptive mean, not a seed confidence interval | **7.825 pt** | `s4_msdnet.csv` |
