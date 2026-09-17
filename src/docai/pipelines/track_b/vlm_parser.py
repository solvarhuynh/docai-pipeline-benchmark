"""
Module VLM-native parser (Track B - Single pass) cho Product và Research layer của DocAI.

Thuộc: Giai đoạn 5 (Track B: VLM-native parsing - hóa đơn) và Giai đoạn 6 (Mở rộng Hợp đồng).
Tham chiếu: docs/specs/implementation-guide.md và docs/tasks/task-split.md, Giai đoạn 5.

Mục đích:
Sử dụng Vision-Language Model mã nguồn mở (PaddleOCR-VL hoặc dots.ocr) để đọc và trích xuất
toàn bộ thông tin tài liệu trong một lượt duy nhất (single pass) thông qua structured prompt,
sau đó ánh xạ trực tiếp kết quả vào JSON schema thống nhất (docai.core.schema).

Input mong đợi:
- image_input: Path hoặc PIL.Image của tài liệu.
- document_type: DocumentType (hóa đơn hoặc hợp đồng).
- prompt_template: Optional[str] - prompt ép kiểu JSON.

Output mong đợi:
- Đối tượng UnifiedDocumentOutput chứa các trường dữ liệu, độ tin cậy và thời gian suy luận.

TODO chi tiết:
1. Tích hợp pipeline gọi PaddleOCR-VL / dots.ocr qua API local hoặc Modal Serverless endpoint.
2. Thiết kế và tinh chỉnh cấu trúc prompt (zero-shot/few-shot) để ép VLM trả về đúng JSON keys.
3. Xử lý hậu kỳ (post-processing): parse chuỗi JSON từ text sinh ra của VLM, xử lý lỗi cú pháp (JSON repair).
4. Ánh xạ dữ liệu vào Pydantic model `UnifiedDocumentOutput`.
5. Đo lường latency (giây/trang), F1-score và tỷ lệ ảo giác (hallucination) so với ground truth.
6. Mở rộng thử nghiệm zero-shot trên hợp đồng CUAD ở Giai đoạn 6 để đo độ giảm F1 (generalization drop).
"""

from pathlib import Path
from typing import Any, Union
from PIL import Image

from docai.core.schema import DocumentType, UnifiedDocumentOutput


class VLMDocumentParser:
    """
    Trình phân tích tài liệu sử dụng Vision-Language Model (Track B - Single pass).
    """

    def __init__(self, model_name: str = "PaddleOCR-VL"):
        self.model_name = model_name
        self.endpoint_url = None
        # TODO: Giai đoạn 5 - Cấu hình endpoint Modal hoặc local model runner

    def build_prompt(self, document_type: DocumentType) -> str:
        """
        Tạo prompt định hướng để ép VLM trả về JSON đúng schema.
        """
        if document_type == DocumentType.INVOICE:
            return (
                "You are an expert Document AI system. Extract information from this invoice into valid JSON with fields: "
                "seller_name, invoice_date, total_amount, tax_amount, line_items. Do not hallucinate."
            )
        elif document_type == DocumentType.CONTRACT:
            return (
                "You are a legal AI assistant. Extract key clauses from this contract into valid JSON: "
                "parties, agreement_date, governing_law, termination_clause, payment_terms. Do not hallucinate."
            )
        return "Extract all key information from this document into valid structured JSON."

    def parse(
        self,
        image_input: Union[str, Path, Image.Image],
        document_type: DocumentType = DocumentType.INVOICE
    ) -> UnifiedDocumentOutput:
        """
        Thực hiện suy luận end-to-end từ ảnh sang UnifiedDocumentOutput.

        Args:
            image_input: Đường dẫn file ảnh hoặc đối tượng PIL Image.
            document_type: Loại tài liệu cần phân tích.

        Returns:
            UnifiedDocumentOutput chuẩn hoá.
        """
        # TODO: Giai đoạn 5 - Triển khai gọi VLM và parse JSON response
        raise NotImplementedError("TODO: Giai đoạn 5 - Chạy mô hình VLM-native (PaddleOCR-VL/dots.ocr)")

    def parse_raw_json_to_output(
        self,
        raw_json_str: str,
        document_type: DocumentType,
        latency_ms: float
    ) -> UnifiedDocumentOutput:
        """
        Hàm tiện ích chuyển chuỗi JSON thô từ VLM thành UnifiedDocumentOutput.
        """
        # TODO: Giai đoạn 5 - Parse JSON, validate qua Pydantic và gắn cờ cảnh báo nếu trích xuất lỗi
        raise NotImplementedError("TODO: Giai đoạn 5 - Ánh xạ raw JSON của VLM vào UnifiedDocumentOutput")
