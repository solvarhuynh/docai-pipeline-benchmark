# Progress Log

Muc dich: ghi lai toan bo tien do du an theo thoi gian thuc de bat ky AI hoac nguoi nao tiep tuc cong viec deu biet chinh xac da lam gi, tao file nao, o dau, con thieu gi.
Mục đích: ghi lại toàn bộ tiến độ dự án theo thời gian thực để bất kỳ AI hoặc người nào tiếp tục công việc đều biết chính xác đã làm gì, tạo file nào, ở đâu, còn thiếu gì.

## Cach dung
- Sau moi task hoan thanh, them mot dong moi vao bang. Khong xoa dong cu.
- Truoc khi bat dau phien lam viec moi, doc toan bo bang, uu tien doc tu duoi len.
## Cách dùng
- Sau mỗi task hoàn thành, thêm một dòng mới vào bảng. Không xóa dòng cũ.
- Trước khi bắt đầu phiên làm việc mới, đọc toàn bộ bảng, ưu tiên đọc từ dưới lên.

## Bang tien do
## Bảng tiến độ

| Thoi gian | Giai doan | Nhanh (A/B) | Viec da lam | File da tao/sua | Duong dan | Trang thai | Ghi chu |
| Thời gian | Giai đoạn | Nhánh (A/B) | Việc đã làm | File đã tạo/sửa | Đường dẫn | Trạng thái | Ghi chú |
|---|---|---|---|---|---|---|---|
| 2026-09-17 14:52 | Giai doan 2 | A | Khoi tao file nhat ky tien do | progress-log.md | log/progress-log.md | Done | Khoi tao bang tien do du an theo Prompt 1 |
| 2026-09-17 14:53 | Giai doan 1 | A | Tao placeholder thu muc du lieu tho | .gitkeep | data/raw/.gitkeep | Done | Giu thu muc data/raw tren Git |
| 2026-09-17 14:53 | Giai doan 1 | A | Tao placeholder thu muc du lieu da xu ly | .gitkeep | data/processed/.gitkeep | Done | Giu thu muc data/processed tren Git |
| 2026-09-17 14:54 | Giai doan 1 | A | Tao notebook khung cho khao sat du lieu EDA | 01-eda.ipynb | notebooks/01-eda.ipynb | Done | Khung EDA cho 4 bo du lieu mcocr2021, CORD, SROIE, CUAD |
| 2026-09-17 14:55 | Giai doan 1 | B | Thiet ke khung JSON schema thong nhat bang Pydantic | schema.py | shared/schema.py | Done | Dinh nghia DocumentType, BoundingBox, ExtractedField, RiskFlag, UnifiedDocumentOutput |
| 2026-09-17 14:56 | Giai doan 2 | A | Tao file cau hinh gitignore | .gitignore | .gitignore | Done | Loai tru data/raw/*, data/processed/*, checkpoints, credentials Modal |
| 2026-09-17 14:56 | Giai doan 2 | A | Tao file danh sach thu vien phu thuoc | requirements.txt | requirements.txt | Done | Liet ke fastapi, pydantic, ultralytics, paddleocr, transformers, modal |
| 2026-09-17 14:57 | Giai doan 2 | A | Tao docker-compose service dev local | docker-compose.yml | docker-compose.yml | Done | Cau hinh FastAPI dev local voi hot-reload qua volume mount |
| 2026-09-17 14:58 | Giai doan 2 | A | Tao modal app va ham test billing GPU | deploy.py | modal_app/deploy.py | Done | Ham test_gpu_billing chay nvidia-smi xac nhan GPU T4 va billing Modal |
| 2026-09-17 14:59 | Giai doan 3 | A | Tao stub module layout detection | layout_detection.py | track_a_classic/layout_detection.py | Done | Khung YOLOv8-doc/DocLayout-YOLO pretrained phan vung hoa don |
| 2026-09-17 15:00 | Giai doan 3 | A | Tao stub module ocr extraction | ocr_extraction.py | track_a_classic/ocr_extraction.py | Done | Khung PaddleOCR trich xuat text va bounding box tao JSON trung gian |
| 2026-09-17 15:00 | Giai doan 3 | B | Tao khung bao cao ket qua benchmark | benchmark-results.md | docs/reports/benchmark-results.md | Done | Khung bao cao tong hop kem ghi chu Cho Giai doan tuong ung |
| 2026-09-17 15:01 | Giai doan 4 | B | Tao stub module KIE LayoutLMv3 | kie_layoutlmv3.py | track_a_classic/kie_layoutlmv3.py | Done | Khung fine-tune va inference KIE LayoutLMv3 BIO tagging |
| 2026-09-17 15:02 | Giai doan 4 | A | Tao khung bao cao phan tich chi phi | cost-analysis.md | docs/reports/cost-analysis.md | Done | Khung phan tich Modal GPU-gio vs API thuong mai kem ghi chu Cho Giai doan tuong ung |
| 2026-09-17 15:03 | Giai doan 5 | A | Tao stub module VLM-native parser | vlm_parser.py | track_b_vlm/vlm_parser.py | Done | Khung PaddleOCR-VL/dots.ocr single-pass ep kieu UnifiedDocumentOutput |
| 2026-09-17 15:04 | Giai doan 7 | A | Tao stub module Fraud va Risk rules engine | fraud_rules.py | shared/fraud_rules.py | Done | Khung rule kiem tra doi chieu so hoa don va phat hien rui ro hop dong |
| 2026-09-17 15:05 | Giai doan 8 | B | Tao stub module Explainability Layer | explainability.py | shared/explainability.py | Done | Khung trich attention LayoutLMv3 va VLM grounding tao overlay heatmap |
| 2026-09-17 15:05 | Giai doan 8 | A | Tao khung bao cao kha nang giai thich | explainability-report.md | docs/reports/explainability-report.md | Done | Khung bao cao heatmap chu y kem ghi chu Cho Giai doan tuong ung |
| 2026-09-17 15:06 | Giai doan 9 | A | Tao khung bao cao do ben truoc nhieu | robustness-report.md | docs/reports/robustness-report.md | Done | Khung bao cao kiem thu Robustness Test Suite kem ghi chu Cho Giai doan tuong ung |
| 2026-09-17 15:07 | Giai doan 10 | A | Tao khung FastAPI service voi 4 route | main.py | api/main.py | Done | Dinh nghia 4 route /parse/classic, /parse/vlm, /compare, /explain dang stub |
| 2026-09-17 15:07 | Giai doan 10 | A | Sao chep dac ta implementation guide | implementation-guide.md | docs/specs/implementation-guide.md | Done | Sao chep nguyen van tu docai-implementation-guide.md |
| 2026-09-17 15:08 | Giai doan 10 | A | Sao chep overview PDF | docai-benchmark-overview.pdf | docs/specs/docai-benchmark-overview.pdf | Done | Sao chep nguyen van file overview PDF vao specs |
| 2026-09-17 15:09 | Giai doan 10 | A | Hoan thien README.md goc | README.md | README.md | Done | Hoan thanh 9 muc bat buoc khong icon theo Prompt 1 |
| 2026-09-17 15:15 | Giai doan 10 | A + B | Hoan thien bo tai lieu architecture va guides | architecture-explained.md, data-dictionary.md, repository-structure.md, glossary.md, how-to-run.md | docs/architecture/*, docs/guides/* | Done | Hoan thanh Prompt 2: kien truc he thong, tu dien du lieu, thuat ngu va huong dan van hanh |
| 2026-09-17 15:20 | Review | A + B | Kiem duyet toan bo repo va lap bao cao danh gia | review-report-2026-09-17.md | log/review-report-2026-09-17.md | Done | Hoan thanh kiem duyet static check 2a-2g, tu sua 4 sai lech |
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

## Giai doan hien tai
Giai doan 1 — Khao sat & chuan bi du lieu that (Chuan bi tai va tien xu ly du lieu)
## Giai đoạn hiện tại
Giai đoạn 1 — Khảo sát & chuẩn bị dữ liệu thật (Chuẩn bị tải và tiền xử lý dữ liệu)

## Viec tiep theo can lam
Tai 4 bo du lieu ve data/raw/ (mcocr2021, cord, sroie, cuad), thuc hien khao sat thong ke co ban trong notebooks/01-eda.ipynb va cap nhat so lieu thuc nghiem vao docs/architecture/data-dictionary.md.
## Việc tiếp theo cần làm
Tải 4 bộ dữ liệu về data/raw/ (mcocr2021, cord, sroie, cuad), thực hiện khảo sát thống kê cơ bản trong notebooks/01-eda.ipynb và cập nhật số liệu thực nghiệm vào docs/architecture/data-dictionary.md.
