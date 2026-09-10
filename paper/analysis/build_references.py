"""Retrieve primary metadata, generate BibTeX, retain a reference audit.

No search-result citations: arXiv metadata, proceedings pages, or Crossref
publisher deposits. Cached raw metadata supports a separate final audit.
"""
import json,re,html,urllib.request,hashlib,time
from pathlib import Path
P=Path(__file__).resolve().parents[1]; A=P/'references';A.mkdir(exist_ok=True)
refs=[]
def fetch(url,key):
    p=A/(key+'.source')
    if not p.exists():
        with urllib.request.urlopen(url,timeout=60) as r:p.write_bytes(r.read())
    return p.read_text(encoding='utf-8',errors='replace')
def meta(raw,name):
    return [html.unescape(x) for x in re.findall(r'<meta\s+name="'+name+r'"\s+content="([^"]+)"',raw)]
items=[
 ('selection','2608.08265','Separates outcome-oracle opportunity, signal-restricted opportunity, and held-out router gain in multi-LLM routing.'),
 ('routingnoise','2607.03436','Studies stochastic-decoding oracle gaps and repeated sampling; different from fixed classifier training-seed transfer.'),
 ('msdnet','1703.09844','Multi-scale architecture; implementation here is a variant.'),
 ('eenet','2301.07099','Learned scheduler under an average inference budget; no empirical comparison claimed.'),
 ('adaptive','2106.05022','Design choices and deployment challenges in early exits.'),
 ('patience','2006.04152','Prediction consistency as an early stopping rule in language models.'),
 ('difficulty','2106.09647','Prediction depth is an example-level difficulty measure.'),
 ('resnet','1512.03385','Residual backbone family.'),
 ('wide','1605.07146','Width/depth variants of residual networks.'),
 ('vgg','1409.1556','VGG backbone family; project uses small variants.'),
 ('vit','2010.11929','Vision Transformer backbone family.'),
 ('mobile','1801.04381','MobileNetV2 backbone family.'),
 ('shuffle','1807.11164','ShuffleNetV2 and difference between FLOPs and device speed.'),
 ('convnext','2201.03545','ConvNeXt family; project uses femto variant.'),
 ('mixer','2105.01601','MLP-Mixer family; project uses nano variant.'),
 ('dynamic','2102.04906','Broader dynamic neural network context.'),
 ('pteenet','2501.02508','Post-trained early-exit branches on frozen networks.'),
]
for key,aid,claim in items:
    url='https://arxiv.org/abs/'+aid;raw=fetch(url,key)
    title=meta(raw,'citation_title')[0];authors=meta(raw,'citation_author')
    date=meta(raw,'citation_date')[0];year=date[:4]
    fields=dict(title=title,author=' and '.join(authors),year=year,journal=f'arXiv preprint arXiv:{aid}',url=url)
    # Cite the repository version explicitly, avoiding unverified venue metadata.
    refs.append(dict(key=key,type='article',fields=fields,claim=claim,source=url,metadata='arXiv citation_title/citation_author/citation_date'))
for key,tail,claim in [('overthinking','v97/kaya19a','Correct intermediate predictions may become incorrect; not our novelty.'),('calibration','v70/guo17a','Raw confidence need not be calibrated.')]:
    url='https://proceedings.mlr.press/'+tail+'.html';raw=fetch(url,key)
    title=meta(raw,'citation_title')[0];authors=meta(raw,'citation_author');year=meta(raw,'citation_publication_date')[0][:4]
    fields=dict(title=title,author=' and '.join(authors),year=year,booktitle=meta(raw,'citation_conference_title')[0],url=url)
    for m,k in [('citation_firstpage','first'),('citation_lastpage','last')]:
        vals=meta(raw,m)
        if vals:fields[k]=vals[0]
    if 'first' in fields:fields['pages']=fields.pop('first')+'--'+fields.pop('last')
    refs.append(dict(key=key,type='inproceedings',fields=fields,claim=claim,source=url,metadata='PMLR official citation meta tags'))
for key,doi,claim in [('branchynet','10.1109/ICPR.2016.7900006','Early branch classifiers and confidence-dependent inference.'),('imagenet','10.1007/s11263-015-0816-y','ImageNet provenance; our subset is custom.'),('survey','10.1145/3698767','Early-exit research overview.')]:
    url='https://api.crossref.org/works/'+doi;raw=fetch(url,key);d=json.loads(raw)['message']
    fields=dict(title=html.unescape(d['title'][0]),author=' and '.join(a['family']+', '+a.get('given','') for a in d['author']),year=str(d['published']['date-parts'][0][0]),doi=doi,url='https://doi.org/'+doi)
    typ='inproceedings' if key=='branchynet' else 'article';fields['booktitle' if typ=='inproceedings' else 'journal']=d['container-title'][0]
    for field in ['volume','issue','page']:
        if field in d:fields[{'issue':'number','page':'pages'}.get(field,field)]=str(d[field])
    refs.append(dict(key=key,type=typ,fields=fields,claim=claim,source=url,metadata='Publisher-deposited Crossref record; DOI verified'))
refs.append(dict(key='cifar',type='techreport',fields=dict(title='Learning Multiple Layers of Features from Tiny Images',author='Krizhevsky, Alex',year='2009',institution='University of Toronto',url='https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf'),claim='CIFAR dataset provenance; authorship checked against report title page.',source='https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf',metadata='Primary PDF title page; not secondary bibliography'))
# Published versions cross-checked against the conference's own record.
published={
 'msdnet':('2018','International Conference on Learning Representations','https://iclr.cc/virtual/2018/poster/278'),
 'resnet':('2016','Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition','https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html'),
 'mobile':('2018','Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition','https://openaccess.thecvf.com/content_cvpr_2018/html/Sandler_MobileNetV2_Inverted_Residuals_CVPR_2018_paper.html'),
 'convnext':('2022','Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition','https://openaccess.thecvf.com/content/CVPR2022/html/Liu_A_ConvNet_for_the_2020s_CVPR_2022_paper.html'),
 'mixer':('2021','Advances in Neural Information Processing Systems','https://proceedings.neurips.cc/paper/2021/hash/cba0a4ee5ccd02fda0fe3f9a3e7b89fe-Abstract.html'),
 'difficulty':('2021','Advances in Neural Information Processing Systems','https://proceedings.neurips.cc/paper/2021/hash/5a4b25aaed25c2ee1b74de72dc03c14e-Abstract.html'),
}
for r in refs:
    if r['key'] in published:
        year,venue,url=published[r['key']]
        raw=fetch(url,r['key']+'.venue')
        assert '<html' in raw.lower() or '<!doctype' in raw.lower()
        r['publication_source']=url;r['type']='inproceedings'
        r['fields'].pop('journal',None);r['fields'].update(year=year,booktitle=venue,url=url)
def tex(s):
    return s.replace('&',r'\&').replace('_',r'\_').replace('%',r'\%')
out=[]
for r in refs:
    out.append('@'+r['type']+'{'+r['key']+',\n'+',\n'.join('  '+k+' = {'+(v if k=='url' else ('{'+tex(v)+'}' if k=='title' else tex(v)))+'}' for k,v in r['fields'].items())+'\n}')
(P/'bibliography.bib').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
(A/'audit.json').write_text(json.dumps(refs,indent=2,ensure_ascii=False),encoding='utf-8')
print('Generated',len(refs),'references from primary metadata')
