# Cấu trúc Repository — DocAI Dual-Pipeline Benchmark

Tài liệu này giải thích toàn diện cấu trúc tổ chức thư mục và tập tin của dự án. Mục tiêu là giúp bất kỳ thành viên nào tham gia dự án đều hiểu rõ vị trí của từng module, ý nghĩa thiết kế kiến trúc phía sau và quy tắc phân chia trách nhiệm của từng thành phần.

---

## 1. Cây thư mục tổng thể (Directory Tree)

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

---

## 2. Giải thích ý nghĩa và Mục đích kiến trúc của từng thư mục

### 2.1. Tại sao tách biệt `track_a_classic/` và `track_b_vlm/`?

Điểm mấu chốt của dự án là so sánh thực nghiệm một cách công bằng giữa hai hướng tiếp cận Document AI có bản chất hoàn toàn trái ngược nhau:
- **`track_a_classic/` (Hướng tiếp cận cổ điển đa tầng)**:
  Bao gồm chuỗi xử lý độc lập:
  - `layout_detection.py`: Sử dụng mô hình thị giác máy tính chuyên dụng YOLOv8-doc để nhận diện bố cục.
  - `ocr_extraction.py`: Sử dụng công cụ nhận dạng ký tự PaddleOCR để lấy văn bản và tọa độ.
  - `kie_layoutlmv3.py`: Sử dụng mô hình ngôn ngữ kết hợp hình ảnh LayoutLMv3 được tinh chỉnh (fine-tune) theo nhãn thực thể BIO.
  Các file được tách riêng vì mỗi khâu có thể được tinh chỉnh, đánh giá lỗi (debug) và chạy độc lập.
- **`track_b_vlm/` (Hướng tiếp cận VLM-native đơn nhất)**:
  Chỉ chứa file `vlm_parser.py`. Trong kiến trúc VLM-native, một mô hình đa phương thức duy nhất (như PaddleOCR-VL hoặc dots.ocr) nhận ảnh đầu vào và trả về trực tiếp văn bản có cấu trúc thông qua câu lệnh chỉ dẫn (prompt).
  
Việc tách hai thư mục này đảm bảo mã nguồn không bị phụ thuộc chéo (decoupled). Nhà nghiên cứu có thể thay thế một thư viện OCR trong Track A mà không làm ảnh hưởng đến Track B, và ngược lại có thể đổi mô hình VLM khác trong Track B mà Track A vẫn hoạt động ổn định.

### 2.2. Vai trò của thư mục `shared/`

Thư mục `shared/` chứa các module mà cả hai track đều phải phụ thuộc và tuân thủ chặt chẽ:
- `schema.py`: Định nghĩa các model Pydantic chuẩn hoá (`UnifiedDocumentOutput`, `ExtractedField`, `BoundingBox`, `RiskFlag`). Đây là "hợp đồng giao tiếp" (contract interface) bắt buộc. Bất kể Track A xử lý qua 3 bước hay Track B xử lý trong 1 bước, kết quả cuối cùng bắt buộc phải ép về đúng schema này để có thể so sánh trên cùng một thước đo.
- `fraud_rules.py`: Chuyển hoá các luật kiểm tra gian lận số liệu hóa đơn và rủi ro điều khoản hợp đồng thành các rule độc lập với mô hình. Cả hai track đều sử dụng chung bộ luật này trên kết quả trích xuất.
- `explainability.py`: Cung cấp các hàm vẽ bản đồ nhiệt chú ý (attention heatmap) và overlay lên ảnh gốc. Dù kỹ thuật trích attention của Track A (Transformer attention weights) khác với Track B (Visual grounding / Grad-CAM), khâu blend màu lên ảnh gốc và trả về tọa độ hotspot được dùng chung tại đây.

### 2.3. Logic phân chia 4 thư mục con trong `docs/`

Tài liệu được phân cấp rõ ràng theo 4 mục đích sử dụng khác nhau:
- **`docs/specs/` (Specifications — Đặc tả yêu cầu gốc)**:
  Chứa các file tài liệu đặc tả gốc của dự án như `docai-benchmark-overview.pdf` và `implementation-guide.md`. Đây là chân lý (source of truth) về phạm vi công việc, lộ trình 10 giai đoạn và các tiêu chí hoàn thành (Definition of Done).
