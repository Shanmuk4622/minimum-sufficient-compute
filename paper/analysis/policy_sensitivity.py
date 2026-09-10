"""Cost matching and selection sensitivity among source-optimal policies."""
from reanalyse import *
from scipy.sparse import kron,eye,csr_matrix,vstack
o=pd.read_csv(ROOT/'paper/data/oracle_audit.csv');cache={}
def table(a,s):
    key=(a,s)
    if key not in cache:
        d=pd.read_parquet(ROOT/f'msc_results/runs/p1-{a}-cifar100-base-s{s}/per_sample/test.parquet').sort_values('sample_idx')
        ks=sorted(int(x[6:]) for x in d if x.startswith('pred_d') and x[6:].isdigit())
        cache[key]=(np.stack([d[f'pred_d{k}'].to_numpy()==d.label.to_numpy() for k in ks],1),np.stack([d[f'top1p_d{k}'] for k in ks],1))
    return cache[key]
def envelope(source,target,rho,b):
    opt,_=exact_oracle(source,source,rho,b)
    patterns,count=np.unique(np.column_stack([source,target]),axis=0,return_counts=True)
    K=len(rho);G=len(count);w=count/count.sum()
    sc=patterns[:,:K];tc=patterns[:,K:]
    eq=vstack([kron(eye(G),np.ones((1,K))),csr_matrix((sc*w[:,None]).ravel()[None,:])],format='csr')
    beq=np.r_[np.ones(G),opt]
    cost=csr_matrix((np.tile(rho,(G,1))*w[:,None]).ravel()[None,:])
    objective=(tc*w[:,None]).ravel()
    vals=[]
    for sign in [1,-1]:
        r=linprog(sign*objective,A_ub=cost,b_ub=[b],A_eq=eq,b_eq=beq,bounds=(0,1),method='highs')
        assert r.success,r.message
        assert abs((sc*w[:,None]).ravel()@r.x-opt)<1e-7
        vals.append(float(objective@r.x))
    return vals
rows=[];matched=[]
for r in o.itertuples():
    rho=np.array(json.loads((ROOT/f'msc_results/budgets/{r.arch}.json').read_text())['axes']['depth']['rho'])
    c,p=table(r.arch,r.target);cs,_=table(r.arch,r.source)
    th=calibrate(p,rho,r.cross_cost);k=route(p,th)
    matched.append((c[np.arange(10000),k].mean(),rho[k].mean()))
    if r.budget==.8:
        low,high=envelope(cs,c,rho,.8)
        assert low-1e-7<=r.cross<=high+1e-7
        rows.append(dict(arch=r.arch,source=r.source,target=r.target,budget=.8,minimum_target_accuracy=low,maximum_target_accuracy=high,canonical_target_accuracy=r.cross,canonical_cost=r.cross_cost))
o['confidence_matched_cost']=[x[0] for x in matched];o['confidence_matched_realised_cost']=[x[1] for x in matched]
o['matched_adv']=100*(o.cross-o.confidence_matched_cost)
o.to_csv(ROOT/'paper/data/oracle_audit.csv',index=False)
e=pd.DataFrame(rows);e.to_csv(ROOT/'paper/data/optimal_policy_envelope.csv',index=False)
a=e.groupby('arch').mean(numeric_only=True)
print('Median source-optimal transfer lower/upper/canonical:',100*a[['minimum_target_accuracy','maximum_target_accuracy','canonical_target_accuracy']].median())
print('Median interval width:',100*(a.maximum_target_accuracy-a.minimum_target_accuracy).median())
print('Matched-cost transfer advantage:',o.groupby(['arch','budget']).matched_adv.mean().groupby('budget').median())
print('Largest matched-cost discrepancy:',(o.cross_cost-o.confidence_matched_realised_cost).max())
