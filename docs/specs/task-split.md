# Task split — DocAI Product + Research

Task split này chia responsibility theo bốn vùng: **Track A — AI/ML/DL**, **Track B — VLM/Integration**, **Product Engineering** và **Research & Evaluation**. Đây không phải cách chia dự án thành hai sản phẩm; Track A/B là hai processing engine bên trong cùng product Invoice + Contract Intelligence.

## Nguyên tắc chung

- Invoice Intelligence và Contract Intelligence là hai product domain ngang hàng.
- Mọi engine và consumer dùng `src/docai/core/schema.py` làm shared output contract; không ép Contract vào field Invoice.
- FastAPI là backend/API; Plotly Dash là frontend web; không thêm frontend framework khác ở phase hiện tại.
- Product Engineering tạo đường chạy upload → processing → structured output → risk/explainability → API/UI.
- Research & Evaluation chạy song song để so sánh hai engine trên Invoice và Contract, nhưng không được thay thế product identity.
- Chỉ gắn nhãn Implemented/Baseline khi code và test/runtime evidence hỗ trợ. Phần chưa chạy phải ghi `SCAFFOLD`, `PLANNED` hoặc `CHƯA CHỐT MODEL CỤ THỂ`.

## 1. Track A — AI/ML/DL

Owner chính: thành viên mạnh AI/ML/DL; phối hợp với Product Engineering ở schema, interfaces và integration.

- Layout Detection và model-specific preprocessing.
- OCR, tokenization, bounding-box normalization.
- KIE với LayoutLMv3 và BIO tagging.
- Fine-tuning/inference, checkpoint management và phân tích lỗi model.
- Robustness ở cấp model và hỗ trợ VLM experimentation khi cần.
- Bàn giao output theo `UnifiedDocumentOutput`, không bàn giao output tùy tiện cho API/Dash.

Trạng thái hiện tại: `layout_detection.py`, `ocr_extraction.py` và `kie_layoutlmv3.py` là `SCAFFOLD`; model/checkpoint cụ thể chưa chốt.

## 2. Track B — VLM/Integration

Owner chính: thành viên thiên Data Engineering/Integration phối hợp với thành viên AI/ML khi thiết kế prompt và đánh giá model.

- Input preparation cho ảnh/PDF và batch processing.
- Structured prompt, structured response và field/clause mapping cho Invoice/Contract.
- Parsing JSON, schema validation, retry/error handling và latency logging.
- Quản lý endpoint/model runner local hoặc Modal sau khi model được chốt.
- Bàn giao output theo `UnifiedDocumentOutput`.

Trạng thái hiện tại: `vlm_parser.py` có prompt interface; inference, parsing thật, retry và model cụ thể là `SCAFFOLD`/`PLANNED`.

## 3. Product Engineering

Owner chính: thành viên thiên Data Engineering/Integration; phối hợp với Track A/B và Research.

- Data ingestion, preprocessing, normalization và quản lý `raw/interim/processed`.
- Shared schema, validation, serialization và pipeline orchestration.
- Invoice Workspace và Contract Workspace trong Plotly Dash.
- FastAPI request validation, upload interface, invocation, error handling và REST responses.
- Domain risk: Invoice arithmetic/missing-field/low-confidence; Contract missing-clause/clause-risk.
- Explainability evidence: Invoice bounding box/confidence; Contract text span/clause location/supporting passage.
- Docker, CLI scripts, logging, local outputs, integration tests và documentation.

Boundary bắt buộc:

```text
Plotly Dash (Frontend) → FastAPI (Backend) → docai pipelines → core schema
```

Dash không chứa processing logic; FastAPI route không chứa model implementation. Không thêm React/Vue/Angular/Next.js, Power BI, PostgreSQL, Redis, Kafka, Celery, Airflow, Kubernetes, microservices hoặc OAuth khi chưa có requirement.

Trạng thái hiện tại: schema và một số risk rules có baseline code/test; API parse handlers, orchestration, Dash callbacks và end-to-end product flow là `SCAFFOLD`.

## 4. Research & Evaluation

Owner: A + B cùng phối hợp; A phụ trách runtime/data collection, B phụ trách metrics, experimental design và analysis.

- Chuẩn bị ground truth và protocol so sánh công bằng.
- Đo Precision/Recall/F1, field agreement, latency, robustness, explainability evidence và cost.
- So sánh riêng Invoice và Contract; phân tích clean/noisy documents.
- Dùng CUAD cho Contract Information Extraction, Clause Classification/Detection, Contract Risk Analysis và generalization research.
- Duy trì Research Lab và báo cáo; không đưa benchmark vào product parse flow bắt buộc.
- Không kết luận winner nếu chưa có output thật, ground truth và số liệu thực nghiệm.

Research question:

> Khi cùng phục vụ một sản phẩm Document Intelligence cho hóa đơn và hợp đồng, pipeline Classic modular và pipeline VLM-native đánh đổi như thế nào về accuracy, latency, robustness, explainability và cost?

Trạng thái hiện tại: metric helpers có code; benchmark runner và report là scaffold/template, chưa có benchmark thật, mock result hoặc dataset được tải trong task này.

## Phân chia theo domain

### Invoice Intelligence

- Product: fields, validation, arithmetic risk, confidence và end-to-end review.
- Track A/B: xử lý hóa đơn ở mức capability của từng engine.
- Research: so sánh field extraction trên tài liệu ngắn, nhiều số và bảng.

### Contract Intelligence

- Product: metadata, clause spans/categories, missing-clause và Contract Risk.
- Track A/B: xử lý hợp đồng khi input, context length và schema mapping đáp ứng.
- Research: CUAD taxonomy, clause detection và generalization trên tài liệu dài/pháp lý.

Contract là product domain thật, không phải secondary use case. Taxonomy CUAD đầy đủ và Contract end-to-end chỉ được đánh dấu hoàn thành sau khi code/test chứng minh.

## Roadmap trách nhiệm

1. **Data và shared contract** — Product Engineering lập input layer; A/B chốt mapping và schema envelope.
2. **Track A Classic** — AI/ML/DL triển khai layout/OCR/KIE theo interfaces.
3. **Track B VLM-native** — VLM/Integration triển khai prompt/parser/validation sau khi model được chốt.
4. **Invoice capability** — Product Engineering tích hợp ít nhất một path có structured output và basic risk.
5. **Contract capability** — Product Engineering + A/B map CUAD, clause output và Contract Risk theo schema thực tế; phần chưa đủ là scaffold.
6. **FastAPI backend** — Product Engineering kết nối upload, request validation, orchestration và serialization.
7. **Plotly Dash frontend** — Product Engineering dựng Invoice Workspace, Contract Workspace và Research Lab; không tạo frontend stack mới.
8. **Risk và Explainability** — tích hợp hai domain; phân biệt Invoice Risk với Contract Risk và không overclaim legal/fraud conclusions.
9. **Product MVP** — chỉ hoàn thành khi có ít nhất một đường chạy end-to-end thật qua API/UI.
10. **Research milestone** — A + B chỉ hoàn thành khi có hai output thật, ground truth, metrics, latency, robustness và cost có căn cứ.

## Quy tắc phối hợp

- Thay đổi schema phải được cả A và B review trước khi merge.
- Mỗi task cập nhật `log/progress-log.md` với owner, file và trạng thái thực tế.
- Task dùng chung không gán độc quyền cho A hoặc B nếu cả hai pipeline phụ thuộc.
- Không train model, tải dataset, benchmark giả hoặc triển khai feature lớn trong task điều chỉnh định vị này.
