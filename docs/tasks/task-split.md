# Phân chia công việc — Product và Research DocAI

Đây là tài liệu phân công chung cho hai pipeline và các phần product liên quan. DocAI là một sản phẩm với hai domain ngang hàng: Invoice Intelligence và Contract Intelligence; Track A và Track B là hai engine xử lý thay thế cho nhau.

## Bảng ownership

| Khu vực | Owner chính | Trách nhiệm chính |
| --- | --- | --- |
| Track A | Thành viên A | Pipeline AI/ML/DL cổ điển: layout, OCR, KIE và hỗ trợ đánh giá model. |
| Track B | Thành viên B | Parsing bằng VLM, prompt, validate response và tích hợp model. |
| Product Engineering | Hai thành viên phối hợp | FastAPI, React, API contract, risk/evidence và luồng end-to-end. |
| Research & Evaluation | Hai thành viên cùng làm | Ground truth, protocol, metrics, robustness, latency và cost. |

Owner là người dẫn dắt và chuẩn bị bàn giao. Không thành viên nào tự đổi shared schema hoặc evaluation protocol mà không review với track còn lại.

## Quy tắc chung

- `src/docai/core/schema.py` là source of truth Python của `UnifiedDocumentOutput`.
- `frontend/src/types/document.ts` phản ánh API contract ở phía trình duyệt.
- FastAPI/Python là business backend duy nhất; React + TypeScript + Vite là frontend.
- Track A/B phụ trách processing; frontend không chứa model logic.
- Invoice và Contract được phép có taxonomy field/clause khác nhau trong cùng envelope.
- Chỉ dùng `Implemented` hoặc `Baseline` khi có code và evidence; nếu chưa thì dùng `SCAFFOLD`, `PLANNED` hoặc `NOT SELECTED`.
- Mỗi task phải cập nhật [`log/progress-log.md`](../../log/progress-log.md).
- Không train, fine-tune, tải dataset, bịa metric hoặc deploy production nếu chưa có task được duyệt.

## Ranh giới Product và Research

Product Engineering xây luồng để người dùng gửi tài liệu và review kết quả. Research đo chất lượng engine theo protocol. Placeholder của product không phải benchmark, và benchmark không tự động trở thành tính năng production.

```text
React + TypeScript + Vite
        ↓ HTTP/REST/JSON
FastAPI → Track A hoặc Track B
        ↓
Pydantic UnifiedDocumentOutput
        ↓
Risk / evidence / evaluation
```

## Thứ tự triển khai

1. Thống nhất input và shared output contract.
2. Implement mỗi track sau một interface ổn định.
3. Kết nối engine vào FastAPI, không đưa model logic vào route.
4. Kết nối trang Invoice và Contract với API thật.
5. Thêm risk và evidence vào luồng review.
6. Chạy end-to-end checks rồi mới bắt đầu so sánh research.

Xem kế hoạch chi tiết tại [`track-a-classic-tasks.md`](./track-a-classic-tasks.md) và [`track-b-vlm-tasks.md`](./track-b-vlm-tasks.md).
