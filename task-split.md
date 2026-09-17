# Phân chia công việc — DocAI Dual-Pipeline Benchmark

Dự án chia thành 2 nhánh công việc song song, phối hợp qua `log/progress-log.md` và JSON schema thống nhất (`src/docai/core/schema.py`). Mỗi giai đoạn trong `implementation-guide.md` được tách thành các task cụ thể, gán cho từng nhánh.

- **Nhánh A — Hạ tầng, Dữ liệu, Sản phẩm hoá**
- **Nhánh B — Mô hình, Đánh giá, Nghiên cứu**

Hai nhánh gặp nhau tại JSON schema chung (Giai đoạn 1) và tại báo cáo benchmark cuối cùng (Giai đoạn 9-10).

---

## Giai đoạn 1 — Khảo sát & chuẩn bị dữ liệu

| Task | Nhánh phụ trách |
|---|---|
| Tải và tổ chức 4 bộ dữ liệu vào `data/raw/` | A |
| Khảo sát thống kê cơ bản (số lượng, độ phân giải, phân bố nhãn) bằng `src/docai/data/` | A |
| Thiết kế JSON schema thống nhất (`src/docai/core/schema.py`) | B |
| Phân tích sâu định dạng nhãn gốc của từng bộ (đặc biệt CUAD — SQuAD-style span) để đảm bảo schema map đúng | B |

## Giai đoạn 2 — Hạ tầng & Đóng gói Package

| Task | Nhánh phụ trách |
|---|---|
| Setup Modal, test billing, viết `modal_app/deploy.py` khung | A |
| Thiết lập `pyproject.toml` chuẩn hoá `src/ layout` và `pip install -e .` | A |
| Viết `docker-compose.yml`, `requirements.txt` | A |
| Khởi tạo `log/progress-log.md` | A |

## Giai đoạn 3 — Track A: Layout Detection & OCR

| Task | Nhánh phụ trách |
|---|---|
| Chạy pretrained YOLOv8-doc/DocLayout-YOLO trong `src/docai/pipelines/track_a/layout_detection.py` | A |
| Tinh chỉnh ngưỡng confidence, xử lý edge case layout phức tạp | B |
| Tích hợp PaddleOCR trong `src/docai/pipelines/track_a/ocr_extraction.py`, ghép output vào JSON trung gian | A |
| Đánh giá sơ bộ tỷ lệ đọc đúng ký tự/vùng bảng so với ground truth | B |

## Giai đoạn 4 — Track A: Fine-tune LayoutLMv3

| Task | Nhánh phụ trách |
|---|---|
| Chuẩn bị hạ tầng chạy fine-tune trên Modal (script khởi tạo job, lưu checkpoint) | A |
| Thiết kế tập fine-tune, xử lý format BIO tagging trong `src/docai/pipelines/track_a/kie_layoutlmv3.py` | B |
| Thiết lập vòng lặp huấn luyện, chọn hyperparameter, đánh giá F1 field-level | B |
| Log chi phí GPU-giờ vào `log/progress-log.md` | A |

## Giai đoạn 5 — Track B: VLM-native parsing

| Task | Nhánh phụ trách |
|---|---|
| Tích hợp gọi model PaddleOCR-VL/dots.ocr qua API/Modal trong `src/docai/pipelines/track_b/vlm_parser.py` | A |
| Thiết kế prompt/schema trích field, tối ưu qua nhiều vòng thử nghiệm | B |
| Đánh giá F1, latency, so sánh với Track A | B |

## Giai đoạn 6 — Mở rộng sang hợp đồng (CUAD)

| Task | Nhánh phụ trách |
|---|---|
| Chuẩn bị subset CUAD, chuyển định dạng sang schema thống nhất | A |
| Chạy zero-shot/fine-tune nhẹ Track A trên CUAD | B |
| Điều chỉnh prompt Track B cho phù hợp hợp đồng | B |
| Phân tích số liệu tổng quát hoá, viết nhận định so sánh 2 track | B |

## Giai đoạn 7 — Fraud/Risk Engine

| Task | Nhánh phụ trách |
|---|---|
| Viết rule kiểm tra số liệu hóa đơn (tổng tiền, VAT) | A |
| Thiết kế logic phát hiện bất thường dựa trên độ tin cậy OCR (statistical threshold) | B |
| Xây taxonomy điều khoản rủi ro từ CUAD, viết rule clause-risk flagging | B |
| Tích hợp cả hai vào `src/docai/fraud/rules.py`, expose qua API | A |

## Giai đoạn 8 — Explainability Layer

| Task | Nhánh phụ trách |
|---|---|
| Trích attention weights từ LayoutLMv3, ánh xạ về bounding box | B |
| Triển khai Grad-CAM/visual grounding cho Track B | B |
| Vẽ overlay heatmap lên ảnh, đóng gói hàm dùng chung tại `src/docai/explainability/explainer.py` | A |
| Expose endpoint `/explain` | A |

## Giai đoạn 9 — Robustness Test & Benchmark tổng hợp

| Task | Nhánh phụ trách |
|---|---|
| Viết script sinh biến thể ảnh (xoay, mờ, watermark, thiếu sáng) | A |
| Chạy thử nghiệm cả 2 track trên từng mức nhiễu, thu thập số liệu | A |
| Phân tích đường cong độ giảm hiệu năng, thiết kế cách đo lường thống kê trong `src/docai/evaluation/metrics.py` | B |
| Tổng hợp toàn bộ báo cáo benchmark, đối chiếu chi phí GPU-giờ vs API thương mại | A + B (cùng viết) |

## Giai đoạn 10 — FastAPI Service, Scripts, Dashboard & Tài liệu hoá

| Task | Nhánh phụ trách |
|---|---|
| Viết `src/docai/api/main.py`, expose toàn bộ endpoint | A |
| Xây dựng các entry points CLI trong `scripts/` (`run_eda.py`, `run_track_a.py`, `run_track_b.py`, `run_benchmark.py`) | A |
| Deploy Modal, đóng gói Docker cho local | A |
| Chuẩn hoá kiến trúc Dashboard Plotly Dash (`src/docai/dashboard/app.py`), không dùng Power BI | A |
| Viết `docs/guides/how-to-run.md`, `docs/architecture/repository-structure.md` | A |
| Viết `docs/architecture/architecture-explained.md`, `docs/guides/glossary.md` (phần giải thích kỹ thuật sâu) | B |
| Xây dựng test suite trong `tests/` (unit & integration tests) | A + B (cùng làm) |
| Review chéo toàn bộ tài liệu trước khi hoàn thiện | A + B (cùng làm) |

---

## Nguyên tắc phối hợp

- Mọi thay đổi JSON schema (`src/docai/core/schema.py`) phải thông báo cho nhánh còn lại trước khi merge — vì cả 2 track đều phụ thuộc vào đó.
- Sau mỗi task hoàn thành, cập nhật `log/progress-log.md` ghi rõ nhánh nào đã làm, file nào bị ảnh hưởng.
- Nếu một nhánh bị chặn vì chờ output của nhánh kia (ví dụ Track B ở Giai đoạn 8 chờ schema từ Giai đoạn 1), ghi rõ vào mục "Việc tiếp theo cần làm" trong log để không bị quên.
- Giai đoạn 9 và 10 là điểm hợp nhất bắt buộc — cả 2 nhánh cùng review số liệu trước khi chốt báo cáo cuối cùng.
