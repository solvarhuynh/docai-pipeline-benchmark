# Giải thích kiến trúc tổng thể — DocAI Document Intelligence Platform

Tài liệu này giải thích kiến trúc product-first của DocAI: một hệ thống xử lý Invoice/Receipt Document Intelligence có hai processing engine bên trong, kèm một research component để benchmark các trade-off giữa Classic và VLM-native.

Mỗi quyết định kiến trúc được trình bày theo cấu trúc chuẩn: **Vấn đề — Giải pháp — Lý do chọn**.

---

## 1. Product Architecture và Research Architecture

### Product Architecture

Product layer chịu trách nhiệm nhận tài liệu, điều phối engine, chuẩn hoá output và phục vụ người dùng. Luồng mục tiêu là:

```text
Upload PDF/Image hóa đơn hoặc biên lai
          ↓
Input validation & normalization
          ↓
Document Processing Engine
       ┌──┴──┐
       ↓     ↓
   Track A  Track B
       └──┬──┘
          ↓
UnifiedDocumentOutput
          ↓
Schema validation → Fraud/Risk → Explainability khi khả dụng
          ↓
FastAPI → Plotly Dash
```

Invoice/Receipt là primary product use case. Contract/CUAD vẫn dùng chung các contract và module, nhưng được xem là extension và secondary research use case để kiểm tra generalization.

### Research Architecture

Research layer nhận output chuẩn hoá từ hai engine, không trở thành product flow bắt buộc cho từng tài liệu:

```text
Track A output ─┐
                ├→ Evaluation → Benchmark → Robustness/Cost reports
Track B output ─┘
```

Mục tiêu là trả lời: khi cùng phục vụ một product Document AI, Classic modular và VLM-native đánh đổi như thế nào về accuracy, latency, robustness, explainability và cost?

Product MVP và Research Complete là hai milestone độc lập. Hiện repository mới có schema, baseline rules và scaffold cho các engine/API/Dash; chưa có Product MVP end-to-end hoặc kết quả research thật.

## 2. Tổng quan kiến trúc và Luồng dữ liệu (Data Flow)

Hệ thống được thiết kế để nhận đầu vào là một file ảnh tài liệu (hóa đơn, biên lai hoặc hợp đồng pháp lý) và đưa qua một trong hai pipeline (hoặc cả hai đồng thời để so sánh), sau đó trả về một kết quả chuẩn hoá duy nhất theo JSON schema thống nhất kèm các cảnh báo rủi ro và bản đồ nhiệt giải thích.

```
                   [ Tài liệu đầu vào: Ảnh Hóa đơn hoặc Hợp đồng ]
                                         |
            +----------------------------+----------------------------+
            |                                                         |
     [ Track A: Classic ]                                      [ Track B: VLM ]
            |                                                         |
  (1) Layout Detection                                       (1) Vision-Language Model
      YOLOv8-doc phân vùng                                       PaddleOCR-VL / dots.ocr
      (Header, Table, Signature)                                 (Đọc chữ + hiểu layout
            |                                                     trong một lượt single-pass)
  (2) OCR Extraction                                                  |
      PaddleOCR đọc ký tự                                             |
      kèm tọa độ bounding box                                         |
            |                                                         |
  (3) Key Information Extraction                                      |
      LayoutLMv3 fine-tuned                                           |
      (Phân loại thực thể BIO)                                        |
            |                                                         |
            +----------------------------+----------------------------+
                                         |
                        [ Unified JSON Schema Output ]
                        (docai.core.schema: DocumentType,
                         Fields, Confidence, BoundingBox)
                                         |
            +----------------------------+----------------------------+
            |                                                         |
  [ Fraud/Risk Engine ]                                    [ Explainability Layer ]
  (docai.fraud.rules)                                      (docai.explainability.explainer)
  - Hóa đơn: Kiểm tra số học,                              - Track A: LayoutLMv3 attention
    bất thường độ tin cậy OCR                                - Track B: Visual grounding / Grad-CAM
  - Hợp đồng: Rủi ro điều khoản CUAD                       - Tạo overlay heatmap lên ảnh gốc
            |                                                         |
            +----------------------------+----------------------------+
                                         |
                            [ FastAPI REST Endpoints ]
                            (docai.api.main: /parse/classic,
                             /parse/vlm, /compare, /explain)
                                         |
                                         v
                         [ Visualization Dashboard ]
                         (Plotly Dash: Python -> pandas -> Plotly -> Dash)
                         - Trích xuất & Confidence
                         - So sánh Track A vs Track B
                         - Fraud/Rule Flags & Explainability
                         - Benchmark Metrics
```

### Luồng xử lý chi tiết của Track A (Classic Multi-stage Pipeline)

Track A chia nhỏ bài toán thành chuỗi ba giai đoạn độc lập nối tiếp:

