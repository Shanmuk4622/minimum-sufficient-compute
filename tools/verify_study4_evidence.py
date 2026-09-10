"""Verify the pinned HF snapshot; optionally recompute P2/P3 from local parquets.

python tools/verify_study4_evidence.py
python tools/verify_study4_evidence.py --parquet-root msc_results

The optional parquet check requires pyarrow. This script reads local files only.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/evidence/hf_2026-09-07'


def verify(parquet_root=None):
    manifest = json.loads((SNAPSHOT / 'manifest.json').read_text())
    checked = 0
    for row in manifest['files']:
        local = SNAPSHOT / row['repo'].split('/')[-1] / row['path']
        expected_retained = row['path'].startswith('analysis/s') or any(
            tag in row['path'] for tag in ('p6-', 'p7-msdnet-'))
        if row.get('retained', '').startswith('msc_results only'):
            expected_retained = False
        if not local.exists():
            if expected_retained:
                raise ValueError(f'Missing retained evidence: {local}')
            continue
        raw = local.read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError(f'Evidence differs from pinned source: {local}')
        checked += 1

    records = list(csv.DictReader((SNAPSHOT / 'msc-cifar100/analysis/s4_msdnet.csv').open()))
    msd = [r for r in records if r['arch'] == 'msdnet' and r['exits'] == 'designed']
    if sorted(int(r['seed']) for r in msd) != [1, 2]:
        raise ValueError('Expected exactly MSDNet seeds 1 and 2')
    validation = {r['run_id']: r for r in json.loads((SNAPSHOT / 'study4_validation.json').read_text())}
    image_validation = json.loads((SNAPSHOT / 'study4_imagenet_validation.json').read_text())
    validation.update({r['run_id']: r for r in image_validation})
    imagenet = list(csv.DictReader((SNAPSHOT / 'msc-cifar100/analysis/s4_imagenet_excess.csv').open()))
    if sorted(r['arch'] for r in imagenet) != ['resnet50', 'vit_small_p16']:
        raise ValueError('Expected exactly the two P2 architectures')
    checks = list(msd)
    for r in imagenet:
        matches = [v for v in image_validation if v['arch'] == r['arch']]
        if len(matches) != 1:
            raise ValueError('Expected one P2 validation record per architecture')
        checks.append(dict(r, run_id=matches[0]['run_id'], n_samples=10000, n_exits=5,
                           oracle_in=float(r['acc_full']) + float(r['excess'])))
    for r in checks:
        base = SNAPSHOT / 'msc-cifar100/runs' / r['run_id']
        summary = json.loads((base / 'summary.json').read_text())
        if summary['status'] != 'completed' or summary['num_epochs_run'] != summary['num_epochs_planned']:
            raise ValueError(f'Incomplete run: {r["run_id"]}')
        if abs(float(r['oracle_in']) - float(r['acc_full']) - float(r['excess'])) > 1e-8:
            raise ValueError('CSV excess identity fails')
        if not parquet_root:
            continue
        import pyarrow.parquet as pq
        p = Path(parquet_root) / 'runs' / r['run_id'] / 'per_sample/test.parquet'
        if hashlib.sha256(p.read_bytes()).hexdigest() != validation[r['run_id']]['parquet_sha256']:
            raise ValueError(f'Parquet differs from audit revision: {p}')
        keys = sorted((k for k in pq.read_schema(p).names
                       if k.startswith('pred_d') and k[6:].isdigit()), key=lambda k: int(k[6:]))
        data = pq.read_table(p, columns=['sample_idx', 'label'] + keys).to_pydict()
        n = len(data['label'])
        if n != int(r['n_samples']) or len(set(data['sample_idx'])) != n or len(keys) != int(r['n_exits']):
            raise ValueError('Unexpected sample IDs, sample count or exit count')
        full = sum(a == b for a, b in zip(data['label'], data[keys[-1]]))
        any_right = sum(any(data[k][i] == y for k in keys) for i, y in enumerate(data['label']))
        saves = sum(data[keys[-1]][i] != y and any(data[k][i] == y for k in keys[:-1])
                    for i, y in enumerate(data['label']))
        if any_right - full != saves:
            raise ValueError('Early-save count identity fails')
        for key, value in [('acc_full', 100 * full / n), ('oracle_in', 100 * any_right / n),
                           ('excess', 100 * saves / n)]:
            if abs(float(r[key]) - value) > 1e-9:
                raise ValueError(f'Parquet disagrees with CSV: {key}')
        print(f'{r["run_id"]}: {full}/{n} final correct; {any_right}/{n} any-exit correct; {saves} early saves')
    print(f'PASS: {checked} retained source hashes; all four P2/P3 completion records and CSV identities')
    if not parquet_root:
        print('Parquet recomputation not requested; pass --parquet-root to reproduce it.')
    print('D-91 remains open: generic final.json is not trained-final-exit evaluation.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parquet-root', type=Path)
    verify(parser.parse_args().parquet_root)
