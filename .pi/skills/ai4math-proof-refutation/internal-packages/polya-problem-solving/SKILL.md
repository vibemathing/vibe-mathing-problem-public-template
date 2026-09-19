---
name: polya-problem-solving
description: "Polya math solving: proofs, heuristics, tutoring, review."
---

<!-- argument-hint: [problem, proof, tutoring situation, topic, or chapter number] -->

# 怎样解题：数学方法的新面貌
**Author**: 乔治·波利亚 | **Source**: EPUB, 4 parts + heuristic dictionary + 20 exercises | **Operational chapters**: 13 | **Generated**: 2026-09-12

## How to Use This Skill

Use this skill when the task requires discovering a route through an unfamiliar problem, planning or checking a proof, diagnosing why a learner is stuck, or reviewing a proposed solution.

1. **Classify the task**
   - **求解题 / find**: identify **未知量、已知条件、条件**.
   - **证明题 / prove**: identify **假设、结论**.
   - **实际问题 / practical**: identify goal, materially relevant data, constraints, model assumptions, and acceptable approximation.
   - **教学 / tutoring**: diagnose which stage is blocked before giving a hint.
   - **审查 / review**: start with independent checks, then trace the argument.

2. **Run the four-stage control loop**
   1. **理解问题** — make the target and constraints explicit.
   2. **拟订计划** — build a connection between what is given and what is sought.
   3. **执行计划** — switch from plausible search to justified steps.
   4. **回顾** — verify, simplify, derive differently, and reuse.

3. **Route by failure signal**
   - Target or conditions unclear → [ch02](chapters/ch02-understand-the-problem.md)
   - No plan appears → [ch03](chapters/ch03-related-problems-and-auxiliaries.md), then [ch04](chapters/ch04-transform-the-problem.md)
   - Goal is clear but forward search is blocked → [ch05](chapters/ch05-backward-work-and-pappus.md)
   - A pattern or hunch exists but is unproved → [ch06](chapters/ch06-heuristic-reasoning-and-conjectures.md)
   - A plan exists but proof/derivation has gaps → [ch07](chapters/ch07-execution-proof-and-rigor.md)
   - A result exists and needs checking → [ch08](chapters/ch08-review-validation-and-reuse.md)
   - A student is stuck → [ch09](chapters/ch09-teaching-diagnosis-and-hints.md)
   - The task is messy, real-world, or approximate → [ch10](chapters/ch10-practical-problems-and-models.md)
   - Representation is the bottleneck → [ch11](chapters/ch11-diagrams-notation-and-equations.md)
   - Work is cycling or attention is exhausted → [ch12](chapters/ch12-progress-persistence-and-incubation.md)
   - Need practice examples or method-selection cases → [ch13](chapters/ch13-problem-workshop.md)

4. **Load the relevant chapter before giving method-specific advice.** Use `glossary.md` for terms, `patterns.md` for procedures, and `cheatsheet.md` for rapid routing.

## Core Frameworks & Mental Models

### 四阶段法
**Use the stages as gates, not a ritual.** If execution fails because the problem was never understood, return to understanding. If a learner is already progressing, do not interrupt with checklist questions.

- **理解问题**: Can the target be restated? What is given? What constrains the answer? Is the condition possible, sufficient, redundant, or contradictory? Would a diagram or better notation expose structure?
- **拟订计划**: Look at the unknown/conclusion. Recall a solved problem with the same or similar target. Try its result or method. If the fit is close but incomplete, introduce a purposeful auxiliary element. If direct attack fails, transform the problem.
- **执行计划**: Treat heuristic ideas as provisional. Check each decisive step and justify it.
- **回顾**: Check the result and reasoning through a different lens; then ask what else the result or method can solve.

### 目标导向检索
When memory is large and undirected, **look at the unknown or conclusion first**. Search for a familiar problem that sought the same kind of object or a theorem with the same kind of conclusion. This narrows retrieval and often suggests the missing construction, theorem, or representation.

### 变换问题
When repeated attempts stop producing new information, change the problem deliberately:
- **重新表述 / 回到定义** when terminology hides usable relations.
- **分解与重组** when too many conditions are entangled.
- **特殊化** when variation is overwhelming or a conjecture needs a stress test.
- **一般化** when accidental details hide the essential property; a broader problem can become cleaner.
- **类比** when another problem has the same relation structure.
- **辅助问题** when a stepping stone can expose a route.
Record whether the new problem is **equivalent, weaker, or stronger**; otherwise reverse transfer can create lost or extraneous solutions.

### 逆向工作
When the endpoint is vivid but the route from the data is obscure, temporarily assume the endpoint has been reached. Ask what immediately preceding condition would make it possible, then repeat until reaching something known or constructible. Reverse the chain to execute. Verify every backward reduction that must be reversible.

### 启发式推理与严格证明分工
Use analogy, induction, symmetry, special cases, and progress signs to generate and rank ideas. Their output is **plausibility**, not certainty. Once a plan crystallizes, switch modes: prove, calculate, or construct with explicit justification. A conjecture becomes a proof problem only after it has been stated precisely.

