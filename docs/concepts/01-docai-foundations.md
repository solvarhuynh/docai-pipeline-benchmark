# 01. Nền tảng Document AI và Hợp đồng Dữ liệu Chung

Tài liệu này giải thích bản chất của bài toán Trí tuệ nhân tạo cho tài liệu (Document AI), phân tích các tầng thông tin mà máy tính cần giải mã trên một trang giấy, và lý do vì sao một hệ thống benchmark bắt buộc phải có một hợp đồng dữ liệu chuẩn hoá duy nhất.

---

## 1. Document AI là gì và tại sao tài liệu không chỉ là một bức ảnh thông thường?

Hãy tưởng tượng bạn chụp một bức ảnh phong cảnh bãi biển. Đối với bức ảnh đó, mắt bạn nhìn tổng thể: bầu trời xanh, cát vàng, rặng dừa. Nếu một góc ảnh bị mờ một chút, bạn vẫn hiểu trọn vẹn bức ảnh.

Nhưng một tờ hóa đơn tiền điện hay một bản hợp đồng mua bán nhà đất thì hoàn toàn khác:
- Nó chứa đầy các ký tự chữ cái và con số mang tính pháp lý và tài chính nghiêm ngặt.
- Một con số "0" bị đọc nhầm thành chữ "O", hay số "8" bị mờ thành số "3" có thể biến hóa đơn 10 triệu thành 18 triệu đồng.
- Quan trọng hơn, thông tin trên tài liệu được sắp xếp theo **quy ước không gian**: số tiền nằm cạnh chữ "Tổng cộng", chữ ký nằm ở góc dưới cùng bên phải, tên công ty bán hàng nằm ở phần tiêu đề trên cùng.

> **Document AI (Document Artificial Intelligence - Trí tuệ nhân tạo cho tài liệu)**, hiểu một cách mộc mạc nhất, là công nghệ dạy máy tính không chỉ "nhìn thấy bức ảnh trang giấy", mà phải "đọc, hiểu và trích xuất đúng thông tin nghiệp vụ" giống như một nhân viên kế toán hoặc nhân viên pháp chế đang xử lý hồ sơ.

Một bức ảnh tài liệu khi đưa vào máy tính ban đầu chỉ là một ma trận gồm hàng triệu điểm ảnh (pixels) với các giá trị màu sắc từ 0 đến 255. Bản thân các điểm ảnh này hoàn toàn vô nghĩa đối với máy tính. Để hiểu được tài liệu, máy tính phải bóc tách qua nhiều tầng thông tin liên tiếp.

---

## 2. Máy tính cần giải mã những tầng thông tin nào trên một trang giấy?

Để biến một bức ảnh thô thành dữ liệu có thể đưa vào phần mềm kế toán, hệ thống phải vượt qua một chuỗi 7 tầng thông tin từ thấp lên cao:

```text
[ Tầng 1: Pixel thô ]           → Các chấm màu RGB rời rạc
        ↓
[ Tầng 2: Vùng bố cục (Layout) ] → Nhận diện đâu là Tiêu đề, Bảng hàng, Chữ ký
        ↓
[ Tầng 3: Ký tự chữ viết (OCR) ] → Chuyển các nét vẽ thành chuỗi ký tự "Tổng tiền"
        ↓
[ Tầng 4: Tọa độ chữ (BBox) ]   → Chữ này nằm ở tọa độ pixel nào trên trang
        ↓
[ Tầng 5: Thực thể nghiệp vụ ]   → Con số "1.500.000" chính là giá trị của "total_amount"
        ↓
[ Tầng 6: Quan hệ giữa các mục ] → Dòng sản phẩm này có đơn giá, số lượng và thành tiền tương ứng
        ↓
[ Tầng 7: Hợp đồng dữ liệu ]    → Ép toàn bộ vào cấu trúc JSON chuẩn hoá
```

### Chi tiết từng tầng thông tin:

