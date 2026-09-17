# Báo cáo explainability — DocAI

**Trạng thái: SCAFFOLD / PLANNED.** `DocumentExplainer` mới là interface; chưa có heatmap overlay hoặc localization runtime.

## Evidence theo domain

- **Invoice:** field bounding box, highlighting, confidence và input của arithmetic/risk rule.
- **Contract:** text span, page/clause location, clause category và supporting passage.

Track A có thể dùng token/box evidence và LayoutLMv3 attention nếu artifact hỗ trợ. Track B có thể dùng visual grounding hoặc gradient-based method nếu artifact hỗ trợ. Attention không tự động là explanation hoàn hảo.

## Điều kiện hoàn thành

Phải có evidence thật cho phạm vi đã chọn, mô tả model/method/giới hạn và kiểm tra localization hoặc supporting passage khi ground truth cho phép. Không dùng heatmap giả để tuyên bố hoàn thành.
