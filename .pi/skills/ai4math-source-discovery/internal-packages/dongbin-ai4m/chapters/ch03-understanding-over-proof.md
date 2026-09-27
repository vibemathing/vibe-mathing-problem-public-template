# Chapter 3: Understanding as the Research Objective

## Core Idea
The guide closes by treating proof as a means toward mathematical understanding. As AI assumes more mechanical proof and verification work, the human research frontier should shift toward explanations, connections, patterns, and deeper conceptual structure.

## Frameworks Introduced

### Understanding-over-proof review
**When to use**: an AI system has produced or verified a proof, or a project is becoming dominated by proof mechanics.

**How**:
1. Identify what mathematical obstacle the proof actually resolves.
2. Extract the decisive lemmas, invariants, constructions, or representations.
3. Explain why those ingredients work together.
4. Compare the mechanism with neighboring theorems or known patterns.
5. Ask what generalizes, what fails, and what new question becomes visible.
6. Preserve the proof/checker artifact for rigor while presenting the explanatory structure to humans.

### Automation dividend
When AI removes repetitive proving, search, or verification work, reinvest the saved time in tasks where human mathematical judgment has highest value: choosing definitions, forming abstractions, spotting connections, designing conjectures, and deciding what deserves study.

## Key Concepts
- **Mathematical understanding**: explanatory and structural knowledge that reveals why results hold and how they connect.
- **Proof as tool**: a rigorous instrument for establishing results and supporting understanding, without exhausting the purpose of mathematical research.
- **Automation dividend**: research capacity recovered when mechanical tasks are delegated to reliable AI/formal tools.

## Mental Models
- **Checked proof ≠ finished research**: correctness closes one question; understanding can open the next several.
- **Human attention is the scarce resource**: spend it on abstraction, interpretation, and direction-setting once machines can handle routine checking.
- **Rigor and insight are complementary**: formal verification secures correctness; conceptual analysis turns correctness into reusable mathematical knowledge.

## Anti-patterns
- **Proof completion as the only metric**: optimizing only for solved statements can produce technically correct output with little explanatory value.
- **Discarding the proof artifact after extraction**: insight should not replace rigor; retain the checked artifact so interpretation remains anchored.
- **Automation without research reallocation**: saving proof time has little value if the freed attention is not redirected toward deeper questions.

## Worked Example
An agent returns a formally verified theorem proof. The task continues with an understanding pass: compress the proof into its essential ideas, name the key invariant, explain which step would fail under weaker assumptions, compare the mechanism to a related theorem, and propose one generalization worth testing. The verified Lean artifact remains the correctness anchor; the human-facing deliverable becomes the structure and new questions extracted from it.

## Continuing Resource
The guide closes by pointing to Terence Tao’s Crowdsourced Math Projects page as a living index of projects, papers, datasets, code, and participation opportunities. Treat it as a discovery surface whose current contents should be checked at use time.

## Key Takeaways
1. Use AI proof automation to free mathematical attention, not to define the endpoint of research.
2. Preserve rigorous proof/checking artifacts while extracting human-readable explanatory structure.
3. Evaluate AI4M systems partly by whether they enable better mathematical questions and connections.
4. Continue surveying community projects and research resources because the AI4M landscape changes quickly.

## Connects To
- **Ch 1**: insight/connection is one of the three primary AI4M capabilities.
- **Ch 2**: formal verification and agents create the automation capacity whose value is realized through understanding.
