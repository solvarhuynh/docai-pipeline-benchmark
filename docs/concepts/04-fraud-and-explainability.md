# 04. Phát Hiện Gian Lận và Giải Thích Mô Hình (Fraud Detection & Explainability)

Tài liệu này giải thích hai hệ thống bảo vệ và minh bạch hóa quan trọng nhất của dự án: Động cơ phát hiện gian lận dựa trên luật nghiệp vụ (Fraud & Risk Engine) và Tầng giải thích trực quan bằng bản đồ nhiệt (Explainability Layer). Cả hai thành phần này đảm bảo hệ thống không phải là một "chiếc hộp đen" đưa ra kết luận thiếu căn cứ trong nghiệp vụ kế toán và thẩm định pháp lý.

---

## 1. Tại sao AI trích xuất thôi là chưa đủ trong môi trường sản xuất?

Trong môi trường học thuật, một mô hình đạt độ chính xác 95% có thể được coi là xuất sắc. Nhưng trong hệ thống tài chính thực tế của doanh nghiệp:
- 5% sai sót còn lại có thể là một giao dịch chuyển tiền nhầm 500 triệu đồng.
- Một hóa đơn bị cố tình chỉnh sửa số tiền bằng phần mềm đồ họa (Photoshop) có thể qua mặt OCR nếu chỉ dựa vào văn bản đọc được.
- Một hợp đồng thương mại bị đối tác cố tình bỏ bớt điều khoản tài phán trọng tài có thể gây thiệt hại hàng triệu đô la nếu không được phát hiện kịp thời.

Mô hình Deep Learning (cả Track A lẫn Track B) về bản chất là **mô hình ước lượng xác suất (probabilistic models)**. Chúng không bao giờ có thể đưa ra cam kết chắc chắn 100%. Vì vậy, hệ thống sản xuất cần một lớp bảo vệ thứ hai mang tính **quyết định tuyệt đối (deterministic logic)**:

```text
[ Ảnh tài liệu ]
       ↓
[ AI Pipelines (Track A / Track B) ] → Ước lượng xác suất các trường dữ liệu
       ↓
[ Hợp đồng dữ liệu JSON ]
       ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. Fraud & Risk Engine: Kiểm tra logic và tính toàn vẹn     │
│ 2. Explainability Layer: Vẽ bản đồ nhiệt minh chứng vị trí  │
└─────────────────────────────────────────────────────────────┘
       ↓
[ Quyết định nghiệp vụ an toàn (Tự động duyệt / Chuyển nhân viên soát xét) ]
```

---

## 2. Phân biệt Dự đoán của Mô hình (Model Prediction) và Động cơ Luật (Rule Engine)

Hai khái niệm này thường bị nhầm lẫn, nhưng chúng đóng hai vai trò hoàn toàn khác nhau trong hệ thống:

| Đặc điểm | Dự đoán của Mô hình (Model Prediction) | Động cơ Luật Nghiệp vụ (Rule Engine) |
| :--- | :--- | :--- |
| **Bản chất** | Học máy thống kê (Statistical / Neural Network) | Logic điều kiện nếu - thì (If - Else / Heuristics) |
| **Tính chất** | Xác suất (Probabilistic): có độ tin cậy $0.0 \le p \le 1.0$ | Tất định (Deterministic): đúng là đúng, sai là sai |
| **Mục đích** | "Đọc xem chữ trên ảnh viết nội dung gì" | "Kiểm tra xem con số đọc được có hợp lý về mặt kế toán/pháp lý không" |
| **Cách xử lý ngoại lệ** | Suy diễn gần đúng dựa trên trọng số đã học | Bật cờ cảnh báo rủi ro (`RiskFlag`) với mức độ nghiêm trọng cụ thể |

---

## 3. Động cơ Phát hiện Gian lận và Cảnh báo Rủi ro (Fraud & Risk Engine)

Động cơ luật trong repository được thiết kế chuyên biệt cho hai bài toán nghiệp vụ cốt lõi: Hóa đơn và Hợp đồng pháp lý.

### 3.1. Nghiệp vụ Hóa đơn: Kiểm tra đối chiếu số học (Invoice Arithmetic Check)
Một hóa đơn tài chính hợp lệ bắt buộc phải thỏa mãn phương trình kế toán cơ bản:
$$\text{Tiền hàng trước thuế (Subtotal)} + \text{Tiền thuế GTGT (Tax)} = \text{Tổng tiền thanh toán (Total)}$$

Tuy nhiên, trong thực tế quét tài liệu:
- Do làm tròn số thập phân của tỷ lệ thuế (ví dụ 8% hay 10%), tổng số tiền có thể lệch một lượng rất nhỏ.
- Engine trang bị tham số dung sai `arithmetic_tolerance` (ví dụ $\pm 1000$ VND hoặc $\pm 0.01$ USD) để không bắt lỗi sai số làm tròn hợp lệ.