1. **Tầng Pixel (Điểm ảnh)**:
   Máy tính chỉ thấy các mảng số thể hiện độ sáng tối. Ở bước này, kỹ thuật **tiền xử lý ảnh (Image Preprocessing)** được sử dụng để xoay ảnh ngay ngắn, khử nhiễu, cân bằng độ sáng. Trong repository, các hàm kiểm tra kích thước và tính hợp lệ được đặt tại [`src/docai/data/preprocessing.py`](../../src/docai/data/preprocessing.py).
2. **Tầng Vùng bố cục (Layout Regions)**:
   Mắt người khi nhìn vào hóa đơn sẽ tự động phân tách: "Đây là phần đầu hóa đơn chứa logo, đây là bảng danh sách món ăn, đây là phần chân trang có chữ ký". Máy tính cũng cần làm điều này thông qua kỹ thuật **Layout Detection (Phân vùng bố cục)**.
3. **Tầng Nhận dạng chữ viết (OCR - Optical Character Recognition)**:
   Biến hình vẽ các nét chữ thành các ký tự số học mà máy tính lưu trữ được (mã Unicode).
4. **Tầng Tọa độ không gian (Bounding Box)**:
   Không chỉ biết trang giấy có chữ "Tổng tiền", máy tính phải biết chính xác chữ "Tổng tiền" nằm ở đâu trên trang giấy. Vị trí này được biểu diễn bằng một hình chữ nhật bao quanh chữ.
5. **Tầng Thực thể thông tin then chốt (KIE - Key Information Extraction)**:
   Biết chữ "350.000" nằm trên hóa đơn là chưa đủ. Máy phải hiểu "350.000" ở đây đóng vai trò là "Tổng tiền thanh toán" chứ không phải "Tiền thuế" hay "Số chứng minh nhân dân".
6. **Tầng Quan hệ ngữ nghĩa (Semantic Relations)**:
   Liên kết cặp chìa khóa - giá trị (Key - Value pairs), ví dụ liên kết nhãn "Ngày lập:" với giá trị "15/08/2026", hoặc gom các cột trong một dòng của bảng hóa đơn thành một món hàng hoàn chỉnh.
7. **Tầng Cấu trúc chuẩn hoá (Structured JSON Output)**:
   Đóng gói toàn bộ các thông tin trên thành một đối tượng dữ liệu duy nhất mà hệ thống ngân hàng hay phần mềm ERP của doanh nghiệp có thể đọc được ngay mà không cần xử lý thêm.

---

## 3. Bounding Box là gì và tại sao cần chuẩn hoá tọa độ?

Khi bạn muốn chỉ cho bạn của mình một món đồ trên bàn ăn, bạn sẽ nói: "Món cá nướng nằm ở phía trên bên trái". Trong thị giác máy tính, máy tính không dùng lời nói mà dùng tọa độ hình học.

> **Bounding Box (Hộp giới hạn)**, viết tắt là **bbox**, là một khung hình chữ nhật nhỏ nhất bao bọc xung quanh một từ, một dòng chữ hoặc một vùng layout trên ảnh.

Một hộp giới hạn thường được xác định bởi 4 con số:
`[xmin, ymin, xmax, ymax]`
- `xmin`: Khoảng cách từ mép trái ảnh đến cạnh trái của hộp.
- `ymin`: Khoảng cách từ mép trên ảnh đến cạnh trên của hộp.
- `xmax`: Khoảng cách từ mép trái ảnh đến cạnh phải của hộp.
- `ymax`: Khoảng cách từ mép trên ảnh đến cạnh dưới của hộp.

### Vấn đề: Tọa độ pixel phụ thuộc vào độ phân giải ảnh
Giả sử bạn có 2 bức ảnh của cùng một tờ hóa đơn:
- Bức ảnh A chụp bằng máy ảnh chuyên nghiệp độ phân giải cao ($4000 \times 3000$ pixels): Ô tổng tiền có tọa độ là `[2000, 2500, 2800, 2600]`.
- Bức ảnh B chụp bằng điện thoại cũ độ phân giải thấp ($800 \times 600$ pixels): Ô tổng tiền có tọa độ là `[400, 500, 560, 520]`.

