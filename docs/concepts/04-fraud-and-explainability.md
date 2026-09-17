# What should DocAI flag, and how can a reviewer understand why?

Extraction answers “what did the document say?” Risk and explainability answer two follow-up questions: “what deserves attention?” and “where did this result come from?” They are decision-support layers around both Track A and Track B.

## Why is an extracted value not automatically trustworthy?

Suppose an invoice says subtotal `100`, tax `10` and total `150`. All three values may have been read successfully, but the arithmetic does not agree. Or suppose OCR read a blurry `8` as `B`. A system should expose the inconsistency for review instead of silently treating the output as truth.

The shared output carries `confidence`, `bounding_box`, `raw_text` and `risk_flags`. Confidence is the model's or pipeline's estimate of certainty; it is not a guarantee of correctness. A low-confidence result deserves attention, but a high-confidence hallucination or systematic error can still be wrong.

## Why must Invoice Risk and Contract Risk stay separate?

**Invoice Risk** concerns signals such as arithmetic mismatch, missing important fields, inconsistent amounts or unusually low extraction confidence. These are clues for checking a transaction; they are not proof of fraud.

**Contract Risk** concerns review-worthy language or missing information, such as an absent termination clause, an unusual renewal condition or inconsistent metadata. A missing clause is not fraud. Contract Risk supports a reviewer and does not decide whether an agreement is legal, enforceable or appropriate. It does not replace a lawyer.

The rule layer lives in [`src/docai/fraud/`](../../src/docai/fraud/). Its name is historical; the behavior is domain-specific risk checking.

## How does a rule-based risk flag work?

A **rule-based** check is an explicit test that a person can read. For example:

```text
if subtotal + tax does not equal total:
    create an invoice arithmetic risk flag
```

The result identifies a rule, severity, description and optional target field. A flag asks someone to investigate. It does not claim that the document is fraudulent or that a contract is invalid.

## What counts as useful evidence?

For an invoice, a **bounding box** can highlight the source area for `total_amount`; the reviewer can compare the highlighted number with the printed label. For a contract, evidence is usually a text span, page number, clause heading or supporting passage. Evidence should answer “which part of the document supports this field or flag?”

The product UI may eventually show:

```text
field/clause → value → confidence → source location → risk flag
```

If the pipeline cannot provide evidence, the UI should say so. It must not draw a convincing highlight that was not produced by the model or a verified post-processing step.

## Is attention a perfect explanation?

**Attention** is an internal mechanism that weights context while a Transformer makes a prediction. An attention map or **heatmap** can be useful for investigation: brighter areas may show which tokens or image regions received more weight. But attention is not automatically causal evidence, and a pretty heatmap does not prove that the model relied on the correct text.

Other methods such as visual grounding or gradient-based overlays may also be evaluated. In this repository, [`src/docai/explainability/`](../../src/docai/explainability/) is a scaffold. Explainability is complete only when a real model produces evidence and that evidence is checked against suitable annotations or supporting text.

## Where does this layer fit?

```text
Track A or Track B
        ↓
UnifiedDocumentOutput
        ├─ fields/clauses + confidence + evidence
        └─ domain risk rules
                    ↓
            reviewer-facing result
```

This separation keeps extraction, risk policy and user explanation understandable and testable. It also prevents the frontend from inventing model logic.
