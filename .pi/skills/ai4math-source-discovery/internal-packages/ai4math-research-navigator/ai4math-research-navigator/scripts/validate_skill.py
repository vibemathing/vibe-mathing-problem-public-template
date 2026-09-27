#!/usr/bin/env python3
import json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
required=[
 'SKILL.md','metadata.json','manifest.txt','README.md',
 'references/source-record.md','references/book-map.md','references/concept-graph.md',
 'references/method-dependency-graph.md','references/taxonomy-routing.md',
 'references/capability-library.md','references/benchmark-guide.md','references/failure-modes.md',
 'references/visual-findings.md','references/catalog.jsonl','provenance/provenance_map.json',
 'workflows/research-navigation.md','workflows/system-design.md','workflows/evaluation-design.md',
 'workflows/formal-proving.md','workflows/multimodal-geometry.md','workflows/discovery.md','workflows/recovery.md',
 'templates/research-plan.md','templates/benchmark-card.md','templates/method-comparison.md',
 'tests/evals.json','tests/eval-results.md','tests/coverage-audit.md','tests/fresh-agent-simulation.md','tests/independent-audit.md','tests/quality-scores.json',
 'licenses/source-MIT.txt'
]
errors=[]
for rel in required:
    if not (ROOT/rel).is_file(): errors.append(f'missing {rel}')

skill=(ROOT/'SKILL.md').read_text(encoding='utf-8') if (ROOT/'SKILL.md').exists() else ''
if not re.match(r'^---\nname: [a-z0-9-]+\ndescription: .+?\n---\n', skill, re.S): errors.append('invalid SKILL.md frontmatter')
for marker in ['SELF_CHECK','Failure recovery','Progressive loading','Output contract']:
    if marker not in skill: errors.append(f'SKILL.md missing marker: {marker}')

manifest=(ROOT/'manifest.txt').read_text(encoding='utf-8').splitlines() if (ROOT/'manifest.txt').exists() else []
actual=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='manifest.txt')
listed=sorted(x for x in manifest if x and x!='manifest.txt')
if listed!=actual: errors.append('manifest does not match file set')


# Referenced package paths in SKILL.md must exist.
for rel in sorted(set(re.findall(r'`((?:references|workflows|scripts|provenance|templates|tests)/[^`]+)`', skill))):
    if not (ROOT/rel).exists(): errors.append(f'broken internal reference: {rel}')

# No unfinished placeholders.
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in {'.md','.json','.txt','.py'}:
        txt=p.read_text(encoding='utf-8', errors='ignore')
        banned=['TO'+'DO','TB'+'D','PLACE'+'HOLDER']
        if any(re.search(r'\b'+re.escape(term)+r'\b', txt) for term in banned): errors.append(f'unfinished marker in {p.relative_to(ROOT)}')

# Catalog must be parseable and non-trivial.
catalog=ROOT/'references/catalog.jsonl'
if catalog.exists():
    n=0
    for line in catalog.read_text(encoding='utf-8').splitlines(): json.loads(line); n+=1
    if n < 200: errors.append(f'catalog unexpectedly small: {n}')

# Eval suite parse and coverage.
ev=ROOT/'tests/evals.json'
if ev.exists():
    data=json.loads(ev.read_text(encoding='utf-8'))
    if len(data.get('cases',[])) < 10: errors.append('too few eval cases')
    cats={c.get('test_type') for c in data.get('cases',[])}
    for needed in {'trigger','negative_trigger','method_selection','failure_recovery','freshness'}:
        if needed not in cats: errors.append(f'missing eval category {needed}')

if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-',e)
    sys.exit(1)
print('VALIDATION PASSED')
print(f'files: {len(actual)+1}')
print('catalog_records:', sum(1 for _ in catalog.open(encoding="utf-8")))
