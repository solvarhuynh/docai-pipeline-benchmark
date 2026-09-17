# Từ điển dữ liệu (Data Dictionary) — DocAI Dual-Pipeline Benchmark

Tài liệu này mô tả chi tiết 4 bộ dữ liệu thực tế dự kiến sử dụng trong dự án, quy định cấu trúc nhãn gốc và phương pháp ánh xạ (mapping) sang JSON schema thống nhất (`src/docai/core/schema.py`).

Ghi chú về trạng thái: Theo đối chiếu với `log/progress-log.md`, dự án hiện ở bước hoàn thành dựng khung (Scaffold). Các số liệu thống kê chi tiết về dung lượng file, phân bố chiều cao/chiều rộng ảnh sẽ được điền đầy đủ khi Giai đoạn 1 (Tải và tiền xử lý dữ liệu thật) được thực thi.

---

## 1. Bảng tổng hợp 4 bộ dữ liệu

| Bộ dữ liệu | Loại tài liệu | Quy mô danh nghĩa | Định dạng nhãn gốc | Vai trò trong dự án | Trạng thái dữ liệu |
|---|---|---|---|---|---|
| mcocr2021 | Hóa đơn / biên lai Việt Nam | Ảnh chụp camera thực tế | JSON/CSV (polygon tọa độ và chữ tiếng Việt) | Nguồn đánh giá chính cho bối cảnh Việt Nam | Đã lên kế hoạch, chờ tải thật ở Giai đoạn 1 |
| CORD | Biên lai bán lẻ quốc tế | 1.000 mẫu (800 train, 100 val, 100 test) | JSON phân cấp (hierarchical labels kèm box) | Đối chiếu benchmark chuẩn quốc tế | Đã lên kế hoạch, chờ tải thật ở Giai đoạn 1 |
| SROIE (ICDAR 2019) | Hóa đơn scan | 626 train, 347 test | Cặp file .txt (box + text) và .json (entities) | Đối chiếu benchmark cho bước OCR và KIE | Đã lên kế hoạch, chờ tải thật ở Giai đoạn 1 |
| CUAD | Hợp đồng pháp lý | 510 hợp đồng, hơn 13.000 điều khoản gán nhãn | JSON phong cách SQuAD (text context + span offsets) | Đánh giá khả năng tổng quát hoá sang văn bản dài | Đã lên kế hoạch, chờ tải thật ở Giai đoạn 1 |

---

## 2. Mô tả chi tiết từng bộ dữ liệu

### 2.1. mcocr2021 (Mobile Captured OCR 2021)

- **Nguồn gốc**: Cuộc thi RIVF 2021 dành cho bài toán OCR và bóc tách thông tin biên lai tiếng Việt.
- **Loại tài liệu**: Hóa đơn bán lẻ, phiếu thanh toán, hóa đơn ăn uống tại Việt Nam chụp bằng điện thoại di động.
- **Đặc điểm chất lượng**:
  - Ảnh chụp camera thực tế có nhiều góc nghiêng, nếp gấp, bị bóng mờ hoặc thiếu sáng.
  - Chứa các ký tự có dấu tiếng Việt phức tạp mà các bộ OCR chuẩn quốc tế thường đọc sai nếu không được tinh chỉnh.
- **Cấu trúc nhãn gốc**:
  - Mỗi ảnh đi kèm danh sách các vùng chữ được xác định bởi polygon 4 điểm: `[[x1, y1], [x2, y2], [x3, y3], [x4, y4]]`.
  - Nhãn văn bản (transcription) tiếng Việt đi kèm.
- **Phương pháp ánh xạ sang Schema thống nhất**:
  - Tọa độ polygon được bao ngoài bằng bounding box hình chữ nhật 2 điểm `[xmin, ymin, xmax, ymax]`.
  - Các thực thể được gán nhãn vào các trường: `seller_name`, `invoice_date`, `total_amount`, `vat_amount`, `line_items`.
- **Số liệu khảo sát thực nghiệm**:
  - Chờ Giai đoạn 1 thực thi: Thống kê số lượng mẫu, độ phân giải ảnh trung bình sẽ được cập nhật vào đây sau khi chạy `notebooks/01-eda.ipynb`.

### 2.2. CORD (Consolidated Receipt One-stop Dataset)

- **Nguồn gốc**: Bộ dữ liệu biên lai chuẩn hoá do NAVER Clova AI công bố dành cho bài toán Document Visual Question Answering và Key Information Extraction.
- **Loại tài liệu**: Biên lai bán lẻ, cửa hàng tiện lợi quốc tế.
- **Cấu trúc nhãn gốc**:
  - Sử dụng cấu trúc cây phân cấp (hierarchical structure) gồm các nhóm lớn: `menu` (danh sách mặt hàng), `sub_total`, `total`, `void_menu`.
  - Trong mỗi nhóm có các trường con: `cnt` (số lượng), `nm` (tên mặt hàng), `price` (đơn giá), `discountprice` (tiền giảm giá).
  - Tọa độ được biểu diễn dưới dạng polygon 4 đỉnh cho từng từ (word-level).
- **Phương pháp ánh xạ sang Schema thống nhất**:
  - Chuyển đổi nhãn phân cấp thành các phần tử trong danh sách `fields` của `UnifiedDocumentOutput`.
  - Nhóm `menu` được ánh xạ thành `line_items`, `total.total_price` được ánh xạ thành `total_amount`.
