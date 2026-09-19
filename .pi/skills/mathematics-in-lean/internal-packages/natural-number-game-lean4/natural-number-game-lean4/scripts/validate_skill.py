#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, zipfile, tempfile, shutil

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ['SKILL.md','glossary.md','patterns.md','cheatsheet.md']
CHAPTERS = [f'chapters/ch{i:02d}-' for i in range(1,10)]
errors=[]; warnings=[]

def words_to_tokens(text): return round(len(text.split())/0.75)

for rel in REQUIRED:
    if not (ROOT/rel).is_file(): errors.append(f'missing {rel}')

# Front matter and required keys
skill=(ROOT/'SKILL.md').read_text(encoding='utf-8') if (ROOT/'SKILL.md').exists() else ''
m=re.match(r'^---\n(.*?)\n---\n',skill,re.S)
if not m: errors.append('SKILL.md missing YAML frontmatter')
else:
    fm=m.group(1)
    for key in ['name','description','when_to_use','allowed-tools','argument-hint']:
        if not re.search(rf'^{re.escape(key)}:\s*\S+',fm,re.M): errors.append(f'frontmatter missing {key}')
    if not re.search(r'^name:\s*natural-number-game-lean4\s*$',fm,re.M): errors.append('unexpected skill name')
    wt=re.search(r'^when_to_use:\s*(.+)$',fm,re.M)
    if wt:
        triggers=[x.strip() for x in wt.group(1).split(',') if x.strip()]
        if not (10 <= len(triggers) <= 15): errors.append(f'when_to_use trigger count {len(triggers)} outside 10-15')

body=skill[m.end():] if m else skill
if words_to_tokens(body) >= 4000: errors.append(f'SKILL.md body token estimate too high: {words_to_tokens(body)}')

for i,prefix in enumerate(CHAPTERS,1):
    hits=[p for p in ROOT.glob(prefix.split('/')[-1]+'*.md')] if False else list((ROOT/'chapters').glob(f'ch{i:02d}-*.md'))
    if len(hits)!=1: errors.append(f'chapter {i:02d} count={len(hits)}')
    elif not (800 <= words_to_tokens(hits[0].read_text(encoding='utf-8')) <= 1200):
        errors.append(f'{hits[0].name} estimated tokens {words_to_tokens(hits[0].read_text(encoding="utf-8"))} outside required 800-1200 band')

for rel,limit in [('glossary.md',1500),('patterns.md',2000),('cheatsheet.md',1000)]:
    if (ROOT/rel).exists():
        t=words_to_tokens((ROOT/rel).read_text(encoding='utf-8'))
        if t>limit: errors.append(f'{rel} token estimate {t} > {limit}')

# Relative markdown links must resolve, skipping anchors/URLs.
for p in ROOT.rglob('*.md'):
    txt=p.read_text(encoding='utf-8')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',txt):
        if target.startswith(('http://','https://','#','mailto:')): continue
        target=target.split('#',1)[0]
        if not target: continue
        if not (p.parent/target).resolve().exists(): errors.append(f'broken link {p.relative_to(ROOT)} -> {target}')

# Placeholder audit
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in {'.md','.json','.py'}:
        txt=p.read_text(encoding='utf-8')
        markers=['<'+'Full Title>','<'+'Author','<'+'generate ','TBD'+'_PLACEHOLDER','TODO'+'_PLACEHOLDER']
        for marker in markers:
            if marker in txt: errors.append(f'placeholder {marker!r} in {p.relative_to(ROOT)}')

# Required master sections and package hygiene
for heading in ['## How to Use This Skill','## Core Frameworks & Mental Models','## Chapter Index','## Topic Index','## Supporting Files','## Scope & Limits','## SELF_CHECK']:
    if heading not in skill: errors.append(f'missing master section {heading}')
for p in ROOT.rglob('*'):
    if p.is_file() and (p.name in {'.DS_Store'} or p.suffix in {'.pyc','.tmp'} or p.name.endswith('~')):
        errors.append(f'junk file {p.relative_to(ROOT)}')

# Eval schema / breadth
evalp=ROOT/'tests/evals.json'
if not evalp.exists(): errors.append('missing tests/evals.json')
else:
    e=json.loads(evalp.read_text(encoding='utf-8'))
    for key,minn in [('trigger_positive',5),('trigger_negative',4),('method_selection',5),('failure_recovery',4)]:
        if len(e.get(key,[]))<minn: errors.append(f'evals {key} too small')

# Coverage/provenance required by this compiled skill architecture.
for rel in ['references/foundations.md','references/tactic-semantics.md','references/theorem-inventory.md','references/provenance.md','references/coverage.md','workflows/proof-routing.md','workflows/failure-recovery.md']:
    if not (ROOT/rel).is_file(): errors.append(f'missing supporting file {rel}')

print(f'ROOT={ROOT}')
print(f'SKILL_BODY_EST_TOKENS={words_to_tokens(body)}')
for rel in REQUIRED[1:]:
    if (ROOT/rel).exists(): print(f'{rel}_EST_TOKENS={words_to_tokens((ROOT/rel).read_text(encoding="utf-8"))}')
print(f'MD_FILES={len(list(ROOT.rglob("*.md")))}')
if warnings:
    print('WARNINGS:')
    for x in warnings: print(' -',x)
if errors:
    print('ERRORS:')
    for x in errors: print(' -',x)
    sys.exit(1)
print('VALIDATION_OK')
