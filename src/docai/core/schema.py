"""
Module schema chuẩn hoá cho toàn bộ pipeline DocAI Dual-Pipeline Benchmark.

Thuộc: Giai đoạn 1 (Khảo sát và chuẩn bị dữ liệu thật) và Giai đoạn 7 (Fraud/Risk Engine).
Nhiệm vụ: Định nghĩa khung Pydantic model cho JSON schema thống nhất để cả Track A (Classic)
và Track B (VLM-native) đều trả về cùng một định dạng dữ liệu chuẩn hoá trên cả hai loại tài liệu
(hóa đơn/biên lai và hợp đồng pháp lý).

Các thành phần bắt buộc:
- document_type: loại tài liệu (invoice, receipt, contract, unknown)
- fields: danh sách các trường trích xuất (tên, giá trị, confidence, bounding box)
- confidence: độ tin cậy tổng thể hoặc theo trường
- bounding_box: tọa độ hộp giới hạn [xmin, ymin, xmax, ymax]
- risk_flags: danh sách cảnh báo gian lận hoặc rủi ro điều khoản từ Giai đoạn 7
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator


class DocumentType(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"
    CONTRACT = "contract"
    UNKNOWN = "unknown"


class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BoundingBox(BaseModel):
    """
    Tọa độ bounding box chuẩn hoá hoặc tọa độ pixel tuyệt đối.
    Thứ tự: [xmin, ymin, xmax, ymax].
    """
    xmin: float = Field(..., description="Tọa độ x nhỏ nhất")
    ymin: float = Field(..., description="Tọa độ y nhỏ nhất")
    xmax: float = Field(..., description="Tọa độ x lớn nhất")
    ymax: float = Field(..., description="Tọa độ y lớn nhất")
    normalized: bool = Field(default=False, description="True nếu tọa độ đã chuẩn hoá về khoảng [0, 1]")

    @model_validator(mode="after")
    def validate_coordinates(self) -> "BoundingBox":
        if self.xmin > self.xmax:
            raise ValueError(f"xmin ({self.xmin}) không thể lớn hơn xmax ({self.xmax})")
        if self.ymin > self.ymax:
            raise ValueError(f"ymin ({self.ymin}) không thể lớn hơn ymax ({self.ymax})")
        return self


class ExtractedField(BaseModel):
    """
    Thông tin của một trường được trích xuất từ tài liệu.
    """
    field_name: str = Field(..., description="Tên trường (ví dụ: total_amount, seller_name, termination_clause)")
    field_value: str = Field(..., description="Giá trị văn bản trích xuất được")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Độ tin cậy trích xuất [0.0, 1.0]")
    bounding_box: Optional[BoundingBox] = Field(default=None, description="Tọa độ hộp giới hạn trên ảnh")
    page_number: int = Field(default=1, ge=1, description="Trang chứa trường trích xuất")
    raw_text: Optional[str] = Field(default=None, description="Văn bản gốc trước khi chuẩn hoá")


class RiskFlag(BaseModel):
    """
    Cảnh báo rủi ro gian lận số liệu hoặc điều khoản bất thường (Giai đoạn 7).
    """
    rule_id: str = Field(..., description="Mã định danh luật kiểm tra (ví dụ: RULE_MATH_TOTAL_MISMATCH)")
    rule_name: str = Field(..., description="Tên mô tả luật kiểm tra")
    severity: SeverityLevel = Field(default=SeverityLevel.MEDIUM, description="Mức độ nghiêm trọng của rủi ro")
    description: str = Field(..., description="Mô tả chi tiết bất thường phát hiện được")
    target_field: Optional[str] = Field(default=None, description="Trường bị ảnh hưởng nếu có")


class UnifiedDocumentOutput(BaseModel):
    """
    JSON schema thống nhất đầu ra cho cả Track A và Track B trên cả hóa đơn và hợp đồng.
    """
    document_type: DocumentType = Field(..., description="Loại tài liệu đã xác định")
    fields: List[ExtractedField] = Field(default_factory=list, description="Danh sách trường đã trích xuất")
    overall_confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Độ tin cậy tổng thể của kết quả")
    risk_flags: List[RiskFlag] = Field(default_factory=list, description="Danh sách các cảnh báo rủi ro / gian lận")
    execution_time_ms: Optional[float] = Field(default=None, description="Thời gian thực thi tính bằng mili giây")
    pipeline_track: Optional[str] = Field(default=None, description="Nhánh pipeline xử lý: 'track_a_classic' hoặc 'track_b_vlm'")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Thông tin phụ (kích thước ảnh, model checkpoint, v.v.)")
