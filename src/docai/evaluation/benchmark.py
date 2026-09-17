"""
Module điều phối chạy benchmark và so sánh đối đầu (Benchmark Runner).

Thuộc: Giai đoạn 9 và 10 (Benchmark tổng hợp và API so sánh).
Tham chiếu: implementation-guide.md; task-split.md.

Mục đích:
Cung cấp class BenchmarkRunner nhận đầu vào là tài liệu, thực thi song song hai track,
đo lường độ trễ và tính toán tỷ lệ đồng thuận để phục vụ endpoint /compare và báo cáo benchmark.
"""

from typing import Any, Dict, List, Optional
from docai.core.schema import DocumentType, UnifiedDocumentOutput
from docai.evaluation.metrics import calculate_field_agreement


class BenchmarkRunner:
    """
    Trình điều phối so sánh hiệu năng giữa Track A và Track B.
    """

    def __init__(self):
        pass

    def compare_outputs(
        self,
        output_a: UnifiedDocumentOutput,
        output_b: UnifiedDocumentOutput
    ) -> Dict[str, Any]:
        """
        Đối chiếu trực tiếp hai output chuẩn hoá đã có từ Track A và Track B.
        """
        agreement = calculate_field_agreement(output_a, output_b)
        latency_a = output_a.execution_time_ms or 0.0
        latency_b = output_b.execution_time_ms or 0.0
        diff_ms = round(latency_b - latency_a, 2)

        summary = (
            f"Độ đồng thuận giữa Track A và Track B đạt {agreement * 100:.1f}%. "
            f"Chênh lệch thời gian suy luận: {abs(diff_ms):.2f} ms "
            f"({'Track A nhanh hơn' if diff_ms > 0 else 'Track B nhanh hơn hoặc tương đương'})."
        )

        return {
            "field_agreement_ratio": agreement,
            "latency_track_a_ms": latency_a,
            "latency_track_b_ms": latency_b,
            "latency_difference_ms": diff_ms,
            "summary": summary,
        }

    def run_benchmark_on_sample(
        self,
        image_path: str,
        document_type: DocumentType = DocumentType.INVOICE
    ) -> Dict[str, Any]:
        """
        Chạy cả 2 track trên một file ảnh và tổng hợp kết quả đối chiếu.
        """
        # TODO: Giai đoạn 10 - Kết nối pipeline thực tế khi đã nạp weights
        raise NotImplementedError("TODO: Giai đoạn 10 - Chạy thực thi 2 pipeline trên ảnh thật để benchmark")
