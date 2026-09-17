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


## 7. Cấu trúc repo (`src/ layout`)

Repository được tổ chức theo kiến trúc chuẩn `src/ layout`, phân định rõ ràng giữa mã nguồn đóng gói, entry point CLI, notebook khám phá, kiểm thử tự động, dữ liệu và tài liệu kỹ thuật:

```
docai-dual-pipeline-benchmark/
├── .cursor/
│   └── rules/
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── docker-compose.yml
├── task-split.md
├── README.md
│
├── src/                               # Mã nguồn Python chính (package docai)
│   └── docai/
│       ├── core/                      # Cấu hình tập trung và schema Pydantic thống nhất
│       ├── data/                      # Module tải dữ liệu, tiền xử lý, thống kê và EDA
│       ├── pipelines/                 # Hai pipeline Document AI chính (track_a và track_b)
│       ├── fraud/                     # Động cơ kiểm tra gian lận và rủi ro điều khoản
│       ├── explainability/            # Lớp giải thích bản đồ nhiệt chú ý
│       ├── evaluation/                # Công thức tính chỉ số đánh giá và so sánh benchmark
│       ├── api/                       # Dịch vụ FastAPI REST endpoints
│       └── dashboard/                 # Giao diện Plotly Dash trực quan hoá
│
├── scripts/                           # Entry point chạy bằng Python CLI (không cần mở Jupyter)
│   ├── run_eda.py                     # CLI khảo sát dữ liệu thô
│   ├── run_track_a.py                 # CLI chạy pipeline Track A
│   ├── run_track_b.py                 # CLI chạy pipeline Track B
│   └── run_benchmark.py               # CLI so sánh đối đầu 2 track
│
├── notebooks/                         # Khám phá, phân tích tương tác và hiển thị (EDA)
│   └── 01-eda.ipynb
│
├── tests/                             # Kiểm thử tự động (Unit & Integration tests)
│   ├── unit/                          # Kiểm thử schema, fraud rules, cấu hình
│   └── integration/                   # Kiểm thử router và endpoints FastAPI
│
├── data/                              # Dữ liệu phục vụ nghiên cứu và thực nghiệm
│   ├── raw/                           # Dữ liệu gốc tải về (mcocr2021, CORD, SROIE, CUAD)
│   ├── interim/                       # Dữ liệu trung gian trong quá trình chuyển đổi
│   └── processed/                     # Dữ liệu đã chuẩn hoá sẵn sàng cho benchmark
│
├── modal_app/                         # Triển khai hạ tầng điện toán đám mây Modal Serverless
│   └── deploy.py
│
├── log/                               # Nhật ký tiến độ và báo cáo kiểm duyệt
│   ├── progress-log.md
│   └── review-report-2026-09-17.md
│
└── docs/                              # Tài liệu kỹ thuật chi tiết
    ├── architecture/                  # Kiến trúc hệ thống, từ điển dữ liệu, cấu trúc repo
    ├── concepts/                      # Bản đồ tri thức, giải thích thuật toán & mô hình chuyên sâu
    ├── guides/                        # Hướng dẫn vận hành và bảng thuật ngữ
    ├── reports/                       # Báo cáo thực nghiệm chuyên đề
    └── specs/                         # Đặc tả yêu cầu gốc của dự án
```

### Vai trò của các phân vùng thư mục:
- `src/docai/`: Chứa toàn bộ mã nguồn có thể tái sử dụng. Mọi module đều được import qua package `docai` (ví dụ: `from docai.core.schema import UnifiedDocumentOutput`).
- `scripts/`: Chứa các kịch bản chạy dòng lệnh độc lập. Đóng vai trò là entry point gọi hàm từ `src/docai/`, không chứa logic nghiệp vụ nhân bản.
- `notebooks/`: Chỉ dùng cho mục đích khám phá, minh họa biểu đồ và trình bày kết luận; toàn bộ hàm xử lý được gọi trực tiếp từ `docai.data.*`.
- `tests/`: Bộ kiểm thử tự động với các ca kiểm thử có ý nghĩa cho schema, logic kiểm tra gian lận và cấu hình.
- `data/`: Lưu trữ dữ liệu qua 3 giai đoạn: `raw` (gốc), `interim` (trung gian), `processed` (chuẩn hoá).
- `docs/`: Hệ thống tài liệu kỹ thuật hoàn chỉnh không dùng emoji/icon, tra cứu thuật ngữ và phân tích kiến trúc.

## 8. Cách chạy dự án

Hướng dẫn thiết lập môi trường và vận hành chi tiết được trình bày tại:
`docs/guides/how-to-run.md`

Các cách khởi chạy nhanh:
- Cài đặt package ở chế độ phát triển (editable mode):
  `pip install -e .`
- Chạy kiểm thử tự động:
  `pytest` hoặc `python -m unittest discover -s tests`
- Chạy CLI khảo sát dữ liệu EDA:
  `python scripts/run_eda.py --dataset all`
- Chạy FastAPI server local bằng Uvicorn:
  `uvicorn docai.api.main:app --host 0.0.0.0 --port 8000 --reload`
- Chạy bằng Docker Compose:
  `docker compose up --build`
- Kiểm tra billing và kết nối Modal GPU:
  `modal run modal_app/deploy.py`

## 9. Trạng thái hiện tại

Theo dõi nhật ký tiến độ thực hiện theo thời gian thực tại:
`log/progress-log.md`

Hiện tại dự án đã hoàn thành tái cấu trúc sang kiến trúc chuẩn `src/ layout` (`src/docai/`), tích hợp `pyproject.toml`, chuẩn bị bộ `scripts/`, `tests/`, `data/interim/`, hoàn thiện toàn bộ tài liệu kỹ thuật và bộ tài liệu học tập chuyên sâu bằng tiếng Việt có dấu. Repository sẵn sàng 100% bước vào Giai đoạn 1 (Khảo sát & chuẩn bị dữ liệu thật).

## 10. Bản đồ tri thức & Tài liệu học tập

Để hiểu cặn kẽ bản chất bài toán Document AI, sự khác biệt giữa hai trường phái Track A và Track B, cũng như nguyên lý hoạt động của từng mô hình và thuật toán được triển khai trong repository, xem chi tiết bộ tài liệu tại:
`docs/concepts/README.md`

Các chuyên đề kỹ thuật chính:
- `docs/concepts/01-docai-foundations.md`: Nền tảng Document AI, 7 tầng thông tin và chuẩn hoá tọa độ Bounding Box.
- `docs/concepts/02-track-a-classic.md`: Pipeline cổ điển đa chặng (YOLOv8, PaddleOCR, LayoutLMv3, BIO tagging).
- `docs/concepts/03-track-b-vlm.md`: Pipeline VLM-native đơn lượt (PaddleOCR-VL, dots.ocr, structured prompting, rủi ro ảo giác).
- `docs/concepts/04-fraud-and-explainability.md`: Động cơ kiểm tra gian lận số học & rủi ro hợp đồng CUAD; lớp giải thích trực quan bằng bản đồ nhiệt JET overlay.
- `docs/concepts/05-evaluation.md`: Phương pháp đo lường khoa học (Field F1, Agreement ratio, Latency phân vị, chi phí GPU Modal vs API thương mại, Robustness suite).

