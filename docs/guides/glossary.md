# Bảng thuật ngữ kỹ thuật (Glossary) — DocAI Dual-Pipeline Benchmark

Tài liệu này tra cứu toàn bộ các thuật ngữ chuyên ngành được sử dụng trong dự án Document AI này. Mỗi thuật ngữ đều có một câu giải thích ngắn gọn, dễ hiểu và chỉ rõ vị trí xuất hiện trong mã nguồn hoặc báo cáo.

---

## Bảng tra cứu thuật ngữ

| Thuật ngữ | Giải thích ngắn gọn | Xuất hiện ở đâu trong dự án |
|---|---|---|
| Layout Detection | Kỹ thuật thị giác máy tính xác định tọa độ và phân loại các khối chức năng trên trang tài liệu (Header, Table, Signature, Paragraph). | `src/docai/pipelines/track_a/layout_detection.py`, Giai đoạn 3 |
| OCR (Optical Character Recognition) | Công nghệ nhận dạng và chuyển đổi hình ảnh chứa chữ viết thành chuỗi ký tự số mà máy tính có thể đọc và xử lý. | `src/docai/pipelines/track_a/ocr_extraction.py`, Giai đoạn 3 |
| KIE (Key Information Extraction) | Quá trình trích xuất và gán nhãn các trường thông tin nghiệp vụ có ý nghĩa (tên người bán, ngày, tổng tiền) từ tập hợp các từ rời rạc của OCR. | `src/docai/pipelines/track_a/kie_layoutlmv3.py`, Giai đoạn 4 |
| VLM-native (Vision-Language Model) | Kiến trúc mô hình học sâu đa phương thức hợp nhất khả năng nhìn ảnh và hiểu văn bản trong một mạng duy nhất, xử lý trực tiếp từ ảnh sang JSON mà không cần qua bước OCR tách rời. | `src/docai/pipelines/track_b/vlm_parser.py`, Giai đoạn 5 |
| LayoutLMv3 | Mô hình ngôn ngữ đa phương thức tiên tiến của Microsoft, kết hợp đồng thời thông tin văn bản, tọa độ vị trí 2D và đặc trưng hình ảnh để hiểu tài liệu. | `src/docai/pipelines/track_a/kie_layoutlmv3.py`, Giai đoạn 4 |
| Attention weights | Các trọng số toán học trong cơ chế Transformer thể hiện mức độ chú ý của mô hình vào một từ hoặc một vùng ảnh khi dự đoán một nhãn thực thể. | `src/docai/explainability/explainer.py`, Giai đoạn 8 |
| Explainability (Khả năng giải thích) | Khả năng giải thích và minh bạch hoá căn cứ mà mô hình AI dựa vào để đưa ra kết quả dự đoán thay vì hoạt động như một hộp đen. | `src/docai/explainability/explainer.py`, `docs/reports/explainability-report.md`, Giai đoạn 8 |
| Grad-CAM (Gradient-weighted Class Activation Mapping) | Kỹ thuật sử dụng đạo hàm (gradient) của điểm số dự đoán truyền ngược về lớp tích chập cuối cùng để tạo bản đồ nhiệt xác định vùng ảnh quan trọng nhất. | `src/docai/explainability/explainer.py`, Giai đoạn 8 |
| Robustness Test (Kiểm thử độ bền) | Quy trình chủ động tạo ra các biến thể ảnh bị nhiễu (xoay lệch, làm mờ, thiếu sáng, chèn watermark) để đo lường mức độ suy giảm độ chính xác của hệ thống. | `docs/reports/robustness-report.md`, Giai đoạn 9 |
| Generalization (Khả năng tổng quát hoá) | Khả năng của một mô hình hoạt động tốt trên các miền dữ liệu mới hoặc loại tài liệu khác biệt hoàn toàn so với dữ liệu đã dùng để huấn luyện (ví dụ từ hóa đơn sang hợp đồng). | `docs/reports/benchmark-results.md`, Giai đoạn 6 |
| Clause-risk flagging (Cảnh báo rủi ro điều khoản) | Luật logic nghiệp vụ tự động phát hiện các hợp đồng thiếu điều khoản chuẩn bắt buộc hoặc có chứa các điều khoản bất lợi có nguy cơ rủi ro cao. | `src/docai/fraud/rules.py`, Giai đoạn 7 |
| F1 field-level | Chỉ số đo lường độ chính xác tính bằng trung bình điều hoà giữa Precision và Recall ở mức độ từng trường nghiệp vụ (trường chỉ đúng khi toàn bộ giá trị được trích xuất chính xác). | `docs/reports/benchmark-results.md`, `src/docai/evaluation/metrics.py`, Giai đoạn 4, 5, 6 |
| Latency (Độ trễ) | Thời gian cần thiết để hệ thống xử lý hoàn tất một trang tài liệu từ lúc nhận ảnh đến khi trả về JSON kết quả, tính bằng giây hoặc mili giây. | `docs/reports/benchmark-results.md`, `src/docai/api/main.py` |
| GPU-giờ (GPU-hours) | Đơn vị đo lường tổng thời gian tài nguyên bộ xử lý đồ họa (GPU) được sử dụng, làm căn cứ tính chi phí thực tế trên hạ tầng đám mây (như Modal). | `modal_app/deploy.py`, `docs/reports/cost-analysis.md`, Giai đoạn 4 |
| JSON schema thống nhất | Khung cấu trúc dữ liệu Pydantic chung quy định mọi pipeline đều phải trả về cùng một định dạng trường, kiểu dữ liệu và tọa độ để phục vụ so sánh khách quan. | `src/docai/core/schema.py`, Giai đoạn 1 |
| Bounding Box | Khung hộp chữ nhật xác định bởi 4 tọa độ [xmin, ymin, xmax, ymax] dùng để khoanh vùng vị trí của chữ hoặc vùng layout trên ảnh tài liệu. | `src/docai/core/schema.py`, `src/docai/pipelines/track_a/layout_detection.py` |
| BIO Tagging | Quy ước đánh nhãn cho bài toán trích xuất thực thể trong đó B là bắt đầu thực thể (Begin), I là bên trong thực thể (Inside) và O là bên ngoài thực thể (Outside). | `src/docai/pipelines/track_a/kie_layoutlmv3.py`, Giai đoạn 4 |
| Spatial Join | Thao tác kết hợp hình học không gian giữa các tọa độ bounding box của OCR và tọa độ các vùng layout để biết từ nào thuộc vùng tiêu đề hoặc vùng bảng. | `src/docai/pipelines/track_a/ocr_extraction.py`, Giai đoạn 3 |
