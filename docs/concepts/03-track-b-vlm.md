# Why can Track B return a document result in one model call?

Track B is DocAI's VLM-native processing engine. **VLM (Vision-Language Model)** means a model that can work with both visual input and language. Instead of exposing layout, OCR and KIE as separate product stages, Track B presents a document image and an instruction to one multimodal model and asks for a structured response.

```text
Invoice or contract image
        +
Structured prompt: what to extract and how to format it
        ↓
VLM inference
        ↓
Candidate structured response
        ↓
Schema validation and domain risk checks
        ↓
UnifiedDocumentOutput
```

The word “single-pass” describes the product-facing model flow. It does not mean the system has no validation, parsing or error handling around the model.

## Why is this useful?

Consider a legal reviewer reading a contract. They can look at the page, connect a heading to its paragraph and fill in a report without separately drawing every region and transcribing every word. A VLM attempts to learn a similar combined visual-and-language task.

This can reduce hand-built stage boundaries and may handle unusual layouts more flexibly. It can also be more expensive, slower or less predictable. Track B is therefore an alternative engine, not an automatic replacement for Track A.

The repository currently contains a prompt/parser interface in [`vlm_parser.py`](../../src/docai/pipelines/track_b/vlm_parser.py). PaddleOCR-VL and dots.ocr are candidates, not selected production models, and real inference is not enabled in this architecture task.

## What happens inside a VLM?

A VLM usually combines:

1. A **vision encoder**, which turns image patches into numeric visual representations.
2. A language model, which processes instructions and text-like tokens.
3. A connector or shared representation that allows visual information to influence the generated answer.

A **multimodal** input contains more than one kind of information, here an image and language. A **token** is a small unit of text or model input. An **embedding** is a list of numbers representing an item in a form the model can compare and process. These representations let the model relate a number near `Total` to the meaning requested by the prompt.

The exact internal architecture depends on the selected checkpoint. The project should document that exact model only after it is chosen and tested.

## Why does the prompt matter?

A **prompt** is the instruction sent to the model. A useful prompt states the document type, requested fields or clauses, missing-value behavior and output format. A **structured prompt** makes those requirements explicit rather than asking vaguely, “What is in this document?”

For example, an invoice instruction might request `seller_name`, `invoice_date`, `tax_amount` and `total_amount`. A contract instruction might request renewal, termination and payment clauses with page or text evidence. The domain changes the questions; the API contract remains shared.

## Why ask for structured output?

**Structured Output** means the response follows a predictable shape such as JSON instead of a paragraph. **JSON** is a text format for objects, arrays, strings and numbers that software can exchange. In DocAI, the candidate JSON is parsed and checked against the Pydantic representation of `UnifiedDocumentOutput`.

**Schema validation** checks whether required keys have the right types and allowed ranges. For example, confidence must be between `0.0` and `1.0`, and a bounding box must not have its minimum coordinate larger than its maximum. Validation catches malformed responses; it cannot prove that the model extracted the correct value.

## What is hallucination and why is it dangerous here?

**Hallucination** is when a generative model produces a plausible-looking statement that is not supported by the document. If an invoice does not show a tax number, the model might still invent one. If a contract has no renewal clause, it might write a likely-sounding clause.

DocAI must treat generated values as candidates for verification. Prompts can require “not found” values, schema validation can reject malformed data, and evidence fields can let a reviewer inspect the source. None of those controls guarantees factual correctness. Product UI must make missing evidence and uncertainty visible.

## Is Track B a generalist while Track A is a specialist?

This is a useful research contrast:

- A **specialist** is like a person trained for one profession. Track A can combine several focused models and domain-specific mappings.
- A **generalist** has broader capabilities and can switch tasks when given clear instructions. Track B can use different prompts and schemas for invoices and contracts.

“One VLM” does not mean “one universal capability.” It still needs appropriate prompts, examples, output validation and domain evaluation. Conversely, “Track A” does not mean “one model”; it is a pipeline boundary.

## How does Track B connect to the rest of DocAI?

The VLM response is not returned directly to the browser. The backend parses it, validates it, applies the correct invoice or contract risk rules and converts it to `UnifiedDocumentOutput`. FastAPI serializes that output as JSON, and the React frontend renders it using TypeScript interfaces.

Research compares Track A and Track B only with the same workload and suitable ground truth. A convenient one-pass flow is not evidence that Track B is more accurate, cheaper or more robust. Those claims belong in the evaluation protocol.
