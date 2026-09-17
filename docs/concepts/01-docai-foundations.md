# 01. Why does DocAI need more than an image reader?

## What is the problem?

An invoice photo and a contract PDF are not structured database rows. A computer initially sees pixels, or a sequence of PDF objects, while a person sees labels, numbers, tables, paragraphs and relationships.

**Document AI** means software that reads documents and turns their visible content into useful information. It is closer to asking a careful office worker to read a document than to asking a normal image classifier whether a picture contains a cat.

- An Invoice contains fields such as seller, date, tax and total, often arranged in a table.
- A Contract contains metadata and clauses, where the relevant meaning may be spread across pages.

## What does the computer need to recover?

```text
pixels/PDF
  → layout regions
  → words and positions
  → fields or clauses
  → validated structured output
```

### Pixel and image

A **pixel** is one small colored point in an image. Millions of pixels can show a receipt to a person, but pixels alone do not say which number is the total. Image preprocessing makes the input easier to inspect; it does not create business meaning by itself.

### OCR

**OCR (Optical Character Recognition)**, in everyday terms, reads letters and numbers from an image. It turns the visual shape of “Total 500,000” into text that software can process. OCR may still read the wrong character, and it does not know whether the number is a total, a tax value or a line-item price.

### Bounding Box

A **bounding box** is a rectangle around a piece of content. It answers “where on the page is this word or field?” DocAI represents it as `xmin`, `ymin`, `xmax`, `ymax`. Location matters because the number beside “Total” is more likely to be the total than a number in a product table.

### Field and clause

A **field** is a named value, such as `invoice_date` or `total_amount`. A **clause** is a meaningful contract passage, such as a termination clause. The two domains use different field names; they should not be forced into the same business taxonomy.

### Document type

`DocumentType` tells the system whether the input is an invoice, receipt, contract or unknown document. It lets later validation choose Invoice Risk rules or Contract Risk rules.

## What is structured output?

**Structured output** is information arranged with predictable keys instead of a paragraph written for a human. **JSON (JavaScript Object Notation)** is a common text format for sending that information between systems.

DocAI uses **Pydantic** models to validate the shared envelope [`UnifiedDocumentOutput`](../../src/docai/core/schema.py). It contains the document type, extracted fields, confidence, optional locations, risk flags and execution metadata. Invoice and Contract values can differ inside the envelope.

```text
Track A output ─┐
                ├→ UnifiedDocumentOutput → FastAPI JSON → React types/UI
Track B output ─┘
```

The schema is the bridge between AI code and product code. The frontend mirrors it in [`frontend/src/types/document.ts`](../../frontend/src/types/document.ts), so React does not guess the API shape.

## Why are there two processing tracks?

Track A breaks the work into specialist steps. Track B asks a VLM to combine more of the work. Both can serve Invoice and Contract when their actual capabilities support the input.

```text
Track A: layout → OCR → KIE → schema
Track B: document → VLM → structured response → schema validation
```

The Product uses a chosen engine to process a document. Research compares the two engines using ground truth; comparison is not required for every product request.

## Where is this implemented?

- Schema and configuration: `src/docai/core/`.
- Data loading and preprocessing: `src/docai/data/`.
- AI engines: `src/docai/pipelines/`.
- Backend/API: `src/docai/api/`.
- Browser UI: `frontend/`.
- Risk and evidence: `src/docai/fraud/` and `src/docai/explainability/`.

Most model and API processing methods are currently scaffolds. The important architecture is already explicit: document input becomes a validated contract before it is consumed by risk rules, FastAPI or React.
