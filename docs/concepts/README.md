# Bản đồ tri thức kỹ thuật (Concept Map) — DocAI Product & Research

Chào mừng bạn đến với khu vực tài liệu giải thích kiến trúc, thuật toán và khái niệm kỹ thuật của **DocAI Document Intelligence Platform**.

Nếu bạn là người mới tiếp cận hệ thống, tài liệu này được thiết kế như một **bản đồ lộ trình học tập**. Hãy bắt đầu từ Product flow xử lý hóa đơn/biên lai, sau đó đi vào hai processing engine và cuối cùng là Research Lab dùng chung output để benchmark.

---

## 1. Product flow và Research flow khác nhau như thế nào?

Product flow ưu tiên biến một ảnh/PDF hóa đơn hoặc biên lai thành JSON có cấu trúc, có thể kiểm tra rủi ro và hiển thị cho người dùng:

```text
[ Upload Invoice / Receipt ]
              ↓
[ Input validation & normalization ]
              ↓
      +-------+-------+
      |               |
 [ Track A ]      [ Track B ]
 Layout → OCR →   VLM → Prompt
 KIE                → JSON
      |               |
      +-------+-------+
              ↓
[ UnifiedDocumentOutput ]
              ↓
[ Validation → Risk/Fraud → Explainability ]
              ↓
[ FastAPI → Plotly Dash ]
```

Research flow dùng output chung để trả lời câu hỏi về trade-off giữa hai engine:

```text
Track A output ─┐
                ├→ Evaluation → Benchmark → Robustness/Cost reports
Track B output ─┘
```

Contract/CUAD đi qua các contract/module tương tự nhưng là secondary research use case, không phải product MVP thứ hai.

---

## 2. Thứ tự đọc khuyến nghị

Để nắm bắt dự án một cách tự nhiên và có hệ thống, bạn nên đọc các bài viết theo trình tự sau:

### Bước 0: Nắm vững quy chuẩn giải thích
- [`explanation-style.md`](./explanation-style.md): Quy ước bắt buộc về cách viết tài liệu kỹ thuật trong repo — giải thích bằng ví dụ đời thường, dẫn dắt bằng câu hỏi, trực giác trước công thức sau, và minh bạch về trạng thái implementation.

### Bước 1: Nền tảng Document AI
- [`01-docai-foundations.md`](./01-docai-foundations.md):
  - Document AI là gì và tại sao tài liệu quét không đơn giản là một bức ảnh?
  - Các tầng thông tin: từ pixel thô đến cấu trúc bảng biểu và ngữ nghĩa nghiệp vụ.
  - Tọa độ hộp giới hạn (Bounding Box) và kỹ thuật chuẩn hoá không gian.
  - Tại sao hai processing engine trong cùng product bắt buộc phải nói cùng một ngôn ngữ đầu ra (`UnifiedDocumentOutput`)?

### Bước 2: Đi sâu vào Track A — Hướng tiếp cận Cổ điển đa tầng
- [`02-track-a-classic.md`](./02-track-a-classic.md):
  - Phân vùng bố cục (Layout Detection) bằng mô hình thị giác máy tính.
  - Đọc chữ bằng OCR (Optical Character Recognition) và lý do vì sao chỉ đọc được chữ vẫn chưa hiểu được tài liệu.
  - Trích xuất thông tin then chốt (KIE - Key Information Extraction).
  - Khám phá chuyên sâu mô hình LayoutLMv3: Sự kết hợp giữa chữ, vị trí 2D và đặc trưng thị giác; cơ chế đánh nhãn thực thể BIO.

### Bước 3: Đi sâu vào Track B — Hướng tiếp cận VLM-native đơn nhất
- [`03-track-b-vlm.md`](./03-track-b-vlm.md):
  - Vision-Language Model (VLM) là gì và tại sao nó có thể "nhìn một lượt" trả về JSON?
  - Kỹ thuật điều hướng suy luận bằng Structured Prompt.
  - Rủi ro ảo giác (Hallucination) và thách thức về tài nguyên tính toán (GPU VRAM lớn).
  - So sánh triết lý kiến trúc giữa Track A (kiểm soát từng khâu, chia để trị) và Track B (hợp nhất, tổng quát hoá mạnh mẽ).

### Bước 4: Kiểm tra gian lận và Minh bạch hoá quyết định của AI
- [`04-fraud-and-explainability.md`](./04-fraud-and-explainability.md):
  - Phân biệt rạch ròi giữa Dự đoán của mô hình AI (Model Prediction) và Luật nghiệp vụ tất định (Rule-based Engine).
  - Cơ chế đối chiếu số học hóa đơn và phát hiện bất thường độ tin cậy OCR.
  - Kiểm tra điều khoản rủi ro trong hợp đồng pháp lý như một research extension dựa trên taxonomy CUAD.
  - Lớp giải thích (Explainability Layer): Cách trích xuất trọng số chú ý (Attention weights) và Grad-CAM để tạo bản đồ nhiệt phủ màu lên ảnh gốc.

### Bước 5: Đo lường, Đánh giá thực nghiệm và Phân tích chi phí
- [`05-evaluation.md`](./05-evaluation.md):
  - Làm thế nào để biết một pipeline hoạt động tốt hay dở?
  - Giải mã các chỉ số: Precision (Độ chuẩn xác), Recall (Độ phủ), F1-score ở cấp độ từng trường nghiệp vụ (Field-level).
  - Tỷ lệ đồng thuận (Agreement ratio) khi Track A và Track B đối đầu.
  - Đánh giá độ bền trước nhiễu ảnh thực tế (Robustness Test Suite).
  - Phân tích chi phí vận hành thật: GPU-giờ trên hạ tầng Modal Serverless so với API thương mại (Google Cloud DocAI, AWS Textract, Azure Document Intelligence).

---

## 3. Lộ trình đọc theo vai trò chuyên môn

Tùy theo mục tiêu nghiên cứu hoặc phát triển của bạn:

- **Dành cho Kỹ sư AI / Nghiên cứu (AI / ML Engineer)**:
  Ưu tiên đọc `01-docai-foundations.md` → `02-track-a-classic.md` → `03-track-b-vlm.md` → `05-evaluation.md`. Tập trung vào sự khác biệt giữa cơ chế Transformer đa phương thức của LayoutLMv3 và cơ chế sinh văn bản có cấu trúc của VLM, cách tính F1 field-level và thiết kế thí nghiệm Robustness.
- **Dành cho Kỹ sư Phần mềm / Hệ thống (Backend & Platform Engineer)**:
  Ưu tiên đọc `01-docai-foundations.md` → `04-fraud-and-explainability.md` → `05-evaluation.md` kết hợp đối chiếu [`docs/architecture/architecture-explained.md`](../architecture/architecture-explained.md) và [`docs/guides/how-to-run.md`](../guides/how-to-run.md). Tập trung vào luồng xử lý API, hợp đồng dữ liệu Pydantic, rule engine và quản lý chi phí GPU-giờ trên Modal.
- **Dành cho Chuyên viên Phân tích Nghiệp vụ / Quản lý Sản phẩm (BA / Product Manager)**:
  Ưu tiên đọc `01-docai-foundations.md` → `04-fraud-and-explainability.md` → `05-evaluation.md`. Tập trung trước vào nghiệp vụ hóa đơn/biên lai, validation/risk và bằng chứng giải thích; phần rủi ro hợp đồng và tối ưu chi phí thuộc research extension.
