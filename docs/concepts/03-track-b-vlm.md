# 03. Track B: Pipeline VLM-Native Đơn Lượt (Vision-Language Model Single-Pass)

Tài liệu này giải thích chi tiết kiến trúc hiện đại của Track B — trường phái sử dụng Mô hình Thị giác - Ngôn ngữ (Vision-Language Model - VLM) để đọc hiểu và trích xuất tài liệu trong một lượt suy luận duy nhất (single-pass), đối chiếu triết lý với Track A và phân tích các thách thức cốt lõi như hiện tượng ảo giác (hallucination) và chi phí tài nguyên tính toán.

**Trạng thái quyết định:** `CHƯA CHỐT MODEL CỤ THỂ`. PaddleOCR-VL và dots.ocr hiện chỉ là các ứng viên trong kế hoạch; code Track B mới cung cấp interface/prompt scaffold, chưa thực hiện inference.

Track B cũng là processing backend bên trong Product. VLM-native parsing chỉ là một cách triển khai engine; việc so sánh với Track A thuộc Research component, không phải mục tiêu duy nhất của product.

---

## 1. Triết lý của Track B là gì và tại sao lại có xu hướng chuyển sang VLM-native?

Nếu như Track A chia nhỏ bài toán thành 3 chặng nối tiếp (Tìm vùng → Đọc chữ → Gán nhãn), thì Track B chọn một triết lý hoàn toàn đối lập: **hợp nhất tất cả vào một mạng nơ-ron đa phương thức duy nhất**.

```text
[ Ảnh tài liệu (Hóa đơn / Hợp đồng) ] + [ Prompt cấu trúc yêu cầu trích xuất ]
                               ↓
          [ Vision-Language Model (PaddleOCR-VL / dots.ocr) ]
                               ↓
               [ Chuỗi JSON hoàn chỉnh trong 1 lượt ]
                               ↓
              [ Pydantic UnifiedDocumentOutput ]
```

### Trực giác đời thường
Hãy tưởng tượng bạn đưa một bản hợp đồng cho một chuyên viên pháp chế có kinh nghiệm 10 năm. Chuyên viên đó không cần cầm thước kẻ kẻ từng khung chữ nhật quanh từng đoạn văn, cũng không cần ngồi gõ lại toàn bộ văn bản ra file Word rồi mới tìm ngày hết hạn. Họ cầm tập tài liệu, lướt mắt qua các điều khoản, hiểu ngữ cảnh và điền ngay thông tin "Thời hạn thanh toán: 30 ngày kể từ ngày nghiệm thu" vào biểu mẫu báo cáo.

> **VLM-native Document Parsing** là phương pháp tiếp cận xem trang tài liệu như một hình ảnh trực quan kết hợp văn bản tự nhiên, đưa thẳng vào một mô hình thị giác - ngôn ngữ lớn để mô hình tự quan sát, tự đọc và tự sinh ra kết quả JSON có cấu trúc chỉ sau một lần tính toán (single-pass).

---

## 2. Bên trong một Vision-Language Model có những thành phần nào?

Một mô hình VLM (như PaddleOCR-VL hay dots.ocr) không phải là một chiếc hộp đen thần bí. Về mặt kiến trúc, nó được ghép nối từ 3 khối xử lý chính:

```text
                     [ Ảnh tài liệu ]
                            ↓
             ┌─────────────────────────────┐
             │   1. Vision Encoder         │ → Chuyển đổi điểm ảnh thành các vector
             │   (ViT / ConvNeXt)          │   đặc trưng thị giác (Visual Tokens)
             └──────────────┬──────────────┘
                            ↓
             ┌─────────────────────────────┐
             │   2. Projection Adapter     │ → Chiếu vector thị giác vào cùng không gian
             │   (Cross-Attention / MLP)   │   ngữ nghĩa với vector văn bản
             └──────────────┬──────────────┘
                            ↓
[ Prompt văn bản ] ──→ ┌─────────────────────────────┐
                       │   3. Large Language Model   │ → Tiếp nhận cả Visual Tokens và Text Tokens,
                       │   (Autoregressive Decoder)  │   sinh ra từng từ của chuỗi JSON
                       └──────────────┬──────────────┘
                                      ↓
                         { "total_amount": "1.500.000" }
```

### Chi tiết từng thành phần:

1. **Vision Encoder (Bộ mã hóa thị giác)**:
   Thường sử dụng kiến trúc Vision Transformer (ViT). Ảnh tài liệu được chia thành hàng trăm mẩu ảnh nhỏ (patches, ví dụ kích thước $14 \times 14$ pixels). Mỗi patch được biến thành một vector đặc trưng biểu diễn độ tương phản, nét chữ, khoảng cách các dòng.
