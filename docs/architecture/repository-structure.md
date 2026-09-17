# Cấu trúc Repository — DocAI Document Intelligence Platform

Tài liệu này giải thích cấu trúc `src/ layout` của sản phẩm Document Intelligence và ranh giới giữa Product layer với Research/Evaluation layer. Mục tiêu là giúp thành viên mới hiểu vị trí, trách nhiệm và trạng thái của từng module.

---

## 1. Cây thư mục tổng thể (Directory Tree)

```
docai-dual-pipeline-benchmark/
├── .cursor/
│   └── rules/
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── docker-compose.yml
├── docs/
│   └── specs/
│       └── task-split.md
├── README.md
│
├── src/                               # Package chính duy nhất của hệ thống
│   └── docai/
│       ├── __init__.py
│       ├── core/                      # Thành phần cốt lõi: config tập trung & schema Pydantic
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── schema.py
│       │
│       ├── data/                      # Module xử lý dữ liệu phục vụ chung
│       │   ├── __init__.py
│       │   ├── loaders.py             # Định vị và nạp metadata các dataset
│       │   ├── preprocessing.py      # Tiền xử lý ảnh và chuẩn hoá bounding box
│       │   ├── statistics.py          # Thống kê mô tả số học và phân bố
│       │   └── eda.py                 # Hàm phân tích khám phá dữ liệu dùng lại
│       │
│       ├── pipelines/                 # Hai pipeline Document AI chính
│       │   ├── __init__.py
│       │   ├── track_a/               # Track A: Classic Multi-stage Pipeline
│       │   │   ├── __init__.py
│       │   │   ├── layout_detection.py
│       │   │   ├── ocr_extraction.py
│       │   │   └── kie_layoutlmv3.py
│       │   └── track_b/               # Track B: VLM-native Single-pass Pipeline
│       │       ├── __init__.py
│       │       └── vlm_parser.py
│       │
│       ├── fraud/                     # Động cơ kiểm tra gian lận số liệu & rủi ro hợp đồng
│       │   ├── __init__.py
│       │   └── rules.py
│       │
│       ├── explainability/            # Lớp giải thích (Attention heatmap & Grounding)
│       │   ├── __init__.py
│       │   └── explainer.py
│       │
│       ├── evaluation/                # Khung đánh giá thực nghiệm & so sánh đối đầu
│       │   ├── __init__.py
│       │   ├── metrics.py
│       │   └── benchmark.py
│       │
│       ├── api/                       # REST API endpoints sử dụng FastAPI
│       │   ├── __init__.py
│       │   └── main.py
│       │
│       └── dashboard/                 # Tầng trực quan hoá sử dụng Plotly Dash
│           ├── __init__.py
│           └── app.py
│
├── scripts/                           # Entry point chạy bằng Python CLI
│   ├── run_eda.py                     # Khảo sát dữ liệu thô
│   ├── run_track_a.py                 # Thực thi pipeline Track A
│   ├── run_track_b.py                 # Thực thi pipeline Track B
│   └── run_benchmark.py               # Chạy so sánh đối đầu 2 track
│
├── notebooks/                         # Khám phá, phân tích tương tác và trực quan hoá
│   └── 01-eda.ipynb
│
├── tests/                             # Kiểm thử tự động (Unit & Integration)
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/                          # Kiểm thử độc lập cho schema, fraud rules, config
│   │   ├── __init__.py
│   │   ├── test_schema.py
│   │   ├── test_fraud_rules.py
│   │   └── test_config.py
│   └── integration/                   # Kiểm thử tích hợp router FastAPI
│       ├── __init__.py
│       └── test_api_routes.py
│
├── data/                              # Dữ liệu phân tách theo 3 tầng
│   ├── raw/                           # Dữ liệu gốc tải về (mcocr2021, CORD, SROIE, CUAD)
│   ├── interim/                       # Dữ liệu trung gian trong quá trình chuẩn hoá
│   └── processed/                     # Dữ liệu đã chuẩn hoá sẵn sàng cho benchmark
│
├── modal_app/                         # Triển khai hạ tầng Serverless GPU trên Modal
│   └── deploy.py
│
├── log/                               # Nhật ký tiến độ và báo cáo kiểm duyệt
│   ├── progress-log.md
│   └── track_b/
│       └── review-report-2026-09-17.md
│
└── docs/                              # Tài liệu kỹ thuật chi tiết
    ├── architecture/                  # Kiến trúc hệ thống, từ điển dữ liệu, cấu trúc repo
    ├── guides/                        # Hướng dẫn vận hành và bảng thuật ngữ
    ├── reports/                       # Báo cáo thực nghiệm chuyên đề
    └── specs/                         # Đặc tả yêu cầu gốc của dự án
```

