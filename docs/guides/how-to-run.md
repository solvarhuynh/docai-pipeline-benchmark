# Chạy DocAI ở local

Tài liệu này hướng dẫn khởi động repository và phân biệt phần đã chạy được với phần scaffold. Python là business backend; React là frontend riêng; Node.js chỉ phục vụ tooling frontend.

## Cần chuẩn bị

- Python 3.10 trở lên và virtual environment.
- Node.js/npm để chạy `frontend/`.
- Git nếu làm từ checkout.

Dataset, credential và model weight lớn không được commit. Inference thật còn phụ thuộc model đã chọn và runtime tương ứng.

## Cài dependency Python

Tại thư mục gốc:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Chạy FastAPI backend

```powershell
uvicorn docai.api.main:app --reload --host 127.0.0.1 --port 8000
```

**FastAPI** là web framework Python của DocAI. Nó cung cấp **API (Application Programming Interface)**, tức cách chương trình khác gửi request và nhận response. Route hiện có:

- `GET /health` — kiểm tra service;
- `POST /parse/classic` — route dự kiến cho Track A;
- `POST /parse/vlm` — route dự kiến cho Track B;
- `POST /compare` — so sánh Research;
- `POST /explain` — evidence/explainability.

Parse, compare và explain hiện là scaffold, trả `501 Not Implemented`; health pass không có nghĩa model inference đã sẵn sàng.

Kiểm tra health:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

API docs tương tác ở `http://127.0.0.1:8000/docs`.

## Chạy React frontend

```powershell
cd frontend
npm install
npm run dev
```

Mở `http://localhost:5173`. Các route là `/`, `/invoice`, `/contract` và `/research`. **React** tạo component, **TypeScript** mô tả data shape, **Vite** chạy/build browser code. Node.js chạy npm/Vite/compiler và không phải API backend.

Trong local development, Vite proxy `/api/*` tới FastAPI và bỏ prefix `/api`: `/api/health` ở browser đi tới `/health` ở backend. Dùng `VITE_API_BASE_URL` nếu backend ở base URL khác.

Build static bundle:

```powershell
npm run build
npm run preview
```

Output nằm ở `frontend/dist/` và đã được Git ignore.

## Boundary dữ liệu

React gửi HTTP và nhận **JSON**, là text format cho dữ liệu có cấu trúc. Python dùng **Pydantic** kiểm tra response theo schema; TypeScript type ở `frontend/src/types/document.ts` mirror `UnifiedDocumentOutput`.

```text
React → HTTP/REST/JSON → FastAPI → DocAI pipeline
     ← JSON đã được Pydantic validate ←
```

Browser không gọi model trực tiếp.

## Kiểm tra repository

```powershell
.venv\Scripts\python.exe -m compileall src scripts tests
.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Các lệnh này kiểm tra compile và test Python; không chứng minh Modal, model hoặc upload flow end-to-end hoạt động.

## Không nằm trong task này

Không train/fine-tune model, tải dataset, tạo benchmark giả, làm authentication/database hay deploy production. Xem roadmap tại [`docs/specs/implementation-guide.md`](../specs/implementation-guide.md).
