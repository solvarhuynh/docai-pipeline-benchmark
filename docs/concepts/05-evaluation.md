# 05. Phương Pháp Đánh Giá và Thử Nghiệm Thực Nghiệm (Evaluation & Benchmark Methodology)

Tài liệu này trình bày toàn bộ hệ thống phương pháp luận đo lường khoa học của dự án DocAI Dual-Pipeline Benchmark. Để so sánh công bằng giữa hai trường phái Track A và Track B, hệ thống không chỉ đánh giá độ chính xác của chữ viết, mà còn đo lường độ chính xác ở cấp độ trường nghiệp vụ (Field-level F1), tỷ lệ đồng thuận (Agreement Ratio), độ trễ suy luận (Latency), chi phí điện toán GPU trên Modal, và độ bền bỉ khi gặp tài liệu bị biến dạng (Robustness testing).

---

## 1. Tại sao chỉ đo độ chính xác nhận dạng chữ (OCR) là chưa đủ?

Trong các bài toán xử lý ảnh truyền thống, người ta thường dùng:
- **Tỷ lệ lỗi ký tự (Character Error Rate - CER)**: Phần trăm ký tự bị đọc sai, thiếu hoặc thừa.
- **Tỷ lệ lỗi từ (Word Error Rate - WER)**: Phần trăm từ bị đọc sai.

Tuy nhiên, trong bài toán Document AI thực tế:
- Giả sử một hóa đơn có 200 từ gồm các dòng ghi chú, hướng dẫn thanh toán, lời cảm ơn. OCR đọc đúng 198 từ râu ria đó, nhưng đọc sai đúng 2 từ quan trọng nhất: số tiền tổng cộng `100.000.000` bị đọc thành `100.000`.
- Theo chỉ số CER, độ chính xác của hệ thống đạt hơn 99%. Nhưng về mặt nghiệp vụ kế toán, hệ thống này đã thất bại 100% vì làm thất thoát dữ liệu nghiêm trọng.

Do đó, một hệ thống Document AI bắt buộc phải được đánh giá dựa trên **chỉ số ở cấp độ trường thông tin then chốt (Field-level Metrics)**.

---

## 2. Chỉ số Cấp độ Trường: Precision, Recall và F1-Score

### Trực giác đời thường
Hãy tưởng tượng bạn là người chấm bài thi cho một nhân viên kế toán tập sự:
- Trên tờ hóa đơn có đúng **4 trường thông tin bắt buộc**: Tên công ty, Ngày lập, Tiền thuế và Tổng tiền.
- Nhân viên đó nộp bài với **5 thông tin trích xuất được**: Trong đó 3 thông tin đúng hoàn toàn, 1 thông tin đọc sai số tiền, và 1 thông tin tự bịa thêm (ví dụ ghi nhầm mã số thuế vào tên người bán).

Khi đó:
- **Precision (Độ chuẩn xác - Nói ra câu nào chắc câu đó)**: Trong 5 câu nhân viên nói ra, có bao nhiêu câu đúng? Trả lời: $3 / 5 = 60\%$.
- **Recall (Độ bao phủ - Tìm được bao nhiêu phần trăm những thứ cần tìm)**: Trong 4 trường bắt buộc trên hóa đơn, nhân viên tìm ra được bao nhiêu trường? Trả lời: $3 / 4 = 75\%$.
- **F1-Score (Điểm cân bằng điều hòa)**: Con số trung bình dung hòa giữa việc "nói đúng" và "tìm đủ".

