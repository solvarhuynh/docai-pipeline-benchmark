# 02. Track A: Pipeline Đa Chặng Cổ Điển (Classic Multi-stage Pipeline)

Tài liệu này đi sâu vào kiến trúc và nguyên lý hoạt động của Track A — trường phái xử lý tài liệu truyền thống dựa trên sự phối hợp của ba công đoạn độc lập: Phân vùng bố cục (Layout Detection), Nhận dạng chữ (OCR) và Trích xuất thông tin then chốt (Key Information Extraction - KIE) với mô hình đa phương thức LayoutLMv3.

---

## 1. Triết lý "chia để trị" của Track A là gì và tại sao lại tách thành 3 chặng?

Trong kỹ nghệ phần mềm và xử lý dữ liệu, khi đứng trước một bài toán lớn phức tạp, phương pháp tự nhiên nhất là chia nó thành các bài toán con nhỏ hơn mà mỗi bài toán con đều đã có công cụ giải quyết xuất sắc:

```text
[ Ảnh hóa đơn ]
       ↓
[ Chặng 1: Layout Detection (YOLOv8-doc) ] → Khoanh vùng Header, Bảng hàng, Tổng tiền
       ↓
[ Chặng 2: OCR Extraction (PaddleOCR) ]    → Đọc từng chữ kèm tọa độ trong từng vùng
       ↓
[ Chặng 3: KIE (LayoutLMv3 fine-tuned) ]   → Hiểu ngữ nghĩa và gán nhãn thực thể BIO
       ↓
[ Hợp đồng dữ liệu JSON (UnifiedDocumentOutput) ]
```

### Tại sao lại chia như vậy?
1. **Kiểm soát và gỡ lỗi từng bước**: Nếu hệ thống trích xuất sai tên công ty, kỹ sư có thể mở kết quả của Chặng 1 xem vùng header có bị cắt sót không; mở kết quả Chặng 2 xem OCR có đọc đúng ký tự không; hay do Chặng 3 phân loại nhầm nhãn. Mọi mắt xích đều minh bạch.
2. **Tối ưu tài nguyên tính toán (VRAM)**: Từng mô hình chuyên biệt có kích thước nhỏ gọn (YOLOv8 chỉ vài chục MB, PaddleOCR text recognition chỉ khoảng 10-20 MB, LayoutLMv3 base khoảng 125M tham số), có thể chạy tuần tự trên các GPU phổ thông như NVIDIA T4 (16GB VRAM) mà không lo tràn bộ nhớ.
3. **Tận dụng các mô hình chuyên biệt tốt nhất**: Bài toán nhận diện vật thể đã có YOLO tối ưu hàng chục năm; bài toán OCR tiếng Việt đã có bộ nhận diện chuyên sâu; bài toán hiểu cấu trúc bảng biểu đã có Transformer đa phương thức.

---

## 2. Chặng 1: Phân vùng bố cục (Layout Detection) giải quyết việc gì?

### Trực giác đời thường
Trước khi đọc một tờ báo giấy, mắt bạn không đọc ngay từng chữ cái từ trên xuống dưới. Bạn liếc nhìn bố cục trang báo: đâu là tiêu đề bài viết lớn nhất, đâu là bức ảnh minh họa, đâu là các cột chữ nội dung, và đâu là khung quảng cáo. 

> **Layout Detection (Phân vùng bố cục)** là bài toán xác định vị trí và phân loại các khối chức năng trên trang tài liệu thành các hình chữ nhật (bounding boxes) mang nhãn ngữ nghĩa: Tiêu đề (`header`), Bảng danh mục (`table`), Khu vực người bán (`seller_info`), Chữ ký/Con dấu (`signature`), Tổng cộng (`total`).

