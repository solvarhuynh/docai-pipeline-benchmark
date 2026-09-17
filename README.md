# DocAI Document Intelligence Platform

> Invoice + Contract Intelligence với FastAPI, Plotly Dash và dual-pipeline research

DocAI là nền tảng Document Intelligence hướng tới hai product domain:

- **Invoice Intelligence**: trích xuất dữ liệu có cấu trúc từ hóa đơn/biên lai, kiểm tra tính nhất quán và gắn cờ rủi ro.
- **Contract Intelligence**: trích xuất metadata/clauses/law từ hợp đồng, phát hiện thiếu điều khoản và hỗ trợ rà soát rủi ro.

Sản phẩm cung cấp REST API bằng **FastAPI** và giao diện web tương tác bằng **Plotly Dash**. Bên trong processing layer có hai engine: **Track A Classic** và **Track B VLM-native**. Hai engine phục vụ product flow ở mức phù hợp với khả năng thực tế, đồng thời tạo nền tảng cho research benchmark trên Invoice và Contract.

Repository/Git remote hiện tại có thể tiếp tục dùng tên kỹ thuật `docai-pipeline-benchmark`; không tự động rename repository hoặc remote. Display name được định hướng là **DocAI Document Intelligence Platform** để nhấn mạnh giá trị sản phẩm.

## Sản phẩm giải quyết gì?

Luồng sản phẩm mục tiêu:

```text
USER
  ↓
PLOTLY DASH — Frontend / User Interface
  ↓
FASTAPI — Backend / REST API
  ↓
Document input → processing engine → UnifiedDocumentOutput
  ↓
Domain validation / risk → explainability → result review
```

Người dùng có thể chọn loại tài liệu Invoice hoặc Contract, upload tài liệu, nhận kết quả có cấu trúc, xem bằng chứng trích xuất và các cảnh báo cần được con người xem xét. Product MVP không yêu cầu Research Lab hoàn thành trước.

### Product Capabilities và trạng thái

- **Invoice Intelligence — BASELINE / SCAFFOLD**: schema `invoice`/`receipt`, các rule kiểm tra tổng tiền và confidence đã có; pipeline inference và đường chạy end-to-end còn scaffold.
- **Contract Intelligence — BASELINE / SCAFFOLD**: schema envelope hỗ trợ `contract`, rule phát hiện thiếu clause đã có; taxonomy CUAD đầy đủ, extraction và UI end-to-end còn scaffold/planned.
- **Risk Analysis — BASELINE**: `src/docai/fraud/rules.py` có invoice arithmetic/confidence checks và contract missing-clause checks. Đây là risk flagging, không phải kết luận gian lận hay kết luận pháp lý.
- **Explainability — SCAFFOLD**: interface cho bounding box, text/clause evidence, attention/grounding; implementation heatmap chưa hoàn thành.
- **FastAPI REST API — SCAFFOLD**: route và response contract đã định nghĩa; parse/compare/explain hiện chưa điều phối pipeline thật.
- **Plotly Dash — SCAFFOLD**: layout và các workspace/tab định hướng đã có; callbacks và dữ liệu thật chưa có.
- **Dual processing engine — SCAFFOLD**: interface Track A/Track B đã có; model inference thực tế chưa chạy trong repository hiện tại.

## Hai product workspace

### Invoice Workspace

Luồng mục tiêu là:

```text
Upload invoice / receipt
  → document processing
  → fields + confidence + bounding boxes
  → arithmetic / missing-field / low-confidence risk flags
  → structured JSON và explainability
```

Các field chỉ được dùng khi schema/dataset thực tế hỗ trợ, chẳng hạn `seller_name`, `invoice_date`, `subtotal_amount`, `tax_amount`, `total_amount` và `line_items`.

### Contract Workspace

Luồng mục tiêu là:

```text
Upload contract
  → document processing
  → metadata + clause spans
  → missing-clause / clause-risk flags
  → structured JSON và supporting passages
```

Các thông tin có thể bao gồm parties, effective date, termination, governing law, confidentiality, liability và các clause quan trọng. Taxonomy cụ thể phải bám schema/dataset; phần chưa có implementation được ghi là `SCAFFOLD` hoặc `PLANNED`. Hệ thống hỗ trợ information extraction, document review và decision support; không thay luật sư và không đưa ra tư vấn pháp lý chắc chắn.

## Product và Research khác nhau thế nào?

Product dùng một engine đã chọn để xử lý một tài liệu và trả kết quả cho người dùng. Research Lab là khu vực riêng trong frontend, dùng khi cần chạy hai engine trên cùng input/ground truth để đo:

- accuracy, Precision/Recall/F1;
- latency;
- robustness trên tài liệu clean/noisy;
- explainability evidence;
- cost hoặc estimate có căn cứ;
- agreement/disagreement giữa hai engine.

Research question chính:

> Khi cùng phục vụ một sản phẩm Document Intelligence cho hóa đơn và hợp đồng, pipeline Classic modular và pipeline VLM-native đánh đổi như thế nào về accuracy, latency, robustness, explainability và cost?

Invoice và Contract tạo ra hai điều kiện khác nhau: Invoice thường ngắn, nhiều con số, bảng biểu và field tương đối rõ; Contract thường dài, giàu ngôn ngữ pháp lý, clause và quan hệ ngữ nghĩa phức tạp. Vì vậy CUAD có vai trò kép: hỗ trợ Contract Information Extraction/Clause Detection/Risk Analysis trong product và cung cấp dữ liệu cho generalization research. CUAD không phải dataset phụ bị hạ vai trò, nhưng cũng không được dùng để tuyên bố đã có capability khi code chưa triển khai.

