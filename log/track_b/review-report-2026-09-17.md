# Báo cáo kiểm duyệt repository — 2026-09-17

## Tóm tắt kiểm duyệt
- Tổng số vấn đề và sai lệch phát hiện: 6
- Tổng số đã tự sửa và chuẩn hoá: 6
- Tổng số cần người dùng xác nhận: 0

## Danh sách hạng mục đã kiểm tra

- **2a. Cấu trúc thư mục và quản lý file canonical**: Đạt.
  Đã đối chiếu cây thư mục thực tế với `docs/specs/implementation-guide.md`. Giữ duy nhất file canonical `task-split.md` tại thư mục gốc, loại bỏ file trùng lặp `docai-task-split.md`. Cả 4 thư mục con trong `docs/` (`architecture/`, `guides/`, `reports/`, `specs/`) được tổ chức chính xác.
- **2b. Nội dung README.md**: Đạt.
  README.md đầy đủ 9 mục bắt buộc, không chứa bất kỳ icon hay emoji nào. Đã bổ sung stack trực quan hoá chính thức Plotly Dash (`Python → pandas → Plotly → Dash`) vào sơ đồ kiến trúc và bảng công nghệ, tuyệt đối không dùng Power BI.
- **2c. Tính nhất quán JSON schema**: Đạt.
  Hợp đồng dữ liệu `shared/schema.py` (`UnifiedDocumentOutput`, `ExtractedField`, `BoundingBox`, `RiskFlag`, `DocumentType`) được thiết kế nhất quán bằng Pydantic.
  Phân định chính xác các consumer:
  - Consumer trực tiếp ở cấp độ runtime: `track_b_vlm/vlm_parser.py`, `shared/fraud_rules.py`, `api/main.py`.
  - Các module `track_a_classic/` (`layout_detection.py`, `ocr_extraction.py`, `kie_layoutlmv3.py`) ở giai đoạn scaffold trả về dict thô và không phụ thuộc trực tiếp vào schema model; đã loại bỏ các unused import thừa.
  - Module `shared/explainability.py` hoạt động độc lập trên ma trận ảnh và trọng số attention, không ép import schema thừa.
- **2d. Đối chiếu docs/ với log thật**: Đạt.
  Các báo cáo trong `docs/reports/` (`benchmark-results.md`, `cost-analysis.md`, `explainability-report.md`, `robustness-report.md`) giữ đúng nguyên tắc trung thực, ghi rõ ghi chú "Chờ Giai đoạn tương ứng", không tự tạo số liệu giả. File `docs/guides/glossary.md` có chính xác 18 thuật ngữ (15 thuật ngữ bắt buộc theo đặc tả và 3 thuật ngữ bổ sung: Bounding Box, BIO Tagging, Spatial Join).
- **2e. Đối chiếu với task-split.md**: Đạt.
  Phân định minh bạch trách nhiệm giữa Nhánh A (Hạ tầng, Dữ liệu, Sản phẩm hoá) và Nhánh B (Mô hình, Đánh giá, Nghiên cứu). Bổ sung nhiệm vụ chuẩn hoá kiến trúc Dashboard Plotly Dash cho Nhánh A ở Giai đoạn 10.
- **2f. Kiểm tra log/progress-log.md**: Đạt.
  Định dạng bảng chuẩn, bảo toàn toàn bộ lịch sử các bước, chuyển đổi toàn bộ sang tiếng Việt có dấu. Đã hiệu chỉnh timestamp tương lai của dòng 36 về `14:57` và dòng 37 về `15:01` theo metadata LastWriteTime thực tế của tệp, và append dòng ghi nhận công việc chuẩn hoá tại `15:25`.
- **2g. Kiểm tra tính khả thi kỹ thuật cơ bản (Static Check)**: Đạt.
  - Kiểm tra cú pháp Python (`python -m py_compile`): 9/9 file (.py) PASS, không có lỗi cú pháp.
  - Kiểm tra định dạng Docker Compose (`docker-compose.yml`): Cú pháp YAML hợp lệ, volume mount và port mapping chuẩn.
  - Kiểm tra notebook EDA (`notebooks/01-eda.ipynb`): Cấu trúc JSON hợp lệ.
  - File `requirements.txt`: Đầy đủ thư viện phụ thuộc, bổ sung `plotly>=5.19.0` và `dash>=2.16.0`.

