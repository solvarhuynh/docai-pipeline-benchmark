# Hướng dẫn vận hành và chạy dự án (How-to-Run Guide)

Tài liệu này hướng dẫn chi tiết từng bước để cài đặt, thiết lập môi trường và vận hành hệ thống DocAI Dual-Pipeline Benchmark theo chuẩn kiến trúc `src/ layout` trên máy tính cá nhân hoặc trên hạ tầng đám mây Modal.

---

## 1. Yêu cầu tiên quyết (Prerequisites)

Trước khi bắt đầu, đảm bảo máy tính đã cài đặt các công cụ sau:
- Python 3.10 trở lên.
- Git.
- Docker và Docker Compose (nếu muốn chạy dev container local).
- Tài khoản Modal (đăng ký miễn phí tại https://modal.com để nhận credit GPU miễn phí hàng tháng).

---

## 2. Bước 1: Cài đặt môi trường và Package `docai`

### 2.1. Tạo môi trường ảo Python (Virtual Environment)

Mở terminal tại thư mục gốc của dự án (thư mục đã clone repository):

```bash
# Tạo virtualenv có tên là .venv
python -m venv .venv

# Kích hoạt môi trường ảo trên Windows PowerShell:
.venv\Scripts\Activate.ps1

# Hoặc trên Linux/macOS:
source .venv/bin/activate
```

### 2.2. Cài đặt package ở chế độ phát triển (Editable Install)

Hệ thống được đóng gói theo chuẩn `pyproject.toml`. Cài đặt package `docai` ở chế độ editable để có thể import từ mọi vị trí mà không cần chỉnh sửa `PYTHONPATH`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

Kiểm tra cài đặt thành công:

```bash
python -c "import docai; print('docai version:', docai.__version__)"
python -c "from docai.core.schema import UnifiedDocumentOutput; print('Schema OK')"
```

---

## 3. Bước 2: Chạy kiểm thử tự động (Test Suite)

Dự án trang bị bộ test tự động tại thư mục `tests/`:

```bash
# Chạy toàn bộ test bằng pytest:
pytest

# Hoặc chạy bằng unittest có sẵn trong Python:
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 4. Bước 3: Chạy các CLI Scripts độc lập (`scripts/`)

Người dùng có thể thực thi các tác vụ chính trực tiếp từ dòng lệnh mà không bắt buộc phải mở Jupyter Notebook:

### 4.1. Khảo sát dữ liệu thô (EDA)
```bash
# Khảo sát toàn bộ 4 bộ dữ liệu:
python scripts/run_eda.py --dataset all

# Khảo sát một bộ dữ liệu cụ thể:
python scripts/run_eda.py --dataset mcocr2021
```

### 4.2. Chạy pipeline Track A (Classic Multi-stage)
```bash
python scripts/run_track_a.py --image path/to/invoice.jpg --lang vi
```

### 4.3. Chạy pipeline Track B (VLM-native Single-pass)
```bash
python scripts/run_track_b.py --image path/to/invoice.jpg --type invoice
```

### 4.4. Chạy đối chiếu Benchmark Track A vs Track B
```bash
python scripts/run_benchmark.py --image path/to/invoice.jpg
```

---

## 5. Bước 4: Khảo sát tương tác bằng Jupyter Notebook

Notebook khám phá dữ liệu nằm tại: `notebooks/01-eda.ipynb`.
Toàn bộ logic xử lý trong notebook đều gọi trực tiếp các hàm dùng chung từ package `docai.data.*`:

```bash
jupyter notebook notebooks/01-eda.ipynb
```

Ghi chú về dữ liệu:
- Ở Giai đoạn 1, 4 bộ dữ liệu mcocr2021, CORD, SROIE, CUAD sẽ được tải về các thư mục con tương ứng trong `data/raw/`:
  - `data/raw/mcocr2021/`
  - `data/raw/cord/`
  - `data/raw/sroie/`
  - `data/raw/cuad/`
- Dữ liệu trung gian trong quá trình tiền xử lý được lưu tại `data/interim/`.
- Dữ liệu chuẩn hoá sẵn sàng cho huấn luyện và đánh giá được lưu tại `data/processed/`.

---

## 6. Bước 5: Chạy FastAPI Server cục bộ (Local Dev Server)

FastAPI cung cấp 4 endpoint: `/parse/classic`, `/parse/vlm`, `/compare`, `/explain`.

Hiện tại các route parsing/compare/explain là `SCAFFOLD` và trả HTTP 501; chỉ `/health` có hành vi runtime hoàn chỉnh.

### Cách 1: Chạy trực tiếp bằng Uvicorn

```bash
uvicorn docai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Sau khi server khởi động, mở trình duyệt truy cập:
- Tài liệu OpenAPI Swagger UI: http://localhost:8000/docs
- Kiểm tra trạng thái hệ thống: http://localhost:8000/health

### Cách 2: Chạy thông qua Docker Compose

```bash
docker compose up --build
```

Dịch vụ sẽ tự động cài đặt package `docai` ở chế độ editable và mount thư mục mã nguồn để hot-reload khi có thay đổi code.

Dừng dịch vụ:
```bash
docker compose down
```

---

## 7. Bước 6: Khởi chạy Dashboard trực quan hoá (Plotly Dash)

Dự án sử dụng Plotly Dash làm framework trực quan hoá mặc định (tuyệt đối không dùng Power BI):

```bash
python -m docai.dashboard.app
```

Giao diện dashboard sẽ mở tại `http://localhost:8050`. Hiện tại lệnh chỉ khởi tạo scaffold layout khi Dash đã được cài; callbacks và dữ liệu thật sẽ bổ sung ở phase sau.

---

## 8. Bước 7: Thiết lập tài khoản và kiểm tra GPU trên Modal

### 8.1. Xác thực tài khoản Modal
```bash
modal setup
```

### 8.2. Chạy hàm test billing GPU
```bash
modal run modal_app/deploy.py
```
Kết quả trả về sẽ xác nhận GPU T4 khả dụng và kiểm tra billing thực tế trên trang quản trị của Modal tại https://modal.com.

### 8.3. Triển khai FastAPI lên Modal Web Endpoint (Kế hoạch Giai đoạn 10)
```bash
modal deploy modal_app/deploy.py
```

---

## 9. Bước 8: Theo dõi tiến độ thực hiện

Mọi bước thực hiện, thay đổi kiến trúc và chi phí GPU-giờ đều được ghi lại trong:
`log/progress-log.md`
