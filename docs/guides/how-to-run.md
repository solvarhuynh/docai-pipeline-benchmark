# How to run DocAI locally

This guide starts the repository without implying that model inference is already complete. The Python service is the business backend. The React application is a separate browser frontend, and Node.js is used only for its tooling.

## What you need

- Python 3.10 or newer, with a virtual environment.
- Node.js and npm for `frontend/` development.
- Git, if you are working from a checkout.

Large model weights, credentials and datasets are intentionally not committed. Real inference also depends on selecting and installing the appropriate model implementation.

## Install Python dependencies

From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For package-style imports, an editable install may also be used:

```powershell
python -m pip install -e .
```

## Start the FastAPI backend

```powershell
uvicorn docai.api.main:app --reload --host 127.0.0.1 --port 8000
```

**FastAPI** is the Python web framework used by DocAI. It exposes an **API (Application Programming Interface)**: a defined way for another program to send a request and receive a response. The current backend has:

- `GET /health` for a service check;
- `POST /parse/classic` for the planned Track A product route;
- `POST /parse/vlm` for the planned Track B product route;
- `POST /compare` for the planned Research comparison;
- `POST /explain` for the planned evidence route.

The parse, compare and explain handlers are scaffolds and currently return `501 Not Implemented`. A healthy service therefore does not mean model inference is ready.

Check health in another terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

FastAPI also exposes interactive API documentation at `http://127.0.0.1:8000/docs`.

## Start the React frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The scaffold contains:

- `/` — product overview;
- `/invoice` — Invoice Intelligence workflow placeholder;
- `/contract` — Contract Intelligence workflow placeholder;
- `/research` — Research Lab placeholder.

The **frontend** is the part users see and click. **React** builds it from components, **TypeScript** describes expected data shapes, and **Vite** serves and builds the browser code. **Node.js** runs npm, Vite and the TypeScript compiler here; it is not a second API backend.

During local development, Vite proxies `/api/*` to FastAPI and removes the `/api` prefix. Thus a browser request to `/api/health` reaches FastAPI as `/health`. Set `VITE_API_BASE_URL` only when the backend is hosted at a different base URL.

Build the frontend for a static preview:

```powershell
npm run build
npm run preview
```

The output is a browser bundle in `frontend/dist/`, which is ignored by Git.

## Understand the data boundary

React sends HTTP requests and receives **JSON**, a text format for structured objects and arrays. Python validates the response with **Pydantic**, which checks that values match the declared schema. The TypeScript interfaces in `frontend/src/types/document.ts` mirror `UnifiedDocumentOutput`.

The browser does not call a model directly. The intended flow is:

```text
React → HTTP/REST/JSON → FastAPI → DocAI pipeline
     ← JSON validated by Pydantic ←
```

## Run repository checks

From the root, after installing the project dependencies:

```powershell
.venv\Scripts\python.exe -m compileall src scripts tests
.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

These checks validate Python compilation and repository tests. They do not prove that a model, Modal deployment or full upload workflow is operational.

## What is deliberately not covered?

This task does not train or fine-tune models, download datasets, create benchmark numbers, implement authentication, add a database or deploy production infrastructure. Follow the roadmap in [`docs/specs/implementation-guide.md`](../specs/implementation-guide.md) before enabling those activities.
