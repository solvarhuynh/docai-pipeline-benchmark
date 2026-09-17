# Cách giải thích — viết tài liệu kỹ thuật dễ hiểu

Các quy tắc này giữ độ chính xác kỹ thuật mà không giả định người đọc đã biết AI/ML/DL.

## Kể câu chuyện trước khi liệt kê thuật ngữ

Đi theo thứ tự:

```text
Sản phẩm muốn làm gì?
  ↓ vấn đề thực tế là gì?
  ↓ cách đơn giản thiếu ở đâu?
  ↓ kỹ thuật nào giải quyết phần đó?
  ↓ trực giác đời thường là gì?
  ↓ nó nằm ở đâu trong DocAI?
  ↓ output đi đâu tiếp?
```

Trước khi chuyển ý, phải trả lời được “vậy thì sao?”.

## Giải thích lần xuất hiện đầu tiên

Giữ English term, sau đó giải nghĩa dễ hiểu và đưa ví dụ Invoice/Contract. Ví dụ: **OCR (Optical Character Recognition)** là bước biến chữ trong ảnh thành text; OCR giúp máy có chuỗi để xử lý nhưng chưa biết con số là total hay tax.

Áp dụng cách này cho KIE, VLM, Transformer, token, embedding, attention, bounding box, pretrained model, fine-tuning, inference, schema, Pydantic, API, REST, JSON, Precision, Recall, F1-score, latency và structured output.

Không dùng một thuật ngữ khó khác để giải thích thuật ngữ khó. Dùng ví dụ đời thường trước rồi mới thêm định nghĩa formal.

## Dùng cả hai domain

Dùng ví dụ Invoice (vendor, date, tax, total, số và bảng) và Contract (metadata, termination clause, governing law, văn bản dài). Không giả định một field list hoặc model phải phù hợp cho cả hai.

## Giải thích code và luồng, không chỉ lý thuyết

Mỗi phần kỹ thuật cần nêu file liên quan dưới `src/docai/` hoặc `frontend/`, input/output, owner là Track A/B/Product/Research, cách đi tới `UnifiedDocumentOutput`/FastAPI/React và test/metric dùng để kiểm chứng.

## Trực giác trước công thức

Với Recall, trước hết hỏi: trong mọi clause thật sự cần tìm, hệ thống tìm được bao nhiêu? Sau đó mới định nghĩa TP/FN và đưa công thức. Không gọi metric tốt/xấu nếu thiếu dataset, domain, field/track và điều kiện đo.

## Trung thực về trạng thái

`Implemented/Baseline` cần evidence; `Scaffold` là interface chưa đủ runtime; `Planned` chưa bắt đầu; `Not selected` là candidate. Attention map không tự động là explanation; risk flag không phải kết luận pháp lý; mock result không phải benchmark.

## Giữ cấu trúc dễ đọc

Ưu tiên tiêu đề dạng câu hỏi như “Vì sao OCR đọc được chữ nhưng chưa biết đâu là total?”. Không biến tài liệu thành glossary thuần túy và không tạo một file cho mỗi keyword.
