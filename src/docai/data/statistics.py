"""
Module thống kê số liệu dữ liệu (Statistics).

Thuộc: Giai đoạn 1 (Khảo sát và chuẩn bị dữ liệu thật).
Nhiệm vụ:
- Tính toán thống kê mô tả (min, max, mean, median, standard deviation) cho kích thước ảnh,
  độ dài văn bản và số lượng trường.
- Hỗ trợ báo cáo EDA cho cả notebook và scripts.
"""

import math
from typing import Any, Dict, List


def calculate_summary_statistics(values: List[float]) -> Dict[str, float]:
    """
    Tính toán các chỉ số thống kê mô tả cơ bản cho một danh sách số thực.
    """
    if not values:
        return {
            "count": 0,
            "min": 0.0,
            "max": 0.0,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
        }

    n = len(values)
    sorted_vals = sorted(values)
    val_min = sorted_vals[0]
    val_max = sorted_vals[-1]
    val_mean = sum(sorted_vals) / n

    if n % 2 == 1:
        val_median = sorted_vals[n // 2]
    else:
        val_median = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0

    variance = sum((x - val_mean) ** 2 for x in sorted_vals) / max(n - 1, 1)
    val_std = math.sqrt(variance)

    return {
        "count": n,
        "min": round(val_min, 4),
        "max": round(val_max, 4),
        "mean": round(val_mean, 4),
        "median": round(val_median, 4),
        "std": round(val_std, 4),
    }


def aggregate_resolution_distribution(metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Tổng hợp phân bố độ phân giải và tỷ lệ khung hình từ danh sách metadata ảnh.
    """
    widths = [m["width"] for m in metadata_list if m.get("is_valid") and "width" in m]
    heights = [m["height"] for m in metadata_list if m.get("is_valid") and "height" in m]
    aspect_ratios = [m["aspect_ratio"] for m in metadata_list if m.get("is_valid") and "aspect_ratio" in m]
    file_sizes_kb = [m["file_size_bytes"] / 1024.0 for m in metadata_list if "file_size_bytes" in m]

    return {
        "total_samples": len(metadata_list),
        "valid_samples": len(widths),
        "width_stats": calculate_summary_statistics(widths),
        "height_stats": calculate_summary_statistics(heights),
        "aspect_ratio_stats": calculate_summary_statistics(aspect_ratios),
        "file_size_kb_stats": calculate_summary_statistics(file_sizes_kb),
    }
