"""
Module trích xuất chữ kèm bounding box (OCR Extraction) cho Track A - Classic Pipeline.

Thuộc: Giai đoạn 3 (Track A: Layout Detection & OCR - hóa đơn).
Tham chiếu: implementation-guide.md, Giai đoạn 3; task-split.md, Giai đoạn 3.

Mục đích:
Sử dụng PaddleOCR để đọc toàn bộ văn bản trên ảnh hóa đơn hoặc trên từng vùng layout đã được phân vùng,
trích xuất chữ kèm bounding box 4 điểm tọa độ. Kết hợp layout + OCR tạo thành JSON trung gian trước khi đưa vào KIE.

Input mong đợi:
- image_input: Path hoặc str trỏ tới file ảnh, hoặc np.ndarray.
- layout_regions: Optional[list[dict]] - các vùng đã phân loại từ LayoutDetector (header, table, v.v.).
- lang: str, ngôn ngữ OCR ('vi' cho mcocr2021, 'en' cho CORD/SROIE).

Output mong đợi:
- Danh sách các token văn bản kèm:
  - text: str (văn bản được nhận dạng)
  - confidence: float
  - bbox: [xmin, ymin, xmax, ymax]
  - layout_label: Optional[str] (nhãn layout tương ứng)
- Hoặc đối tượng JSON trung gian sẵn sàng ánh xạ sang schema tại docai.core.schema.

TODO chi tiết:
1. Khởi tạo PaddleOCR với hỗ trợ tiếng Việt ('vi') và tiếng Anh ('en').
2. Tính toán bounding box chuẩn hoá 2 điểm [xmin, ymin, xmax, ymax] từ polygon 4 điểm của PaddleOCR.
3. Ghép kết quả OCR với vùng layout (Spatial Join giữa OCR bbox và Layout bbox).
4. Xây dựng hàm `extract_text_and_boxes(image_input, layout_regions)`.
5. Tính toán tỷ lệ đọc đúng ký tự (CER/WER) trên tập ground truth và ghi vào docs/reports/benchmark-results.md.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import numpy as np


class OCRExtractor:
    """
    Trình trích xuất OCR dựa trên PaddleOCR.
    """

    def __init__(self, lang: str = "vi", use_angle_cls: bool = True):
        self.lang = lang
        self.use_angle_cls = use_angle_cls
        self.ocr_engine = None
        # TODO: Giai đoạn 3 - Khởi tạo PaddleOCR tại đây
        # from paddleocr import PaddleOCR
        # self.ocr_engine = PaddleOCR(use_angle_cls=self.use_angle_cls, lang=self.lang)

    def extract_text_and_boxes(
        self,
        image_input: Union[str, Path, np.ndarray],
        layout_regions: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Đọc chữ và tọa độ bounding box trên toàn bộ ảnh hoặc theo vùng layout.

        Args:
            image_input: Đường dẫn ảnh hoặc mảng numpy.
            layout_regions: Danh sách vùng phân bố bởi LayoutDetector nếu có.

        Returns:
            Danh sách token gồm text, confidence, bbox, layout_tag.
        """
        # TODO: Giai đoạn 3 - Triển khai trích xuất PaddleOCR
        raise NotImplementedError("TODO: Giai đoạn 3 - Chạy PaddleOCR và tạo JSON trung gian")

    def convert_polygon_to_box(self, polygon: List[List[float]]) -> List[float]:
        """
        Chuyển đổi 4 đỉnh polygon của PaddleOCR về dạng [xmin, ymin, xmax, ymax].
        """
        x_coords = [pt[0] for pt in polygon]
        y_coords = [pt[1] for pt in polygon]
        return [min(x_coords), min(y_coords), max(x_coords), max(y_coords)]
