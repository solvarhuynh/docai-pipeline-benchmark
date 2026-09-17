"""
Module phân vùng Layout (Layout Detection) cho Track A - Classic Pipeline.

Thuộc: Giai đoạn 3 (Track A: Layout Detection & OCR - hóa đơn).
Tham chiếu: implementation-guide.md, Giai đoạn 3; task-split.md, Giai đoạn 3.

Mục đích:
Sử dụng mô hình pretrained YOLOv8-doc hoặc DocLayout-YOLO để phân vùng các khu vực trong hóa đơn
(Header, Table, Signature, Text, Total, v.v.), không huấn luyện từ đầu.

Input mong đợi:
- image_input: Path hoặc str trỏ tới file ảnh hóa đơn (hoặc PIL.Image / np.ndarray).
- conf_threshold: float, ngưỡng độ tin cậy để lọc bounding box (mặc định: 0.25).

Output mong đợi:
- List các dictionary chứa:
  - box: [xmin, ymin, xmax, ymax]
  - label: str (ví dụ: 'header', 'table', 'signature', 'seller_info')
  - confidence: float

TODO chi tiết:
1. Load model pretrained DocLayout-YOLO / YOLOv8-doc từ Ultralytics hoặc HuggingFace.
2. Tinh chỉnh ngưỡng confidence và IoU NMS để tránh đè lặp box trên các hóa đơn nghiêng/mờ.
3. Hàm `detect(image_input, conf_threshold)`: thực hiện suy luận (inference).
4. Xử lý crop từng vùng đã phân loại để chuyển tiếp cho bước OCR (ocr_extraction.py).
5. Ghi nhận tỷ lệ phát hiện đúng vùng bảng vào docs/reports/benchmark-results.md.
"""

from pathlib import Path
from typing import Any, Dict, List, Union
import numpy as np


class LayoutDetector:
    """
    Trình phân vùng layout tài liệu dựa trên YOLOv8-doc / DocLayout-YOLO pretrained.
    """

    def __init__(self, model_path: str = "yolov8x-doc.pt", conf_threshold: float = 0.25):
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.model = None
        # TODO: Giai đoạn 3 - Khởi tạo mô hình Ultralytics YOLO tại đây
        # from ultralytics import YOLO
        # self.model = YOLO(self.model_path)

    def detect(self, image_input: Union[str, Path, np.ndarray]) -> List[Dict[str, Any]]:
        """
        Thực hiện phân vùng layout trên một ảnh.

        Args:
            image_input: Đường dẫn ảnh hoặc mảng numpy ảnh RGB.

        Returns:
            Danh sách các vùng phát hiện kèm tọa độ, nhãn và confidence.
        """
        # TODO: Giai đoạn 3 - Triển khai suy luận layout
        raise NotImplementedError("TODO: Giai đoạn 3 - Chạy pretrained YOLOv8-doc/DocLayout-YOLO")

    def filter_regions_by_type(self, detections: List[Dict[str, Any]], region_type: str) -> List[Dict[str, Any]]:
        """
        Lọc các vùng phân vùng theo nhãn mong muốn (ví dụ: table, header).
        """
        return [d for d in detections if d.get("label") == region_type]
