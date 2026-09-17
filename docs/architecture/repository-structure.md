# Repository structure — DocAI

Repository giữ `src/` layout hiện tại. Tên thư mục phản ánh responsibility kỹ thuật; `frontend/` và `backend/` riêng không cần thiết vì vai trò đã được thể hiện bởi `src/docai/dashboard/` và `src/docai/api/`.

## Cây thư mục

```text
docai-pipeline-benchmark/
├── src/docai/
│   ├── core/                    # Shared Pydantic contracts và config
│   ├── data/                    # Ingestion, preprocessing, statistics
│   ├── pipelines/
│   │   ├── track_a/             # Classic: layout → OCR → KIE
│   │   └── track_b/             # VLM-native: prompt → parse → validate
│   ├── fraud/                   # Invoice Risk và Contract Risk rules
│   ├── explainability/          # Evidence/explanation scaffold
│   ├── evaluation/              # Research metrics và comparison
│   ├── api/                     # FastAPI backend
│   └── dashboard/               # Plotly Dash frontend
├── scripts/                     # CLI entry points gọi package logic
├── tests/                       # Unit và integration tests
├── data/
│   ├── raw/                     # Dataset gốc; chưa tải trong task này
│   ├── interim/                 # Dữ liệu trung gian
│   └── processed/               # Dữ liệu chuẩn hoá
├── docs/
│   ├── architecture/           # System overview, structure, data dictionary
│   ├── concepts/               # Kỹ thuật gắn với product và research
│   ├── guides/                 # Hướng dẫn chạy và protocol
│   ├── reports/                # Report scaffold và kết quả khi có thực nghiệm
│   └── specs/                  # Roadmap và task split
├── notebooks/                  # Khám phá/EDA, không chứa business logic độc lập
├── modal_app/                  # Modal infrastructure scaffold
├── log/                        # Progress và review logs
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Các boundary chính

### `src/docai/api/` là Backend

FastAPI nhận request/upload, validate input, gọi orchestration/pipeline, serialize `UnifiedDocumentOutput` và trả lỗi. Route không được chứa implementation của YOLO, OCR, LayoutLMv3 hay VLM.

Các interface được định hướng:

- `/parse/classic`, `/parse/vlm`: product processing cho Invoice hoặc Contract;
- `/explain`: product explainability;
- `/compare`: Research Lab comparison;
- `/health`: service health.

Hiện parse/compare/explain vẫn là scaffold và trả HTTP 501.

### `src/docai/dashboard/` là Frontend

Plotly Dash là frontend web chính thức. Layout tương lai có Invoice Workspace, Contract Workspace và Research Lab. Dashboard tiêu thụ API/core output; không tự xử lý model và không sao chép logic từ backend. `app.py` hiện mới có layout scaffold, chưa có callbacks/dữ liệu thật.

### `src/docai/core/` là shared contract

`schema.py` định nghĩa `DocumentType`, `ExtractedField`, `RiskFlag`, `BoundingBox` và `UnifiedDocumentOutput`. Đây là envelope chung cho hai domain, không phải danh sách field cố định cho Invoice. Contract được biểu diễn bằng `document_type=contract` và các field/clause phù hợp; taxonomy chi tiết vẫn là scaffold/planned.

### `src/docai/pipelines/` là processing layer

- `track_a/`: Classic modular pipeline. `layout_detection.py`, `ocr_extraction.py` và `kie_layoutlmv3.py` hiện là scaffold.
- `track_b/`: VLM-native pipeline. `vlm_parser.py` có prompt interface; model invocation và parsing thật hiện là scaffold, model cụ thể chưa chốt.

Cả hai track có thể phục vụ Invoice và Contract ở mức capability thực tế; chúng không phải product riêng.

### `src/docai/fraud/` là domain risk layer

Package name được giữ tương thích, nhưng tài liệu và output phải phân biệt:

- Invoice Risk: arithmetic consistency, missing field và low-confidence amount.
- Contract Risk: missing important clause, clause inconsistency và clause-risk flagging.

Không dùng `fraud` để đưa ra kết luận gian lận hoặc kết luận pháp lý khi evidence không đủ.

### `src/docai/explainability/` là evidence layer

Invoice hướng tới bounding box/highlighting/confidence. Contract hướng tới text span/clause location/supporting passage. Attention/grounding/Grad-CAM là hướng triển khai; module hiện chưa sinh explanation runtime.

### `src/docai/evaluation/` là Research layer

Metrics và `BenchmarkRunner` nhận output chung để đánh giá accuracy, latency, robustness, explainability và cost trên Invoice/Contract. Evaluation không bắt buộc cho một product parse đơn lẻ và không được chứa số liệu giả.

## Nguyên tắc phụ thuộc

```text
Dashboard → FastAPI/API contract → orchestration → pipelines
                                             ↘ core schema
Risk và Explainability tiêu thụ output chuẩn hoá.
Evaluation tiêu thụ output chuẩn hoá + ground truth.
```

Không để consumer phụ thuộc trực tiếp vào output tùy tiện của model. Không thêm React/Vue/Angular/Next.js, Power BI hoặc một hệ thống hạ tầng mới khi chưa có requirement.
