# Phân tích chi phí — DocAI Research Lab

**Trạng thái: PLANNED / REPORT SCAFFOLD.** Chưa có GPU run, inference measurement hoặc cost benchmark trong repository.

## Phạm vi đo

Đo runtime layout/OCR/KIE của Track A, runtime VLM của Track B sau khi chọn model, overhead API/UI nếu tách được, và cost trên cùng số trang, input size, hardware, batch size.

## Cách ghi nhận

Mỗi kết quả phải ghi model/checkpoint, hardware, page count, warm-up, batch size, wall-clock time, nguồn đơn giá và công thức. Estimate không được gọi là actual measurement.

## So sánh dự kiến

So sánh GPU-hour/serverless runtime, cost theo workload Invoice/Contract, sensitivity theo volume/latency/batching và break-even với commercial API nếu có dữ liệu giá đáng tin cậy. Không tuyên bố engine rẻ hơn khi chưa có số liệu.
