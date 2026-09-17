"""
CLI Script chạy pipeline Track A (Classic Multi-stage Pipeline) trên một tài liệu.

Cách chạy:
    python scripts/run_track_a.py --image path/to/invoice.jpg --lang vi
"""

import argparse
from pathlib import Path
from docai.pipelines.track_a import LayoutDetector, OCRExtractor, LayoutLMv3Extractor


def main():
    parser = argparse.ArgumentParser(description="Chạy Track A (Classic Multi-stage) trên ảnh tài liệu")
    parser.add_argument("--image", type=str, required=True, help="Đường dẫn file ảnh tài liệu đầu vào")
    parser.add_argument("--lang", type=str, default="vi", choices=["vi", "en"], help="Ngôn ngữ OCR (mặc định: vi)")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Lỗi: Không tìm thấy file ảnh tại {image_path}")
        return

    print("==================================================")
    print("DOCAI TRACK A (CLASSIC PIPELINE) RUNNER")
    print("==================================================")
    print(f"File đầu vào: {image_path}")
    print(f"Ngôn ngữ: {args.lang}")

    detector = LayoutDetector()
    ocr = OCRExtractor(lang=args.lang)
    kie = LayoutLMv3Extractor()

    print("\nKhởi tạo các thành phần thành công:")
    print(f"- LayoutDetector: {detector.model_path}")
    print(f"- OCRExtractor: lang={ocr.lang}")
    print(f"- LayoutLMv3Extractor: checkpoint={kie.model_checkpoint}")
    print("\nLưu ý: Logic inference thực tế đang ở mức Scaffold (Giai đoạn 3-4).")


if __name__ == "__main__":
    main()
