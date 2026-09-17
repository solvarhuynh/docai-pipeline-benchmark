# 04. DocAI nên đánh dấu rủi ro và giải thích kết quả thế nào?

Extraction trả lời “tài liệu nói gì?”. Risk và explainability trả lời “điều gì cần chú ý?” và “kết quả dựa vào đâu?”. Đây là lớp hỗ trợ review cho cả Track A và Track B.

## Vì sao output không tự động đáng tin?

Invoice có thể ghi subtotal `100`, tax `10`, total `150`; OCR đọc đúng chữ nhưng các số không khớp. Vì vậy output cần confidence, raw text, bounding box và risk flag. Confidence là ước lượng của model, không phải cam kết đúng.

## Invoice Risk khác Contract Risk thế nào?

**Invoice Risk** kiểm tra arithmetic mismatch, field quan trọng bị thiếu, amount không nhất quán hoặc confidence thấp. Đây là tín hiệu kiểm tra giao dịch, không phải bằng chứng fraud.

**Contract Risk** đánh dấu clause thiếu/bất thường hoặc metadata không nhất quán. Nó hỗ trợ người review và không kết luận hợp đồng hợp pháp, vô hiệu hay thay thế luật sư.

## Evidence có dạng gì?

Invoice có thể highlight bounding box của `total_amount` để người dùng đối chiếu với nhãn in. Contract thường cần text span, page, clause heading và supporting passage. Nếu pipeline không có evidence, UI phải nói rõ, không vẽ highlight giả.

**Attention**/heatmap có thể là tín hiệu chẩn đoán vùng model chú ý, nhưng không phải causal proof. Visual grounding hoặc gradient-based overlay chỉ được gọi là explanation sau khi có model thật và kiểm tra localization. `src/docai/explainability/` hiện là scaffold.

```text
Track A/B → UnifiedDocumentOutput
          → field/clause + confidence + evidence
          → domain risk → reviewer
```
