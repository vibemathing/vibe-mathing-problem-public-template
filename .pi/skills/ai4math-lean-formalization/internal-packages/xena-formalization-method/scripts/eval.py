#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/'evals/cases.json').read_text(encoding='utf-8'))
files={p.name:p.read_text(encoding='utf-8').lower() for p in (ROOT/'chapters').glob('*.md')}
skill=(ROOT/'SKILL.md').read_text(encoding='utf-8').lower()
route_files={
 '04 equality':'ch04-equality-rewriting-and-normalization.md',
 '06 definition/API':'ch06-definition-api-and-library-engineering.md',
 '10 research blueprint':'ch10-research-blueprints-and-library-growth.md',
 '12 AI audit':'ch12-ai-autoformalization-and-semantic-audit.md',
 '13 counterexample':'ch13-counterexamples-benchmarks-and-proof-digestion.md',
 '07 Prop-to-data':'ch07-representation-specification-and-computation.md',
}
# Accept compact synonym sets for terms whose exact wording differs.
alias={
 'syntactic':['syntactic'], 'definitional':['definitional'], 'normalization':['normalization','normalize'],
 'generality':['generality'], 'extensionality':['extensionality'], 'instances':['instances','typeclass'], 'client proofs':['client proofs','downstream proofs'],
 'statement':['statement'], 'dependency graph':['dependency graph'], 'library gaps':['missing reusable','library'], 'parallel':['parallel'],
 'statement semantics':['statement','semantic'], 'definitions':['definition'], 'type-check proof':['type-check','compile','kernel'],
 'formalize negation':['negation','formalize'], 'verify witness':['verify','witness'], 'digest':['digest'],
 'prop':['prop'], 'choice':['choice'], 'data':['data'], 'computability':['computability','noncomputable'],
}
errs=[]
for c in cases['positive_triggers']:
    fn=route_files.get(c['expect_route'])
    if not fn or fn not in files:
        errs.append(f"missing route file for {c['expect_route']}")
        continue
    corpus=(skill+'\n'+files[fn])
    for term in c['must']:
        opts=alias.get(term.lower(),[term.lower()])
        if not any(o in corpus for o in opts):
            errs.append(f"positive route {c['expect_route']} missing concept {term}")
# Negative-trigger guardrails must be explicit enough to reject ordinary math/general programming/unrelated tasks.
for phrase in ['ordinary mathematical answer','pure lean software engineering','formalization']:
    if phrase not in skill: errs.append(f'negative trigger guardrail missing {phrase}')
# Failure-recovery anchors.
recovery=(files['ch14-failure-recovery-version-drift-and-self-check.md']+'\n'+skill)
for phrase in ['syntax','statement','equality','representation','api','generality','missing']:
    if phrase not in recovery: errs.append(f'recovery ladder missing {phrase}')
print('EVAL STATIC', 'PASS' if not errs else 'FAIL')
print('positive_triggers',len(cases['positive_triggers']))
print('negative_triggers',len(cases['negative_triggers']))
print('method_selection',len(cases['method_selection']))
print('failure_recovery',len(cases['failure_recovery']))
print('fresh_agent_simulations',len(cases['fresh_agent_simulations']))
for e in errs: print('ERROR:',e)
sys.exit(1 if errs else 0)
