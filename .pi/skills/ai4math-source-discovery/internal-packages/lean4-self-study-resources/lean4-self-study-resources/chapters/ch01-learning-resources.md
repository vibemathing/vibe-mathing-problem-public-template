# Chapter 1: 学习资源

## Core Idea

Use the archived list to match a Lean4 learning goal with a resource that was explicitly listed for that role. For formal mathematics, *Mathematics in Lean* carries the strongest recommendation in the source.

## Frameworks Introduced

The source does not name a formal framework. The following is an operational synthesis for applying its resource list.

- **Learning-goal routing** *(STRUCTURAL_SYNTHESIS)*
  - **When to use**: a learner asks where to begin or which material fits a specific goal.
  - **How**: classify the goal → choose the matching listed resource → give the smallest useful next step → avoid attributing unrecorded features.
- **Foundation-to-formal-math ladder** *(STRUCTURAL_SYNTHESIS)*
  - **When to use**: a learner wants a study order rather than a single link.
  - **How**: installation if needed → functional programming and/or theorem proving → optional Natural Number Game practice → *Mathematics in Lean* → specialization/reference material.
  - **Why it works**: it uses the archive's explicit categories and preserves the source's strong recommendation for *Mathematics in Lean*.
  - **Failure mode**: treating the sequence as mandatory. Skip stages the learner already knows.

## Key Concepts

- **ReasLab** — a listed Lean4 learning resource entry: https://beta.reaslab.io. The source says bug feedback is welcome but gives no feedback channel.
- **leanprover.cn** — a Chinese Lean resource hub listing four tracks: Functional Programming in Lean, Theorem Proving in Lean, Metaprogramming in Lean, and Mathematics in Lean: https://www.leanprover.cn
- **Functional Programming in Lean** — the archived Chinese hub's functional-programming learning track.
- **Theorem Proving in Lean** — the archived Chinese hub's theorem-proving learning track.
- **Metaprogramming in Lean** — the archived Chinese hub's metaprogramming learning track.
- **Mathematics in Lean** — formal-mathematics material described by the archive as main class content and strongly recommended: https://github.com/leanprover-community/mathematics_in_lean
- **Natural Number Game** — an introductory game around natural-number theorems: https://adam.math.hhu.de/#/g/leanprover-community/nng4
- **Installation tutorial** — the archive's installation resource: http://faculty.bicmr.pku.edu.cn/~wenzw/formal/docs/#/install
- **Terence Tao's Lean cheatsheet** — a compact Lean reference: https://docs.google.com/spreadsheets/d/1Gsn5al4hlpNc_xKoXdU6XGmMyLiX4q-LFesFVsMlANo/edit?gid=1045418473#gid=1045418473
- **NUS Lean minicourse** — listed Lean lecture/minicourse material: https://github.com/NUS-Math-Formalization/minicourse/tree/main

## Mental Models

- **Choose by task, not popularity**: use the resource whose archived label matches the learner's current goal.
- **Separate foundations from specialization**: functional programming and theorem proving serve broad foundations; metaprogramming is a distinct goal; formal mathematics has its own strongly recommended resource.
- **Use quick references as quick references**: a cheatsheet can shorten recall time, while declaration-level lookup belongs to the working-resource layer in ch02.

## Anti-patterns

- **Inventing features from a resource name**: the archive often supplies only a name, URL, and short label. Stay within that evidence.
- **Flattening all resources into equivalents**: the list distinguishes installation, programming, theorem proving, formal mathematics, metaprogramming, practice, lectures, and quick reference.
- **Turning a recommendation into a requirement**: *Mathematics in Lean* is strongly recommended in the source; learners may still need a different entry point based on prerequisites.

## Source Gaps and Special Cases

- The *Mathematics in Lean* entry says a Chinese version can be found in “4.a”, but the archived snapshot contains no section 4.a and no corresponding link. Treat that cross-reference as unresolved.
- The ReasLab entry explicitly welcomes bug feedback. The archive does not specify where or how to submit it, so do not invent a channel.

## Worked Example

A learner says: “I want to study formal mathematics in Lean, but I have never used Lean.”

1. Ask whether Lean is already installed. If not, point to the archived installation tutorial.
2. Use the Chinese hub's **Functional Programming in Lean** and/or **Theorem Proving in Lean** tracks for foundations, depending on the learner's gap.
3. If the learner benefits from game-based proof practice, add **Natural Number Game**.
4. Move to **Mathematics in Lean**, preserving the archive's strong recommendation.
5. Keep **Terence Tao's Lean cheatsheet** available for quick reference, and use ch02 resources when theorem/API lookup becomes the bottleneck.

## Key Takeaways

1. Route by the learner's immediate goal.
2. Preserve *Mathematics in Lean* as the source's strongest formal-math recommendation.
3. Use the Chinese hub when a Chinese-language path is desired.
4. Treat Natural Number Game as optional beginner practice, not as a full curriculum.
5. Use the installation tutorial for setup and the cheatsheet for quick reference.
6. Avoid claiming details that the archive does not contain.

## Connects To

- **Ch 2**: once the learner starts writing proofs, use the online compiler, Mathlib/API lookup, theorem search, automation, and community support.
- **Provenance**: see `../provenance.md` for source-vs-synthesis labels.
