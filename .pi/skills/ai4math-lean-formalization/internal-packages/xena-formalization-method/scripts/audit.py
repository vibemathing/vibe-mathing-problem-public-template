#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
errs=[]; notes=[]

def fail(x): errs.append(x)
# Capability ↔ provenance consistency.
cap=(ROOT/'references/capability-library.md').read_text(encoding='utf-8')
prov=(ROOT/'references/provenance.md').read_text(encoding='utf-8')
cap_names=re.findall(r'^## ([a-z0-9][a-z0-9-]+)\s*$',cap,re.M)
prov_names=re.findall(r'^- \*\*([a-z0-9][a-z0-9-]+)\*\* —',prov,re.M)
if len(cap_names)!=36: fail(f'expected 36 capabilities, got {len(cap_names)}')
if set(cap_names)!=set(prov_names):
    fail(f'capability/provenance mismatch: only_cap={sorted(set(cap_names)-set(prov_names))}, only_prov={sorted(set(prov_names)-set(cap_names))}')
# Validate every uNNN reference/range in provenance against the frozen source IDs.
valid=set(range(1,134))
for a,b in re.findall(r'u(\d{3})(?:-u?(\d{3}))?',prov):
    lo=int(a); hi=int(b) if b else lo
    if lo>hi or any(i not in valid for i in range(lo,hi+1)):
        fail(f'invalid provenance source range u{lo:03d}-u{hi:03d}')
# Master chapter shape + naming + budgets and uniqueness.
chapters=sorted((ROOT/'chapters').glob('*.md'))
if len(chapters)!=14: fail(f'expected 14 thematic chapters, got {len(chapters)}')
for p in chapters:
    if not re.match(r'ch\d{2}-[a-z0-9-]+\.md$',p.name): fail(f'bad chapter filename: {p.name}')
    txt=p.read_text(encoding='utf-8')
    for h in ['## Core Idea','## Anti-patterns','## Validation Checkpoint','## Key Takeaways','## Connects To']:
        if h not in txt: fail(f'{p.name} missing {h}')
    tok=int(len(txt.split())/.75)
    if not 800<=tok<=1200: fail(f'{p.name} outside 800-1200 approx tokens: {tok}')
# Check chapter text is not duplicated by crude 5-word shingle Jaccard.
def shingles(text,n=5):
    w=re.findall(r"[A-Za-z0-9_`'-]+",text.lower())
    return {' '.join(w[i:i+n]) for i in range(max(0,len(w)-n+1))}
sets={p.name:shingles(p.read_text(encoding='utf-8')) for p in chapters}
max_pair=(None,None,0.0)
for i,a in enumerate(chapters):
    for b in chapters[i+1:]:
        A,B=sets[a.name],sets[b.name]
        j=len(A&B)/max(1,len(A|B))
        if j>max_pair[2]: max_pair=(a.name,b.name,j)
        if j>0.18: fail(f'suspicious chapter duplication {a.name} vs {b.name}: {j:.3f}')
notes.append(f'max chapter 5-shingle Jaccard={max_pair[2]:.3f} ({max_pair[0]} vs {max_pair[1]})')
# Frozen reading record.
ledger=json.loads((ROOT/'references/reading-ledger.json').read_text(encoding='utf-8'))
if sum(1 for x in ledger if x.get('processed') is True and x.get('status')=='read') != 133:
    fail('not all 133 source units are marked read/processed')
# Coverage by expected skill themes.
themes={
    'statement semantics':['statement','quantifier','semantics'],
    'proof-state workflow':['proof state','intro','exact'],
    'equality':['definitional equality','extensionality','rewrite'],
    'API engineering':['extensionality','coercion','typeclass'],
    'representation/computability':['computability','choice','representation'],
    'trust/reflection':['reflection','kernel','certificate'],
    'research architecture':['dependency graph','staged assumptions','library'],
    'AI audit':['autoformalization','semantic audit','misformalization'],
    'counterexamples':['counterexample','witness','digest'],
}
alltext='\n'.join([ (ROOT/'SKILL.md').read_text(encoding='utf-8'), cap, (ROOT/'patterns.md').read_text(encoding='utf-8') ]+[p.read_text(encoding='utf-8') for p in chapters]).lower()
for theme,terms in themes.items():
    missing=[t for t in terms if t.lower() not in alltext]
    if missing: fail(f'coverage theme {theme} missing terms {missing}')
# No giant source-like dump.
mds=list(ROOT.rglob('*.md'))
max_words=max((len(p.read_text(encoding='utf-8').split()),p.relative_to(ROOT)) for p in mds)
notes.append(f'largest markdown={max_words[1]} words={max_words[0]}')
notes.append(f'capabilities={len(cap_names)} provenance_entries={len(prov_names)} chapters={len(chapters)}')
print('AUDIT', 'PASS' if not errs else 'FAIL')
for n in notes: print('NOTE:',n)
for e in errs: print('ERROR:',e)
sys.exit(1 if errs else 0)
