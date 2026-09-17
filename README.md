# DocAI Document Intelligence Platform

DocAI is a Document Intelligence platform for two equal product domains:

- **Invoice Intelligence** — extract structured fields from invoices and receipts, then surface validation and risk signals.
- **Contract Intelligence** — extract contract metadata and clauses, then support clause and risk review.

The product has one Python backend, **FastAPI**, and one independent web frontend, **React + TypeScript + Vite**. Inside the backend, Track A and Track B are alternative AI processing engines. Research compares them on Invoice and Contract; the benchmark is part of the platform, not the platform's identity.

## What the product is meant to do

```text
USER
  ↓
React + TypeScript + Vite frontend
  ↓ HTTP / REST / JSON
FastAPI backend
  ↓
DocAI core → Track A or Track B
  ↓
UnifiedDocumentOutput
  ↓
Domain Risk / Explainability → review result
```

The intended user flow is: choose Invoice or Contract, upload a document, choose a processing engine, process the document, and review structured output with confidence, risk flags and supporting evidence. The current repository is a scaffold; it does not claim that this end-to-end flow is complete.

## Current capability status

- **Invoice Intelligence — BASELINE / SCAFFOLD**: shared output and basic invoice risk rules exist; model inference and end-to-end processing are not enabled.
- **Contract Intelligence — BASELINE / SCAFFOLD**: contract document type and baseline missing-clause rules exist; full CUAD taxonomy and extraction are planned.
- **Risk Analysis — BASELINE**: invoice arithmetic/confidence checks and contract missing-clause checks are implemented and tested. They are review signals, not definitive fraud or legal conclusions.
- **Explainability — SCAFFOLD**: interfaces for field boxes, clause spans and model evidence exist; runtime explanations are not implemented.
- **FastAPI API — SCAFFOLD**: route contracts exist; parse, compare and explain handlers currently return `501 Not Implemented`.
- **React frontend — SCAFFOLD**: page structure and typed API boundary exist; backend calls and result views are not complete.
- **Research Lab — PLANNED**: no real benchmark, ground truth result or fake metric is included.

## Product pages

The frontend is intentionally small and has four routes:

- `/` — product overview.
- `/invoice` — Invoice Workspace: upload, extraction, confidence, risk, evidence and JSON.
- `/contract` — Contract Workspace: metadata, clause spans, supporting text and Contract Risk.
- `/research` — Research Lab: Track A/B comparison, F1, latency, cost, robustness and agreement.

The pages are placeholders until the FastAPI processing endpoints are connected. The UI must never fabricate extraction results or metrics.

## Backend and processing

### FastAPI backend

`src/docai/api/` is the only business backend. It validates requests, accepts uploads, invokes the processing layer, serializes Pydantic output and handles errors. Node.js is not a second backend; it is only used for frontend tooling.

### Track A — Specialist pipeline

```text
Layout Detection → OCR → KIE / LayoutLMv3 → UnifiedDocumentOutput
```

Track A is the ML/DL-intensive path. It can use specialist components for layout, OCR and document understanding, with domain-specific mapping for Invoice or Contract. Current model classes are scaffold and the exact checkpoint is not selected.

### Track B — VLM-native pipeline

```text
Document → VLM → structured prompt/response → parsing → schema validation
```

Track B is the VLM/integration path. It will own input preparation, prompts, structured parsing, validation, retries and batching. The exact VLM is not selected.

Both tracks must return `UnifiedDocumentOutput`; neither is a separate product.

## Frontend/backend contract

```text
Pydantic schema
  ↓
FastAPI REST/JSON contract
  ↓
TypeScript interface
  ↓
React UI
```

The matching TypeScript types are in [`frontend/src/types/document.ts`](frontend/src/types/document.ts). The frontend communicates through [`frontend/src/services/api.ts`](frontend/src/services/api.ts); it does not read Python files or duplicate AI logic.

## Repository layout

```text
docai-pipeline-benchmark/
├── frontend/                 # React + TypeScript + Vite web application
│   ├── src/components/       # Small reusable UI pieces
│   ├── src/pages/            # Home, Invoice, Contract, Research Lab
│   ├── src/services/         # HTTP/API boundary
│   ├── src/types/            # TypeScript API contract
│   ├── src/App.tsx
│   └── src/main.tsx
├── src/docai/
│   ├── api/                  # FastAPI backend
│   ├── core/                 # Pydantic contracts/configuration
│   ├── pipelines/            # Track A and Track B
│   ├── data/                 # Data processing
│   ├── fraud/                # Domain risk rules
│   ├── explainability/       # Evidence scaffold
│   └── evaluation/           # Research metrics/comparison
├── scripts/                  # Python CLI entry points
├── tests/                    # Unit and integration tests
├── data/                     # raw/interim/processed data directories
├── docs/                     # Architecture, concepts, guides, reports and specs
├── modal_app/                # Modal infrastructure scaffold
├── log/                      # Progress log
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Setup and run

### Python backend

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
uvicorn docai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

`/health` is the currently usable API route. The parse, compare and explain routes remain scaffold until pipeline orchestration is implemented.

### React frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite development server runs on `http://localhost:5173` and proxies `/api` to FastAPI at `http://localhost:8000`. Build validation is `npm run build`.

### Tests

```bash
pytest
python -m compileall src scripts tests
```

## Research scope

Research asks:

> When Classic specialist processing and VLM-native processing serve the same Invoice and Contract product, how do they trade off accuracy, latency, robustness, explainability and cost?

Invoice provides short, numeric and table-heavy documents. Contract provides long, legally worded documents with clause-level semantics. CUAD therefore has a dual role: it supports Contract Intelligence and provides ground truth for generalization research. It is not a secondary product afterthought.

Research is complete only when both tracks have real outputs, ground truth, measured metrics, latency, robustness evidence and a reasoned cost measurement or estimate. No benchmark result in this repository should be read as real until that evidence exists.

## Documentation path

Start with [`docs/architecture/architecture-explained.md`](docs/architecture/architecture-explained.md), then follow [`docs/concepts/README.md`](docs/concepts/README.md). The implementation roadmap is in [`docs/specs/implementation-guide.md`](docs/specs/implementation-guide.md), responsibilities are in [`docs/specs/task-split.md`](docs/specs/task-split.md), and current status is in [`log/progress-log.md`](log/progress-log.md).

## Scope boundaries

This phase does not train or fine-tune models, download datasets, create fake benchmark outputs, build a production frontend, add authentication/database/microservices, or deploy to production. React, TypeScript and Vite are the frontend stack; FastAPI/Python remains the only business backend.
