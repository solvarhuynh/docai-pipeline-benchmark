"""
Module Key Information Extraction (KIE) với LayoutLMv3 cho Track A - Classic Pipeline.

Thuộc: Giai đoạn 4 (Track A: Fine-tune LayoutLMv3 cho Invoice/Contract theo schema thực tế).
Tham chiếu: docs/specs/implementation-guide.md và docs/specs/task-split.md, Giai đoạn 4.

Mục đích:
Fine-tune mô hình LayoutLMv3 trên tập dữ liệu được phê duyệt (Invoice hoặc Contract, theo phase)
để trích xuất các trường thông tin chủ chốt (KIE) bằng token classification BIO tagging.
Sau đó thực hiện suy luận (inference) trên ảnh và tokens OCR đầu vào để trả về định dạng trường dữ liệu chuẩn.

Input mong đợi:
- image_input: Path hoặc PIL.Image của tài liệu.
- tokens: Danh sách các từ được tách từ OCR.
- boxes_1000: Tọa độ box chuẩn hoá về hệ quy chiếu [0, 1000].

Output mong đợi:
- Danh sách các dictionary chứa:
  - field_name: Tên trường (seller_name, date, total_amount, vat_amount, line_items)
  - field_value: Giá trị văn bản trích xuất
  - confidence: Độ tin cậy của từng trường
  - bounding_box: Box gộp của toàn bộ thực thể

TODO chi tiết:
1. Chuyển đổi nhãn và tọa độ box từ format mcocr2021/CORD sang LayoutLMv3Processor format (chuẩn hoá 0-1000).
2. Định nghĩa tập nhãn BIO: B-SELLER, I-SELLER, B-DATE, I-DATE, B-TOTAL, I-TOTAL, B-VAT, I-VAT, O.
3. Viết hàm train/fine-tune trên Modal GPU với learning rate thấp, lưu checkpoint ra Modal Volume.
4. Ghi rõ thời gian chạy và chi phí GPU-giờ vào log/progress-log.md và docs/reports/cost-analysis.md.
5. Xây dựng hàm `extract_fields(image_input, tokens, boxes_1000)`.
6. Tính F1 field-level trên tập test riêng bằng seqeval và cập nhật docs/reports/benchmark-results.md.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from PIL import Image


class LayoutLMv3Extractor:
    """
    Trình trích xuất KIE sử dụng LayoutLMv3 fine-tuned.
    """

    def __init__(self, model_checkpoint: Optional[str] = None):
        self.model_checkpoint = model_checkpoint or "microsoft/layoutlmv3-base"
        self.processor = None
        self.model = None
        # TODO: Giai đoạn 4 - Khởi tạo AutoProcessor và AutoModelForTokenClassification
        # from transformers import AutoProcessor, AutoModelForTokenClassification
        # self.processor = AutoProcessor.from_pretrained(self.model_checkpoint, apply_ocr=False)
        # self.model = AutoModelForTokenClassification.from_pretrained(self.model_checkpoint)

    def extract_fields(
        self,
        image_input: Union[str, Path, Image.Image],
        tokens: List[str],
        boxes_1000: List[List[int]]
    ) -> List[Dict[str, Any]]:
        """
        Dự đoán nhãn KIE cho từng token và gộp thành các thực thể hoàn chỉnh.

        Args:
            image_input: Ảnh gốc của tài liệu.
            tokens: Danh sách từ được tách từ OCR.
            boxes_1000: Tọa độ box chuẩn hoá về hệ quy chiếu [0, 1000].

        Returns:
            Danh sách các trường trích xuất kèm nhãn, giá trị text và box.
        """
        # TODO: Giai đoạn 4 - Triển khai suy luận LayoutLMv3 và gom nhóm thực thể (entity aggregation)
        raise NotImplementedError("TODO: Giai đoạn 4 - Chạy inference KIE với LayoutLMv3 fine-tuned")

    def run_finetuning(self, train_data_path: str, eval_data_path: str, output_dir: str):
        """
        Hàm fine-tune LayoutLMv3 trên subset hóa đơn.
        Chạy trên Modal GPU (A10G hoặc T4).
        """
        # TODO: Giai đoạn 4 - Script huấn luyện với HuggingFace Trainer
        raise NotImplementedError("TODO: Giai đoạn 4 - Huấn luyện LayoutLMv3 trên Modal GPU")
