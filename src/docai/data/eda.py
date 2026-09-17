"""
Module phân tích khám phá dữ liệu (Exploratory Data Analysis - EDA).

Thuộc: Giai đoạn 1 (Khảo sát và chuẩn bị dữ liệu thật).
Nhiệm vụ:
- Cung cấp các hàm phân tích cấu trúc bộ dữ liệu có thể tái sử dụng cho notebook và script CLI.
- Tổng hợp số lượng file, định dạng tệp và đánh giá sơ bộ độ sẵn sàng của dữ liệu.
"""

from typing import Any, Dict, List
from docai.data.loaders import DATASET_METADATA, get_dataset_dir, scan_raw_samples
from docai.data.preprocessing import load_image_metadata
from docai.data.statistics import aggregate_resolution_distribution


def summarize_dataset_structure(dataset_name: str) -> Dict[str, Any]:
    """
    Tóm tắt cấu trúc thư mục của một bộ dữ liệu cụ thể trong data/raw/.
    """
    dataset_path = get_dataset_dir(dataset_name)
    metadata = DATASET_METADATA.get(dataset_name.lower(), {})
    samples = scan_raw_samples(dataset_name)

    extensions_count: Dict[str, int] = {}
    for sample in samples:
        ext = sample.suffix.lower()
        extensions_count[ext] = extensions_count.get(ext, 0) + 1

    return {
        "dataset_name": dataset_name,
        "display_name": metadata.get("display_name", dataset_name),
        "document_type": metadata.get("document_type", "unknown"),
        "path": str(dataset_path),
        "exists": dataset_path.is_dir(),
        "total_files": len(samples),
        "extensions_breakdown": extensions_count,
        "is_ready_for_eda": len(samples) > 0,
    }


def analyze_dataset(dataset_name: str, max_samples: int = 50) -> Dict[str, Any]:
    """
    Thực hiện khảo sát phân tích một bộ dữ liệu:
    - Quét các file mẫu (tối đa max_samples file ảnh để tối ưu tốc độ).
    - Đo lường phân bố kích thước ảnh và tỷ lệ khung hình.
    """
    summary = summarize_dataset_structure(dataset_name)
    if not summary["is_ready_for_eda"]:
        return {
            **summary,
            "status": "DATASET_NOT_FOUND_OR_EMPTY",
            "message": f"Bộ dữ liệu '{dataset_name}' chưa có file trong thư mục raw. Vui lòng tải dữ liệu về ở Giai đoạn 1.",
            "resolution_analysis": {},
        }

    samples = scan_raw_samples(dataset_name, extensions=[".jpg", ".jpeg", ".png"])
    sample_subset = samples[:max_samples]

    metadata_list: List[Dict[str, Any]] = []
    for img_path in sample_subset:
        meta = load_image_metadata(img_path)
        metadata_list.append(meta)

    resolution_analysis = aggregate_resolution_distribution(metadata_list)

    return {
        **summary,
        "status": "ANALYZED",
        "sampled_images_count": len(sample_subset),
        "resolution_analysis": resolution_analysis,
    }
