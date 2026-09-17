# Track B VLM — kế hoạch công việc chi tiết

## Owner và mục tiêu

**Owner chính:** Thành viên B — VLM/integration.

Track B là engine VLM-native. Mục tiêu là chuẩn bị tài liệu và instruction theo domain, nhận candidate structured response, validate rồi map thành `UnifiedDocumentOutput`.

```text
image/PDF + structured prompt
  → VLM inference → candidate response
  → parse + schema validation
  → Invoice fields hoặc Contract clauses
  → UnifiedDocumentOutput
```

“Single-pass” chỉ mô tả model-facing flow; preparation, parsing, validation, retry và logging vẫn là các bước bao quanh model call.

## Trong phạm vi

- chuẩn bị ảnh/PDF và chọn trang;
- prompt riêng cho Invoice và Contract;
- parse response và validate schema;
- xử lý missing value, malformed output và timeout;
- tích hợp model runner/endpoint sau khi model được chọn;
- logging latency, request metadata và failure;
- map value/evidence vào shared schema;
- test bằng response fixture deterministic.

## Ngoài phạm vi

- layout/OCR/KIE internals của Track A;
- React và browser state;
- tạo Node API backend;
- tự sửa response không hợp lệ thành giá trị có vẻ hợp lý;
- claim Track B tốt hơn nếu chưa benchmark công bằng;
- gọi paid endpoint hoặc tải weight khi chưa được duyệt.

## B1 — Chốt adapter và API boundary

Đọc [`schema.py`](../../src/docai/core/schema.py), API routes và data dictionary. Chốt adapter interface trước khi gắn external model:

- payload ảnh/PDF và page;
- response thô trước validation;
- prompt version và model metadata;
- cách biểu diễn “không tìm thấy”;
- mapping Invoice field/Contract clause;
- điều kiện evidence để coi value là có căn cứ.

**Done khi:** Thành viên A và Product Engineering đồng ý input/output và error vocabulary.

## B2 — Chuẩn bị input tài liệu

Chuẩn hóa page image, giới hạn kích thước, thứ tự trang và document type. Với contract dài, phải ghi rõ gửi toàn bộ, chọn trang hay chunk; không che giấu truncation.

**Kiểm tra:** page order, file không hỗ trợ, size limit và metadata deterministic.

## B3 — Thiết kế prompt có cấu trúc

Tạo prompt riêng cho Invoice/Contract, nêu rõ document type, field/clause cần lấy, kiểu dữ liệu, missing-value behavior, evidence, JSON shape và yêu cầu không bịa giá trị.

Version prompt bằng config/constant; không đưa prompt text vào frontend.

**Kiểm tra:** snapshot cho hai domain, coverage của required key và case field/clause vắng mặt.

## B4 — Implement model adapter

Bọc local runner, hosted endpoint hoặc Modal function sau một adapter. Phân biệt timeout/transport/model error với response hợp lệ. Ghi model/checkpoint nhưng không log credential hoặc toàn bộ tài liệu nhạy cảm.

PaddleOCR-VL và dots.ocr chỉ là candidate. Khi chưa chọn model, adapter vẫn là `SCAFFOLD`.

**Kiểm tra:** success mock, timeout, malformed response, model unavailable và thiếu credential.

## B5 — Parse và validate output

Không giả định model luôn trả JSON hợp lệ. Xử lý prose thừa, JSON thiếu, sai type, confidence ngoài `[0, 1]`, box đảo tọa độ. Pydantic là lớp kiểm tra contract cuối cùng.

Schema hợp lệ không chứng minh value đúng với tài liệu.

**Kiểm tra:** JSON thường/fenced/truncated, missing key, wrong type, invalid confidence và fixture value không có evidence.

## B6 — Map evidence và risk input

Map invoice seller/date/tax/total; map contract metadata, clause text, category, page và source evidence nếu có. Dùng chung risk layer, không copy Invoice Risk sang Track B.

Nếu VLM không có evidence thì giữ trạng thái thiếu evidence; không tạo highlight giả.

## B7 — Retry và observability

Định nghĩa lỗi được retry, số lần tối đa, backoff và idempotency. Ghi request ID, model/checkpoint, prompt version, page count, latency và final status; tuyệt đối không log secret.

Validation error không được retry vô hạn.

## B8 — Expose Track B runner

Runner nhận document và `DocumentType`, chọn prompt, gọi adapter, validate và trả `pipeline_track = track_b_vlm`. Khi adapter chưa sẵn sàng, runner phải báo lỗi rõ và không trả extraction giả.

Product Engineering phải gọi được runner mà không biết prompt/model internals.

## B9 — Bàn giao cho Research

Bàn giao prompt version, model/checkpoint, input preparation, generation settings, latency definition, failure list và mapping raw-to-validated. Fixture deterministic chỉ là test fixture, không phải benchmark result.

## Checklist bàn giao

- [ ] Runner và adapter interface được ghi rõ.
- [ ] Prompt/taxonomy Invoice và Contract tách biệt.
- [ ] Response validate bằng shared Pydantic schema.
- [ ] Malformed, missing và unsupported value báo lỗi rõ.
- [ ] Không log credential hoặc sensitive payload.
- [ ] Model/checkpoint và prompt version được ghi khi có.
- [ ] Không trả kết quả giả khi inference chưa có.
- [ ] Unit test và compile pass.
- [ ] Cập nhật progress log với file và status thực tế.

Code chính nằm trong [`src/docai/pipelines/track_b/`](../../src/docai/pipelines/track_b/). Thay đổi schema cần Thành viên A review; API orchestration thuộc Product Engineering; protocol và report thuộc Research.