### Công nghệ sử dụng: YOLOv8-doc / DocLayout-YOLO
Trong dự án này, Chặng 1 áp dụng các mô hình Object Detection hiện đại thuộc họ YOLO đã được huấn luyện sẵn trên tập dữ liệu bố cục tài liệu (Document Layout Analysis):
- **Cơ chế**: Mô hình chia ảnh thành các lưới (grid cells), đồng thời dự đoán tọa độ bounding box $[x_{\text{min}}, y_{\text{min}}, x_{\text{max}}, y_{\text{max}}]$, xác suất chứa vật thể (objectness score), và phân phối xác suất trên các nhãn vùng.
- **Kỹ thuật Non-Maximum Suppression (NMS)**: Khi hóa đơn bị nghiêng hoặc chữ quá dày, mô hình có thể tạo ra nhiều khung bao trùng lặp cho cùng một vùng. Thuật toán NMS tính toán chỉ số giao thoa trên hội (Intersection over Union - IoU) giữa các khung:
  $$\text{IoU}(B_1, B_2) = \frac{\text{Area}(B_1 \cap B_2)}{\text{Area}(B_1 \cup B_2)}$$
  Nếu $\text{IoU}$ vượt qua một ngưỡng quy định (ví dụ 0.45) và cùng một nhãn, khung có độ tin cậy thấp hơn sẽ bị triệt tiêu để giữ lại duy nhất khung tối ưu.

