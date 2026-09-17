"""
Module chứa các processing backend chính của DocAI Document Intelligence Platform.

Bao gồm:
- track_a: Pipeline cổ điển đa tầng (Layout Detection + PaddleOCR + LayoutLMv3 KIE).
- track_b: Pipeline hiện đại đơn nhất (VLM-native: PaddleOCR-VL / dots.ocr).
"""
