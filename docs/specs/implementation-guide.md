# Implementation guide và roadmap — DocAI

## Mục tiêu

DocAI là sản phẩm Document Intelligence cho hai domain ngang hàng: **Invoice Intelligence** và **Contract Intelligence**. Sản phẩm nhận tài liệu, trích xuất structured output, kiểm tra validation/risk, cung cấp FastAPI backend và hiển thị qua Plotly Dash frontend.

Track A Classic và Track B VLM-native là hai processing engine bên trong product. Research/Evaluation chạy song song để trả lời cách hai engine đánh đổi accuracy, latency, robustness, explainability và cost trên Invoice và Contract.

Model/checkpoint cụ thể của Track A và Track B chưa chốt. Task định vị này không train model, tải dataset, chạy benchmark hoặc triển khai feature lớn.

## Product MVP và Research milestone

### Product MVP

Product MVP được xem là đạt khi ít nhất một đường chạy thực tế thực hiện được:

```text
User mở Plotly Dash
  → upload Invoice hoặc Contract
  → FastAPI nhận request
  → chọn/chạy một processing engine
  → UnifiedDocumentOutput
  → domain risk cơ bản
  → hiển thị fields/clauses, evidence và JSON
```

MVP không cần toàn bộ benchmark/research capability hoàn thành. Hiện Product MVP chưa đạt: API parse, pipeline inference, orchestration và Dash callbacks còn scaffold.

### Research Complete

Research milestone độc lập với Product MVP. Chỉ đánh dấu đạt khi có:

- output thật của Track A và Track B;
- ground truth cho Invoice và/hoặc Contract;
- accuracy/Precision/Recall/F1;
- latency đo được;
- robustness test trên clean/noisy input;
- explainability evidence và cost measurement/estimate có căn cứ.

Không dùng mock result hoặc Product MVP để tự động suy ra Research PASS.

## Roadmap product-first

### Giai đoạn 1 — Data và input foundation

- Tổ chức ingestion, preprocessing và normalization cho dữ liệu Invoice và Contract.
- Map nhãn/field của các dataset được phê duyệt; CUAD phải giữ span/clause semantics.
- Hoàn thiện data dictionary và ghi số liệu chỉ sau khi dữ liệu thật được tải/khảo sát.

Definition of Done: input layer và mapping có evidence; không tuyên bố dataset đã tải nếu thư mục chỉ có placeholder.

### Giai đoạn 2 — Core contract và package foundation

- Duy trì `src/docai/` layout, Pydantic schema và config.
- Giữ shared envelope đủ nhỏ cho common metadata, field values, confidence, evidence và risk flags.
- Chỉ mở rộng domain-specific schema khi Invoice/Contract mapping đã rõ.

Definition of Done: Track A/B và consumer có boundary rõ quanh `UnifiedDocumentOutput`.

### Giai đoạn 3 — Track A: Layout Detection và OCR

- Tích hợp candidate pretrained layout model và OCR cho tài liệu phù hợp.
- Trả token/text/bounding box qua interface nội bộ.
- Chuẩn bị đường map output về shared schema.

Đây là AI/ML/DL work; code hiện tại là `SCAFFOLD`.

### Giai đoạn 4 — Track A: KIE/LayoutLMv3

- Chuẩn bị BIO tagging, fine-tuning/inference và field aggregation.
- Đánh giá trên ground truth riêng khi có data thật.
- Ghi checkpoint, runtime và cost có căn cứ.

Không fine-tune trong task định vị hiện tại; checkpoint cụ thể chưa chốt.

### Giai đoạn 5 — Track B: VLM-native parsing

- Chốt model sau khi có requirement và kiểm tra khả năng triển khai.
- Xây input preparation, structured prompt, structured response, parser và Pydantic validation.
- Bổ sung retry/error handling, batch processing và latency logging.

Code hiện tại mới là prompt/interface scaffold; không coi candidate model là model đã chọn.

### Giai đoạn 6 — Contract Intelligence với CUAD

Contract là product domain ngang hàng, đồng thời CUAD phục vụ research. Work cần làm:

- map CUAD SQuAD-style spans thành clause fields/evidence;
- xác định taxonomy được hỗ trợ trong từng phase;
- phục vụ metadata, important clauses, clause categories và structured output;
- chạy Track A/B trên Contract khi input/context/schema đã đáp ứng;
- tách capability product khỏi generalization comparison trong report.

