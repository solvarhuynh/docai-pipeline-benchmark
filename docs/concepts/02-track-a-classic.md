# Why does Track A split document processing into several specialist steps?

Track A is the classic, multi-stage processing engine. It is one backend option inside DocAI, not a separate product and not necessarily one model. It can support both Invoice Intelligence and Contract Intelligence, although each domain needs its own labels and field/clause mapping.

## What problem is Track A solving?

An invoice is not just a sentence. A contract is not just a long text file. Meaning depends on both the words and where those words appear. On an invoice, `Total` is usually related to a number beside it. In a contract, a clause may be identified by its heading, page location and surrounding text.

Track A makes those clues explicit by passing the document through focused steps:

```text
Document image or rendered PDF
        ↓
Layout Detection: find useful regions
        ↓
OCR: read text and its locations
        ↓
Document Understanding / KIE: assign business meaning
        ↓
Domain mapping: invoice fields or contract clauses
        ↓
UnifiedDocumentOutput
```

The advantage is observability. If `total_amount` is missing, an engineer can ask whether the total region was missed, the text was read incorrectly, or the right text received the wrong business label.

The disadvantage is an **error cascade**: a later step cannot recover information that an earlier step discarded. This is why each boundary must be inspectable and why evaluation should measure stages as well as the final result.

## Why find the layout before reading every word?

**Layout Detection** is the task of locating and classifying page regions. Imagine looking at a newspaper before reading it: you first notice the headline, columns, image and advertisement. A document layout model does something similar with regions such as `header`, `table`, `seller_info`, `signature` or `total`.

The result is a **bounding box**, a rectangle described by `[xmin, ymin, xmax, ymax]`. It tells the next step where a region is, not what the region means in full.

Models in the YOLO family, such as YOLOv8-doc or DocLayout-YOLO, are candidates for this job. **Non-Maximum Suppression (NMS)** removes overlapping duplicate boxes when several predictions point to the same region. **IoU (Intersection over Union)** is the overlap ratio used to compare two boxes:

```text
IoU = area shared by both boxes / area covered by either box
```

The repository interface is [`layout_detection.py`](../../src/docai/pipelines/track_a/layout_detection.py). The implementation is currently `SCAFFOLD`; no checkpoint has been selected.

## Why does OCR need both text and coordinates?

**OCR (Optical Character Recognition)** turns pixels into characters. If a phone photo contains `Total: 500.000đ`, the computer initially sees colors and shapes; OCR produces text that later steps can search and classify.

Modern OCR normally has two jobs:

1. **Text detection** finds each word or line in the image.
2. **Text recognition** converts each detected crop into Unicode text.

OCR therefore returns more than a string. It returns text, a confidence value and a polygon or box showing where that text was found. A polygon can be converted to a rectangle by taking the minimum and maximum x/y coordinates. The helper [`convert_polygon_to_box`](../../src/docai/pipelines/track_a/ocr_extraction.py) represents this boundary conversion.

The pipeline can also perform a spatial join: if an OCR token lies inside the layout box for `table`, it receives that region as context. This helps the understanding step distinguish a table amount from a total amount.

The repository interface is [`ocr_extraction.py`](../../src/docai/pipelines/track_a/ocr_extraction.py), currently `SCAFFOLD`.

## Why is OCR still not enough?

OCR might return these tokens:

```text
"Total"       at [100, 800, 150, 820]
"amount"      at [160, 800, 210, 820]
"1,500,000"   at [500, 800, 620, 820]
```

The text is readable, but software still needs to know whether the number is a total, tax, subtotal or account number. **KIE (Key Information Extraction)** assigns business meaning to pieces of text. For a contract, the equivalent output may be a termination clause, renewal clause or payment clause rather than a numeric field.

## Why does LayoutLMv3 use text, layout and image together?

A text-only model reads a sequence. It may know the words `Total amount`, but it does not naturally know that `1,500,000` is positioned to the right on the same row. **LayoutLMv3** is a **Transformer**, a model architecture that lets each input piece compare its context with other pieces. It combines three kinds of input:

```text
text tokens       → words or subwords from OCR
2D bounding boxes → where each token appears
visual patches    → small pieces of the page image
```

A **token** is a small unit the model processes; one word can become one or several tokens. An **embedding** is a numeric representation of a token or image patch. You can think of it as placing an item on a map of meaning so related items have useful relationships for the model.

**Attention** is the mechanism that decides which other inputs deserve more influence for the current prediction. On an invoice, the amount may attend to the nearby `Total` label and the same-row layout. Attention is an internal signal, not automatically a human-proof explanation.

LayoutLM-style models commonly normalize pixel coordinates to `[0, 1000]` before processing them. That is an internal model convention; the shared DocAI schema can still retain normalized `[0, 1]` boxes or absolute pixel boxes according to its `normalized` flag.

## How does the model represent multi-word fields?

KIE often uses **BIO tagging** so a field with several tokens has a clear start:

- `B-SELLER` begins a seller name.
- `I-SELLER` continues that same seller name.
- `O` means the token is outside the fields being extracted.

For example, `ABC Technology Joint Stock Company` can be tagged `B-SELLER I-SELLER I-SELLER I-SELLER`. An aggregation step joins consecutive pieces and computes one union bounding box for the complete field.

The KIE interface is [`kie_layoutlmv3.py`](../../src/docai/pipelines/track_a/kie_layoutlmv3.py), currently `SCAFFOLD`. A **pretrained model** is a model that has already learned general patterns from earlier data. **Fine-tuning** adapts it to a narrower task, such as invoice fields or contract clauses. A **checkpoint** is the saved model state used for inference. **Inference** means using that saved state on a new document. LayoutLMv3/Hugging Face are integration candidates; the project has not fine-tuned or selected a production checkpoint in this task.

## Why can Invoice and Contract use different specialists?

A Track is like a hospital, not one doctor:

```text
Track A
├─ layout specialist
├─ OCR specialist
├─ invoice KIE specialist
└─ contract/clause specialist
```

An invoice specialist learns fields such as seller, date, tax and total. A contract specialist needs clause spans, headings, page context and a legal-domain taxonomy. One model may eventually serve both, but the architecture does not assume that it must.

## Where does Track A output go?

The final output is mapped to [`UnifiedDocumentOutput`](../../src/docai/core/schema.py), then passed to FastAPI, risk rules and the React UI. The shared output contains fields, confidence, evidence boxes, risk flags, timing and metadata. This contract lets Product Engineering consume either Track A or Track B without copying model logic into TypeScript.

Track A is currently a pipeline interface and scaffold. Claims about accuracy require real inference, ground truth and an evaluation run.
