# Progress Log

Mục đích: ghi lại toàn bộ tiến độ dự án theo thời gian thực để bất kỳ AI hoặc người nào tiếp tục công việc đều biết chính xác đã làm gì, tạo file nào, ở đâu, còn thiếu gì.

## Cách dùng
- Sau mỗi task hoàn thành, thêm một dòng mới vào bảng. Không xóa dòng cũ.
- Trước khi bắt đầu phiên làm việc mới, đọc toàn bộ bảng, ưu tiên đọc từ dưới lên.

## Bảng tiến độ

| Thời gian | Giai đoạn | Nhánh (A/B) | Việc đã làm | File đã tạo/sửa | Đường dẫn | Trạng thái | Ghi chú |
|---|---|---|---|---|---|---|---|
| 2026-09-17 14:52 | Giai đoạn 2 | A | Khởi tạo file nhật ký tiến độ | progress-log.md | log/progress-log.md | Done | Khởi tạo bảng tiến độ dự án theo Prompt 1 |
| 2026-09-17 14:53 | Giai đoạn 1 | A | Tạo placeholder thư mục dữ liệu thô | .gitkeep | data/raw/.gitkeep | Done | Giữ thư mục data/raw trên Git |
| 2026-09-17 14:53 | Giai đoạn 1 | A | Tạo placeholder thư mục dữ liệu đã xử lý | .gitkeep | data/processed/.gitkeep | Done | Giữ thư mục data/processed trên Git |
| 2026-09-17 14:54 | Giai đoạn 1 | A | Tạo notebook khung cho khảo sát dữ liệu EDA | 01-eda.ipynb | notebooks/01-eda.ipynb | Done | Khung EDA cho 4 bộ dữ liệu mcocr2021, CORD, SROIE, CUAD |
| 2026-09-17 14:55 | Giai đoạn 1 | B | Thiết kế khung JSON schema thống nhất bằng Pydantic | schema.py | shared/schema.py | Done | Định nghĩa DocumentType, BoundingBox, ExtractedField, RiskFlag, UnifiedDocumentOutput |
| 2026-09-17 14:56 | Giai đoạn 2 | A | Tạo file cấu hình gitignore | .gitignore | .gitignore | Done | Loại trừ data/raw/*, data/processed/*, checkpoints, credentials Modal |
| 2026-09-17 14:56 | Giai đoạn 2 | A | Tạo file danh sách thư viện phụ thuộc | requirements.txt | requirements.txt | Done | Liệt kê fastapi, pydantic, ultralytics, paddleocr, transformers, modal, plotly, dash |
| 2026-09-17 14:57 | Giai đoạn 2 | A | Tạo docker-compose service dev local | docker-compose.yml | docker-compose.yml | Done | Cấu hình FastAPI dev local với hot-reload qua volume mount |
| 2026-09-17 14:58 | Giai đoạn 2 | A | Tạo modal app và hàm test billing GPU | deploy.py | modal_app/deploy.py | Done | Hàm test_gpu_billing chạy nvidia-smi xác nhận GPU T4 và billing Modal |
| 2026-09-17 14:59 | Giai đoạn 3 | A | Tạo stub module layout detection | layout_detection.py | track_a_classic/layout_detection.py | Done | Khung YOLOv8-doc/DocLayout-YOLO pretrained phân vùng hóa đơn |
| 2026-09-17 15:00 | Giai đoạn 3 | A | Tạo stub module ocr extraction | ocr_extraction.py | track_a_classic/ocr_extraction.py | Done | Khung PaddleOCR trích xuất text và bounding box tạo JSON trung gian |
| 2026-09-17 15:00 | Giai đoạn 3 | B | Tạo khung báo cáo kết quả benchmark | benchmark-results.md | docs/reports/benchmark-results.md | Done | Khung báo cáo tổng hợp kèm ghi chú Chờ Giai đoạn tương ứng |
| 2026-09-17 15:01 | Giai đoạn 4 | B | Tạo stub module KIE LayoutLMv3 | kie_layoutlmv3.py | track_a_classic/kie_layoutlmv3.py | Done | Khung fine-tune và inference KIE LayoutLMv3 BIO tagging |
| 2026-09-17 15:02 | Giai đoạn 4 | A | Tạo khung báo cáo phân tích chi phí | cost-analysis.md | docs/reports/cost-analysis.md | Done | Khung phân tích Modal GPU-giờ vs API thương mại kèm ghi chú Chờ Giai đoạn tương ứng |
| 2026-09-17 15:03 | Giai đoạn 5 | A | Tạo stub module VLM-native parser | vlm_parser.py | track_b_vlm/vlm_parser.py | Done | Khung PaddleOCR-VL/dots.ocr single-pass ép kiểu UnifiedDocumentOutput |
| 2026-09-17 15:04 | Giai đoạn 7 | A | Tạo stub module Fraud và Risk rules engine | fraud_rules.py | shared/fraud_rules.py | Done | Khung rule kiểm tra đối chiếu số hóa đơn và phát hiện rủi ro hợp đồng |
| 2026-09-17 15:05 | Giai đoạn 8 | B | Tạo stub module Explainability Layer | explainability.py | shared/explainability.py | Done | Khung trích attention LayoutLMv3 và VLM grounding tạo overlay heatmap |
| 2026-09-17 15:05 | Giai đoạn 8 | A | Tạo khung báo cáo khả năng giải thích | explainability-report.md | docs/reports/explainability-report.md | Done | Khung báo cáo heatmap chú ý kèm ghi chú Chờ Giai đoạn tương ứng |
| 2026-09-17 15:06 | Giai đoạn 9 | A | Tạo khung báo cáo độ bền trước nhiễu | robustness-report.md | docs/reports/robustness-report.md | Done | Khung báo cáo kiểm thử Robustness Test Suite kèm ghi chú Chờ Giai đoạn tương ứng |
| 2026-09-17 15:07 | Giai đoạn 10 | A | Tạo khung FastAPI service với 4 route | main.py | api/main.py | Done | Định nghĩa 4 route /parse/classic, /parse/vlm, /compare, /explain dạng stub |
| 2026-09-17 15:07 | Giai đoạn 10 | A | Sao chép đặc tả implementation guide | implementation-guide.md | docs/specs/implementation-guide.md | Done | Sao chép nguyên văn từ docai-implementation-guide.md |
| 2026-09-17 15:08 | Giai đoạn 10 | A | Sao chép overview PDF | docai-benchmark-overview.pdf | docs/specs/docai-benchmark-overview.pdf | Done | Sao chép nguyên văn file overview PDF vào specs |
| 2026-09-17 15:09 | Giai đoạn 10 | A | Hoàn thiện README.md gốc | README.md | README.md | Done | Hoàn thành 9 mục bắt buộc không icon theo Prompt 1 |
| 2026-09-17 14:57 | Giai đoạn 10 | A + B | Hoàn thiện bộ tài liệu architecture và guides | architecture-explained.md, data-dictionary.md, repository-structure.md, glossary.md, how-to-run.md | docs/architecture/*, docs/guides/* | Done | Hoàn thành Prompt 2: kiến trúc hệ thống, từ điển dữ liệu, thuật ngữ và hướng dẫn vận hành (hiệu chỉnh giờ theo metadata LastWriteTime thực tế) |
| 2026-09-17 15:01 | Review | A + B | Kiểm duyệt toàn bộ repo và lập báo cáo đánh giá | review-report-2026-09-17.md | log/review-report-2026-09-17.md | Done | Hoàn thành kiểm duyệt static check 2a-2g, tự sửa 4 sai lệch ban đầu (hiệu chỉnh giờ theo metadata LastWriteTime thực tế) |
| 2026-09-17 15:25 | Review | A + B | Chuẩn hoá tiếng Việt có dấu, sửa Cursor rules, kiến trúc Plotly Dash và tái kiểm duyệt | review-report-2026-09-17.md, progress-log.md, .cursor/rules/*, docs/*, shared/*, track_* | Toàn bộ repo | Done | Chuẩn hoá tiếng Việt có dấu UTF-8 toàn repo, dọn dẹp Cursor rules, chốt Plotly Dash (loại bỏ Power BI), loại bỏ unused import, tái kiểm duyệt trung thực |
| 2026-09-17 15:55 | Giai đoạn 2 | A + B | Tái cấu trúc repository sang kiến trúc chuẩn src/ layout (src/docai) | pyproject.toml, src/docai/*, scripts/*, tests/*, notebooks/01-eda.ipynb | Toàn bộ repo | Done | Đóng gói package docai (editable install), tách bạch src/scripts/tests/data/docs, chuyển logic EDA vào docai.data, chốt Plotly Dash, xóa legacy folders (shared, track_a_classic, track_b_vlm, api) |
| 2026-09-17 16:15 | Giai đoạn 2 | A + B | Xây dựng bộ tài liệu giải thích kiến trúc, mô hình và thuật toán chuyên sâu | explanation-style.md, README.md, 01-docai-foundations.md, 02-track-a-classic.md, 03-track-b-vlm.md, 04-fraud-and-explainability.md, 05-evaluation.md | docs/concepts/* | Done | Hoàn thiện 7 tài liệu giải thích chi tiết theo quy chuẩn explanation-style, phân định 5 trạng thái minh bạch, neo file src/docai, không emoji, chốt Plotly Dash |

## Giai đoạn hiện tại
Giai đoạn 1 — Khảo sát & chuẩn bị dữ liệu thật (Chuẩn bị tải và tiền xử lý dữ liệu)

## Việc tiếp theo cần làm
Tải 4 bộ dữ liệu về data/raw/ (mcocr2021, cord, sroie, cuad), thực hiện khảo sát thống kê cơ bản trong notebooks/01-eda.ipynb và scripts/run_eda.py, cập nhật số liệu thực nghiệm vào docs/architecture/data-dictionary.md.
