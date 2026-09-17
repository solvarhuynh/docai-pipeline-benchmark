# Hướng dẫn triển khai và lộ trình — DocAI

DocAI là sản phẩm Document Intelligence cho hai domain ngang hàng: Invoice Intelligence và Contract Intelligence. Sản phẩm nhận tài liệu, trích xuất field/clause, validate kết quả, thêm tín hiệu risk và cung cấp evidence để người dùng review.

```text
React + TypeScript + Vite
        ↓ HTTP/REST/JSON
FastAPI / Python
        ↓
DocAI core → Track A hoặc Track B
        ↓
UnifiedDocumentOutput → risk/evidence → giao diện review
```

Node.js chỉ chạy `npm`, Vite và TypeScript compiler; không phải business backend thứ hai.

## Product MVP là gì?

MVP cần ít nhất một luồng thật: user mở giao diện, upload Invoice/Contract, FastAPI nhận request, một engine thật xử lý, Pydantic validate `UnifiedDocumentOutput`, risk/evidence được gắn vào và React hiển thị kết quả. Hiện parse handler và model inference chưa kết nối nên MVP chưa hoàn thành.

## Research Complete là gì?

Research là milestone riêng, cần output thật của Track A/B, ground truth, accuracy field/clause, latency đo được, robustness clean/noisy, evidence analysis và cost measurement hoặc estimate có giả định rõ. Không điền số giả vào report.

## Roadmap

1. **Input/data foundation:** quy định ảnh/PDF, preprocessing, raw/interim/processed và mapping dataset cho Invoice/Contract; giữ đúng semantics clause của CUAD.
2. **Shared core contract:** duy trì package `src/docai`, config và Pydantic schema; không ép taxonomy Contract thành taxonomy Invoice.
3. **Track A layout/OCR:** tích hợp layout model và OCR được duyệt, trả token/text/box qua interface. Hiện là `SCAFFOLD`.
4. **Track A KIE:** triển khai document understanding, LayoutLMv3 hoặc lựa chọn tương đương, BIO, aggregation và checkpoint/inference test. Fine-tune là phase sau.
5. **Track B VLM:** chọn model sau khi rõ requirement/deployment; làm input preparation, structured prompt, parser, schema validation, retry và latency logging.
6. **Contract Intelligence/CUAD:** map metadata, clause category, text span và page evidence; ghi rõ taxonomy/context limit.
7. **Risk/validation:** Invoice Risk kiểm tra arithmetic, missing field và confidence; Contract Risk đánh dấu clause thiếu/bất thường. Risk flag không phải kết luận fraud hay pháp lý.
8. **Evidence/explainability:** Invoice dùng box/highlight/confidence; Contract dùng span/page/supporting passage. Attention/heatmap chỉ là diagnostic evidence.
9. **Research evaluation:** dùng cùng workload/protocol, report riêng Invoice và Contract với Precision, Recall, F1, latency, robustness, evidence, cost và agreement.
10. **Product integration:** nối FastAPI upload/orchestration/serialization/error handling với React pages và integration tests; hoàn thành một đường end-to-end trước khi mở rộng Research Lab.

## Trạng thái repository

- `src/docai/core/`: Pydantic contract và configuration baseline.
- `src/docai/fraud/`: domain risk rules baseline có test.
- `src/docai/api/main.py`: `/health` dùng được; parse/compare/explain trả `501` scaffold.
- `src/docai/pipelines/`: interface Track A/B, chưa có production inference.
- `src/docai/explainability/`: evidence scaffold.
- `src/docai/evaluation/`: metric/comparison helper, chưa có benchmark thật.
- `frontend/`: React/TypeScript/Vite scaffold, không có kết quả giả.
- `data/`: task này chưa tải dataset.

Từ điển trạng thái và phân công chi tiết nằm ở [`docs/concepts/README.md`](../concepts/README.md), [`docs/guides/glossary.md`](../guides/glossary.md) và [`docs/tasks/task-split.md`](../tasks/task-split.md).
