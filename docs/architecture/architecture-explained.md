# System overview — DocAI Document Intelligence Platform

Tài liệu này là overview architecture canonical của DocAI. Hệ thống được định vị trước hết là sản phẩm **Invoice Intelligence + Contract Intelligence**; dual-pipeline benchmark là research layer bên trong sản phẩm.

## Bức tranh tổng thể

```text
                    USER
                      │
                      ▼
              PLOTLY DASH
                Frontend
                      │
                      ▼
                 FASTAPI
                  Backend
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
 Invoice Intelligence     Contract Intelligence
          │                       │
          └───────────┬───────────┘
                      │
               Processing Layer
                      │
             ┌────────┴────────┐
             │                 │
          Track A           Track B
          Classic          VLM-native
             │                 │
             └────────┬────────┘
                      │
            UnifiedDocumentOutput
                      │
             Validation / Risk
                      │
               Explainability

Research/Evaluation chạy song song:

Track A output ─┐
                ├→ Evaluation → accuracy / latency / robustness / cost
Track B output ─┘
```

Luồng trên mô tả ranh giới trách nhiệm, không tuyên bố mọi bước đã chạy được. Trạng thái runtime hiện tại được ghi ở cuối tài liệu.

## Ranh giới các lớp

### Frontend: `src/docai/dashboard/`

Plotly Dash là web frontend chính thức của MVP. Dashboard được định hướng thành ba khu vực tách biệt:

- **Invoice Workspace**: upload invoice/receipt, xem document, extracted fields, confidence, bounding boxes, risk flags và JSON.
- **Contract Workspace**: upload contract, xem metadata, clause spans/categories, contract risk flags và structured output.
- **Research Lab**: compare Track A/B, benchmark metrics, robustness, latency, cost và agreement/disagreement.

Dashboard chỉ trình bày kết quả và gọi API/service; không chứa model implementation hoặc bản sao của processing logic. Hiện `app.py` mới có layout scaffold, chưa có callbacks hay dữ liệu thật.

### Backend: `src/docai/api/`

FastAPI là backend/API layer, chịu trách nhiệm request validation, document upload interface, pipeline invocation, response serialization và error handling. Route `/parse/classic` và `/parse/vlm` là product processing interfaces; `/compare` là research interface; `/explain` phục vụ explainability của product. Các route parse/compare/explain hiện là scaffold và trả HTTP 501.

API không nhúng model implementation trực tiếp trong route. Luồng mong muốn là:

```text
FastAPI → service/orchestration khi cần → docai.pipelines → schema
                                      → risk / explainability
```

Chưa tạo thêm tầng service riêng khi chưa có nhu cầu thực tế.

### Core contract: `src/docai/core/`

`schema.py` cung cấp shared envelope `UnifiedDocumentOutput` cho cả hai domain và hai track. Envelope hiện có `document_type`, `fields`, confidence, optional `bounding_box`, `risk_flags`, execution metadata và pipeline metadata.

Schema hiện tại là abstraction nhỏ, không phải taxonomy Contract hoàn chỉnh. `fields[]` cho phép field name/value khác nhau giữa Invoice và Contract, nên Contract không bị ép vào các field hóa đơn. Việc mở rộng contract-specific schema chỉ thực hiện sau khi schema/dataset mapping được chốt; task định vị này không tạo schema lớn mới.

### Processing engines: `src/docai/pipelines/`

**Track A — Classic Document AI**

```text
Layout Detection → OCR → KIE / LayoutLMv3 → UnifiedDocumentOutput
```

Track A là vùng AI/ML/DL chuyên sâu: layout detection, OCR, token/BIO tagging, fine-tuning và phân tích lỗi từng module. Candidate hiện tại được giữ nguyên; checkpoint cụ thể chưa chốt.

**Track B — VLM-native Document AI**

```text
Document → VLM → structured prompt → structured response
         → parsing → schema validation
```

Track B là vùng VLM/integration: input preparation, prompt, parsing, schema validation, retry/error handling và batch processing. Model cụ thể chưa chốt; các tên trong code chỉ là candidate/scaffold.

