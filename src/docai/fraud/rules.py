"""
Module động cơ kiểm tra gian lận và cảnh báo rủi ro (Fraud & Risk Engine).

Thuộc: Giai đoạn 7 (Fraud/Risk Engine).
Tham chiếu: implementation-guide.md, Giai đoạn 7; task-split.md, Giai đoạn 7.

Mục đích:
Kết hợp AI trích xuất với luật logic nghiệp vụ để phát hiện rủi ro:
1. Với Hóa đơn:
   - Rule đối chiếu số học: Tổng tiền trước thuế (subtotal) + Tiền thuế VAT (tax) == Tổng thanh toán (total).
   - Rule phát hiện bất thường độ tin cậy OCR (OCR confidence anomaly): Phát hiện các số bị sửa/tẩy xóa
     (ví dụ: số 8 có confidence 0.4 trong khi các chữ xung quanh đạt 0.95).
2. Với Hợp đồng:
   - Clause-risk flagging: Tự động cảnh báo khi hợp đồng thiếu các điều khoản chuẩn bắt buộc
     (Governing Law, Termination, Dispute Resolution) hoặc có điều khoản bất thường dựa trên taxonomy CUAD.

TODO chi tiết:
1. Viết hàm chuẩn hoá số tiền từ chuỗi (loại bỏ dấu chấm, phẩy, ký hiệu tiền tệ VND/USD) thành float.
2. Viết hàm kiểm tra đối chiếu số học với ngưỡng dung sai làm tròn (tolerance: +-1000 VND hoặc +-0.01 USD).
3. Định nghĩa danh mục taxonomy 41 loại điều khoản của CUAD và danh sách điều khoản bắt buộc / rủi ro cao.
4. Xây dựng hàm tổng `run(doc: UnifiedDocumentOutput) -> list[RiskFlag]`.
5. Viết unit test kiểm thử với 1 hóa đơn cố tình sai số liệu và 1 hợp đồng cố tình thiếu điều khoản.
"""

from typing import List
from docai.core.schema import DocumentType, ExtractedField, RiskFlag, SeverityLevel, UnifiedDocumentOutput


class FraudRiskEngine:
    """
    Engine kiểm tra gian lận số liệu hóa đơn và rủi ro điều khoản hợp đồng.
    """

    MANDATORY_CONTRACT_CLAUSES = [
        "governing_law",
        "termination_clause",
        "dispute_resolution",
    ]

    def __init__(self, arithmetic_tolerance: float = 1.0):
        self.arithmetic_tolerance = arithmetic_tolerance

    def check_invoice_math(self, fields: List[ExtractedField]) -> List[RiskFlag]:
        """
        Kiểm tra tính nhất quán số học: subtotal + tax == total.
        """
        field_dict = {f.field_name.lower(): f for f in fields}
        total = field_dict.get("total_amount")
        subtotal = field_dict.get("subtotal_amount")
        tax = field_dict.get("tax_amount")

        flags: List[RiskFlag] = []

        if not total:
            flags.append(RiskFlag(
                rule_id="RULE_INVOICE_MISSING_TOTAL",
                rule_name="Thiếu trường tổng tiền",
                severity=SeverityLevel.HIGH,
                description="Hóa đơn không trích xuất được trường tổng tiền thanh toán.",
                target_field="total_amount"
            ))
            return flags

        # Nếu có cả subtotal và tax thì tiến hành đối chiếu
        if subtotal and tax:
            try:
                val_subtotal = float(subtotal.field_value.replace(",", "").replace(".", "").replace("VND", "").strip())
                val_tax = float(tax.field_value.replace(",", "").replace(".", "").replace("VND", "").strip())
                val_total = float(total.field_value.replace(",", "").replace(".", "").replace("VND", "").strip())

                if abs((val_subtotal + val_tax) - val_total) > self.arithmetic_tolerance:
                    flags.append(RiskFlag(
                        rule_id="RULE_INVOICE_ARITHMETIC_MISMATCH",
                        rule_name="Sai lệch đối chiếu số học hóa đơn",
                        severity=SeverityLevel.CRITICAL,
                        description=f"Tổng tiền ({val_total}) không khớp với tổng tiền hàng ({val_subtotal}) + thuế ({val_tax}).",
                        target_field="total_amount"
                    ))
            except ValueError:
                flags.append(RiskFlag(
                    rule_id="RULE_INVOICE_NUMBER_PARSE_ERROR",
                    rule_name="Lỗi định dạng số liệu hóa đơn",
                    severity=SeverityLevel.MEDIUM,
                    description="Không thể chuyển đổi giá trị số tiền thành dạng số để đối chiếu.",
                    target_field="total_amount"
                ))

        return flags

    def check_ocr_confidence_anomalies(self, fields: List[ExtractedField], threshold: float = 0.5) -> List[RiskFlag]:
        """
        Phát hiện các trường số liệu có độ tin cậy thấp bất thường (dấu hiệu chỉnh sửa).
        """
        flags: List[RiskFlag] = []
        for field in fields:
            if "amount" in field.field_name.lower() or "total" in field.field_name.lower():
                if field.confidence < threshold:
                    flags.append(RiskFlag(
                        rule_id="RULE_OCR_CONFIDENCE_ANOMALY",
                        rule_name="Độ tin cậy OCR vùng số liệu thấp bất thường",
                        severity=SeverityLevel.HIGH,
                        description=f"Trường '{field.field_name}' có độ tin cậy chỉ đạt {field.confidence:.2f} (dưới ngưỡng {threshold}).",
                        target_field=field.field_name
                    ))
        return flags

    def check_contract_clauses(self, fields: List[ExtractedField]) -> List[RiskFlag]:
        """
        Kiểm tra thiếu điều khoản bắt buộc trong hợp đồng pháp lý dựa trên CUAD.
        """
        flags: List[RiskFlag] = []
        present_clauses = {f.field_name.lower() for f in fields}

        for mandatory_clause in self.MANDATORY_CONTRACT_CLAUSES:
            if mandatory_clause not in present_clauses:
                flags.append(RiskFlag(
                    rule_id=f"RULE_CONTRACT_MISSING_{mandatory_clause.upper()}",
                    rule_name="Thiếu điều khoản bắt buộc trong hợp đồng",
                    severity=SeverityLevel.HIGH,
                    description=f"Hợp đồng không chứa điều khoản bắt buộc: '{mandatory_clause}'.",
                    target_field=mandatory_clause
                ))
        return flags

    def run(self, doc: UnifiedDocumentOutput) -> List[RiskFlag]:
        """
        Chạy toàn bộ các rule tương ứng với loại tài liệu của document.
        """
        flags: List[RiskFlag] = []
        if doc.document_type in [DocumentType.INVOICE, DocumentType.RECEIPT]:
            flags.extend(self.check_invoice_math(doc.fields))
            flags.extend(self.check_ocr_confidence_anomalies(doc.fields))
        elif doc.document_type == DocumentType.CONTRACT:
            flags.extend(self.check_contract_clauses(doc.fields))
        return flags
