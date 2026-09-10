"""Create compact Overleaf and complete analysis/source packages."""
from pathlib import Path
import zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'paper';out=ROOT/'output';out.mkdir(exist_ok=True)
minimal=[P/'main.tex',P/'bibliography.bib',P/'atlas_rows.tex',P/'budget_rows.tex']+sorted((P/'figures').glob('*.pdf'))
with zipfile.ZipFile(out/'oracle_headroom_overleaf.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in minimal:z.write(p,p.relative_to(P))
    z.writestr('README.txt','Set main.tex as the main document. Compile with pdfLaTeX or XeLaTeX and BibTeX. Authors are intentionally empty. This archive contains the complete typesetting inputs. Scientific scope and reproducibility details are in the companion full package.\n')
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.published.source' not in p.name]
files += [p for p in (ROOT/'docs/evidence/hf_2026-09-07').rglob('*') if p.is_file()]
files += [ROOT/p for p in ['src/msc_lib.py','build_notebooks_study3.py','build_notebooks_study4.py','tools/verify_study4_evidence.py','PROJECT_UNDERSTANDING.md','PROGRESS.md','PAPER_CLAIM.md','output/pdf/main.pdf']]
records=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files]
with zipfile.ZipFile(out/'oracle_headroom_reproducibility.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,p.relative_to(ROOT))
    z.writestr('PACKAGE_MANIFEST.json',json.dumps(records,indent=2))
    z.writestr('README.txt','Start with paper/README.md. The compiled manuscript is output/pdf/main.pdf. Raw prediction files are retrieved from public revision-pinned URLs by paper/analysis/fetch_inputs.py. This package includes the current source paths relevant to the methodological audit; it is not a full training-repository snapshot. No original image datasets or backbone checkpoints are bundled.\n')
for name in ['oracle_headroom_overleaf.zip','oracle_headroom_reproducibility.zip']:
    with zipfile.ZipFile(out/name) as z:assert z.testzip() is None
    print(name,(out/name).stat().st_size,'bytes')
