# 05. Làm sao biết Track A hay Track B thực sự hoạt động tốt?

Sơ đồ kiến trúc không cho biết engine nào tốt hơn. Cần **ground truth** (đáp án tham chiếu đáng tin), protocol lặp lại được và đo đúng câu hỏi.

## Đo đúng và bỏ sót

Trước hết phải ghi rõ domain, dataset/split, track, model/checkpoint, taxonomy và cách match field/clause. **Precision** hỏi: trong các item hệ thống dự đoán, bao nhiêu item đúng? **Recall** hỏi: trong mọi item thật sự tồn tại, hệ thống tìm được bao nhiêu?

`TP` là item dự đoán đúng, `FP` là item dự đoán sai, `FN` là item bị bỏ sót:

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 × Precision × Recall / (Precision + Recall)
```

F1 cân bằng Precision và Recall. Con số như `0.82` không có ý nghĩa nếu không biết nó đo field/clause nào, domain nào, dataset nào và track nào.

## Đo tốc độ, chi phí và độ bền

**Latency** là thời gian từ request đến response; phải ghi rõ có tính model loading/warm-up không. **Cost** gồm GPU time, API charge và các giả định về page, batch, hardware; estimate không phải actual measurement.

**Robustness** là khả năng giữ chất lượng khi input bị blur, xoay, thiếu sáng hoặc che nhẹ. Có thể báo `ΔF1 = F1_clean - F1_noisy`; hai track phải dùng cùng protocol và workload.

## So sánh hai track

Khi cùng trả `UnifiedDocumentOutput`, Research có thể so value, missing field, confidence, evidence và agreement/disagreement. Agreement không chứng minh đúng nếu cả hai cùng sai; disagreement là mẫu cần review.

Metric helper nằm ở [`src/docai/evaluation/`](../../src/docai/evaluation/), report ở [`docs/reports/`](../reports/). Hiện chúng là `SCAFFOLD`/`PLANNED`, chưa có benchmark thật.