1. **Layout Detection (Phân vùng bố cục)**:
   - Thuật ngữ: Layout Detection là kỹ thuật thị giác máy tính dùng để xác định vị trí và phân loại các khối chức năng trên trang tài liệu (như tiêu đề, bảng biểu, đoạn văn, chữ ký).
   - Xử lý: Ảnh gốc được đưa qua mô hình YOLOv8-doc / DocLayout-YOLO đã được huấn luyện sẵn (pretrained) để tìm tọa độ các vùng như Header, Table, Signature.

2. **OCR Extraction (Nhận dạng ký tự quang học)**:
   - Thuật ngữ: OCR (Optical Character Recognition) là công nghệ nhận dạng và chuyển đổi hình ảnh chứa chữ viết thành văn bản ký tự số mà máy tính có thể đọc và xử lý.
   - Xử lý: PaddleOCR quét trên từng vùng layout hoặc toàn bộ ảnh, trả về từng từ (token) kèm độ tin cậy (confidence score) và hộp giới hạn 4 điểm (bounding box). Tọa độ này được ghép vùng (spatial join) với layout để tạo ra JSON trung gian.

3. **Key Information Extraction (KIE — Trích xuất thông tin then chốt)**:
   - Thuật ngữ: KIE (Key Information Extraction) là bước phân loại và trích xuất các trường nghiệp vụ cụ thể (ví dụ: tên người bán, ngày lập, tổng tiền) từ tập hợp các từ rời rạc của OCR.
   - Xử lý: Mô hình LayoutLMv3 (mô hình đa phương thức kết hợp chữ, vị trí 2D và hình ảnh) gán nhãn theo quy ước BIO (Begin-Inside-Outside) để gom các từ thành từng thực thể nghiệp vụ hoàn chỉnh.

### Luồng xử lý chi tiết của Track B (VLM-native Single-pass Pipeline)

Track B tiếp cận theo hướng hợp nhất, loại bỏ các bước trung gian:

1. **VLM-native Parsing (Trích xuất thông qua mô hình thị giác — ngôn ngữ)**:
   - Thuật ngữ: VLM-native (Vision-Language Model) là kiến trúc mô hình học sâu hợp nhất khả năng nhìn ảnh và hiểu ngôn ngữ trong cùng một mạng nơ-ron duy nhất, xử lý trực tiếp ảnh đầu vào thành văn bản có cấu trúc mà không cần qua bước OCR tách rời.
   - Xử lý: Toàn bộ ảnh tài liệu được đưa vào PaddleOCR-VL hoặc dots.ocr kèm một câu lệnh định hướng (structured prompt). Mô hình tự động phân tích bố cục và trả về trực tiếp các cặp trường — giá trị đúng theo JSON schema thống nhất.

---

## 3. Các quyết định kiến trúc cốt lõi

Mỗi quyết định dưới đây giải thích rõ vì sao product cần các thành phần hiện tại, đồng thời chỉ ra phần nào thuộc research/quality evaluation.

### Quyết định 1: Xây dựng 2 track song song thay vì chỉ chọn một hướng duy nhất

- **Vấn đề**:
  Trong cộng đồng Document AI hiện nay có sự chia rẽ giữa hai xu hướng:
  - Xu hướng cổ điển (Track A) được tối ưu hoá qua nhiều năm, các thành phần mô-đun hoá rất rõ ràng, dễ kiểm soát lỗi ở từng bước nhưng hệ thống cồng kềnh và tốn công fine-tune riêng từng mô hình.
  - Xu hướng VLM-native (Track B) đơn giản hoá toàn bộ pipeline chỉ với một mô hình duy nhất, không cần gán nhãn tọa độ phức tạp, nhưng lại tốn nhiều tài nguyên tính toán (GPU VRAM lớn) và có nguy cơ tạo ra thông tin sai lệch (hallucination — hiện tượng mô hình ngôn ngữ tự sinh ra thông tin không có thật trong ảnh).
- **Giải pháp**:
  Triển khai song song cả hai pipeline trên cùng một hệ thống mã nguồn, áp dụng cùng một bộ dữ liệu đánh giá và ép đầu ra về cùng một JSON schema thống nhất (`docai.core.schema`).
- **Lý do chọn**:
  Product có thể chọn một engine để xử lý tài liệu, còn research có thể đặt hai engine lên cùng một bàn cân với cùng điều kiện thử nghiệm để đo sự đánh đổi giữa độ chính xác (F1-score), thời gian phản hồi (latency), chi phí vận hành (cost) và tài nguyên phần cứng.

### Quyết định 2: Giữ Hợp đồng (CUAD) như extension nghiên cứu

