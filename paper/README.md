# Oracle Headroom Is Policy-Dependent

**Complete first research manuscript, 2026-09-08.** Authors are intentionally empty. The manuscript is an empirical evaluation paper, with a mathematical allocation construction, five vector figures, four tables, an evidence appendix, and 23 verified references. It is not submitted to a journal.

- [LaTeX manuscript](main.tex)
- [Bibliography](bibliography.bib)
- [Compiled manuscript](../output/pdf/main.pdf)
- [Overleaf ZIP](../output/oracle_headroom_overleaf.zip)
- [Analysis and reproducibility ZIP](../output/oracle_headroom_reproducibility.zip)
- [Numerical summary](data/summary.json)
- [Reference audit](REFERENCE_AUDIT.md)
- [Verification record](VERIFICATION.json)
- [Submission assessment](SUBMISSION_ASSESSMENT.md)

## Central contribution

The earlier budget-dependent transfer narrative changed after checking the actual solver and resource use. The manuscript now demonstrates three distinct sensitivities:

1. Exact allocation across a tied group improves the median same-seed oracle by **7.88 percentage points at budget 0.50**.
2. At budget 0.80, the canonical source policy's median transfer advantage is **−7.43 points under a common cap**, but **+14.20 points at matched realized cost**. It spends a median cost of only **0.496**.
3. Source-optimal policies under that cap permit a median target-accuracy range of **25.78 points**. This is a policy-selection range, not a confidence interval or achievable router performance.

A new disjoint 4,000/2,000/4,000-image router split gives a **+0.175-point** median transferred logistic-gate gain at target 0.80. The old overlapping test-image gate result is not used as generalization evidence.

All primary aggregation averages seed comparisons within architecture before taking the median over 15 architectures. The 90 ordered seed pairs share 45 models and the same images. Original HF files are preserved and have not been uploaded or changed.

## Compile

Upload `main.tex`, `bibliography.bib`, the two `*_rows.tex` files, and `figures/` to Overleaf. Select `main.tex` as the main document; pdfLaTeX or XeLaTeX with BibTeX is suitable. Authors remain empty in `\author{}`.

With a local LaTeX installation, run from this directory:

```text
latexmk -pdf main.tex
```

The delivered PDF was compiled using Tectonic 0.17.0. From the repository root:

```text
tectonic --outdir output/pdf paper/main.tex
```

On this workspace, Tectonic's cache was directed into `scratch/tectonic-cache` to keep all generated files inside the project. The portable compiler and dependency caches are not included in the source package.

## Reproduce the CPU analyses

The analysis uses public saved predictions; it does not retrain backbones. Install the versions in [requirements.txt](requirements.txt), then run from the repository root:

```text
python paper/analysis/fetch_inputs.py
python paper/analysis/reanalyse.py
python paper/analysis/policy_sensitivity.py
python paper/analysis/make_results.py
```

The second analysis enriches `oracle_audit.csv` with cost-matched comparisons; run it after `reanalyse.py` and before generating figures. The downloaded files occupy roughly 140 MB and are cached under `msc_results/`. Existing files are reused; hashes are checked before the primary analysis. Requests are sequential, with retries for rate limits and temporary server failures. No token or HF write operation is used.

`verify_manuscript.py` additionally verifies the seven joint controls, all included in the fetch manifest. `build_references.py` regenerates the bibliography from cached primary metadata. `verify_manuscript.py` conducts a separate online title-verification pass, and `render_check.py` renders every PDF page for visual inspection.

## Evidence boundaries

The reanalysis is post hoc. The gate split is disjoint at the router stage, but the dataset already informed earlier model/project decisions. Costs omit cumulative previous-head and router overhead; no measured latency or energy gain is claimed. The ImageNet subset is custom and animal-heavy. The MSDNet architecture is a documented variant. Generic final-model artifacts in joint runs score an inactive classifier and remain quarantined; the manuscript's depth-head counts are independently verified.

The larger source package includes the analysis data, reference checks, and public-artifact manifests. The compact Overleaf package contains only files required to compile the manuscript.

## Independent manuscript audit (8 September 2026)

See [AUDIT_REPORT.md](AUDIT_REPORT.md) and [INDEPENDENT_AUDIT.json](INDEPENDENT_AUDIT.json). The independent audit checks every real-model oracle against a separately formulated linear program and reconstructs transferred policies directly from raw predictions. Run `python paper/analysis/independent_audit.py` after the analyses above. Displayed tables use decimal rounding with ties rounded up after removing numerical noise below ten decimal places; full-precision analysis values are retained.
