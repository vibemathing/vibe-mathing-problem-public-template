#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

def tokens(s):
    return [t for t in re.findall(r"[A-Za-z0-9+_.-]+", s.lower()) if len(t) > 1]

def text_of(r):
    parts=[str(r.get(k,'')) for k in ('title','note','section','subsection','link_text','url')]
    parts += [str(v) for v in r.get('fields',{}).values()]
    return ' '.join(parts).lower()

def main():
    ap=argparse.ArgumentParser(description='Search the bundled AI4Math source catalog.')
    ap.add_argument('--query', required=True)
    ap.add_argument('--section')
    ap.add_argument('--year', type=int)
    ap.add_argument('--limit', type=int, default=10)
    args=ap.parse_args()
    path=Path(__file__).resolve().parents[1]/'references'/'catalog.jsonl'
    qs=tokens(args.query)
    scored=[]
    for line in path.read_text(encoding='utf-8').splitlines():
        r=json.loads(line); hay=text_of(r)
        if args.section and args.section.lower() not in str(r.get('section','')).lower(): continue
        if args.year and r.get('year') != args.year and str(args.year) not in hay: continue
        score=sum(3 for q in qs if q in str(r.get('title','')).lower()) + sum(1 for q in qs if q in hay)
        if score: scored.append((score, r))
    scored.sort(key=lambda x:(-x[0], x[1].get('source_line',10**9)))
    for score,r in scored[:args.limit]:
        title=r.get('title') or r.get('fields',{}).get('Dataset') or r.get('fields',{}).get('Benchmark') or r.get('fields',{}).get('Authors') or '[table row]'
        print(f"[{score}] {title}")
        print(f"  section: {r.get('section','')} / {r.get('subsection','')} | source line {r.get('source_line')}")
        if r.get('url'): print(f"  url: {r['url']}")
        if r.get('note'): print(f"  note: {r['note']}")
        if r.get('fields'): print('  fields: '+json.dumps(r['fields'], ensure_ascii=False))

if __name__=='__main__': main()
