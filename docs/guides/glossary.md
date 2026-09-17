# DocAI glossary

These terms are introduced in the concepts path with examples. The short explanations below are a quick reference, not a substitute for the story in [`docs/concepts/`](../concepts/).

| Term | Plain-language meaning | Where it matters |
| --- | --- | --- |
| API | Rules that let two software components communicate. | React sends document requests to FastAPI. |
| REST | A common HTTP style for APIs, using routes and methods such as GET and POST. | Product and research endpoints. |
| JSON | Text representation of structured objects, lists, strings and numbers. | FastAPI responses and the frontend contract. |
| Pydantic | Python library that validates data against declared models. | `UnifiedDocumentOutput` validation. |
| React | UI library for composing browser screens from components. | `frontend/src/`. |
| TypeScript | JavaScript with declared types that catch many shape errors before runtime. | Mirrors the Python API contract. |
| Vite | Frontend development server and build tool. | Runs and bundles the React app. |
| Node.js | Runtime used here for npm, Vite and TypeScript tooling. | It is not DocAI's business backend. |
| Document AI | Software that turns documents into usable, structured information. | The overall product area. |
| OCR | Optical Character Recognition: turns image pixels into readable text. | Track A and visual reading. |
| Layout Detection | Finds and labels regions such as tables or totals. | First Track A stage. |
| Bounding Box | Rectangle describing an item's location as min/max x and y. | Evidence and layout features. |
| KIE | Key Information Extraction: assigns business meaning to text. | Invoice fields and contract clauses. |
| VLM | Vision-Language Model that processes images and language together. | Track B. |
| Multimodal | Using more than one input type, such as an image plus text. | VLM document parsing. |
| Transformer | Model architecture that compares input pieces using context. | LayoutLMv3 and VLMs. |
| Token | Small unit processed by a language model; one word may split into several. | KIE labels and prompts. |
| Embedding | Numeric representation of an item that a model can compare and process. | Text/image representations. |
| Attention | Internal weighting of which context influences a prediction. | Useful diagnostic signal, not perfect proof. |
| Prompt | Instruction sent to a generative model. | Tells Track B what to extract. |
| Structured Output | Result following a predictable schema instead of free text. | JSON returned to the product. |
| Schema | Declared shape, types and constraints for data. | Python/TypeScript contract. |
| Pretrained Model | Model that learned general patterns before this project uses it. | Candidate starting point for Track A/B. |
| Fine-tuning | Adapting a pretrained model to a narrower task. | Future invoice/contract work. |
| Checkpoint | Saved model state used to reproduce inference. | Must be recorded with results. |
| Inference | Using a saved model to process a new document. | Runtime pipeline step. |
| Hallucination | Plausible model output not supported by the source document. | Main Track B reliability risk. |
| Precision | Of predicted items, the fraction that is correct. | Accuracy evaluation. |
| Recall | Of correct items that exist, the fraction the system found. | Measures missed fields/clauses. |
| F1-score | Combined measure balancing precision and recall. | Field/clause comparison. |
| Latency | Time taken to process a request. | Product experience and research. |
| Robustness | Ability to keep working on realistic noisy inputs. | Blur, rotation and contrast tests. |
| Invoice Risk | Transaction-review signals such as arithmetic mismatch. | Invoice Intelligence. |
| Contract Risk | Review signals about clauses or metadata. | Contract Intelligence; not legal advice. |
| Explainability | Evidence that helps a person understand a result. | Boxes, spans and supporting text. |
| Ground Truth | Trusted reference answer used for evaluation. | Required before claiming metrics. |

## Status words

`Implemented` means behavior exists and is supported by checks. `Baseline` means a small working foundation exists. `SCAFFOLD` means an interface or placeholder exists without the full runtime. `PLANNED` means the work has not started. `NOT SELECTED` means a model or technology remains a candidate.
