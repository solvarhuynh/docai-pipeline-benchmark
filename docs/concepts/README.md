# Lộ trình khái niệm — học DocAI từ tài liệu đi ra

Thư mục này giải thích vì sao DocAI được thiết kế như hiện tại, dành cho người biết lập trình/data nhưng chưa làm AI/ML/DL hằng ngày.

## Câu chuyện trong một trang

```text
Invoice hoặc Contract
  ↓ đọc chữ, layout và meaning
  ↓ trích xuất field hoặc clause
  ↓ validate, gắn risk/evidence
  ↓ trả JSON qua FastAPI
  ↓ hiển thị trên React
```

Track A và Track B là hai cách xử lý phần giữa. Product có thể dùng một trong hai; Research chỉ so sánh khi có output thật và ground truth.

## Thứ tự nên đọc

1. [`01-docai-foundations.md`](./01-docai-foundations.md) — document khác image thế nào và structured output là gì.
2. [`02-track-a-classic.md`](./02-track-a-classic.md) — vì sao pipeline specialist tách layout, OCR và understanding.
3. [`03-track-b-vlm.md`](./03-track-b-vlm.md) — vì sao VLM có thể kết hợp visual understanding và response generation.
4. [`04-fraud-and-explainability.md`](./04-fraud-and-explainability.md) — risk flag/evidence hỗ trợ review ra sao.
5. [`05-evaluation.md`](./05-evaluation.md) — cách biết pipeline hoạt động tốt đến đâu.

Đọc song song [`docs/architecture/architecture-explained.md`](../architecture/architecture-explained.md) để nối khái niệm với code.

## Mental model

```text
product problem → document representation → processing engine
                → shared schema → API/frontend → risk/evidence
                → research measurement
```

Mỗi khái niệm cần trả lời: giải quyết vấn đề gì, trực giác đời thường là gì, nằm ở file nào, và output đi đâu tiếp.

## Từ chỉ trạng thái

- **Implemented/Baseline:** code có và có test/runtime evidence.
- **Scaffold:** interface/page có nhưng hành vi thật chưa hoàn chỉnh.
- **Planned:** có trong roadmap nhưng chưa bắt đầu.
- **Not selected:** model/tool còn là candidate.

Hiện React frontend, model inference, API orchestration và Research Lab chủ yếu là scaffold/planned. Không coi output hoặc metric là thật nếu chưa có run thật.
