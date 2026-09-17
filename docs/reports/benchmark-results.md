# Báo cáo kết quả Benchmark — DocAI Dual-Pipeline

Ghi chú: Chờ Giai đoạn tương ứng (Giai đoạn 3, Giai đoạn 4, Giai đoạn 5, Giai đoạn 6, Giai đoạn 9).
Nội dung thật sẽ được tổng hợp và điền dần khi từng giai đoạn hoàn thành.

---

## 1. Track A — Layout & OCR Baseline (Chờ Giai đoạn 3)
- Tỷ lệ phát hiện đúng vùng bảng (Table detection accuracy).
- Tỷ lệ đọc đúng ký tự (CER / WER) so với ground truth trên mcocr2021, CORD, SROIE.

## 2. Track A — KIE với LayoutLMv3 Fine-tuned (Chờ Giai đoạn 4)
- F1-score cấp field trên tập test riêng.
- Độ chính xác theo từng trường dữ liệu (seller, date, total, vat, items).

## 3. Track B — VLM-Native Parsing (Chờ Giai đoạn 5)
- F1-score cấp field với PaddleOCR-VL / dots.ocr trên cùng tập test.
- Độ trễ (latency) trung bình trên mỗi trang tài liệu.

## 4. So sánh trực tiếp trên Hóa đơn (Track A vs Track B) (Chờ Giai đoạn 5)
- Bảng đối chiếu F1, Latency, độ phức tạp hệ thống.

## 5. Đánh giá tổng quát hoá trên Hợp đồng CUAD (Chờ Giai đoạn 6)
- Tỷ lệ suy giảm hiệu năng khi chuyển từ hóa đơn sang hợp đồng dài.
- Nhận định về khả năng tổng quát hoá của từng kiến trúc.

## 6. Tổng hợp Benchmark cuối cùng (Chờ Giai đoạn 9)
- Bảng so sánh tổng hợp tất cả chỉ số đánh giá trên cả 4 bộ dữ liệu.

## 7. Định hướng mở rộng
- Ghi nhận các ý tưởng nghiên cứu và cải tiến ngoài 10 giai đoạn.
