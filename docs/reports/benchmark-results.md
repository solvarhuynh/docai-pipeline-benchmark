# Benchmark results — DocAI Research Lab

**Trạng thái: PLANNED / REPORT SCAFFOLD.** Repository chưa tải dataset, chưa có output inference thật và chưa có benchmark result. Không điền số liệu giả vào tài liệu này.

## Research scope

Benchmark sẽ so sánh Track A Classic và Track B VLM-native khi cả hai trả cùng `UnifiedDocumentOutput`, theo từng domain:

- **Invoice**: tài liệu ngắn, nhiều số, bảng biểu và field tương đối rõ.
- **Contract**: tài liệu dài, ngôn ngữ pháp lý, clause và quan hệ ngữ nghĩa phức tạp; CUAD phục vụ cả Contract capability và generalization research.

## Metrics sẽ ghi nhận

- field-level Precision, Recall, F1 trên ground truth;
- OCR/layout metrics khi phù hợp;
- latency theo page/document;
- robustness trên clean/noisy variants;
- explainability evidence quality và localization khi có ground truth phù hợp;
- cost measurement hoặc estimate có nêu rõ assumptions;
- agreement/disagreement giữa hai track.

## Milestones

1. Track A layout/OCR baseline — `PLANNED`.
2. Track A KIE/LayoutLMv3 — `PLANNED`.
3. Track B VLM parsing — `PLANNED`; model cụ thể chưa chốt.
4. Invoice comparison — `PLANNED`.
5. Contract/CUAD extraction và clause analysis — `PLANNED`.
6. Clean/noisy robustness — `PLANNED`.
7. Cost analysis và tổng hợp — `PLANNED`.

Không kết luận track nào thắng trước khi có output thật, ground truth và số liệu được tái lập. Research Complete là milestone riêng, không suy ra từ Product MVP.

## Định hướng mở rộng

Ý tưởng ngoài roadmap 10 phase được ghi ở đây, không tự động triển khai trong task định vị.
