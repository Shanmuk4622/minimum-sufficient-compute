"""Post-hoc routing audit; predictions only, no backbone training.

Run from repo root after fetch_inputs.py. Dependencies: numpy, pandas,
pyarrow, scipy, scikit-learn. All quantities in CSVs are fractions.
"""
from pathlib import Path
import sys, json, hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scratch/deps'))
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from scipy.optimize import linprog

def exact_oracle(source, target, rho, budget):
    """Expected target accuracy of an optimal source policy; uniform tie mixture."""
    n,K=source.shape
    if budget < rho[0]-1e-10: raise ValueError('infeasible budget')
    first=source.argmax(1)
    upgrades=(~source[:,0]) & source.any(1)
    remaining=n*(budget-rho[0]); acc=target[:,0].sum(dtype=float); spent=n*rho[0]
    for k in range(1,K):
        group=upgrades & (first==k); count=int(group.sum())
        if not count: continue
        delta=rho[k]-rho[0]
        prob=min(1.,max(0.,remaining/(count*delta)))
        acc+=prob*(target[group,k].astype(float)-target[group,0]).sum()
        spent+=prob*count*delta;remaining-=prob*count*delta
    return acc/n,spent/n

def legacy_oracle(source,target,rho,budget):
    lo,hi=0.,100.
    for _ in range(80):
        lam=(lo+hi)/2;k=(source-lam*rho).argmax(1)
        if rho[k].mean()>budget: lo=lam
        else: hi=lam
    k=(source-hi*rho).argmax(1)
    return target[np.arange(len(k)),k].mean(),rho[k].mean()

def route(scores,threshold):
    fires=scores>=threshold;fires=fires.copy();fires[:,-1]=True
    return fires.argmax(1)

def calibrate(scores,rho,budget):
    # Largest feasible shared threshold, with explicit feasible-side return.
    lo,hi=0.,1.0000001
    for _ in range(60):
        mid=(lo+hi)/2
        if rho[route(scores,mid)].mean()<=budget:lo=mid
        else:hi=mid
    return lo

def features(p,q,k):
    a,b=p[:,k],q[:,k]
    return np.column_stack([a,b,a-b,np.log(np.clip(a,1e-9,1)),a/np.clip(b,1e-9,None)])

def validate_solver():
    rng=np.random.default_rng(53)
    for _ in range(30):
        c=rng.random((9,4))>.5;rho=np.array([.1,.3,.6,1.]);b=rng.uniform(.1,1)
        a,cost=exact_oracle(c,c,rho,b)
        eq=np.kron(np.eye(9),np.ones((1,4)))
        lp=linprog(-c.ravel().astype(float)/9,A_ub=np.tile(rho,9)[None,:]/9,b_ub=[b],A_eq=eq,b_eq=np.ones(9),bounds=(0,1),method='highs')
        assert lp.success and abs(a+lp.fun)<1e-9 and cost<=b+1e-9
    print('Exact oracle agrees with 30 independent linear programs',flush=True)

