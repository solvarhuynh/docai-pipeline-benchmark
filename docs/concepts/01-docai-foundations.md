# 01. Vì sao DocAI cần nhiều hơn một trình đọc ảnh?

## Vấn đề bắt đầu từ đâu?

Con người nhìn hóa đơn và thấy ngay người bán, ngày, bảng hàng và tổng tiền. Máy tính ban đầu chỉ nhận các điểm ảnh (**pixel**), tức những chấm màu nhỏ. Hợp đồng còn khó hơn vì thông tin có thể trải dài qua nhiều trang và nằm trong các clause có ý nghĩa pháp lý.

```text
ảnh/PDF → đọc chữ + vị trí → hiểu meaning → field/clause → JSON có cấu trúc
```

## OCR biến pixel thành chữ ra sao?

**OCR (Optical Character Recognition)** là công nghệ đọc chữ từ ảnh. Khi camera chụp dòng `Total: 500.000đ`, OCR biến hình dạng pixel thành text để phần mềm phía sau xử lý. OCR có thể đọc nhầm ký tự và chưa biết số đó là total, tax hay giá một dòng hàng.

## Vì sao vị trí cũng quan trọng?

**Bounding Box** là hình chữ nhật cho biết một chữ/vùng nằm ở đâu, thường dùng `[xmin, ymin, xmax, ymax]`. Số ở cạnh chữ `Total` có khả năng là tổng tiền cao hơn số nằm giữa bảng sản phẩm. **Layout Detection** tìm các vùng như header, table, signature hoặc total trước khi hiểu chúng.

## Field, clause và document type là gì?

**Field** là một giá trị có tên, ví dụ `invoice_date` hoặc `total_amount`. **Clause** là một đoạn có ý nghĩa trong hợp đồng, ví dụ termination clause. `DocumentType` cho biết input là `invoice`, `receipt`, `contract` hay `unknown`, để hệ thống chọn mapping và risk rules đúng domain.

## Structured Output giải quyết bước nào?

Text rời rạc chưa đủ cho kế toán hay ứng dụng khác. **Structured Output** là kết quả theo hình dạng ổn định, ví dụ `UnifiedDocumentOutput`, gồm document type, fields, confidence, vị trí, risk flags và metadata. **Pydantic** kiểm tra object Python có đúng schema hay không; sau đó FastAPI trả JSON cho React.

```text
Track A ─┐
         ├→ UnifiedDocumentOutput → FastAPI JSON → React
Track B ─┘
```

Schema kiểm tra hình dạng, không tự chứng minh giá trị trích xuất là đúng. Accuracy cần ground truth và evaluation riêng.
