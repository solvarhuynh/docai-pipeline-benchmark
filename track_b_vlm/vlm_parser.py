"""
Module VLM-Native Document Parser cho Track B.

Thuộc: Giai đoạn 5 (Track B: VLM-native parsing - hóa đơn) và mở rộng sang Giai đoạn 6 (Hợp đồng CUAD).
Tham chiếu: implementation-guide.md, Giai đoạn 5; task-split.md, Giai đoạn 5.

Mục đích:
Sử dụng mô hình Vision-Language Model (VLM) pretrained như PaddleOCR-VL hoặc dots.ocr để đọc chữ và
hiểu layout trong một lượt duy nhất (single-pass end-to-end), không cần pipeline tách rời (Layout + OCR + KIE)
và không cần huấn luyện lại. Output được chuẩn hoá về JSON schema thống nhất (shared/schema.py).

Input mong đợi:
- image_input: Đường dẫn ảnh, PIL.Image hoặc bytes của tài liệu.
- document_type: DocumentType ('invoice', 'receipt' hoặc 'contract').
- custom_fields: Optional[list[str]] mô tả các trường cần trích xuất (seller_name, total_amount, v.v.).

Output mong đợi:
- UnifiedDocumentOutput (Pydantic model) chứa:
  - document_type: DocumentType
  - fields: List[ExtractedField] với field_name, field_value, confidence, bounding_box (nếu VLM hỗ trợ visual grounding)
  - execution_time_ms: Thời gian suy luận
  - metadata: Thông tin mô hình VLM đã dùng

TODO chi tiết:
1. Thiết kế system prompt và extraction schema JSON chuẩn để ép VLM trả về đúng định dạng mong muốn.
2. Tích hợp gọi model PaddleOCR-VL hoặc dots.ocr chạy trên Modal GPU serverless hoặc local.
3. Chạy evaluation trên cùng tập test của Giai đoạn 4 (mcocr2021 / CORD) để so sánh công bằng với Track A.
4. Đo lường latency, GPU-giờ, F1 field-level và ghi vào docs/reports/benchmark-results.md và docs/reports/cost-analysis.md.
5. Chuẩn bị mở rộng sang hợp đồng pháp lý CUAD ở Giai đoạn 6 bằng cách thay đổi prompt schema.
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from PIL import Image

from shared.schema import DocumentType, ExtractedField, UnifiedDocumentOutput


class VLMDocumentParser:
    """
    Trình phân tích tài liệu sử dụng Vision-Language Model (Track B - Single pass).
    """

    def __init__(self, model_name: str = "PaddleOCR-VL"):
        self.model_name = model_name
        self.client = None
        # TODO: Giai đoạn 5 - Khởi tạo VLM client hoặc weights tại đây

    def build_prompt(self, document_type: DocumentType, custom_fields: Optional[List[str]] = None) -> str:
        """
        Xây dựng prompt chỉ định các trường cần trích xuất theo loại tài liệu.
        """
        if document_type in (DocumentType.INVOICE, DocumentType.RECEIPT):
            fields_to_extract = custom_fields or [
                "seller_name", "invoice_date", "total_amount", "vat_amount", "line_items"
            ]
        elif document_type == DocumentType.CONTRACT:
            fields_to_extract = custom_fields or [
                "parties", "agreement_date", "termination_date", "governing_law", "indemnification"
            ]
        else:
            fields_to_extract = custom_fields or ["document_summary"]

        return (
            f"You are a document extraction engine. Extract the following fields from the document image "
            f"as strict JSON: {', '.join(fields_to_extract)}."
        )

    def parse(
        self,
        image_input: Union[str, Path, Image.Image],
        document_type: DocumentType = DocumentType.INVOICE
    ) -> UnifiedDocumentOutput:
        """
        Trích xuất thông tin tài liệu thông qua VLM.

        Args:
            image_input: File ảnh tài liệu hoặc PIL Image.
            document_type: Loại tài liệu (invoice, receipt, contract).

        Returns:
            UnifiedDocumentOutput theo JSON schema thống nhất.
        """
        start_time = time.time()
        # TODO: Giai đoạn 5 - Triển khai suy luận VLM (PaddleOCR-VL / dots.ocr)
        raise NotImplementedError("TODO: Giai đoạn 5 - Chạy inference VLM-native parser")