- **`docs/architecture/` (Kiến trúc hệ thống)**:
  Dành cho kỹ sư và kiến trúc sư muốn hiểu sâu về thiết kế hệ thống. Gồm:
  - `architecture-explained.md`: Giải thích dòng chảy dữ liệu và lý do lựa chọn kiến trúc.
  - `data-dictionary.md`: Từ điển dữ liệu và quy tắc ánh xạ trường.
  - `repository-structure.md`: Giải thích tổ chức mã nguồn.
- **`docs/guides/` (Hướng dẫn vận hành)**:
  Dành cho người sử dụng hoặc lập trình viên cần triển khai dự án. Gồm:
  - `how-to-run.md`: Hướng dẫn từng bước cài đặt và chạy hệ thống.
  - `glossary.md`: Tra cứu nhanh các thuật ngữ kỹ thuật.
- **`docs/reports/` (Báo cáo thực nghiệm)**:
  Chứa kết quả đo đạc và số liệu thật của benchmark. Gồm 4 báo cáo chuyên đề:
  - `benchmark-results.md`: Độ chính xác F1, độ trễ của từng track.
  - `cost-analysis.md`: Chi phí GPU-giờ trên Modal đối chiếu với API thương mại.
  - `explainability-report.md`: Minh họa và đánh giá bản đồ nhiệt chú ý.
  - `robustness-report.md`: Kết quả kiểm thử độ bền dưới các mức nhiễu khác nhau.

### 2.4. Ý nghĩa của các thư mục và tập tin khác

- **`data/`**:
  Chia thành `raw/` (chứa dữ liệu gốc tải về) và `processed/` (chứa dữ liệu đã qua làm sạch). Cả hai đều có file `.gitkeep` để giữ cấu trúc thư mục trên git, nhưng nội dung dữ liệu thật bị `.gitignore` chặn để không làm tăng dung lượng repo.
- **`notebooks/01-eda.ipynb`**:
  Nơi thực hiện khảo sát sơ bộ (Exploratory Data Analysis), kiểm tra phân bố dữ liệu và đánh giá chất lượng ảnh trước khi lập trình pipeline tự động.
- **`api/main.py`**:
  Ứng dụng FastAPI đóng gói toàn bộ chức năng thành các REST API endpoint sẵn sàng tích hợp vào hệ thống doanh nghiệp.
- **`modal_app/deploy.py`**:
  Mã nguồn triển khai hệ thống lên nền tảng điện toán đám mây không máy chủ (Serverless Cloud) của Modal, tận dụng GPU T4/A10G để fine-tune và phục vụ suy luận (inference).
- **`log/progress-log.md`**:
  Nhật ký theo dõi tiến độ thực hiện theo thời gian thực. Mọi hành động tạo/sửa file đều được ghi lại ngay lập tức để đảm bảo quá trình cộng tác không bị gián đoạn.
- **`docker-compose.yml` và `requirements.txt`**:
  Đảm bảo khả năng tái lập môi trường (reproducibility) trên bất kỳ máy tính lập trình viên nào mà không bị xung đột thư viện.
- **`task-split.md`**:
  Tài liệu phân công công việc canonical giữa Nhánh A (Hạ tầng, Dữ liệu, Sản phẩm hoá) và Nhánh B (Mô hình, Đánh giá, Nghiên cứu).

### 2.5. Tầng trực quan hoá và Dashboard (Plotly Dash)

Dự án xác định stack trực quan hoá chuẩn mực:
`Python → pandas → Plotly → Dash`

- Không sử dụng Power BI, không tạo file `.pbix`, không thêm dependency hay workflow Power BI.
- Khi bước vào giai đoạn triển khai dashboard tương ứng, dashboard Plotly Dash sẽ đọc trực tiếp kết quả chuẩn hoá từ pipeline DocAI/API (`UnifiedDocumentOutput`) để trình diễn kết quả trích xuất, độ tin cậy của các trường, so sánh Track A và Track B, cờ cảnh báo gian lận/rủi ro điều khoản, bản đồ nhiệt giải thích và các metric benchmark khi có số liệu thật.