- **Số liệu khảo sát thực nghiệm**:
  - Chờ Giai đoạn 1 thực thi: Tỷ lệ phân bổ các loại biên lai và thống kê chiều dài/chiều rộng ảnh.

### 2.3. SROIE (Scanned Receipts OCR and Information Extraction — ICDAR 2019)

- **Nguồn gốc**: Cuộc thi ICDAR 2019 Robust Reading Challenge on Scanned Receipts.
- **Loại tài liệu**: Hóa đơn được quét (scan) từ các cửa hàng bán lẻ, hóa đơn tiếp xúc trực tiếp với máy scan phẳng.
- **Cấu trúc nhãn gốc**:
  - Task 1 & 2 (OCR): File `.txt` chứa mỗi dòng là 8 tọa độ `x1,y1,x2,y2,x3,y3,x4,y4` theo sau bởi văn bản nhận dạng.
  - Task 3 (Information Extraction): File `.json` chứa 4 thực thể chính:
    - `company`: Tên công ty hoặc đơn vị bán hàng.
    - `date`: Ngày phát hành hóa đơn.
    - `address`: Địa chỉ đơn vị bán hàng.
    - `total`: Tổng số tiền thanh toán trên hóa đơn.
- **Phương pháp ánh xạ sang Schema thống nhất**:
  - Ánh xạ `company` -> `seller_name`.
  - Ánh xạ `date` -> `invoice_date`.
  - Ánh xạ `total` -> `total_amount`.
  - Ánh xạ `address` -> `seller_address`.
- **Số liệu khảo sát thực nghiệm**:
  - Chờ Giai đoạn 1 thực thi: Thống kê chi tiết số lượng ký tự trung bình mỗi hóa đơn.

### 2.4. CUAD (Contract Understanding Atticus Dataset)

- **Nguồn gốc**: Bộ dữ liệu chuyên sâu về hiểu hợp đồng do Atticus Project công bố, được gán nhãn bởi các luật sư chuyên nghiệp tại Mỹ.
- **Loại tài liệu**: Hợp đồng thương mại, kinh doanh, thỏa thuận bảo mật (NDA), thỏa thuận cấp phép (License Agreement) có độ dài từ vài trang đến hàng chục trang.
- **Cấu trúc nhãn gốc**:
  - Định dạng JSON theo kiểu SQuAD (Stanford Question Answering Dataset):
    - `context`: Đoạn văn bản pháp lý dài của toàn bộ hợp đồng.
    - `qas`: Danh sách 41 câu hỏi tương ứng với 41 loại điều khoản pháp lý (ví dụ: "Governing Law", "Termination for Convenience", "Indemnification", "Non-Compete").
    - `answers`: Chọn đoạn văn bản (text span) chứa câu trả lời kèm vị trí bắt đầu `answer_start` (ký tự thứ bao nhiêu trong văn bản).
- **Phương pháp ánh xạ sang Schema thống nhất**:
  - `document_type` được gán cố định là `DocumentType.CONTRACT`.
  - Mỗi câu trả lời span được chuyển thành một `ExtractedField` với `field_name` là tên loại điều khoản pháp lý, `field_value` là đoạn trích văn bản điều khoản đó.
  - `bounding_box` sẽ được xác định thông qua tọa độ của trang chứa đoạn trích đó khi chuyển PDF hợp đồng thành ảnh.
- **Số liệu khảo sát thực nghiệm**:
  - Chờ Giai đoạn 1 thực thi: Thống kê số trang trung bình mỗi hợp đồng và phân bố 41 loại điều khoản.

---

## 3. Quy định ánh xạ trường dữ liệu (Field Mapping Reference)

Để cả hai pipeline (Track A và Track B) trả về kết quả đồng nhất, các trường gốc của 4 bộ dữ liệu được quy về bộ từ khóa chuẩn sau:

| Trường chuẩn (`field_name`) | mcocr2021 | CORD | SROIE | CUAD | Kiểu dữ liệu |
|---|---|---|---|---|---|
| `seller_name` | SELLER / Tên người bán | nm / store_name | company | parties / contractor | string |
| `invoice_date` | TIMESTAMP / Ngày | date | date | agreement_date / effective_date | string (chuẩn hoá YYYY-MM-DD nếu có) |
| `total_amount` | TOTAL_COST / Tổng tiền | total.total_price | total | không áp dụng | float / string số tiền |
| `vat_amount` | VAT / Thuế | sub_total.tax_price | không có sẵn | không áp dụng | float / string số tiền |
| `line_items` | Danh sách dòng hàng | menu items | không có sẵn | không áp dụng | json / list |
| `governing_law` | Không áp dụng | Không áp dụng | Không áp dụng | Governing Law clause | string đoạn văn |
| `termination_clause` | Không áp dụng | Không áp dụng | Không áp dụng | Termination clause | string đoạn văn |
| `indemnification` | Không áp dụng | Không áp dụng | Không áp dụng | Indemnification clause | string đoạn văn |

---

## 4. Kế hoạch lưu trữ tài nguyên dữ liệu

Toàn bộ dữ liệu thô được tổ chức tại:
- `data/raw/mcocr2021/`
- `data/raw/cord/`
- `data/raw/sroie/`
- `data/raw/cuad/`

Các dữ liệu sau khi qua bước làm sạch, lọc bớt nhiễu và chuẩn hoá tọa độ sẽ được lưu tại:
- `data/processed/`

Tất cả đều được loại khỏi git commit thông qua file `.gitignore` để tránh làm phình dung lượng repository.
