# Kết quả benchmark — DocAI Research Lab

**Trạng thái: PLANNED / REPORT SCAFFOLD.** Repository chưa tải dataset, chưa có inference output thật và chưa có benchmark result. Không điền metric giả.

## Phạm vi nghiên cứu

So sánh Track A Classic và Track B VLM-native khi cả hai trả cùng `UnifiedDocumentOutput`, tách riêng Invoice và Contract. Invoice là tài liệu ngắn, nhiều số/bảng; Contract là tài liệu dài, clause và quan hệ ngữ nghĩa phức tạp. CUAD phục vụ cả Contract capability và research.

## Metrics dự kiến

Field/clause Precision, Recall, F1; OCR/layout metrics khi phù hợp; latency theo page/document; robustness clean/noisy; chất lượng evidence; cost measurement/estimate có assumption; agreement/disagreement giữa hai track.

## Milestone

Layout/OCR, KIE, VLM parsing, Invoice comparison, Contract/CUAD, robustness và cost đều đang `PLANNED`. Chỉ kết luận track nào tốt hơn sau khi có output thật, ground truth và số liệu tái lập.
