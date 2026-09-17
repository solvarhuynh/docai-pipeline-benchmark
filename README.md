# Nền tảng DocAI Document Intelligence

DocAI là nền tảng Document Intelligence cho hai domain sản phẩm ngang hàng:

- **Invoice Intelligence** — trích xuất field có cấu trúc từ invoice/receipt, sau đó đưa ra tín hiệu validation và risk.
- **Contract Intelligence** — trích xuất metadata và clause của hợp đồng để hỗ trợ review điều khoản và rủi ro.

Sản phẩm có một backend Python duy nhất là **FastAPI** và một frontend web độc lập là **React + TypeScript + Vite**. Track A và Track B là hai engine AI xử lý bên trong backend; Research so sánh chúng trên Invoice và Contract.

## Luồng sản phẩm

```text
USER → React + TypeScript + Vite → HTTP/REST/JSON → FastAPI
     → DocAI core → Track A hoặc Track B → UnifiedDocumentOutput
     → Domain Risk / Explainability → kết quả review
```

Luồng dự kiến là người dùng chọn Invoice hoặc Contract, upload tài liệu, chọn engine, chạy xử lý rồi xem field/clause, confidence, risk flag và evidence. Repository hiện vẫn là scaffold; chưa tuyên bố luồng end-to-end đã hoàn thành.

## Trạng thái hiện tại

- **Invoice Intelligence — BASELINE / SCAFFOLD:** shared output và một số invoice risk rules đã có; model inference và processing end-to-end chưa bật.
- **Contract Intelligence — BASELINE / SCAFFOLD:** document type và baseline missing-clause rules đã có; taxonomy CUAD đầy đủ và extraction còn planned.
- **Risk Analysis — BASELINE:** các kiểm tra arithmetic/confidence cho Invoice và missing-clause cho Contract có code/test. Đây là tín hiệu review, không phải kết luận fraud hay pháp lý.
- **Explainability — SCAFFOLD:** có interface cho box, clause span và evidence; runtime explanation chưa hoàn thiện.
- **FastAPI API — SCAFFOLD:** contract của route đã có; parse/compare/explain hiện trả `501 Not Implemented`.
- **React frontend — SCAFFOLD:** page structure và typed API boundary đã có; backend call và result view chưa hoàn chỉnh.
- **Research Lab — PLANNED:** chưa có benchmark thật, ground truth result hay metric giả.

## Các trang frontend

- `/` — tổng quan sản phẩm.
- `/invoice` — Invoice Workspace.
- `/contract` — Contract Workspace.
- `/research` — Research Lab cho so sánh Track A/B.

Các trang không được tự tạo extraction result hoặc metric khi backend chưa trả dữ liệu thật.

## Chất lượng tài liệu và Document/Image Preprocessing

Tài liệu ngoài đời có thể là ảnh điện thoại bị nghiêng, tối, mờ, có bóng hoặc chụp xiên. Luồng product hướng tới việc kiểm tra chất lượng đầu vào trước khi gọi engine:

```text
Upload PDF/Image
  ↓
Document Quality Check
  ↓
Document/Image Preprocessing nếu cần
  ↓
Track A hoặc Track B
  ↓
UnifiedDocumentOutput
```

**Document/Image Preprocessing** là việc cố cải thiện tài liệu đầu vào để AI dễ đọc hơn, ví dụ orientation/deskew, crop, perspective correction, điều chỉnh contrast/brightness, denoise, sharpen hoặc resize. Đây khác với **Data Preprocessing**, là việc chuẩn bị dataset, annotation và train/test split cho code/model. Runtime preprocessing hiện chưa có pipeline riêng; trạng thái là `PLANNED` và chỉ nên chốt kỹ thuật sau khi có dữ liệu/thử nghiệm.

## Backend và hai engine

### FastAPI

`src/docai/api/` là business backend duy nhất. FastAPI nhận request/upload, gọi pipeline, serialize Pydantic output và trả lỗi. Node.js chỉ chạy npm, Vite và TypeScript tooling; không phải backend thứ hai.

### Track A — pipeline specialist

```text
Layout Detection → OCR → KIE / LayoutLMv3 → UnifiedDocumentOutput
```

