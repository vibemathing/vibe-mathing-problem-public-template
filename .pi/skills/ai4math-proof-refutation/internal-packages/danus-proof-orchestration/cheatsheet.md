# Cheatsheet

## Route fast

| User need | Action |
|---|---|
| “What is true?” | fact graph only |
| “What has been tried?” | global memory + local memory (own worker only) |
| “What should workers do next?” | main-agent portfolio + elaboration + master guidance |
| “This lemma is stuck.” | counterexample → two direct attempts → obstacle/dead end → replan |
| “Can we use this partial lemma downstream?” | verify it first |
| “A known theorem looks similar.” | exact statement/definitions → proof mechanism → extra-hypothesis analysis |
| “Candidate proof is ready.” | self-contained `fact_submit` via worker |
| “Verifier rejected it.” | repair every error/gap; resubmit |
| “Need progress update.” | human-summary pipeline |
| “Need a paper.” | finalize target → curate subgraph → write → compile → audit/verify refs → revise → whole-paper math verify |

## Truth rules

- Local memory: private scratch.
- Global memory: shared awareness.
- Fact graph: established mathematics within Danus.
- Main: steer/revoke, no submit.
- Worker: prove/submit, no revoke.
- Verifier: judge, no shared writes.

## Timing defaults

- Main control beat: ~30 min while active.
- Macro route audit: ~4 h.
- Worker hard round timeout in supplied snapshot: 4 h.
- Consecutive worker failure limit in supplied snapshot: 5.

## Paper thresholds

- Closure ≥10 facts: curate `fact_ids`; do not send the whole closure.
- Whole-paper verifier: `must-fix` blocks; `ignorable` does not.
- Unset target: writer refuses.
- Unknown selected fact id: writer refuses.
- Compile/leak/degenerate revision: quarantine; preserve last clean artifact.

## Core CLI

```text
bin/danus list
bin/danus new <project>
bin/danus assign <project>/<worker> --task "..."
bin/danus start <project>
bin/danus status <project>
bin/danus stop <project> [--force]
bin/danus finalize <project> [--paper <id>] [<fact_id> ...]
```

## Required service

```text
bash scripts/services.sh up verify
bash scripts/services.sh status
bash scripts/doctor.sh
```

## Red flags

- global-memory claim used as predecessor;
- “standard/classical” load-bearing step with no precise source/derivation;
- conditional narrowing with no signed fact;
- paper target inferred instead of selected;
- full closure dumped into writer;
- bibliographic metadata promoted from memory;
- reader artifact contains fact ids/internal role machinery;
- “verified” described as formal proof-assistant certainty.

## Final self-check

Goal fixed? Route appropriate? Role authorized? Inputs complete? Facts live? Interfaces matched? Fragile lemma stress-tested? Downstream intermediates verified? Reader artifact leak-free? Citations confirmed? Compile clean? Whole-paper must-fix count zero? Limitations stated?
