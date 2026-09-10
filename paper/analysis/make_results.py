"""Build manuscript tables, vector figures, and numerical summary."""
from pathlib import Path
import sys,json
from decimal import Decimal, ROUND_HALF_UP
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scratch/deps'))
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=ROOT/'paper';D=P/'data';F=P/'figures';F.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#233342','text.color':'#233342','pdf.fonttype':42})
o=pd.read_csv(D/'oracle_audit.csv');g=pd.read_csv(D/'heldout_routing.csv');c=pd.read_csv(D/'complementarity.csv')
o['gap']=100*(o.oracle-o.cross);o['cross_adv']=100*(o.cross-o.confidence)
o['legacy_adv']=100*(o.legacy_cross-o.confidence)
o['solver_gain']=100*(o.oracle-o.legacy_oracle)
o['avoidable_slack']=o.oracle_cost-o.legacy_cost
o['cross_solver_change']=100*(o.cross-o.legacy_cross)
# Primary summaries: average six pairs within architecture, median over 15.
a=o.groupby(['arch','budget']).mean(numeric_only=True).reset_index()
rng=np.random.default_rng(808)
def interval(v):
    v=np.asarray(v); draws=rng.choice(v,(10000,len(v)),replace=True)
    return np.percentile(np.median(draws,axis=1),[2.5,97.5]).tolist()
summary=[]
for b,z in a.groupby('budget'):
    row={'budget':b,'n_arch':len(z)}
    for k in ['oracle','cross','confidence','gap','cross_adv','legacy_adv','solver_gain','avoidable_slack','cross_solver_change','oracle_cost','cross_cost','legacy_cost','matched_adv','confidence_matched_cost']:
        row[k]=float(z[k].median())
    row['cross_adv_interval']=interval(z.cross_adv)
    row['positive_architectures']=int((z.cross_adv>0).sum())
    row['matched_positive_architectures']=int((z.matched_adv>0).sum())
    row['matched_adv_interval']=interval(z.matched_adv)
    summary.append(row)
s=pd.DataFrame(summary);s.to_csv(D/'budget_summary.csv',index=False)
base=g[g.rule=='confidence'].set_index(['arch','target','budget'])
paired=[]
for r in g.itertuples():
    b=base.loc[(r.arch,r.target,r.budget)]
    paired.append(dict(arch=r.arch,source=r.source,target=r.target,budget=r.budget,rule=r.rule,kind='same' if r.source==r.target else 'transfer',gain=100*(r.accuracy-b.accuracy),cost_difference=r.cost-b.cost,accuracy=r.accuracy,cost=r.cost,overspend=r.cost-r.budget,headroom=100*(r.oracle_at_realised_cost-r.accuracy)))
p=pd.DataFrame(paired);p.to_csv(D/'routing_comparisons.csv',index=False)
ga=p.groupby(['arch','budget','rule','kind']).mean(numeric_only=True).reset_index()
gs=ga.groupby(['budget','rule','kind']).median(numeric_only=True).reset_index()
gs.to_csv(D/'gate_summary.csv',index=False)
gate_rng=np.random.default_rng(809)
gate_ci=[]
for key,z in ga[ga.budget==.8].groupby(['rule','kind']):
    ci=np.percentile(np.median(gate_rng.choice(z.gain.to_numpy(),(10000,len(z)),replace=True),axis=1),[2.5,97.5]).tolist()
    gate_ci.append(dict(rule=key[0],kind=key[1],gain=float(z.gain.median()),ci_low=ci[0],ci_high=ci[1]))
pd.DataFrame(gate_ci).to_csv(D/'gate_gain_intervals.csv',index=False)
e=pd.read_csv(D/'optimal_policy_envelope.csv');ea=e.groupby('arch').mean(numeric_only=True)
width=100*(ea.maximum_target_accuracy-ea.minimum_target_accuracy)
report={'aggregation':'mean seed pairs within architecture, median of 15 architecture means','budget':summary,'envelope':{'median_width':float(width.median()),'interval':interval(width),'min_arch_width':float(width.min()),'max_arch_width':float(width.max()),'lower_median':float(100*ea.minimum_target_accuracy.median()),'upper_median':float(100*ea.maximum_target_accuracy.median())},'complementarity':{'median_of_45':float(100*c.save.median()),'median_of_15_seed_means':float(100*c.groupby('arch').save.mean().median()),'min':float(100*c.save.min()),'max':float(100*c.save.max())},'gate_080':gs[gs.budget==.8].to_dict('records'),'max_oracle_gain':float(o.solver_gain.max()),'changed_oracle_rows':int((o.solver_gain>1e-8).sum()),'gate_budget_violation_count':int((g.cost>g.budget+.01).sum()),'gate_rows':len(g),'gate_max_overspend':float((g.cost-g.budget).max())}
(D/'summary.json').write_text(json.dumps(report,indent=2))

fig,ax=plt.subplots(1,2,figsize=(7,2.8),layout='constrained')
for k,label,color in [('oracle','Same-seed oracle','#126B7A'),('cross','Transferred oracle','#BE6A35'),('confidence','Confidence (transductive)','#4E5B68')]:
    ax[0].plot(s.budget,100*s[k],'-o',ms=3,label=label,color=color)
