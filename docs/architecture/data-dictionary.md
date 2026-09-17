# Từ điển dữ liệu — kết quả DocAI có nghĩa gì?

Tài liệu này mô tả contract chung của Track A, Track B, FastAPI và React. Contract được implement bằng Pydantic trong [`schema.py`](../../src/docai/core/schema.py) và mirror bằng TypeScript trong [`document.ts`](../../frontend/src/types/document.ts).

## Envelope chung

Hai engine đều trả `UnifiedDocumentOutput`. Có thể hình dung đây là một chiếc hộp có nhãn cố định: nội dung Invoice và Contract khác nhau nhưng consumer biết vị trí của document type, item, confidence và flag.

| Field | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `document_type` | `invoice \| receipt \| contract \| unknown` | Loại tài liệu. |
| `fields` | mảng `ExtractedField` | Field Invoice hoặc metadata/clause Contract. |
| `overall_confidence` | số `0`–`1` | Confidence tổng thể, không phải bằng chứng đúng tuyệt đối. |
| `risk_flags` | mảng `RiskFlag` | Tín hiệu cần người dùng review. |
| `execution_time_ms` | số hoặc `null` | Thời gian xử lý nếu đo được. |
| `pipeline_track` | chuỗi hoặc `null` | Engine tạo ra output. |
| `metadata` | object JSON | Thông tin trace như kích thước ảnh/checkpoint. |

API contract là thỏa thuận về hình dạng này giữa các phần mềm. Khi đổi schema phải review cả backend và frontend.

## `ExtractedField` là gì?

Đây là một câu trả lời lấy từ tài liệu. Invoice có thể dùng `seller_name`, `total_amount`; Contract có thể dùng `termination_clause`.

| Field | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `field_name` | string | Tên business ổn định. |
| `field_value` | string | Giá trị đã normalize để consumer dùng. |
| `confidence` | số `0`–`1` | Confidence của item. |
| `bounding_box` | `BoundingBox` hoặc `null` | Vị trí trên ảnh nếu có. |
| `page_number` | integer ≥ `1` | Trang chứa item. |
| `raw_text` | string hoặc `null` | Text gốc trước normalize. |

Invoice thường có box quanh số in trên ảnh. Contract có thể cần page và supporting text hơn là một hình chữ nhật.

## Vị trí được lưu thế nào?

`BoundingBox` có `xmin`, `ymin`, `xmax`, `ymax`. `normalized: true` nghĩa tọa độ nằm trong `[0, 1]`; `false` nghĩa tọa độ tuyệt đối như pixel. LayoutLM có thể dùng quy ước nội bộ `[0, 1000]`; phải chuyển đổi ở boundary và không đoán theo phía consumer.

## Risk flag và đường đi dữ liệu

`RiskFlag` là tín hiệu review, gồm `rule_id`, `rule_name`, `severity`, `description` và `target_field` tùy chọn. Invoice Risk có thể phát hiện arithmetic mismatch; Contract Risk có thể đánh dấu clause thiếu/bất thường. Hai domain dùng chung list nhưng rule vẫn tách biệt.

```text
pipeline/model output
  → Pydantic validation
  → JSON từ FastAPI
  → TypeScript type
  → React rendering
```

Frontend không đọc Python file hoặc duplicate extraction logic. List rỗng, `null` và scaffold response phải được giữ nguyên. Parse endpoint hiện trả `501`, nên UI không được bịa kết quả.
