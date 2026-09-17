# Implementation Guide — DocAI Dual-Pipeline Benchmark

> Đọc kèm file `docai-benchmark-overview.pdf` (trong `docs/specs/`) để hiểu bức tranh tổng thể trước khi đi vào chi tiết từng giai đoạn.

## Mục tiêu dự án
So sánh nghiêm túc hai hướng tiếp cận Document AI — pipeline cổ điển nhiều tầng (Track A) và mô hình VLM-native hiện đại (Track B) — trên hai loại tài liệu thật khác hẳn nhau (hóa đơn và hợp đồng), có thêm lớp Explainability, Robustness Test và phân tích chi phí vận hành thật trên Modal.

## Nguồn dữ liệu

| Bộ dữ liệu | Loại tài liệu | Quy mô | Vai trò |
|---|---|---|---|
| mcocr2021 | Hóa đơn/biên lai Việt Nam | Ảnh chụp thật, có nhãn | Nguồn chính |
| CORD | Biên lai | Chuẩn quốc tế, field-level ground truth | Đối chiếu benchmark |
| SROIE (ICDAR2019) | Hóa đơn scan | 626 train / 347 test | Đối chiếu benchmark OCR + IE |
| CUAD | Hợp đồng pháp lý thật | 510 hợp đồng, hơn 13.000 điều khoản gán nhãn bởi luật sư | Kiểm tra tổng quát hoá sang loại tài liệu khác |

---

## Giai đoạn 1 — Khảo sát & chuẩn bị dữ liệu thật

**Việc cần làm:**
1. Tải 4 bộ dữ liệu về `data/raw/` (mỗi bộ một thư mục con: `data/raw/mcocr2021/`, `data/raw/cord/`, `data/raw/sroie/`, `data/raw/cuad/`).
2. Khảo sát nhanh bằng pandas/PIL: số lượng mẫu, độ phân giải ảnh (với 3 bộ hóa đơn), độ dài văn bản (với CUAD), phân bố nhãn.
3. Ghi data dictionary riêng cho từng bộ vào `docs/architecture/data-dictionary.md`.
4. Xác định vấn đề chất lượng dữ liệu: ảnh mờ/nghiêng trong mcocr2021, format nhãn khác nhau giữa các bộ hóa đơn, định dạng CUAD (JSON theo SQuAD-style span extraction) khác hẳn 3 bộ còn lại.
5. Thiết kế 1 JSON schema thống nhất để cả 2 track trả về cùng định dạng, cho cả 2 loại tài liệu (field khác nhau giữa hóa đơn và hợp đồng nhưng cấu trúc bao ngoài giống nhau: `document_type`, `fields[]`, `confidence`, `bounding_box`).

**Definition of Done:**
- [ ] 4 bộ dữ liệu đã tải về đúng thư mục.
- [ ] `docs/architecture/data-dictionary.md` mô tả đủ 4 bộ.
- [ ] `notebooks/01-eda.ipynb` chứa khảo sát cơ bản từng bộ.
- [ ] File `shared/schema.py` định nghĩa JSON schema thống nhất (dùng Pydantic).

---

## Giai đoạn 2 — Hạ tầng

**Việc cần làm:**
1. Đăng ký Modal, xác nhận free credit hàng tháng đang hoạt động.
2. Viết `modal_app/deploy.py` khung — một function GPU rỗng để test billing (chạy `nvidia-smi` trong container Modal, xác nhận có GPU, dừng ngay, kiểm tra log chi phí trên Modal dashboard).
3. Viết `docker-compose.yml` cho môi trường dev local (không cần GPU) — chạy FastAPI dev server, mount code, để test nhanh mà không tốn GPU-giờ trên Modal.
4. Viết `requirements.txt` liệt kê đầy đủ thư viện cần cho cả 2 track.
5. Tạo file `log/progress-log.md` theo định dạng đã thống nhất (xem mục Log bên dưới).

**Definition of Done:**
- [ ] Modal function test chạy thành công, xác nhận GPU khả dụng, chi phí hiển thị đúng trên dashboard.
- [ ] `docker-compose.yml` chạy được FastAPI dev server local.
- [ ] `log/progress-log.md` khởi tạo, có dòng đầu tiên ghi nhận hoàn thành hạ tầng.

---

## Giai đoạn 3 — Track A: Layout Detection & OCR (hóa đơn)

**Việc cần làm:**
1. Load YOLOv8-doc/DocLayout-YOLO pretrained (không train từ đầu), chạy trên tập mcocr2021/CORD/SROIE để phân vùng Header, Table, Signature.
2. Chạy PaddleOCR trên từng vùng đã phân, trích văn bản kèm bounding box.
3. Ghép kết quả layout + OCR vào 1 JSON trung gian (chưa qua KIE) theo schema đã định nghĩa ở Giai đoạn 1.
4. Đánh giá sơ bộ chất lượng: tỷ lệ vùng bảng phát hiện đúng, tỷ lệ ký tự đọc đúng so với ground truth có sẵn.

