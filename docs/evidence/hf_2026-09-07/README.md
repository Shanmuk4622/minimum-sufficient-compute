# Hugging Face evidence snapshot — 2026-09-07

Read-only retrieval from the two public dataset repositories. No token was
needed and nothing was uploaded. [manifest.json](manifest.json) records the
immutable revisions, source URLs, byte sizes and SHA-256 hashes of fetched files.

The compact Study 2–4 CSVs and P6/P7 run records are stored under `msc-cifar100/`.
Study 4's ImageNet runs are in that repository too. The older ImageNet repository
was inventoried independently; no matching P6/P7 runs were listed there.

Both MSDNet test parquets were downloaded and recomputed. They are excluded from
git under `msc_results/`; their hashes and immutable URLs remain in the manifest.
[study4_validation.json](study4_validation.json) contains the independent integer
counts and the conflicting generic evaluation values.

From the repository root, regenerate the public tables with:

```text
python tools/build_results.py
python tools/verify_study4_evidence.py
```

The generator defaults to this pinned CSV snapshot. To use another result tree,
pass `--results-root PATH` where PATH contains `analysis/`.

To repeat the integer-count check with the downloaded parquets and `pyarrow`
installed, run `python tools/verify_study4_evidence.py --parquet-root msc_results`.
It reads local files only; the manifest supplies pinned URLs for retrieving the
two `test.parquet` inputs on another machine.

The original source bytes are preserved, including inconsistent metadata.
Corrections and interpretation live in [Study 4 findings](../../../study4/04_FINDINGS.md),
not in edited copies of the upstream evidence. File presence and arithmetic
verification do not constitute a new execution of training or the GPU measurement pipeline.

The two P2 ImageNet test parquets were subsequently checked too: see
[study4_imagenet_validation.json](study4_imagenet_validation.json). The local-only
verification command now recomputes all four P2/P3 runs when `--parquet-root` is
supplied. All four files' immutable URLs and hashes are in the manifest.