### 进展信号
Treat these as evidence about where to spend effort:
- a previously unused datum becomes connected to the target;
- another clause of the condition is naturally accounted for;
- a simpler analogous or special problem appears;
- the representation becomes more coherent;
- the route predicts properties the final result ought to have.
Signals can mislead. Follow them with skepticism; abandon a route when signs remain absent and a viable alternative exists.

### 教学提示梯度
Diagnose the blocked stage first. Start with the most general natural question. Increase specificity only until the learner can resume independent work, then stop prompting. A hint that names the decisive theorem too early solves the teacher's problem and weakens the learner's opportunity to learn retrieval.

## Failure Recovery

Use this ladder when the current route fails:
1. Restate target/data/condition or hypothesis/conclusion.
2. Expand a key definition; redraw or relabel.
3. Focus on the unknown/conclusion and retrieve a related solved problem.
4. Change representation or transform the problem.
5. Introduce an auxiliary element/problem with an explicit purpose.
6. Reverse direction and work backward.
7. If effort has been sustained and the search is cycling, record the best partial insight, pause, and return later.

Return **“insufficient to determine”** when essential conditions/data remain genuinely missing, especially in practical problems. Do not manufacture uniqueness or a proof.

## SELF_CHECK

Before finalizing:
- Is the user's actual target explicit?
- Did I choose a method whose prerequisites hold?
- Did I use or deliberately dismiss every materially relevant datum/assumption?
- Did I confuse a heuristic clue with a proof?
- If I transformed the problem, is the direction/equivalence of the reduction clear?
- Did I test exceptions, special/extreme cases, symmetry, dimensions, or an independent derivation where relevant?
- If tutoring, did I leave a reasonable share of the work to the learner?
- Can the result or method be reused or simplified?

## Chapter Index

| # | Title | Key methods |
|---|---|---|
| [ch01](chapters/ch01-four-stage-control-loop.md) | Four-stage control loop | understand, plan, execute, review |
| [ch02](chapters/ch02-understand-the-problem.md) | Understand the problem | task type, conditions, definitions |
| [ch03](chapters/ch03-related-problems-and-auxiliaries.md) | Related problems & auxiliaries | retrieval, reuse, auxiliary elements/problems |
| [ch04](chapters/ch04-transform-the-problem.md) | Transform the problem | reformulate, decompose, generalize, specialize, analogy |
| [ch05](chapters/ch05-backward-work-and-pappus.md) | Backward work | analysis/synthesis, reversibility |
| [ch06](chapters/ch06-heuristic-reasoning-and-conjectures.md) | Heuristic reasoning | conjecture, induction, progress signs |
| [ch07](chapters/ch07-execution-proof-and-rigor.md) | Execution & proof | rigor, contradiction, induction, proof design |
| [ch08](chapters/ch08-review-validation-and-reuse.md) | Review & validation | checks, dimensions, symmetry, reuse |
| [ch09](chapters/ch09-teaching-diagnosis-and-hints.md) | Teaching & diagnosis | hint ladder, autonomy, routine problems |
| [ch10](chapters/ch10-practical-problems-and-models.md) | Practical problems | modeling, approximation, stopping data collection |
| [ch11](chapters/ch11-diagrams-notation-and-equations.md) | Representation | diagrams, notation, equation translation |
| [ch12](chapters/ch12-progress-persistence-and-incubation.md) | Human factors | progress, persistence, incubation, skilled judgment |
| [ch13](chapters/ch13-problem-workshop.md) | Problem workshop | method-selection practice across 20 exercises |

## Topic Index

- **Analogy / 类比** → ch03, ch04, ch06
- **Auxiliary element / 辅助元素** → ch03
- **Auxiliary problem / 辅助问题** → ch03, ch04
- **Backward work / 逆向工作** → ch05
- **Condition analysis / 条件** → ch02, ch10
- **Conjecture / 猜想** → ch06
- **Contradiction / 归谬法** → ch07
- **Definitions / 定义** → ch02, ch04
- **Diagram / 图形** → ch02, ch11
- **Dimensional analysis / 量纲检验** → ch08
- **Equation setup / 列方程** → ch11
- **Generalization / 一般化** → ch04
- **Heuristic reasoning / 启发式推理** → ch06, ch07
- **Induction / 归纳** → ch06, ch07
- **Notation / 记号** → ch11
- **Practical problem / 实际问题** → ch10
- **Progress signs / 进展的征兆** → ch06, ch12
- **Proof problem / 证明题** → ch02, ch07
- **Specialization / 特殊化** → ch04, ch08
- **Symmetry / 对称** → ch04, ch08
- **Teaching / 教学** → ch09
- **Unknown / 未知量** → ch02, ch03
- **Use the result / 利用结果** → ch08

## Supporting Files

- [glossary.md](glossary.md) — key terms with source-module references
- [patterns.md](patterns.md) — compact operational procedures
- [cheatsheet.md](cheatsheet.md) — routing tables and decision rules

## Scope & Limits

This skill encodes the book's problem-solving methods and examples as operational guidance. It does not guarantee a solution, and it does not turn plausible reasoning into proof. For domain-specific mathematics, combine it with the relevant mathematical knowledge. The EPUB's formula and diagram images were reviewed during compilation; the skill stores synthesized methods rather than reproducing the book.
