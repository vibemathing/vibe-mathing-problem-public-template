# Cheatsheet

## Choose the model

| Situation | Model |
|---|---|
| finite qualitative control | transition system |
| guarded software/data | program graph → TS |
| shared variables | compose program graphs, then unfold |
| synchronous interaction | handshake / zero-capacity channel |
| buffered messages | FIFO channel system |
| dense real time | timed automaton |
| fixed stochastic branching | Markov chain |
| stochastic + scheduling/environment choice | MDP |

## Choose the property/check

| Requirement smell | Route |
|---|---|
| “can bad happen?” | reachability |
| “always state condition” | invariant |
| finite bad history | safety; regular → monitor product |
| eventual/repeated progress | liveness; inspect fairness |
| trace order | LTL → `not φ` NBA → product + NDFS |
| branching alternatives | CTL bottom-up fixed points |
| next-free internal-step abstraction | stutter relation / POR |
| time bound | TCTL → region TS |
| probability threshold | PCTL / reachability equations |
| MDP max/min probability | Bellman + VI/LP + scheduler |
| long-run probability | BSCC/MEC + deterministic ω-automaton |

## Fairness decision

- Continuously enabled but ignored → **weak fairness** candidate.
- Enabled infinitely often with gaps but ignored → **strong fairness** candidate.
- Must occur infinitely often regardless of enabledness premise → **unconditional fairness**.
- Before using any: prove/justify **realizability** and implementation enforceability.

## Reduction boundaries

| Reduction | Preserve |
|---|---|
| bisimulation quotient | broad CTL*/CTL branching behavior (chapter conditions) |
| simulation over-approximation | universal properties in the correct direction |
| stutter trace equivalence | LTL without `X` |
| divergence-sensitive stutter bisimulation | CTL*/CTL without `X` |
| POR A1–A4 | LTL without `X` |
| POR A1–A5 | next-free CTL*/CTL |
| clock regions | relevant timed propositions/TCTL reduction |
| probabilistic bisimulation | PCTL/PCTL* quantitative behavior |

## POR provisos

- **A1**: enabled ⇒ ample nonempty.
- **A2**: no dependent action may overtake the ample choice.
- **A3**: reduced ample actions are invisible.
- **A4**: reduced cycles cannot ignore enabled actions forever.
- **A5**: branching-time reduction uses singleton ample set.

## Failure smells

- Counterexample impossible in design → **model error**.
- Counterexample legal and undesirable → **design error**.
- Counterexample contradicts intended English but satisfies formula semantics → **property error**.
- Only unfair scheduling causes liveness failure → justify fairness; do not assume it.
- Model edit after green checks → rerun affected properties.
- BDD explosion → revisit variable order or reduction route.
- Region explosion → remove clocks/constants; isolate timed obligations.
- MDP result treats choices as averaged probabilities → modeling error: nondeterminism needs scheduler quantification.
- Probability threshold near numerical estimate → tighten/certify error before verdict.

## Defaults worth remembering

- Keep `AP` limited to observations needed by requirements.
- Use BFS for a shortest finite counterexample; DFS for lean reachability exploration.
- Generate products on the fly when possible.
- Avoid `X` if the requirement is truly stutter-insensitive.
- For MC reachability: graph-classify `0/1` states before solving equations.
- For MDP `P<=p`, check **max** probability; for `P>=p`, check **min** probability.
- For long-run stochastic behavior: think recurrent component first, path enumeration second.
