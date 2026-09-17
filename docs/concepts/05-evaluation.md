# 05. Phương Pháp Đánh Giá và Thử Nghiệm Thực Nghiệm (Evaluation & Benchmark Methodology)

Đây là tài liệu của Research & Quality layer trong DocAI Document Intelligence Platform. Layer này dùng output chuẩn hoá của Track A và Track B để đo Field-level F1, Agreement Ratio, latency, cost, robustness và explainability. Evaluation không phải bước bắt buộc trong Product flow khi người dùng chỉ xử lý một tài liệu.

Evaluation phải báo cáo riêng theo domain khi có đủ ground truth: Invoice tập trung vào field/number/table extraction; Contract tập trung vào metadata, clause span/category và missing-clause signals. CUAD vì thế phục vụ đồng thời Contract product capability và generalization research.

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
Trong module [`src/docai/evaluation/metrics.py`](../../src/docai/evaluation/metrics.py), một trường dự đoán được coi là **True Positive (TP)** khi và chỉ khi:
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
- **Hàm**: `calculate_field_f1` trong [`src/docai/evaluation/metrics.py`](../../src/docai/evaluation/metrics.py)
- **Trạng thái**: `ĐANG SỬ DỤNG` ở mức implementation; chưa có test riêng cho metrics trong test suite hiện tại và chưa có kết quả benchmark trên dữ liệu thật.

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
- **Hàm**: `calculate_field_agreement` trong [`src/docai/evaluation/metrics.py`](../../src/docai/evaluation/metrics.py)
- **Trạng thái**: `ĐANG SỬ DỤNG` ở mức implementation; chưa có kết quả benchmark trên dữ liệu thật.

---

## 4. Đo lường Độ trễ Suy luận (Inference Latency)

### Tại sao không thể chỉ nhìn vào giá trị trung bình (Mean)?
Khi đo tốc độ xử lý của hệ thống, giá trị trung bình thường tạo ra ảo tưởng:
- Giả sử hệ thống xử lý 100 trang tài liệu: 99 trang mất 0.2 giây, nhưng 1 trang ảnh bị mờ phân giải 8K khiến mô hình bị nghẽn trong 60 giây.
- Thời gian trung bình: $(99 \times 0.2 + 60) / 100 \approx 0.8$ giây. Con số 0.8s trông có vẻ chấp nhận được.
- Nhưng đối với khách hàng thực tế gặp phải trang tài liệu thứ 100, trình duyệt web của họ đã bị treo (timeout) và giao dịch bị hủy.

### Các phân vị đo lường bắt buộc:
Benchmark tương lai cần báo cáo các chỉ số sau. Hiện tại [`compute_latency_stats`](../../src/docai/evaluation/metrics.py) mới sử dụng helper thống kê để cung cấp count, min, max, mean, median và standard deviation; P90/P95 chưa được tính trong code.
- **Median (Phân vị thứ 50 - P50)**: Thời gian xử lý của một tài liệu điển hình ở mức bình thường.
- **P90 / P95**: Thời gian xử lý của 5% đến 10% các tài liệu phức tạp nhất; sẽ bổ sung khi benchmark được triển khai. Đây là chỉ số then chốt để cam kết chất lượng dịch vụ (Service Level Agreement - SLA) trong kỹ nghệ phần mềm.
- **Standard Deviation (Độ lệch chuẩn)**: Đo lường tính ổn định của pipeline.

---

## 5. Chi phí Product và Research sẽ được đo như thế nào?

Một sản phẩm thực tế cần biết mỗi trang Invoice hoặc Contract tốn bao nhiêu tài nguyên. Đây là planned research measurement, chưa phải số liệu đã có.

### Cơ chế tính giá theo giây của Modal Serverless GPU
Trên nền tảng [Modal](https://modal.com), runtime GPU có thể được ghi theo thời gian thực thi. Khi đo, phải ghi model/checkpoint, GPU, warm-up, batch size, số trang, wall-clock time, đơn giá tại thời điểm đo và công thức. Candidate hardware trong các tài liệu cũ không phải lựa chọn đã chốt.

### So sánh với API thương mại (Commercial APIs)
API thương mại chỉ được dùng làm comparison khi có nguồn giá công khai, ngày kiểm tra và workload tương đương. Không dùng một khoảng giá tham khảo để tuyên bố cost advantage.

### Break-even Analysis (PLANNED)

Chỉ tính break-even sau khi có workload, cold start, utilization, storage, retry và đơn giá thực tế. Repository hiện chưa có kết luận engine nào rẻ hơn API thương mại.

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
- Mô phỏng thực thi qua: [`src/docai/evaluation/benchmark.py`](../../src/docai/evaluation/benchmark.py) (Trạng thái: `SCAFFOLD`).
