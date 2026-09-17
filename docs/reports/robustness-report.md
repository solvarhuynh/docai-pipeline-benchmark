# Báo cáo độ bền trước nhiễu (Robustness Report)

Ghi chú: Chờ Giai đoạn tương ứng (Giai đoạn 9).
Nội dung thật và đường cong độ giảm hiệu năng F1 sẽ được tổng hợp sau khi chạy bộ kiểm thử Robustness Test Suite ở Giai đoạn 9.

---

## 1. Thiết kế bộ nghịch biến (Perturbation Suite)
- Xoay lệch góc (Rotation): 5 độ, 10 độ, 15 độ.
- Làm mờ quang học (Gaussian Blur): kernel size 3x3, 5x5, 7x7.
- Giảm độ sáng / độ tương phản (Low illumination / Low contrast): 70%, 50%, 30%.
- Watermark mờ đè lên nội dung văn bản.

## 2. Đường cong suy giảm F1-score theo loại nhiễu (Track A vs Track B)
- Biểu đồ độ giảm F1 khi tăng mức độ xoay góc ảnh.
- Biểu đồ độ giảm F1 khi tăng độ mờ Gaussian.
- Biểu đồ độ giảm F1 dưới điều kiện thiếu sáng và nhiễu watermark.

## 3. Phân tích nguyên nhân và tính ổn định hệ thống
- Điểm đứt gãy của Track A (ví dụ: PaddleOCR nhạy cảm với góc nghiêng nếu không bật angle classification).
- Khả năng chống chịu của Track B (VLM-native với cơ chế visual attention tự động bù trừ nhiễu).
- Kết luận về tính sẵn sàng đưa vào production trong môi trường thực tế.
