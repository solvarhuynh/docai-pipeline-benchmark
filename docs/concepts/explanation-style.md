# Quy ước giải thích kỹ thuật và khái niệm — DocAI

Tài liệu này xác lập quy chuẩn bắt buộc cho toàn bộ các bài viết giải thích kiến trúc, thuật toán và mô hình machine learning trong thư mục `docs/concepts/`.

Mục tiêu cao nhất: giúp một người có nền tảng lập trình cơ bản nhưng chưa từng tiếp xúc với Machine Learning, Computer Vision hay Document AI có thể hiểu bản chất từng kỹ thuật, lý do vì sao sản phẩm Invoice/Contract cần nó và nó đóng góp gì cho cả Product flow lẫn Research Lab.

---

## 1. Nguyên tắc cốt lõi: Kể chuyện theo dòng tư duy, không liệt kê định nghĩa khô khan

Không bắt đầu bài viết bằng một chuỗi định nghĩa từ điển rời rạc kiểu:
- OCR là...
- KIE là...
- VLM là...

Mọi bài viết phải dẫn dắt người đọc theo một chuỗi câu hỏi tự nhiên:

```text
Bức tranh lớn là gì?
        ↓
Khó khăn / Vấn đề thực tế gì xuất hiện?
        ↓
Tại sao cách làm thông thường thất bại?
        ↓
Kỹ thuật mới giải quyết vấn đề bằng cách nào?
        ↓
Ví dụ đời thường cụ thể là gì?
        ↓
Nó nằm ở module nào trong repository DocAI?
        ↓
Ý nghĩa của nó đối với pipeline là gì? ("Vậy thì sao?")
```

Mỗi đoạn văn phải giải quyết thỏa đáng câu hỏi: **"Biết điều này thì giúp ích gì cho việc hiểu và vận hành hệ thống DocAI?"** trước khi chuyển sang nội dung tiếp theo.

---

## 2. Giữ nguyên thuật ngữ tiếng Anh và giải thích ngay bằng ngôn ngữ đời thường

Trong ngành Trí tuệ nhân tạo, các thuật ngữ tiếng Anh đã trở thành chuẩn mực giao tiếp quốc tế. Khi một thuật ngữ xuất hiện lần đầu:
- Bắt buộc giữ nguyên tên tiếng Anh chuẩn (kèm chữ viết tắt nếu có).
- Cung cấp ngay một câu giải thích bằng ngôn ngữ đời thường, ngắn gọn, súc tích.
- Tuyệt đối không dùng một thuật ngữ hàn lâm khác để định nghĩa cho thuật ngữ đang xét.

Cách viết chuẩn mực:
> **OCR (Optical Character Recognition - Nhận dạng ký tự quang học)**, nôm na là công nghệ giúp máy tính "đọc chữ từ ảnh". Nếu con người nhìn một tờ hóa đơn và đọc được dòng "Tổng tiền: 350.000 VND", thì OCR đang cố làm công việc tương tự nhưng bằng thuật toán máy tính.

---

## 3. Luôn sử dụng ví dụ đời thường và phép so sánh trực quan

Ưu tiên liên hệ các cơ chế máy học phức tạp với những tình huống thực tế mà ai cũng từng gặp:
- Đọc hóa đơn khi đi siêu thị.
- Giáo viên chấm bài thi trắc nghiệm hoặc bài luận.
- Nhân viên kiểm toán đối chiếu chứng từ kế toán.
- Bác bảo vệ kiểm tra danh sách khách ra vào tòa nhà.
- Người phân loại thư từ tại bưu điện.

Ví dụ khi giải thích chỉ số **Recall (Độ phủ)**:
- *Không viết*: "Recall = TP / (TP + FN)."
- *Hãy viết*: "Hãy tưởng tượng doanh nghiệp nhận được 100 hóa đơn bị làm giả số tiền. Nếu hệ thống quét qua và chỉ phát hiện được 27 hóa đơn sai, thì Recall chỉ đạt 27%. Điều nguy hiểm ở đây không phải con số toán học, mà là 73 trường hợp gian lận đã lọt lưới kiểm soát và đi thẳng vào hệ thống thanh toán."

Chỉ đưa công thức toán học sau khi người đọc đã thấu suốt ý nghĩa thực tế.

---

## 4. Tiêu đề phải là câu hỏi dẫn dắt người đọc

Thay vì đặt tiêu đề danh từ chung chung, hãy sử dụng các câu hỏi gợi mở tò mò:
- Tránh: `## OCR` -> Ưu tiên: `## OCR là gì và tại sao hệ thống Document AI bắt buộc phải có nó?`
- Tránh: `## LayoutLMv3` -> Ưu tiên: `## Tại sao chỉ đọc được chữ vẫn chưa đủ, và LayoutLMv3 nhìn trang giấy khác OCR ở điểm nào?`
- Tránh: `## Precision và Recall` -> Ưu tiên: `## Precision thấp và Recall thấp: Đâu là rủi ro nghiêm trọng hơn cho doanh nghiệp?`