def main():
    validate_solver()
    manifest=json.loads((ROOT/'paper/data/input_manifest.json').read_text())
    tables={}; budgetmap={}; identity=[]; common=None
    for record in manifest:
        p=ROOT/'msc_results'/record['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256']
        if record['path'].endswith('config.yaml') or (record['path'].startswith('runs/') and not record['path'].startswith('runs/p1-')):continue
        if record['path'].startswith('budgets/'):
            b=json.loads(p.read_text());budgetmap[b['arch']]=np.array(b['axes']['depth']['rho']);continue
        d=pd.read_parquet(p).sort_values('sample_idx')
        ids=d.sample_idx.to_numpy();labels=d.label.to_numpy()
        assert len(d)==10000 and len(np.unique(ids))==10000
        if common is None:common=(ids,labels)
        else:assert np.array_equal(ids,common[0]) and np.array_equal(labels,common[1])
        ks=sorted(int(x[6:]) for x in d if x.startswith('pred_d') and x[6:].isdigit())
        c=np.stack([d[f'pred_d{k}'].to_numpy()==labels for k in ks],axis=1)
        p1=np.stack([d[f'top1p_d{k}'] for k in ks],axis=1).astype(float)
        p2=np.stack([d[f'top2p_d{k}'] for k in ks],axis=1).astype(float)
        rid=record['path'].split('/')[1];arch=rid.split('-')[1];seed=int(rid[-1])
        tables[(arch,seed)]=(c,p1,p2)
        identity.append(dict(arch=arch,seed=seed,final=c[:,-1].mean(),any=c.any(1).mean(),save=(c.any(1)&~c[:,-1]).mean(),n_exits=len(ks)))
    # Fixed, class-stratified disjoint router-fit/calibration/evaluation split.
    rng=np.random.default_rng(20260908);fit=[];cal=[];test=[]
    for y in np.unique(common[1]):
        ix=np.flatnonzero(common[1]==y);rng.shuffle(ix)
        fit.extend(ix[:40]);cal.extend(ix[40:60]);test.extend(ix[60:])
    fit,cal,test=map(lambda x:np.sort(np.array(x)),(fit,cal,test))
    pd.DataFrame({'sample_idx':common[0],'label':common[1],'role':np.where(np.isin(np.arange(10000),fit),'fit',np.where(np.isin(np.arange(10000),cal),'calibration','evaluation'))}).to_csv(ROOT/'paper/data/router_split.csv',index=False)
    rows=[];gate_rows=[]
    for arch in sorted(budgetmap):
        rho=budgetmap[arch];assert np.all(np.diff(rho)>0) and rho[-1]==1
        gates={}
        for s in (1,2,3):
            c,p,q=tables[(arch,s)];assert c.shape[1]==len(rho)
            gates[s]=[]
            for k in range(len(rho)-1):
                model=make_pipeline(StandardScaler(),LogisticRegression(C=1.,max_iter=2000,random_state=0))
                model.fit(features(p,q,k)[fit],c[fit,k]);gates[s].append(model)
        for target in (1,2,3):
            c,p,q=tables[(arch,target)]
            for source in (1,2,3):
                cs,_,_=tables[(arch,source)]
                pg=np.column_stack([g.predict_proba(features(p,q,k))[:,1] for k,g in enumerate(gates[source])]+[np.ones(10000)])
                for b in (.4,.5,.6,.7,.8,.9,.95):
                    if b<rho[0]:continue
                    if source!=target:
                        same,oc=exact_oracle(c,c,rho,b);cross,sc=exact_oracle(cs,c,rho,b)
                        old,oldc=legacy_oracle(c,c,rho,b);oldx,oldxc=legacy_oracle(cs,c,rho,b)
                        th=calibrate(p,rho,b);k=route(p,th);base=c[np.arange(10000),k].mean()
                        rows.append(dict(arch=arch,source=source,target=target,budget=b,oracle=same,oracle_cost=oc,cross=cross,cross_cost=sc,legacy_oracle=old,legacy_cost=oldc,legacy_cross=oldx,legacy_cross_cost=oldxc,confidence=base,confidence_cost=rho[k].mean()))
                    for rule,score in [('confidence',p),('margin',p-q),('logistic',pg)]:
                        if rule!='logistic' and source!=target:continue
                        th=calibrate(score[cal],rho,b);k=route(score[test],th)
                        acc=c[test,k].mean();cost=rho[k].mean()
                        ceiling,_=exact_oracle(c[test],c[test],rho,cost)
                        gate_rows.append(dict(arch=arch,source=source,target=target,budget=b,rule=rule,accuracy=acc,cost=cost,calibration_cost=rho[route(score[cal],th)].mean(),threshold=th,oracle_at_realised_cost=ceiling,n_fit=len(fit),n_cal=len(cal),n_eval=len(test)))
        print('Analysed',arch,flush=True)
    out=ROOT/'paper/data'
    pd.DataFrame(identity).to_csv(out/'complementarity.csv',index=False)
    pd.DataFrame(rows).to_csv(out/'oracle_audit.csv',index=False)
    pd.DataFrame(gate_rows).to_csv(out/'heldout_routing.csv',index=False)
    print('Saved',len(rows),'oracle rows and',len(gate_rows),'routing rows',flush=True)

if __name__=='__main__':main()
