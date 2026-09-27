# Chapter 5: AI for Constructing Counterexamples

## Core Idea
Counterexample construction is an unusually good fit for AI search: the space of candidate objects may be enormous, yet candidate validity and degree of conjecture violation can often be scored automatically. The chapter develops three increasingly structured approaches: deep cross-entropy/RL search, PatternBoost's local–global loop, and LLM agents with independent verifiers.

## Frameworks Introduced

### Counterexample Search as an RL/Optimization Problem
- **When to use**: A conjecture concerns finite/discrete objects and violation can be measured or checked.
- **How**:
  1. **Agent**: constructs an object incrementally.
  2. **State**: partial construction.
  3. **Action**: add/change the next component.
  4. **Environment**: constraint logic and evaluator.
  5. **Reward**: numerical measure of conjecture violation or extremal quality.
  6. Search until a candidate crosses the refutation threshold, then verify it independently.
- **Representation example**: serialize the upper-triangular adjacency matrix of a graph as a binary action sequence.
- **Failure mode**: a reward that is merely correlated with violation can produce high-scoring invalid objects. Put hard mathematical constraints into the evaluator or repair stage.

### Deep Cross-Entropy Method (CEM)
- **When to use**: Construction is a discrete sequence with fast evaluation and enough successful/near-successful elite samples to imitate.
- **How**:
  1. Sample `N` complete candidates from policy `πθ`.
  2. Compute reward for each.
  3. Keep `K = ceil(ρN)` best candidates; the book describes typical elite retention around 5–20%.
  4. Turn each elite trajectory into state–action training pairs.
  5. Update the policy by minimizing negative log-probability/cross-entropy on elite actions.
  6. Repeat until a counterexample is found or the search budget ends.
- **Encoding detail**: for binary sequences, combine the partially filled decision vector with an explicit one-hot position indicator so the network knows both history and current decision position.
- **Why it works**: each generation tilts the proposal distribution toward structural decisions repeatedly present in high-reward objects.

### PatternBoost
- **When to use**: High-quality constructions possess learnable global patterns while a local search procedure can repair constraints and improve candidates.
- **How**:
  1. Start from seeds and apply **local search** to produce feasible strong constructions.
  2. Serialize elite constructions into token sequences.
  3. Train an autoregressive Transformer on the elite set to learn long-range/global structural patterns.
  4. Sample fresh candidates from the Transformer.
  5. Run those candidates through local repair/improvement and exact scoring.
  6. Insert new elites into the dataset and repeat.
- **Why it works**: local search exploits a basin; the learned generator can jump between basins by modeling whole-object patterns.
- **Boundary**: it works best when strong objects share implicit regularities. Highly random optima or weak local search reduce its value.

### Generator–Verifier LLM Agent
- **When to use**: The construction needs flexible mathematical reasoning, coding, retrieval, or adaptive decomposition that is awkward to encode as a fixed action space.
- **How**:
  1. **Core engine layer**: LLM generates candidate ideas/objects.
  2. **Agent layer**: plans, decomposes, records failed attempts, and chooses tools.
  3. **Application layer**: translates “refute conjecture X” into executable subtasks and a final verified object.
  4. Every proposal goes to an independent verifier: formal prover, exact checker, CAS, exhaustive program, or expert review.
  5. Verifier failure returns actionable diagnostics; the agent repairs or changes strategy.
  6. Final output passes whole-object verification, not merely local checks.
- **Why it works**: generative flexibility is retained while epistemic authority resides in a stricter checker.

## Key Concepts

### Near-miss structure as mathematical evidence
The chapter's graph-construction examples show that AI may repeatedly converge on recognizable motifs before finding a literal counterexample. In one case, the search highlighted a structure involving path/star/clique-like components; human researchers parameterized the family and were able to reason about much larger instances where the conjecture finally failed.

Operational rule: **if elite candidates stabilize structurally, inspect the family rather than declaring the search failed**. A stable motif can reveal the correct parameterization of the extremal regime.

### Human seed → machine generalization
PatternBoost can benefit strongly from a small number of high-value human constructions. Good seeds initialize the data distribution; repeated generate–repair–select cycles then explore variants at scale. Human insight and machine search are complementary inputs to the same loop.

### PatternBoost counterexample case
The book discusses a long-standing conjecture about the minimum number of edges in a spanning subgraph of a `d`-dimensional hypercube with diameter `d`. For `d=6`, PatternBoost finds an 81-edge construction where the conjectured family used 82, providing a counterexample. The transferable lesson is that a one-unit objective improvement can cross a logical threshold from “better optimization” to “refutation.”

