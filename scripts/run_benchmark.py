"""
CLI Script chạy so sánh benchmark giữa Track A và Track B trên một tài liệu.

Cách chạy:
    python scripts/run_benchmark.py --image path/to/invoice.jpg
"""

import argparse
from pathlib import Path
from docai.core.schema import DocumentType, ExtractedField, UnifiedDocumentOutput
from docai.evaluation.benchmark import BenchmarkRunner


def main():
    parser = argparse.ArgumentParser(description="Chạy đối chiếu benchmark Track A vs Track B")
    parser.add_argument("--image", type=str, default="sample.jpg", help="Đường dẫn file ảnh tài liệu để đối chiếu")
    args = parser.parse_args()

    print("==================================================")
    print("DOCAI BENCHMARK RUNNER (TRACK A vs TRACK B)")
    print("==================================================")
    print(f"File đầu vào: {args.image}")

    runner = BenchmarkRunner()

    # Tạo mẫu dữ liệu minh hoạ cho interface benchmark
    doc_a = UnifiedDocumentOutput(
        document_type=DocumentType.INVOICE,
        fields=[
            ExtractedField(field_name="seller_name", field_value="CONG TY ABC", confidence=0.95),
            ExtractedField(field_name="total_amount", field_value="1000000", confidence=0.92),
        ],
        execution_time_ms=1250.0,
        pipeline_track="track_a_classic"
    )

    doc_b = UnifiedDocumentOutput(
        document_type=DocumentType.INVOICE,
        fields=[
            ExtractedField(field_name="seller_name", field_value="CONG TY ABC", confidence=0.90),
            ExtractedField(field_name="total_amount", field_value="1000000", confidence=0.94),
        ],
        execution_time_ms=850.0,
        pipeline_track="track_b_vlm"
    )

    comparison = runner.compare_outputs(doc_a, doc_b)
    print("\nKết quả đối chiếu mẫu:")
    print(f"- Tỷ lệ đồng thuận trường: {comparison['field_agreement_ratio'] * 100:.1f}%")
    print(f"- Độ trễ Track A: {comparison['latency_track_a_ms']} ms")
    print(f"- Độ trễ Track B: {comparison['latency_track_b_ms']} ms")
    print(f"- Chênh lệch độ trễ: {comparison['latency_difference_ms']} ms")
    print(f"- Tóm tắt: {comparison['summary']}")


if __name__ == "__main__":
    main()