### Khái niệm kỹ thuật: True Positive (TP), False Positive (FP), False Negative (FN)
Trong module [`src/docai/evaluation/metrics.py`](file:///d:/2-personal-project/src/docai/evaluation/metrics.py#L19-L53), một trường dự đoán được coi là **True Positive (TP)** khi và chỉ khi:
1. Tên trường (`name`) khớp với nhãn chuẩn trong ground truth.
2. Giá trị trường (`value`) sau khi chuẩn hoá (bỏ khoảng trắng thừa, đưa về chữ thường) trùng khớp với giá trị ground truth.

Nếu mô hình:
- Trích xuất ra một trường không có trong ground truth hoặc giá trị bị sai: tính là **False Positive (FP)**.
- Bỏ sót một trường có trong ground truth mà không trích xuất được: tính là **False Negative (FN)**.

### Công thức toán học:

$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$

$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

$$\text{F1-score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2 \times \text{TP}}{2 \times \text{TP} + \text{FP} + \text{FN}}$$

### Vị trí trong codebase và Trạng thái
- **Hàm**: `calculate_field_f1` trong [`src/docai/evaluation/metrics.py`](file:///d:/2-personal-project/src/docai/evaluation/metrics.py#L19)
- **Trạng thái**: `ĐANG SỬ DỤNG` (Đã được kiểm thử và bao phủ trong test suite).

---

## 3. Tỷ lệ Đồng thuận giữa hai Pipeline (Field Agreement Ratio)

### Bài toán trong môi trường thực tế không có đáp án mẫu (Unlabeled Data)
Khi triển khai hệ thống AI vào doanh nghiệp, hàng ngày có hàng chục nghìn hóa đơn mới được đẩy lên. Tại thời điểm đó, **không hề có nhãn chuẩn (Ground Truth)** để tính F1-score. 

Làm thế nào để hệ thống biết được một hóa đơn vừa trích xuất xong có đáng tin cậy hay không?

### Trực giác: Nguyên lý "Hội đồng hai chuyên gia độc lập"
Nếu bạn giao một bài toán khó cho hai chuyên gia hoàn toàn độc lập, áp dụng hai phương pháp giải khác nhau:
- Chuyên gia A (Track A) dùng thước kẻ và kính lúp để tính toán từng bước.
- Chuyên gia B (Track B) dùng trực giác thị giác đọc lướt tổng thể.

Nếu cả hai chuyên gia đều đưa ra cùng một đáp số cho trường `total_amount = "1.500.000 VND"`, xác suất kết quả này đúng là cực kỳ cao. Ngược lại, nếu Chuyên gia A nói là 1,5 triệu còn Chuyên gia B nói là 15 triệu, hệ thống sẽ tự động chặn quy trình tự động và gửi hóa đơn đó cho nhân viên con người kiểm tra lại.

### Công thức tính Tỷ lệ Đồng thuận:
Gọi $K_A$ là tập hợp các trường trích xuất bởi Track A, $K_B$ là tập hợp các trường trích xuất bởi Track B, và tập hợp tất cả các trường là $K = K_A \cup K_B$:

$$\text{Agreement Ratio} = \frac{\sum_{k \in K} \mathbb{I}\left(V_A[k] == V_B[k]\right)}{|K|}$$

trong đó $\mathbb{I}(\cdot)$ là hàm chỉ thị (trả về 1 nếu giá trị chuẩn hoá của trường $k$ ở hai track giống nhau, ngược lại trả về 0).

### Vị trí trong codebase và Trạng thái
- **Hàm**: `calculate_field_agreement` trong [`src/docai/evaluation/metrics.py`](file:///d:/2-personal-project/src/docai/evaluation/metrics.py#L55)
- **Trạng thái**: `ĐANG SỬ DỤNG`.

---

## 4. Đo lường Độ trễ Suy luận (Inference Latency)

### Tại sao không thể chỉ nhìn vào giá trị trung bình (Mean)?
Khi đo tốc độ xử lý của hệ thống, giá trị trung bình thường tạo ra ảo tưởng:
- Giả sử hệ thống xử lý 100 trang tài liệu: 99 trang mất 0.2 giây, nhưng 1 trang ảnh bị mờ phân giải 8K khiến mô hình bị nghẽn trong 60 giây.
- Thời gian trung bình: $(99 \times 0.2 + 60) / 100 \approx 0.8$ giây. Con số 0.8s trông có vẻ chấp nhận được.
- Nhưng đối với khách hàng thực tế gặp phải trang tài liệu thứ 100, trình duyệt web của họ đã bị treo (timeout) và giao dịch bị hủy.

### Các phân vị đo lường bắt buộc:
Module [`compute_latency_stats`](file:///d:/2-personal-project/src/docai/evaluation/metrics.py#L73) sử dụng các chỉ số phân vị từ [`src/docai/data/statistics.py`](file:///d:/2-personal-project/src/docai/data/statistics.py):
- **Median (Phân vị thứ 50 - P50)**: Thời gian xử lý của một tài liệu điển hình ở mức bình thường.
- **P90 / P95**: Thời gian xử lý của 5% đến 10% các tài liệu phức tạp nhất. Đây là chỉ số then chốt để cam kết chất lượng dịch vụ (Service Level Agreement - SLA) trong kỹ nghệ phần mềm.
- **Standard Deviation (Độ lệch chuẩn)**: Đo lường tính ổn định của pipeline.

---

## 5. Phân tích Chi phí Điện toán GPU trên Modal vs Commercial API

Một bài báo khoa học chỉ quan tâm đến F1-score, nhưng một dự án kỹ thuật thực tế phải trả lời câu hỏi: **"Mỗi trang tài liệu xử lý tốn bao nhiêu tiền điện toán?"**.

### Cơ chế tính giá theo giây của Modal Serverless GPU
Trên nền tảng [Modal](https://modal.com), máy chủ GPU được khởi chạy theo nhu cầu (serverless) và tính tiền chính xác tới từng giây thực thi (per-second billing):

| Loại GPU | VRAM | Đơn giá ước tính | Phù hợp với |
| :--- | :--- | :--- | :--- |
| **NVIDIA T4** | 16 GB | $\approx \$0.59$ / giờ ($\approx \$0.00016$ / giây) | Track A (YOLOv8 + PaddleOCR + LayoutLMv3) |
| **NVIDIA A10G** | 24 GB | $\approx \$1.10$ / giờ ($\approx \$0.00030$ / giây) | Track B (PaddleOCR-VL / dots.ocr inference) |
| **NVIDIA A100 (40GB)** | 40 GB | $\approx \$3.67$ / giờ ($\approx \$0.00102$ / giây) | Fine-tuning LayoutLMv3 trên batch size lớn |

### So sánh với API thương mại (Commercial APIs)
Các dịch vụ đám mây như Google Cloud Document AI, AWS Textract hay Azure Form Recognizer thường tính phí cố định theo trang:
- Đơn giá trung bình của API thương mại: Dao động từ $\$0.015$ đến $\$0.05$ cho mỗi trang tài liệu được phân tích.

### Phân tích Điểm hòa vốn (Break-even Analysis):
- **Ở quy mô nhỏ (Dưới 1.000 trang/tháng)**: Sử dụng API thương mại tiết kiệm chi phí hơn vì không phải chịu chi phí thời gian khởi động lạnh của GPU (Cold start overhead) và chi phí duy trì hạ tầng.
- **Ở quy mô lớn (Hàng trăm nghìn trang/tháng)**: Việc tự triển khai pipeline mã nguồn mở (Track A hoặc Track B) trên Serverless GPU như Modal giúp giảm chi phí từ $5\times$ đến $10\times$ so với gọi API trả tiền theo trang, đồng thời đảm bảo bảo mật dữ liệu tài chính nội bộ.

---

## 6. Bộ Thử nghiệm Tính Bền Bỉ Trước Biến Dạng (Robustness Test Suite)

Trong điều kiện phòng thí nghiệm lý tưởng, ảnh tài liệu quét từ máy scan phẳng (flatbed scanner) luôn có độ tương phản cao, góc xoay $0^\circ$ hoàn hảo. 

Nhưng trong đời thực, người dùng chụp ảnh hóa đơn ở quán ăn:
- Bàn ăn thiếu sáng, bóng tay người chụp che khuất một góc.
- Hóa đơn bị vò nhàu trong túi quần, gập nếp ngang thân.
- Ống kính điện thoại bị rung hoặc nhòe mờ (blur).
- Ảnh bị chụp nghiêng một góc $15^\circ - 30^\circ$.

> **Robustness Testing (Thử nghiệm tính bền bỉ)** là quá trình cố tình áp dụng các phép biến dạng nhân tạo (artificial perturbations) lên tập dữ liệu chuẩn để kiểm tra xem độ chính xác của hai pipeline suy giảm như thế nào trước các điều kiện khắc nghiệt của đời thực.

```text
[ Ảnh gốc chuẩn (Clean image) ]
              ↓
  ┌─────────────────────────────────────────────────────────────┐
  │ Bộ biến dạng nhân tạo (Perturbation Suite)                  │
  │ 1. Xoay góc (Rotation): 5°, 15°, 45°                        │
  │ 2. Làm mờ ống kính (Gaussian Blur): kernel 3, 5             │
  │ 3. Nhiễu hạt (Gaussian Noise / Salt-and-Pepper)             │
  │ 4. Giảm tương phản và thiếu sáng (Contrast & Brightness)    │
  └──────────────────────────────┬──────────────────────────────┘
                                 ↓
                     [ Ảnh bị làm giảm chất lượng ]
                                 ↓
       ┌─────────────────────────┴─────────────────────────┐
       ↓                                                   ↓
   [ Track A ]                                         [ Track B ]
       ↓                                                   ↓
   F1-score degraded                                   F1-score degraded
       ↓                                                   ↓
       └─────────────────────────┬─────────────────────────┘
                                 ↓
             [ Độ suy giảm hiệu năng ΔF1 = F1_clean - F1_degraded ]
```

### Chỉ số suy giảm hiệu năng:
$$\Delta \text{F1} = \text{F1}_{\text{clean}} - \text{F1}_{\text{degraded}}$$

Pipeline nào có $\Delta \text{F1}$ nhỏ hơn khi chịu cùng một mức độ nhiễu là pipeline có **tính bền bỉ trong thực tế (Real-world Robustness)** cao hơn.

### Vị trí trong kế hoạch dự án:
- Kế hoạch triển khai: Thuộc Giai đoạn 9 (Benchmark tổng hợp).
- Mô phỏng thực thi qua: [`src/docai/evaluation/benchmark.py`](file:///d:/2-personal-project/src/docai/evaluation/benchmark.py) (Trạng thái: `SCAFFOLD`).

