# Chapter 1: Orientation and AI4M Foundations

## Core Idea
AI4M should be organized around the bottlenecks it removes from frontier mathematics: knowledge navigation, proof/verification, and insight/connection. A student's entry path then depends on whether their comparative advantage leans toward mathematics or toward algorithm/programming work.

## Frameworks Introduced

### Three AI4M capabilities
- **Knowledge navigation**
  - When to use: the researcher is spending substantial time locating related results, learning a theory, finding tools, or retrieving reusable formal/library knowledge.
  - How: define the precise knowledge gap; retrieve candidate material; compare definitions/assumptions; connect it to the current problem; verify relevance before relying on it.
- **Proof & verification**
  - When to use: correctness, counterexamples, proof completion, or proof inspiration is the main bottleneck.
  - How: separate proof search from checking; use a verifier whenever a formal representation is available; preserve explicit uncertainty before verification.
- **Insight & connection**
  - When to use: the goal is to discover patterns, analogous structures, new viewpoints, or latent relations.
  - How: collect relevant structures/data/proofs; look for stable regularities; turn them into mathematical hypotheses; test them with examples, theory, or formal verification.

### Interest fork
- If the learner is strongest in **mathematics**, begin from mathematical questions and learn enough ML/AI to identify data-driven subproblems and interpret results.
- If the learner is strongest in **algorithms/programming**, build stronger foundations in LLMs, agents, formal mathematics, Lean, and systems that solve reusable classes of tasks.
- Both routes require working literacy in machine learning, deep learning, reinforcement learning, large language models, and programming.

## Key Concepts
- **AI4M**: AI used to reduce the time cost and increase the effectiveness of mathematical research.
- **Knowledge navigation**: AI support for finding and learning theories, tools, definitions, and related results.
- **Proof & verification**: AI support for constructing proof steps, checking counterexamples, and establishing rigorous correctness.
- **Insight & connection**: AI support for discovering mathematical patterns, relations, and viewpoints.
- **Agent**: an orchestration approach in which a model performs a multi-step task through planning, tool use, feedback, and iteration.
- **Prompt engineering (PE)**: structured interaction with a model; the guide points readers to an optimal-control view of PE and PE-based agents.

## Source Learning Anchors
The guide points learners to a Chinese LLM textbook by Wen Jirong’s team at Renmin University, Dimitri Bertsekas’s reinforcement-learning course/book, the Prompt Engineering Guide for agents and PE, and the author team’s optimal-control treatment of prompt engineering (arXiv:2310.14201). Use these as orientation resources; verify current editions and links externally when needed.

## Mental Models
- **Bottleneck before tool**: choose AI technology only after identifying which research bottleneck dominates.
- **Two-entry-path model**: mathematical sensitivity and algorithmic engineering are different strengths; neither eliminates the need for baseline literacy in the other.
- **Agent as control loop**: view prompting/tool use as iterative control with feedback, not as a single static prompt.

## Anti-patterns
- **Tool-first learning**: collecting fashionable systems without a mathematical bottleneck to solve produces shallow competence.
- **Ignoring baseline AI literacy**: specializing in mathematics does not remove the need to understand ML/LLM/RL concepts well enough to judge tool behavior.
- **Treating retrieval as proof**: finding a similar theorem or plausible argument does not establish correctness.

## Worked Example
A mathematics-first student wants AI help on a research topic. Start by classifying the pain point. If most time is spent learning adjacent theory, prioritize knowledge navigation and a strong retrieval workflow. If the problem has many computable examples and the goal is a new conjecture, route toward a special-purpose data-driven tool. If the immediate need is rigorous proof checking, begin learning Lean and verifier-guided methods. The student's AI curriculum is then chosen to support that concrete route rather than pursued as an undirected survey.

## Key Takeaways
1. Diagnose the research bottleneck before choosing an AI technique.
2. Keep knowledge navigation, proof/verification, and insight/connection distinct because they demand different validation standards.
3. Choose an entry path based on both personal strengths and the shape of the mathematical task.
4. Maintain baseline competency in ML, deep learning, RL, LLMs, programming, and agents whichever path you choose.

## Connects To
- **Ch 2**: turns the two-entry-path orientation into concrete research methods.
- **Ch 3**: explains why proof automation should ultimately serve mathematical understanding.
