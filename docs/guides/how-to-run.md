# Hướng dẫn vận hành và chạy dự án (How-to-Run Guide)

Tài liệu này hướng dẫn chi tiết từng bước để cài đặt, thiết lập môi trường và vận hành hệ thống DocAI Dual-Pipeline Benchmark từ đầu trên máy tính cá nhân hoặc trên hạ tầng đám mây Modal.

---

## 1. Yêu cầu tiên quyết (Prerequisites)

Trước khi bắt đầu, đảm bảo máy tính đã cài đặt các công cụ sau:
- Python 3.10 trở lên.
- Git.
- Docker và Docker Compose (nếu muốn chạy dev container local).
- Tài khoản Modal (đăng ký miễn phí tại https://modal.com để nhận credit GPU miễn phí hàng tháng).

---

## 2. Bước 1: Cài đặt môi trường cục bộ (Local Environment Setup)

### 2.1. Tạo môi trường ảo Python (Virtual Environment)

Mở terminal tại thư mục gốc của dự án (`d:/2-personal-project` hoặc thư mục đã clone repo) và thực hiện:

```bash
# Tạo virtualenv có tên là .venv
python -m venv .venv

# Kích hoạt môi trường ảo trên Windows PowerShell:
.venv\Scripts\Activate.ps1

# Hoặc trên Linux/macOS:
source .venv/bin/activate
```

### 2.2. Cài đặt các thư viện phụ thuộc

Chạy lệnh cài đặt toàn bộ thư viện được liệt kê trong `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Các thư viện chính bao gồm: `fastapi`, `uvicorn`, `pydantic`, `ultralytics`, `paddleocr`, `transformers`, `modal`, `torch`, `pillow`, `opencv-python-headless`.

---

## 3. Bước 2: Thiết lập tài khoản và kiểm tra GPU trên Modal

Hệ thống sử dụng Modal Serverless GPU để chạy fine-tune LayoutLMv3 và inference VLM mà không cần trang bị GPU rời cục bộ.

### 3.1. Xác thực tài khoản Modal

Chạy lệnh xác thực qua trình duyệt web:

```bash
modal setup
```

Lệnh này sẽ mở trình duyệt để bạn đăng nhập và tự động lưu token xác thực vào hệ thống.

### 3.2. Chạy hàm test billing GPU

Trong file `modal_app/deploy.py`, hàm `test_gpu_billing` đã được viết sẵn để kiểm tra kết nối GPU T4 thực tế trên Modal. Bạn có thể chạy ngay lệnh sau:

```bash
modal run modal_app/deploy.py
```

Kết quả trả về sẽ hiển thị thông tin lệnh `nvidia-smi` từ container Modal, xác nhận GPU T4 đã sẵn sàng và mức chi phí (billing) được hiển thị trên trang dashboard của Modal tại https://modal.com.

---

## 4. Bước 3: Khảo sát dữ liệu bằng Jupyter Notebook

Notebook khảo sát sơ bộ nằm tại: `notebooks/01-eda.ipynb`.

Khởi động Jupyter Lab hoặc Notebook:

```bash
jupyter notebook notebooks/01-eda.ipynb
```

Ghi chú:
- Ở Giai đoạn 1 (Khảo sát & chuẩn bị dữ liệu), 4 bộ dữ liệu mcocr2021, CORD, SROIE, CUAD sẽ được tải về các thư mục con tương ứng trong `data/raw/`:
  - `data/raw/mcocr2021/`
  - `data/raw/cord/`
  - `data/raw/sroie/`
  - `data/raw/cuad/`
- Chạy các cell trong notebook để quan sát ảnh mẫu, kích thước và cấu trúc nhãn gốc.

---

## 5. Bước 4: Vận hành các thành phần Pipeline

Ghi chú về trạng thái: Tại thời điểm hiện tại (hoàn thành Scaffold), các file mã nguồn đang ở dạng khung stub có định nghĩa hàm và docstring TODO đầy đủ. Khi các giai đoạn logic tương ứng được hoàn thiện, các lệnh sau sẽ thực thi đầy đủ logic nghiệp vụ:

### 5.1. Track A (Classic Pipeline)

- **Chạy Layout Detection (Giai đoạn 3)**:
  File: `track_a_classic/layout_detection.py`
  Dùng để phân vùng các khối trên hóa đơn:
  ```bash
  python -m track_a_classic.layout_detection
  ```

- **Chạy OCR Extraction (Giai đoạn 3)**:
  File: `track_a_classic/ocr_extraction.py`
  Dùng để đọc ký tự và ghép tọa độ bounding box thành JSON trung gian:
  ```bash
  python -m track_a_classic.ocr_extraction
  ```

- **Chạy KIE LayoutLMv3 (Giai đoạn 4)**:
  File: `track_a_classic/kie_layoutlmv3.py`
  Dùng để fine-tune trên Modal GPU hoặc chạy inference trích xuất thực thể:
  ```bash
  python -m track_a_classic.kie_layoutlmv3
  ```

### 5.2. Track B (VLM-native Pipeline)

- **Chạy VLM Parser (Giai đoạn 5)**:
  File: `track_b_vlm/vlm_parser.py`
  Dùng để trích xuất thực thể trực tiếp từ ảnh thông qua PaddleOCR-VL / dots.ocr:
  ```bash
  python -m track_b_vlm.vlm_parser
  ```

### 5.3. Lớp Fraud/Risk Engine và Explainability

- **Kiểm tra luật gian lận và rủi ro điều khoản (Giai đoạn 7)**:
  File: `shared/fraud_rules.py`
- **Trích xuất heatmap giải thích (Giai đoạn 8)**:
  File: `shared/explainability.py`

---

## 6. Bước 5: Chạy FastAPI Server cục bộ (Local Dev Server)

FastAPI cung cấp 4 endpoint: `/parse/classic`, `/parse/vlm`, `/compare`, `/explain`.

### Cách 1: Chạy trực tiếp bằng Uvicorn

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Sau khi server khởi động, mở trình duyệt truy cập:
- Tài liệu OpenAPI Swagger UI: http://localhost:8000/docs
- Kiểm tra hệ thống: http://localhost:8000/health

### Cách 2: Chạy thông qua Docker Compose

Không cần cài đặt các thư viện Python lên máy host, chạy trực tiếp:

```bash
docker compose up --build
```

Dịch vụ sẽ tự động build image dựa trên Python 3.10-slim, mount thư mục code hiện tại và mở cổng 8000. Mọi thay đổi trong code sẽ được hot-reload ngay lập tức.

Dừng dịch vụ:

```bash
docker compose down
```

---

## 7. Bước 6: Triển khai lên Modal Web App (Kế hoạch Giai đoạn 10)

Khi hoàn thành logic của toàn bộ các giai đoạn, service sẽ được deploy trực tiếp lên serverless web endpoint của Modal thông qua file `modal_app/deploy.py`:

```bash
modal deploy modal_app/deploy.py
```

Modal sẽ trả về một URL công khai (ví dụ: `https://<ten-user>--docai-pipeline-benchmark-fastapi-app.modal.run`) cho phép gọi API từ bất kỳ đâu mà không cần quản lý máy chủ.

---

## 8. Bước 7: Theo dõi tiến độ thực hiện

Mọi bước thực hiện, đánh giá và chi phí GPU-giờ đều được ghi lại trong:
`log/progress-log.md`

Trước khi bắt đầu bất kỳ phiên làm việc mới nào, vui lòng đọc bảng tiến độ trong file này để nắm bắt trạng thái hiện tại và việc tiếp theo cần làm.
