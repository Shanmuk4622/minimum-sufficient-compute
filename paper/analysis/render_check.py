"""Render every final PDF page and report text/layout checks."""
from pathlib import Path
import sys,json,re
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scratch/deps'))
import pymupdf as fitz
from PIL import Image,ImageOps,ImageDraw
pdf=ROOT/'output/pdf/main.pdf';doc=fitz.open(pdf)
out=ROOT/'scratch/paper_pdf';out.mkdir(parents=True,exist_ok=True)
pages=[]
for i,page in enumerate(doc):
    pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5));p=out/f'page-{i+1:02}.png';pix.save(p)
    text=page.get_text()
    for word in page.get_text('words'):
        assert word[0]>=0 and word[1]>=0 and word[2]<=page.rect.width+1 and word[3]<=page.rect.height+1,(i,word)
    pages.append(dict(page=i+1,words=len(text.split()),first=text[:130],last=text[-100:]))
    assert '??' not in text
for start in range(0,len(doc),6):
    sheet=Image.new('RGB',(1350,1960),'#dce3e7');draw=ImageDraw.Draw(sheet)
    for j in range(6):
        i=start+j
        if i>=len(doc):break
        im=Image.open(out/f'page-{i+1:02}.png');im.thumbnail((430,920))
        x=(j%3)*450+10;y=(j//3)*980+30
        sheet.paste(im,(x,y));draw.text((x,y-20),f'Page {i+1}',fill='black')
    sheet.save(out/f'contact-{start//6+1}.png')
(ROOT/'paper/PDF_CHECK.json').write_text(json.dumps({'pages':pages,'page_count':len(doc),'total_words_including_references':sum(x['words'] for x in pages),'no_unresolved_question_mark_references':True,'text_within_page_bounds':True},indent=2))
print('Pages',len(doc),'words',sum(x['words'] for x in pages));print(json.dumps(pages,indent=2,ensure_ascii=True))