- **Vấn đề**:
  Phần lớn các dự án Document AI trên GitHub chỉ dừng lại ở hóa đơn và biên lai. Hóa đơn là loại tài liệu có bố cục tương đối cố định, độ dài ngắn (1-2 trang), chứa nhiều số liệu và các từ khóa lặp lại (Tổng tiền, VAT, Ngày). Một pipeline hoạt động tốt trên hóa đơn không đồng nghĩa với việc sẽ hoạt động tốt trên các loại tài liệu khác. Khi đưa vào hợp đồng pháp lý (văn bản dài hàng chục trang, ngôn từ pháp lý phức tạp, cấu trúc phi tiêu chuẩn), hiệu năng mô hình thường bị tụt giảm nghiêm trọng.
- **Giải pháp**:
  Giữ bộ dữ liệu hợp đồng pháp lý CUAD (Contract Understanding Atticus Dataset) gồm 510 hợp đồng thật với hơn 13.000 điều khoản được các luật sư gán nhãn như một extension để đo Generalization drop (độ sụt giảm hiệu năng khi tổng quát hoá sang miền dữ liệu mới), không đặt ngang hàng với Invoice/Receipt trong Product MVP.
- **Lý do chọn**:
  Kiểm tra xem kiến trúc nào tổng quát hoá tốt hơn khi chuyển từ hóa đơn sang hợp đồng. Về mặt lý thuyết, mô hình VLM được huấn luyện trên kho ngữ liệu khổng lồ thường có khả năng tổng quát hoá zero-shot tốt hơn Track A vốn bị bó buộc vào tập nhãn BIO của LayoutLMv3. Đây là điểm nhấn nghiên cứu quan trọng nhất của dự án.

### Quyết định 3: Tích hợp lớp giải thích (Explainability Layer)

- **Vấn đề**:
  Các mô hình học sâu truyền thống hoạt động như một "hộp đen" (black-box). Khi mô hình trả về một con số "Tổng tiền: 5.000.000 VND", người dùng, kế toán viên hoặc cơ quan kiểm toán không thể biết mô hình dựa vào đâu trên hóa đơn để ra được con số đó. Nếu trích xuất sai, rất khó để truy vết lỗi nằm ở khâu OCR hay khâu hiểu layout.
- **Giải pháp**:
  Xây dựng module `docai.explainability.explainer`:
  - Với Track A: Trích xuất attention weights (trọng số chú ý của cơ chế Transformer) từ LayoutLMv3, quy đổi về tọa độ hộp giới hạn và vẽ bản đồ nhiệt (attention heatmap).
  - Với Track B: Trích xuất visual grounding (cơ chế ánh xạ từ khóa vào vùng nhìn của ảnh) hoặc dùng Grad-CAM (kỹ thuật tính gradient của lớp tích chập để xác định vùng ảnh ảnh hưởng nhiều nhất đến kết quả).
  - Dùng OpenCV tạo ảnh overlay bản đồ nhiệt màu (JET colormap) phủ lên ảnh gốc.
- **Lý do chọn**:
  Explainability biến hệ thống từ một "hộp đen" thành một công cụ minh bạch, giúp người vận hành có thể xác minh bằng mắt thường vùng ảnh mô hình đã "nhìn", từ đó phát hiện sớm các lỗi ảo giác hoặc đọc nhầm dòng.

### Quyết định 4: Xây dựng bộ kiểm thử độ bền (Robustness Test Suite)

- **Vấn đề**:
  Trong môi trường thực nghiệm, mô hình thường được đánh giá trên ảnh sạch, độ phân giải cao, chụp thẳng góc. Tuy nhiên trong thực tế vận hành doanh nghiệp, tài liệu được người dùng chụp bằng điện thoại trong điều kiện rung tay, thiếu sáng, góc chụp nghiêng hoặc có dấu chìm (watermark). Phần lớn các giải pháp Document AI thường bị "sập" hoặc giảm độ chính xác nặng nề khi gặp ảnh bị biến dạng.
- **Giải pháp**:
  Xây dựng bộ script sinh biến thể ảnh chủ động (Perturbation Suite):
  - Xoay ảnh lệch góc: 5 độ, 10 độ, 15 độ.
  - Làm mờ quang học (Gaussian Blur).
  - Giảm độ sáng và độ tương phản xuống 70%, 50%, 30%.
  - Chèn watermark chữ mờ lên bề mặt văn bản.
  Sau đó chạy cả 2 track trên từng mức độ nhiễu để vẽ đường cong độ giảm F1-score.
- **Lý do chọn**:
  Giúp đo lường chính xác ngưỡng chịu đựng (tolerance threshold) của từng track, chỉ ra điểm đứt gãy của từng thành phần (ví dụ: bước nào bị ảnh hưởng trước giữa Layout và OCR khi bị mờ), từ đó kết luận giải pháp nào đủ độ tin cậy để triển khai thực tế (production-ready).

