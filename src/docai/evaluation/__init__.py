"""
Module đánh giá và so sánh benchmark (Evaluation & Benchmark).

Cung cấp các công thức tính chỉ số thực nghiệm (metrics) và trình so sánh đối đầu giữa
Track A (Classic) và Track B (VLM-native).
"""

from docai.evaluation.benchmark import BenchmarkRunner
from docai.evaluation.metrics import (
    calculate_field_agreement,
    calculate_field_f1,
    compute_latency_stats,
)

__all__ = [
    "BenchmarkRunner",
    "calculate_field_agreement",
    "calculate_field_f1",
    "compute_latency_stats",
]
