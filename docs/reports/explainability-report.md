# Báo cáo khả năng giải thích mô hình (Explainability Report)

Ghi chú: Chờ Giai đoạn tương ứng (Giai đoạn 8).
Nội dung thật và các hình ảnh minh hoạ overlay heatmap sẽ được bổ sung khi hoàn tất Giai đoạn 8.

---

## 1. Cơ chế giải thích của Track A (LayoutLMv3 Attention Weights)
- Phương pháp trích xuất attention maps giữa các token và nhãn KIE.
- Ánh xạ từ token coordinates sang pixel bounding box trên ảnh gốc.
- Mẫu overlay heatmap trên 3 trường dữ liệu hóa đơn (ví dụ: Total Amount, Invoice Date, Seller Name).

## 2. Cơ chế giải thích của Track B (VLM Visual Grounding / Grad-CAM)
- Phương pháp truyền ngược gradient hoặc trích xuất visual grounding token từ VLM.
- Mẫu overlay heatmap trên hóa đơn và hợp đồng mẫu.

## 3. Đánh giá so sánh độ tin cậy vùng nhìn (Visual Localization Quality)
- Đánh giá tính hợp lý của vùng tập trung chú ý giữa hai kiến trúc.
- Khả năng phát hiện ảo giác (hallucination) thông qua heatmap chú ý lệch vị trí.