Nếu độ lệch vượt quá dung sai:
$$|\text{val}_{\text{subtotal}} + \text{val}_{\text{tax}} - \text{val}_{\text{total}}| > \text{tolerance}$$
Hệ thống sẽ lập tức gắn cờ vi phạm `RULE_INVOICE_ARITHMETIC_MISMATCH` với mức độ nghiêm trọng tối cao `CRITICAL`.

### 3.2. Nghiệp vụ Hóa đơn: Bất thường độ tin cậy OCR (OCR Confidence Anomaly)
Kẻ gian khi làm giả hóa đơn thường tẩy xóa con số gốc (ví dụ số `1.000.000`) và in đè hoặc dán con số mới (ví dụ số `8.000.000`). 

Khi đi qua chặng OCR:
- Vùng chữ in nguyên bản của hóa đơn có chất lượng nét mực tự nhiên, đồng đều với nền giấy nên mô hình OCR trả về độ tin cậy rất cao (ví dụ $0.95 - 0.99$).
- Vùng bị dán đè hoặc tẩy xóa có các vết răng cưa quang học, độ tương phản bất thường, khiến mô hình OCR phân vân và trả về độ tin cậy sụt giảm đột ngột (ví dụ $0.35 - 0.45$).

Rule `check_ocr_confidence_anomalies` quét toàn bộ các trường liên quan đến tiền bạc (`amount`, `total`). Nếu độ tin cậy rơi xuống dưới ngưỡng an toàn (mặc định $0.50$), hệ thống sẽ phát tín hiệu cảnh báo nghi vấn chỉnh sửa số liệu `RULE_OCR_CONFIDENCE_ANOMALY`.

### 3.3. Nghiệp vụ Hợp đồng: Cảnh báo thiếu điều khoản theo Taxonomy CUAD
Hợp đồng pháp lý trong bộ dữ liệu CUAD được phân loại theo danh mục chuẩn gồm 41 loại điều khoản (CUAD 41 Clauses Taxonomy).

Trong giao kết hợp đồng kinh tế, có những điều khoản mang tính sống còn để bảo vệ doanh nghiệp:
- **Luật điều chỉnh (Governing Law)**: Hợp đồng áp dụng luật pháp của quốc gia nào khi có tranh chấp?
- **Chấm dứt hợp đồng (Termination Clause)**: Các bên được quyền đơn phương chấm dứt khi nào và thủ tục báo trước ra sao?
- **Giải quyết tranh chấp (Dispute Resolution)**: Giải quyết bằng hòa giải thương lượng hay đưa ra Trung tâm Trọng tài Quốc tế (VIAC)?

Phương thức `check_contract_clauses` đối chiếu danh sách các trường trích xuất được với danh mục điều khoản bắt buộc. Nếu thiếu bất kỳ điều khoản nào, hệ thống phát sinh cờ cảnh báo `RULE_CONTRACT_MISSING_*` mức độ `HIGH`.

