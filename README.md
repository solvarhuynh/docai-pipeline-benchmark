# DocAI Dual-Pipeline Benchmark

Dự án cá nhân — So sánh pipeline Document AI cổ điển và VLM-native trên hóa đơn và hợp đồng thật, có Explainability, Robustness Test và phân tích chi phí vận hành.

## 1. Tên dự án và mô tả ngắn

DocAI Dual-Pipeline Benchmark là hệ thống nghiên cứu và đánh giá thực nghiệm đối chiếu giữa hai trường phái Document AI tiêu biểu:
- Pipeline truyền thống đa tầng (Track A - Classic): Layout Detection (YOLOv8-doc) kết hợp OCR (PaddleOCR) và Key Information Extraction (LayoutLMv3 fine-tuned).
- Pipeline hiện đại đơn nhất (Track B - VLM-native): Vision-Language Model đa phương thức (PaddleOCR-VL / dots.ocr) trích xuất trực tiếp end-to-end qua schema prompt.

Hệ thống không chỉ dừng ở việc xây dựng một bộ parser, mà tập trung đo lường các đánh đổi thực tế về độ chính xác (F1-score), độ trễ (latency), chi phí tính toán (GPU-giờ trên Modal vs Commercial API) và độ bền vững trước nhiễu ảnh thực tế (Robustness Test).

## 2. Mục tiêu dự án

Doanh nghiệp nhận hàng triệu hóa đơn và hợp đồng ở dạng ảnh chụp hoặc PDF quét lệch góc mỗi năm. Dự án xây dựng và so sánh nghiêm túc hai hướng tiếp cận Document AI:
- Xây dựng pipeline hoàn chỉnh cho cả 2 track trên cùng một tập dữ liệu chuẩn hoá.
- Đo lường hiệu năng thực tế trên 2 loại tài liệu có bản chất khác biệt: hóa đơn (bảng biểu, số liệu ngắn) và hợp đồng pháp lý (văn bản dài, điều khoản phức tạp).
- Cung cấp lớp Explainability trực quan hoá vùng ảnh mô hình tập trung bằng bản đồ nhiệt chú ý (heatmap overlay).
- Tích hợp động cơ Fraud/Risk Engine phát hiện sai lệch số liệu hóa đơn và cảnh báo điều khoản bất thường trên hợp đồng.
- Lập báo cáo benchmark tổng hợp có số liệu thực nghiệm thật trên hạ tầng Modal Serverless GPU.

## 3. Điểm khác biệt so với các dự án tương tự

Khảo sát trên GitHub cho thấy tổ hợp Layout Detection + PaddleOCR + LayoutLMv3 + FastAPI đã trở thành stack mặc định của rất nhiều repo invoice-parser, kể cả phần fraud detection. Dự án này khác biệt ở các điểm:
- Đa loại tài liệu: Kiểm tra khả năng tổng quát hoá của cả 2 track trên hai loại tài liệu khác hẳn nhau — hóa đơn (bảng số liệu) và hợp đồng pháp lý (văn bản dài, điều khoản) — thay vì chỉ dừng ở hóa đơn.
- Explainability: Trực quan hoá vùng ảnh mà mô hình dựa vào để trích xuất từng trường dữ liệu, thay vì trả JSON như hộp đen.
- Robustness Test Suite: Chủ động tạo biến thể ảnh xoay lệch, mờ, có watermark, thiếu sáng để đo mức độ giảm độ chính xác — phần lớn dự án khác chỉ demo trên ảnh đẹp.
- Risk/Fraud mở rộng sang hợp đồng: Ngoài kiểm tra số liệu hóa đơn, thêm việc phát hiện thiếu điều khoản chuẩn hoặc điều khoản bất lợi trong hợp đồng.
- Phân tích chi phí vận hành thật: Đo chi phí GPU-giờ thực tế trên Modal, đối chiếu với chi phí ước tính của các API thương mại phổ biến.

## 4. Nguồn dữ liệu

Toàn bộ dữ liệu sử dụng trong dự án đều là dữ liệu thật, công khai, có bản quyền rõ ràng, không sử dụng dữ liệu tự sinh cho phần đánh giá chính:

| Bộ dữ liệu | Loại tài liệu | Quy mô | Vai trò |
|---|---|---|---|
| mcocr2021 | Hóa đơn/biên lai Việt Nam | Ảnh chụp thật, có nhãn | Nguồn chính, khớp bối cảnh Việt Nam |
| CORD | Biên lai | Chuẩn quốc tế, có ground truth field-level | Đối chiếu benchmark |
| SROIE (ICDAR2019) | Hóa đơn scan | 626 mẫu train, 347 test | Đối chiếu benchmark OCR + IE |
| CUAD | Hợp đồng pháp lý thật | 510 hợp đồng, hơn 13.000 điều khoản do luật sư gán nhãn | Kiểm tra tổng quát hoá sang loại tài liệu khác |

## 5. Kiến trúc tổng quan

Hệ thống bao gồm các thành phần cốt lõi sau:
- Track A — Classic Pipeline:
  Layout Detection (YOLOv8-doc / DocLayout-YOLO pretrained) -> OCR (PaddleOCR trích xuất chữ và bounding box) -> KIE (LayoutLMv3 fine-tune trên subset nhỏ).
