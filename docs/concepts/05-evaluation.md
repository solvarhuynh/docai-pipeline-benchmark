# How do we know whether Track A or Track B is actually doing well?

An architecture diagram cannot tell us which engine is better. We need documents with a known correct answer, a repeatable protocol and measurements that match the question we care about. This is the role of the Research Lab.

## What is the evaluation unit?

Evaluation must state the domain and level being measured. A result for invoice `total_amount` is not automatically a result for all invoice fields. A contract clause result is not automatically comparable with an invoice field. Every report should identify:

- domain: Invoice or Contract;
- dataset and split, including the ground truth source;
- track and model/checkpoint;
- field or clause taxonomy;
- preprocessing and pass/fail rules.

**Ground truth** is the trusted reference answer against which a prediction is compared. Without it, we can inspect examples, but we cannot make a defensible accuracy claim.

## Does the system find the things it predicts correctly?

Start with a simple question: of the values the system returned, how many were correct? **Precision** answers that question. If the system predicts 10 invoice fields and 8 match the ground truth, precision is `8/10 = 0.80`.

Now ask the opposite: of all values that really existed, how many did the system find? **Recall** answers that question. If the ground truth has 10 fields and the system found 8, recall is `8/10 = 0.80`. Missing a termination clause is a recall problem for Contract Intelligence.

For field-level matching, a **true positive (TP)** is a correctly extracted field, a **false positive (FP)** is an incorrect or unsupported field, and a **false negative (FN)** is a field that should have been extracted but was missed:

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
```

**F1-score** combines precision and recall using their harmonic mean:

```text
F1 = 2 × Precision × Recall / (Precision + Recall)
```

It is useful when both invented values and missed values matter. An F1 such as `0.82` has no meaning by itself: the report must say which field or clause, domain, dataset, split and track produced it.

## How quickly and cheaply does it work?

**Latency** is the time from request to response. Report it per page or document, and state whether model loading and warm-up are included. A faster engine may be preferable for an interactive Invoice Workspace, while a slower engine may still be useful for an offline contract review.

**Cost** is the resource price of processing the workload. It can include GPU time, hosted API charges, storage or other measured components. A cost comparison must state hardware, model, page count, batch size, input size, price source and formula. An estimate is not an actual measurement.

## What happens when the input is poor?

**Robustness** means how well performance holds when inputs change in realistic ways. Compare clean documents with controlled variants such as blur, rotation, low contrast or mild occlusion. A common summary is:

```text
ΔF1 = F1 on clean input - F1 on noisy input
```

The same documents, perturbation protocol and acceptance rules should be used for both tracks. A degradation result should identify whether OCR, layout, KIE or VLM parsing caused the loss when that diagnosis is possible.

## How do we compare disagreement and evidence?

When both tracks return `UnifiedDocumentOutput`, we can compare field values, missing fields, confidence and evidence locations. Agreement is useful for triage, but agreement does not prove correctness if both models make the same mistake. Disagreement is a sample for human review, not a winner declaration.

The evaluation helpers are under [`src/docai/evaluation/`](../../src/docai/evaluation/), and the report templates are under [`docs/reports/`](../reports/). They remain `PLANNED` or `SCAFFOLD` until real inference and ground truth are available. This task deliberately adds no fake metrics, dataset download or benchmark claim.
