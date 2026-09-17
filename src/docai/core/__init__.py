"""
Module lõi (Core) của hệ thống DocAI Benchmark.

Chứa cấu hình hệ thống (config) và hợp đồng schema Pydantic thống nhất (schema).
"""

from docai.core.config import Settings, settings
from docai.core.schema import (
    BoundingBox,
    DocumentType,
    ExtractedField,
    RiskFlag,
    UnifiedDocumentOutput,
)

__all__ = [
    "BoundingBox",
    "DocumentType",
    "ExtractedField",
    "RiskFlag",
    "Settings",
    "UnifiedDocumentOutput",
    "settings",
]
