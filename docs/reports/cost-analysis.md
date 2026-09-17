# Cost analysis — DocAI Research Lab

**Trạng thái: PLANNED / REPORT SCAFFOLD.** Chưa có GPU run, inference measurement hoặc giá trị cost benchmark được ghi nhận trong repository này.

## Phạm vi đo

- Track A: layout/OCR/KIE runtime và fine-tuning cost nếu được phê duyệt.
- Track B: VLM inference runtime theo model/endpoint thực tế sau khi model được chốt.
- Product API/UI overhead nếu có thể đo tách biệt.
- Ước tính theo cùng số trang, input size, hardware và batching assumptions.

## Cách ghi nhận

Mỗi kết quả phải nêu model/checkpoint, hardware, số trang, warm-up, batch size, wall-clock time, đơn giá nguồn và công thức tính. Chi phí Modal/API thương mại chỉ được so sánh khi nguồn giá và assumptions được ghi rõ.

## Planned comparison

- GPU-hour hoặc serverless runtime của Track A và Track B.
- Cost trên workload Invoice và Contract.
- Sensitivity theo volume, latency target và batching.
- Break-even estimate với API thương mại nếu có dữ liệu giá công khai phù hợp.

Không dùng estimate như actual measurement và không tuyên bố engine rẻ hơn khi chưa có số liệu thật.
