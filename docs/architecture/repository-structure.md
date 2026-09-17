# Repository structure — where each responsibility lives

The repository has one browser application and one Python package. A folder is created only when it has a clear responsibility.

```text
docai-pipeline-benchmark/
├── frontend/                      # React + TypeScript + Vite web UI
│   ├── src/
│   │   ├── components/             # Reusable UI pieces
│   │   ├── pages/                  # Home, Invoice, Contract, Research
│   │   ├── services/               # HTTP calls to FastAPI
│   │   ├── types/                  # TypeScript API contract
│   │   ├── App.tsx                 # Small route/page shell
│   │   ├── main.tsx                # Browser entry point
│   │   └── styles.css
│   ├── package.json                # Node development/build tooling
│   ├── tsconfig*.json
│   ├── vite.config.ts
│   └── index.html
├── src/docai/
│   ├── api/                        # FastAPI backend
│   ├── core/                       # Pydantic contracts/configuration
│   ├── pipelines/                  # Track A and Track B processing
│   ├── data/                       # Data ingestion/preprocessing
│   ├── fraud/                      # Domain risk rules
│   ├── explainability/             # Evidence/explanation scaffold
│   └── evaluation/                 # Research metrics/comparison
├── scripts/                        # Python CLI entry points
├── tests/                          # Unit and integration tests
├── data/                           # raw/interim/processed directories
├── docs/                           # Architecture, concepts, guides, reports, specs
├── notebooks/                      # EDA and exploration
├── modal_app/                      # Modal infrastructure scaffold
├── log/                            # Progress/review history
├── docker-compose.yml              # Local FastAPI container
├── pyproject.toml                  # Python package definition
└── README.md
```

## The important boundaries

```text
React UI
  ↓ HTTP request
FastAPI
  ↓ Python function/service call
DocAI pipelines
  ↓
Pydantic UnifiedDocumentOutput
  ↓ JSON response
React TypeScript types and components
```

- `frontend/` is the web UI. It does not import Python files, run models or duplicate AI logic.
- `src/docai/api/` is the only business backend. Node.js is not a second backend.
- `src/docai/pipelines/` owns AI processing. Track A is the specialist/modular path; Track B is the VLM-native path.
- `src/docai/core/` owns the shared data contract. Invoice and Contract fields may differ inside the shared envelope.
- `src/docai/data/` owns data processing, not UI state.
- `src/docai/evaluation/` owns Research Lab metrics, not normal product parsing.

## Why is there no `frontend/` Python dashboard anymore?

The official frontend has moved from Plotly Dash to React + TypeScript + Vite. The old `src/docai/dashboard/` Dash scaffold was removed so the repository has one unambiguous frontend direction. Plotly.js may be added later for research charts, but it would be a chart library, not the frontend framework.

## Current status

The React structure is a scaffold. FastAPI `/health` is usable; parse/compare/explain handlers, model inference, backend orchestration and real result views are not complete. No dataset or benchmark result is included as part of this change.