Cả hai track là processing backend có thể phục vụ Invoice và Contract theo capability thực tế, không phải hai product riêng.

### Data layer: `src/docai/data/`

Data layer phụ trách ingestion, preprocessing, normalization và statistics. `data/raw/`, `data/interim/` và `data/processed/` hiện chỉ giữ cấu trúc; task này không tải dataset.

### Domain validation/risk: `src/docai/fraud/`

Tên package lịch sử là `fraud`, nhưng semantics phải phân biệt domain:

- **Invoice Risk**: arithmetic consistency (`subtotal_amount + tax_amount` so với `total_amount`), missing important field và low confidence ở field số liệu.
- **Contract Risk**: missing important/required clause, clause inconsistency hoặc clause flag dựa trên taxonomy đã được chốt.

`FraudRiskEngine` hiện có baseline cho invoice arithmetic/confidence và một nhóm missing contract clauses. Đây là risk flagging/decision support; không tuyên bố phát hiện gian lận chắc chắn và không kết luận hợp đồng hợp pháp/bất hợp pháp.

### Explainability: `src/docai/explainability/`

Product cần trả lời “thông tin này đến từ đâu?” và “vì sao có flag?”. Invoice có thể dùng field bounding box, highlighting và confidence; Contract có thể dùng text span, page/clause location và supporting passage. Attention, visual grounding và Grad-CAM chỉ là kỹ thuật dự kiến; `DocumentExplainer` hiện là scaffold, không được xem là explanation hoàn chỉnh.

### Research/Evaluation: `src/docai/evaluation/`

Evaluation chạy song song với product flow, nhận output chuẩn hoá của hai track và ground truth để đo Precision/Recall/F1, agreement, latency, robustness, explainability evidence và cost. `BenchmarkRunner` là research orchestration, không phải dependency bắt buộc của một lần parse product.

Research không được kết luận track thắng khi chưa có benchmark thật. Product MVP và Research Complete là hai milestone độc lập.

## Vì sao giữ cả Invoice và Contract?

Invoice thường ngắn, có nhiều con số/bảng biểu và field tương đối rõ. Contract thường dài, dùng ngôn ngữ pháp lý, chứa clause và quan hệ ngữ nghĩa phức tạp. Hai domain vừa tạo product breadth vừa giúp research kiểm tra các failure mode khác nhau trên clean và noisy documents.

CUAD giữ vai trò kép: hỗ trợ Contract Information Extraction, Clause Classification/Detection và Contract Risk Analysis; đồng thời là nguồn cho generalization research. CUAD không phải use case phụ. Tuy nhiên, taxonomy CUAD đầy đủ và end-to-end Contract processing chỉ được gọi là implemented khi code và test thực tế chứng minh điều đó.

## Các quyết định phạm vi

- FastAPI là backend; Plotly Dash là frontend web chính thức.
- Không thêm React, Vue, Angular, Next.js, Node frontend stack hoặc Power BI ở phase hiện tại.
- Không thêm PostgreSQL, Redis, Kafka, Celery, Airflow, Kubernetes, microservices hoặc OAuth khi chưa có requirement.
- Giữ cấu trúc `src/docai/` hiện tại; không đổi tên folder chỉ để tạo nhãn frontend/backend.
- Không train model, tải dataset, tạo mock benchmark hoặc triển khai feature lớn trong task định vị.

## Trạng thái hiện tại

- **Đã chốt**: product domains Invoice + Contract, FastAPI backend, Plotly Dash frontend, Track A/B là processing engines, shared Pydantic envelope và bốn vùng responsibility trong task split.
- **Baseline có code/test**: schema validation, invoice/contract risk rules, metric helpers và route `/health`.
- **Scaffold**: model inference, pipeline orchestration, API parse/compare/explain handlers, Dash callbacks và explainability implementation.
- **Planned**: Contract taxonomy mở rộng, end-to-end Product MVP, ground-truth benchmark, robustness suite và cost measurement.