Nếu mô hình AI học trực tiếp các con số pixel hàng nghìn này, nó sẽ bị bối rối vì cùng một vị trí trên tờ giấy nhưng con số tọa độ lại khác nhau hoàn toàn.

### Giải pháp: Chuẩn hoá tọa độ về dải [0, 1] (Normalized Coordinates)
Ta chia tọa độ x cho chiều rộng ($W$) và tọa độ y cho chiều cao ($H$) của ảnh:
$$x_{\text{norm}} = \frac{x}{W}, \quad y_{\text{norm}} = \frac{y}{H}$$

Khi đó, dù ảnh lớn hay ảnh nhỏ, một điểm nằm chính giữa trang giấy luôn có tọa độ $(0.5, 0.5)$.

Trong repository:
- Class [`BoundingBox`](../../src/docai/core/schema.py) quản lý 4 tọa độ này và có validator tự động kiểm tra để đảm bảo $x_{\text{min}} \le x_{\text{max}}$ và $y_{\text{min}} \le y_{\text{max}}$.
- Hàm chuyển đổi tọa độ chuẩn hoá được triển khai tại [`src/docai/data/preprocessing.py`](../../src/docai/data/preprocessing.py).

---

## 4. Tại sao hai pipeline khác nhau lại bắt buộc phải nói cùng một ngôn ngữ đầu ra?

Dự án này mang tên **DocAI Dual-Pipeline Benchmark** vì nó so sánh hai trường phái kỹ thuật có tư duy hoàn toàn trái ngược:
- **Track A (Classic)**: Chia nhỏ bài toán làm 3 bước nối tiếp (tìm vùng → đọc chữ → hiểu nghĩa).
- **Track B (VLM-native)**: Dùng một mô hình ngôn ngữ - thị giác duy nhất đọc một lượt từ ảnh ra kết quả.

Hãy hình dung bạn giao việc kiểm tra một tập hồ sơ cho hai nhân viên:
- Nhân viên A (đại diện Track A): Cầm bút chì khoanh từng ô, dùng kính lúp đọc từng chữ, rồi lấy sổ ghi chép lại từng số.
- Nhân viên B (đại diện Track B): Đọc lướt toàn bộ văn bản một lượt rồi nhớ lại trong đầu và ghi kết quả.

Nếu Nhân viên A nộp báo cáo dạng bảng Excel, còn Nhân viên B nộp báo cáo dạng đoạn văn mô tả tự do, làm sao người quản lý có thể đối chiếu xem ai làm chính xác hơn, ai đọc nhanh hơn và ai làm tốn ít chi phí hơn?

**Đó là lý do bắt buộc phải có JSON Schema Thống nhất (Unified JSON Schema).**

Dù Track A chạy qua 3 mô hình hay Track B chạy qua 1 mô hình, cả hai đều phải xuất dữ liệu ra cùng một cấu trúc Pydantic duy nhất: [`UnifiedDocumentOutput`](../../src/docai/core/schema.py).

```text
[ Kết quả Track A ] ─── ép về ───┐
                                  ├──→ [ UnifiedDocumentOutput ] ──→ [ So sánh Benchmark / API / Dash ]
[ Kết quả Track B ] ─── ép về ───┘
```

