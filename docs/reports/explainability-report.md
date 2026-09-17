# Explainability report — DocAI

**Trạng thái: SCAFFOLD / PLANNED.** `DocumentExplainer` mới cung cấp interface; chưa có overlay heatmap hoặc đánh giá localization runtime.

## Product evidence theo domain

- **Invoice**: field bounding box, highlighting, confidence và input của arithmetic/risk rule.
- **Contract**: text span, page/clause location, clause category và supporting passage.

## Kỹ thuật sẽ đánh giá

- Track A: token/bounding-box evidence và LayoutLMv3 attention nếu model artifact hỗ trợ.
- Track B: visual grounding hoặc gradient-based method nếu model artifact hỗ trợ.
- So sánh evidence với annotation/ground truth phù hợp; không coi attention là explanation hoàn hảo.

## Tiêu chí hoàn thành

- Có output evidence thật cho cả domain/track trong phạm vi được chọn.
- Có mô tả input, model artifact, phương pháp và giới hạn.
- Có kiểm tra localization hoặc supporting passage khi ground truth cho phép.
- Không dùng heatmap minh hoạ giả để tuyên bố explainability đã hoàn thành.
