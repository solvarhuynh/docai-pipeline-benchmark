# DocAI Document Intelligence Platform

> Dual-Pipeline Product & Research Benchmark

Repository này xây dựng một sản phẩm Document Intelligence có khả năng tiếp nhận tài liệu thật, trích xuất dữ liệu có cấu trúc, kiểm tra rủi ro, cung cấp API và giao diện trực quan. Hai processing engine độc lập — Track A Classic và Track B VLM-native — là thành phần bên trong sản phẩm, đồng thời tạo nền cho phần nghiên cứu/benchmark.

Tên repository kỹ thuật vẫn có thể giữ là `docai-pipeline-benchmark`; thay đổi ở đây là định vị sản phẩm, không phải rename Git remote.

## 1. Product definition và use case chính

Use case ưu tiên của Product MVP là **Invoice / Receipt Document Intelligence**:

```text
Upload PDF hoặc Image hóa đơn/biên lai
        ↓
Validate và chuẩn hoá input
        ↓
Chọn processing engine Track A hoặc Track B
        ↓
UnifiedDocumentOutput
        ↓
Validation + Fraud/Risk baseline
        ↓
Confidence và bằng chứng vùng ảnh khi khả dụng
        ↓
FastAPI + Plotly Dash
```

Người dùng cần hình dung được việc upload hóa đơn, nhận JSON chuẩn hoá, xem field/confidence, phát hiện các inconsistency rõ ràng và xem hoặc tải kết quả. Contract/CUAD không bị loại bỏ; đây là extension để nghiên cứu khả năng tổng quát hoá sang tài liệu pháp lý dài và khác biệt.

## 2. Product MVP và trạng thái hiện tại

Product MVP về mặt mục tiêu gồm:

- nhận một tài liệu hóa đơn/biên lai;
- trả structured output theo schema chung;
- chạy validation và các risk rule cơ bản;
- cung cấp kết quả qua API và hiển thị qua Dash.

Hiện tại Product MVP **chưa hoàn thành end-to-end**. Schema, data layer, fraud baseline, API routes và Dash layout đã có; các model inference, API orchestration, Dashboard callbacks và output thật vẫn là `SCAFFOLD` hoặc `DỰ KIẾN`.

## 3. Điểm khác biệt

Product value của repository gồm:

- End-to-end document processing cho invoice/receipt theo lộ trình.
- Unified output contract để các engine và consumer dùng cùng cấu trúc dữ liệu.
- Validation và Fraud/Risk baseline giúp kết quả có kiểm soát nghiệp vụ.
- Explainability hướng tới việc cho người dùng biết field được lấy từ vùng nào hoặc vì sao risk flag được kích hoạt.
- FastAPI và Plotly Dash làm giao diện tích hợp của sản phẩm.
- Hai processing engine cho phép nghiên cứu trade-off mà không biến chúng thành hai sản phẩm riêng.

## 4. Research component

Phần research dùng cùng `UnifiedDocumentOutput` của Product để trả lời câu hỏi:

> Khi cùng phục vụ một hệ thống Document AI thực tế, pipeline Classic modular và pipeline VLM-native đánh đổi như thế nào về độ chính xác, latency, robustness, explainability và cost?

Research flow:

```text
Track A ─┐
         ├→ Evaluation / Benchmark / Robustness / Cost Analysis
Track B ─┘
                         ↓
                  Research reports
```

Benchmark là quality/research layer của sản phẩm, không phải identity duy nhất của repository. Research Complete chỉ được xác nhận khi có output thật của hai track, ground truth, evaluation, latency, cost và robustness thực nghiệm.

## 5. Kiến trúc tổng quan

### Product Architecture

```text
Người dùng / hệ thống bên ngoài
          ↓
Upload PDF / Image
          ↓
Document Input & Validation
          ↓
Document Processing Engine
       ┌──┴──┐
       ↓     ↓
   Track A  Track B
       └──┬──┘
          ↓
UnifiedDocumentOutput
          ↓
Validation → Fraud/Risk → Explainability khi khả dụng
          ↓
FastAPI → Plotly Dash
```