### Cấu trúc của `UnifiedDocumentOutput` gồm những gì?
Mỗi tài liệu sau khi xử lý sẽ trả về một đối tượng gồm 7 trường then chốt:
1. `document_type`: Loại tài liệu đã nhận diện (`invoice`, `receipt`, `contract`, `unknown`).
2. `fields`: Danh sách các trường thông tin trích xuất được. Mỗi trường ([`ExtractedField`](../../src/docai/core/schema.py)) gồm:
   - `field_name`: Tên trường chuẩn hoá (ví dụ: `total_amount`, `seller_name`, `governing_law`).
   - `field_value`: Giá trị văn bản đọc được (ví dụ: `1.500.000 VND`).
   - `confidence`: Độ tin cậy của mô hình từ 0.0 đến 1.0.
   - `bounding_box`: Tọa độ hình học của trường đó trên ảnh gốc để phục vụ vẽ khung và giải thích.
3. `overall_confidence`: Độ tin cậy trung bình của toàn bộ trang tài liệu.
4. `risk_flags`: Danh sách các cảnh báo gian lận hoặc rủi ro điều khoản từ Fraud/Risk Engine.
5. `execution_time_ms`: Thời gian xử lý tính bằng mili giây (dùng để đo độ trễ latency).
6. `pipeline_track`: Đánh dấu nguồn gốc xử lý là `track_a_classic` hay `track_b_vlm`.
7. `metadata`: Thông tin phụ trợ (kích thước ảnh, tên model checkpoint, ngày giờ xử lý).

---

## 5. Vai trò của Pydantic: Người gác cổng chất lượng dữ liệu

Trong hệ sinh thái Python, **Pydantic** là thư viện số một về xác thực dữ liệu (Data Validation) dựa trên kiểu dữ liệu (Python Type Hints).

Pydantic đóng vai trò như một "nhân viên hải quan nghiêm ngặt":
- Nếu một mô hình AI trả về độ tin cậy $1.5$ (vượt quá dải quy định $[0.0, 1.0]$), Pydantic sẽ từ chối ngay lập tức (`ValidationError`).
- Nếu mô hình vô tình trả về tọa độ $x_{\text{min}} = 500$ nhưng $x_{\text{max}} = 200$ (hộp bị lộn ngược), validator trong [`BoundingBox`](../../src/docai/core/schema.py) sẽ chặn lại và báo lỗi rõ ràng.

Nhờ có Pydantic, các tầng tiếp theo như Fraud Engine, API FastAPI và Dashboard Plotly Dash hoàn toàn yên tâm rằng dữ liệu đầu vào luôn chuẩn chỉnh về kiểu và khuôn mẫu, không bao giờ bị lỗi sập chương trình vì dữ liệu rác.

---

## 6. Kỹ thuật này đang ở đâu trong repository?

| Thành phần kỹ thuật | Vị trí file trong repo | Trạng thái thực tế | Giai đoạn triển khai |
|---|---|---|---|
| Hợp đồng JSON Schema (`UnifiedDocumentOutput`, `BoundingBox`, `ExtractedField`, `RiskFlag`) | [`src/docai/core/schema.py`](../../src/docai/core/schema.py) | **ĐANG SỬ DỤNG** | Giai đoạn 1 (Đã có unit test đầy đủ trong `tests/unit/test_schema.py`) |
| Quản lý cấu hình đường dẫn an toàn (`Settings`) | [`src/docai/core/config.py`](../../src/docai/core/config.py) | **ĐANG SỬ DỤNG** | Giai đoạn 2 (Đã kiểm thử trong `tests/unit/test_config.py`) |
| Nạp dữ liệu và quét metadata (`loaders.py`, `preprocessing.py`) | [`src/docai/data/`](../../src/docai/data/) | **ĐANG SỬ DỤNG** | Giai đoạn 1 (Sẵn sàng nạp 4 bộ dataset thật) |
| Notebook khảo sát EDA tương tác | [`notebooks/01-eda.ipynb`](../../notebooks/01-eda.ipynb) | **ĐANG SỬ DỤNG** | Giai đoạn 1 |
| Kịch bản dòng lệnh khảo sát dữ liệu thô | [`scripts/run_eda.py`](../../scripts/run_eda.py) | **ĐANG SỬ DỤNG** | Giai đoạn 1 |