Nếu taxonomy chưa đủ hoặc chưa có inference thật, ghi `SCAFFOLD`/`PLANNED`, không ghi như capability hoàn thành.

### Giai đoạn 7 — Domain Risk và validation

- **Invoice Risk**: subtotal/tax/total arithmetic consistency, missing important field, low confidence và amount inconsistency.
- **Contract Risk**: missing important/required clause, unusual/inconsistent clause và metadata inconsistency khi có cơ sở.
- Expose `risk_flags` qua shared output.

Không gọi Contract Risk là fraud nếu evidence chỉ cho thấy thiếu clause. Không đưa ra kết luận hợp đồng hợp pháp/bất hợp pháp.

Baseline invoice/contract rules hiện có trong `src/docai/fraud/rules.py`; mở rộng taxonomy và currency handling thuộc phase sau.

### Giai đoạn 8 — Explainability cho cả hai domain

- Invoice: field bounding box, highlighting và confidence.
- Contract: text span, page/clause location và supporting passage.
- Attention/visual grounding/Grad-CAM chỉ được xem là explanation khi implementation và validation chứng minh được; không đồng nhất attention với explanation hoàn hảo.

`src/docai/explainability/explainer.py` hiện là scaffold.

### Giai đoạn 9 — Research evaluation

- Đánh giá hai track trên cùng protocol/ground truth khi có thể.
- Báo cáo riêng Invoice và Contract; clean/noisy robustness; agreement/disagreement.
- Đo accuracy, Precision/Recall/F1, latency, robustness, explainability evidence và cost.
- Chỉ kết luận trade-off theo số liệu thật, không dự đoán winner từ kiến trúc.

`src/docai/evaluation/` hiện có metric helpers; benchmark execution và reports vẫn là scaffold/template.

### Giai đoạn 10 — Product integration

- FastAPI: request validation, upload, pipeline invocation, serialization và error handling.
- Plotly Dash: Invoice Workspace, Contract Workspace và Research Lab.
- Docker/CLI/logging và integration tests.
- Kết nối một end-to-end Product MVP trước khi mở rộng toàn bộ Research Lab.

Không thêm React/Vue/Angular/Next.js, Power BI hay hạ tầng phân tán mới nếu chưa có requirement.

## Trạng thái repository hiện tại

- `src/docai/core/schema.py`: shared Pydantic envelope; có `DocumentType.CONTRACT`, nhưng chưa phải Contract taxonomy đầy đủ.
- `src/docai/fraud/rules.py`: baseline rules có code và test cho invoice risk và một nhóm contract missing-clause flags.
- `src/docai/api/main.py`: route scaffold; `/health` hoạt động, parse/compare/explain trả 501.
- `src/docai/dashboard/app.py`: Plotly Dash layout scaffold; chưa có callback/dữ liệu thật.
- `src/docai/pipelines/`: Track A/B scaffold; chưa có model inference thật.
- `src/docai/explainability/`: scaffold; chưa có heatmap runtime.
- `src/docai/evaluation/`: metric helpers và comparison scaffold; chưa có benchmark thật.
- `data/`: chưa tải dataset trong task này.

## Quy tắc Definition of Done

Mỗi phase phải ghi rõ code, test/runtime evidence và giới hạn. `Implemented` chỉ dùng khi hành vi thật đã được kiểm thử; `Baseline` dùng cho logic nhỏ đã có code/test; `SCAFFOLD` dùng cho interface/TODO; `PLANNED` dùng cho việc chưa bắt đầu; model chưa chọn phải ghi `CHƯA CHỐT MODEL CỤ THỂ`.

## Thứ tự delivery logic

Số phase 1–10 được giữ để không làm vỡ các reference cũ, nhưng dependency của Product MVP được đọc theo thứ tự:

```text
Data/input
  → Core schema
  → Track A / Track B
  → Invoice capability + Contract capability
  → FastAPI integration
  → Plotly Dash MVP
  → Domain Risk / Explainability
  → End-to-end Product MVP
  → Research benchmark
  → Robustness / Cost research
```

Vì vậy một phase có thể chuẩn bị code trước khi phase tích hợp được thực thi; chỉ đường chạy đã tích hợp và kiểm thử mới được gọi là Product MVP. Research vẫn là milestone riêng.

Các reference cũ vẫn giữ số phase 1–10 để link không bị vỡ. `docs/specs/docai-benchmark-overview.pdf` là tài liệu lịch sử/tham chiếu; các tài liệu Markdown hiện hành là source of truth cho product-first direction.