- Track B — VLM-native Pipeline:
  Single-pass Vision-Language Model (PaddleOCR-VL / dots.ocr pretrained) trích xuất field trực tiếp thông qua schema prompt định sẵn.
- Chuẩn hoá output: Cả 2 track trả về cùng một cấu trúc JSON schema thống nhất (`shared/schema.py`) gồm document_type, fields, confidence, bounding_box và risk_flags để đảm bảo so sánh công bằng.
- Explainability Layer (`shared/explainability.py`):
  Trích attention weights từ LayoutLMv3 và visual grounding / Grad-CAM từ VLM để vẽ overlay heatmap lên ảnh gốc, giải thích căn cứ trích xuất cho từng trường.
- Fraud/Risk Engine (`shared/fraud_rules.py`):
  Rule-based fraud check cho hóa đơn (kiểm tra đối chiếu số học và bất thường độ tin cậy OCR vùng số) và clause-risk flagging cho hợp đồng (dựa trên taxonomy điều khoản CUAD).
- Robustness Test Suite:
  Sinh biến thể ảnh (xoay 5-15 độ, làm mờ Gaussian, giảm sáng, chèn watermark) và vẽ đường cong suy giảm F1-score theo mức độ nhiễu.
- Benchmark & Cost Analysis:
  Tổng hợp F1 field-level, độ trễ, độ bền trước nhiễu và phân tích chi phí GPU-giờ Modal đối chiếu với API thương mại (Google Cloud Document AI, AWS Textract, Azure Document Intelligence).
- FastAPI Service & Deployment:
  Expose các REST endpoint `/parse/classic`, `/parse/vlm`, `/compare`, `/explain` trên FastAPI, đóng gói Docker cho dev local và deploy trên Modal Serverless GPU.
- Visualization & Dashboard:
  Sử dụng Plotly Dash (`Python → pandas → Plotly → Dash`) làm dashboard framework chính thức để đọc kết quả từ pipeline DocAI/API hiển thị trích xuất, confidence, so sánh 2 track, fraud flags, explainability và các metric benchmark (không dùng Power BI).

## 6. Công nghệ sử dụng

| Hạng mục | Công cụ |
|---|---|
| Layout Detection (Track A) | YOLOv8-doc / DocLayout-YOLO (pretrained) |
| OCR (Track A) | PaddleOCR |
| KIE (Track A) | LayoutLMv3 (fine-tune subset nhỏ) |
| VLM-native (Track B) | PaddleOCR-VL / dots.ocr (pretrained) |
| Explainability | Attention weights (LayoutLMv3), Grad-CAM / visual grounding |
| Compute | Modal (GPU serverless, free credit hàng tháng) |
| API | FastAPI, đóng gói Docker cho dev local |
| Dashboard & Trực quan hoá | Plotly Dash (Python → pandas → Plotly → Dash) |
| Quản lý mã nguồn & tài liệu | Git/GitHub, log tiến độ trong log/progress-log.md |


## 7. Cấu trúc repo

```
docai-dual-pipeline-benchmark/
├── .cursor/
│   └── rules/
├── .gitignore
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
├── docs/
│   ├── architecture/
│   │   ├── architecture-explained.md
│   │   ├── data-dictionary.md
│   │   └── repository-structure.md
│   ├── guides/
│   │   ├── glossary.md
│   │   └── how-to-run.md
│   ├── reports/
│   │   ├── benchmark-results.md
│   │   ├── cost-analysis.md
│   │   ├── explainability-report.md
│   │   └── robustness-report.md
│   └── specs/
│       ├── implementation-guide.md
│       └── docai-benchmark-overview.pdf
├── notebooks/
│   └── 01-eda.ipynb
├── track_a_classic/
│   ├── layout_detection.py
│   ├── ocr_extraction.py
│   └── kie_layoutlmv3.py
├── track_b_vlm/
│   └── vlm_parser.py
├── shared/
│   ├── schema.py
│   ├── fraud_rules.py
│   └── explainability.py
├── api/
│   └── main.py
├── modal_app/
│   └── deploy.py
├── log/
│   └── progress-log.md
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 8. Cách chạy dự án

Hướng dẫn thiết lập môi trường và vận hành chi tiết được trình bày tại:
`docs/guides/how-to-run.md`

Các cách khởi chạy nhanh hiện tại:
- Chạy FastAPI server local bằng Docker Compose:
  `docker compose up --build`
- Kiểm tra billing và kết nối Modal GPU:
  `modal run modal_app/deploy.py`

## 9. Trạng thái hiện tại

Theo dõi nhật ký tiến độ thực hiện theo thời gian thực tại:
`log/progress-log.md`

Hiện tại dự án đã hoàn thành xong phần dựng khung repo (Scaffold Giai đoạn 1 đến 10) và bộ tài liệu kỹ thuật toàn diện (`docs/architecture/` và `docs/guides/`). Các file mã nguồn đang ở dạng stub với TODO chi tiết, sẵn sàng để bước vào Giai đoạn 1 (tải và tiền xử lý 4 bộ dữ liệu thật).
