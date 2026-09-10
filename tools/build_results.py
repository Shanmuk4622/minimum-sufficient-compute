#!/usr/bin/env python3
"""Regenerate RESULTS.md and RESULTS.csv from the analysis CSVs.

Every headline number in this repository is produced HERE, from the artifacts,
so a figure quoted in prose can never drift from the file it came from. Run it
after any analysis notebook.

Usage:  python tools/build_results.py [--results-root C:\\msc_results]
"""
import argparse, csv, statistics as st
from collections import defaultdict
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--results-root", default=None)
ap.add_argument("--out", default=None)
a = ap.parse_args()

ROOT = Path(__file__).resolve().parent.parent
res = Path(a.results_root) if a.results_root else None
if res is None:
    for c in (ROOT / "docs/evidence/hf_2026-09-07/msc-cifar100",
              Path(r"C:\msc_results"), Path("/sessions/jolly-happy-gates/mnt/msc_results")):
        if (c / "analysis").is_dir():
            res = c; break
if res is None or not (res / "analysis").is_dir():
    raise SystemExit("no analysis/ found; pass --results-root")
AN = res / "analysis"
out_dir = Path(a.out) if a.out else ROOT
rows = []          # (study, question, metric, scope, value, unit, source)

def add(*r): rows.append(r)
def load(n):
    p = AN / n
    return list(csv.DictReader(p.open())) if p.exists() else []

# ---- Study 2 -------------------------------------------------------------
orc = [r for r in load("s2_true_oracle.csv") if r.get("dataset") == "cifar100"]
if orc:
    f = lambda k: st.median(float(r[k]) for r in orc) * 100
    for k, lab in [("baseline", "confidence baseline"), ("acc_full", "full compute"),
                   ("oracle_in", "oracle, in-seed"), ("oracle_cross", "oracle, cross-seed"),
                   ("ceiling_optimistic", "in-seed - baseline"),
                   ("ceiling_honest", "cross-seed - baseline"),
                   ("bias_true", "optimism bias"),
                   ("frac_early_saves", "early-right/final-wrong pool")]:
        # levels are percentages; differences and pools are points. Keyed on the
        # column, not on punctuation in the label -- "oracle, in-seed" contains
        # a hyphen and is a LEVEL.
        unit = "%" if k in ("baseline", "acc_full", "oracle_in", "oracle_cross") else "pt"
        add("2", "oracle ceiling", lab, f"CIFAR-100, {len(orc)} seed pairs, rho=0.80",
            round(f(k), 2), unit, "s2_true_oracle.csv")
    excess = [float(r["oracle_in"]) - float(r["acc_full"]) for r in orc]
    add("2", "oracle ceiling", "oracle ABOVE own full-compute accuracy",
        f"{sum(1 for x in excess if x > 0)}/{len(excess)} ordered seed-pair rows (45 trained models)",
        round(st.median(excess) * 100, 2), "pt", "s2_true_oracle.csv")

grid = [r for r in load("s2_reliability_grid.csv")
        if r.get("dataset") == "cifar100" and r.get("split") == "test"]
if grid:
    v = [float(r["rho_seed"]) for r in grid]
    add("2", "reliability atlas", "rho_seed range across the grid",
        f"{len({r['arch'] for r in grid})} archs x {len({r['score'] for r in grid})} scores",
        round(max(v) - min(v), 3), "rho", "s2_reliability_grid.csv")
    add("2", "reliability atlas", "rho_seed minimum", "mixer_nano / entropy",
        round(min(v), 3), "rho", "s2_reliability_grid.csv")
    add("2", "reliability atlas", "rho_seed maximum", "mobilenetv2 / ce_loss",
        round(max(v), 3), "rho", "s2_reliability_grid.csv")

mem = load("s2_memorisation.csv")
if mem:
    def sp(x, y):
        rx = [sorted(x).index(v) + 1 for v in x]; ry = [sorted(y).index(v) + 1 for v in y]
        mx, my = st.mean(rx), st.mean(ry)
        n = sum((p - mx) * (q - my) for p, q in zip(rx, ry))
        d = (sum((p - mx) ** 2 for p in rx) * sum((q - my) ** 2 for q in ry)) ** .5
        return n / d
    g = lambda k: [float(r[k]) for r in mem]
    for k, lab in [("frac_conf_over_99", "softmax saturation"),
                   ("acc_train", "train accuracy"),
                   ("acc_test", "TEST accuracy (control)")]:
        add("2", "memorisation collapse", f"Spearman({lab}, rho_seed drop)",
            f"{len(mem)} architectures", round(sp(g(k), g("rho_drop")), 3), "rho",
            "s2_memorisation.csv")
    worst = max(mem, key=lambda r: float(r["rho_drop"]))
    add("2", "memorisation collapse", "largest rho_seed drop, test -> train_holdout",
        worst["arch"], round(float(worst["rho_drop"]), 3), "rho", "s2_memorisation.csv")

