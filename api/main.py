"""
FastAPI Service cho hệ thống DocAI Dual-Pipeline Benchmark.

Thuộc: Giai đoạn 10 (FastAPI Service & Tài liệu hoá).
Tham chiếu: implementation-guide.md, Giai đoạn 10; task-split.md, Giai đoạn 10.

Mục đích:
Cung cấp các REST API endpoint để đưa vào sử dụng thực tế hoặc kiểm thử local:
- POST /parse/classic: Xử lý tài liệu bằng Track A (YOLO + PaddleOCR + LayoutLMv3)
- POST /parse/vlm: Xử lý tài liệu bằng Track B (VLM-native: PaddleOCR-VL / dots.ocr)
- POST /compare: Chạy đồng thời cả 2 track, trả về kết quả đối chiếu song song
- POST /explain: Trả về bản đồ nhiệt chú ý (heatmap overlay) giải thích trường trích xuất
"""

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel

from shared.schema import DocumentType, UnifiedDocumentOutput

app = FastAPI(
    title="DocAI Dual-Pipeline Benchmark API",
    version="1.0.0",
    description="API so sánh pipeline Document AI cổ điển (Track A) và VLM-native (Track B) trên hóa đơn và hợp đồng."
)


class CompareResponse(BaseModel):
    """
    Schema phản hồi so sánh song song hai pipeline.
    """
    document_type: DocumentType
    track_a_classic: UnifiedDocumentOutput
    track_b_vlm: UnifiedDocumentOutput
    latency_difference_ms: float
    field_agreement_ratio: float
    summary: str


@app.get("/health", tags=["System"])
async def health_check():
    """
    Kiểm tra trạng thái hoạt động của hệ thống.
    """
    return {"status": "ok", "service": "docai-dual-pipeline-benchmark"}


@app.post(
    "/parse/classic",
    response_model=UnifiedDocumentOutput,
    tags=["Parsing"],
    summary="Phân tích tài liệu sử dụng Track A (Classic Multi-stage Pipeline)"
)
async def parse_classic(
    file: UploadFile = File(..., description="File ảnh hóa đơn hoặc hợp đồng"),
    document_type: DocumentType = Form(default=DocumentType.INVOICE)
):
    """
    Endpoint chạy Track A: Layout Detection -> OCR -> KIE (LayoutLMv3) -> Fraud/Risk rules.
    """
    # TODO: Giai đoạn 10 - Tích hợp Track A: đọc file bytes -> LayoutDetector -> OCRExtractor -> LayoutLMv3Extractor -> FraudRiskEngine
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: Giai đoạn 10 - Handler /parse/classic chưa được kích hoạt logic thực thi."
    )


@app.post(
    "/parse/vlm",
    response_model=UnifiedDocumentOutput,
    tags=["Parsing"],
    summary="Phân tích tài liệu sử dụng Track B (VLM-native Single-pass Pipeline)"
)
async def parse_vlm(
    file: UploadFile = File(..., description="File ảnh hóa đơn hoặc hợp đồng"),
    document_type: DocumentType = Form(default=DocumentType.INVOICE)
):
    """
    Endpoint chạy Track B: VLM-native parser (PaddleOCR-VL / dots.ocr) -> Fraud/Risk rules.
    """
    # TODO: Giai đoạn 10 - Tích hợp Track B: đọc file bytes -> VLMDocumentParser -> FraudRiskEngine
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: Giai đoạn 10 - Handler /parse/vlm chưa được kích hoạt logic thực thi."
    )


@app.post(
    "/compare",
    response_model=CompareResponse,
    tags=["Benchmark"],
    summary="Chạy song song Track A và Track B và trả về kết quả đối chiếu"
)
async def compare_pipelines(
    file: UploadFile = File(..., description="File ảnh tài liệu cần đối chiếu"),
    document_type: DocumentType = Form(default=DocumentType.INVOICE)
):
    """
    Endpoint chạy đồng thời cả hai track, đánh giá độ đồng thuận giữa các trường và so sánh thời gian suy luận.
    """
    # TODO: Giai đoạn 10 - Gọi parse_classic và parse_vlm đồng thời bằng asyncio.gather, tính tỷ lệ đồng thuận
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: Giai đoạn 10 - Handler /compare chưa được kích hoạt logic thực thi."
    )


@app.post(
    "/explain",
    tags=["Explainability"],
    summary="Tạo bản đồ nhiệt chú ý (heatmap overlay) giải thích vùng ảnh trích xuất"
)
async def explain_field(
    file: UploadFile = File(..., description="File ảnh tài liệu gốc"),
    target_field: str = Form(..., description="Tên trường cần giải thích (ví dụ: total_amount)"),
    track: str = Form(default="track_a_classic", description="'track_a_classic' hoặc 'track_b_vlm'")
):
    """
    Endpoint trả về ảnh overlay heatmap hoặc tọa độ vùng chú ý (visual grounding / attention weights).
    """
    # TODO: Giai đoạn 10 - Tích hợp shared/explainability.py tạo ảnh heatmap overlay và trả về Response(media_type='image/png')
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="TODO: Giai đoạn 10 - Handler /explain chưa được kích hoạt logic thực thi."
    )
