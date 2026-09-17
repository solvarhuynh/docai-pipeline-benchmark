"""
Unit test kiểm tra động cơ luật gian lận và rủi ro (docai.fraud.rules).
"""

import unittest
from docai.core.schema import (
    DocumentType,
    ExtractedField,
    SeverityLevel,
    UnifiedDocumentOutput,
)
from docai.fraud.rules import FraudRiskEngine


class TestFraudRules(unittest.TestCase):
    """
    Kiểm tra logic phát hiện bất thường trong FraudRiskEngine.
    """

    def setUp(self):
        self.engine = FraudRiskEngine(arithmetic_tolerance=1.0)

    def test_invoice_math_matching(self):
        fields = [
            ExtractedField(field_name="subtotal_amount", field_value="1,000,000"),
            ExtractedField(field_name="tax_amount", field_value="100,000"),
            ExtractedField(field_name="total_amount", field_value="1,100,000"),
        ]
        flags = self.engine.check_invoice_math(fields)
        self.assertEqual(len(flags), 0, "Hóa đơn đúng số học không được sinh cờ cảnh báo")

    def test_invoice_math_mismatch(self):
        fields = [
            ExtractedField(field_name="subtotal_amount", field_value="1,000,000"),
            ExtractedField(field_name="tax_amount", field_value="100,000"),
            ExtractedField(field_name="total_amount", field_value="1,500,000"),  # Sai lệch 400,000
        ]
        flags = self.engine.check_invoice_math(fields)
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0].rule_id, "RULE_INVOICE_ARITHMETIC_MISMATCH")
        self.assertEqual(flags[0].severity, SeverityLevel.CRITICAL)

    def test_invoice_missing_total(self):
        fields = [
            ExtractedField(field_name="seller_name", field_value="CONG TY A"),
        ]
        flags = self.engine.check_invoice_math(fields)
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0].rule_id, "RULE_INVOICE_MISSING_TOTAL")

    def test_ocr_confidence_anomaly(self):
        fields = [
            ExtractedField(field_name="seller_name", field_value="CONG TY A", confidence=0.98),
            ExtractedField(field_name="total_amount", field_value="5,000,000", confidence=0.35),
        ]
        flags = self.engine.check_ocr_confidence_anomalies(fields, threshold=0.5)
        self.assertEqual(len(flags), 1)
        self.assertEqual(flags[0].rule_id, "RULE_OCR_CONFIDENCE_ANOMALY")

    def test_contract_missing_mandatory_clauses(self):
        fields = [
            ExtractedField(field_name="parties", field_value="Ben A va Ben B"),
            # Thiếu governing_law, termination_clause, dispute_resolution
        ]
        flags = self.engine.check_contract_clauses(fields)
        self.assertEqual(len(flags), 3)
        rule_ids = [f.rule_id for f in flags]
        self.assertIn("RULE_CONTRACT_MISSING_GOVERNING_LAW", rule_ids)
        self.assertIn("RULE_CONTRACT_MISSING_TERMINATION_CLAUSE", rule_ids)
        self.assertIn("RULE_CONTRACT_MISSING_DISPUTE_RESOLUTION", rule_ids)


if __name__ == "__main__":
    unittest.main()
