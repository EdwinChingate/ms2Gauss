---
title: Codex Agents for ms2Gauss
kind: meta
source: documentation/Agents.md
last_updated: 2025-02-14
---

# Codex Agents Configuration for the ms2Gauss Repository

This file routes every request to the correct **mode** (Documentation, Analysis, Planning, Concept, Refactor) while enforcing the scientific context and the requirements described in [`Prompt_CodexDocumentation.md`](../Prompt_CodexDocumentation.md).

## 1. Global principles

1. **Protect scientific intent.** Every change must honor the Orbitrap MS2-first, Gaussian modeling workflow described in the ms2Gauss draft and references.
2. **Obey the documentation prompt.** Use [`DocumentationTemplate.md`](../DocumentationTemplate.md) semantics, metadata headers, cross-linking, math notes, plots, and table examples.
3. **Prefer Python for figures.** Code snippets that illustrate peaks, chromatograms, or networks should rely on numpy + matplotlib.
4. **Keep links alive.** Any object that is mentioned must link to its markdown doc; missing docs require stubs that clearly say so.
5. **No silent refactors.** Do not alter behavior unless a task explicitly requires it, and explain any numerical implications.

## 2. Mode reference

| Mode | When to use | Key responsibilities |
| --- | --- | --- |
| DocumentationAgent | New or updated docs, glossaries, theory chapters, or figure instructions. | Follow the full prompt, expand coverage to all functions/variables/tables, add math notes, Python examples, and figures. |
| AnalysisAgent | User asks to run workflows, produce exploratory plots, or demonstrate usage. | Build runnable examples referencing repo functions and variables; keep outputs MS2-first. |
| PlanningAgent | User needs a roadmap or improvement strategy. | Update [`documentation/IMPROVEMENT_PLAN.md`](./IMPROVEMENT_PLAN.md) and outline actionable steps linked to functions/variables. |
| RefactorAgent | Code structure or performance improvements are explicitly requested. | Preserve semantics, cite affected files, and synchronize docs. |
| ConceptAgent | Pure explanations of ms2Gauss concepts. | Lean on [`documentation/DEFINITIONS.md`](./DEFINITIONS.md) and [`documentation/GLOSSARY.md`](./GLOSSARY.md), including LaTeX where needed. |

## 3. Mode selection checklist

1. Parse the user request and determine whether it is documentation-, analysis-, planning-, refactor-, or concept-focused.
2. Adopt the matching mode (or combination) internally and follow its guardrails.
3. Always apply the global principles above plus any nested instructions from directory-level `AGENTS.md` files (currently only this file).

## 4. Documentation-specific guardrails

- Generate a **plan-first** response when explicitly requested before writing docs.
- Every new doc must start with the metadata header defined above.
- Each function doc must include: description with scientific context, math notes (if non-trivial), verbatim code block, key operations bullets, parameter descriptions, input/output links, helper-function links, “Called by” links, and an `Examples` section with runnable Python showing realistic data and at least one matplotlib visualization snippet.
- Each variable/table doc must include a physical description, snippet showing how it is defined (code or representative rows), key operations, per-column meaning, an example table with real units, and references to producer/consumer functions.

## 5. Analysis and plotting rules

- Prefer simulated but realistic Orbitrap-like data when real files are unavailable.
- Show how to build `numpy` arrays that mimic m/z or RT axes and how Gaussian parameters map to physical quantities.
- When illustrating redundancy or alignment, use scatter/heatmap plots with annotated tolerances.

## 6. Improvement planning rules

- Separate conceptual vs computational vs missing-function recommendations.
- Tie each recommendation to specific docs or source files so future contributors can act quickly.

## 7. Concept explanations

- Cross-link to glossary entries such as [m/z](./GLOSSARY.md#mz), [spectral redundancy](./DEFINITIONS.md#spectral-redundancy), or [Gaussian peak](./DEFINITIONS.md#gaussian-peak) whenever those ideas appear.
- Include LaTeX for mass error, Gaussian models, or similarity scores, and cite supporting references from `/references` when possible.

Following this routing document keeps every ms2Gauss change coherent, reproducible, and scientifically faithful.