### Anderson-conjecture agent case
The cited AI4Math case is used to demonstrate the generator–verifier division: AI agents construct a candidate counterexample and formal verification certifies it. The chapter treats this division of labor as a particularly natural setting for LLM creativity: generation can be broad and fallible because the final gate is rigorous.

## Mental Models

### Refutation as Rare-Event Search
A counterexample may occupy a tiny region of a huge construction space. CEM makes that rare event progressively less rare by fitting the proposal distribution to elite samples.

### Local Search as Verifier/Polisher
In PatternBoost, local optimization can do more than improve score: it can restore hard feasibility. The global model is allowed to propose approximate structure because local logic repairs the exact constraints.

### Elite Population as a Scientific Instrument
Do not watch only the best reward curve. Inspect the population of near-best constructions. Repeated motifs, bottlenecks, and transitions can reveal the mathematics of the extremal family.

### Failed Attempts Need Memory
An LLM agent without a record of failed constructions may repeatedly rediscover the same invalid idea. Store the attempted object, the failed condition, and the verifier's explanation in a compact searchable history.

## Anti-patterns
- **Binary success-only logging**: discarding high-quality near-misses erases structural clues.
- **Reward-only validity**: penalizing invalidity softly when it can be checked exactly allows optimization loopholes.
- **Local search alone in a multi-basin space**: repeated minor edits may never discover a new global motif.
- **Global generator without repair**: learned samples may have the right pattern but violate hard combinatorial constraints.
- **Self-verification by the same LLM**: correlated generation and checking errors make confident false counterexamples likely.
- **Over-decomposition**: splitting an agent task so finely that dependencies/context are lost; use subgoals that are independently checkable but mathematically meaningful.
- **Under-decomposition**: asking for one giant construction leaves no diagnostic boundary when verification fails.

## Reference Table: Counterexample Method Selection
| Condition | Deep CEM | PatternBoost | LLM Agent |
|---|---:|---:|---:|
| fixed discrete sequence encoding | strong | possible | possible |
| fast scalar reward | required | required for selection | helpful |
| strong local repair/improver | optional | central | tool-dependent |
| global motifs across elites | helpful | central | can infer in context |
| flexible symbolic reasoning/tools | limited | limited | strong |
| exact independent verifier | strongly recommended | strongly recommended | essential |
| easiest scaling bottleneck | sequence length/exploration | data + local search + model | verifier/tool orchestration |

## Worked Example
Suppose the conjecture states an inequality `F(G) ≤ B(n)` for every graph `G` on `n` vertices.

### Phase 1 — formulate
1. Choose an adjacency encoding that represents every allowed graph once or with controlled symmetry.
2. Implement exact checks for graph validity and an exact/high-precision computation of `F(G)`.
3. Define reward `R(G)=F(G)-B(n)`; `R>0` is a counterexample only if all constraints pass.

### Phase 2 — search
- If `n` is moderate and the graph can be built edge-by-edge, run deep CEM.
- If local edge flips can reliably improve feasible graphs and elites show recurring global structure, switch to PatternBoost.
- If constructing/evaluating `G` needs theorem-prover/CAS/code interactions or adaptive mathematical planning, use an LLM agent with the exact checker as a separate tool.

### Phase 3 — learn from failure
If no `R>0` object appears, collect the top percentile and cluster by structural features. If many share “two dense regions connected by a long sparse component,” parameterize that family analytically and examine the asymptotic formula for `F`. This can reveal the `n` at which the inequality changes sign even when the neural search never directly reaches it.

### Phase 4 — certify
Once a candidate is found, recompute from a clean implementation and, where practical, formalize the finite check or derive a symbolic proof that the construction violates the conjecture.

## Key Takeaways
1. Counterexample search is powerful when candidate quality and validity can be evaluated automatically.
2. Deep CEM learns a proposal distribution from elite construction trajectories.
3. PatternBoost combines local feasibility/precision with global pattern learning.
4. Elite near-misses can contain the mathematical structure needed to invent a parameterized counterexample family.
5. LLM agents should generate and adapt; independent tools should decide correctness.
6. A one-unit objective improvement can be logically decisive when it crosses a conjectured bound.

## Connects To
- **Ch 1**: refutation is one leg of the discovery–proof–refutation research loop.
- **Ch 2**: uses RL, cross-entropy training, Transformers, and reward design.
- **Ch 3**: shares search/evaluator design and stress-testing logic.
- **Ch 4**: formal verification supplies the strongest final gate for agent-generated constructions.