Track A có thể dùng nhiều specialist model cho layout, OCR và document understanding, sau đó mapping riêng cho Invoice/Contract. Model/checkpoint production chưa được chọn.

Track A có thể nhạy hơn với chất lượng ảnh vì OCR/layout detector phụ thuộc vào chữ và biên vùng rõ ràng. Đây là giả thuyết cần Robustness Testing kiểm chứng, không phải kết luận sẵn.

### Track B — pipeline VLM-native

```text
Document → VLM → structured prompt/response → parse → schema validation
```

Track B phụ trách input preparation, prompt, structured parsing, validation, retry và batching. VLM cụ thể chưa được chọn.

Một VLM có thể chịu một số loại noise tốt hơn hoặc kém hơn Track A tùy model. Không suy ra ưu thế từ kiến trúc; cần đo trên cùng protocol.

## Contract giữa backend và frontend

```text
Pydantic schema → FastAPI REST/JSON contract → TypeScript interface → React UI
```

TypeScript type tương ứng nằm ở [`frontend/src/types/document.ts`](frontend/src/types/document.ts). Frontend không đọc Python file và không duplicate AI logic.

## Cấu trúc repository

```text
frontend/                 # React + TypeScript + Vite
src/docai/api/            # FastAPI backend
src/docai/core/           # Pydantic contract/config
src/docai/pipelines/      # Track A và Track B
src/docai/data/           # xử lý dữ liệu
src/docai/fraud/          # domain risk rules
src/docai/explainability/ # evidence scaffold
src/docai/evaluation/     # metrics/research
scripts/                  # Python entry points
tests/                    # unit/integration tests
data/                     # raw/interim/processed
docs/                     # tài liệu
modal_app/                # Modal scaffold
log/                      # progress log
```

## Cài đặt và chạy

### Backend Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
uvicorn docai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

`/health` là route hiện dùng được. Các route parse, compare và explain vẫn là scaffold.

### Frontend React

```powershell
cd frontend
npm install
npm run dev
```

Vite chạy ở `http://localhost:5173` và proxy `/api` tới FastAPI ở port `8000`. Kiểm tra build bằng `npm run build`.

### Test

```powershell
.venv\Scripts\python.exe -m compileall src scripts tests
.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

## Phạm vi Research

Research trả lời câu hỏi: khi Classic specialist pipeline và VLM-native pipeline cùng phục vụ Invoice/Contract, chúng đánh đổi thế nào về accuracy, latency, robustness, explainability và cost?

Invoice có tài liệu ngắn, nhiều số và bảng. Contract có văn bản dài, ngôn ngữ pháp lý và clause phức tạp. CUAD có thể phục vụ cả Contract product và research ground truth.

Research chỉ hoàn thành khi có output thật, ground truth, metric, latency, robustness evidence và cost có căn cứ. Không đọc report scaffold như kết quả thật.

### Robustness Testing

Robustness Testing thuộc Research, không phải preprocessing của product. Test cố tình làm input xấu đi bằng blur, rotation, giảm brightness/contrast, noise, watermark, crop hoặc perspective distortion, rồi đo performance degradation như F1 giảm bao nhiêu:

```text
Ảnh sạch → Artificial Degradation → Track A/B → so sánh performance degradation
```

Nói ngắn gọn: preprocessing cố làm input tốt hơn; robustness test cố làm input xấu hơn để xem hệ thống chịu được đến đâu. Câu hỏi nghiên cứu phụ là: preprocessing có cải thiện Track A và Track B giống nhau không?

## Tài liệu nên đọc

Bắt đầu từ [`docs/architecture/architecture-explained.md`](docs/architecture/architecture-explained.md), sau đó đọc [`docs/concepts/README.md`](docs/concepts/README.md). Roadmap ở [`docs/specs/implementation-guide.md`](docs/specs/implementation-guide.md), phân công ở [`docs/tasks/task-split.md`](docs/tasks/task-split.md), và trạng thái ở [`log/progress-log.md`](log/progress-log.md).

## Ranh giới scope

Task hiện tại không train/fine-tune model, tải dataset, tạo benchmark giả, build production frontend, thêm authentication/database/microservices hoặc deploy production. React/TypeScript/Vite là frontend; FastAPI/Python vẫn là business backend duy nhất.
