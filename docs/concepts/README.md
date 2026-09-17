# Bản đồ khái niệm kỹ thuật — DocAI

Khu vực `docs/concepts/` giải thích kỹ thuật theo product flow của DocAI: một nền tảng **Invoice Intelligence + Contract Intelligence** có FastAPI backend, Plotly Dash frontend và hai processing engine. Mỗi kỹ thuật phải được nối về module, output schema, product capability và research metric tương ứng.

## Product flow và Research flow

Product flow cho cả hai domain:

```text
User → Plotly Dash → FastAPI
                   ↓
        Invoice hoặc Contract
                   ↓
        Track A hoặc Track B
                   ↓
        UnifiedDocumentOutput
                   ↓
        Domain Risk → Explainability → Review
```

Hai workspace sản phẩm:

- **Invoice Workspace**: fields, confidence, bounding boxes, structured JSON và Invoice Risk.
- **Contract Workspace**: metadata, clause spans/categories, structured JSON và Contract Risk.

Research Lab là khu vực riêng:

```text
Track A output ─┐
                ├→ Evaluation → accuracy / latency / robustness / explainability / cost
Track B output ─┘
```

Product và Research hỗ trợ nhau nhưng là hai mục tiêu khác nhau. CUAD giữ vai trò kép cho Contract capability và generalization research; không gọi Contract là dataset phụ.

## Trạng thái cần đọc đúng

- `ĐÃ CHỐT`: Pydantic shared envelope, FastAPI backend, Plotly Dash frontend và Track A/B là processing engines.
- `BASELINE`: schema/risk/metric logic nhỏ đã có code và test tương ứng.
- `SCAFFOLD`: class/interface/TODO đã dựng nhưng chưa có runtime implementation đầy đủ.
- `PLANNED`: có trong roadmap nhưng chưa bắt đầu.
- `CHƯA CHỐT MODEL CỤ THỂ`: hướng model còn là candidate, chưa phải lựa chọn chính thức.

Repository hiện chưa có model inference end-to-end, callback Dashboard, benchmark thật hoặc dataset được tải trong task định vị này.

## Thứ tự đọc khuyến nghị

1. [`01-docai-foundations.md`](./01-docai-foundations.md): bài toán Document Intelligence, shared schema và hai domain.
2. [`02-track-a-classic.md`](./02-track-a-classic.md): Layout Detection, OCR, KIE và LayoutLMv3 trong Track A.
3. [`03-track-b-vlm.md`](./03-track-b-vlm.md): VLM-native parsing, prompt, structured output và failure modes của Track B.
4. [`04-fraud-and-explainability.md`](./04-fraud-and-explainability.md): Invoice Risk, Contract Risk và evidence/explainability.
5. [`05-evaluation.md`](./05-evaluation.md): metrics và protocol Research Lab.

Đọc kèm [`docs/architecture/architecture-explained.md`](../architecture/architecture-explained.md), [`docs/specs/task-split.md`](../specs/task-split.md) và [`docs/specs/implementation-guide.md`](../specs/implementation-guide.md) để hiểu boundary và roadmap.

## Theo vai trò

- AI/ML/DL: đọc foundations → Track A → Track B → evaluation.
- Data/Integration/Product: đọc foundations → architecture → risk/explainability → how-to-run.
- Product/BA: đọc foundations → hai workspace → risk/explainability → roadmap.
