# Track A Classic — kế hoạch công việc chi tiết

## Owner và mục tiêu

**Owner chính:** Thành viên A — AI/ML/DL.

Track A là pipeline xử lý theo nhiều chặng. Mục tiêu là biến ảnh hoặc PDF thành layout regions, tokens, vị trí và business meaning, sau đó trả về `UnifiedDocumentOutput`. Track A là một pipeline boundary, không đồng nghĩa với một model duy nhất.

```text
document → layout → OCR text + box → KIE labels
          → invoice fields hoặc contract clauses
          → UnifiedDocumentOutput
```

## Trong phạm vi

- preprocessing ảnh/trang và layout detection;
- OCR, confidence, polygon và bounding box;
- tokenization và chuẩn hóa tọa độ;
- KIE, BIO tagging và aggregation;
- mapping riêng cho Invoice và Contract;
- model/checkpoint metadata và inference configuration;
- phân tích lỗi theo từng stage và input cho evaluation;
- unit test cho transformation và schema compatibility.

## Ngoài phạm vi

- React, browser state và TypeScript API calls;
- FastAPI upload/orchestration, ngoại trừ việc thống nhất interface;
- prompt hoặc response parsing của Track B;
- tự đổi risk policy;
- claim accuracy khi chưa có ground truth và run tái lập;
- train/fine-tune/tải weight nếu chưa có task riêng.

## A1 — Chốt contract nội bộ

Đọc [`schema.py`](../../src/docai/core/schema.py), các pipeline stub và data dictionary. Ghi rõ input/output của từng stage trước khi viết model code:

- dạng ảnh/trang được nhận;
- token gồm text, confidence, box và page như thế nào;
- label vocabulary của layout;
- cách biểu diễn missing OCR/KIE;
- Invoice field khác Contract clause ra sao;
- `pipeline_track` và `metadata` được điền khi nào.

**Done khi:** interface được ghi trong docstring/design note và hai thành viên đồng ý rằng output có thể tạo `UnifiedDocumentOutput`.

## A2 — Layout và preprocessing

Chốt image size, page number, hệ tọa độ và các utility chuyển đổi. Model loading phải nằm sau interface rõ ràng; thiếu checkpoint phải báo lỗi, không trả kết quả giả.

YOLOv8-doc và DocLayout-YOLO chỉ là candidate cho tới khi checkpoint được chọn.

**Output:** region có label, confidence, page và bounding box.

**Kiểm tra:** box không đảo tọa độ, page hợp lệ và test chuyển tọa độ ảnh sang schema.

## A3 — OCR boundary

Tích hợp OCR đã được chọn, giữ raw text, confidence, vị trí và page. Polygon phải chuyển thành box mà không mất traceability.

**Output:** danh sách token/dòng chữ có text, confidence và location.

**Kiểm tra:** test polygon conversion, empty result, confidence range và mẫu kiểm tra tay khi có dữ liệu thật.

## A4 — Gắn layout context cho OCR

Định nghĩa cách token thuộc region, xử lý overlap và token nằm ngoài region. Label layout chỉ là context, không tự động là business field.

**Kiểm tra:** case inside/outside/overlap và bảo đảm tọa độ gốc vẫn truy được.

## A5 — Chuẩn bị input KIE

Chuẩn bị token text, box và thông tin ảnh cho model document understanding. Nếu dùng LayoutLMv3, ghi riêng quy ước tọa độ nội bộ `[0, 1000]` với schema `[0, 1]`.

BIO tagging:

```text
B-FIELD → bắt đầu field
I-FIELD → tiếp tục field
O       → không thuộc field cần lấy
```

**Kiểm tra:** entity nhiều token, BIO lỗi, truncation và taxonomy Invoice/Contract tách biệt.

## A6 — Gom field và clause

Gom entity BIO liên tiếp, giữ raw text, chỉ normalize khi có rule rõ ràng, và tính union box nếu phù hợp. Contract phải giữ clause text/page evidence; không ép mọi clause thành scalar Invoice.

**Output:** các `ExtractedField` hợp lệ.

**Kiểm tra:** seller/date/total cho Invoice; termination/renewal/payment cho Contract; empty, duplicate và broken entity.

## A7 — Expose Track A runner

Tạo một entry point điều phối các stage theo đúng thứ tự. Runner trả `UnifiedDocumentOutput` hợp lệ hoặc typed error rõ ràng. Điền `pipeline_track = track_a_classic`, model/checkpoint vào metadata khi biết và chỉ đo timing khi runtime thật tồn tại.

Product Engineering phải gọi được runner mà không import model internals.

## A8 — Error analysis và bàn giao

Cung cấp diagnostic theo stage để Research phân biệt lỗi layout, OCR và KIE. Run record phải ghi model/checkpoint, preprocessing, hardware, input scope và failure counts.

Không ghi Precision/Recall/F1 nếu chưa có ground truth và run tái lập. Bàn giao output examples và protocol cho Research.

## Checklist bàn giao

- [ ] Runner, type hints và input/output được ghi rõ.
- [ ] Output validate được bằng `UnifiedDocumentOutput`.
- [ ] Mapping Invoice và Contract tách riêng.
- [ ] Coordinate convention và page numbering đã ghi.
- [ ] Thiếu model/input báo lỗi rõ, không trả dữ liệu giả.
- [ ] Trạng thái model là `NOT SELECTED`, `SCAFFOLD` hoặc có evidence.
- [ ] Unit test và compile pass.
- [ ] Cập nhật progress log với file và status thực tế.

Code chính nằm trong [`src/docai/pipelines/track_a/`](../../src/docai/pipelines/track_a/). Thay đổi schema cần Thành viên B review.