# ---- Study 3 -------------------------------------------------------------
q1 = load("s3_q1_comparison.csv")
for r in q1:
    add("3", "Q1 joint exits", f"excess, {r['arch']}", "frozen",
        round(float(r["excess_frozen"]), 2), "pt", "s3_q1_comparison.csv")
    add("3", "Q1 joint exits", f"excess, {r['arch']}", "JOINT",
        round(float(r["excess_joint"]), 2), "pt", "s3_q1_comparison.csv")
if q1:
    ex = [float(r["excess_joint"]) for r in q1]
    add("3", "Q1 joint exits", "H1: excess >= 2.0 pt under joint training",
        f"{sum(1 for x in ex if x >= 2.0)}/{len(ex)} architectures",
        round(st.median(ex), 2), "pt", "s3_q1_comparison.csv")
    d = [float(r["d_excess"]) for r in q1]
    add("3", "Q1 joint exits", "change frozen -> joint (raw median)", "3 architectures",
        round(st.median(d), 2), "pt", "s3_q1_comparison.csv")

cap = load("s3_router_capture.csv")
for kind in ("in-seed", "cross-seed"):
    v = [float(r["capture"]) for r in cap if r["kind"] == kind]
    if v:
        add("3", "Q2 learned router", f"capture fraction, {kind}",
            f"{len(v)} architectures, rho=0.80", round(st.median(v) * 100, 2), "%",
            "s3_router_capture.csv")
gaps = [float(r["gap"]) for r in cap if r["kind"] == "cross-seed"]
if gaps:
    add("3", "Q2 learned router", "oracle gap available to be captured",
        "median over architectures", round(st.median(gaps), 2), "pt",
        "s3_router_capture.csv")

pr = load("s3_pruning.csv")
if pr:
    g = defaultdict(list)
    for r in pr: g[(int(r["rate"]), r["arm"])].append(float(r["acc"]) * 100)
    for (rate, arm), v in sorted(g.items()):
        add("3", "Q3 pruning", f"target accuracy, {arm}", f"keep {rate}%",
            round(st.mean(v), 2), "%", "s3_pruning.csv")

# ---- Study 4 -------------------------------------------------------------
bs = load("s4_bootstrap.csv")
for r in bs:
    add("4", "P0 bootstrap CI", f"excess, {r['arch']}",
        f"95% CI over {int(float(r['n_samples'])):,} TEST SAMPLES (not seeds)",
        f"{float(r['excess']):.2f}  [{float(r['ci_lo']):.2f}, {float(r['ci_hi']):.2f}]",
        "pt", "s4_bootstrap.csv")
if bs:
    add("4", "P0 bootstrap CI", "intervals excluding zero",
        f"{len(bs)} joint runs",
        sum(1 for r in bs if float(r["ci_lo"]) > 0), f"of {len(bs)}",
        "s4_bootstrap.csv")

im = load("s4_imagenet_excess.csv")
for r in im:
    add("4", "P2 ImageNet-100 @224px", f"excess, {r['arch']}",
        "1 seed; per-run identity", round(float(r["excess"]), 2), "pt",
        "s4_imagenet_excess.csv")
    add("4", "P2 ImageNet-100 @224px", f"full-compute accuracy, {r['arch']}",
        "1 seed", round(float(r["acc_full"]), 2), "%", "s4_imagenet_excess.csv")
if im:
    add("4", "P2 ImageNet-100 @224px", "H4: excess >= 2.0 pt",
        f"{sum(1 for r in im if float(r['excess']) >= 2.0)} of {len(im)} archs",
        round(min(float(r["excess"]) for r in im), 2), "pt (min)",
        "s4_imagenet_excess.csv")
    vit = [r for r in im if "vit" in r["arch"]]
    if vit:
        add("4", "P2 ImageNet-100 @224px", "H4b: the TRANSFORMER alone",
            vit[0]["arch"], round(float(vit[0]["excess"]), 2), "pt",
            "s4_imagenet_excess.csv")

bl = load("s4_baselines.csv")
if bl:
    hh = defaultdict(list)
    accs = defaultdict(list)
    for r in bl:
        hh[(float(r["target_rho"]), r["baseline"])].append(float(r["honest_headroom"]))
        accs[(float(r["target_rho"]), r["baseline"])].append(float(r["baseline_acc"]))
    rhos = sorted({float(r["target_rho"]) for r in bl})
    # confidence and margin hit the budget exactly; patience cannot, so the
    # sign question is answered on the two that are comparable.
    for rr in rhos:
        v = st.median(hh[(rr, "confidence")])
        add("4", "P1 honest headroom vs budget",
            f"cross-seed oracle - confidence, rho={rr:.2f}",
            "median over 15 CIFAR architectures", round(v, 2), "pt",
            "s4_baselines.csv")
    flip = [rr for rr in rhos if st.median(hh[(rr, "confidence")]) > 0]
    add("4", "P1 honest headroom vs budget", "budgets with POSITIVE honest headroom",
        "confidence baseline", str(flip), "rho", "s4_baselines.csv")
    sp = max(abs(st.median(hh[(rr, "confidence")]) - st.median(hh[(rr, "margin")]))
             for rr in rhos)
    add("4", "P1 baseline independence",
        "max |confidence - margin| headroom gap",
        "difference of architecture medians across 7 target budgets", round(sp, 2), "pt",
        "s4_baselines.csv")
    fair = [r for r in bl
            if float(r["achieved_cost"]) <= float(r["target_rho"]) + 0.01]
    # Compare the SAME architecture/budget cells across all rules. Pooling each
    # rule's eligible rows independently gives patience a different population.
    rules = {r['baseline'] for r in bl}
    coverage = defaultdict(set)
    for r in fair:
        coverage[(r['arch'], float(r['target_rho']))].add(r['baseline'])
    common = {key for key, present in coverage.items() if present == rules}
    m = defaultdict(list)
    for r in fair:
        if (r['arch'], float(r['target_rho'])) in common:
            m[r["baseline"]].append(float(r["baseline_acc"]))
    for k in sorted(m):
        add("4", "P1 baseline strength", f"{k}, common eligible cells",
            f"median over {len(common)} shared arch/budget cells; cost <= target + 0.01 (not exact cost matching)", round(st.median(m[k]), 2), "%",
            "s4_baselines.csv")

