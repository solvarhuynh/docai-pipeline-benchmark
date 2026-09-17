"""
CLI Script chạy pipeline Track B (VLM-native Single-pass Pipeline) trên một tài liệu.

Cách chạy:
    python scripts/run_track_b.py --image path/to/invoice.jpg --type invoice
"""

import argparse
from pathlib import Path
from docai.core.schema import DocumentType
from docai.pipelines.track_b import VLMDocumentParser


def main():
    parser = argparse.ArgumentParser(description="Chạy Track B (VLM-native Single-pass) trên ảnh tài liệu")
    parser.add_argument("--image", type=str, required=True, help="Đường dẫn file ảnh tài liệu đầu vào")
    parser.add_argument(
        "--type",
        type=str,
        default="invoice",
        choices=["invoice", "receipt", "contract"],
        help="Loại tài liệu (mặc định: invoice)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="PaddleOCR-VL",
        help="Tên mô hình VLM sử dụng (mặc định: PaddleOCR-VL)"
    )
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Lỗi: Không tìm thấy file ảnh tại {image_path}")
        return

    doc_type_mapping = {
        "invoice": DocumentType.INVOICE,
        "receipt": DocumentType.RECEIPT,
        "contract": DocumentType.CONTRACT,
    }
    doc_type = doc_type_mapping[args.type]

    print("==================================================")
    print("DOCAI TRACK B (VLM-NATIVE PIPELINE) RUNNER")
    print("==================================================")
    print(f"File đầu vào: {image_path}")
    print(f"Loại tài liệu: {doc_type.value}")
    print(f"Mô hình VLM: {args.model}")

    parser_vlm = VLMDocumentParser(model_name=args.model)
    prompt = parser_vlm.build_prompt(doc_type)

    print("\nKhởi tạo VLM parser thành công.")
    print(f"Structured Prompt:\n{prompt}")
    print("\nLưu ý: Logic inference thực tế đang ở mức Scaffold (Giai đoạn 5-6).")


if __name__ == "__main__":
    main()
