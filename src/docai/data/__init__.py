"""
Module xử lý dữ liệu cho hệ thống DocAI Benchmark.

Cung cấp các hàm tải dữ liệu (loaders), tiền xử lý (preprocessing), thống kê (statistics)
và phân tích khám phá dữ liệu (eda) dùng chung cho cả notebook và scripts.
"""

from docai.data.eda import analyze_dataset, summarize_dataset_structure
from docai.data.loaders import get_dataset_dir, list_available_datasets, scan_raw_samples
from docai.data.preprocessing import load_image_metadata, normalize_bounding_box
from docai.data.statistics import calculate_summary_statistics

__all__ = [
    "analyze_dataset",
    "calculate_summary_statistics",
    "get_dataset_dir",
    "list_available_datasets",
    "load_image_metadata",
    "normalize_bounding_box",
    "scan_raw_samples",
    "summarize_dataset_structure",
]