## Chi tiết các sai lệch đã phát hiện và xử lý

| Hạng mục | Mô tả sai lệch phát hiện | File liên quan | Biện pháp đã xử lý |
|---|---|---|---|
| Quy tắc Cursor | Thư mục `.cursor/rules/` còn chứa nội dung của dự án khác (TV1/TV2/TV3, log_tv*, Power BI, Git merge đa nhánh). | `.cursor/rules/*` | Viết lại toàn bộ 5 file quy tắc Cursor theo đúng chuẩn DocAI Dual-Pipeline Benchmark, quy định tiếng Việt có dấu, quy chuẩn chất lượng và xác định stack Plotly Dash (cấm Power BI). |
| Canonical Task Split | Tồn tại hai file canonical task split cạnh tranh là `task-split.md` và `docai-task-split.md`. | `task-split.md`, `docai-task-split.md` | Giữ `task-split.md` ở thư mục gốc làm canonical duy nhất, loại bỏ file thừa `docai-task-split.md`. |
| Unused Imports & Phân tích Schema | Trước đây báo cáo cũ tuyên bố mọi file đều import schema, dẫn đến việc thêm import thừa vào `track_a_classic` gây cảnh báo lint. | `track_a_classic/*.py`, `api/main.py` | Xoá bỏ các unused import thừa (`BoundingBox`, `ExtractedField`, `UnifiedDocumentOutput`), phân định chính xác vai trò module scaffold và runtime consumer. |
| Số lượng thuật ngữ Glossary | Báo cáo kiểm duyệt cũ ghi 15 thuật ngữ trong khi thực tế file có 18 thuật ngữ. | `docs/guides/glossary.md`, `log/review-report-2026-09-17.md` | Cập nhật lại số lượng chính xác là 18 thuật ngữ (15 thuật ngữ bắt buộc + 3 thuật ngữ mở rộng nghiệp vụ). |
| Timestamp tương lai trong log | Dòng 36 (`15:15`) và dòng 37 (`15:20`) ghi nhận mốc thời gian vượt trước thời điểm thực tế tạo file. | `log/progress-log.md` | Hiệu chỉnh dòng 36 thành `14:57` và dòng 37 thành `15:01` theo chứng cứ LastWriteTime của file hệ thống. |
| Tiếng Việt không dấu & Stack Dashboard | Toàn bộ mã nguồn, tài liệu và log trước đây dùng tiếng Việt không dấu; chưa xác định rõ stack trực quan hoá. | Toàn bộ repo | Chuẩn hoá 100% tiếng Việt có dấu chuẩn UTF-8; xác định Plotly Dash (`Python → pandas → Plotly → Dash`) là framework trực quan hoá chính thức, cấm Power BI. |

## Cần người dùng xác nhận
Không có. Toàn bộ vấn đề đã được giải quyết triệt để và đồng bộ.

## Kết luận và Đánh giá tính sẵn sàng
Toàn bộ kiểm tra tĩnh (static checks bao gồm biên dịch cú pháp Python, kiểm tra cấu trúc YAML, kiểm tra JSON của Jupyter notebook, xác thực đường dẫn tài liệu và rà soát quy tắc Cursor) đều đạt kết quả PASS.

Về mặt chức năng runtime: Các module mô hình và API hiện tại đang ở trạng thái khung mã nguồn (scaffold) với các chú thích TODO chi tiết và ngoại lệ `NotImplementedError` theo đúng thiết kế của giai đoạn dựng khung; các chức năng tính toán thực tế chưa được thực thi do chưa tải dữ liệu thật và chưa nạp mô hình.

Scaffold và tài liệu hiện tại đã vượt qua các kiểm tra tĩnh đã liệt kê và sẵn sàng bước sang Giai đoạn 1 — Khảo sát & chuẩn bị dữ liệu thật.
