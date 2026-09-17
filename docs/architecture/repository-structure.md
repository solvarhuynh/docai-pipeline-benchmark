# Cấu trúc repository — trách nhiệm nằm ở đâu?

Repository có một browser application và một Python package. Chỉ tạo folder khi folder đó có trách nhiệm rõ ràng.

```text
frontend/                      # React + TypeScript + Vite
  src/components/              # UI component dùng lại
  src/pages/                   # Home, Invoice, Contract, Research
  src/services/                # HTTP call tới FastAPI
  src/types/                   # TypeScript API contract
src/docai/api/                 # FastAPI backend
src/docai/core/                # Pydantic contract/config
src/docai/pipelines/           # Track A và Track B
src/docai/data/                # ingestion/preprocessing
src/docai/fraud/               # domain risk rules
src/docai/explainability/      # evidence scaffold
src/docai/evaluation/          # research metrics/comparison
scripts/                       # Python entry points
tests/                         # unit/integration tests
data/                          # raw/interim/processed
docs/                          # architecture, concepts, guides, tasks, reports
notebooks/                     # EDA và exploration
modal_app/                     # Modal scaffold
log/                           # lịch sử tiến độ/review
```

## Boundary quan trọng

```text
React UI
  ↓ HTTP request
FastAPI
  ↓ Python service call
DocAI pipelines
  ↓
Pydantic UnifiedDocumentOutput
  ↓ JSON
React TypeScript types/components
```

- `frontend/` không import Python, chạy model hoặc duplicate AI logic.
- `src/docai/api/` là business backend duy nhất; Node.js chỉ là frontend tooling.
- `src/docai/pipelines/` sở hữu processing; Track A là modular, Track B là VLM-native.
- `src/docai/core/` sở hữu data contract; field Invoice và Contract có thể khác nhau.
- `src/docai/data/` sở hữu data processing, không sở hữu UI state.
- `src/docai/evaluation/` sở hữu metric Research, không sở hữu product parsing thông thường.

## Vì sao không còn frontend Python cũ?

Frontend chính thức đã chuyển sang React + TypeScript + Vite. Scaffold frontend Python cũ trong `src/docai/dashboard/` đã bị xóa để repository chỉ còn một hướng frontend rõ ràng. Nếu cần chart research, Plotly.js chỉ là thư viện chart phía frontend, không phải framework.

## Trạng thái

React structure là scaffold. FastAPI `/health` dùng được; parse/compare/explain, model inference, orchestration và result view thật chưa hoàn thiện. Task này không bao gồm dataset hoặc benchmark result.
