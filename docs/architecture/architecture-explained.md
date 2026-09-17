# Tổng quan hệ thống — DocAI được ghép như thế nào?

DocAI là sản phẩm Document Intelligence cho Invoice Intelligence và Contract Intelligence. Research Lab là khu vực riêng để so sánh hai cách xử lý.

## Luồng người dùng

```text
Người dùng mở React
  ↓ upload Invoice hoặc Contract
React gửi HTTP/REST/JSON tới FastAPI
  ↓
FastAPI gọi pipeline DocAI
  ↓
Pipeline trả UnifiedDocumentOutput
  ↓
React hiển thị field, clause, risk flag và evidence
```

Có thể hình dung frontend là quầy tiếp nhận, còn backend là căn bếp. Frontend nhận thao tác và hiển thị kết quả; backend mới thực hiện xử lý. React không chạy model và FastAPI là business backend duy nhất.

## Vai trò của từng phần

### Frontend — `frontend/`

Frontend là phần người dùng nhìn thấy và bấm vào, được xây bằng React + TypeScript + Vite. React ghép giao diện từ component; TypeScript mô tả hình dạng dữ liệu; Vite chạy dev server/build; HTML/CSS tạo cấu trúc và kiểu dáng. Node.js chỉ chạy npm, Vite và TypeScript compiler, không phải backend thứ hai.

Scaffold hiện có các route `/`, `/invoice`, `/contract`, `/research` và không hiển thị extraction result/metric giả.

### Backend — `src/docai/api/`

Backend nhận upload, kiểm tra request, gọi pipeline và trả JSON. **API** là bộ quy tắc để hai phần mềm giao tiếp; **REST** là cách dùng HTTP để tổ chức các request đó. Route dự kiến gồm `/parse/classic`, `/parse/vlm`, `/compare` và `/explain`; parse/compare/explain hiện còn scaffold và trả `501 Not Implemented`.

### Core contract — `src/docai/core/`

JSON là định dạng text để trao đổi dữ liệu có cấu trúc. Pydantic kiểm tra dữ liệu Python theo schema đã khai báo. `UnifiedDocumentOutput` là contract chung giữa pipeline, FastAPI và frontend; TypeScript mirror nằm ở `frontend/src/types/document.ts`.

### AI processing — `src/docai/pipelines/`

```text
Track A: Layout Detection → OCR → KIE → output có cấu trúc
Track B: Document → VLM → response có cấu trúc → validation
```

Inference là việc dùng model đã học để xử lý tài liệu mới. Hai track hiện mới có interface/scaffold, chưa bật inference thật.

### Data, risk và research

`src/docai/data/` nạp/làm sạch dữ liệu, không thuộc React. `src/docai/fraud/` chứa rule risk theo domain: Invoice Risk kiểm tra arithmetic/missing field/low confidence; Contract Risk đánh dấu clause cần review. Risk flag không phải bằng chứng fraud hay tư vấn pháp lý.

`src/docai/evaluation/` phục vụ Research, dùng ground truth thật để đo Precision, Recall, F1, latency, cost, robustness và agreement. Research tách khỏi luồng xử lý một tài liệu của product.

## Sơ đồ kiến trúc

```text
                    USER
                      │
                      ▼
              React Frontend
         TypeScript + HTML + CSS
                      │ REST/JSON
                      ▼
                  FastAPI
                      │
                      ▼
               DocAI Core
                 /      \
             Track A   Track B
              Classic    VLM
                 \      /
              UnifiedDocumentOutput
                      │
               Risk / Evidence
```

Research chạy song song:

```text
Track A output ─┐
                ├→ Evaluation → accuracy/latency/robustness/cost
Track B output ─┘
```

## Hai domain sản phẩm

Invoice Workspace sẽ hướng tới upload invoice/receipt, chọn engine, xem field, confidence, box, risk flag và JSON. Contract Workspace sẽ xem metadata, clause span, supporting text và Contract Risk. CUAD phục vụ cả Contract product và research, không phải use case phụ.

## Trạng thái

- **Baseline:** Pydantic schema, config, risk rules và một số metric helper.
- **Scaffold:** React pages, FastAPI routes, Track A/B interfaces và explainability interface.
- **Planned:** model inference thật, orchestration, result view, taxonomy Contract đầy đủ và evaluation thật.

Task này không thêm Express/NestJS, Redux, database, authentication hay microservices.
