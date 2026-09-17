# Glossary DocAI

Đây là mục tra cứu nhanh. Phần giải thích theo mạch câu chuyện nằm trong [`docs/concepts/`](../concepts/).

| Thuật ngữ | Nghĩa dễ hiểu | Vị trí sử dụng |
| --- | --- | --- |
| API | Bộ quy tắc để hai phần mềm giao tiếp. | React gửi request cho FastAPI. |
| REST | Cách tổ chức API qua HTTP method và route. | Endpoint product/research. |
| JSON | Dạng text biểu diễn object, list, string và number. | Response FastAPI/frontend. |
| Pydantic | Thư viện Python kiểm tra dữ liệu theo model/schema. | Validate `UnifiedDocumentOutput`. |
| React | Thư viện ghép giao diện browser từ component. | `frontend/src/`. |
| TypeScript | JavaScript có type để bắt nhiều lỗi trước runtime. | Mirror API contract. |
| Vite | Dev server và build tool cho frontend. | Chạy/đóng gói React. |
| Node.js | Runtime chạy npm, Vite và TypeScript ở project này. | Không phải business backend. |
| Document AI | Phần mềm biến tài liệu thành thông tin có cấu trúc. | Phạm vi sản phẩm. |
| OCR | Đổi chữ trong pixel ảnh thành text. | Track A và visual reading. |
| Layout Detection | Tìm và gán nhãn vùng như table/total. | Stage đầu của Track A. |
| Bounding Box | Hình chữ nhật chỉ vị trí của item. | Layout và evidence. |
| KIE | Gán business meaning cho text. | Field Invoice/clause Contract. |
| VLM | Model xử lý hình ảnh và ngôn ngữ cùng nhau. | Track B. |
| Transformer | Kiến trúc dùng context để so sánh các phần input. | LayoutLMv3/VLM. |
| Token | Đơn vị nhỏ model xử lý; một từ có thể tách nhiều token. | KIE và prompt. |
| Embedding | Biểu diễn số của item để model so sánh/xử lý. | Text/image representation. |
| Attention | Trọng số context ảnh hưởng đến dự đoán. | Diagnostic, không phải proof. |
| Prompt | Instruction gửi cho model sinh output. | Track B. |
| Schema | Hình dạng, type và constraint của dữ liệu. | Python/TypeScript contract. |
| Structured Output | Kết quả theo schema ổn định thay vì đoạn văn tự do. | JSON cho product. |
| Pretrained Model | Model đã học pattern tổng quát từ dữ liệu trước đó. | Điểm bắt đầu của pipeline. |
| Fine-tuning | Điều chỉnh pretrained model cho task hẹp hơn. | Phase tương lai. |
| Checkpoint | Trạng thái model được lưu để inference. | Cần ghi khi benchmark. |
| Inference | Dùng model đã lưu để xử lý tài liệu mới. | Runtime pipeline. |
| Hallucination | Model sinh nội dung nghe hợp lý nhưng không có trong tài liệu. | Rủi ro Track B. |
| Precision | Trong các item dự đoán, tỷ lệ item đúng. | Evaluation. |
| Recall | Trong các item thật, tỷ lệ item tìm được. | Đo bỏ sót. |
| F1-score | Số cân bằng Precision và Recall. | So sánh field/clause. |
| Latency | Thời gian xử lý request. | Product/research. |
| Robustness | Khả năng giữ chất lượng khi input nhiễu. | Blur, xoay, contrast. |
| Invoice Risk | Tín hiệu review như arithmetic mismatch. | Invoice Intelligence. |
| Contract Risk | Tín hiệu review về clause/metadata. | Contract Intelligence, không phải legal advice. |
| Explainability | Evidence giúp người dùng hiểu kết quả. | Box, span, supporting text. |
| Ground Truth | Đáp án tham chiếu dùng để đo accuracy. | Bắt buộc trước khi claim metric. |

## Từ chỉ trạng thái

`Implemented` là hành vi đã có evidence. `Baseline` là nền tảng nhỏ đã chạy/test. `SCAFFOLD` là interface/placeholder chưa đủ runtime. `PLANNED` là việc trong roadmap chưa bắt đầu. `NOT SELECTED` là model/tool còn ở mức candidate.