---

## 5. Luôn neo kỹ thuật trở lại mã nguồn của repository

Tài liệu trong `docs/concepts/` không phải là bách khoa toàn thư lý thuyết chung chung. Sau khi giải thích cơ chế, mỗi phần bắt buộc phải trả lời:
- Kỹ thuật này nằm ở file hoặc module cụ thể nào trong `src/docai/`?
- Ai gọi nó trong luồng chạy của hệ thống?
- Input của nó là gì và Output của nó đổ về đâu?
- Thuộc Track A (Classic) hay Track B (VLM-native)?
- Kết quả của nó ảnh hưởng thế nào đến JSON schema thống nhất (`docai.core.schema`)?
- Chỉ số nào trong `docai.evaluation.metrics` sẽ được dùng để đo lường nó?

---

## 6. Phân định minh bạch trạng thái thực tế của công nghệ trong repository

Tài liệu kỹ thuật phải trung thực tuyệt đối với hiện trạng mã nguồn. Phải phân biệt rõ 5 mức độ:
1. **ĐÃ CHỐT**: Công nghệ hoặc quyết định kiến trúc đã được lựa chọn chính thức (ví dụ: JSON schema Pydantic, Plotly Dash, cấm Power BI).
2. **ĐANG SỬ DỤNG**: Mã nguồn đã được hiện thực hoá hoàn chỉnh và có kiểm thử tự động xác nhận hoạt động; khi gắn nhãn trạng thái cho module cụ thể phải đối chiếu cả implementation và test hiện có.
3. **SCAFFOLD**: Khung module, class, interface, tham số đã được dựng sẵn kèm TODO và ngoại lệ `NotImplementedError`, sẵn sàng tiếp nhận mô hình thật (ví dụ: `LayoutDetector`, `OCRExtractor`, `LayoutLMv3Extractor`, `VLMDocumentParser`, `DocumentExplainer`).
4. **DỰ KIẾN Ở GIAI ĐOẠN X**: Kỹ thuật đã có lộ trình rõ ràng trong `docs/specs/implementation-guide.md` nhưng chưa đến giai đoạn thực hiện (ví dụ: fine-tune LayoutLMv3 ở Giai đoạn 4, kiểm thử độ bền ở Giai đoạn 9).
5. **CHƯA CHỐT CỤ THỂ**: Kỹ thuật nằm trong định hướng nhưng chưa cố định phiên bản hoặc checkpoint cụ thể (ví dụ: mô hình VLM chính xác cho Track B khi mở rộng hợp đồng CUAD).

Tuyệt đối không biến kế hoạch tương lai thành chức năng đã chạy thật.

---

## 7. Quy trình đưa công thức toán học: Trực giác trước, Công thức sau

Nếu cần trình bày công thức toán học, bắt buộc tuân theo thứ tự 6 bước:
1. **Vấn đề đời thường**: Tình huống phát sinh nhu cầu đo đạc.
2. **Ý nghĩa trực giác**: Ý nghĩa thực chất của con số muốn đo.
3. **Ví dụ số học nhỏ**: Tính nhẩm thử trên 2-3 mẫu cụ thể.
4. **Công thức toán học**: Sử dụng định dạng KaTeX rõ ràng.
5. **Giải thích từng ký hiệu**: Từng biến số trong công thức đại diện cho cái gì.
6. **Quay lại hệ thống DocAI**: Con số này được tính ở module nào (`docai.evaluation.metrics`).

---

## 8. Phân biệt rõ các tầng khái niệm kỹ thuật

Không để người đọc nhầm lẫn giữa các cấp độ:
- **Bài toán / Nhiệm vụ (Task / Problem)**: OCR, Layout Detection, Key Information Extraction (KIE).
- **Mô hình / Kiến trúc (Model / Architecture)**: YOLOv8-doc, LayoutLMv3, PaddleOCR-VL, Transformer.
- **Thư viện / Công cụ (Library / Tool)**: PaddleOCR, PyTorch, Ultralytics, OpenCV.
- **Framework hạ tầng và ứng dụng (Infrastructure Framework)**: FastAPI, Modal, Plotly Dash, Docker.
- **Hợp đồng dữ liệu (Data Contract)**: Pydantic models trong `docai.core.schema`.

---

## 9. Giọng văn và Quy chuẩn định dạng

- **Giọng văn**: Đóng vai trò như một người kỹ sư cố vấn giàu kinh nghiệm, giải thích mạch lạc, gần gũi, tôn trọng tư duy logic của người học.
- **Ngôn ngữ**: Sử dụng tiếng Việt chuẩn có dấu UTF-8.
- **Tuyệt đối không dùng emoji hoặc icon**: Không dùng bất kỳ biểu tượng cảm xúc nào để đảm bảo tính trang trọng và độ tin cậy của tài liệu kỹ thuật chuẩn công nghiệp.
- **Liên kết chéo**: Trỏ link markdown trực tiếp đến các file mã nguồn và tài liệu liên quan để người đọc dễ dàng đối chiếu.