ax[0].set(xlabel='Normalized prefix budget',ylabel='Accuracy (%)');ax[0].legend(fontsize=7,frameon=False)
ax[1].axhline(0,c='#aab3ba',lw=1)
for arch,z in a.groupby('arch'):ax[1].plot(z.budget,z.cross_adv,c='#bdc9d2',lw=.6,alpha=.7)
ax[1].plot(s.budget,s.cross_adv,'-o',c='#BE6A35',ms=3,label='Median across architectures')
ax[1].plot(s.budget,s.matched_adv,'--s',c='#126B7A',ms=3,label='Matched realized cost')
ax[1].legend(fontsize=7,frameon=False)
ax[1].set(xlabel='Normalized prefix budget',ylabel='Transfer minus confidence (pp)')
fig.savefig(F/'budget_transfer.pdf');plt.close(fig)

fig,ax=plt.subplots(1,2,figsize=(7,2.8),layout='constrained')
ax[0].plot(s.budget,s.solver_gain,'-o',color='#126B7A',ms=3)
ax[0].set(xlabel='Normalized prefix budget',ylabel='Exact minus legacy oracle (pp)')
ax[1].plot(s.budget,s.cross_solver_change,'-o',color='#BE6A35',ms=3)
ax[1].axhline(0,c='#aab3ba',lw=1)
ax[1].set(xlabel='Normalized prefix budget',ylabel='Change in transferred accuracy (pp)')
fig.savefig(F/'solver_audit.pdf');plt.close(fig)

fig,ax=plt.subplots(1,2,figsize=(7,2.8),layout='constrained')
for rule,kind,label,color in [('margin','same','Margin','#4E5B68'),('logistic','same','Logistic, same seed','#126B7A'),('logistic','transfer','Logistic, transferred','#BE6A35')]:
    z=gs[(gs.rule==rule)&(gs.kind==kind)]
    ax[0].plot(z.budget,z.gain,'-o',label=label,c=color,ms=3)
    ax[1].plot(z.budget,z.cost_difference,'-o',c=color,ms=3)
for x in ax:x.axhline(0,c='#aab3ba',lw=1);x.set_xlabel('Calibration target budget')
ax[0].set_ylabel('Gain over confidence (pp)');ax[0].legend(fontsize=7,frameon=False)
ax[1].set_ylabel('Realized cost minus confidence')
fig.savefig(F/'heldout_routing.pdf');plt.close(fig)

fig,ax=plt.subplots(figsize=(7,3.4),layout='constrained')
order=c.groupby('arch').save.mean().sort_values().index
for i,arch in enumerate(order):
    z=c[c.arch==arch];ax.scatter(100*z.save,[i]*3,s=18,c='#126B7A',alpha=.75)
ax.set_yticks(range(len(order)),[x.replace('_',' ') for x in order],fontsize=7)
ax.set_xlabel('Any-correct-exit minus final-exit accuracy (pp)');ax.grid(axis='x',alpha=.2)
fig.savefig(F/'complementarity.pdf');plt.close(fig)

fig,ax=plt.subplots(figsize=(7,3.4),layout='constrained')
for i,(arch,z) in enumerate(ea.sort_values('canonical_target_accuracy').iterrows()):
    ax.plot(100*np.array([z.minimum_target_accuracy,z.maximum_target_accuracy]),[i,i],c='#94b9c1',lw=4,solid_capstyle='round')
    ax.scatter(100*z.canonical_target_accuracy,i,c='#BE6A35',s=22,zorder=3)
ax.set_yticks(range(len(ea)),[x.replace('_',' ') for x in ea.sort_values('canonical_target_accuracy').index],fontsize=7)
ax.set_xlabel('Target accuracy among source-optimal policies at budget 0.80 (%)')
ax.grid(axis='x',alpha=.2)
fig.savefig(F/'policy_envelope.pdf');plt.close(fig)

def write_table(name,rows):
    (P/name).write_text('\n'.join(' & '.join(row)+r' \\' for row in rows)+'\n')
def display(value,digits=2,signed=False):
    # Remove numerical roundoff far below display precision, then use one
    # explicit convention for decimal ties (14.195 -> 14.20).
    d=Decimal(str(round(float(value),10))).quantize(Decimal(1).scaleb(-digits),rounding=ROUND_HALF_UP)
    return ('+' if signed and d>=0 else '')+format(d,f'.{digits}f')
write_table('budget_rows.tex',[[display(r.budget),display(100*r.oracle),display(100*r.cross),display(r.cross_cost,3),display(r.cross_adv,signed=True),display(r.matched_adv,signed=True),str(r.positive_architectures),str(r.matched_positive_architectures)] for r in s.itertuples()])
atlas=pd.read_csv(D/'backbone_summary.csv').set_index('arch')
write_table('atlas_rows.tex',[[arch.replace('_',r'\_'),str(int(z.n_exits.iloc[0])),display(atlas.loc[arch,'params_M']),display(100*z.final.mean()),display(100*z['any'].mean()),display(100*z.save.mean())] for arch,z in c.groupby('arch')])
print(json.dumps(report,indent=2))