**Definition of Done:**
- [ ] `track_a_classic/layout_detection.py` chạy được trên toàn bộ 3 bộ hóa đơn.
- [ ] `track_a_classic/ocr_extraction.py` sinh ra JSON trung gian có bounding box.
- [ ] Ghi số liệu đánh giá sơ bộ vào `docs/reports/benchmark-results.md` (mục "Track A — Layout & OCR baseline").

---

## Giai đoạn 4 — Track A: Fine-tune LayoutLMv3 (hóa đơn)

**Việc cần làm:**
1. Chuẩn bị tập fine-tune nhỏ (vài trăm mẫu) từ mcocr2021/CORD theo format LayoutLMv3 yêu cầu (token + bbox + label BIO).
2. Fine-tune LayoutLMv3 trên Modal GPU, log rõ thời gian và chi phí GPU-giờ vào `log/progress-log.md`.
3. Đánh giá F1 field-level trên tập test riêng (không overlap với tập fine-tune).
4. Lưu model checkpoint (không commit trực tiếp vào git nếu file lớn — dùng Modal Volume hoặc HuggingFace Hub cá nhân, ghi rõ cách tải lại trong `docs/guides/how-to-run.md`).

**Definition of Done:**
- [ ] `track_a_classic/kie_layoutlmv3.py` chạy fine-tune và inference.
- [ ] F1 field-level trên tập test ghi vào `docs/reports/benchmark-results.md`.
- [ ] Chi phí GPU-giờ của bước fine-tune ghi vào `docs/reports/cost-analysis.md`.

---

## Giai đoạn 5 — Track B: VLM-native parsing (hóa đơn)

**Việc cần làm:**
1. Thiết kế prompt/schema để PaddleOCR-VL hoặc dots.ocr trả trực tiếp các field cần thiết (không cần train).
2. Chạy trên cùng tập test đã dùng ở Giai đoạn 4 để so sánh công bằng với Track A.
3. Đánh giá F1 field-level, latency, chi phí GPU-giờ (nếu chạy trên Modal) hoặc chi phí API (nếu dùng dịch vụ ngoài).

**Definition of Done:**
- [ ] `track_b_vlm/vlm_parser.py` chạy được, trả JSON đúng schema thống nhất.
- [ ] F1, latency, chi phí ghi vào `docs/reports/benchmark-results.md` và `docs/reports/cost-analysis.md`, đặt cạnh số liệu Track A để so sánh trực tiếp.

---

## Giai đoạn 6 — Mở rộng sang hợp đồng (CUAD)

**Việc cần làm:**
1. Chuẩn bị subset CUAD (vài chục đến vài trăm hợp đồng), chuyển định dạng SQuAD-style span extraction sang JSON schema thống nhất.
2. Chạy cả Track A (fine-tune thêm một lượt nhỏ trên CUAD hoặc dùng zero-shot để xem mức độ tổng quát hoá) và Track B (chỉ cần đổi prompt/schema, không cần train lại) trên tập CUAD.
3. So sánh mức độ giảm hiệu năng của từng track khi chuyển từ hóa đơn sang hợp đồng — đây là số liệu quan trọng nhất của phần mở rộng này.
4. Ghi nhận định: track nào tổng quát hoá tốt hơn, và tại sao (dựa trên kiến trúc — VLM-native thường tổng quát hoá tốt hơn vì không phụ thuộc fine-tune riêng biệt).

**Definition of Done:**
- [ ] Cả 2 track chạy được trên subset CUAD.
- [ ] `docs/reports/benchmark-results.md` có riêng một mục so sánh hiệu năng hóa đơn vs hợp đồng cho từng track.
- [ ] Nhận định bằng văn bản về khả năng tổng quát hoá, có số liệu dẫn chứng.

---

## Giai đoạn 7 — Fraud/Risk Engine

**Việc cần làm:**
1. Với hóa đơn: viết rule kiểm tra tổng tiền trước thuế + VAT = tổng tiền, phát hiện dấu hiệu vùng số bị chỉnh sửa (dựa vào độ tin cậy OCR bất thường ở vùng số).
2. Với hợp đồng: dùng taxonomy điều khoản có sẵn trong CUAD (loại điều khoản như Termination, Governing Law, Indemnification...) để viết rule phát hiện hợp đồng thiếu điều khoản chuẩn hoặc có điều khoản đánh dấu rủi ro cao.
3. Đóng gói cả hai thành `shared/fraud_rules.py`, expose qua field `risk_flags` trong JSON output.

