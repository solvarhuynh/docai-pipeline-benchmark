# 06. Vì sao preprocessing và robustness testing không phải cùng một việc?

Hai khái niệm đều nói về tài liệu xấu, nhưng mục đích trái ngược nhau:

```text
Document/Image Preprocessing → cố làm input TỐT HƠN cho product
Robustness Testing           → cố làm input XẤU HƠN để Research đo sức chịu đựng
```

## Document/Image Preprocessing nằm ở đâu?

Người dùng có thể chụp hóa đơn hơi nghiêng, tối, mờ hoặc chụp xiên. Product có thể kiểm tra chất lượng rồi chỉnh tài liệu trước khi đưa vào Track A/B:

```text
Ảnh/PDF thật
  ↓ Quality Check
  ↓ Document/Image Preprocessing nếu cần
  ↓ Track A hoặc Track B
  ↓ UnifiedDocumentOutput
```

Các kỹ thuật có thể được cân nhắc, nhưng chưa phải danh sách bắt buộc:

- **Deskew:** xoay trang bị nghiêng về gần thẳng, giống như đặt lại tờ giấy trên bàn.
- **Crop:** cắt phần ngoài tài liệu hoặc vùng không cần thiết.
- **Perspective Correction:** kéo bốn góc ảnh chụp xiên về hình chữ nhật nhìn thẳng.
- **Contrast/Brightness normalization:** cân bằng độ tương phản và độ sáng để chữ dễ thấy hơn.
- **Denoise:** giảm các chấm/nhiễu không thuộc nội dung thật.
- **Sharpening:** làm biên chữ rõ hơn khi ảnh hơi nhòe; làm quá mạnh có thể tạo artefact.
- **Resize/normalization:** đưa kích thước hoặc giá trị pixel về giới hạn model yêu cầu.

Các kỹ thuật này có thể dùng chung cho Invoice và Contract, nhưng mức phù hợp có thể khác. Invoice thường gặp ảnh điện thoại, shadow, blur và perspective; Contract thường gặp PDF scan cũ, trang nghiêng, noise và contrast thấp.

Trong repository hiện tại, `src/docai/data/preprocessing.py` chủ yếu hỗ trợ metadata ảnh và chuẩn hóa bounding box cho data/EDA. Đây chưa phải runtime document-preprocessing pipeline. Vì vậy trạng thái layer product là `PLANNED`; chưa tạo folder `src/docai/preprocessing/` và chưa triển khai thuật toán.

**Data Preprocessing** khác phần trên: nó chuẩn bị dataset, annotation, tọa độ và train/test split để code/model dùng được. Data preprocessing không đồng nghĩa với việc chỉnh ảnh người dùng upload lúc inference.

## Robustness Testing làm gì?

Thay vì sửa ảnh xấu, Research cố tình tạo **Artificial Degradation** (suy giảm nhân tạo) trên ảnh sạch để trả lời: “Nếu dữ liệu ngoài đời không đẹp như dataset, hệ thống còn hoạt động tốt không?”

```text
Ảnh sạch
  ↓ blur / rotate / noise / dark / watermark / crop / perspective distortion
  ↓ Track A và Track B
  ↓ so sánh performance degradation
```

**Blur** làm mất độ nét; **noise** thêm các điểm nhiễu; giảm brightness làm ảnh tối; watermark che một phần nội dung; crop bỏ mất vùng tài liệu; perspective distortion làm trang méo như bị chụp lệch. Đây là biến đổi dùng để kiểm thử, không phải mặc định áp dụng cho input product.

Research có thể đo Precision, Recall, F1, latency và evidence trước/sau degradation. Ví dụ `ΔF1 = F1_clean - F1_noisy`. Không được kết luận preprocessing luôn tăng accuracy, vì sharpen/denoise quá mạnh hoặc crop sai có thể làm mất thông tin.

## Hai track có thể phản ứng khác nhau không?

Có thể. Track A có OCR/layout detector nên có thể nhạy với chữ và biên vùng mờ. Track B có thể chịu một số noise tốt hơn hoặc kém hơn tùy VLM. Đây là giả thuyết, không phải kết luận trước benchmark.

Một research question phụ là:

> Preprocessing có cải thiện Track A và Track B giống nhau không?

Về sau có thể so sánh `raw image` với `preprocessed image` cho từng track, đồng thời so sánh `clean` với `degraded` cho robustness. Task hiện tại chỉ bổ sung architecture và tài liệu, chưa chạy experiment.
