"""
Unit test kiểm tra tính toàn vẹn và xác thực của JSON schema (docai.core.schema).
"""

import unittest
from pydantic import ValidationError

from docai.core.schema import (
    BoundingBox,
    DocumentType,
    ExtractedField,
    RiskFlag,
    SeverityLevel,
    UnifiedDocumentOutput,
)


class TestSchemaModels(unittest.TestCase):
    """
    Kiểm tra các Pydantic models trong docai.core.schema.
    """

    def test_bounding_box_valid(self):
        bbox = BoundingBox(xmin=10.0, ymin=20.0, xmax=100.0, ymax=200.0, normalized=False)
        self.assertEqual(bbox.xmin, 10.0)
        self.assertEqual(bbox.ymin, 20.0)
        self.assertEqual(bbox.xmax, 100.0)
        self.assertEqual(bbox.ymax, 200.0)
        self.assertFalse(bbox.normalized)

    def test_normalized_bounding_box_range(self):
        with self.assertRaises(ValidationError):
            BoundingBox(xmin=0.0, ymin=0.0, xmax=1.1, ymax=1.0, normalized=True)

    def test_bounding_box_invalid_coords(self):
        # xmin > xmax phải báo lỗi
        with self.assertRaises(ValidationError):
            BoundingBox(xmin=150.0, ymin=20.0, xmax=100.0, ymax=200.0)

        # ymin > ymax phải báo lỗi
        with self.assertRaises(ValidationError):
            BoundingBox(xmin=10.0, ymin=250.0, xmax=100.0, ymax=200.0)

    def test_extracted_field_creation(self):
        field = ExtractedField(
            field_name="total_amount",
            field_value="1,500,000 VND",
            confidence=0.95
        )
        self.assertEqual(field.field_name, "total_amount")
        self.assertEqual(field.field_value, "1,500,000 VND")
        self.assertEqual(field.confidence, 0.95)
        self.assertEqual(field.page_number, 1)

    def test_extracted_field_confidence_range(self):
        # Confidence > 1.0 phải báo lỗi
        with self.assertRaises(ValidationError):
            ExtractedField(field_name="test", field_value="val", confidence=1.5)

        # Confidence < 0.0 phải báo lỗi
        with self.assertRaises(ValidationError):
            ExtractedField(field_name="test", field_value="val", confidence=-0.1)

    def test_risk_flag_creation(self):
        flag = RiskFlag(
            rule_id="RULE_TEST",
            rule_name="Kiểm tra mẫu",
            severity=SeverityLevel.HIGH,
            description="Mô tả cảnh báo"
        )
        self.assertEqual(flag.rule_id, "RULE_TEST")
        self.assertEqual(flag.severity, SeverityLevel.HIGH)

    def test_unified_document_output_serialization(self):
        doc = UnifiedDocumentOutput(
            document_type=DocumentType.INVOICE,
            fields=[
                ExtractedField(field_name="seller_name", field_value="CONG TY A", confidence=0.99)
            ],
            overall_confidence=0.99,
            pipeline_track="track_a_classic"
        )
        data = doc.model_dump()
        self.assertEqual(data["document_type"], "invoice")
        self.assertEqual(len(data["fields"]), 1)
        self.assertEqual(data["fields"][0]["field_name"], "seller_name")
        self.assertEqual(data["pipeline_track"], "track_a_classic")


if __name__ == "__main__":
    unittest.main()