---

## 2. Giải thích ý nghĩa và Mục đích kiến trúc của từng phân vùng

### 2.1. Tại sao chuyển sang `src/ layout` và package `docai`?

Kiến trúc `src/ layout` giải quyết triệt để các vấn đề thường gặp trong các dự án Document AI:
- **Ngăn ngừa rò rỉ import cục bộ (Import parity)**: Khi chạy lệnh `python` từ thư mục gốc, Python không thể tự động import module nếu không cài đặt package hoặc cấu hình đường dẫn đúng chuẩn. Cấu trúc `src/docai` bắt buộc lập trình viên phải cài package qua `pip install -e .`, đảm bảo môi trường kiểm thử giống hệt môi trường production.
- **Loại bỏ hoàn toàn các thủ thuật `sys.path.append`**: Mọi module đều được import qua namespace thống nhất `docai.*` (ví dụ: `from docai.core.schema import UnifiedDocumentOutput`), độc lập hoàn toàn với thư mục làm việc hiện tại (working directory).
- **Phân tách rành mạch mã nguồn và công cụ thực thi**: Mã nguồn tái sử dụng nằm hoàn toàn trong `src/docai/`, các kịch bản chạy dòng lệnh nằm trong `scripts/`, việc khám phá nằm trong `notebooks/`, và việc xác minh nằm trong `tests/`.

### 2.2. Phân chia trách nhiệm giữa `track_a` và `track_b` trong `src/docai/pipelines/`

- **`track_a/` (Hướng tiếp cận cổ điển đa tầng)**:
  Bao gồm chuỗi xử lý mô-đun hoá:
  - `layout_detection.py`: Phân vùng bố cục bằng YOLOv8-doc.
  - `ocr_extraction.py`: Nhận dạng ký tự quang học bằng PaddleOCR.
  - `kie_layoutlmv3.py`: Trích xuất thực thể theo nhãn BIO bằng LayoutLMv3.
- **`track_b/` (Hướng tiếp cận VLM-native đơn nhất)**:
  Chứa `vlm_parser.py`: Sử dụng một mô hình đa phương thức duy nhất (PaddleOCR-VL hoặc dots.ocr) trích xuất trực tiếp end-to-end từ ảnh sang JSON.

Hai track này hoàn toàn độc lập về logic thuật toán nhưng bắt buộc phải gặp nhau tại một hợp đồng dữ liệu duy nhất: `docai.core.schema.UnifiedDocumentOutput`.

### 2.3. Trách nhiệm của `src/docai/core/`, `fraud/` và `explainability/`

- **`docai.core`**:
  - `config.py`: Quản lý đường dẫn tuyệt đối an toàn tới `data/raw/`, `data/interim/`, `data/processed/` và các tham số cấu hình.
  - `schema.py`: Định nghĩa Pydantic models chuẩn hoá cho toàn bộ hệ thống (`UnifiedDocumentOutput`, `ExtractedField`, `BoundingBox`, `RiskFlag`).
- **`docai.fraud`**:
  - `rules.py`: Chứa `FraudRiskEngine` độc lập với mô hình, ưu tiên đối chiếu số học hóa đơn; kiểm tra thiếu điều khoản hợp đồng CUAD là extension.
- **`docai.explainability`**:
  - `explainer.py`: Chứa `DocumentExplainer` điều phối trích xuất attention map từ LayoutLMv3 hoặc visual grounding từ VLM để tạo ảnh overlay heatmap.

