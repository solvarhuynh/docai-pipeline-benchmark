# Task split — DocAI Product and Research

This document is the canonical responsibility map. DocAI is one product with two equal domains—Invoice Intelligence and Contract Intelligence—and two alternative processing engines. The four work areas below describe responsibilities, not four separate products.

## Shared rules

- `src/docai/core/schema.py` is the Python source of truth for `UnifiedDocumentOutput`.
- `frontend/src/types/document.ts` mirrors the API contract for the browser.
- FastAPI/Python is the only business backend. React + TypeScript + Vite is the web frontend.
- Track A and Track B own processing; they do not expose model logic to the browser.
- Invoice and Contract may have different field/clause taxonomies while sharing the outer result envelope.
- `Implemented` and `Baseline` require evidence. Otherwise use `SCAFFOLD`, `PLANNED` or `NOT SELECTED`.
- Do not train, fine-tune, download datasets, fabricate metrics or build production infrastructure in this architecture task.

## 1. Track A — AI/ML/DL

Owner: the AI/ML/DL contributor, with Product Engineering at interface boundaries.

Responsibilities:

- layout detection, image preprocessing and box normalization;
- OCR, tokenization and text-location handling;
- KIE with LayoutLMv3, BIO tagging and field/clause aggregation;
- pretrained checkpoint selection, fine-tuning and inference when those phases are approved;
- model-level error analysis and robustness experiments;
- returning results through `UnifiedDocumentOutput`.

Current state: `src/docai/pipelines/track_a/` contains interfaces/scaffolds. No production checkpoint is selected.

## 2. Track B — VLM/Integration

Owner: the VLM/integration contributor, with Track A and Product Engineering where the contract or evaluation is shared.

Responsibilities:

- image/PDF input preparation and batching;
- prompts that differ appropriately for Invoice and Contract;
- parsing candidate structured responses and validating them;
- retry/error handling, model runner integration and latency logging;
- mapping VLM results to `UnifiedDocumentOutput`.

Current state: `src/docai/pipelines/track_b/` contains prompt/parser scaffolding. PaddleOCR-VL and dots.ocr remain candidates; real inference is not enabled.

## 3. Product Engineering

Owner: the product/integration contributor, coordinating with both processing areas.

Responsibilities:

- React pages and reusable components in `frontend/`;
- TypeScript API types and HTTP service calls;
- FastAPI request validation, upload routes, orchestration, serialization and errors;
- Docker/local development integration;
- shared schema changes and compatibility checks;
- Invoice Workspace: fields, confidence, evidence and Invoice Risk;
- Contract Workspace: metadata, clause spans, supporting text and Contract Risk;
- integration tests and user-facing documentation.

The boundary is:

```text
React + TypeScript + Vite
        ↓ HTTP/REST/JSON
FastAPI
        ↓
DocAI pipelines
        ↓
Pydantic UnifiedDocumentOutput
```

Node.js is frontend tooling only. Do not create an Express/NestJS backend or add Next.js, Redux, Zustand, Tailwind, a database, authentication or microservices without a separate requirement. Do not put model logic in React.

Current state: the React scaffold, typed API boundary and FastAPI route contracts exist. Upload orchestration and real result rendering remain `SCAFFOLD`.

## 4. Research and Evaluation

Owner: Track A + Track B together; Product Engineering supports data collection and the Research Lab surface.

Responsibilities:

- define ground truth, dataset splits and a repeatable comparison protocol;
- report field/clause Precision, Recall and F1;
- measure latency, cost assumptions, robustness and evidence quality;
- analyze agreement/disagreement between engines;
- report Invoice and Contract separately;
- use CUAD for Contract Intelligence and contract generalization research when the approved mapping supports it;
- keep benchmark reports separate from product claims.

Research cannot declare a winner from architecture alone. It needs real outputs, suitable ground truth and reproducible measurements. Current evaluation helpers and reports are `SCAFFOLD`/`PLANNED`.

## Domain ownership

### Invoice Intelligence

Product Engineering owns the review workflow and API/UI integration. Track A/B own their extraction capability. Risk work covers arithmetic consistency, missing fields and confidence. Research measures field extraction on numeric and table-heavy documents.

### Contract Intelligence

Product Engineering owns the review workflow and API/UI integration. Track A/B own clause/metadata extraction. Risk work highlights missing or unusual clauses for human review; it does not decide legality. Research uses clause-level ground truth such as CUAD when the taxonomy and input context are ready.

Contract is a first-class product domain, not only a research dataset.

## Delivery order

1. Establish data/input boundaries and the shared schema.
2. Implement Track A and Track B behind stable interfaces.
3. Connect Invoice and Contract capabilities to FastAPI.
4. Connect React pages to real API responses.
5. Add domain risk and evidence to the review flow.
6. Run end-to-end tests and only then begin comparative research.

Each task must update [`log/progress-log.md`](../../log/progress-log.md) with owner, files, evidence and actual status. Schema changes require review by both processing areas and Product Engineering.