**Definition of Done:**
- [ ] `shared/fraud_rules.py` chạy được cho cả hóa đơn và hợp đồng.
- [ ] Test thử với 1 hóa đơn cố tình sai số liệu và 1 hợp đồng cố tình thiếu điều khoản, xác nhận rule phát hiện đúng.

---

## Giai đoạn 8 — Explainability Layer

**Việc cần làm:**
1. Với Track A: trích attention weights từ LayoutLMv3 cho từng field đã dự đoán, ánh xạ về bounding box tương ứng trên ảnh gốc.
2. Với Track B: nếu model VLM hỗ trợ visual grounding/attention map, trích tương tự; nếu không hỗ trợ trực tiếp, dùng kỹ thuật gradient-based (Grad-CAM) trên input image.
3. Vẽ overlay heatmap lên ảnh gốc, đóng gói thành hàm dùng chung trong `shared/explainability.py`.
4. Expose qua endpoint `/explain` trả về ảnh overlay hoặc tọa độ heatmap.

**Definition of Done:**
- [ ] `shared/explainability.py` sinh được overlay heatmap cho ít nhất 3 field mẫu từ mỗi track.
- [ ] Ảnh minh hoạ lưu vào `docs/reports/explainability-report.md`.

---

## Giai đoạn 9 — Robustness Test & Benchmark tổng hợp

**Việc cần làm:**
1. Từ tập test thật (hóa đơn + hợp đồng), sinh biến thể: xoay 5-15 độ, làm mờ Gaussian, thêm watermark mờ, giảm độ sáng.
2. Chạy cả 2 track trên từng mức độ biến dạng, đo F1 giảm bao nhiêu so với ảnh gốc — vẽ đường cong độ giảm hiệu năng theo mức nhiễu.
3. Tổng hợp toàn bộ số liệu từ Giai đoạn 3 đến 9 (F1, latency, chi phí GPU-giờ, độ bền trước nhiễu) thành báo cáo benchmark cuối cùng.
4. Viết `docs/reports/cost-analysis.md` đối chiếu chi phí tự vận hành trên Modal với chi phí ước tính của API thương mại phổ biến (dựa trên giá công khai của các nhà cung cấp) cho cùng khối lượng trang xử lý.

**Definition of Done:**
- [ ] `docs/reports/robustness-report.md` có đường cong độ giảm F1 theo từng loại nhiễu, cho cả 2 track.
- [ ] `docs/reports/benchmark-results.md` là bản tổng hợp đầy đủ, có bảng so sánh cuối cùng giữa Track A và Track B trên mọi tiêu chí.
- [ ] `docs/reports/cost-analysis.md` hoàn chỉnh với số liệu đối chiếu chi phí.

---

## Giai đoạn 10 — FastAPI Service & Tài liệu hoá

**Việc cần làm:**
1. Viết `api/main.py` expose các endpoint: `/parse/classic`, `/parse/vlm`, `/compare` (chạy cả 2 track, trả kết quả song song), `/explain`.
2. Deploy service lên Modal (`modal deploy`), xác nhận endpoint hoạt động qua request thật.
3. Đóng gói `docker-compose.yml` hoàn chỉnh cho người khác chạy local (không cần tài khoản Modal, dùng model nhỏ hơn hoặc mock cho mục đích demo).
4. Hoàn thiện toàn bộ `docs/` (xem cấu trúc bên dưới), README.md ở root.

**Definition of Done:**
- [ ] API deploy thành công trên Modal, có URL truy cập được.
- [ ] `docker-compose.yml` chạy được bản demo local.
- [ ] README.md và toàn bộ docs/ hoàn chỉnh, không còn mục "TODO" hoặc "Chờ giai đoạn X".

---

## Cấu trúc thư mục

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

## Ghi chú chung cho AI hỗ trợ code
- Không train model từ đầu — luôn dùng pretrained, chỉ fine-tune LayoutLMv3 trên subset nhỏ để tiết kiệm GPU-giờ trên Modal.
- Mọi lần chạy tốn GPU trên Modal phải ghi log chi phí vào `log/progress-log.md` và tổng hợp vào `docs/reports/cost-analysis.md`.
- Track A và Track B luôn phải trả về cùng JSON schema (`shared/schema.py`) để so sánh công bằng.
- Không tự ý mở rộng phạm vi ngoài 10 giai đoạn đã định nghĩa — nếu phát hiện ý tưởng hay ngoài kế hoạch, ghi vào `docs/reports/benchmark-results.md` mục "Định hướng mở rộng" thay vì tự triển khai.
- Mỗi giai đoạn hoàn thành nên commit riêng, cập nhật `log/progress-log.md` ngay sau khi hoàn thành, không dồn lại.