### 2.4. Trách nhiệm của `src/docai/evaluation/`

- `metrics.py`: Cung cấp các công thức tính F1 field-level, tỷ lệ đồng thuận (agreement ratio) và phân tích độ trễ (latency).
- `benchmark.py`: Cung cấp `BenchmarkRunner` cho Research layer, điều phối so sánh Track A và Track B trên cùng một tập dữ liệu thử nghiệm; không phải dependency bắt buộc của Product parsing flow.

### 2.5. Tầng trực quan hoá Dashboard (`src/docai/dashboard/`)

Dự án xác định stack trực quan hoá chuẩn mực:
`Python → pandas → Plotly → Dash`

- Tuyệt đối không sử dụng Power BI, không tạo file `.pbix`, không thêm dependency hay workflow Power BI.
- Theo lộ trình, ứng dụng Plotly Dash (`app.py`) sẽ đọc kết quả chuẩn hoá từ pipeline DocAI (`UnifiedDocumentOutput`) để trực quan hoá kết quả trích xuất, confidence, so sánh 2 track, cảnh báo rủi ro, bản đồ nhiệt giải thích và các biểu đồ benchmark. Hiện tại `app.py` mới là scaffold layout, chưa có callbacks hoặc dữ liệu thật.

### 2.6. Nguyên tắc tổ chức Scripts và Notebooks

- **`scripts/`**: Đóng vai trò là entry point dòng lệnh cho người dùng chạy trực tiếp pipeline mà không cần mở Jupyter:
  - `run_eda.py`: Khảo sát dữ liệu thô.
  - `run_track_a.py`: Chạy pipeline Track A.
  - `run_track_b.py`: Chạy pipeline Track B.
  - `run_benchmark.py`: So sánh đối đầu 2 track.
- **`notebooks/`**: `01-eda.ipynb` chỉ đóng vai trò phân tích tương tác, gọi trực tiếp các hàm từ `docai.data.*` và hiển thị trực quan; không chứa logic nghiệp vụ nhân bản. Nếu sau này xoá toàn bộ notebook, hệ thống vẫn vận hành bình thường qua `scripts/` và `src/docai/`.

### 2.7. Tổ chức dữ liệu 3 tầng (`data/`)

- `data/raw/`: Chứa dữ liệu gốc tải về (mcocr2021, CORD, SROIE, CUAD). Tuyệt đối không chỉnh sửa trực tiếp.
- `data/interim/`: Chứa dữ liệu trung gian trong quá trình làm sạch và chuyển đổi định dạng.
- `data/processed/`: Chứa dữ liệu chuẩn hoá cuối cùng sẵn sàng nạp vào Product processing flow hoặc Research evaluation/benchmark.
Cả 3 thư mục đều được giữ trên Git bằng file `.gitkeep`, nhưng toàn bộ nội dung dữ liệu thật bị chặn bởi `.gitignore`.

### 2.8. Product layer và Research layer nằm ở đâu?

- **Product layer**: `src/docai/data/`, `src/docai/pipelines/`, `src/docai/core/`, `src/docai/fraud/`, `src/docai/explainability/`, `src/docai/api/` và `src/docai/dashboard/`. Đây là các thành phần hướng tới luồng upload tài liệu, xử lý, chuẩn hoá output, kiểm tra rủi ro và trình bày kết quả.
- **Research/Evaluation layer**: `src/docai/evaluation/`, `scripts/run_benchmark.py` và `docs/reports/`. Layer này dùng output chung để đo accuracy, latency, cost, robustness và explainability; không bắt buộc chạy khi Product chỉ xử lý một tài liệu.
- **Shared contract**: `src/docai/core/schema.py` là điểm giao tiếp giữa hai processing engine và mọi consumer phía sau. Product không phụ thuộc trực tiếp vào chi tiết nội bộ của Track A hoặc Track B.
- **Trạng thái hiện tại**: Product flow, API orchestration và Dashboard callbacks còn scaffold; Research reports chưa có kết quả thực nghiệm.
