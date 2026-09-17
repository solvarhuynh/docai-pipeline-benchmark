"""
CLI Script chạy so sánh benchmark giữa Track A và Track B trên một tài liệu.

Cách chạy:
    python scripts/run_benchmark.py --image path/to/invoice.jpg
"""

import argparse
from pathlib import Path
from docai.core.schema import DocumentType
from docai.evaluation.benchmark import BenchmarkRunner


def main() -> int:
    parser = argparse.ArgumentParser(description="Chạy đối chiếu benchmark Track A vs Track B")
    parser.add_argument("--image", type=str, required=True, help="Đường dẫn file ảnh tài liệu để đối chiếu")
    parser.add_argument(
        "--type",
        type=str,
        default="invoice",
        choices=["invoice", "receipt", "contract"],
        help="Loại tài liệu (mặc định: invoice)"
    )
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.is_file():
        print(f"Lỗi: Không tìm thấy file ảnh tại {image_path}")
        return 1

    document_type = {
        "invoice": DocumentType.INVOICE,
        "receipt": DocumentType.RECEIPT,
        "contract": DocumentType.CONTRACT,
    }[args.type]

    print("==================================================")
    print("DOCAI BENCHMARK RUNNER (TRACK A vs TRACK B)")
    print("==================================================")
    print(f"File đầu vào: {image_path}")
    print(f"Loại tài liệu: {document_type.value}")

    runner = BenchmarkRunner()

    try:
        comparison = runner.run_benchmark_on_sample(str(image_path), document_type)
    except NotImplementedError as exc:
        print(f"\nCHƯA TRIỂN KHAI — benchmark runtime thuộc giai đoạn sau.\n{exc}")
        return 2

    print("\nKết quả đối chiếu:")
    print(f"- Tỷ lệ đồng thuận trường: {comparison['field_agreement_ratio'] * 100:.1f}%")
    print(f"- Độ trễ Track A: {comparison['latency_track_a_ms']} ms")
    print(f"- Độ trễ Track B: {comparison['latency_track_b_ms']} ms")
    print(f"- Chênh lệch độ trễ: {comparison['latency_difference_ms']} ms")
    print(f"- Tóm tắt: {comparison['summary']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
