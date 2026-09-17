# 02. Vì sao Track A chia xử lý tài liệu thành nhiều specialist step?

Track A là processing engine cổ điển theo nhiều chặng; không phải một product riêng và cũng không bắt buộc chỉ có một model.

## Vì sao phải chia chặng?

Ý nghĩa của tài liệu phụ thuộc cả chữ lẫn vị trí. Track A làm rõ từng phần để dễ kiểm tra:

```text
Document → Layout Detection → OCR → Document Understanding/KIE
         → mapping Invoice field hoặc Contract clause
         → UnifiedDocumentOutput
```

Nếu `total_amount` mất, ta có thể kiểm tra layout có cắt mất vùng không, OCR có đọc sai không hay KIE gán sai nhãn. Nhược điểm là **error cascade**: stage sau không thể khôi phục thông tin stage trước đã bỏ mất.

## Layout Detection và OCR làm gì?

**Layout Detection** tìm và phân loại vùng trên trang, giống như nhìn bố cục tờ báo trước khi đọc. Kết quả là bounding box của `table`, `header`, `total`… Các model họ YOLO là candidate; NMS loại box trùng và IoU đo phần giao nhau giữa hai box.

**OCR** gồm text detection (tìm chữ ở đâu) và text recognition (đổi vùng chữ thành Unicode). OCR phải giữ text, confidence và polygon/box. Polygon có thể đổi thành rectangle bằng min/max tọa độ. Token OCR nằm trong layout region nào có thể nhận region đó làm context.

## Vì sao KIE cần LayoutLMv3?

OCR chỉ trả token, ví dụ `Total`, `amount`, `1,500,000`; **KIE (Key Information Extraction)** phải quyết định số nào là `total_amount`. **LayoutLMv3** là Transformer kết hợp text token, 2D box và visual patch, nên có thể dùng quan hệ “số nằm cạnh nhãn Total”.

**Token** là đơn vị nhỏ model xử lý; **embedding** là biểu diễn số của token/ảnh; **attention** là cơ chế cân nhắc context nào ảnh hưởng đến dự đoán. Attention là tín hiệu nội bộ, không tự động là bằng chứng giải thích hoàn hảo.

LayoutLM thường chuẩn hóa tọa độ nội bộ về `[0,1000]`, trong khi schema DocAI có thể dùng `[0,1]`; phải chuyển đổi rõ ở boundary.

## BIO, pretrained và fine-tuning

KIE dùng **BIO tagging** để biết field nhiều token bắt đầu ở đâu: `B-SELLER` bắt đầu, `I-SELLER` tiếp tục, `O` là ngoài field. Aggregation ghép các token liên tiếp và tạo union box.

**Pretrained model** giống người đã biết kiến thức nền. **Fine-tuning** là đào tạo thêm để chuyên đọc Invoice hoặc Contract. **Checkpoint** là trạng thái model đã lưu; **inference** là dùng trạng thái đó trên tài liệu mới. Checkpoint production của Track A chưa được chọn; các module hiện là `SCAFFOLD`.

## Vì sao Invoice và Contract có thể dùng specialist khác nhau?

Track A giống một bệnh viện: layout/OCR là khoa chung, Invoice KIE là bác sĩ chuyên hóa đơn, Contract clause model là bác sĩ chuyên hợp đồng. Invoice cần seller/date/tax/total; Contract cần clause span, page context và taxonomy pháp lý. Output cuối cùng vẫn về `UnifiedDocumentOutput` để FastAPI, risk và React dùng chung.
