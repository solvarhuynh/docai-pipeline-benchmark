# 04. Vì sao Document Intelligence cần Risk và Explainability?

AI có thể đọc ra một field nhưng người dùng vẫn cần biết field đó đến từ đâu và có dấu hiệu bất thường nào không. DocAI vì vậy có hai lớp hỗ trợ review: domain risk rules và explainability evidence. Hai lớp này phục vụ cả Invoice Intelligence và Contract Intelligence.

## Model prediction khác rule-based risk ở điểm nào?

Model prediction là kết quả xác suất, thường đi kèm confidence. Rule engine là logic nghiệp vụ minh bạch, dùng output đã trích xuất để gắn cờ khi có điều kiện cụ thể. Risk flag là tín hiệu để người dùng xem xét, không phải phán quyết cuối cùng.

```text
Document → Track A/B → UnifiedDocumentOutput
                     ↙                 ↘
             Domain Risk           Evidence / Explanation
                     ↘                 ↙
                    Human review / decision support
```

## Invoice Risk: kiểm tra điều gì?

`src/docai/fraud/rules.py` hiện có baseline cho Invoice/Receipt:

- `subtotal_amount + tax_amount` so với `total_amount`, trong `arithmetic_tolerance`;
- thiếu `total_amount`;
- confidence thấp ở field liên quan đến amount/total.

Rule `RULE_INVOICE_ARITHMETIC_MISMATCH` phát hiện inconsistency số học. Rule confidence chỉ phát hiện tín hiệu cần review; confidence thấp không tự chứng minh tài liệu bị chỉnh sửa hay gian lận. Chuẩn hoá tiền tệ nâng cao, missing-field taxonomy rộng hơn và kiểm tra forensic chưa triển khai.

## Contract Risk: khác Invoice Risk như thế nào?

Contract không nên bị gắn nhãn “fraud” chỉ vì phát hiện một vấn đề về clause. Contract Risk tập trung vào:

- missing important/required clause;
- clause category cần người review;
- metadata hoặc clause inconsistency khi có evidence;
- supporting passage để người dùng kiểm tra lại.

`check_contract_clauses` hiện kiểm tra một nhóm clause bắt buộc (`governing_law`, `termination_clause`, `dispute_resolution`) và tạo `RiskFlag`. Đây là baseline, không phải taxonomy CUAD đầy đủ. CUAD giữ vai trò kép: hỗ trợ Contract Information Extraction/Clause Detection/Risk Analysis trong product và cung cấp ground truth cho research.

Hệ thống hỗ trợ document review, information extraction và decision support. Nó không thay luật sư, không đưa ra tư vấn pháp lý chắc chắn và không kết luận hợp đồng hợp pháp/bất hợp pháp.

## Explainability cần trả lời câu hỏi gì?

Người dùng cần biết:

1. Thông tin này được lấy từ đâu?
2. Tại sao hệ thống đưa ra risk flag này?

Định hướng evidence theo domain:

- Invoice: field bounding box, field highlighting, confidence và rule inputs.
- Contract: text span, page/clause location, clause category và supporting passage.

Attention, heatmap, visual grounding và Grad-CAM có thể hỗ trợ phân tích model, nhưng attention không đồng nghĩa với explanation hoàn hảo. Cần validation riêng trước khi dùng như bằng chứng cho người dùng.

## Hai track cung cấp evidence ra sao?

```text
Track A: Layout/OCR/KIE
  → token và bounding box
  → field evidence (khi pipeline thực tế hỗ trợ)

Track B: VLM structured response
  → model-provided grounding hoặc supporting span (nếu có)
  → evidence sau schema validation
```

`src/docai/explainability/explainer.py` hiện định nghĩa interface cho LayoutLMv3 attention, VLM grounding và overlay heatmap nhưng các method còn `NotImplementedError`. Trạng thái là `SCAFFOLD`, không phải runtime explanation.

## Vị trí trong product và research

- Product sử dụng risk flags/evidence để người dùng review Invoice hoặc Contract.
- Research đánh giá xem evidence có location/supporting passage hay không, mức ổn định trên clean/noisy input và trade-off giữa hai track.
- API `/explain` là product interface; `/compare` và các báo cáo evaluation là Research Lab.

Các module liên quan:

- [`src/docai/fraud/rules.py`](../../src/docai/fraud/rules.py)
- [`src/docai/explainability/explainer.py`](../../src/docai/explainability/explainer.py)
- [`src/docai/core/schema.py`](../../src/docai/core/schema.py)
- [`tests/unit/test_fraud_rules.py`](../../tests/unit/test_fraud_rules.py)