### Vị trí trong codebase và Trạng thái
- **Tập tin**: [`src/docai/fraud/rules.py`](file:///d:/2-personal-project/src/docai/fraud/rules.py)
- **Class chính**: `FraudRiskEngine`
- **Trạng thái**: `ĐANG SỬ DỤNG` (Toàn bộ logic đối chiếu số học, quét confidence và kiểm tra điều khoản đã được triển khai hoàn chỉnh và kiểm thử thành công bằng test suite tại [`tests/test_core.py`](file:///d:/2-personal-project/tests/test_core.py)).

---

## 4. Tầng Giải thích Mô hình (Explainability Layer) — Xóa bỏ "Hộp Đen"

### Trực giác đời thường
Hãy tưởng tượng một kiểm toán viên nội bộ đang rà soát hồ sơ thanh toán. Hệ thống AI hiển thị trên màn hình: *"Tổng tiền thanh toán: 89.000.000 VND"*. 

Kiểm toán viên không thể chỉ nhìn vào dòng chữ đó và nhấn nút "Phê duyệt chuyển tiền". Họ có quyền đặt câu hỏi chất vấn hệ thống: *"Bạn dựa vào đâu trên tờ giấy này để đọc ra con số 89 triệu đó? Hãy chỉ cho tôi xem!"*.

> **Tầng giải thích mô hình (Explainability Layer)** là thành phần trực quan hóa vùng chú ý của mạng nơ-ron, tạo ra một bức ảnh có phủ bản đồ nhiệt màu (heatmap) làm bằng chứng cho thấy mô hình đã "nhìn" vào chính xác góc nào trên trang giấy để đưa ra kết quả đó.

---

## 5. Cơ chế giải thích hoạt động như thế nào cho từng Track?

Do hai track có kiến trúc khác nhau, kỹ thuật giải thích cũng được tùy biến tương ứng:

```text
               ┌─────────────────────────────────────────────────────────────┐
               │                     Tài liệu đầu vào                        │
               └──────────────┬───────────────────────────────┬──────────────┘
                              │                               │
                      [ Track A: LayoutLMv3 ]          [ Track B: VLM ]
                              ↓                               ↓
           ┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐
           │ Trích Attention Weights giữa tokens │  │ Grad-CAM / Visual Grounding         │
           │ Ánh xạ trọng số về 2D Bounding Box  │  │ Tính đạo hàm theo feature map ảnh   │
           └──────────────────┬──────────────────┘  └──────────────────┬──────────────────┘
                              │                               │
                              └───────────────┬───────────────┘
                                              ↓
                              [ Bản đồ nhiệt 2D (Heatmap) ]
                                              ↓
                      [ Áp bảng màu JET (Xanh dương → Đỏ rực) ]
                                              ↓
                      [ Trộn bán trong suốt lên ảnh gốc (alpha = 0.5) ]
```

### 5.1. Cơ chế cho Track A (LayoutLMv3 Attention Map)
Trong các lớp Transformer cuối cùng của LayoutLMv3, các ma trận chú ý đa đầu (Multi-Head Attention Matrices) lưu trữ điểm tương quan giữa từng cặp token.

Khi giải thích cho trường `total_amount`:
1. Thuật toán trích xuất các trọng số attention mà token `1.500.000` hướng về các token ngữ cảnh xung quanh (ví dụ từ `Tổng`, `cộng`, `thanh`, `toán`).
2. Tọa độ bounding box $[x_{\text{min}}, y_{\text{min}}, x_{\text{max}}, y_{\text{max}}]$ của các token có trọng số chú ý cao nhất được lấy ra.
3. Trên một ma trận 2D có kích thước bằng ảnh gốc, hệ thống gán các giá trị cường độ nhiệt cao tương ứng tại tọa độ các khung bao này và làm mịn bằng bộ lọc Gauss (Gaussian Blur).

### 5.2. Cơ chế cho Track B (VLM Grad-CAM / Visual Grounding)
Đối với VLM, mô hình không xử lý bằng từng bounding box rời rạc mà xử lý qua bản đồ đặc trưng thị giác (Visual Feature Maps).

Kỹ thuật **Grad-CAM (Gradient-weighted Class Activation Mapping)** được áp dụng:
1. Tính toán đạo hàm (gradient) của logit dự đoán cho token mục tiêu đối với bản đồ đặc trưng ở lớp tích chập hoặc transformer layer cuối cùng của Vision Encoder:
   $$\alpha_k = \frac{1}{Z} \sum_{i} \sum_{j} \frac{\partial y^c}{\partial A_{i,j}^k}$$
2. Tính tổ hợp tuyến tính có trọng số của các bản đồ đặc trưng, sau đó áp hàm ReLU để chỉ giữ lại những vùng ảnh có tác động tích cực đến việc sinh ra từ đó:
   $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_k \alpha_k A^k\right)$$

### 5.3. Kỹ thuật phủ màu JET và Trộn ảnh bán trong suốt (OpenCV Colormap JET)
Bản đồ nhiệt thô ban đầu chỉ là một ma trận số thực trong khoảng $[0.0, 1.0]$. Để mắt người có thể quan sát trực quan:

1. **Chuẩn hoá và áp bảng màu (Colormap)**:
   Hệ thống ánh xạ dải giá trị $[0, 255]$ sang bảng màu **JET** của thư viện OpenCV:
   - Giá trị $0.0$ (không chú ý): Màu xanh dương đậm (lạnh).
   - Giá trị $0.5$ (chú ý trung bình): Màu xanh lá / vàng.
   - Giá trị $1.0$ (vùng tập trung chú ý cao nhất): Màu đỏ rực rỡ (nóng).
2. **Trộn ảnh bán trong suốt (Alpha Blending)**:
   Để kiểm toán viên vừa thấy được màu nhiệt, vừa đọc được nét chữ gốc bên dưới, hai bức ảnh được trộn theo công thức:
   $$I_{\text{overlay}} = \alpha \cdot I_{\text{heatmap}} + (1 - \alpha) \cdot I_{\text{original}}$$
   Với hệ số $\alpha = 0.5$, bức ảnh kết quả cho thấy một quầng sáng đỏ rực bao quanh đúng vị trí dòng tổng tiền trên trang giấy.

### Vị trí trong codebase và Trạng thái
- **Tập tin**: [`src/docai/explainability/explainer.py`](file:///d:/2-personal-project/src/docai/explainability/explainer.py)
- **Class chính**: `DocumentExplainer`
- **Trạng thái**: `SCAFFOLD` (Dự kiến hoàn thiện trích xuất attention weights và Grad-CAM ở Giai đoạn 8).

