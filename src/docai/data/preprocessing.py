"""
Module tiền xử lý dữ liệu và hình ảnh (Preprocessing).

Thuộc: Giai đoạn 1 (Khảo sát và chuẩn bị dữ liệu thật).
Nhiệm vụ:
- Chuẩn hoá kích thước và tọa độ bounding box về dải chuẩn [0, 1].
- Kiểm tra tính hợp lệ và trích xuất metadata của ảnh mà không cần nạp toàn bộ vào bộ nhớ.
"""

from pathlib import Path
from typing import Any, Dict, List
from PIL import Image


def load_image_metadata(image_path: Path) -> Dict[str, Any]:
    """
    Trích xuất thông tin kỹ thuật của file ảnh (kích thước, định dạng, dung lượng).
    """
    if not image_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file ảnh: {image_path}")

    file_size_bytes = image_path.stat().st_size
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            img_format = img.format or image_path.suffix.lstrip(".").upper()
            mode = img.mode
    except Exception as exc:
        return {
            "path": str(image_path),
            "file_size_bytes": file_size_bytes,
            "is_valid": False,
            "error": str(exc),
        }

    return {
        "path": str(image_path),
        "file_size_bytes": file_size_bytes,
        "width": width,
        "height": height,
        "aspect_ratio": round(width / max(height, 1), 4),
        "format": img_format,
        "mode": mode,
        "is_valid": True,
    }


def normalize_bounding_box(
    bbox: List[float],
    width: int,
    height: int
) -> List[float]:
    """
    Quy đổi tọa độ bounding box tuyệt đối [xmin, ymin, xmax, ymax] sang dải [0, 1].
    """
    if width <= 0 or height <= 0:
        raise ValueError(f"Chiều rộng ({width}) và chiều cao ({height}) phải lớn hơn 0")
    if len(bbox) != 4:
        raise ValueError(f"Bounding box phải có đúng 4 phần tử [xmin, ymin, xmax, ymax], nhận được {len(bbox)}")

    xmin, ymin, xmax, ymax = bbox
    return [
        max(0.0, min(1.0, xmin / width)),
        max(0.0, min(1.0, ymin / height)),
        max(0.0, min(1.0, xmax / width)),
        max(0.0, min(1.0, ymax / height)),
    ]


def denormalize_bounding_box(
    bbox: List[float],
    width: int,
    height: int
) -> List[int]:
    """
    Quy đổi tọa độ bounding box chuẩn hoá [0, 1] sang tọa độ pixel nguyên.
    """
    if len(bbox) != 4:
        raise ValueError("Bounding box phải có đúng 4 phần tử")

    xmin, ymin, xmax, ymax = bbox
    return [
        int(round(xmin * width)),
        int(round(ymin * height)),
        int(round(xmax * width)),
        int(round(ymax * height)),
    ]
