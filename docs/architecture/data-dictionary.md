# Data dictionary — DocAI Product + Research

Tài liệu này mô tả các dataset mục tiêu và nguyên tắc mapping vào shared envelope [`src/docai/core/schema.py`](../../src/docai/core/schema.py). Đây là data plan, không phải bằng chứng dữ liệu đã được tải. Hiện `data/raw/`, `data/interim/` và `data/processed/` chưa chứa dataset thật trong task này.

## Dataset và vai trò

- **mcocr2021** — hóa đơn/biên lai Việt Nam chụp bằng camera; polygon + transcription; phục vụ Invoice extraction, OCR/layout và robustness.
- **CORD** — retail receipts; hierarchical JSON có `menu`, `sub_total`, `total`; phục vụ Invoice KIE và đối chiếu.
- **SROIE** — scanned receipts; OCR text boxes và entities `company`, `date`, `address`, `total`; phục vụ Invoice OCR/KIE đối chiếu.
- **CUAD** — hợp đồng pháp lý với SQuAD-style `context`, `qas`, `answers` span; phục vụ Contract Information Extraction, Clause Classification/Detection, Contract Risk Analysis và generalization research.

Quy mô và phân bố cụ thể chỉ được ghi sau EDA trên dữ liệu thật. Các con số danh nghĩa trong nguồn dataset không phải số liệu benchmark của repository.

## Mapping theo domain

### Invoice/Receipt

Các field có thể dùng khi dataset/schema hỗ trợ:

- `seller_name`: mcocr2021 seller; CORD store/name; SROIE `company`.
- `invoice_date`: timestamp/date tương ứng.
- `subtotal_amount`: subtotal khi có dữ liệu phù hợp.
- `tax_amount`: VAT/tax khi có dữ liệu phù hợp.
- `total_amount`: total/total price.
- `line_items`: CORD `menu` hoặc item annotations tương ứng.
- `seller_address`: SROIE `address` khi product schema cần và mapping được chốt.

Tên field trong `fields[]` là dữ liệu domain-specific, không phải các thuộc tính bắt buộc cố định của Pydantic envelope. Không thêm field chỉ vì một dataset khác có field đó.

### Contract

CUAD giữ semantics span/clause, không map vào `seller_name`, `invoice_date`, `total_amount` hay `line_items` chỉ để làm cho hai domain giống nhau. Mapping dự kiến là:

- `document_type = contract`;
- `field_name` là clause category đã được chốt trong taxonomy;
- `field_value` là supporting text span;
- `raw_text` giữ text gốc khi cần;
- `page_number`/`bounding_box` được điền khi có document-to-page alignment;
- metadata contract như parties/effective date được thêm chỉ khi annotation/schema thực tế hỗ trợ.

Các category có thể nghiên cứu gồm governing law, termination, confidentiality, liability, indemnification và dispute resolution. Đây là taxonomy candidate/scaffold, không phải tuyên bố CUAD extraction đã hoàn thành.

## Shared output contract

Hai track đều phải trả `UnifiedDocumentOutput` với:

- `document_type`: `invoice`, `receipt`, `contract` hoặc `unknown`;
- `fields[]`: `field_name`, `field_value`, confidence và optional evidence location;
- `risk_flags[]`: domain risk flags;
- execution/pipeline metadata khi đo được.

Envelope chung giúp FastAPI, Dash và Evaluation không phụ thuộc output tùy tiện của model. Nó không có nghĩa field Invoice và Contract phải giống nhau.

## Data quality và EDA

EDA cần kiểm tra:

- Invoice: ảnh mờ/nghiêng, độ phân giải, polygon, OCR text và phân bố field/line item.
- Contract: độ dài context, span offset, số trang nếu có, overlap/thiếu clause và phân bố taxonomy.
- Mapping: giữ provenance từ annotation gốc đến `field_name`, `field_value`, `raw_text` và evidence.

Thực hiện bằng `notebooks/01-eda.ipynb` hoặc `scripts/run_eda.py` sau khi phase dữ liệu được phê duyệt. Không tạo số liệu giả để điền báo cáo.

## Lưu trữ

```text
data/raw/<dataset>/        # dữ liệu gốc, không sửa trực tiếp
data/interim/              # chuyển đổi/trung gian
data/processed/            # chuẩn hoá cho product/research
```

Dataset license, provenance, split và ground truth phải được ghi kèm trước khi dùng cho Research milestone.
