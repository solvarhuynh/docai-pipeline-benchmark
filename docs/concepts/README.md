# Concept map — learn DocAI from the document outward

This folder explains why DocAI is built this way. It is written for someone who can program and work with data, but does not work with AI/ML/DL every day.

## The story in one page

A document starts as pixels or a PDF. The product must turn it into information a person or another system can use:

```text
Invoice or Contract
  ↓
Read words, layout and meaning
  ↓
Extract fields or clauses
  ↓
Validate and attach risk/evidence
  ↓
Return JSON through FastAPI
  ↓
Show the result in React
```

Track A and Track B are two ways to do the middle part. The product can use either. The Research Lab compares them only when real outputs and ground truth exist.

## Suggested reading path

1. [`01-docai-foundations.md`](./01-docai-foundations.md) — why a document is more than an image, and what structured output means.
2. [`02-track-a-classic.md`](./02-track-a-classic.md) — why a specialist pipeline separates layout, OCR and understanding.
3. [`03-track-b-vlm.md`](./03-track-b-vlm.md) — why a VLM can combine visual understanding and response generation.
4. [`04-fraud-and-explainability.md`](./04-fraud-and-explainability.md) — how risk flags and evidence support review without overclaiming.
5. [`05-evaluation.md`](./05-evaluation.md) — how to decide whether a pipeline is actually performing well.

Read the architecture guide alongside this path: [`docs/architecture/architecture-explained.md`](../architecture/architecture-explained.md).

## The mental model

```text
Product problem
  → document representation
  → processing engine
  → shared schema
  → API and frontend
  → risk/evidence
  → research measurement
```

Every concept should answer four questions: What problem does it solve? What is the everyday intuition? Where is it in this repository? Where does its output go next?

## Status vocabulary

- **Implemented/Baseline** means code exists and tests or runtime evidence support the claim.
- **Scaffold** means an interface or page exists, but the real implementation is not complete.
- **Planned** means it belongs to the roadmap but has not started.
- **Not selected** means a model or external technology is still a candidate.

At this stage the React frontend, model inference, API orchestration and Research Lab are scaffolds or planned. No document output or benchmark metric should be treated as real unless it is produced by a real run.
