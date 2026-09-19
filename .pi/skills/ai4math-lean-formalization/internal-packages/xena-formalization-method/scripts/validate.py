#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
errors=[]; warnings=[]

def words(p): return len(p.read_text(encoding='utf-8').split())
def tokens(p): return int(words(p)/0.75)

def err(x): errors.append(x)
def warn(x): warnings.append(x)

required=['SKILL.md','glossary.md','patterns.md','cheatsheet.md']
for r in required:
    if not (ROOT/r).is_file(): err(f'missing {r}')
chap=list((ROOT/'chapters').glob('*.md')) if (ROOT/'chapters').is_dir() else []
if not chap: err('no chapter files')

# Frontmatter
p=ROOT/'SKILL.md'
if p.exists():
    text=p.read_text(encoding='utf-8')
    m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
    if not m: err('SKILL.md missing YAML frontmatter')
    else:
        try: fm=yaml.safe_load(m.group(1))
        except Exception as e: err(f'bad YAML: {e}'); fm={}
        for k in ['name','description','when_to_use','allowed-tools','argument-hint']:
            if k not in fm: err(f'frontmatter missing {k}')
        if fm.get('name')!='xena-formalization-method': err('unexpected skill name')
        if fm.get('allowed-tools')!='Read Grep': err('allowed-tools must be Read Grep')
    if tokens(p)>4000: err(f'SKILL.md too large: ~{tokens(p)} tokens')

# Master target budgets; warn rather than fail at small deviations.
for c in chap:
    t=tokens(c)
    if t<800: err(f'{c.name} below master chapter target: ~{t} tokens')
    if t>1200: err(f'{c.name} above master chapter target: ~{t} tokens')
for fn,lim in [('glossary.md',1700),('patterns.md',2200),('cheatsheet.md',1200)]:
    q=ROOT/fn
    if q.exists() and tokens(q)>lim: err(f'{fn} too large: ~{tokens(q)} tokens')

# Internal markdown links.
for md in ROOT.rglob('*.md'):
    text=md.read_text(encoding='utf-8')
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
        if '://' in target or target.startswith('#'): continue
        target=target.split('#')[0]
        if not target: continue
        if not (md.parent/target).resolve().exists(): err(f'broken link {md.relative_to(ROOT)} -> {target}')

# Source coverage.
ledger=json.loads((ROOT/'references/reading-ledger.json').read_text(encoding='utf-8'))
if len(ledger)!=133: err(f'reading ledger count {len(ledger)} != 133')
ids=[x.get('id') for x in ledger]
expected=[f'u{i:03d}' for i in range(1,134)]
if ids!=expected: err('reading ledger IDs not exactly u001..u133')
if not all(x.get('processed') is True and x.get('status')=='read' for x in ledger): err('reading ledger has unprocessed units')
source_map=(ROOT/'references/source-map.md').read_text(encoding='utf-8')
for i in expected:
    if i not in source_map: err(f'source map missing {i}')

# Unfinished-marker audit. The word 'placeholder' is legitimate in discussions
# of staged assumptions, so only flag conventional unfinished markers/templates.
unfinished = re.compile(r'(?im)^\s*(?:[-*]\s*)?(TODO|TBD|FIXME)\b|<(?:insert|fill|todo|tbd)[^>]*>|\{\{(?:todo|tbd|insert|fill)[^}]*\}\}')
for path in ROOT.rglob('*'):
    if path.is_file() and path.suffix in {'.md','.json','.py'}:
        txt=path.read_text(encoding='utf-8',errors='ignore')
        if unfinished.search(txt): err(f'unfinished marker in {path.relative_to(ROOT)}')

# Eval shape.
ev=json.loads((ROOT/'evals/cases.json').read_text(encoding='utf-8'))
for k in ['positive_triggers','negative_triggers','method_selection','failure_recovery','fresh_agent_simulations']:
    if not ev.get(k): err(f'eval group empty: {k}')

# No source raw HTML/book dump inside skill.
for x in ROOT.rglob('*'):
    if x.is_file() and x.suffix.lower() in {'.html','.pdf','.epub'}: err(f'raw source unexpectedly packaged: {x.relative_to(ROOT)}')

print(f'root: {ROOT}')
print(f'chapters: {len(chap)}')
print(f'SKILL tokens approx: {tokens(ROOT/"SKILL.md")}')
for c in sorted(chap): print(f'  {c.name}: ~{tokens(c)} tokens')
print(f'errors: {len(errors)} warnings: {len(warnings)}')
for x in errors: print('ERROR:',x)
for x in warnings: print('WARN:',x)
sys.exit(1 if errors else 0)