msd = [r for r in load('s4_msdnet.csv') if r['arch'] == 'msdnet' and r['exits'] == 'designed']
if msd:
    seeds = [int(r['seed']) for r in msd]
    if sorted(seeds) != [1, 2]:
        raise ValueError('H5 requires exactly one MSDNet row for each of seeds 1 and 2')
    for r in msd:
        if r['joint'].lower() != 'true' or int(r['n_exits']) != 5 or int(r['n_samples']) != 10000:
            raise ValueError('Unexpected MSDNet population or training mode')
        if abs(float(r['oracle_in']) - float(r['acc_full']) - float(r['excess'])) > 1e-8:
            raise ValueError('MSDNet excess identity does not hold')
        for key, label, unit in [('acc_full', 'final-exit accuracy', '%'),
                                 ('oracle_in', 'any-correct-exit oracle', '%'),
                                 ('excess', 'oracle excess', 'pt')]:
            add('4', 'P3 MSDNet variant', label, f"seed {r['seed']}; 5 joint exits; 10,000 test samples",
                round(float(r[key]), 2), unit, 's4_msdnet.csv')
    passed = sum(float(r['excess']) >= 2.0 for r in msd)
    add('4', 'P3 MSDNet variant', 'H5: excess >= 2.0 pt in both seeds',
        'documented variant; not an official MSDNet replication', passed, 'of 2', 's4_msdnet.csv')
    add('4', 'P3 MSDNet variant', 'mean excess', '2 seeds; descriptive mean, not a seed confidence interval',
        f"{st.mean(float(r['excess']) for r in msd):.3f}", 'pt', 's4_msdnet.csv')

# ---- write ---------------------------------------------------------------
with (out_dir / "RESULTS.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["study", "question", "metric", "scope", "value", "unit", "source"])
    w.writerows(rows)

by = defaultdict(list)
for r in rows: by[(r[0], r[1])].append(r)
lines = ["# Results — every headline number, generated from the artifacts", "",
         "**Do not hand-edit.** Regenerate with `python tools/build_results.py`.",
         "Machine-readable copy: [`RESULTS.csv`](RESULTS.csv).", "",
         "**September 8 manuscript extension:** these are archived study summaries, not the new paper-analysis tables.",
         "See [`paper/README.md`](paper/README.md) for exact oracle allocation, realized-cost matching,",
         "source-optimal policy envelopes, and the disjoint router experiment. Historical gate capture",
         "reused test images for fitting and evaluation and is not held-out generalization evidence.", "",
         "Source CSVs are on HuggingFace at",
         "[`Shanmuk4622/msc-cifar100`](https://huggingface.co/datasets/Shanmuk4622/msc-cifar100)",
         "under `analysis/`. The default input is the pinned 2026-09-07 snapshot;",
         "pass `--results-root` explicitly to use another analysis tree.",
         "Provenance: [`manifest.json`](docs/evidence/hf_2026-09-07/manifest.json).", "",
         "Differences are aggregated per row; subtracting separately aggregated levels need not reproduce them.",
         "Study 2 has 90 ordered seed pairs from 45 models, not 90 independent training runs.",
         "Historical CSV fields `oracle_cross` / `honest_headroom` describe seed-transfer diagnostics,",
         "not proven upper bounds on deployable routing. See [`PAPER_CLAIM.md`](PAPER_CLAIM.md).",
         "MSDNet values use the trained final exit; generic `metrics/final.json` is quarantined",
         "because it evaluates a different classifier. See [`Study 4 findings`](study4/04_FINDINGS.md).", ""]
for (study, q), rs in by.items():
    lines += [f"## Study {study} — {q}", "",
              "| metric | scope | value | source |", "|---|---|---|---|"]
    for _, _, metric, scope, val, unit, src in rs:
        metric = str(metric).replace('|', r'\|')
        scope = str(scope).replace('|', r'\|')
        lines.append(f"| {metric} | {scope} | **{val} {unit}** | `{src}` |")
    lines.append("")
(out_dir / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
print(f"wrote RESULTS.md and RESULTS.csv  ({len(rows)} rows) to {out_dir}")
