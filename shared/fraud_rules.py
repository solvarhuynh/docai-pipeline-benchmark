"""
Module Fraud & Risk Detection Engine dùng chung.

Thuộc: Giai đoạn 7 (Fraud/Risk Engine).
Tham chiếu: implementation-guide.md, Giai đoạn 7; task-split.md, Giai đoạn 7.

Mục đích:
Kiểm tra và phát hiện các dấu hiệu bất thường, sai lệch số liệu trên hóa đơn hoặc rủi ro pháp lý trên hợp đồng.
Kết quả kiểm tra được trả về dưới dạng danh sách RiskFlag trong output thống nhất (shared/schema.py).

Các nhóm rule chính:
1. Nhóm luật Hóa đơn (Invoice Rules):
   - RULE_MATH_TOTAL_MISMATCH: Kiểm tra quan hệ toán học: Tổng tiền trước thuế + Tiền thuế (VAT) = Tổng thanh toán.
   - RULE_OCR_CONFIDENCE_ANOMALY: Phát hiện vùng số tiền có độ tin cậy OCR thấp bất thường so với trung bình tài liệu
     (dấu hiệu chỉnh sửa, tẩy xóa, chèn số).
2. Nhóm luật Hợp đồng (Contract Rules):
   - RULE_CONTRACT_MISSING_MANDATORY_CLAUSE: Phát hiện thiếu các điều khoản chuẩn bắt buộc (ví dụ: Governing Law, Termination).
   - RULE_CONTRACT_HIGH_RISK_CLAUSE: Đánh dấu các điều khoản có nguy cơ rủi ro cao dựa theo taxonomy CUAD
     (ví dụ: Unlimited Indemnification, Non-compete quá rộng, Unilateral Termination).

Input mong đợi:
- doc: UnifiedDocumentOutput chứa danh sách fields đã trích xuất từ Track A hoặc Track B.

Output mong đợi:
- List[RiskFlag]: Danh sách các cảnh báo rủi ro kèm mã rule_id, tên, mức độ nghiêm trọng và mô tả.

TODO chi tiết:
1. Xây dựng hàm phân tích và chuẩn hoá số tiền từ string sang float để đối chiếu toán học.
2. Xây dựng thuật toán phát hiện bất thường thống kê (statistical threshold) về độ tin cậy OCR tại vùng số tiền.
3. Định nghĩa danh mục taxonomy 41 loại điều khoản của CUAD và danh sách điều khoản bắt buộc / rủi ro cao.
4. Xây dựng hàm tổng `run(doc: UnifiedDocumentOutput) -> list[RiskFlag]`.
5. Viết unit test kiểm thử với 1 hóa đơn cố tình sai số liệu và 1 hợp đồng cố tình thiếu điều khoản.
"""

from typing import List
from shared.schema import DocumentType, ExtractedField, RiskFlag, UnifiedDocumentOutput


class FraudRiskEngine:
    """
    Engine kiểm tra gian lận số liệu hóa đơn và rủi ro điều khoản hợp đồng.
    """

    MANDATORY_CONTRACT_CLAUSES = [
        "governing_law",
        "termination",
        "confidentiality",
        "dispute_resolution"
    ]

    def __init__(self, confidence_anomaly_threshold: float = 0.35):
        self.confidence_anomaly_threshold = confidence_anomaly_threshold

    def evaluate_invoice(self, fields: List[ExtractedField], avg_confidence: float) -> List[RiskFlag]:
        """
        Kiểm tra các rule gian lận trên hóa đơn: đối chiếu số học và bất thường độ tin cậy OCR.
        """
        flags: List[RiskFlag] = []
        # TODO: Giai đoạn 7 - Triển khai tính toán: subtotal + vat == total
        # TODO: Giai đoạn 7 - So sánh confidence của số tiền với avg_confidence
        return flags

    def evaluate_contract(self, fields: List[ExtractedField]) -> List[RiskFlag]:
        """
        Kiểm tra các rule rủi ro trên hợp đồng: thiếu điều khoản chuẩn và điều khoản rủi ro cao.
        """
        flags: List[RiskFlag] = []
        # TODO: Giai đoạn 7 - Đối chiếu danh sách điều khoản trích xuất với MANDATORY_CONTRACT_CLAUSES
        # TODO: Giai đoạn 7 - Phát hiện các điều khoản rủi ro bất lợi
        return flags

    def run(self, doc: UnifiedDocumentOutput) -> List[RiskFlag]:
        """
        Thực thi toàn bộ tập rule tương ứng với loại tài liệu và trả về danh sách RiskFlag.
        """
        if doc.document_type in (DocumentType.INVOICE, DocumentType.RECEIPT):
            return self.evaluate_invoice(doc.fields, doc.overall_confidence)
        elif doc.document_type == DocumentType.CONTRACT:
            return self.evaluate_contract(doc.fields)
        return []
