"""Final evidence and citation integrity checks, separate from generation."""
from pathlib import Path
import sys,re,json,hashlib,urllib.request,html
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scratch/deps'))
import numpy as np,pandas as pd
import pyarrow.parquet as pq
P=ROOT/'paper';D=P/'data';checks=[]
def check(name,condition):
    assert condition,name
    checks.append(name)
o=pd.read_csv(D/'oracle_audit.csv');g=pd.read_csv(D/'heldout_routing.csv')
check('630 oracle rows / 15 architectures / 90 seed pairs',len(o)==630 and o.arch.nunique()==15 and len(o[['arch','source','target']].drop_duplicates())==90)
check('1575 disjoint-router rows',len(g)==1575)
check('Oracle feasible',bool((o.oracle_cost<=o.budget+1e-9).all()))
check('Exact oracle weakly dominates legacy',bool((o.oracle>=o.legacy_oracle-1e-9).all()))
check('Target optimum bounds transferred policy',bool((o.oracle>=o.cross-1e-9).all()))
check('Confidence cost matching discrepancy < 0.000074',bool((o.cross_cost-o.confidence_matched_realised_cost).abs().max()<.000074))
split=pd.read_csv(D/'router_split.csv')
check('Unique 10000 split IDs',len(split)==10000 and split.sample_idx.is_unique)
check('Per-class 40/20/40 partition',all(split.groupby('label').role.value_counts().unstack()[k].eq(v).all() for k,v in [('fit',40),('calibration',20),('evaluation',40)]))
check('No fit/calibration/evaluation image overlap',sum(len(set(split[split.role==k].sample_idx)) for k in split.role.unique())==len(set(split.sample_idx)))
check('All calibration costs feasible',bool((g.calibration_cost<=g.budget+1e-9).all()))
check('Held-out accuracy bounded at its realized cost',bool((g.accuracy<=g.oracle_at_realised_cost+1e-9).all()))
controls=[]
for prefix,arch,seed,full,anyc in [('p4','resnet20',1,6802,7866),('p4','resnet32x4',1,7783,8638),('p4','vgg8',1,7228,8143),('p6','resnet50',1,8158,8897),('p6','vit_small_p16',1,6323,7014),('p7','msdnet',1,7393,8167),('p7','msdnet',2,7408,8199)]:
    dataset='imagenet100' if prefix=='p6' else 'cifar100'
    rid=f'{prefix}-{arch}-{dataset}-jointexit-s{seed}'
    path=ROOT/f'msc_results/runs/{rid}/per_sample/test.parquet'
    d=pq.read_table(path).to_pandas().sort_values('sample_idx')
    ks=sorted(int(k[6:]) for k in d if k.startswith('pred_d') and k[6:].isdigit())
    correct=np.stack([d[f'pred_d{k}'].to_numpy()==d.label.to_numpy() for k in ks],axis=1)
    check(rid+' raw counts',len(d)==10000 and d.sample_idx.is_unique and correct[:,-1].sum()==full and correct.any(1).sum()==anyc)
    controls.append(dict(run_id=rid,n=10000,final_correct=full,any_correct=anyc,early_saves=anyc-full,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
(D/'controls_validation.json').write_text(json.dumps(controls,indent=2))
tex=(P/'main.tex').read_text();bib=(P/'bibliography.bib').read_text()
cites={k.strip() for block in re.findall(r'\\cite\w*\{([^}]+)\}',tex) for k in block.split(',')}
keys=set(re.findall(r'@\w+\{([^,]+),',bib))
check('All 23 references cited and all citations resolved',cites==keys and len(keys)==23)
check('Authors empty',r'\author{}' in tex)
check('No unresolved draft placeholders',not re.search(r'\b(TODO|TBD|FIXME|INSERT HERE)\b',tex))
audit=json.loads((P/'references/audit.json').read_text())
second=[]
for r in audit:
    if r['key']=='cifar':continue
    url=r['source']
    try:
        with urllib.request.urlopen(url,timeout=45) as response:raw=response.read()
        text=raw.decode('utf-8','replace')
        if 'api.crossref' in url:
            title=json.loads(text)['message']['title'][0]
        else:
            matches=re.findall(r'<meta\s+name="citation_title"\s+content="([^"]+)"',text)
            title=html.unescape(matches[0])
        norm=lambda s:re.sub(r'[^a-z0-9]','',html.unescape(s).lower())
        check(r['key']+' second-pass title match',norm(title)==norm(r['fields']['title']))
        second.append(dict(key=r['key'],url=url,status='title reverified from primary metadata',sha256=hashlib.sha256(raw).hexdigest()))
    except Exception as error:
        raise RuntimeError(f'Reference reverification failed: {r["key"]}: {error}')
for r in audit:
    if 'publication_source' in r:
        raw=(P/'references'/(r['key']+'.venue.source')).read_text(encoding='utf-8')
        # A challenge page is never treated as bibliographic evidence.
        check(r['key']+' published title present',re.sub('[^a-z0-9]','',r['fields']['title'].lower()) in re.sub('[^a-z0-9]','',html.unescape(raw).lower()))
(P/'references/second_pass.json').write_text(json.dumps(second,indent=2))
(P/'VERIFICATION.json').write_text(json.dumps({'date':'2026-09-08','passed_checks':checks,'status':'Evidence and reference checks passed; PDF visual review separate'},indent=2))
print('PASSED',len(checks),'checks')
