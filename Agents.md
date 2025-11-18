
---

## File 2 — `documentation/Agents.md`

```markdown
---
title: Codex Agents for ms2Gauss
kind: meta
source: documentation/Agents.md
last_updated: 2025-11-18
---

# Codex Agents Configuration for the ms2Gauss Repository

This file defines **how Codex should behave** when handling tasks related to this repository.

It does **not** describe chemical or spectral “agents”.  
Instead, it describes **Codex modes** (“agents”) and how to:

- choose the right mode for a given request,  
- respect the ms2Gauss scientific context,  
- follow `Prompt_CodexDocumentation.md`,  
- and keep all code, plots, and documentation consistent.

Whenever you work with this repo, you MUST:

1. Read and follow `Prompt_CodexDocumentation.md`.  
2. Use this `Agents.md` file to route the task to one or more “agents” (modes).  

---

## 1. Global Principles (Apply in ALL Modes)

These rules are universal:

1. **Respect the ms2Gauss Context**  
   - This is a high-resolution LC–HRMS workflow centered on **Orbitrap**, **Gaussian modeling**, and **MS2-first feature construction**.  
   - Scientific semantics must not be broken when refactoring or simplifying.

2. **Follow the Documentation Prompt**  
   - All documentation work MUST follow `Prompt_CodexDocumentation.md`.  
   - Use `DocumentationTemplate.md` for every object doc.  
   - Apply cross-linking, math notes, examples, tables, and figures as specified.

3. **Use Python for Plots**  
   - Any example plot must be generated via Python code snippets, using either real functions from this repo or clear simulated data.  
   - Use `matplotlib` as the default plotting library in examples.

4. **No Behavior-Breaking Refactors Unless Explicitly Requested**  
   - Refactor only in ways that preserve scientific and numerical behavior, unless the user explicitly authorizes conceptual or algorithmic changes.

5. **Hyperlink Everything**  
   - When mentioning functions / variables / tables / meta-docs, use markdown links according to the cross-linking rules in `Prompt_CodexDocumentation.md`.

6. **Be Explicit About Modes**  
   - Internally, pick a mode (agent) based on the task type.  
   - You don’t need to announce the mode to the user, but you must obey its rules.

---

## 2. DocumentationAgent

**When to use:**  
- The user asks to “document”, “improve docs”, “generate docs”, “explain functions/variables in doc form”, or implicitly wants new `.md` files for the repo.  

**Primary references:**  
- `Prompt_CodexDocumentation.md` (hard constraint).  
- `DocumentationTemplate.md`.  
- Existing `documentation/` files (to keep style consistent).

**Responsibilities:**

- Generate **plans** and then docs for:
  - `documentation/Functions/*.md`
  - `documentation/Variables/*.md`
  - `documentation/INDEX.md`
  - `documentation/GLOSSARY.md`
  - `documentation/DEFINITIONS.md`
  - `documentation/IMPROVEMENT_PLAN.md`
- Always:
  - Include math notes where relevant.  
  - Provide example tables for structured data.  
  - Provide Python + matplotlib code snippets for visualizable concepts.  
  - Hyperlink all referenced objects.

**Guardrails:**

- Never invent columns or parameters that contradict real code.  
- Do not modify source code unless user explicitly asks; this agent is for docs.

---

## 3. AnalysisAgent

**When to use:**  
- The user asks to **analyze data** with the repository’s functions.  
- The user wants to see **plots**, **workflows**, or **usage examples** for real or synthetic data.  
- The user asks “how would I use ms2Gauss to do X with data Y?”

**Primary references:**

- Functions in `Functions/` (e.g. `AllMS2Data`, `ms2_spectrum`, `feat_ms2_Gauss`).  
- Data structures documented in `Variables/`.  
- Scientific descriptions in `DEFINITIONS.md`.

**Responsibilities:**

- Propose concrete **Python code examples** that:
  - Import real functions from this repo where possible.  
  - Build minimal synthetic or pseudo-synthetic datasets when real data is not provided.  
  - Show plots via matplotlib:
    - Gaussian m/z peaks  
    - RT chromatograms  
    - MS2 redundancy clusters  
    - Feature distributions  

- Respect the semantics of ms2Gauss (MS2-first, Gaussian modeling, etc.).

**Guardrails:**

- Do not claim that example code is using real data unless data is actually present.  
- Keep examples minimal but scientifically meaningful (e.g. plausible m/z and RT ranges).

---

## 4. RefactorAgent

**When to use:**  
- The user asks to “refactor”, “simplify”, “optimize”, “modularize”, or “clean up” code.  
- The focus is on code structure and efficiency, not documentation.

**Primary references:**

- Original Python files in `Functions/` and `src/`.  
- Any performance suggestions already written in `IMPROVEMENT_PLAN.md`.

**Responsibilities:**

- Improve:
  - readability,  
  - modularity,  
  - vectorization (NumPy usage),  
  - efficiency of algorithms (where safe).  

- Keep **behavior identical**, especially:
  - same input/output shapes and types,  
  - same numerical behavior (within floating-point tolerance),  
  - same scientific meaning.

- Propose additional small helper functions if it reduces duplication.

**Guardrails:**

- Do not change core scientific logic (e.g. how Gaussians are computed, how CI is calculated) unless explicitly approved.  
- When in doubt, preserve the existing algorithm.

---

## 5. PlanningAgent

**When to use:**  

- The user asks for:
  - “a plan to improve the whole repository”,  
  - “a roadmap”,  
  - “what should I implement next?”,  
  - or anything about long-term architecture.

**Primary references:**

- `documentation/IMPROVEMENT_PLAN.md` (if it exists; otherwise you will create/update it).  
- `INDEX.md` (dependencies and entry points).  
- The paper draft and `/references`.

**Responsibilities:**

- Generate or extend `IMPROVEMENT_PLAN.md` with:
  - conceptual improvements (better modeling, new workflows),  
  - computational improvements (vectorization, caching, etc.),  
  - missing functions and suggested implementations,  
  - suggestions for tests and validation datasets.

- Ensure the plan references:
  - specific functions by link,  
  - specific tables/variables by link,  
  - relevant theoretical concepts in `DEFINITIONS.md`.

**Guardrails:**

- The plan is **descriptive and suggestive**, not silently destructive.  
- Do not assume removal of functions or tables without explicit user confirmation.

---

## 6. ConceptAgent (Theory & Explanation)

**When to use:**  

- The user asks for **conceptual explanations**:
  - “Explain how ms2Gauss models peaks.”  
  - “What is spectral redundancy?”  
  - “How does the feature table propagate uncertainty?”

**Primary references:**

- `DEFINITIONS.md` and `GLOSSARY.md`.  
- Individual function docs for detailed behavior.

**Responsibilities:**

- Provide clear, layered explanations:
  - Intuitive story.  
  - Formal definitions.  
  - Equations with LaTeX.  
  - Links to functions and variables.

- Use the same terminology as the docs (no new inconsistent jargon).

**Guardrails:**

- Do not drift away from the implementation; explanations must match what the code actually does.  
- If there is an ambiguity between paper draft and code, call it out and suggest resolving it in documentation or implementation (not silently pick one).

---

## 7. Mode Selection Logic

When a user request arrives, route internally as follows:

1. **If the user wants docs, templates, or better documentation → `DocumentationAgent`.**  
2. **If the user wants to run analyses, generate plots, or see workflows → `AnalysisAgent`.**  
3. **If the user wants refactors or performance improvements → `RefactorAgent`.**  
4. **If the user wants a roadmap or high-level improvements → `PlanningAgent`.**  
5. **If the user wants conceptual/theoretical explanation → `ConceptAgent`.**  

Mixed requests:

- If the request mixes documentation + explanation, let `DocumentationAgent` lead and use `ConceptAgent` logic inside descriptions.  
- If it mixes refactor + docs, clarify priorities internally:
  - First ensure scientific behavior is preserved (RefactorAgent rules).  
  - Then adjust documentation to match (DocumentationAgent rules).

You do **not** need to tell the user which agent you picked; you just act accordingly.

---

## 8. Interaction with `Prompt_CodexDocumentation.md`

This `Agents.md` file is a **routing/configuration layer**.

For any task involving documentation, you MUST:

1. Adopt `DocumentationAgent`.  
2. Apply **all** rules from `Prompt_CodexDocumentation.md`.  

For analysis, refactor, planning, or conceptual tasks:

- You still must **not** contradict the documentation prompt:
  - Respect cross-linking conventions.  
  - Use Python + matplotlib for plots.  
  - Use the same scientific definitions and equations.

If there is any conflict between this file and `Prompt_CodexDocumentation.md` in a documentation-related task, **`Prompt_CodexDocumentation.md` wins**.

---

## 9. Example Task Routing

A few examples:

- **User:** “Generate documentation for all ms2 redundancy functions and show example plots.”  
  - Mode: `DocumentationAgent` (primary) + `AnalysisAgent` for plot examples.  
  - Behavior: follow `Prompt_CodexDocumentation.md`; include Python + matplotlib examples in each doc.

- **User:** “Make ms2_spectrum faster, but keep results the same.”  
  - Mode: `RefactorAgent`.  
  - Behavior: refactor `ms2_spectrum` for speed, preserve semantics, and update docs if asked.

- **User:** “Explain how ms2Gauss integrates MS1 info into feature tables.”  
  - Mode: `ConceptAgent`.  
  - Behavior: use `DEFINITIONS.md`, function docs for `ms2_features_stats` and `feat_ms2_Gauss`, include equations and links.

- **User:** “Design a plan to extend this to MS3 data and isotope labeling.”  
  - Mode: `PlanningAgent`.  
  - Behavior: extend `IMPROVEMENT_PLAN.md` with conceptual and computational steps.

---

## 10. Philosophy of These Agents

These agents are internal “hats” Codex wears to keep work on this repo:

- **Coherent** (same concepts and language everywhere),  
- **Reproducible** (Python examples & plots),  
- **Scientifically faithful** (Orbitrap + Gaussian + MS2-first logic),  
- **Book-like** (definitions, glossary, examples, figures, cross-links),  
- **Evolvable** (clear improvement plans and refactor paths).

They are not separate programs.  
They are structured instructions for how you should think and respond when working inside the ms2Gauss universe.

---
