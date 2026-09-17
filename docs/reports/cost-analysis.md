# Báo cáo phân tích chi phí vận hành — Modal vs Commercial APIs

Ghi chú: Chờ Giai đoạn tương ứng (Giai đoạn 4, Giai đoạn 5, Giai đoạn 9).
Nội dung thật sẽ được tổng hợp và điền dần khi các giai đoạn tính toán GPU hoàn tất.

---

## 1. Chi phí Huấn luyện / Fine-tuning trên Modal (Chờ Giai đoạn 4)
- Loại GPU sử dụng (T4 / A10G / A100).
- Thời gian huấn luyện thực tế (GPU-giờ).
- Đơn giá Modal theo giờ và tổng chi phí tính bằng USD.

## 2. Chi phí Inference trên 1.000 trang tài liệu (Chờ Giai đoạn 5 & 9)
- Track A (Classic: YOLO + PaddleOCR + LayoutLMv3):
  - Thời gian xử lý mỗi trang (giây).
  - Chi phí serverless Modal trên 1.000 trang.
- Track B (VLM-native: PaddleOCR-VL / dots.ocr):
  - Thời gian xử lý mỗi trang (giây).
  - Chi phí serverless Modal trên 1.000 trang.

## 3. Đối chiếu với API thương mại phổ biến (Chờ Giai đoạn 9)
- So sánh với đơn giá công khai của:
  - Google Cloud Document AI
  - AWS Textract
  - Azure AI Document Intelligence
- Bảng phân tích điểm hoà vốn (break-even point) giữa tự vận hành Modal và dùng API SaaS theo quy mô tài liệu tháng.