### Quyết định 5: Chuẩn hoá JSON schema và Tích hợp Fraud/Risk Engine

- **Vấn đề**:
  Một hệ thống Document AI hoàn chỉnh không chỉ dừng ở việc nhận dạng chữ, mà phải giúp doanh nghiệp phát hiện rủi ro nghiệp vụ. Đối với hóa đơn, đó là rủi ro bị sửa số tiền hoặc chèn thêm số. Đối với hợp đồng, đó là rủi ro thiếu điều khoản bắt buộc bảo vệ pháp lý.
- **Giải pháp**:
  - Thiết kế JSON schema thống nhất (`docai.core.schema`) chứa trường `risk_flags`.
  - Module `docai.fraud.rules` triển khai:
    - Rule đối chiếu số học hóa đơn: Tổng tiền trước thuế + Tiền thuế VAT = Tổng thanh toán.
    - Rule bất thường độ tin cậy OCR: Phát hiện các ký tự số có confidence thấp hơn bất thường so với các chữ xung quanh (dấu hiệu tẩy xóa, chỉnh sửa ảnh).
    - Rule hợp đồng ở mức extension: Kiểm tra một số điều khoản bắt buộc (Governing Law, Termination, Dispute Resolution); taxonomy CUAD đầy đủ và generalization evaluation thuộc research phase sau.
- **Lý do chọn**:
  Tạo ra giá trị ứng dụng nghiệp vụ thực tế, kết hợp giữa trí tuệ nhân tạo (trích xuất) và luật logic nghiệp vụ (business rules validation) trong cùng một gói API.

### Quyết định 6: Lựa chọn Plotly Dash cho tầng trực quan hoá và Dashboard (Visualization Layer)

- **Vấn đề**:
  Product cần giao diện để người dùng xem kết quả trích xuất, confidence, risk flags và bằng chứng giải thích. Research Lab cũng cần một khu vực so sánh hai pipeline và theo dõi metric benchmark. Việc sử dụng các công cụ Business Intelligence độc quyền (như Power BI) tạo ra sự phụ thuộc vào phần mềm bên ngoài, định dạng nhị phân đóng (.pbix), khó tích hợp vào quy trình CI/CD mã nguồn mở và không tận dụng được cấu trúc dữ liệu JSON/Pydantic của hệ sinh thái Python.
- **Giải pháp**:
  Chuẩn hoá stack trực quan hoá mặc định trên nền tảng Python native:
  `Python → pandas → Plotly → Dash`
  Dashboard sẽ đọc trực tiếp kết quả chuẩn hoá từ pipeline DocAI/API (`UnifiedDocumentOutput`) để phục vụ hai khu vực:
  - **Product**: Document Parser, Risk Review, Document Details và Explainability khi đã có output.
  - **Research Lab**: Track Comparison, Benchmark, Robustness và Cost Analysis khi đã có dữ liệu thực nghiệm.
  Các nhóm nội dung gồm:
  - Kết quả trích xuất tài liệu chi tiết theo từng trường;
  - Độ tin cậy (confidence score) của các trường;
  - So sánh đối đầu giữa Track A (Classic) và Track B (VLM);
  - Danh sách cảnh báo gian lận và rủi ro điều khoản (fraud/rule flags);
  - Lớp bản đồ nhiệt giải thích (Explainability);
  - Các metric benchmark tổng hợp khi giai đoạn đánh giá đã có dữ liệu thực nghiệm thật.
- **Lý do chọn**:
  Plotly Dash là framework mã nguồn mở chạy hoàn toàn trên nền tảng Python, tích hợp tự nhiên với pandas DataFrame và API FastAPI, kiểm soát phiên bản mã nguồn 100% bằng Git, không phụ thuộc license bên ngoài, và tuyệt đối loại bỏ sự phụ thuộc vào Power BI hay file .pbix.

---

## 4. Trạng thái triển khai hiện tại (Status)

Theo dõi đối chiếu với `log/progress-log.md`:
- **Product layer**: Đã xác định data/input, processing engines, schema, validation/risk, API và Dashboard responsibilities; phần runtime end-to-end chưa hoàn thành.
- **Research layer**: Đã có khung metrics/benchmark và các báo cáo chờ dữ liệu thật; chưa có kết quả thực nghiệm.
- **Khung kiến trúc và mã nguồn (Scaffolding)**: Đã hoàn thành (Pydantic schema, các class stub, FastAPI routes, Docker Compose, script test Modal GPU).
- **Logic xử lý thực tế của các mô hình**: Đã lên kế hoạch, chưa triển khai (sẽ được hiện thực hoá lần lượt qua các Giai đoạn 1 đến 10 trong `docs/specs/implementation-guide.md`).
