# Bản đồ tri thức kỹ thuật (Concept Map) — DocAI Benchmark

Chào mừng bạn đến với khu vực tài liệu giải thích kiến trúc, thuật toán và khái niệm kỹ thuật của dự án **DocAI Dual-Pipeline Benchmark**.

Nếu bạn là người mới tiếp cận hệ thống, tài liệu này được thiết kế như một **bản đồ lộ trình học tập**. Thay vì đọc ngẫu nhiên từng file mã nguồn, bạn nên đi theo câu chuyện diễn tiến của một tài liệu từ lúc bước vào hệ thống cho đến khi trở thành dữ liệu chuẩn hoá có thể tin cậy được.

---

## 1. Dòng chảy tri thức: Tài liệu đi qua hệ thống như thế nào?

Toàn bộ hệ thống DocAI Benchmark xoay quanh một nhiệm vụ cốt lõi: **Biến một bức ảnh chụp hóa đơn nhàu nhĩ hoặc một bản quét hợp đồng pháp lý phức tạp thành dữ liệu có cấu trúc (JSON), có thể kiểm chứng tính trung thực và giải thích được bằng mắt thường.**

Dòng chảy xử lý và các chủ đề kỹ thuật tương ứng:

```text
[ 1. Bức ảnh tài liệu đầu vào (Pixel) ]
                    ↓
[ 2. Hiểu cấu trúc trang & các lớp thông tin ]  →  Đọc: 01-docai-foundations.md
                    ↓
        +-----------+-----------+
        |                       |
[ Track A: Tiếp cận Cổ điển ]   [ Track B: VLM-native ]
(Layout → OCR → LayoutLMv3)     (Vision-Language Model)
        ↓                               ↓
Đọc: 02-track-a-classic.md      Đọc: 03-track-b-vlm.md
        |                               |
        +-----------+-----------+
                    ↓
[ 3. Hợp đồng dữ liệu chung: Unified JSON Schema ]  →  src/docai/core/schema.py
                    ↓
[ 4. Phát hiện bất thường & Minh bạch hoá AI ]
     - Động cơ kiểm tra gian lận (Fraud/Risk Engine)
     - Bản đồ nhiệt giải thích (Explainability Heatmap)
     →  Đọc: 04-fraud-and-explainability.md
                    ↓
[ 5. Đánh giá, So sánh đối đầu & Chi phí GPU ]  →  Đọc: 05-evaluation.md
                    ↓
[ 6. Đưa vào sản phẩm & Trực quan hoá ]
     - FastAPI REST Endpoints (src/docai/api/main.py)
     - Plotly Dash Dashboard (src/docai/dashboard/app.py)
```

---

## 2. Thứ tự đọc khuyến nghị

Để nắm bắt dự án một cách tự nhiên và có hệ thống, bạn nên đọc các bài viết theo trình tự sau:

### Bước 0: Nắm vững quy chuẩn giải thích
- [`explanation-style.md`](file:///d:/2-personal-project/docs/concepts/explanation-style.md): Quy ước bắt buộc về cách viết tài liệu kỹ thuật trong repo — giải thích bằng ví dụ đời thường, dẫn dắt bằng câu hỏi, trực giác trước công thức sau, và minh bạch về trạng thái implementation.

### Bước 1: Nền tảng Document AI
- [`01-docai-foundations.md`](file:///d:/2-personal-project/docs/concepts/01-docai-foundations.md):
  - Document AI là gì và tại sao tài liệu quét không đơn giản là một bức ảnh?
  - Các tầng thông tin: từ pixel thô đến cấu trúc bảng biểu và ngữ nghĩa nghiệp vụ.
  - Tọa độ hộp giới hạn (Bounding Box) và kỹ thuật chuẩn hoá không gian.
  - Tại sao hai hướng tiếp cận trái ngược bắt buộc phải nói cùng một ngôn ngữ đầu ra (`UnifiedDocumentOutput`)?

### Bước 2: Đi sâu vào Track A — Hướng tiếp cận Cổ điển đa tầng
- [`02-track-a-classic.md`](file:///d:/2-personal-project/docs/concepts/02-track-a-classic.md):
  - Phân vùng bố cục (Layout Detection) bằng mô hình thị giác máy tính.
  - Đọc chữ bằng OCR (Optical Character Recognition) và lý do vì sao chỉ đọc được chữ vẫn chưa hiểu được tài liệu.
  - Trích xuất thông tin then chốt (KIE - Key Information Extraction).
  - Khám phá chuyên sâu mô hình LayoutLMv3: Sự kết hợp giữa chữ, vị trí 2D và đặc trưng thị giác; cơ chế đánh nhãn thực thể BIO.

### Bước 3: Đi sâu vào Track B — Hướng tiếp cận VLM-native đơn nhất
- [`03-track-b-vlm.md`](file:///d:/2-personal-project/docs/concepts/03-track-b-vlm.md):
  - Vision-Language Model (VLM) là gì và tại sao nó có thể "nhìn một lượt" trả về JSON?
  - Kỹ thuật điều hướng suy luận bằng Structured Prompt.
  - Rủi ro ảo giác (Hallucination) và thách thức về tài nguyên tính toán (GPU VRAM lớn).
  - So sánh triết lý kiến trúc giữa Track A (kiểm soát từng khâu, chia để trị) và Track B (hợp nhất, tổng quát hoá mạnh mẽ).

### Bước 4: Kiểm tra gian lận và Minh bạch hoá quyết định của AI
- [`04-fraud-and-explainability.md`](file:///d:/2-personal-project/docs/concepts/04-fraud-and-explainability.md):
  - Phân biệt rạch ròi giữa Dự đoán của mô hình AI (Model Prediction) và Luật nghiệp vụ tất định (Rule-based Engine).
  - Cơ chế đối chiếu số học hóa đơn và phát hiện bất thường độ tin cậy OCR.
  - Kiểm tra điều khoản rủi ro trong hợp đồng pháp lý dựa trên bộ taxonomy CUAD 41 điều khoản.
  - Lớp giải thích (Explainability Layer): Cách trích xuất trọng số chú ý (Attention weights) và Grad-CAM để tạo bản đồ nhiệt phủ màu lên ảnh gốc.

### Bước 5: Đo lường, Đánh giá thực nghiệm và Phân tích chi phí
- [`05-evaluation.md`](file:///d:/2-personal-project/docs/concepts/05-evaluation.md):
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
  Ưu tiên đọc `01-docai-foundations.md` → `04-fraud-and-explainability.md` → `05-evaluation.md` kết hợp đối chiếu [`docs/architecture/architecture-explained.md`](file:///d:/2-personal-project/docs/architecture/architecture-explained.md) và [`docs/guides/how-to-run.md`](file:///d:/2-personal-project/docs/guides/how-to-run.md). Tập trung vào luồng xử lý API, hợp đồng dữ liệu Pydantic, rule engine và quản lý chi phí GPU-giờ trên Modal.
- **Dành cho Chuyên viên Phân tích Nghiệp vụ / Quản lý Sản phẩm (BA / Product Manager)**:
  Ưu tiên đọc `01-docai-foundations.md` → `04-fraud-and-explainability.md` → `05-evaluation.md`. Tập trung vào nghiệp vụ đối chiếu hóa đơn, kiểm tra rủi ro hợp đồng, ý nghĩa của bản đồ nhiệt minh bạch hoá và bài toán tối ưu chi phí vận hành doanh nghiệp.