Research milestone chỉ được gọi là hoàn thành khi có output thật từ cả hai track, ground truth, metrics, latency, robustness và cost measurement/estimate có căn cứ. Repository hiện chưa có benchmark thật và không dùng mock result để thay thế.

## Kiến trúc tổng quan

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

Vai trò module:

- `src/docai/api/` — **Backend** FastAPI: request validation, upload interface, pipeline invocation, serialization và error handling. Route không chứa model implementation.
- `src/docai/dashboard/` — **Frontend** Plotly Dash: Invoice Workspace, Contract Workspace và Research Lab. UI đọc output chuẩn hoá; không copy processing logic.
- `src/docai/core/` — shared contracts/configuration.
- `src/docai/pipelines/` — Track A và Track B processing engines.
- `src/docai/data/` — data ingestion, preprocessing và statistics.
- `src/docai/fraud/` — domain-specific validation/risk rules.
- `src/docai/explainability/` — evidence/explanation layer.
- `src/docai/evaluation/` — research metrics và comparison orchestration.

### Unified schema

[`src/docai/core/schema.py`](src/docai/core/schema.py) hiện là một shared envelope tối thiểu gồm `document_type`, `fields`, confidence, optional `bounding_box`, `risk_flags`, execution metadata và pipeline metadata. Envelope này không ép Contract vào schema Invoice: field names/values có thể khác theo domain. Taxonomy Contract chi tiết hơn sẽ được bổ sung sau khi schema/dataset mapping được chốt; task hiện tại không thiết kế một schema lớn mới.

Backend, Dash và Evaluation phải phụ thuộc vào contract này thay vì output tùy tiện của từng model.

## Hai processing engine

### Track A — Classic Document AI Pipeline

```text
Layout Detection → OCR → KIE / LayoutLMv3 → UnifiedDocumentOutput
```

Đây là khu vực AI/ML/DL chuyên sâu, phù hợp cho layout detection, OCR, BIO tagging, fine-tuning và phân tích lỗi từng chặng. Model/checkpoint cụ thể vẫn chưa được chốt; các class hiện tại là scaffold.

### Track B — VLM-native Document AI Pipeline

```text
Document → VLM → structured prompt/response → parsing → schema validation
```

Đây là khu vực VLM và integration: input preparation, prompt, structured output, parsing, validation, retry/error handling và batch processing. Model cụ thể cho Track B chưa được chốt; không tự chọn checkpoint mới trong task này.

Cả hai track là processing backend dùng chung cho Invoice và Contract ở mức khả năng thực tế, không phải hai sản phẩm riêng.

## Công nghệ và phạm vi hiện tại

- Python, Pydantic và package `src/` layout.
- FastAPI là backend/API chính thức.
- Plotly Dash là frontend web/MVP chính thức; không thêm React, Vue, Angular, Next.js hoặc Power BI ở phase hiện tại.
- Docker Compose và file/local outputs cho local development.
- Không thêm PostgreSQL, Redis, Kafka, Celery, Airflow, Kubernetes, microservices hoặc OAuth khi chưa có requirement.
- Chưa train model, chưa tải dataset và chưa chạy benchmark thật trong task định vị này.

## Cấu trúc repository

```text
docai-pipeline-benchmark/
├── src/docai/
│   ├── core/             # Shared contracts và config
│   ├── data/             # Data layer
│   ├── pipelines/        # track_a và track_b
│   ├── fraud/            # Invoice risk và Contract risk
│   ├── explainability/   # Evidence/explanation scaffold
│   ├── evaluation/       # Research metrics/comparison
│   ├── api/              # FastAPI backend
│   └── dashboard/        # Plotly Dash frontend
├── scripts/              # CLI entry points
├── tests/                # Unit/integration tests
├── data/                 # raw/interim/processed; chưa chứa dataset thật
├── docs/
│   ├── architecture/    # Architecture và data dictionary
│   ├── concepts/        # Kỹ thuật nối với product/research
│   ├── guides/          # Cách chạy và protocol
│   ├── reports/         # Report scaffold, không phải benchmark result thật
│   └── specs/           # Roadmap và task split
├── modal_app/            # Modal scaffold
├── log/                  # Progress log
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Cách chạy local

```bash
pip install -e .
pytest
uvicorn docai.api.main:app --host 0.0.0.0 --port 8000 --reload
python -c "from docai.dashboard.app import create_dashboard_app; print(create_dashboard_app())"
docker compose up --build
```

`/health` là route có hành vi runtime; các route `/parse/classic`, `/parse/vlm`, `/compare` và `/explain` hiện trả `501 Not Implemented` vì orchestration/inference chưa hoàn thành. Dashboard hiện là layout scaffold, chưa có callbacks hoặc dữ liệu thật. Xem [`docs/guides/how-to-run.md`](docs/guides/how-to-run.md) để biết giới hạn từng lệnh.

## Roadmap

Roadmap chi tiết và Definition of Done nằm trong [`docs/specs/implementation-guide.md`](docs/specs/implementation-guide.md). Trình tự product-first là:

```text
Data/input → shared schema → Track A / Track B
→ Invoice capability + Contract capability
→ FastAPI integration → Dash MVP
→ domain risk + explainability
→ end-to-end Product MVP
→ Research benchmark → robustness / cost study
```

Product MVP cần ít nhất một đường chạy end-to-end thật cho upload, processing, structured output, basic risk và API/UI. Research Complete là milestone riêng và không được suy ra tự động từ Product MVP.

## Tài liệu tiếp theo

- [System architecture](docs/architecture/architecture-explained.md)
- [Repository structure](docs/architecture/repository-structure.md)
- [Concept map](docs/concepts/README.md)
- [Task split](docs/specs/task-split.md)
- [Implementation guide và roadmap](docs/specs/implementation-guide.md)
- [Progress log](log/progress-log.md)