### Research Architecture

Hai track có thể được chạy trên cùng input và cùng output contract để đo F1/Precision/Recall, latency, cost, robustness và explainability. Endpoint `/compare` và các báo cáo benchmark là research/analysis capability; các endpoint `/parse/*` là hướng product processing.

## 6. Nguồn dữ liệu

Phạm vi dữ liệu dự kiến của dự án gồm các bộ dữ liệu thật, công khai, có bản quyền rõ ràng; hiện chưa tải dataset và không sử dụng dữ liệu tự sinh cho phần đánh giá chính:

| Bộ dữ liệu | Loại tài liệu | Quy mô | Vai trò |
|---|---|---|---|
| mcocr2021 | Hóa đơn/biên lai Việt Nam | Ảnh chụp thật, có nhãn | Nguồn chính, khớp bối cảnh Việt Nam |
| CORD | Biên lai | Chuẩn quốc tế, có ground truth field-level | Đối chiếu benchmark |
| SROIE (ICDAR2019) | Hóa đơn scan | 626 mẫu train, 347 test | Đối chiếu benchmark OCR + IE |
| CUAD | Hợp đồng pháp lý thật | 510 hợp đồng, hơn 13.000 điều khoản do luật sư gán nhãn | Kiểm tra tổng quát hoá sang loại tài liệu khác |

## 7. Công nghệ sử dụng

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


## 8. Cấu trúc repo (`src/ layout`)

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
│   └── track_b/
│       └── review-report-2026-09-17.md
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

## 9. Cách chạy dự án

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

## 10. Trạng thái hiện tại

Theo dõi nhật ký tiến độ thực hiện theo thời gian thực tại:
`log/progress-log.md`

Hiện tại dự án đã hoàn thành tái cấu trúc sang kiến trúc chuẩn `src/ layout` (`src/docai/`), tích hợp `pyproject.toml`, chuẩn bị bộ `scripts/`, `tests/`, `data/interim/`, hoàn thiện toàn bộ tài liệu kỹ thuật và bộ tài liệu học tập chuyên sâu bằng tiếng Việt có dấu. Repository đã sẵn sàng để bước vào Giai đoạn 1 (Khảo sát & chuẩn bị dữ liệu thật); các pipeline/model/benchmark vẫn còn scaffold theo lộ trình.

## 11. Bản đồ tri thức & Tài liệu học tập

Để hiểu cặn kẽ bản chất bài toán Document AI, sự khác biệt giữa hai trường phái Track A và Track B, cũng như nguyên lý hoạt động của từng mô hình và thuật toán được triển khai trong repository, xem chi tiết bộ tài liệu tại:
`docs/concepts/README.md`

Các chuyên đề kỹ thuật chính:
- `docs/concepts/01-docai-foundations.md`: Nền tảng Document AI, 7 tầng thông tin và chuẩn hoá tọa độ Bounding Box.
- `docs/concepts/02-track-a-classic.md`: Pipeline cổ điển đa chặng (YOLOv8, PaddleOCR, LayoutLMv3, BIO tagging).
- `docs/concepts/03-track-b-vlm.md`: Pipeline VLM-native đơn lượt (PaddleOCR-VL, dots.ocr, structured prompting, rủi ro ảo giác).
- `docs/concepts/04-fraud-and-explainability.md`: Động cơ kiểm tra gian lận số học & rủi ro hợp đồng CUAD; lớp giải thích trực quan bằng bản đồ nhiệt JET overlay.
- `docs/concepts/05-evaluation.md`: Phương pháp đo lường khoa học (Field F1, Agreement ratio, Latency phân vị, chi phí GPU Modal vs API thương mại, Robustness suite).
