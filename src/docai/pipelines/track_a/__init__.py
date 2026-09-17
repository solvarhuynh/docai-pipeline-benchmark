"""
Track A: Pipeline cổ điển đa tầng (Classic Multi-stage Pipeline).

Bao gồm 3 bước độc lập:
1. Layout Detection (YOLOv8-doc / DocLayout-YOLO)
2. OCR Extraction (PaddleOCR)
3. Key Information Extraction (LayoutLMv3 fine-tuned)
"""

from docai.pipelines.track_a.kie_layoutlmv3 import LayoutLMv3Extractor
from docai.pipelines.track_a.layout_detection import LayoutDetector
from docai.pipelines.track_a.ocr_extraction import OCRExtractor

__all__ = [
    "LayoutDetector",
    "LayoutLMv3Extractor",
    "OCRExtractor",
]