2. **Projection Adapter (Cầu nối phương thức)**:
   Kích thước không gian vector của ảnh (ví dụ 1024 chiều) thường khác với không gian ngữ nghĩa của mô hình ngôn ngữ (ví dụ 4096 chiều). Bộ điều hợp này là một mạng MLP hoặc cơ chế Cross-Attention giúp "dịch" các vector thị giác sang định dạng mà mô hình ngôn ngữ có thể "đọc" được như thể chúng là những từ vựng đặc biệt.
3. **Autoregressive Language Decoder (Bộ giải mã ngôn ngữ tự hồi quy)**:
   Mô hình ngôn ngữ nhận chuỗi visual tokens kết hợp với câu lệnh prompt, sau đó tự sinh ra chuỗi ký tự đầu ra từng token một dựa trên xác suất có điều kiện:
   $$P(w_t \mid w_{<t}, \text{Image}, \text{Prompt})$$

---

## 3. Làm thế nào để ép VLM trả về đúng cấu trúc JSON mà không bị lan man?

Mô hình ngôn ngữ tự nhiên vốn được huấn luyện để trò chuyện tự do. Nếu chỉ yêu cầu đơn giản: *"Hãy trích xuất thông tin hóa đơn này"*, mô hình có thể trả lời một câu lịch sự dài dòng như: *"Chào bạn, hóa đơn này được phát hành bởi công ty A vào ngày B với tổng tiền là C..."*. 

Định dạng này hoàn toàn vô dụng đối với các hệ thống backend tự động.

### Kỹ thuật Structured Prompting (Câu lệnh cấu trúc)
Trong file [`src/docai/pipelines/track_b/vlm_parser.py`](../../src/docai/pipelines/track_b/vlm_parser.py), phương thức `build_prompt` định hình câu lệnh theo nguyên tắc chặt chẽ:

```text
Vai trò hệ thống: Bạn là chuyên gia Document AI.
Mục tiêu: Trích xuất các trường nghiệp vụ từ ảnh tài liệu này thành JSON hợp lệ.
Danh mục trường bắt buộc:
- seller_name: Tên người bán
- invoice_date: Ngày lập hóa đơn
- total_amount: Tổng tiền thanh toán
- tax_amount: Tiền thuế VAT
- line_items: Danh sách các dòng hàng hóa
Yêu cầu định dạng:
Chỉ trả về chuỗi JSON thuần túy, không thêm lời chào, không bao bọc bởi giải thích thừa.
Tuyệt đối không tự suy diễn nếu không tìm thấy dữ liệu trên ảnh (Do not hallucinate).
```

### Xử lý hậu kỳ (Post-processing) và JSON Repair
Ngay cả khi đã hướng dẫn kỹ, VLM vẫn có xác suất sinh ra các lỗi cú pháp nhỏ như:
- Đặt chuỗi JSON trong markdown block ````json ... ````.
- Thiếu dấu đóng ngoặc nhọn `}` ở cuối chuỗi do hết độ dài token cho phép (max tokens).
- Thừa dấu phẩy `,` ở phần tử cuối cùng của mảng.

Đây là quy trình hậu kỳ dự kiến của Track B: bóc tách chuỗi JSON sạch, áp dụng thuật toán vá lỗi JSON (JSON Repair), sau đó đưa qua Pydantic model [`UnifiedDocumentOutput`](../../src/docai/core/schema.py) để kiểm định kiểu dữ liệu. Hiện tại `build_prompt` đã có implementation; `parse` và `parse_raw_json_to_output` vẫn là `SCAFFOLD`, chưa thực hiện inference hoặc JSON repair.

---

## 4. Ảo giác (Hallucination) là gì và tại sao nó là rủi ro lớn nhất của VLM?

Trong khi Track A chịu rủi ro "Lỗi dây chuyền" (Error Cascade), thì điểm yếu chết người của Track B lại nằm ở **Hiện tượng ảo giác (Hallucination)**.

### Trực giác đời thường
Bạn nhờ một người bạn đọc lướt một hợp đồng bằng tiếng nước ngoài. Ở trang thứ 5, chữ bị mờ một vết mực lớn. Thay vì nói: *"Tôi không đọc được chỗ này"*, người bạn đó vì đã từng đọc nhiều hợp đồng mẫu trước đây nên tự động đoán: *"Chắc điều khoản này ghi là phạt 10% nếu vi phạm hợp đồng"*. Người bạn đó đã tự "bịa" ra thông tin dựa trên kinh nghiệm quá khứ chứ không dựa trên sự thật trước mắt.

> **Ảo giác (Hallucination)** trong Document AI là hiện tượng mô hình VLM sinh ra một giá trị trông rất thuyết phục và chuẩn cú pháp, nhưng giá trị đó hoàn toàn không tồn tại trên bức ảnh tài liệu thực tế.

