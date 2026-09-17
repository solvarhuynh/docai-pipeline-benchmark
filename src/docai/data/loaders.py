"""
Module nạp và định vị dữ liệu (Data Loaders).

Thuộc: Giai đoạn 1 (Khảo sát và chuẩn bị dữ liệu thật).
Nhiệm vụ:
- Định vị thư mục của 4 bộ dataset (mcocr2021, CORD, SROIE, CUAD).
- Quét danh sách file ảnh và file nhãn thô từ thư mục data/raw/.
- Cung cấp interface chuẩn để notebook và scripts gọi mà không cần code trùng lặp.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from docai.core.config import settings

# Metadata định nghĩa 4 bộ dữ liệu chính
DATASET_METADATA: Dict[str, Dict[str, Any]] = {
    "mcocr2021": {
        "display_name": "mcocr2021 (Hóa đơn / Biên lai Việt Nam)",
        "document_type": "invoice",
        "description": "Ảnh chụp thật từ điện thoại, nhãn tiếng Việt, có góc nghiêng và mờ.",
        "expected_format": "images + csv/json annotations",
    },
    "cord": {
        "display_name": "CORD (Consolidated Receipt Dataset)",
        "document_type": "receipt",
        "description": "Biên lai chuẩn quốc tế, có ground truth phân cấp field-level.",
        "expected_format": "images + json annotations",
    },
    "sroie": {
        "display_name": "SROIE (ICDAR 2019 Receipt Dataset)",
        "document_type": "receipt",
        "description": "Hóa đơn quét scan, chuẩn đối chiếu OCR và trích xuất thông tin.",
        "expected_format": "images + txt annotations",
    },
    "cuad": {
        "display_name": "CUAD (Contract Understanding Atticus Dataset)",
        "document_type": "contract",
        "description": "510 hợp đồng pháp lý thật với 41 loại điều khoản do luật sư gán nhãn.",
        "expected_format": "pdf/txt/json SQuAD-style",
    },
}


def get_dataset_dir(dataset_name: str) -> Path:
    """
    Trả về đường dẫn thư mục thô của bộ dữ liệu chỉ định trong data/raw/.
    """
    name_normalized = dataset_name.strip().lower()
    return settings.raw_data_dir / name_normalized


def list_available_datasets() -> Dict[str, Dict[str, Any]]:
    """
    Liệt kê danh sách các bộ dữ liệu được hỗ trợ kèm trạng thái tồn tại trên ổ đĩa.
    """
    result: Dict[str, Dict[str, Any]] = {}
    for name, meta in DATASET_METADATA.items():
        dataset_path = get_dataset_dir(name)
        exists = dataset_path.is_dir()
        sample_count = len(list(dataset_path.glob("*.*"))) if exists else 0
        result[name] = {
            **meta,
            "path": str(dataset_path),
            "is_downloaded": exists and sample_count > 0,
            "file_count": sample_count,
        }
    return result


def scan_raw_samples(
    dataset_name: str,
    extensions: Optional[List[str]] = None
) -> List[Path]:
    """
    Quét danh sách các file mẫu trong thư mục data/raw/<dataset_name>.
    Mặc định quét các file ảnh (.jpg, .jpeg, .png, .pdf).
    """
    dataset_path = get_dataset_dir(dataset_name)
    if not dataset_path.is_dir():
        return []

    exts = extensions or [".jpg", ".jpeg", ".png", ".pdf", ".json", ".csv", ".txt"]
    exts_lower = {e.lower() for e in exts}

    samples: List[Path] = []
    for item in dataset_path.iterdir():
        if item.is_file() and item.suffix.lower() in exts_lower:
            samples.append(item)
    return sorted(samples)


def load_dataset_annotations(dataset_name: str) -> List[Dict[str, Any]]:
    """
    Đọc nhãn gốc của bộ dữ liệu (Stub interface cho Giai đoạn 1).
    """
    dataset_path = get_dataset_dir(dataset_name)
    if not dataset_path.is_dir():
        return []
    # TODO: Giai đoạn 1 - Hiện thực hoá parser nhãn cho từng format cụ thể (CSV, JSON, SQuAD-style)
    return []
