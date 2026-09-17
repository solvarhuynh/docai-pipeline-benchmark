# Data dictionary: what does a DocAI result mean?

The data dictionary describes the contract shared by Track A, Track B, FastAPI and the React frontend. It is implemented as Pydantic models in [`src/docai/core/schema.py`](../../src/docai/core/schema.py) and mirrored as TypeScript interfaces in [`frontend/src/types/document.ts`](../../frontend/src/types/document.ts).

## The shared envelope

Both engines return `UnifiedDocumentOutput`. Think of it as a shipping box with a stable label: the contents differ between an invoice and a contract, but every consumer knows where to find the document type, extracted items, confidence and review flags.

| Field | Type | Meaning |
| --- | --- | --- |
| `document_type` | `invoice \| receipt \| contract \| unknown` | The kind of document being processed. |
| `fields` | array of `ExtractedField` | Extracted invoice fields or contract metadata/clause items. |
| `overall_confidence` | number from `0` to `1` | A pipeline-level confidence estimate. It is not proof of correctness. |
| `risk_flags` | array of `RiskFlag` | Domain-specific signals that deserve human review. |
| `execution_time_ms` | number or `null` | Measured processing time when available. |
| `pipeline_track` | string or `null` | The engine that produced the result. |
| `metadata` | JSON object | Additional trace information such as image size or checkpoint. |

An **API contract** is the agreement about this shape between software components. If it changes, backend and frontend consumers must be reviewed together.

## What is an extracted field?

`ExtractedField` represents one answer found in the source document. For an invoice, `field_name` might be `seller_name` or `total_amount`. For a contract, it might identify a clause or metadata value such as `termination_clause`.

| Field | Type | Meaning |
| --- | --- | --- |
| `field_name` | string | Stable business name, not a display sentence. |
| `field_value` | string | The normalized value shown to consumers. |
| `confidence` | number from `0` to `1` | Confidence for this item. |
| `bounding_box` | `BoundingBox` or `null` | Image location when available. |
| `page_number` | integer, at least `1` | Page containing the item. |
| `raw_text` | string or `null` | Original text before normalization. |

An invoice field can use a box around the printed number. A contract clause may instead need a page and supporting text; a box is optional because a text span is not always naturally represented by one image rectangle.

## How are locations represented?

`BoundingBox` stores `xmin`, `ymin`, `xmax` and `ymax`. The order is always top-left minimum coordinates followed by bottom-right maximum coordinates. `normalized: true` means each coordinate is in `[0, 1]`; `false` means absolute coordinates such as pixels.

LayoutLM-style model inputs may use a separate `[0, 1000]` convention. That internal representation must be converted at the boundary; consumers should follow the schema's `normalized` flag rather than guessing.

## What is a risk flag?

`RiskFlag` is a review signal, not a verdict. It contains a stable `rule_id`, a readable `rule_name`, a `severity`, a `description` and an optional `target_field`.

Invoice Risk can flag arithmetic inconsistency or low confidence. Contract Risk can flag a missing or unusual clause. The envelope uses one list so the UI can display flags consistently, while the rule implementation remains domain-specific. It does not mean Invoice and Contract fields must have the same taxonomy.

## How does data move through the system?

```text
model/pipeline output
  → Pydantic validation in Python
  → JSON response from FastAPI
  → matching TypeScript type
  → React rendering
```

The frontend must not read Python files or duplicate extraction logic. Empty lists, `null` values and scaffold responses must remain visible as such. The current parse endpoints return `501 Not Implemented`, so no real extraction result should be invented in the UI.
