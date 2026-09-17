# Explanation style — how technical concepts should be taught

These rules keep the technical documentation accurate without assuming that the reader already knows AI/ML/DL.

## Tell the story before listing terms

Use this order:

```text
What is the product trying to do?
  ↓
What practical problem gets in the way?
  ↓
Why is the simple approach insufficient?
  ↓
What technique addresses that problem?
  ↓
What is the everyday intuition?
  ↓
Where is it in DocAI?
  ↓
Where does the output go next?
```

Before moving on, answer “so what?” for the reader.

## Explain the first occurrence of a technical term

Keep the English term, then give a plain-language explanation and a document example. For example:

> **OCR (Optical Character Recognition)** is the step that turns letters in an image into text. When a phone camera sees “Total: 500,000”, OCR gives later software a string to work with. OCR does not, by itself, know that the number is the invoice total.

Apply the same treatment to KIE, VLM, Transformer, token, embedding, attention, bounding box, pretrained model, fine-tuning, inference, schema, Pydantic, API, REST, JSON, Precision, Recall, F1-score, latency and structured output when they first appear.

Do not define a difficult term with another unexplained difficult term. Start with a familiar analogy, then add the formal definition.

## Use both product domains

Use concrete Invoice and Contract examples. Explain when a concept is shared and when it is domain-specific:

- Invoice: fields such as vendor, date, tax and total; numbers and tables matter.
- Contract: metadata and clause spans such as termination or governing law; long context and meaning matter.

Do not pretend that one field list or one model must fit both domains.

## Explain code and flow, not only theory

Every technical section should identify:

- the relevant file under `src/docai/` or `frontend/`;
- the input and output;
- whether it belongs to Track A, Track B, Product Engineering or Research;
- how the output reaches `UnifiedDocumentOutput`, FastAPI and React;
- what metric or test would validate the claim.

## Put intuition before formulas

For a metric such as Recall, first explain the practical question: “Of all the real clauses that should have been found, how many did the system find?” Then define TP and FN with an example, and only then show the formula.

Never call a metric good or bad without naming the dataset, domain, field, track and measurement conditions.

## Be honest about status

- **Implemented/Baseline**: code and tests/runtime evidence support the claim.
- **Scaffold**: interface or page exists, but the real behavior is incomplete.
- **Planned**: on the roadmap, not yet started.
- **Not selected**: a model or tool is still a candidate.

Attention maps are not automatically explanations. Risk flags are not legal conclusions. A mock result is not a benchmark.

## Keep the structure readable

Use question-shaped headings where they help the reader understand the purpose, such as “Why can OCR read words but not identify the total?” Avoid a page that is only a glossary. Do not add a file for every keyword.
