"""Independent LP/row-level audit of the delivered predictions and analysis.

Does not import the paper's oracle or routing implementation.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scratch/deps'))
import numpy as np,pandas as pd
from scipy.optimize import linprog
from scipy.sparse import kron,eye,csr_matrix
D=ROOT/'paper/data';o=pd.read_csv(D/'oracle_audit.csv');g=pd.read_csv(D/'heldout_routing.csv')
cache={};costs={};report={}
manifest=json.loads((D/'input_manifest.json').read_text())
for r in manifest:
    p=ROOT/'msc_results'/r['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],str(p)
    if r['path'].startswith('budgets/'):
        b=json.loads(p.read_text());costs[b['arch']]=np.asarray(b['axes']['depth']['rho'])
    if r['path'].startswith('runs/p1-') and p.suffix=='.parquet':
        d=pd.read_parquet(p).sort_values('sample_idx')
        keys=sorted([x for x in d if x.startswith('pred_d') and x[6:].isdigit()],key=lambda x:int(x[6:]))
        c=np.column_stack([d[x].to_numpy()==d.label.to_numpy() for x in keys])
        rid=r['path'].split('/')[1];a=rid.split('-')[1];s=int(rid[-1])
        cache[(a,s)]=(d,c,keys)
errors=[]
for (a,s),(d,c,keys) in cache.items():
    patterns,counts=np.unique(c,axis=0,return_counts=True)
    weights=counts/len(c);K=c.shape[1];G=len(counts);rho=costs[a]
    objective=(patterns*weights[:,None]).ravel().astype(float)
    ac=csr_matrix((weights[:,None]*rho).ravel()[None,:])
    eq=kron(eye(G),np.ones((1,K)),format='csr')
    for b in sorted(o.budget.unique()):
        solution=linprog(-objective,A_ub=ac,b_ub=[b],A_eq=eq,b_eq=np.ones(G),bounds=(0,1),method='highs')
        assert solution.success and float((ac@solution.x)[0])<=b+1e-8
        stored=o[(o.arch==a)&(o.target==s)&(o.budget==b)].oracle
        error=float(np.max(np.abs(stored+solution.fun)));errors.append(error)
        assert error<1e-9,(a,s,b,error)
report['real_model_LP_comparisons']=len(errors);report['max_oracle_accuracy_difference']=max(errors)
cross_error=[];cost_error=[]
for r in o.itertuples():
    source=cache[(r.arch,r.source)][1];target=cache[(r.arch,r.target)][1];rho=costs[r.arch]
    n,K=source.shape
    allocation=np.zeros((n,K));allocation[:,0]=1
    first=np.argmax(source,axis=1);available=n*(r.budget-rho[0])
    eligible=(~source[:,0])&source.any(axis=1)
    for k in range(1,K):
        members=np.flatnonzero(eligible&(first==k))
        if len(members)==0:continue
        fraction=np.clip(available/(len(members)*(rho[k]-rho[0])),0,1)
        allocation[members,0]=1-fraction;allocation[members,k]=fraction
        available-=fraction*len(members)*(rho[k]-rho[0])
    acc=float((allocation*target).sum()/n);cost=float((allocation*rho).sum()/n)
    cross_error.append(abs(acc-r.cross));cost_error.append(abs(cost-r.cross_cost))
    assert abs(acc-r.cross)<1e-10 and abs(cost-r.cross_cost)<1e-10
report['full_allocation_transfer_comparisons']=len(cross_error)
report['max_transfer_accuracy_difference']=max(cross_error)
split=pd.read_csv(D/'router_split.csv').set_index('sample_idx').role
count=0
for r in g[g.rule.isin(['confidence','margin'])].itertuples():
    d,c,keys=cache[(r.arch,r.target)];rho=costs[r.arch]
    scores=np.column_stack([d['top1p_d'+x[6:]] for x in keys])
    if r.rule=='margin':scores=scores-np.column_stack([d['top2p_d'+x[6:]] for x in keys])
    idx=np.full(len(d),len(keys)-1)
    # Reverse traversal leaves the earliest qualifying exit selected.
    for k in reversed(range(len(keys)-1)):idx[scores[:,k]>=r.threshold]=k
    roles=split.loc[d.sample_idx].to_numpy();ev=roles=='evaluation';cal=roles=='calibration'
    assert abs(c[np.arange(len(c)),idx][ev].mean()-r.accuracy)<1e-10
    assert abs(rho[idx][ev].mean()-r.cost)<1e-10
    assert abs(rho[idx][cal].mean()-r.calibration_cost)<1e-10
    count+=1
report['raw_threshold_rule_checks']=count
report['input_hashes_checked']=len(manifest)
report['status']='passed'
(ROOT/'paper/INDEPENDENT_AUDIT.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
