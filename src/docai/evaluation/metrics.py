"""
Module tính toán chỉ số đánh giá thực nghiệm (Evaluation Metrics).

Thuộc: Giai đoạn 4, 5, 6, 9 (Đánh giá benchmark và so sánh 2 track).
Tham chiếu: docs/specs/implementation-guide.md và docs/specs/task-split.md.

Mục đích:
Cung cấp các công thức tính toán chỉ số khách quan:
- F1 field-level (Precision, Recall, F1)
- Agreement ratio (tỷ lệ đồng thuận giữa Track A và Track B)
- Latency (độ trễ và các thống kê phân bố hiện có; P90/P95 thuộc benchmark sau)
"""

from typing import Any, Dict, List
from docai.core.schema import UnifiedDocumentOutput
from docai.data.statistics import calculate_summary_statistics


def calculate_field_f1(
    predictions: List[Dict[str, str]],
    ground_truth: List[Dict[str, str]]
) -> Dict[str, float]:
    """
    Tính Precision, Recall và F1-score ở mức trường (Field-level).
    Một trường được coi là True Positive (TP) khi cả tên trường và giá trị chuẩn hoá khớp nhau.
    """
    if not ground_truth and not predictions:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0, "tp": 0, "fp": 0, "fn": 0}
    if not ground_truth:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "tp": 0, "fp": len(predictions), "fn": 0}
    if not predictions:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "tp": 0, "fp": 0, "fn": len(ground_truth)}

    pred_set = {(p.get("name", "").strip().lower(), p.get("value", "").strip().lower()) for p in predictions}
    gt_set = {(g.get("name", "").strip().lower(), g.get("value", "").strip().lower()) for g in ground_truth}

    tp = len(pred_set.intersection(gt_set))
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }


def calculate_field_agreement(
    doc_a: UnifiedDocumentOutput,
    doc_b: UnifiedDocumentOutput
) -> float:
    """
    Tính tỷ lệ đồng thuận (Agreement ratio) giữa hai output của Track A và Track B.
    """
    fields_a = {f.field_name.lower(): f.field_value.strip().lower() for f in doc_a.fields}
    fields_b = {f.field_name.lower(): f.field_value.strip().lower() for f in doc_b.fields}

    all_keys = set(fields_a.keys()).union(set(fields_b.keys()))
    if not all_keys:
        return 1.0

    matched = sum(1 for k in all_keys if k in fields_a and k in fields_b and fields_a[k] == fields_b[k])
    return round(matched / len(all_keys), 4)


def compute_latency_stats(latencies_ms: List[float]) -> Dict[str, float]:
    """
    Tính toán phân bố độ trễ suy luận.
    """
    return calculate_summary_statistics(latencies_ms)
