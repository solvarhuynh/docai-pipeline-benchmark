"""
Track B: Pipeline hiện đại đơn nhất (VLM-native Single-pass Pipeline).

Sử dụng Vision-Language Model đa phương thức (PaddleOCR-VL / dots.ocr) để đọc chữ
và hiểu cấu trúc trong một lượt suy luận duy nhất thông qua schema prompt định sẵn.
"""

from docai.pipelines.track_b.vlm_parser import VLMDocumentParser

__all__ = [
    "VLMDocumentParser",
]
