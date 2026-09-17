# Robustness report — DocAI Research Lab

**Trạng thái: PLANNED / REPORT SCAFFOLD.** Chưa có perturbation run hoặc F1 degradation curve. Không có kết luận về production readiness.

## Phạm vi

Đánh giá Track A và Track B trên cả Invoice và Contract khi có dataset, ground truth và pipeline runtime thật. So sánh clean input với noisy variants tương ứng.

## Perturbation suite dự kiến

- rotation ở nhiều mức;
- Gaussian blur;
- low illumination/low contrast;
- watermark hoặc che khuất nhẹ;
- các biến dạng khác chỉ thêm khi protocol và ground truth vẫn hợp lệ.

## Metrics

- F1/Precision/Recall theo domain và field/clause;
- `ΔF1 = F1_clean - F1_noisy`;
- latency/cost thay đổi dưới nhiễu;
- lỗi OCR/layout/KIE hoặc VLM parsing theo nguyên nhân;
- evidence/explainability stability khi có measurement phù hợp.

## Tiêu chí kết luận

Chỉ mô tả track nào robust hơn khi dùng cùng protocol, cùng workload và số liệu tái lập. Không suy ra khả năng chống nhiễu hoặc production readiness từ kiến trúc lý thuyết.
