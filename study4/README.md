# Study 4 — experiments complete, verified 2026-09-07

**P3 was already trained and published.** Both MSDNet-variant seeds completed 240 epochs on 2026-09-01. Direct recalculation from their HF test parquets confirms **+7.74 and +7.91 points** above final-exit accuracy. H5 is supported for this variant in both seeds.

| Phase | State | Result |
|---|---|---|
| P0 — intervals / figure artifacts | Complete | Three attached-joint sample intervals exclude zero |
| P1 — baseline comparisons | Complete | H6's negativity-at-all-budgets prediction is falsified; positive transfer advantage at 0.40–0.60 |
| P2 — ImageNet-100 / transformer | Complete | +7.39/+6.91 pt; H4/H4b supported |
| P3 — MSDNet variant | Complete | +7.74/+7.91 pt; H5 supported in 2/2 seeds |

Read [04_FINDINGS.md](04_FINDINGS.md) for immutable sources, all numbers, scope, and the **generic final-evaluation mismatch (D-91)**. That mismatch does not change the independently recomputed depth-oracle figures, but generic metrics are not ready for citation as final-exit metrics.

The next action is the evaluation and paper-readiness audit in [PAPER_CLAIM.md](../PAPER_CLAIM.md), not another P3 training run. Neither “unreachable by any router” nor “architecture-independent” follows from these experiments.

## Files

| File | Purpose |
|---|---|
| [01_PROTOCOL.md](01_PROTOCOL.md) | Original predictions with a dated outcome note |
| [02_RISKS.md](02_RISKS.md) | Risk register and unresolved issues |
| [03_LOG.md](03_LOG.md) | Current status and historical record |
| [04_FINDINGS.md](04_FINDINGS.md) | Verified results and interpretation |
| [../PROGRESS.md](../PROGRESS.md) | Repository-wide progress |

## Runtime scope

Existing Study 4 notebooks target an offline local workstation: NB0 figures, NB1 baselines, NB2 ImageNet, NB4 MSDNet, then NB3 publishing. They are generated; edit their generator when changing them. This audit did not rebuild training notebooks.

Future training notebooks must follow the user's current Kaggle dual-T4, HF_TOKEN, bounded-storage and periodic-save requirements. The older offline workflow does not itself meet those requirements. See [PROJECT_UNDERSTANDING.md](../PROJECT_UNDERSTANDING.md).
