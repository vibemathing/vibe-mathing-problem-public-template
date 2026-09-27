# Chapter 11: Teaching, Learning, and Collaboration

## Core Idea

Mathematicians learn formalization fastest when the mathematics is already familiar, the proof state is visible, and the learning loop rewards experimentation and asking for help. Separate the difficulty of a new theorem prover from the difficulty of new mathematics until basic fluency exists.

## Beginner Progression

A practical sequence from the Xena teaching experiments:

1. elementary logic and familiar arithmetic;
2. small set/function/relation exercises;
3. core structural tactics (`intro`, `exact`, `apply`, `have`, `cases`, `split`, `induction`, rewriting);
4. library lookup and existing theorem reuse;
5. ordinary undergraduate topics the learner already knows;
6. open-ended projects chosen to match mathematical maturity;
7. only later, new abstract mathematics plus formalization simultaneously.

Games and browser interfaces work because installation friction is low and the goal state provides immediate feedback. Live coding is valuable because learners see an expert encounter and recover from real errors rather than only seeing polished scripts.

## Project-Based Learning

Open projects can outperform uniform assignments for formalization because collaboration stops looking like plagiarism and starts looking like normal mathematical work. A good project assessment asks for:

- compiling Lean code;
- a short human write-up of design choices and difficulties;
- evidence the student understands a selected part of the code;
- reflection on what had to be scaled back or assumed;
- attribution when help/code came from peers.

Learners should discover a core research skill: estimating what is feasible. “Do not bite off more than you can chew, and ask when blocked” is itself a learning objective.

## Help-Seeking Protocol

For a stuck Lean question, prepare:

1. a minimal compiling file or smallest failing example;
2. exact imports/version;
3. the current goal/error text;
4. the intended mathematical step;
5. what has already been tried.

Screen sharing and active community channels shorten debugging loops. If the answer reveals a recurring gap, turn it into documentation or a library lemma so the same novice trap does not recur.

## Course Design Heuristics

- Teach the tools students need for the mathematics they will actually formalize; do not detour through abstractions merely because the instructor likes them.
- Easy early exercises build tactic fluency before realistic problem sheets demand many techniques at once.
- Allow ambitious students to use advanced material, but keep evaluation bounded by what instructors can meaningfully assess.
- If temporary axioms are allowed in projects, require students to state them clearly and check that they are true. A false axiom can make grading/proof interpretation meaningless.
- Provide rich formative feedback. Improvement matters more than a single polished artifact.

## Human-Readable Artifacts

Tactic scripts are hard to read statically because intermediate states are hidden. For teaching and research communication, pair code with explanation, goal-state snapshots, or an interactive document that cross-links human lemmas and Lean declarations. Formalization and informal exposition should reinforce each other.

## Anti-patterns

- Teaching advanced filters/category theory before learners can navigate basic Lean and before they need it.
- Giving polished solutions without showing debugging.
- Treating collaboration as cheating in inherently open-ended formalization work.
- Using completion of every worksheet as the success metric.

## Validation Checkpoint

Choose exercises where the mathematics is already familiar enough that Lean, not subject matter, is the main difficulty. Watch whether learners can predict the next proof state and explain why a tactic applies. When help is needed, ask for the smallest compiling context and current goal rather than a screenshot or long narrative. For open projects, scale ambition after the first dependency scan and keep a visible list of blockers. Success includes learning to shrink a problem, search the library, ask precise questions, and recognize when a definition/API issue is causing proof friction.

## Key Takeaways

Use familiar mathematics, visible proof states, incremental tactics, realistic projects, and a strong help culture. Teach feasibility judgment and explanation alongside proof construction.

## Connects To

Proof-state model: [02](ch02-types-proof-terms-and-proof-state.md). Core tactics: [03](ch03-proof-construction-and-tactic-selection.md). Research collaboration: [10](ch10-research-blueprints-and-library-growth.md).