### Vị trí trong codebase và Trạng thái
- **Tập tin**: [`src/docai/pipelines/track_a/layout_detection.py`](file:///d:/2-personal-project/src/docai/pipelines/track_a/layout_detection.py)
- **Class chính**: `LayoutDetector`
- **Trạng thái**: `SCAFFOLD` (Dự kiến hoàn thiện nạp weights và suy luận ở Giai đoạn 3).

---

## 3. Chặng 2: Nhận dạng chữ (OCR) biến pixel thành ký tự có vị trí như thế nào?

### Trực giác đời thường
Sau khi đã biết vùng bảng hàng nằm ở đâu, bạn cần "đọc" nội dung bên trong vùng đó. Nhưng với máy tính, "đọc" là quá trình hai bước: trước hết phải tìm xem chữ nằm ở đâu trên ảnh (Text Detection), sau đó mới dịch các nét vẽ thành chữ Unicode (Text Recognition).

> **OCR (Optical Character Recognition - Nhận dạng ký tự quang học)** trong hệ thống hiện đại là một pipeline hai pha:
> 1. **Text Detector (ví dụ DBNet)**: Tìm đường bao quanh từng từ hoặc dòng chữ (thường trả về đa giác 4 đỉnh).
> 2. **Text Recognizer (ví dụ CRNN / SVTR)**: Cắt mẩu ảnh dòng chữ đó đưa qua mạng nơ-ron để sinh ra chuỗi ký tự tương ứng.

### Chuyển đổi từ đa giác (Polygon) sang Bounding Box chữ nhật
PaddleOCR thường trả về tọa độ đa giác 4 đỉnh cho mỗi dòng chữ nhằm ôm sát dòng chữ bị nghiêng:
$$P = [[x_1, y_1], [x_2, y_2], [x_3, y_3], [x_4, y_4]]$$

Để đưa vào các mô hình hiểu ngôn ngữ như LayoutLMv3, các đa giác này được quy đổi về hình chữ nhật song song trục tọa độ thông qua giá trị cực trị:
$$x_{\text{min}} = \min(x_1, x_2, x_3, x_4), \quad y_{\text{min}} = \min(y_1, y_2, y_3, y_4)$$
$$x_{\text{max}} = \max(x_1, x_2, x_3, x_4), \quad y_{\text{max}} = \max(y_1, y_2, y_3, y_4)$$

Hàm [`convert_polygon_to_box`](file:///d:/2-personal-project/src/docai/pipelines/track_a/ocr_extraction.py#L68-L74) trong repo đảm nhiệm phép chuyển đổi này.

### Ghép nối không gian (Spatial Join) giữa Layout và OCR
Một bước kỹ thuật quan trọng tại Chặng 2 là ghép nhãn layout cho từng token OCR. Nếu tọa độ của từ "Sữa tươi tiệt trùng" nằm trọn bên trong khung bao của vùng `table` do Chặng 1 tìm thấy, token này sẽ được gán nhãn phụ `layout_tag = "table"`. Điều này cung cấp thêm ngữ cảnh cho chặng KIE tiếp theo.

### Vị trí trong codebase và Trạng thái
- **Tập tin**: [`src/docai/pipelines/track_a/ocr_extraction.py`](file:///d:/2-personal-project/src/docai/pipelines/track_a/ocr_extraction.py)
- **Class chính**: `OCRExtractor`
- **Trạng thái**: `SCAFFOLD` (Dự kiến tích hợp PaddleOCR tiếng Việt 'vi' và tiếng Anh 'en' ở Giai đoạn 3).

---

## 4. Chặng 3: Trích xuất thông tin then chốt (KIE) với LayoutLMv3

### KIE là gì và tại sao OCR xong vẫn chưa đủ?
Sau khi OCR chạy xong, bạn có một danh sách gồm hàng trăm từ rời rạc kèm tọa độ:
- Từ "Tổng": box `[100, 800, 150, 820]`
- Từ "tiền": box `[160, 800, 210, 820]`
- Từ "1.500.000": box `[500, 800, 620, 820]`

Nhưng phần mềm kế toán không thể biết con số "1.500.000" kia là Tổng tiền thanh toán hay là Tiền thuế VAT hay Số tài khoản ngân hàng.

> **KIE (Key Information Extraction - Trích xuất thông tin then chốt)** là quá trình phân loại ngữ nghĩa cho các từ trong tài liệu, xác định từ nào thuộc về trường thông tin nghiệp vụ nào (Tên người bán, Ngày lập, Tổng tiền, Tiền thuế).

### Mô hình LayoutLMv3: Transformer Đa phương thức (Multimodal Transformer)
Các mô hình NLP truyền thống (như BERT) chỉ nhận vào văn bản dạng chuỗi 1 chiều ($x_1, x_2, \dots, x_n$). Nhưng trên hóa đơn, mối quan hệ nằm ở **không gian 2 chiều** và **hình ảnh thị giác**. LayoutLMv3 giải quyết bài toán này bằng cách kết hợp 3 luồng thông tin vào chung một kiến trúc Transformer:

```text
1. Text Tokens      → [ "Tổng", "tiền", "1.500.000" ]
2. 2D Bounding Boxes → Chuẩn hoá về thang [0, 1000]
3. Visual Patches   → Các mẩu ảnh cắt nhỏ từ trang hóa đơn
                            ↓
             [ Bộ nhúng đa phương thức (Multimodal Embedding) ]
                            ↓
             [ Các lớp Self-Attention đa đầu (Self-Attention Layers) ]
                            ↓
             [ Dự đoán nhãn BIO cho từng từ (Token Classification) ]
```

### Chi tiết các kỹ thuật cốt lõi trong LayoutLMv3:

#### a. Chuẩn hoá tọa độ về dải [0, 1000]
Không giống như dải $[0, 1]$ của schema chung, họ mô hình LayoutLM (v1, v2, v3) từ Microsoft quy ước chuẩn hoá tọa độ pixel nguyên bản về số nguyên trong khoảng $[0, 1000]$:
$$x_{\text{1000}} = \text{int}\left(\frac{x}{W} \times 1000\right), \quad y_{\text{1000}} = \text{int}\left(\frac{y}{H} \times 1000\right)$$
Sau đó, mỗi tọa độ $x_{\text{min}}, y_{\text{min}}, x_{\text{max}}, y_{\text{max}}$, cùng chiều rộng $w = x_{\text{max}} - x_{\text{min}}$ và chiều cao $h = y_{\text{max}} - y_{\text{min}}$ sẽ được đưa qua bảng tra cứu tọa độ (2D Position Embedding Lookup Table) để biến thành một vector không gian.

#### b. Cơ chế chú ý (Self-Attention) nhìn thấy cả chữ lẫn vị trí
Trong mạng Transformer, cơ chế Self-Attention cho phép từ "1.500.000" tính toán độ tương quan (attention score) với từ "Tổng tiền" không chỉ vì hai từ này đứng gần nhau trong văn bản, mà còn vì tọa độ $y$ của chúng bằng nhau (cùng nằm trên một hàng ngang) và $x$ của "1.500.000" nằm ngay bên phải $x$ của "Tổng tiền".

#### c. Gắn nhãn BIO (BIO Tagging Scheme)
Một thực thể nghiệp vụ thường bao gồm nhiều từ liên tiếp. Ví dụ tên người bán: "Công ty Cổ phần Công nghệ ABC". Nếu chỉ gán nhãn đơn giản là `SELLER`, mô hình sẽ gặp khó khăn khi phân biệt đâu là điểm bắt đầu của một thực thể mới.

Quy ước BIO giải quyết vấn đề này:
- **B (Begin)**: Token đầu tiên mở đầu một thực thể mới (ví dụ `B-SELLER`).
- **I (Inside)**: Các token tiếp theo nằm bên trong thực thể đó (ví dụ `I-SELLER`).
- **O (Outside)**: Các token không thuộc bất kỳ thực thể nghiệp vụ nào cần trích xuất (ví dụ chữ "Kính chào quý khách", "Ghi chú").

Minh họa phân tách BIO cho hóa đơn:

| Token | Tọa độ chuẩn hoá [0-1000] | Nhãn dự đoán | Diễn giải |
| :--- | :--- | :--- | :--- |
| **Công** | `[50, 100, 120, 130]` | `B-SELLER` | Bắt đầu tên người bán |
| **ty** | `[125, 100, 160, 130]` | `I-SELLER` | Thuộc tên người bán |
| **Sữa** | `[165, 100, 220, 130]` | `I-SELLER` | Thuộc tên người bán |
| **Ngày** | `[50, 140, 110, 165]` | `O` | Từ thừa không cần trích |
| **15/08/2026** | `[120, 140, 250, 165]` | `B-DATE` | Ngày hóa đơn |
| **Tổng** | `[50, 800, 120, 830]` | `O` | Từ khóa chỉ dẫn |
| **tiền** | `[125, 800, 180, 830]` | `O` | Từ khóa chỉ dẫn |
| **1.500.000** | `[500, 800, 650, 830]` | `B-TOTAL` | Tổng tiền thanh toán |

#### d. Gom nhóm thực thể (Entity Aggregation)
Sau khi LayoutLMv3 gán nhãn cho từng token, Chặng 3 thực hiện thuật toán quét tuyến tính để ghép các token `B-` và các token `I-` đi liền kề thành một chuỗi văn bản hoàn chỉnh, đồng thời tính hộp giới hạn bao quát (Union Bounding Box) cho toàn bộ thực thể.

### Vị trí trong codebase và Trạng thái
- **Tập tin**: [`src/docai/pipelines/track_a/kie_layoutlmv3.py`](file:///d:/2-personal-project/src/docai/pipelines/track_a/kie_layoutlmv3.py)
- **Class chính**: `LayoutLMv3Extractor`
- **Trạng thái**: `SCAFFOLD` (Dự kiến fine-tune trên tập hóa đơn mcocr2021 và CORD ở Giai đoạn 4).

---

## 5. Hiện tượng "Lỗi dây chuyền" (Error Cascade) — Gót chân Asin của Track A

Dù có cấu trúc chặt chẽ và dễ kiểm soát, nhược điểm lớn nhất của mô hình đa chặng là **hiện tượng lỗi dây chuyền (Error Cascade)**.

### Cơ chế tích tụ sai số
Đầu ra của chặng trước là đầu vào của chặng sau. Bất kỳ sự sai lệch nào ở chặng đầu cũng sẽ khuếch đại lên các chặng sau:

```text
[ Ảnh chụp bị mờ góc dưới ]
           ↓
[ Chặng 1: Layout Detector ] → Cắt sót vùng chân trang (mất số tổng tiền)
           ↓
[ Chặng 2: OCR Extractor ]   → Chỉ nhận diện được các dòng chữ ở trên, không thấy số tiền
           ↓
[ Chặng 3: LayoutLMv3 ]      → Dù mô hình ngôn ngữ thông minh đến đâu cũng không thể gán nhãn cho một từ không tồn tại
           ↓
[ Kết quả: Precision = 0 cho trường Total Amount ]
```

Hoặc trong một trường hợp khác: Chặng 1 cắt đúng, nhưng Chặng 2 OCR nhận diện sai một ký tự: đọc số `8` thành chữ `B`. Khi chuyển sang Chặng 3, LayoutLMv3 nhận được token `"B00.000"` thay vì `"800.000"`, khiến khâu chuẩn hoá số tiền của hệ thống Fraud Engine sau này báo lỗi parse.

### Làm thế nào để benchmark Track A một cách công bằng?
Trong repository này, hệ thống benchmark được thiết kế để đo lường độ chính xác độc lập ở từng mắt xích:
- **Đo Chặng 2 (OCR)**: Sử dụng chỉ số Tỷ lệ lỗi ký tự (Character Error Rate - CER) và Tỷ lệ lỗi từ (Word Error Rate - WER).
- **Đo Chặng 3 (KIE)**: Tính Field-level Precision, Recall, F1 trên các trường dữ liệu bằng module [`src/docai/evaluation/metrics.py`](file:///d:/2-personal-project/src/docai/evaluation/metrics.py).
Điều này giúp xác định chính xác nguyên nhân khi một tài liệu bị trích xuất thất bại là do OCR đọc sai hay do LayoutLMv3 gán nhãn nhầm.
