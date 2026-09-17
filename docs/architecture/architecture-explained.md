# System overview — how DocAI is put together

This is the beginner-friendly architecture guide. DocAI is a product for **Invoice Intelligence** and **Contract Intelligence**, with a separate research area for comparing two processing approaches.

## Start with the user journey

```text
User opens the React web app
  ↓
Uploads an invoice or contract
  ↓
React sends HTTP/REST/JSON to FastAPI
  ↓
FastAPI calls a DocAI processing pipeline
  ↓
The pipeline returns UnifiedDocumentOutput
  ↓
React displays fields, clauses, risk flags and evidence
```

Think of the frontend as the restaurant counter and the backend as the kitchen. The counter collects the order and shows the result. The kitchen does the work. React never runs a model, and FastAPI is the only business backend.

## What each part means

### Frontend: `frontend/`

The **frontend** is the part a user sees and clicks. In this project it is a standalone **React + TypeScript + Vite** web application.

- **React** builds the screen from small reusable components.
- **TypeScript** describes the shape of data before the application runs.
- **Vite** runs the development server and builds the browser application.
- **HTML/CSS** provide the page structure and visual styling.
- **Node.js** runs `npm`, Vite and the TypeScript compiler. It is not a second API backend.

The scaffold has `/`, `/invoice`, `/contract` and `/research` routes without adding a routing framework. Pages do not show fake extraction results or fake metrics.

### Backend: `src/docai/api/`

The **backend** is the part the user does not see. FastAPI receives the upload, checks the request, invokes a pipeline and returns JSON. It is like the kitchen: the frontend should not enter it or reimplement its recipes.

An **API (Application Programming Interface)** is a set of rules for two pieces of software to communicate. **REST** is the HTTP style used by these rules. The planned product endpoints are `/parse/classic`, `/parse/vlm` and `/explain`; `/compare` belongs to Research Lab. Parsing endpoints are currently scaffold and return `501 Not Implemented`.

### Core contract: `src/docai/core/`

**JSON** is a text format for exchanging structured values. **Pydantic** validates Python data against a declared shape. `UnifiedDocumentOutput` is the shared contract between pipelines, FastAPI and the frontend.

The frontend mirrors that contract in [`frontend/src/types/document.ts`](../../frontend/src/types/document.ts). This prevents the frontend from guessing whether a confidence value is a number or whether a risk flag has a description.

### AI processing: `src/docai/pipelines/`

The processing layer has two alternatives:

```text
Track A: Layout Detection → OCR → KIE → structured output
Track B: Document → VLM → structured response → validation
```

An **Inference** is a model using what it has learned to process a new document. Both tracks currently have interfaces/scaffolds; real inference is not enabled in this phase.

### Data: `src/docai/data/`

The data layer loads, cleans and describes source data. It does not belong in React. Dataset downloads and benchmark preparation are outside this architecture-refinement task.

### Risk: `src/docai/fraud/`

The package name is historical. Its meaning is domain-specific:

- **Invoice Risk** checks arithmetic consistency, missing important values and low confidence.
- **Contract Risk** flags missing or review-worthy clauses.

A flag asks a person to review something. It is not proof of fraud and is not legal advice.

### Research: `src/docai/evaluation/`

Research compares Track A and Track B using real ground truth. It may measure Precision, Recall, F1, latency, cost, robustness and agreement. Research is separate from a single document's product flow.

## Architecture diagram

```text
                    USER
                      │
                      ▼
              React Frontend
         TypeScript + HTML + CSS
                      │
                  REST/JSON
                      │
                      ▼
                  FastAPI
                   Backend
                      │
                      ▼
               DocAI Core
                      │
          ┌───────────┴───────────┐
          │                       │
       Track A                 Track B
      Specialist              VLM-native
       Pipeline                 Pipeline
          │                       │
          └───────────┬───────────┘
                      │
          UnifiedDocumentOutput
                      │
              Risk / Explainability
```

Research runs alongside this flow:

```text
Track A output ─┐
                ├→ Evaluation → accuracy / latency / robustness / cost
Track B output ─┘
```

## Product domains

### Invoice Intelligence

An Invoice Workspace will eventually upload an invoice or receipt, select an engine, show extracted fields, confidence, bounding boxes, risk flags and structured JSON.

### Contract Intelligence

A Contract Workspace will eventually upload a contract, show metadata and clause spans, provide supporting text and surface Contract Risk. CUAD supports both this product capability and research; it is not merely a secondary experiment.

## What is implemented now?

- **Baseline**: Pydantic schema, configuration, basic risk rules and some metric helpers.
- **Scaffold**: React pages, FastAPI parse routes, Track A/B interfaces and explainability interfaces.
- **Planned**: real model inference, API orchestration, result views, full contract taxonomy, real evaluation and production deployment.

The repository deliberately does not add Express, NestJS, Redux, a database, authentication or microservices in this task.