### Ví dụ thực tế:
- Ảnh hóa đơn gốc bị ố vàng, phần tổng tiền chỉ còn thấy mờ mờ số `1.000.???`.
- Thay vì trả về rỗng hoặc độ tin cậy thấp, VLM tự động sinh ra `"total_amount": "1.000.000 VND"` vì trong hàng triệu tài liệu huấn luyện của nó, con số 1 triệu đồng xuất hiện rất phổ biến.
- Trong giao dịch tài chính ngân hàng, một sự tự biên tự diễn như vậy là rủi ro cực kỳ nghiêm trọng.

### Vấn đề thiếu khả năng định vị tọa độ (Grounding Loss)
Track A luôn gắn liền từng từ với một bounding box cụ thể trên ảnh: chữ "Tổng tiền" nằm ở tọa độ nào là rõ ràng. 

Ngược lại, đa số các VLM thế hệ đầu chỉ sinh ra văn bản thuần túy mà không trả về tọa độ pixel của từng trường dữ liệu. Điều này khiến việc kiểm tra chéo (Auditability) của nhân viên kế toán trở nên khó khăn: họ có được con số tổng tiền từ VLM, nhưng không biết con số đó được đọc từ góc nào trên trang giấy.

---

## 5. Bảng so sánh toàn diện giữa Track A và Track B

Để giúp các nhà phát triển đưa ra quyết định kiến trúc đúng đắn, bảng dưới đây tổng kết các tiêu chí đánh giá kỹ thuật giữa hai trường phái:

| Tiêu chí | Track A (Classic Multi-stage) | Track B (VLM-Native Single-pass) |
| :--- | :--- | :--- |
| **Kiến trúc** | Phối hợp 3 mô hình độc lập (YOLOv8 + PaddleOCR + LayoutLMv3) | Một mô hình đa phương thức duy nhất (PaddleOCR-VL / dots.ocr) |
| **Số lượt suy luận (Passes)** | 3 lượt tuần tự (Layout → OCR → KIE) | 1 lượt duy nhất (End-to-End Image-to-JSON) |
| **Yêu cầu phần cứng (VRAM)** | Chưa đo thực nghiệm; phụ thuộc checkpoint và cấu hình | Chưa đo thực nghiệm; phụ thuộc checkpoint và cấu hình |
| **Thời gian suy luận (Latency)** | Chưa có kết quả đo; sẽ đánh giá trong benchmark | Chưa có kết quả đo; sẽ đánh giá trong benchmark |
| **Khả năng giải thích (Explainability)** | Rõ ràng: Bounding box và attention weights gắn trực tiếp với từng token | Phức tạp hơn: Cần dùng Grad-CAM hoặc các kỹ thuật visual grounding chuyên biệt |
| **Rủi ro lớn nhất** | **Lỗi dây chuyền (Error Cascade)**: OCR đọc sai làm hỏng các chặng sau | **Ảo giác (Hallucination)**: Tự bịa thông tin khi ảnh mờ hoặc tài liệu lạ |
| **Khả năng thích ứng (Zero-shot)** | Cần kiểm chứng trên dữ liệu chưa từng train; dự kiến cần dữ liệu có nhãn để fine-tune | Là giả thuyết cần kiểm chứng bằng benchmark; chưa có kết quả thực nghiệm |
| **Vị trí trong repo** | [`src/docai/pipelines/track_a/`](../../src/docai/pipelines/track_a/) | [`src/docai/pipelines/track_b/`](../../src/docai/pipelines/track_b/) |
| **Trạng thái hiện tại** | `SCAFFOLD` (Dự kiến Giai đoạn 3 & 4) | `SCAFFOLD` (Dự kiến Giai đoạn 5 & 6) |

---

## 6. Track B phục vụ Contract Workspace và CUAD research như thế nào?

Hóa đơn có đặc thù là tài liệu bán cấu trúc ngắn (thường 1-2 trang), mật độ thông tin tập trung vào các ô số liệu rõ ràng. 

Ngược lại, hợp đồng pháp lý trong bộ dữ liệu **CUAD (Contract Understanding Atticus Dataset)** là tài liệu văn bản dài dày đặc (thường từ 10 đến 50 trang), chứa ngôn từ pháp lý phức tạp và các điều khoản phụ thuộc lẫn nhau. Đây là input quan trọng cho Contract Workspace; đồng thời tạo điều kiện cho research so sánh khả năng tổng quát hoá.

Trong Giai đoạn 6 của dự án:
- Track A (LayoutLMv3) sẽ gặp rào cản lớn vì độ dài chuỗi tối đa của Transformer cổ điển thường bị giới hạn ở 512 tokens.
- Track B (VLM) sẽ được thử nghiệm khả năng hiểu ngữ cảnh dài không qua huấn luyện chuyên biệt (Zero-shot Generalization). Mục tiêu là đo lường **độ suy giảm F1-score (Generalization Drop)** khi chuyển từ bài toán hóa đơn quen thuộc sang bài toán hợp đồng pháp lý phức tạp.
