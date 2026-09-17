"""
Pytest configuration và fixtures dùng chung cho test suite.
"""

from docai.core.schema import (
    BoundingBox,
    DocumentType,
    ExtractedField,
    UnifiedDocumentOutput,
)


def sample_invoice_output() -> UnifiedDocumentOutput:
    """
    Fixture tạo mẫu UnifiedDocumentOutput cho hóa đơn.
    """
    return UnifiedDocumentOutput(
        document_type=DocumentType.INVOICE,
        fields=[
            ExtractedField(
                field_name="seller_name",
                field_value="CONG TY TNHH ABC",
                confidence=0.98,
                bounding_box=BoundingBox(xmin=10.0, ymin=20.0, xmax=200.0, ymax=50.0)
            ),
            ExtractedField(
                field_name="subtotal_amount",
                field_value="1000000",
                confidence=0.95
            ),
            ExtractedField(
                field_name="tax_amount",
                field_value="100000",
                confidence=0.95
            ),
            ExtractedField(
                field_name="total_amount",
                field_value="1100000",
                confidence=0.96
            ),
        ],
        overall_confidence=0.96,
        pipeline_track="track_a_classic"
    )
