# Báo cáo robustness — DocAI Research Lab

**Trạng thái: PLANNED / REPORT SCAFFOLD.** Chưa có perturbation run hay đường cong suy giảm F1; chưa có kết luận production readiness.

## Phạm vi và phép thử

Đánh giá Track A/B trên Invoice và Contract bằng clean input và noisy variants có ground truth. Đây là Robustness Testing thuộc Research: cố tình làm input xấu để đo sức chịu đựng, không phải Document/Image Preprocessing của product.

Tách riêng hai phép so sánh:

```text
Product: raw image → preprocessing nếu cần → pipeline
Research: clean image → artificial degradation → pipeline → đo degradation
```

Perturbation dự kiến gồm rotation, Gaussian blur, low light/contrast, noise, watermark, crop và perspective distortion.

## Metrics

Đo Precision/Recall/F1 theo domain và field/clause, `ΔF1 = F1_clean - F1_noisy`, thay đổi latency/cost và nguyên nhân lỗi OCR/layout/KIE/VLM khi chẩn đoán được.

Chỉ nói track nào robust hơn khi protocol, workload và số liệu được tái lập giống nhau. Không suy ra robustness từ kiến trúc lý thuyết.
