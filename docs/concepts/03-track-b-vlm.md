# 03. Vì sao Track B có thể trả kết quả trong một model call?

**VLM (Vision-Language Model)** là model làm việc với cả hình ảnh và ngôn ngữ. Track B đưa ảnh tài liệu cùng structured prompt vào model, rồi parse và validate kết quả.

```text
Invoice/Contract image + instruction
  → VLM inference → candidate response
  → parse + schema validation → UnifiedDocumentOutput
```

Single-pass chỉ mô tả cách model nhìn bài toán; preparation, validation, retry và logging vẫn là các bước bao quanh.

## VLM bên trong làm gì?

Vision encoder biến các patch ảnh thành biểu diễn số; language model xử lý instruction/token; connector giúp hai loại thông tin ảnh và chữ ảnh hưởng lẫn nhau. **Multimodal** nghĩa là dùng nhiều loại input. **Embedding** là dãy số giúp model liên hệ số tiền với nhãn `Total`.

## Prompt và structured output có tác dụng gì?

**Prompt** là instruction gửi cho model. **Structured prompt** nói rõ document type, field/clause cần lấy, cách biểu diễn missing value, evidence và JSON shape. Invoice có thể yêu cầu seller/date/tax/total; Contract có thể yêu cầu termination/renewal/payment clause và page evidence.

**Structured Output** là response có hình dạng ổn định thay vì đoạn văn. Pydantic validate key, type, confidence và box. Validation bắt lỗi hình dạng, không chứng minh value có thật trong tài liệu.

## Hallucination nguy hiểm thế nào?

**Hallucination** là khi model sinh ra nội dung nghe hợp lý nhưng không có trong tài liệu. Ví dụ invoice không có tax number nhưng model tự điền một số; hợp đồng không có renewal clause nhưng model tự viết clause. Prompt yêu cầu trả “không tìm thấy”, schema validation và evidence giúp giảm rủi ro, nhưng không đảm bảo đúng tuyệt đối.

## Track B khác Track A ra sao?

Track A giống nhiều specialist; Track B giống một generalist có thể đổi task nhờ prompt. Một VLM không tự động giỏi mọi domain: vẫn cần prompt, taxonomy, validation và evaluation riêng cho Invoice/Contract. Response đã validate mới được backend map sang `UnifiedDocumentOutput`, không trả thẳng cho browser.

Model cụ thể như PaddleOCR-VL hoặc dots.ocr chưa được chọn; parser hiện là `SCAFFOLD`. Không kết luận Track B tốt hơn nếu chưa có ground truth và benchmark công bằng.
