"""Download public, revision-pinned predictions. No credentials or uploads."""
import hashlib, json, time, urllib.request, urllib.error
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
REV = 'a6356f6a8dee0be1c8bdbfa55e07924b62976da8'
REPO = 'Shanmuk4622/msc-cifar100'
existing_manifest=ROOT/'paper/data/input_manifest.json'
if existing_manifest.exists():
    prior=json.loads(existing_manifest.read_text())
    paths=[x['path'] for x in prior]
    expected={x['path']:x['sha256'] for x in prior}
else:
    expected={}
    with urllib.request.urlopen(f'https://huggingface.co/api/datasets/{REPO}/revision/{REV}',timeout=60) as response:meta=json.load(response)
    paths = [x['rfilename'] for x in meta['siblings']]
tests = [p for p in paths if p.startswith('runs/p1-') and p.endswith('/test.parquet')]
archs = sorted({p.split('/')[1].split('-')[1] for p in tests})
selected = tests + [f'budgets/{a}.json' for a in archs]
selected += [f'runs/p1-{a}-cifar100-base-s1/config.yaml' for a in archs]
selected += [f'runs/p4-{a}-cifar100-jointexit-s1/{f}' for a in ['resnet20','resnet32x4','vgg8'] for f in ['config.yaml','per_sample/test.parquet']]
selected += [f'runs/{rid}/per_sample/test.parquet' for rid in ['p6-resnet50-imagenet100-jointexit-s1','p6-vit_small_p16-imagenet100-jointexit-s1','p7-msdnet-cifar100-jointexit-s1','p7-msdnet-cifar100-jointexit-s2']]
manifest = []
for i,p in enumerate(selected):
    local = ROOT/'msc_results'/p
    url = f'https://huggingface.co/datasets/{REPO}/resolve/{REV}/{p}'
    if not local.exists():
        for attempt in range(6):
            try:
                with urllib.request.urlopen(url, timeout=120) as r: raw=r.read()
                local.parent.mkdir(parents=True,exist_ok=True)
                local.write_bytes(raw)
                break
            except urllib.error.HTTPError as e:
                if e.code not in (429,500,502,503,504): raise
                time.sleep(min(60,int(e.headers.get('Retry-After','20'))))
        else: raise RuntimeError(url)
    raw=local.read_bytes()
    if p in expected and hashlib.sha256(raw).hexdigest()!=expected[p]:raise RuntimeError('Cached/downloaded input hash differs from manifest: '+p)
    manifest.append(dict(path=p,url=url,revision=REV,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    print(f'{i+1}/{len(selected)} {p} {len(raw)}',flush=True)
out=ROOT/'paper/data';out.mkdir(parents=True,exist_ok=True)
(out/'input_manifest.json').write_text(json.dumps(manifest,indent=2))
