# Implementation guide and roadmap — DocAI

DocAI is a Document Intelligence product for two equal domains: Invoice Intelligence and Contract Intelligence. It accepts a document, extracts useful fields or clauses, validates the result, adds domain risk signals and presents evidence for human review.

The official architecture is:

```text
React + TypeScript + Vite
        ↓ HTTP/REST/JSON
FastAPI / Python
        ↓
DocAI core → Track A or Track B
        ↓
UnifiedDocumentOutput → risk/evidence → review UI
```

Node.js runs frontend tooling (`npm`, Vite and the TypeScript compiler). It is not a second business backend.

## What is Product MVP?

Product MVP requires at least one real path through the product:

```text
user opens React UI
  → uploads Invoice or Contract
  → FastAPI validates and accepts the request
  → a real processing engine runs
  → Pydantic validates UnifiedDocumentOutput
  → risk/evidence is attached
  → React displays the result and JSON
```

The current repository has the page scaffold and API contracts, but the parse handlers and pipeline inference are not connected. Product MVP is therefore not complete.

## What is Research Complete?

Research is a separate milestone. It requires real Track A and Track B outputs, ground truth, field/clause accuracy, measured latency, clean/noisy robustness, evidence analysis and a cost measurement or clearly qualified estimate. Product MVP does not automatically imply Research Complete, and no number should be invented to fill a report.

## Roadmap

### Phase 1 — Input and data foundation

Define accepted image/PDF inputs, preprocessing, `raw/interim/processed` boundaries and approved dataset mappings for Invoice and Contract. Preserve CUAD clause/span meaning when it is used. Do not claim data is available when directories contain only placeholders.

### Phase 2 — Shared core contract

Maintain package layout under `src/docai/`, configuration and Pydantic schemas. Keep `UnifiedDocumentOutput` small and shared: document type, fields, confidence, evidence/location, risk flags, timing and metadata. Domain-specific taxonomies can live within fields rather than forcing Contract into Invoice names.

### Phase 3 — Track A layout and OCR

Integrate an approved pretrained layout model and OCR implementation. Return tokens/text/boxes through internal interfaces and map them toward the shared contract. The current layout and OCR modules are `SCAFFOLD`.

### Phase 4 — Track A KIE

Add document understanding with LayoutLMv3 or the selected alternative, BIO tagging, field/clause aggregation, checkpoint recording and inference tests. Fine-tuning is future work and is outside the current architecture refinement.

### Phase 5 — Track B VLM parsing

Select a VLM only after requirements and deployment constraints are understood. Implement input preparation, domain-specific structured prompts, response parsing, schema validation, retry behavior and latency logging. The current VLM parser is an interface scaffold.

### Phase 6 — Contract Intelligence and CUAD

Map contract metadata, clause categories, text spans and page evidence. CUAD can support both the Contract product capability and research, but its taxonomy and context limits must be documented. Mark incomplete generalization as `SCAFFOLD` or `PLANNED`.

### Phase 7 — Domain risk and validation

For Invoice Risk, implement and test arithmetic consistency, missing important values and low confidence. For Contract Risk, implement review signals for missing, unusual or inconsistent clauses/metadata. A risk flag is decision support, not proof of fraud or a legal conclusion.

### Phase 8 — Evidence and explainability

Invoice evidence may include field boxes, highlighting and confidence. Contract evidence may include text spans, page/clause locations and supporting passages. Attention or heatmaps are diagnostic evidence only; they are not automatically a perfect explanation. The current explainer is `SCAFFOLD`.

### Phase 9 — Research evaluation

Use the same suitable workload and protocol for both engines. Report Invoice and Contract separately, with Precision, Recall, F1, latency, robustness, evidence quality, cost assumptions and agreement/disagreement. The current metrics and report templates do not constitute a benchmark.

### Phase 10 — Product integration

Connect FastAPI upload routes to pipeline orchestration, Pydantic serialization, error handling and integration tests. Connect the React Invoice, Contract and Research pages to real responses. Keep the frontend independent from Python implementation details. Build one verified end-to-end path before expanding the Research Lab.

## Repository status

- `src/docai/core/`: baseline Pydantic contract and configuration.
- `src/docai/fraud/`: baseline domain risk rules with tests.
- `src/docai/api/main.py`: `/health` works; parse/compare/explain routes are scaffold and return `501`.
- `src/docai/pipelines/`: Track A/B interfaces; no production model inference.
- `src/docai/explainability/`: evidence interface scaffold.
- `src/docai/evaluation/`: metric/comparison helpers; no real benchmark.
- `frontend/`: React/TypeScript/Vite page and API scaffold; no fake results.
- `data/`: no dataset was downloaded for this task.

Status vocabulary and responsibility details are maintained in [`docs/concepts/README.md`](../concepts/README.md), [`docs/guides/glossary.md`](../guides/glossary.md) and [`docs/specs/task-split.md`](./task-split.md).
