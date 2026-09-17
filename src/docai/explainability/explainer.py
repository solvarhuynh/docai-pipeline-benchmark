"""
Module giải thích mô hình (Explainability Layer) cho DocAI Benchmark.

Thuộc: Giai đoạn 8 (Explainability Layer).
Tham chiếu: implementation-guide.md, Giai đoạn 8; task-split.md, Giai đoạn 8.

Mục đích:
Trang bị khả năng giải thích cho cả hai pipeline thay vì trả về JSON như hộp đen:
1. Với Track A (Classic): Trích attention weights từ LayoutLMv3 cho từng field đã dự đoán,
   ánh xạ về bounding box tương ứng trên ảnh gốc.
2. Với Track B (VLM): Trích visual grounding map từ VLM (nếu có hỗ trợ) hoặc sử dụng Grad-CAM trên ảnh gốc.
3. Vẽ overlay heatmap lên ảnh tài liệu gốc và lưu ảnh hoặc trả về qua endpoint /explain.

Input mong đợi:
- original_image: Path hoặc PIL.Image của tài liệu gốc.
- target_field: str (tên trường cần giải thích, ví dụ: 'total_amount').
- track_name: str ('track_a_classic' hoặc 'track_b_vlm').
- model_artifacts: Các thông số nội bộ của mô hình (attention weights, feature maps).

Output mong đợi:
- np.ndarray hoặc PIL.Image chứa overlay heatmap được áp lên ảnh gốc.
- Dict chứa thông tin tọa độ vùng tập trung chú ý cao nhất (hotspot bounding box).

TODO chi tiết:
1. Trích xuất attention matrix từ các layer cuối của LayoutLMv3 cho các token thuộc target_field.
2. Chuyển đổi token-level attention thành bounding box heatmap trên tọa độ pixel của ảnh gốc.
3. Triển khai Grad-CAM hoặc visual grounding attention cho VLM trong Track B.
4. Xây dựng hàm overlay: dùng OpenCV/PIL để blend bản đồ nhiệt (colormap JET) lên ảnh gốc với alpha = 0.5.
5. Tạo hàm `explain_field(original_image, field_name, track_name) -> tuple[Image, dict]`.
6. Lưu ảnh minh họa kết quả cho ít nhất 3 field mẫu vào docs/reports/explainability-report.md.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np
from PIL import Image


class DocumentExplainer:
    """
    Trình tạo overlay heatmap giải thích vùng ảnh mô hình dựa vào để trích xuất dữ liệu.
    """

    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha

    def extract_layoutlmv3_attention_map(
        self,
        attention_weights: Any,
        token_bboxes: list
    ) -> np.ndarray:
        """
        Trích attention từ LayoutLMv3 và tổng hợp thành 2D attention map trên ảnh.
        """
        # TODO: Giai đoạn 8 - Ánh xạ attention weights của các attention head sang 2D map
        raise NotImplementedError("TODO: Giai đoạn 8 - Trích xuất LayoutLMv3 attention")

    def extract_vlm_grounding_map(
        self,
        vlm_model: Any,
        image_input: Any,
        prompt_query: str
    ) -> np.ndarray:
        """
        Trích xuất visual grounding hoặc Grad-CAM từ VLM.
        """
        # TODO: Giai đoạn 8 - Visual grounding / Grad-CAM cho Track B
        raise NotImplementedError("TODO: Giai đoạn 8 - Trích xuất VLM visual grounding map")

    def overlay_heatmap_on_image(
        self,
        original_image: Union[str, Path, Image.Image],
        heatmap: np.ndarray
    ) -> Image.Image:
        """
        Trộn heatmap màu (JET) lên ảnh gốc với độ trong suốt alpha.
        """
        # TODO: Giai đoạn 8 - Sử dụng OpenCV để resize heatmap, áp colormap JET và cv2.addWeighted
        raise NotImplementedError("TODO: Giai đoạn 8 - Tạo ảnh overlay heatmap")

    def explain_field(
        self,
        original_image: Union[str, Path, Image.Image],
        field_name: str,
        track_name: str = "track_a_classic"
    ) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Hàm cấp cao tạo ảnh giải thích cho một trường dữ liệu cụ thể.
        """
        # TODO: Giai đoạn 8 - Điều phối trích xuất và tạo ảnh trả về cho endpoint /explain
        raise NotImplementedError("TODO: Giai đoạn 8 - Hàm tổng hợp tạo giải thích cho field")


# Alias tương thích tên cũ
DocumentExplainability = DocumentExplainer
